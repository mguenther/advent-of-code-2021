RELATIVE_PIXELS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def parse(filename: str = '20.in') -> tuple[str, set[tuple[int, int]]]:
    raw_data = open(filename, 'r').read()
    raw_algorithm, raw_grid = raw_data.split('\n\n')
    algorithm = raw_algorithm.strip()
    G = set()
    for r, raw_grid_line in enumerate(raw_grid.split('\n')):
        for c, raw_grid_char in enumerate(raw_grid_line):
            if raw_grid_char == '#':
                G.add((r,c))
    return G, algorithm


def visualize(G):
    r_min, r_max = row_span_of(G)
    c_min, c_max = col_span_of(G)
    for r in range(r_min, r_max):
        s = ''
        for c in range(c_min, c_max):
            if (r, c) in G:
                s += '#'
            else:
                s += ' '
        print(s)


def row_span_of(G: set[tuple[int, int]]) -> int:
    return (min([r - 1 for (r, _) in G]), max([r + 2 for (r, _) in G]))


def col_span_of(G: set[tuple[int, int]]) -> int:
    return (min([c - 1 for (_, c) in G]), max([c + 2 for (_, c) in G]))


# I coded the solution to work with the provided sample data, which worked
# initially, but then I found that my solution does not work with the input
# data of the puzzle. Looking at the algorithm part of the puzzle input
# suggests that positions that are just outside the inner part of the image
# toggle in between iterations ('0' => '.' and '512' => '#'). This situation
# does not present itself in this way in the sample data. Hence, we need to
# adjust the solution to cope for this kind of toggling behaviour (thus,
# the 'on' function argument). Have to say: I'm getting a bit tired of this.
#
# Disclaimer: I did not come up with the 'on' argument by myself. I got the
# inspiration from Jonathan Paul's solution (watch
# https://www.youtube.com/watch?v=zDCLWtnW0Mg) to get the idea.
#
# There is no problem however if we always traverse the *complete* image per
# iteration instead of going over only those positions that are lit. But in
# this case, we have to cope with the infiniteness of the image by framing
# it inside a sufficiently large finite grid. Given the size of the input data,
# this seems feasible, since for each iteration, we only add 1 row to the left
# and right and 1 column to the top and bottom of the enhanced image.
# (this observation is also used in the computation of the span of the image)
# Thus, the growth of the image is constrained and given the fact that we only 
# need to evaluate up to 50 iterations, the initial grid size goes from 
# 100 by 100 to 200 by 200, which - even for vanilla Python 3.x - should be 
# able to compute the solution in a fair amount of time.
def __iterate(G: set[tuple[int, int]], algorithm: str, on: bool) -> set[tuple[int, int]]:
    r_min, r_max = row_span_of(G)
    c_min, c_max = col_span_of(G)
    G_new = set()
    for r in range(r_min, r_max):
        for c in range(c_min, c_max):
            b = ''
            for (r_delta, c_delta) in RELATIVE_PIXELS:
                if ((r+r_delta, c+c_delta) in G) != on:
                    b += '1'
                else:
                    b += '0'
            index = int(b, 2)
            if (algorithm[index] == '#') == on:
                G_new.add((r, c))
    return G_new


def number_of_lit_pixels(G: set[tuple[int, int]], algorithm: str, steps: int = 2) -> int:
    for i in range(steps):
        on = i % 2 == 1
        G = __iterate(G, algorithm, on)
    return len(G)


G, algorithm = parse('20.in')

print(number_of_lit_pixels(G, algorithm, steps = 2))
print(number_of_lit_pixels(G, algorithm, steps = 50))
