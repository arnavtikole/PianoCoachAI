from collections import defaultdict
from comparison.engine import ComparisonReport


def score_staff_label(staff: int) -> str:
    """Describe the written staff without guessing the player's hand."""

    if staff == 1:
        return "upper staff"

    if staff == 2:
        return "lower staff"

    return f"staff {staff}"


def build_measure_summary(report: ComparisonReport) -> dict:
    measures = defaultdict(lambda: {
        "correct": 0,
        "wrong_note": 0,
        "wrong_octave": 0,
        "missed": 0,
        "extra": 0,
        "on_time": 0,
        "early": 0,
        "late": 0,
        "notes": []
    })

    extra_notes = []

    for (expected, played), note_result, timing_result in zip(
        report.aligned_notes,
        report.note_results,
        report.timing_results
    ):
        if expected is not None:
            measure = expected.measure

            measures[measure][note_result]+=1
            measures[measure][timing_result.result]+=1

            measures[measure]["notes"].append({
                "beat": expected.beat,
                "staff": expected.staff,
                "staff_label": score_staff_label(expected.staff),
                "expected": (
                    f"{expected.pitch}{expected.octave}"
                ),
                "played": (
                    f"{played.pitch}{played.octave}"
                    if played is not None
                    else None
                ),
                "note_result": note_result,
                "timing_result": timing_result.result,
                "timing_error_seconds": timing_result.error
            })

        elif played is not None:
            extra_notes.append({
                "beat": played.beat,
                "played": f"{played.pitch}{played.octave}",
                "timing_result": timing_result.result
            })
    result = dict(sorted(measures.items()))

    if extra_notes:
        result["extra_notes"] = extra_notes
    return result
