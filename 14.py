from collections import defaultdict
from itertools import pairwise
from typing import Dict, List


def parse(filename: str = '14.in') -> tuple[str, Dict[str, List[str]], Dict[str, str]]:
    lines = [line.strip() for line in open(filename, 'r') if line.strip() != '']
    template = lines[0]
    expansions = {}
    for expansion in lines[1:]:
        pattern, produces = expansion.split(' -> ')
        l = pattern[0] + produces
        r = produces + pattern[1]
        expansions[pattern] = [l, r]
    expanded_by = {}
    for expansion in lines[1:]:
        pattern, produces = expansion.split(' -> ')
        expanded_by[pattern] = produces
    return template, expansions, expanded_by


def polymer_strength_after(steps: int) -> int:
    template, expansion_rules, expanded_by = parse('14.in')
    counter_pairs = defaultdict(int)
    counter_elements = defaultdict(int)
    for pair in pairwise(template):
        pattern = ''.join(pair)
        counter_pairs[pattern] += 1
    for element in template:
        counter_elements[element] += 1
    for _ in range(steps):
        counter_pairs_new = defaultdict(int)
        for k in counter_pairs.copy():
            counter_elements[expanded_by[k]] += counter_pairs[k]
            for production in expansion_rules[k]:
                counter_pairs_new[production] += counter_pairs[k]
        counter_pairs = counter_pairs_new
    
    return max(counter_elements.values()) - min(counter_elements.values())

print(polymer_strength_after(10))
print(polymer_strength_after(40))
