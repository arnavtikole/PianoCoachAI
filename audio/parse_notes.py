from parser.models import Note

NOTE_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B"
]

def midi_to_pitch(midi_number):
    pitch = NOTE_NAMES[midi_number%12]
    octave = (midi_number//12)-1

    return pitch, octave

def parse_notes(note_events):
    notes = []

    for event in note_events:
        start_time,end_time,midi_number,amplitude,pitch_bends = event
        pitch, octave = midi_to_pitch(midi_number)
        note = Note(
            pitch=pitch,
            octave=octave,
            midi_number=midi_number,
            duration=end_time - start_time,
            start_time=start_time,
            measure=0,
            beat=0,
            staff=0,
            voice=0,
        )
        notes.append(note)

    notes.sort(key=lambda note: note.start_time)
    return notes
