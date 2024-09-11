from heapq import heapify, heappop


def intervals_distribution(intervals):
    if len(intervals) <= 1:
        return [intervals[:]]
    intervals_queue = [(interval[0], interval) for interval in intervals]
    heapify(intervals_queue)
    interval_groups = [[heappop(intervals_queue)[1]]]
    while intervals_queue:
        current_interval = heappop(intervals_queue)[1]
        for group in interval_groups:
            if current_interval[0] >= group[-1][1]:
                group.append(current_interval)
                break
        else:
            interval_groups.append([current_interval])
    return interval_groups
