from typing import List


def read(filename = '11.in') -> List[List[int]]:
    return [[int(n) for n in line.strip()] for line in open(filename, 'r')]


def flash(row: int, col: int, G: List[List[int]]) -> int:
    def out_of_bounds(row, col):
        return row < 0 or col < 0 or row >= len(G) or col >= len(G[row])
    def flashed_already(row, col):
        return G[row][col] == -1
    flashes = 1
    G[row][col] = -1
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            row_n = row + dr
            col_n = col + dc
            if out_of_bounds(row_n, col_n):
                continue
            if flashed_already(row_n, col_n):
                continue
            G[row_n][col_n] += 1
            if G[row_n][col_n] >= 10:
                flashes += flash(row_n, col_n, G)
    return flashes


def total_flashes_up_to(steps: int = 100) -> int:
    G = read()
    total_flashes = 0
    for step in range(1, steps + 1):
        for row in range(len(G)):
            for col in range(len(G[row])):
                G[row][col] += 1
        for row in range(len(G)):
            for col in range(len(G[row])):
                if G[row][col] == 10:
                    total_flashes += flash(row, col, G)
        for row in range(len(G)):
            for col in range(len(G[row])):
                if G[row][col] == -1:
                    G[row][col] = 0
    return total_flashes


def first_synchronized_flash_at(max_steps: int = 1000) -> int:
    G = read()
    for step in range(1, max_steps + 1):
        for row in range(len(G)):
            for col in range(len(G[row])):
                G[row][col] += 1
        flashes_per_step = 0
        for row in range(len(G)):
            for col in range(len(G[row])):
                if G[row][col] == 10:
                    flashes_per_step += flash(row, col, G)
        if flashes_per_step == len(G) * len(G[row]):
            return step
        for row in range(len(G)):
            for col in range(len(G[row])):
                if G[row][col] == -1:
                    G[row][col] = 0
    return None


print(total_flashes_up_to())
print(first_synchronized_flash_at())