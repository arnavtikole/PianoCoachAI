
def calculate_note_intervals(notes):
    intervals = []

    sorted_notes = sorted(notes,key=lambda note: note.start_time)

    start_times = []

    for note in sorted_notes:
        if not start_times:
            start_times.append(note.start_time)
            continue

        if abs(note.start_time - start_times[-1]) > 0.05:
            start_times.append(note.start_time)

    for i in range(1, len(start_times)):
        interval = start_times[i] - start_times[i-1]
        intervals.append(interval)

    return intervals


def estimate_tempo(intervals):
    if not intervals:
        return 0

    avg_interval = sum(intervals) / len(intervals)

    if avg_interval==0:
        return 0

    return 60/avg_interval


def within_tolerance(expected, actual, tolerance=0.1):
    return abs(expected-actual) <= tolerance
