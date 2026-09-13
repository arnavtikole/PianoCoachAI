from dataclasses import dataclass

from comparison.compare_notes import CORRECT
from comparison.compare_timing import ON_TIME
from comparison.compare_dynamics import CORRECT as DYNAMIC_CORRECT

PITCH_WEIGHT = 0.5
TIMING_WEIGHT = 0.3
DYNAMIC_WEIGHT = 0.2

@dataclass
class OverallComparison:
    pitch_score: float
    timing_score: float
    dynamics_score: float
    overall_score: float

def calculate_pitch_score(note_results: list[str],) -> float:

    if not note_results:
        return 0.0

    correct = note_results.count(CORRECT)

    return (correct/len(note_results))*100


def calculate_timing_score(timing_results,) -> float:

    if not timing_results:
        return 0.0

    correct = sum(
        1
        for result in timing_results
        if result.result==ON_TIME
    )

    return (correct/len(timing_results))*100


def calculate_dynamic_score(dynamic_results,) -> float:

    if not dynamic_results:
        return 0.0

    correct = sum(
        1
        for result in dynamic_results
        if result.result == DYNAMIC_CORRECT
    )

    return (correct/len(dynamic_results))*100


def compare_overall(note_results,timing_results,dynamic_results,) -> OverallComparison:

    pitch_score = calculate_pitch_score(note_results)

    timing_score = calculate_timing_score(timing_results)

    dynamic_score = calculate_dynamic_score(dynamic_results)

    overall_score = (pitch_score*PITCH_WEIGHT + timing_score*TIMING_WEIGHT + dynamic_score*DYNAMIC_WEIGHT)

    return OverallComparison(
        pitch_score=pitch_score,
        timing_score=timing_score,
        dynamics_score=dynamic_score,
        overall_score=overall_score,
    )