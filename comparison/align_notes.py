from parser.models import Note
import copy
import math
from collections import Counter

INSERT_COST = 2.0
DELETE_COST = 2.0
SIMULTANEOUS_TOLERANCE = 0.08
MAX_SUBSTITUTION_DISTANCE = 5

def group_notes(notes: list[Note],tolerance: float = SIMULTANEOUS_TOLERANCE,) -> list[list[Note]]:

    if not notes:
        return []

    sorted_notes = sorted(
        notes,
        key=lambda note: note.start_time
        if note.start_time is not None
        else 0.0
    )

    groups = []
    current_group = [sorted_notes[0]]

    for note in sorted_notes[1:]:

        current_start = current_group[0].start_time

        if current_start is None or note.start_time is None:
            groups.append(current_group)
            current_group = [note]
            continue

        if abs(note.start_time-current_start)<=tolerance:
            current_group.append(note)

        else:
            groups.append(current_group)
            current_group = [note]

    groups.append(current_group)

    return groups


def group_expected_notes(notes: list[Note],tolerance: float = SIMULTANEOUS_TOLERANCE,) -> list[list[Note]]:

    return group_notes(notes,tolerance)


def group_played_notes(notes: list[Note],tolerance: float = SIMULTANEOUS_TOLERANCE,) -> list[list[Note]]:

    return group_notes(notes,tolerance)


def get_midi_numbers(group: list[Note]) -> Counter[int]:

    return Counter(
        note.midi_number
        for note in group
        if note.midi_number is not None
    )


def group_match_cost(expected_group: list[Note],played_group: list[Note],) -> float:

    expected_midi = get_midi_numbers(expected_group)
    played_midi = get_midi_numbers(played_group)

    if not expected_midi or not played_midi:
        return 3.0

    common = expected_midi & played_midi
    missing = expected_midi - played_midi
    extra = played_midi - expected_midi

    if not missing and not extra:
        return 0.0

    if common:
        return (sum(missing.values()) * 1.0 + sum(extra.values()) * 1.0)

    return 4.0


def match_note_groups(expected_group: list[Note],played_group: list[Note],
) -> list[tuple[Note | None, Note | None]]:

    aligned = []

    remaining_expected = expected_group.copy()
    remaining_played = played_group.copy()


    for expected in expected_group:

        match_index = None

        for i, played in enumerate(remaining_played):

            if (
                expected.midi_number is not None
                and played.midi_number is not None
                and expected.midi_number == played.midi_number
            ):
                match_index = i
                break

        if match_index is not None:

            played = remaining_played.pop(match_index)
            remaining_expected.remove(expected)
            aligned.append((expected, played))


    for expected in remaining_expected.copy():

        match_index = None

        for i, played in enumerate(remaining_played):

            if (
                (expected.midi_number is None or played.midi_number is None)
                and
                expected.pitch is not None
                and played.pitch is not None
                and expected.pitch == played.pitch
            ):
                match_index = i
                break

        if match_index is not None:

            played = remaining_played.pop(match_index)
            remaining_expected.remove(expected)

            aligned.append((expected, played))


    while remaining_expected and remaining_played:
        candidates = [
            (abs(expected.midi_number - played.midi_number),expected_index,played_index,)
            for expected_index, expected in enumerate(remaining_expected)
            for played_index, played in enumerate(remaining_played)
            if expected.midi_number is not None and played.midi_number is not None
        ]

        if not candidates:
            break

        distance, expected_index, played_index = min(candidates)

        if distance > MAX_SUBSTITUTION_DISTANCE:
            break

        expected = remaining_expected.pop(expected_index)
        played = remaining_played.pop(played_index)
        aligned.append((expected, played))


    for expected in remaining_expected:
        aligned.append((expected, None))

    for played in remaining_played:
        aligned.append((None, played))

    return aligned


def align_groups(
    expected_groups: list[list[Note]],
    played_groups: list[list[Note]],
) -> list[tuple[list[Note] | None, list[Note] | None]]:

    rows = len(expected_groups)+1
    cols = len(played_groups)+1

    dp = [
        [0.0]*cols
        for _ in range(rows)
    ]

    for i in range(1, rows):

        dp[i][0] = (dp[i-1][0] + DELETE_COST * len(expected_groups[i-1]))

    for j in range(1, cols):
        dp[0][j] = (dp[0][j-1] + INSERT_COST * len(played_groups[j-1]))

    for i in range(1, rows):
        for j in range(1, cols):
            match_cost = group_match_cost(expected_groups[i-1],played_groups[j-1])

            match = (dp[i-1][j-1] + match_cost)

            delete = (dp[i-1][j] + DELETE_COST * len(expected_groups[i-1]))

            insert = (dp[i][j-1] + INSERT_COST * len(played_groups[j-1]))

            dp[i][j] = min(match,delete,insert)

    aligned_groups = []

    i = len(expected_groups)
    j = len(played_groups)

    while i>0 or j>0:

        if i>0 and j>0:

            match_cost = group_match_cost(expected_groups[i-1],played_groups[j-1])

            if math.isclose(dp[i][j],dp[i-1][j-1] + match_cost,rel_tol=1e-9,abs_tol=1e-9,):

                aligned_groups.append((expected_groups[i-1],played_groups[j-1]))

                i-=1
                j-=1
                continue

        if i>0:

            delete_cost = (dp[i-1][j] + DELETE_COST * len(expected_groups[i-1]))

            if math.isclose(dp[i][j],delete_cost,rel_tol=1e-9,abs_tol=1e-9,):

                aligned_groups.append((expected_groups[i-1],None))

                i-=1
                continue

        if j>0:

            aligned_groups.append((None,played_groups[j-1]))

            j -= 1

    aligned_groups.reverse()

    return aligned_groups


def normalize_expected_times(
    expected_notes: list[Note],
    time_scale: float,
    time_offset: float = 0.0,
) -> list[Note]:

    normalized_notes = copy.deepcopy(expected_notes)

    for note in normalized_notes:

        if note.start_time is not None:
            note.start_time = note.start_time * time_scale + time_offset

    return normalized_notes


def align_notes(
    expected_notes: list[Note],
    played_notes: list[Note],
    time_scale: float = 1.0,
    time_offset: float = 0.0,
) -> list[tuple[Note | None, Note | None]]:

    normalized_expected = normalize_expected_times(expected_notes,time_scale,time_offset,)

    expected_groups = group_expected_notes(normalized_expected)

    played_groups = group_played_notes(played_notes)

    aligned_groups = align_groups(expected_groups,played_groups)

    aligned_notes = []

    for expected_group, played_group in aligned_groups:

        if (expected_group is not None and played_group is not None):

            aligned_notes.extend(match_note_groups(expected_group,played_group))

        elif expected_group is not None:

            for expected in expected_group:

                aligned_notes.append((expected, None))

        elif played_group is not None:

            for played in played_group:

                aligned_notes.append((None, played))

    return aligned_notes
