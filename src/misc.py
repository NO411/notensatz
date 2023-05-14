from typing import List
import math

def bound(x, lower, upper):
    return max(min(x, upper), lower)

def bound_in_intervals(x: float, intervals: List[List[float]], return_index: bool = False) -> List[float]:
    bounds = []

    for index, interval in enumerate(intervals):
        bounds.append(interval[0])
        bounds.append(interval[1])
        if (x >= interval[0] and x <= interval[1]):
            if (not return_index):
                return x
            else:
                return index

    closest_index = None
    min_distance = float('inf')
    for i, number in enumerate(bounds):
        distance = abs(number - x)
        if distance < min_distance:
            min_distance = distance
            closest_index = i

    if (closest_index is None):
        return None

    if (not return_index):
        return bounds[closest_index]
    else:
        return math.floor(closest_index / 2)

def find_overlap_interval(intervals: List[List[float]]) -> List[float]:
    overlap = intervals[0]

    for interval in intervals[1:]:
        if interval[0] > overlap[1] or interval[1] < overlap[0]:
            # no overlap found
            return None
        else:
            overlap = [max(overlap[0], interval[0]), min(overlap[1], interval[1])]

    return overlap
