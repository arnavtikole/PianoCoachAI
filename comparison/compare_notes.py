from parser.models import Note

CORRECT = "correct"
WRONG_OCTAVE = "wrong_octave"
WRONG_NOTE = "wrong_note"
MISSED = "missed"
EXTRA = "extra"


def compare_note(expected_note: Note|None,played_note: Note|None,) -> str:
    if expected_note is None:
        return EXTRA

    if played_note is None:
        return MISSED

    if expected_note.midi_number==played_note.midi_number:
        return CORRECT

    difference = abs(expected_note.midi_number-played_note.midi_number)

    if difference%12==0:
        return WRONG_OCTAVE

    return WRONG_NOTE


def compare_notes(aligned_notes: list[tuple[Note|None, Note|None]],) -> list[str]:
    results = []

    for expected_note, played_note in aligned_notes:
        results.append(compare_note(expected_note, played_note))

    return results