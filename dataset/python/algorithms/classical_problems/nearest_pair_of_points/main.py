import math

from heapq import merge


def nearest_points(points):
    def nearest_points_helper(points):
        if len(points) <= 3:
            return brute_force(points), sorted(points, key=lambda point: point[1])
        middle = len(points) // 2
        left_points, right_points = points[:middle], points[middle:]
        left_points_min, left_sorted = nearest_points_helper(left_points)
        right_points_min, right_sorted = nearest_points_helper(right_points)
        min_distance = min(left_points_min, right_points_min)
        merged_parts = list(merge(left_sorted, right_sorted, key=lambda point: point[1]))
        filtered_points = [point for point in merged_parts if left_points[-1][0] - point[0] < min_distance]
        for i in range(len(filtered_points) - 1):
            end_index = min(i + 7, len(filtered_points))
            next_points = filtered_points[i + 1 : end_index]
            for next_point in next_points:
                min_distance = min(
                    euclidian_distance(filtered_points[i], next_point),
                    min_distance,
                )
        return min_distance, merged_parts

    points = sorted(points, key=lambda point: (point[0], point[1]))
    return nearest_points_helper(points)[0]


def brute_force(points):
    min_distance = float("inf")
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            min_distance = min(min_distance, euclidian_distance(points[i], points[j]))
    return min_distance


def euclidian_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
