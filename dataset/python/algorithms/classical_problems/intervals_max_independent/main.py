from heapq import heapify, heappop


def max_independent_intervals(intervals):
    if len(intervals) <= 1:
        return intervals[:]
    intervals_queue = [(interval[1], interval) for interval in intervals]
    heapify(intervals_queue)
    independent_intervals = [heappop(intervals_queue)[1]]
    while intervals_queue:
        current_interval = heappop(intervals_queue)[1]
        if current_interval[0] >= independent_intervals[-1][1]:
            independent_intervals.append(current_interval)
    return independent_intervals
