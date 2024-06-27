from heapq import heapify, heappop


def plan_intervals(entries):
    if len(entries) <= 1:
        return entries[:]
    entries_queue = [(entry[1], entry) for entry in entries]
    heapify(entries_queue)
    intervals = [(0, heappop(entries_queue)[1][0])]
    while entries_queue:
        current_entry = heappop(entries_queue)[1]
        intervals.append(intervals[-1][1], intervals[-1][1] + current_entry[0])
    return intervals
