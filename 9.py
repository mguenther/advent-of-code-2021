from collections import defaultdict, deque
from functools import reduce
from typing import Any, Callable, List


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def is_out_ouf_bounds(position: tuple[int, int], bounds: tuple[int, int]) -> bool:
    return position[0] < 0 or position[0] >= bounds[0] or position[1] < 0 or position[1] >= bounds[1]


def get_positions_of_neighbours(position: tuple[int, int], bounds: tuple[int, int]) -> List[int]:
    positions_of_neighbours = [(position[0] + direction[0], position[1] + direction[1]) for direction in DIRECTIONS]
    positions_of_neighbours = list(filter(lambda position: not(is_out_ouf_bounds(position, bounds)), positions_of_neighbours))
    return positions_of_neighbours


def deref_all(positions: List[tuple[int, int]], grid: List[List[int]]) -> List[int]:
    return list(map(lambda position: grid[position[0]][position[1]], positions))


def deref(position: tuple[int, int], grid: List[List[int]]) -> int:
    return grid[position[0]][position[1]]


def all(predicate: Callable[[tuple[Any, bool]], bool], sequence: List[tuple[int, bool]]) -> bool:
    return len(sequence) == len(list(filter(lambda x: predicate(x), sequence)))


def is_low_point(position: tuple[int, int], grid: List[List[int]]) -> bool:
    bounds = (len(grid), len(grid[0]))
    neighbours = deref_all(get_positions_of_neighbours(position, bounds), grid)
    reference_point = grid[position[0]][position[1]]
    return all(lambda neighbour: reference_point < neighbour, neighbours)


def find_low_points(grid: List[List[int]]) -> List[tuple[int, int]]:
    low_points = []
    for row_pos in range(0, len(grid)):
        for col_pos in range(0, len(grid[row_pos])):
            if is_low_point((row_pos, col_pos), grid):
                low_points.append((row_pos, col_pos))
    return low_points


def sum_of_risk_levels(grid: List[List[int]]) -> int:
    return sum(map(lambda x: 1 + grid[x[0]][x[1]], find_low_points(grid)))


def product_of_top_basins(grid: List[List[int]]) -> int:
    seen = []
    bounds = (len(grid), len(grid[0]))
    basins = {}
    for low_point in find_low_points(grid):
        Q = deque()
        Q.appendleft(low_point)
        seen.append(low_point)
        size_of_basin = 0
        while not(len(Q) == 0):
            point = Q.pop()
            point_value = deref(point, grid)
            size_of_basin += 1
            for direction in DIRECTIONS:
                neighbour = (point[0] + direction[0], point[1] + direction[1])
                if not(is_out_ouf_bounds(neighbour, bounds)):
                    if not(neighbour in seen):
                        neighbour_value = deref(neighbour, grid)
                        if not(neighbour_value == 9) and neighbour_value > point_value:
                            Q.append(neighbour)
                            seen.append(neighbour)
        basins[low_point] = size_of_basin
    values = [v for v in basins.values()]
    values.sort(reverse=True)
    return reduce(lambda l, r: l * r, values[0:3])


grid = [list(map(lambda x: int(x), list(row.strip()))) for row in open('9.in', 'r')]

print(sum_of_risk_levels(grid))
print(product_of_top_basins(grid))