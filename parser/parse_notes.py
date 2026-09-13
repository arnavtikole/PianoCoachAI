import xml.etree.ElementTree as ET

from .models import Note

NOTE_TO_SEMITONE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11
}

def get_duration(note_element):
    duration = note_element.find("duration")

    if duration is None:
        return 0.0

    return float(duration.text)

def get_pitch(note_element):
    pitch = note_element.find("pitch")

    if pitch is None:
        return None

    step = pitch.find("step")

    if step is None:
        return None

    return step.text

def get_octave(note_element):
    pitch = note_element.find("pitch")

    if pitch is None:
        return None

    octave = pitch.find("octave")

    if octave is None:
        return None

    return int(octave.text)

def get_staff(note_element):
    staff = note_element.find("staff")

    if staff is None:
        return 1

    return int(staff.text)

def get_voice(note_element):
    voice = note_element.find("voice")

    if voice is None:
        return None

    return int(voice.text)

def is_rest(note_element):
    return note_element.find("rest") is not None

def is_chord(note_element):
    return note_element.find("chord") is not None

def get_accidental(note_element):
    pitch = note_element.find("pitch")

    if pitch is None:
        return None

    alter = pitch.find("alter")

    if alter is None:
        return None

    value = int(alter.text)

    if value == 2:
        return "double_sharp"

    if value == 1:
        return "sharp"

    if value == 0:
        return "natural"

    if value == -1:
        return "flat"

    if value == -2:
        return "double_flat"

    return None

def is_tie_start(note_element):
    notations = note_element.find("notations")

    if notations is None:
        return False

    for tied in notations.findall("tied"):
        if tied.get("type") == "start":
            return True

    return False

def is_tie_stop(note_element):
    notations = note_element.find("notations")

    if notations is None:
        return False

    for tied in notations.findall("tied"):
        if tied.get("type") == "stop":
            return True

    return False

def get_midi_number(note_element):
    pitch = get_pitch(note_element)
    octave = get_octave(note_element)
    accidental = get_accidental(note_element)

    if pitch is None or octave is None:
        return None

    semitone = NOTE_TO_SEMITONE.get(pitch)

    if semitone is None:
        return None

    if accidental == "double_sharp":
        semitone += 2
    elif accidental == "sharp":
        semitone += 1
    elif accidental == "flat":
        semitone -= 1
    elif accidental == "double_flat":
        semitone -= 2

    return (octave + 1) * 12 + semitone

def parse_note(note_element, measure_number, beat, absolute_beat=None):

    return Note(
        pitch=get_pitch(note_element),
        octave=get_octave(note_element),
        midi_number=get_midi_number(note_element),

        duration=get_duration(note_element),

        measure=measure_number,
        beat=beat,

        staff=get_staff(note_element),
        voice=get_voice(note_element),

        is_rest=is_rest(note_element),
        is_chord=is_chord(note_element),

        accidental=get_accidental(note_element),

        tie_start=is_tie_start(note_element),
        tie_stop=is_tie_stop(note_element),

        dynamic=None,
        articulation=None,
        absolute_beat=absolute_beat,
    )





