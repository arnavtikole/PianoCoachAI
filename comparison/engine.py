from parser.models import Note
from dataclasses import dataclass
from comparison.align_notes import align_notes
from comparison.compare_notes import compare_notes
from comparison.compare_timing import compare_timings
from comparison.compare_dynamics import compare_dynamic
from comparison.compare_overall import compare_overall
from comparison.timing_alignment import estimate_timing_transform

@dataclass
class ComparisonReport:
    aligned_notes: list
    note_results: list
    timing_results: list
    dynamic_results: list
    overall_result: object

def run_comparison(expected_notes: list[Note],played_notes: list[Note],) -> ComparisonReport:

    initial_alignment = align_notes(expected_notes,played_notes,)

    timing_transform = estimate_timing_transform(initial_alignment)

    aligned = align_notes(
        expected_notes,
        played_notes,
        time_scale=timing_transform.scale,
        time_offset=timing_transform.offset,
    )

    note_results = compare_notes(aligned)

    timing_results = compare_timings(aligned)

    dynamic_results = []

    for expected, played in aligned:
        expected_dynamic = (
            expected.dynamic
            if expected
            else None
        )

        played_dynamic = (
            played.dynamic
            if played
            else None
        )

        dynamic_results.append(compare_dynamic(expected_dynamic,played_dynamic,))

    overall_result = compare_overall(note_results,timing_results,dynamic_results,)

    return ComparisonReport(
        aligned_notes=aligned,
        note_results=note_results,
        timing_results=timing_results,
        dynamic_results=dynamic_results,
        overall_result=overall_result,
    )

