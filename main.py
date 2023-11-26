from src.exceptions import CustomException, InvalidCountGamesException, InvalidSeparatorGamesException, \
    InvalidColorException, InvalidCountBoardColumnsException
from src.entities import Color, Board, Ball, Point, SimpleStrategy, RGBGame, Player


def main():
    boards = build_boards(10, 15)

    games = build_games(boards)

    run_games(games)

    print_games(games)


def build_boards(count_rows, count_columns):
    boards = []

    count_boards = int(input())

    if count_boards < 1:
        raise InvalidCountGamesException()

    for number_boards in range(0, count_boards):
        input_line = input()

        if input_line != '':
            raise InvalidSeparatorGamesException()

        rows = []

        for i in range(count_rows, 0, -1):
            input_line = input()

            row = list(input_line)

            check_valid_count_board_columns(len(row), count_columns)

            row_balls = []

            x = 1
            y = i

            for color in row:
                color_enum = build_color_enum(color)

                ball = Ball(Point(x, y), color_enum)

                row_balls.append(ball)

                x += 1

            rows.insert(0, row_balls)

        board = Board(rows, count_rows, count_columns)

        boards.append(board)

    return boards


def check_valid_count_board_columns(count_columns, necessary_count_columns):
    if count_columns != necessary_count_columns:
        raise InvalidCountBoardColumnsException(count_columns, necessary_count_columns)


def build_color_enum(color):
    if color == Color.R.value:
        return Color.R
    elif color == Color.G.value:
        return Color.G
    elif color == Color.B.value:
        return Color.B

    raise InvalidColorException(color)


def build_games(boards):
    games = []

    for board in boards:
        player = Player()
        strategy = SimpleStrategy(board)

        game = RGBGame(player, board, strategy)

        games.append(game)

    return games


def run_games(games):
    for game in games:
        game.run()


def print_games(games):
    count_games = len(games)

    for number_games in range(0, count_games):
        print('Game {}:'.format(number_games + 1))

        print_game(games[number_games])

        if number_games != count_games - 1:
            print("\n", end="")


def print_game(game):
    for move in game.get_moves():
        print_move(move)

    print_final_game(game)


def print_move(move):
    number = move.get_number()

    row = move.get_row()
    column = move.get_column()

    count_balls_removed = move.get_count_balls_removed()
    color = move.get_color()

    score = move.get_score()

    str_move = 'Move {} at ({},{}): removed {} balls of color {}, got {} points.'

    str_move = str_move.format(number, row, column, count_balls_removed, color, score)

    print(str_move)


def print_final_game(game):
    player_score = game.get_player_score()
    balls_remaining = game.get_balls_remaining()

    print('Final score: {}, with {} balls remaining.'.format(player_score, balls_remaining))


if __name__ == '__main__':
    try:   
        main()
    except CustomException as e:
        print(e.message)
