# Unfortunately the puzzle description suggests that this
# is a problem solvable using dynamic programming. I've
# seen others do this successfully (check out Jonathan Paul's
# solution here: https://www.youtube.com/watch?v=hig93Etxims)
# using a DP-based approach. However, using DP failed for my
# input.
# Anyway, here is the DP-based solution that I came up with.
# This should work on some inputs, at least for part one of
# the puzzle. It also works on the sample input.

from typing import List, NoReturn


def parse(filename: str) -> List[List[int]]:
    return [[int(c) for c in line.strip()] for line in open(filename, 'r')]


def visualize(G: List[List[int]]) -> NoReturn:
    for line in G:
        s = ''
        for c in line:
            s += '{:3d} '.format(c)
        print(s)


G = parse('15.sample')

for i in range(0, len(G)):
    for j in range(0, len(G[i])):
        if i == 0 and j == 0:
            continue
        elif i == 0 and j > 0:
            G[i][j] += G[i][j-1]
        elif i > 0 and j == 0:
            G[i][j] += G[i-1][j]
        else:
            G[i][j] += min(G[i-1][j], G[i][j-1])

visualize(G)

min_total_risk = G[-1][-1] - G[0][0]

print(min_total_risk)