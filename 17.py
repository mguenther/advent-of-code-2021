def probe(target_area: tuple[int, int, int, int], dxr: tuple[int, int] = (0, 250), dyr: tuple[int, int] = (-150, 150), steps: int = 250) -> tuple[int, int]:
    overall_area_hits = 0
    overall_max_y = 0
    for initial_dx in range(dxr[0], dxr[1]):
        for initial_dy in range(dyr[0], dyr[1]):
            hit_target_area = False
            x, y = 0, 0
            dx, dy = initial_dx, initial_dy
            max_y = 0
            for _ in range(steps):
                x += dx
                y += dy
                max_y = max(max_y, y)
                if dx < 0:
                    dx +=1 
                elif dx > 0:
                    dx -= 1
                dy -= 1
                if x >= target_area[0] and x <= target_area[2] and y >= target_area[1] and y <= target_area[3]:
                    hit_target_area = True
            if hit_target_area:
                overall_max_y = max(overall_max_y, max_y)
                overall_area_hits += 1
    return overall_max_y, overall_area_hits


test_area = (20, -10, 30, -5)
puzzle_area = (209, -86, 238, -59)

print(probe(puzzle_area))