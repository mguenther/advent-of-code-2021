# Looks at each fish individually. This is painfully slow, but sufficient to
# for solving the first part of the problem. However, don't run this with 256.
# For an input of 256, this solution will not complete in a feasible amount of
# time.
def naive(until: int) -> int:

    timer = [int(i) for i in open('6.in', 'r').readline().split(',')]

    for i in range(until):
        new_timer = []
        for time in timer:
            if time == 0:
                new_timer.append(6)
                new_timer.append(8)
            else:
                new_timer.append(time-1)
        timer = new_timer

    return len(timer)


# This solution does not look at each individual fish, but at 'buckets of
# fish' giving their expected time to birth new fish. It uses a sliding
# window approach to move fish from bucket n to bucket n-1, while
# respecting the constraint that fish in the first bucket give birth
# to new fish and are then resetted.
def optimized(until: int) -> int:

    fishes = [int(i) for i in open('6.in', 'r').readline().split(',')]
    population_by_time = [fishes.count(i) for i in range(9)]

    for _ in range(until):
        population_by_time.append(population_by_time[0]) # birth of new fish
        population_by_time[7] += population_by_time[0]   # reset fish that gave birth
        population_by_time = population_by_time[1:]      # cut off old generation
    
    return sum(population_by_time)


print(optimized(80))
print(optimized(256))