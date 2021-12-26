def is_free(G, r, c):
    return G[r][c] == '.'


def is_east_facing_cucumber(G, r, c):
    return G[r][c] == '>'


def is_south_facing_cucumber(G, r, c):
    return G[r][c] == 'v'


def copy(G):
    R = len(G)
    C = len(G[0])
    return [[G[r][c] for c in range(C)] for r in range(R)]


G = copy([line.strip() for line in open('25.in', 'r')])

R = len(G)
C = len(G[0])
step = 1
while True:
    has_moved = False
    G_ = copy(G)
    for r in range(R):
        for c in range(C):
            c_ = (c + 1) % C
            if is_east_facing_cucumber(G, r, c) and is_free(G, r, c_):
                has_moved = True
                G_[r][c_] = '>'
                G_[r][c] = '.'
    G__ = copy(G_)
    for r in range(R):
        for c in range(C):
            r_ = (r + 1) % R
            if is_south_facing_cucumber(G_, r, c) and is_free(G_, r_, c):
                has_moved = True
                G__[r_][c] = 'v'
                G__[r][c] = '.'
    if not has_moved:
        break
    else:
        step += 1
        G = G__
print(step)