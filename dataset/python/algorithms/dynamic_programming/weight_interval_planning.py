from functools import lru_cache


def weight_interval_planning(intervals):

    @lru_cache(1000)
    def weight_interval_planning_helper(index):
        if index == -1:
            return 0
        return max(
            sorted_intervals[index][1]
            + weight_interval_planning_helper(prev_intervals[index]),
            weight_interval_planning_helper(index - 1),
        )

    sorted_intervals = sorted(
        intervals, key=lambda interval_weight: interval_weight[0][1]
    )
    prev_intervals = get_prev_intervals(sorted_intervals)
    return weight_interval_planning_helper(len(intervals) - 1)


def get_prev_intervals(intervals):
    prev_intervals = []
    for i in range(len(intervals)):
        for j in range(i - 1, -1, -1):
            if intervals[i][0][0] > intervals[j][0][1]:
                prev_intervals.append(j)
                break
        else:
            prev_intervals.append(-1)
    return prev_intervals


def weight_interval_planning_iter(intervals):
    prev_intervals = get_prev_intervals(intervals)
    max_weight = 0
    cache = {-1: 0}
    for i, interval in enumerate(intervals):
        weight = max(interval[1] + cache[prev_intervals[i]], cache[i - 1])
        cache[i] = weight
        max_weight = max(weight, max_weight)
    return max_weight
