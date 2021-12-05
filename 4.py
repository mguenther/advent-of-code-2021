from typing import Callable, List


def parse_draws() -> List[int]:
    lines = [line.strip() for line in open(FILENAME, 'r')]
    return [int(number) for number in lines[0].split(',')]


def parse_line_of_board(board_line_data: List[str]) -> List[tuple[int, bool]]:
    return [(int(n), False) for n in board_line_data.replace('  ', ' ').split(' ')]


def parse_board(board_data: List[List[str]]) -> List[List[tuple[int, bool]]]:
    board = []
    for board_line_data in board_data:
        board.append(parse_line_of_board(board_line_data))
    return board


def parse_boards() -> List[List[List[tuple[int, bool]]]]:
    boards = []
    boards_data = [line.strip() for line in open(FILENAME, 'r') if line.strip() != ''][1:]
    while len(boards_data) > 0:
        boards.append(parse_board(boards_data[:5]))
        boards_data = boards_data[5:]
    return boards


def card_value(card: tuple[int, bool]) -> int:
    return card[0]


def crossed_of(card: tuple[int, bool]) -> bool:
    return card[1]


def cross_of(card: tuple[int, bool], boards: List[List[List[tuple[int, bool]]]]) -> None:
    for board in boards:
        for row in range(len(board)):
            for col in range(len(board[row])):
                if card_value(board[row][col]) == card:
                    board[row][col] = (card_value(board[row][col]), True)


def row(index: int, board: List[List[tuple[int, bool]]]) -> List[tuple[int, bool]]:
    return board[index]


def column(index: int, board: List[List[tuple[int, bool]]]) -> List[tuple[int, bool]]:
    columns = []
    for row in range(len(board)):
        columns.append(board[row][index])
    return columns


def all(predicate: Callable[[tuple[int, bool]], bool], sequence: List[tuple[int, bool]]) -> bool:
    return len(sequence) == len(list(filter(lambda x: predicate(x), sequence)))


def is_winning_board(board: List[List[tuple[int, bool]]]) -> bool:
    for index in range(len(board)):
        if all(crossed_of, row(index, board)) or all(crossed_of, column(index, board)):
            return True
    return False


def sum_of_unmarked_cards(board: List[List[tuple[int, bool]]]) -> int:
    sum = 0
    for row in range(len(board)):
        for column in range(len(board)):
            if not crossed_of(board[row][column]):
                sum += card_value(board[row][column])
    return sum


def score_of_first_winning_board() -> int:
    draws = parse_draws()
    boards = parse_boards()
    for i in range(len(draws)):
        card = draws[i]
        cross_of(card, boards)
        for board in boards:
            if is_winning_board(board):
                s = sum_of_unmarked_cards(board)
                return card * s


def score_of_last_winning_board() -> int:
    draws = parse_draws()
    boards = parse_boards()
    for i in range(len(draws)):
        card = draws[i]
        cross_of(card, boards)
        for board in boards:
            
            if is_winning_board(board) and len(boards) == 1:
                # we are down to the last winning board,
                # so calculate its score and be done with it
                s = sum_of_unmarked_cards(board)
                return card * s
            elif is_winning_board(board):
                # remove all winning boards of this round
                boards.remove(board)


FILENAME = '4.in'

print(score_of_first_winning_board())
print(score_of_last_winning_board())
