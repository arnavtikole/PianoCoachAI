from dataclasses import dataclass
from parser.models import Note

ON_TIME = "on_time"
EARLY = "early"
LATE = "late"
MISSED = "missed"
EXTRA = "extra"
TIMING_TOLERANCE = 0.10

@dataclass
class TimingComparison:
    result: str
    error: float|None

def compare_timing(expected_note: Note|None,played_note: Note|None,) -> TimingComparison:

    if expected_note is None:
        return TimingComparison(result=EXTRA,error=None,)

    if played_note is None:
        return TimingComparison(result=MISSED,error=None,)

    error = round(played_note.start_time - expected_note.start_time,2,)

    if abs(error)<=TIMING_TOLERANCE:
        return TimingComparison(result=ON_TIME,error=error,)

    if error>0:
        return TimingComparison(result=LATE,error=error,)

    return TimingComparison(result=EARLY,error=error,)

def compare_timings(aligned_notes: list[tuple[Note|None, Note|None]],) -> list[TimingComparison]:

    results = []

    for expected_note, played_note in aligned_notes:
        results.append(compare_timing(expected_note,played_note,))

    return results
