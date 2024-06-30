def plan_intervals(entries):
    if len(entries) <= 1:
        return [(0, entries[0][0])] if entries else []

    entries_queue = sorted(entries, key=lambda x: x[1])

    intervals = [(0, entries_queue[0][0])]
    current_time = intervals[-1][1]

    for entry in entries_queue[1:]:
        start_time = current_time
        end_time = start_time + entry[0]
        intervals.append((start_time, end_time))
        current_time = end_time

    return intervals
