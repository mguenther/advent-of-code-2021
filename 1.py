from itertools import pairwise
from typing import List


def windowed(seq: List[int], size: int) -> int:
    for i in range(len(seq) - size + 1):
        yield(seq[i: i + size])
        

def times_increased(seq: List[int], pairsize: int) -> int:
    return len(list(filter(lambda x: x > 0, [sum(y) - sum(x) for (x, y) in pairwise(windowed(seq, pairsize))])))


measurements = [int(line.strip()) for line in open('1.in', 'r').readlines()]

# First solution, before generalizing it
#times_increased = len(list(filter(lambda x: x > 0, [y - x for (x,y) in pairwise(measurements)])))
#print(times_increased)

print(times_increased(measurements, 1))
print(times_increased(measurements, 3))