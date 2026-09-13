from .transcribe_audio import transcribe_audio
from .parse_notes import parse_notes
from .timing import calculate_note_intervals,estimate_tempo

def run_audio_pipeline(audio_file):
    note_events = transcribe_audio(audio_file)
    notes = parse_notes(note_events)
    if notes:
        first_start_time = notes[0].start_time
        for note in notes:
            note.start_time -= first_start_time

    intervals = calculate_note_intervals(notes)
    tempo = estimate_tempo(intervals)

    return notes,tempo

