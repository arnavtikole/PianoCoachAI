
from dataclasses import dataclass
from statistics import median

from parser.models import Note


MIN_ANCHOR_COUNT = 3
MIN_SCALE_SECONDS_PER_BEAT = 0.1
MAX_SCALE_SECONDS_PER_BEAT = 5.0
OUTLIER_FLOOR_SECONDS = 0.10


@dataclass(frozen=True)
class TimingTransform:

    scale: float = 1.0
    offset: float = 0.0
    anchor_count: int = 0


def _correct_pitch_anchors(aligned_notes: list[tuple[Note | None, Note | None]],) -> list[tuple[float, float]]:

    played_by_expected_time: dict[float, list[float]] = {}

    for expected, played in aligned_notes:
        if (
            expected is None
            or played is None
            or expected.start_time is None
            or played.start_time is None
            or expected.midi_number is None
            or played.midi_number is None
            or expected.midi_number != played.midi_number
        ):
            continue

        played_by_expected_time.setdefault(expected.start_time, []).append(played.start_time)

    return [
        (expected_time, median(played_times))
        for expected_time, played_times in sorted(played_by_expected_time.items())
    ]


def _median_slope(anchors: list[tuple[float, float]]) -> float | None:
    slopes = []

    for left_index, (left_expected, left_played) in enumerate(anchors):
        for right_expected, right_played in anchors[left_index + 1:]:
            expected_gap = right_expected - left_expected

            if expected_gap <= 0:
                continue

            slope = (right_played - left_played) / expected_gap

            if MIN_SCALE_SECONDS_PER_BEAT <= slope <= MAX_SCALE_SECONDS_PER_BEAT:
                slopes.append(slope)

    return median(slopes) if slopes else None


def estimate_timing_transform(aligned_notes: list[tuple[Note | None, Note | None]],) -> TimingTransform:

    anchors = _correct_pitch_anchors(aligned_notes)

    if len(anchors) < MIN_ANCHOR_COUNT:
        return TimingTransform(anchor_count=len(anchors))

    scale = _median_slope(anchors)

    if scale is None:
        return TimingTransform(anchor_count=len(anchors))

    offset = median(played - scale * expected for expected, played in anchors)
    residuals = [
        abs(played - (scale * expected + offset))
        for expected, played in anchors
    ]
    median_residual = median(residuals)
    inlier_threshold = max(OUTLIER_FLOOR_SECONDS,median_residual * 3,)
    inliers = [
        anchor
        for anchor, residual in zip(anchors, residuals)
        if residual <= inlier_threshold
    ]

    refined_scale = _median_slope(inliers)
    if refined_scale is not None:
        scale = refined_scale
        offset = median(
            played - scale * expected
            for expected, played in inliers
        )

    return TimingTransform(scale=scale,offset=offset,anchor_count=len(inliers),)
