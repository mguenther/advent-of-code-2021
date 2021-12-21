from itertools import product
from functools import cache


PLAYER_1_WINS = (1, 0)
PLAYER_2_WINS = (0, 1)
POSSIBLE_THROWS = [sum(x) for x in product([1, 2, 3], repeat = 3)]


def deterministic_die():
    current_roll = 1
    while True:
        yield current_roll
        current_roll += 1
        if current_roll > 100:
            current_roll = 1


def play_turn(current_position, current_score, die):
    value = 0
    for _ in range(3):
        value += next(die)
    new_position = (current_position + value) % 10
    new_score = current_score + new_position + 1
    return new_position, new_score


def play_deterministic_game(player_1_position, player_2_position):
    die = deterministic_die()
    number_of_dice_rolls = 0
    # we use 0-based positions and adjust the score
    # advancement as appropriate
    player_1_score, player_2_score = 0, 0
    turn = True

    while player_1_score < 1000 and player_2_score < 1000:
        if turn:
            player_1_position, player_1_score = play_turn(player_1_position, player_1_score, die)
        else:
            player_2_position, player_2_score = play_turn(player_2_position, player_2_score, die)
        number_of_dice_rolls += 3
        turn = not turn

    if player_1_score > player_2_score:
        return player_2_score * number_of_dice_rolls
    else:
        return player_1_score * number_of_dice_rolls


def position(stats):
    return stats[0]


def score(stats):
    return stats[1]


def next_positions(stats):
    return [(position(stats) + throw - 1) % 10 + 1 for throw in POSSIBLE_THROWS]


@cache
def play_quantum_turn(player_1_stats, player_2_stats, turn):
    if score(player_1_stats) >= 21:
        return PLAYER_1_WINS
    if score(player_2_stats) >= 21:
        return PLAYER_2_WINS
    if turn:
        next_turns = [play_quantum_turn((next_position, score(player_1_stats) + next_position), player_2_stats, not turn) for next_position in next_positions(player_1_stats)]
    else:
        next_turns = [play_quantum_turn(player_1_stats, (next_position, score(player_2_stats) + next_position), not turn) for next_position in next_positions(player_2_stats)]
    return (sum(games_won_by_player_1 for games_won_by_player_1, _ in next_turns), sum(games_won_by_player_2 for _, games_won_by_player_2 in next_turns))


def play_quantum_game(player_1_position, player_2_position):
    return max(play_quantum_turn((player_1_position, 0), (player_2_position, 0), True))


print(play_deterministic_game(3, 1))
print(play_quantum_game(4, 2))