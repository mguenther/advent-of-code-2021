def read():
    return [[int(n) for n in line.strip()] for line in open('11.in', 'r')]


def flash(row, col, G):
    flashes = 1
    G[row][col] = -1
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            row_n = row + dr
            col_n = col + dc
            if row_n < 0 or col_n < 0 or row_n >= len(G) or col_n >= len(G[row_n]):
                continue
            if G[row_n][col_n] == -1:
                continue
            G[row_n][col_n] += 1
            if G[row_n][col_n] >= 10:
                flashes += flash(row_n, col_n, G)
    return flashes


def total_flashes_up_to(steps = 100):
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


def first_synchronized_flash_at(max_steps = 1000):
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