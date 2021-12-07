from typing import Callable, List

import sys


def constant_cost(probe: int, position: int) -> int:
    return abs(position - probe)


def incremental_cost(probe: int, position: int) -> int:
    relative_distance = constant_cost(probe, position)
    cost = 0
    for i in range(relative_distance + 1):
        cost += i
    return cost


def cheapest_alignment(probes: List[int], positions: List[int], cost_fn: Callable[[int, int], int]) -> tuple[int, int]:
    cheapest_alignment_position = sys.maxsize
    cheapest_alignment_costs = sys.maxsize
    
    for probe in probes:
        costs = sum([cost_fn(probe, position) for position in positions])
        if costs < cheapest_alignment_costs:
            cheapest_alignment_position = probe
            cheapest_alignment_costs = costs

    return (cheapest_alignment_position, cheapest_alignment_costs)


positions = [int(i) for i in open('7.in', 'r').readline().split(',')]
probes = [probe for probe in range(min(positions), max(positions))]

print(cheapest_alignment(probes, positions, constant_cost))
print(cheapest_alignment(probes, positions, incremental_cost))