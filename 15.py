from collections import defaultdict
from queue import PriorityQueue
from typing import List

import numpy as np


def parse(filename: str = '15.in') -> List[List[int]]:
    return [[int(i) for i in line.strip()] for line in open(filename, 'r').readlines()]


def shortest(G: List[List[int]], start: tuple[int, int], target: tuple[int, int]) -> int:

    def neighbours(position: tuple[int, int], boundary: int) -> List[tuple[int, int]]:
        n = []
        i, j = position
        for d_i, d_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_i = i + d_i
            n_j = j + d_j
            if not(n_i < 0 or n_i >= boundary or n_j < 0 or n_j >= boundary):
                n.append((n_i, n_j))
        return n

    Q = PriorityQueue()
    Q.put((0, start))

    distances = defaultdict(lambda: int(1e9))
    distances[start] = 0
    
    while not Q.empty():
        
        distance, node = Q.get()
        
        if node == target: return distance
        if distances[node] < distance: continue

        for (n_i, n_j) in neighbours(node, len(G)):
            n_distance = distance + G[n_i][n_j]
            if distances[(n_i, n_j)] > n_distance:
                distances[(n_i, n_j)] = n_distance
                Q.put((n_distance, (n_i, n_j)))


# Given the poor description of the problem and sample input (15.dp.py) I lost
# interest at this point and 'borrowed' the graph extension algorithm from
# reddit (user: mapleoctopus621).
def extend(G: List[List[int]], times: int = 5) -> List[List[int]]:
    G_initial = np.array(G) - 1
    G_extended = np.empty((0, len(G) * times), dtype = int)
    for _ in range(times):
        row = np.concatenate(tuple((G_initial + i) % 9 for i in range(times)), axis = 1)
        G_extended = np.concatenate((G_extended, row), axis = 0)
        G_initial = (G_initial + 1)%9
    G_extended += 1
    return G_extended


G = parse()
G_extended = extend(G)

start = (0, 0)
goal = (len(G) - 1, len(G) - 1)
goal_e = (len(G_extended) - 1, len(G_extended) - 1)

print(shortest(G, start, goal))
print(shortest(G_extended, start, goal_e))