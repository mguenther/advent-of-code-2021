from typing import List, NoReturn, Set


def parse(filename: str = '13.in') -> tuple[Set[tuple[int, int]], List[tuple[str, int]]]:
    lines = [line.strip() for line in open(filename, 'r')]
    dots = set()
    instructions = []
    for line in lines:
        if line.startswith('fold'):
            axis, coordinate = line.replace('fold along ', '').split('=')
            instructions.append((axis, int(coordinate)))
        elif ',' in line:
            row, col = line.split(',')
            dots.add((int(row), int(col)))
    return dots, instructions


def visualize(dots: Set[tuple[int, int]]) -> NoReturn:
    w = max([dot[0] for dot in dots]) + 1
    h = max([dot[1] for dot in dots]) + 1
    g = []
    for i in range(0, h):
        row = []
        for j in range(0, w):
            row.append('.')
        g.append(row)
    for dot in dots:
        g[dot[1]][dot[0]] = '#'
    for i in g:
        print(''.join(i))


dots, instructions = parse()

for (fold, at) in instructions:
    print(len(dots))
    dots_ = set()
    for dot in dots:
        dot_x = 2 * at - dot[0] if fold == 'x' and dot[0] > at else dot[0]
        dot_y = 2 * at - dot[1] if fold == 'y' and dot[1] > at else dot[1]
        dots_.add((dot_x, dot_y))
    dots = dots_

visualize(dots)