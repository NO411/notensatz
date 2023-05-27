from typing import List
from math import floor

from os import path

def get_abs_path(current_file: str, relative_path: str) -> str:
    """returns absolute path depending on relative path to the given current file"""
    return path.join(path.dirname(path.abspath(current_file)), relative_path)

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
        return floor(closest_index / 2)

def find_overlap_intervals(intervals: List[List[List[float]]], main_interval: List[float]):

    cut_intervals = []
    start = main_interval[0]
    end = main_interval[1]

    # create cut intervals (where the actual objects are)
    for interval_container in intervals:
        if (len(interval_container) == 0):
            return []

        if interval_container[0][0] > start:
            cut_intervals.append([start, interval_container[0][0]])
        for n, interval in enumerate(interval_container):
            if (n < len(interval_container) - 1 and interval_container[n + 1][0] > interval[1]):
                cut_intervals.append([interval[1], interval_container[n + 1][0]])
            elif (interval[1] < end):
                cut_intervals.append([interval[1], end])

    if (len(cut_intervals) == 0):
        if (end > start):
            return [main_interval]
        else:
            return []

    # connect overlapping intervals
    merged_intervals = []
    sorted_intervals = sorted(cut_intervals, key = lambda x: x[0])

    for interval in sorted_intervals:
        if not merged_intervals or merged_intervals[-1][1] < interval[0]:
            merged_intervals.append(interval)
        else:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])

    spaces = []
    # cut connected intervals from main interval
    if (merged_intervals[0][0] > start):
        spaces.append([start, merged_intervals[0][0]])

    for n, interval in enumerate(merged_intervals):
        if (n < len(merged_intervals) - 1 and merged_intervals[n + 1][0] > interval[1]):
            spaces.append([interval[1], merged_intervals[n + 1][0]])
        elif (interval[1] < end):
            spaces.append([interval[1], end])
    return spaces
