from collections import Counter
from itertools import pairwise
from typing import Dict


import sys


def parse(filename: str = '14.in') -> tuple[str, Dict]:
    lines = [line.strip() for line in open(filename, 'r') if line.strip() != '']
    template = lines[0]
    expansions = {}
    for expansion in lines[1:]:
        pattern, produces = expansion.split(' -> ')
        expansions[pattern] = produces
    return template, expansions


def quantity_of_most_common_element(polymer: str) -> int:
    counter = Counter(polymer)
    most_common_count = 0
    for k in counter:
        if counter[k] > most_common_count:
            most_common_count = counter[k]
    return most_common_count


def quantity_of_least_common_element(polymer: str) -> int:
    counter = Counter(polymer)
    least_common_count = sys.maxsize
    for k in counter:
        if counter[k] < least_common_count:
            least_common_count = counter[k]
    return least_common_count


def expand(template: str, rules: Dict[str, str], expansions: int) -> str:
    expanded_template = template
    for _ in range(expansions):
        new_template = ''
        for pair in pairwise(expanded_template):
            pattern = ''.join(pair)
            new_template += pair[0]
            new_template += rules[pattern]
        new_template += expanded_template[-1]
        expanded_template = new_template
    return expanded_template


def naive() -> int:
    template, rules = parse()
    polymer = expand(template, rules, 10)
    return quantity_of_most_common_element(polymer) - quantity_of_least_common_element(polymer)


print(naive())