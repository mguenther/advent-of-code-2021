def solve_first_part() -> int:

    pos = (0, 0)

    for command in commands:
        direction, steps = command.split(' ')
        if direction == 'forward':
            pos = (pos[0] + int(steps), pos[1])
        elif direction == 'down':
            pos = (pos[0], pos[1] + int(steps))
        elif direction == 'up':
            pos = (pos[0], pos[1] - int(steps))

    return pos[0] * pos[1]


def solve_second_part() -> int:

    pos = (0, 0, 0)

    for command in commands:
        direction, steps = command.split(' ')
        if direction == 'forward':
            pos = (pos[0] + int(steps), pos[1] + pos[2] * int(steps), pos[2])
        elif direction == 'down':
            pos = (pos[0], pos[1], pos[2] + int(steps))
        elif direction == 'up':
            pos = (pos[0], pos[1], pos[2] - int(steps))

    return pos[0] * pos[1]


commands = [l for l in open('2.in', 'r').readlines()]

print(solve_first_part())
print(solve_second_part())
