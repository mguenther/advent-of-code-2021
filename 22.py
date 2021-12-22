def parse_range(range):
    l, r = range[2:].split('..')
    return int(l), int(r)


def parse_line(line):
    command, span = line.split(' ')
    x, y, z = span.split(',')
    return (command, parse_range(x), parse_range(y), parse_range(z))


def parse(filename = '22.in'):
    return [parse_line(line.strip()) for line in open(filename, 'r')]


def is_range_inside_bounds(r, bounds):
    lower, upper = bounds
    return lower <= r[0] <= upper and lower <= r[1] <= upper


def is_inside_bounds(step, bounds):
    _, range_x, range_y, range_z = step
    return is_range_inside_bounds(range_x, bounds) and is_range_inside_bounds(range_y, bounds) and is_range_inside_bounds(range_z, bounds)


def all_inside_bounds(steps, bounds):
    return list(filter(lambda step: is_inside_bounds(step, bounds), steps))


def solve_naive(steps):
    cubes = set()
    for step in steps:
        command, range_x, range_y, range_z = step
        for x in range(range_x[0], range_x[1] + 1):
            for y in range(range_y[0], range_y[1] + 1):
                for z in range(range_z[0], range_z[1] + 1):
                    cube = (x, y, z)
                    if command == 'on':
                        cubes.add(cube)
                    elif command == 'off':
                        if cube in cubes:
                            cubes.remove(cube)
    return len(cubes)


def intersect_on_axis(range_l, range_r):
    assert range_l[1] >= range_l[0]
    assert range_r[1] >= range_r[0]
    if range_r[0] > range_l[1]:
        return None
    if range_l[0] > range_r[1]:
        return None
    points = sorted([range_l[0], range_l[1], range_r[0], range_r[1]])
    return (points[1], points[2])


def intersect(cuboid_l, cuboid_r):

    intersect_on_x = intersect_on_axis(cuboid_l.range_x, cuboid_r.range_x)
    intersect_on_y = intersect_on_axis(cuboid_l.range_y, cuboid_r.range_y)
    intersect_on_z = intersect_on_axis(cuboid_l.range_z, cuboid_r.range_z)

    if not all((intersect_on_x, intersect_on_y, intersect_on_z)):
        return None

    return Cuboid(intersect_on_x, intersect_on_y, intersect_on_z)


class Cuboid(object):

    def __init__(self, range_x, range_y, range_z):
        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z
        self.void = []

    def remove(self, cuboid):
        void_cuboid = intersect(self, cuboid)
        if void_cuboid:
            for v in self.void:
                v.remove(void_cuboid)
            self.void.append(void_cuboid)

    def volume(self):

        edge_length_x = self.range_x[1] - self.range_x[0] + 1
        edge_length_y = self.range_y[1] - self.range_y[0] + 1
        edge_length_z = self.range_z[1] - self.range_z[0] + 1

        void_volume = sum(v.volume() for v in self.void)

        return edge_length_x * edge_length_y * edge_length_z - void_volume


def solve(steps):
    cuboids = []
    for step in steps:
        command, range_x, range_y, range_z = step
        cuboid = Cuboid(range_x, range_y, range_z)    
        for c in cuboids:
            # we have to remove the overlapping portion of the new
            # cuboid from every other cuboid in any case, since we
            # do not want to count overlapping segments twice
            # if the cuboid results from an 'off' command, we are
            # already fine at this point. if not, we add the cuboid
            # to the listof cuboids afterwards
            c.remove(cuboid)
        if command == 'on':
            cuboids.append(cuboid)
    return sum(c.volume() for c in cuboids)


print(solve_naive(all_inside_bounds(parse(), (-50, 50))))
print(solve(all_inside_bounds(parse(), (-50, 50))))
print(solve(parse()))
