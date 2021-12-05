from collections import defaultdict
from typing import Callable, List


def parse_line(raw_line: str) -> tuple[int, int, int, int]:

    lhs, rhs = raw_line.split(' -> ')
    x1, y1 = map(lambda x: int(x), lhs.split(','))
    x2, y2 = map(lambda x: int(x), rhs.split(','))

    return (x1, y1, x2, y2)


def parse() -> List[tuple[int, int, int, int]]:
    return [parse_line(l) for l in open('5.in', 'r')]


def is_vertical(line: tuple[int, int, int, int]) -> bool:
    return line[0] == line[2]


def is_horizontal(line: tuple[int, int, int, int]) -> bool:
    return line[1] == line[3]


def is_diagonal(line: tuple[int, int, int, int]) -> bool:
    vec = (line[0] - line[2], line[1] - line[3])
    return abs(vec[0]) == abs(vec[1])


def determinant(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def points_of(line: tuple[int, int, int, int]) -> List[tuple[int, int]]:
    if is_horizontal(line):
        x1, x2 = min(line[0], line[2]), max(line[0], line[2])
        return [(x, line[1]) for x in range(x1, x2 + 1)]
    elif is_vertical(line):
        y1, y2 = min(line[1], line[3]), max(line[1], line[3])
        return [(line[0], y) for y in range(y1, y2 + 1)]
    else:
        return list()


def points_of_revised(line: tuple[int, int, int, int]) -> List[tuple[int, int]]:
    if is_horizontal(line):
        x1, x2 = min(line[0], line[2]), max(line[0], line[2])
        return [(x, line[1]) for x in range(x1, x2 + 1)]
    elif is_vertical(line):
        y1, y2 = min(line[1], line[3]), max(line[1], line[3])
        return [(line[0], y) for y in range(y1, y2 + 1)]
    elif is_diagonal(line):
        points = []
        vec = (line[2] - line[0], line[3] - line[1])
        step_x = int(vec[0] / abs(vec[0]))
        step_y = int(vec[1] / abs(vec[1]))
        start = (line[0], line[1])
        for i in range(abs(vec[0]) + 1):
            points.append(start)
            start = (int(start[0] + step_x), int(start[1] + step_y))
        return points
    else:
        return list()


def number_of_intersection_points(points_of: Callable[[tuple[int, int, int, int]], List[tuple[int, int]]]) -> int:
    intersection_points = defaultdict(int)
    lines = parse()
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue
            points_of_1 = points_of(lines[i])
            points_of_2 = points_of(lines[j])
            intersections = list(set(points_of_1) & set(points_of_2))
            for intersection_point in intersections:
                intersection_points[intersection_point] += 1
    return len(intersection_points)


print(number_of_intersection_points(points_of))
print(number_of_intersection_points(points_of_revised))
