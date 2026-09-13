from .models import Measure
from .parse_notes import parse_note


def get_measure_number(measure_element):
    number = measure_element.get("number")

    if number is None:
        return 0

    return int(number)


def get_time_signature(measure_element):
    attributes = measure_element.find("attributes")

    if attributes is None:
        return None, None

    time = attributes.find("time")

    if time is None:
        return None, None

    beats = time.find("beats")
    beat_type = time.find("beat-type")

    if beats is None or beat_type is None:
        return None, None

    return int(beats.text), int(beat_type.text)


def get_key_signature(measure_element):
    attributes = measure_element.find("attributes")

    if attributes is None:
        return None

    key = attributes.find("key")

    if key is None:
        return None

    fifths = key.find("fifths")

    if fifths is None:
        return None

    return int(fifths.text)


def get_divisions(measure_element):
    attributes = measure_element.find("attributes")

    if attributes is None:
        return None

    divisions = attributes.find("divisions")

    if divisions is None:
        return None

    return int(divisions.text)


def _duration_in_beats(element, divisions):

    duration = element.find("duration")

    if duration is None or divisions in (None, 0):
        return 0.0

    return float(duration.text) / divisions


def parse_measure(measure_element, state):
    measure_number = get_measure_number(measure_element)

    beats_per_measure, beat_unit = get_time_signature(measure_element)

    if beats_per_measure is not None:
        state["beats_per_measure"] = beats_per_measure
        state["beat_unit"] = beat_unit
    else:
        beats_per_measure = state["beats_per_measure"]
        beat_unit = state["beat_unit"]

    key_sig = get_key_signature(measure_element)

    if key_sig is not None:
        state["key_sig"] = key_sig
    else:
        key_sig = state["key_sig"]

    divisions = get_divisions(measure_element)

    if divisions is not None:
        state["divisions"] = divisions
    else:
        divisions = state["divisions"]

    notes = []

    measure_start = state["current_beat"]
    cursor = measure_start
    furthest_cursor = cursor
    chord_start = None

    for element in measure_element:
        tag = element.tag.rsplit("}", 1)[-1]

        if tag == "backup":
            cursor -= _duration_in_beats(element, divisions)
            chord_start = None
            continue

        if tag == "forward":
            cursor += _duration_in_beats(element, divisions)
            furthest_cursor = max(furthest_cursor, cursor)
            chord_start = None
            continue

        if tag != "note":
            continue

        note_start = chord_start if element.find("chord") is not None else cursor
        beat_in_measure = note_start - measure_start + 1
        note = parse_note(element,measure_number,beat_in_measure,absolute_beat=note_start,)
        notes.append(note)

        if element.find("chord") is None:
            chord_start = note_start
            cursor += _duration_in_beats(element, divisions)
            furthest_cursor = max(furthest_cursor, cursor)

    state["current_beat"] = furthest_cursor
    
    return Measure(
        number=measure_number,
        notes=notes,
        beats_per_measure=beats_per_measure,
        beat_unit=beat_unit,
        key_sig=key_sig
    )

