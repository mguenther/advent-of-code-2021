# came up with the idea of fingerprinting based on the distance to neighbours
# and factoring in rotations and what not, but then came across this solution
# https://github.com/jimcasey/home/blob/master/projects/advent-of-code/2021/19/part1.py
# (which could also inspired by another solution, cf. https://bit.ly/3yOF591)
# and figured that I can optimize heavily by simplyifing the fingerprinting method
# to only take the closest two neighbours of a beacon into account. this marvelously
# works without taking convolutions into consideration (this suggests though that
# the following algorithm is not a general solution, but works given the problem
# input).

# Didn't work through part 2 though.

from math import sqrt


def parse(filename = '19.in'):
    return [[tuple(map(int, line.split(','))) for line in scanner_group.split('\n')[1:]] for scanner_group in open(filename, 'r').read().strip().split('\n\n')]


def euclidean_distance(l, r):
    lx, ly, lz = l
    rx, ry, rz = r
    return sqrt(pow(lx - rx, 2) + pow(ly - ry, 2) + pow(lz - rz, 2) * 1.0)


def closest_neighbours(beacon, scanner):
    neighbours_by_distance = {}
    for peer in scanner:
        if peer != beacon:
            neighbours_by_distance[euclidean_distance(beacon, peer)] = peer
    l, r = sorted(neighbours_by_distance)[:2]
    return (l, neighbours_by_distance[l], r, neighbours_by_distance[r])


def fingerprint(closest_neighbours):
    distance_to_first, first, distance_to_second, second = closest_neighbours
    return (distance_to_first + distance_to_second) * euclidean_distance(first, second)


reports = parse('19.in')
unique = set()
for scanner in reports:
    for beacon in scanner:
        unique.add(fingerprint(closest_neighbours(beacon, scanner)))

print(len(unique))
