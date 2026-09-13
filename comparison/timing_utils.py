def assign_score_beat_times(notes):

    for note in notes:
        score_beat = (
            note.absolute_beat
            if note.absolute_beat is not None
            else note.beat
        )
        note.start_time = score_beat - 1


def assign_start_times(notes, tempo):
    if tempo<=0:
        return
    seconds_per_beat = 60/tempo
    for note in notes:
        score_beat = (
            note.absolute_beat
            if note.absolute_beat is not None
            else note.beat
        )
        note.start_time = (score_beat-1)*seconds_per_beat

