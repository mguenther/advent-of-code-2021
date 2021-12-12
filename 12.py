from collections import defaultdict, deque
from typing import Dict, List


def to_adjacency_list(filename: str = '12.in') -> Dict[str, List[str]]:
    E = defaultdict(list)
    connections = [connection.strip().split('-') for connection in open('12.in', 'r')]
    for (l, r) in connections:
        E[l].append(r)
        E[r].append(l)
    return E


def is_small_cave(node: str) -> bool:
    return node.lower() == node


def number_of_possible_paths() -> int:
    E = to_adjacency_list()
    Q = deque([('start', set(['start']))])
    possible_paths = 0
    while Q:
        node, visited_small_caves = Q.popleft()
        if node == 'end':
            possible_paths += 1
        for adjacent_node in E[node]:
            if not adjacent_node in visited_small_caves:
                extended_visited_small_caves = set(visited_small_caves)
                if is_small_cave(adjacent_node):
                    extended_visited_small_caves.add(adjacent_node)
                Q.append((adjacent_node, extended_visited_small_caves))
    return possible_paths


def number_of_possible_paths_relaxed() -> int:
    E = to_adjacency_list()
    Q = deque([('start', set(['start']), None)])
    possible_paths = 0
    while Q:
        node, visited_small_caves, visited_twice = Q.popleft()
        if node == 'end':
            possible_paths += 1
        for adjacent_node in E[node]:
            if not adjacent_node in visited_small_caves:
                extended_visited_small_caves = set(visited_small_caves)
                if is_small_cave(adjacent_node):
                    extended_visited_small_caves.add(adjacent_node)
                Q.append((adjacent_node, extended_visited_small_caves, visited_twice))
            elif adjacent_node in visited_small_caves and not visited_twice and adjacent_node not in ['start', 'end']:
                Q.append((adjacent_node, visited_small_caves, adjacent_node))
    return possible_paths


print(number_of_possible_paths())
print(number_of_possible_paths_relaxed())