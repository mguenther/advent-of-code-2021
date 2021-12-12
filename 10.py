from collections import deque
from statistics import median
from typing import List


ALLOWED = ['(', '[', '{', '<']

ERROR_SCORE_BY_SYMBOL = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETE_SCORE_BY_SYMBOL = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

EXPECTED_CLOSING = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


def get_error_score_of_corrupted_lines(lines: List[str]) -> int:
    error_score = 0
    for line in lines:
        stack = deque()
        for c in line:
            if c in ALLOWED:
                stack.appendleft(c)
            elif c == ')' and stack[0] == '(':
                stack.popleft()
            elif c == ']' and stack[0] == '[':
                stack.popleft()
            elif c == '}' and stack[0] == '{':
                stack.popleft()
            elif c == '>' and stack[0] == '<':
                stack.popleft()
            else:
                error_score += ERROR_SCORE_BY_SYMBOL[c]
                break
    return error_score


def get_autocomplete_scores(lines: List[str]) -> List[int]:
    autocomplete_scores = []
    for line in lines:
        stack = deque()
        corrupted = False
        for c in line:
            if c in ALLOWED:
                stack.appendleft(c)
            elif c == ')' and stack[0] == '(':
                stack.popleft()
            elif c == ']' and stack[0] == '[':
                stack.popleft()
            elif c == '}' and stack[0] == '{':
                stack.popleft()
            elif c == '>' and stack[0] == '<':
                stack.popleft()
            else:
                # corrupted line, we skip this
                corrupted = True
                break
        if not corrupted:
            autocomplete_score = 0
            autocomplete_by = list(map(lambda x: EXPECTED_CLOSING[x], stack))
            for c in autocomplete_by:
                autocomplete_score = autocomplete_score * 5 + AUTOCOMPLETE_SCORE_BY_SYMBOL[c]
            autocomplete_scores.append(autocomplete_score)
    return autocomplete_scores


lines = [line.strip() for line in open('10.in', 'r')]

print(get_error_score_of_corrupted_lines(lines))
print(median(get_autocomplete_scores(lines)))