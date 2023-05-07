from typing import List

def bound(x, lower, upper):
    return max(min(x, upper), lower)

def bound_in_intervals(x: float, intervals: List[List[float]]):
    bounds = []

    for interval in intervals:
        bounds.append(interval[0])
        bounds.append(interval[1])
        if (x >= interval[0] and x <= interval[1]):
            return x

    closest_index = None
    min_distance = float('inf')
    for i, number in enumerate(bounds):
        distance = abs(number - x)
        if distance < min_distance:
            min_distance = distance
            closest_index = i

    if (closest_index is None):
        return None

    return bounds[closest_index]