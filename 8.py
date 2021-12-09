from collections import defaultdict
from itertools import permutations
from typing import Callable, List


PATTERNS = [
     'abcefg',
     'cf',
     'acdeg',
     'acdfg',
     'bcdf',
     'abdfg',
     'abdefg',
     'acf',
     'abcdefg',
     'abcdfg'
]


def parse_line(line: str) -> tuple[List[str], List[str]]:
    raw_unique_signals, raw_output_values = line.strip().split(' | ')
    return (raw_unique_signals.strip().split(' '), raw_output_values.strip().split(' '))


def parse(filename = '8.in') -> List[tuple[List[str], List[str]]]:
    return [parse_line(line) for line in open(filename, 'r')]


def solve_first_part():
    instances = parse()
    outputs_by_len = defaultdict(int)
    for instance in instances:
        _, output_values = instance
        for output_value in output_values:
            outputs_by_len[len(output_value)] += 1
    return outputs_by_len[2] + outputs_by_len[3] + outputs_by_len[4] + outputs_by_len[7]


def solve_second_part():
    sum = 0
    instances = parse('8.in')
    segments = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    
    for instance in instances:
        signal_patterns, output_values = instance
        key = None
        for permutation in permutations(segments):
            all_match = True
            for signal in signal_patterns:
                transcoded_signal = [permutation[ord(segment)-97] for segment in signal]
                transcoded_signal.sort()
                key = ''.join(transcoded_signal)
                all_match = all_match and key in PATTERNS
            if all_match:
                break
        decoded_values = []
        for output_value in output_values:
            transcoded_output_value = [permutation[ord(segment)-97] for segment in output_value]
            transcoded_output_value.sort()
            transcoded_output_value = ''.join(transcoded_output_value)
            decoded_values.append(str(PATTERNS.index(transcoded_output_value)))
        sum += int(''.join(decoded_values))
    return sum


print(solve_first_part())
print(solve_second_part())
