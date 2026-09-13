from .models import Score

def get_all_notes(score: Score):
    notes = []
    for measure in score.measures:
        for note in measure.notes:
            if not note.is_rest:
                notes.append(note)

    return notes