import enum
from abc import ABCMeta, abstractmethod
from src.exceptions import InvalidCountBoardRowsException, InvalidCountBoardColumnsException, \
    InvalidBallColorClusterException


class Color(enum.Enum):

    R = 'R'
    G = 'G'
    B = 'B'


class RGBGame:

    def __init__(self, player, board, strategy):
        self._player = player
        self._board = board
        self._strategy = strategy

        self._moves = []

        self._number_move = 0

    def get_moves(self):
        return self._moves

    def get_player_score(self):
        return self._player.get_score()

    def get_balls_remaining(self):
        return self._board.get_balls_remaining()

    def run(self):
        while True:
            best_cluster = self._get_best_cluster()

            if best_cluster is None:
                self._add_player_bonus()

                break

            if best_cluster.get_count_balls() < 2:
                break

            self._move(best_cluster)

            self._remove_cluster(best_cluster)

    def _get_best_cluster(self):
        return self._strategy.get_best_cluster()

    def _add_player_bonus(self):
        self._add_player_score(1000)

    def _add_player_score(self, score):
        self._player.add_score(score)

    def _move(self, cluster):
        self._number_move += 1

        move = self._build_move(cluster)

        self._moves.append(move)

        score_per_move = move.get_score()

        self._add_player_score(score_per_move)

    def _build_move(self, cluster):
        count_balls_removed = cluster.get_count_balls()
        priority_ball = cluster.get_priority_ball()

        score_per_move = self._calc_score_per_move(count_balls_removed)

        return Move(self._number_move, priority_ball, count_balls_removed, score_per_move)

    def _calc_score_per_move(self, count_balls_removed):
        return pow(count_balls_removed - 2, 2)

    def _remove_cluster(self, cluster):
        self._board.remove_cluster(cluster)


class Player:

    def __init__(self):
        self._score = 0

    def get_score(self):
        return self._score

    def add_score(self, score):
        self._score += score


class Board:

    def __init__(self, balls, count_rows, count_columns):
        self._check_size(balls, count_rows, count_columns)

        self._balls = balls
        self._count_rows = count_rows
        self._count_columns = count_columns

        self._balls_remaining = sum(len(x) for x in balls)

        self._clusters = []

        self._init_clusters()

    def _check_size(self, balls, necessary_count_rows, necessary_count_columns):
        count_rows = len(balls)

        if count_rows != necessary_count_rows:
            raise InvalidCountBoardRowsException(count_rows, necessary_count_rows)

        for row in balls:
            count_columns = len(row)

            if count_columns != necessary_count_columns:
                raise InvalidCountBoardColumnsException(count_columns, necessary_count_columns)

    def get_count_rows(self):
        return self._count_rows

    def get_count_columns(self):
        return self._count_columns

    def get_balls_remaining(self):
        return self._balls_remaining

    def get_clusters(self):
        return self._clusters

    def _init_clusters(self):
        clusterization_algorithm = ClusterizationAlgorithm(self)

        self._clusters = clusterization_algorithm.build_clusters()

    def remove_cluster(self, cluster):
        self._remove_cluster_on_board(cluster)

        self._compress(cluster)

        self._init_clusters()

    def _remove_cluster_on_board(self, cluster):
        count_balls = cluster.get_count_balls()

        for index_ball in range(0, count_balls):
            ball = cluster[index_ball]

            self.remove_ball_on_board(ball)

        self._balls_remaining -= count_balls

    def remove_ball_on_board(self, ball):
        ball_coordinate_x = ball.get_point().get_coordinate_x()
        ball_coordinate_y = ball.get_point().get_coordinate_y()

        self._balls[ball_coordinate_y - 1][ball_coordinate_x - 1] = None

    def _compress(self, cluster):
        compression_algorithm = CompressionAlgorithm(self, cluster)

        compression_algorithm.run()

    def is_located_ball(self, point):
        coordinate_x = point.get_coordinate_x()
        coordinate_y = point.get_coordinate_y()

        return self._balls[coordinate_y - 1][coordinate_x - 1] is not None

    def get_ball_by_point(self, point):
        coordinate_x = point.get_coordinate_x()
        coordinate_y = point.get_coordinate_y()

        return self._balls[coordinate_y - 1][coordinate_x - 1]

    def set_ball_on_board(self, ball, point):
        coordinate_x = point.get_coordinate_x()
        coordinate_y = point.get_coordinate_y()

        self._balls[coordinate_y - 1][coordinate_x - 1] = ball


class ClusterizationAlgorithm:

    def __init__(self, board):
        self._board = board

        self._clusters = []

        self._index_merged_at_least_once_clusters = []

    def build_clusters(self):
        self._clusters = []

        for y in range(1, self._board.get_count_rows() + 1):
            for x in range(1, self._board.get_count_columns() + 1):
                point = Point(x, y)

                ball = self._board.get_ball_by_point(point)

                if ball is None:
                    continue

                cluster = self._build_cluster_for_ball(ball)

                self._clusters.append(cluster)

                self._union_clusters()

        return self._clusters

    def _build_cluster_for_ball(self, ball):
        cluster = Cluster(ball.get_color())
        cluster.add_ball(ball)

        return cluster

    def _union_clusters(self):
        union_clusters = []

        self._index_merged_at_least_once_clusters = []

        for index_cluster, cluster in enumerate(self._clusters):
            if index_cluster in self._index_merged_at_least_once_clusters:
                continue

            self._index_merged_at_least_once_clusters.append(index_cluster)

            self._merge_cluster_with_all_possible(cluster)

            union_clusters.append(cluster)

        self._clusters = union_clusters

    def _merge_cluster_with_all_possible(self, cluster):
        is_merged_at_least_once_clusters = False

        is_first_step = True
        while is_first_step or is_merged_at_least_once_clusters:  # do while
            is_first_step = False

            is_merged_at_least_once_clusters = False

            for index_other_cluster, other_cluster in enumerate(self._clusters):
                if index_other_cluster in self._index_merged_at_least_once_clusters:
                    continue

                if not other_cluster.can_belong(cluster):
                    continue

                cluster.merge(other_cluster)

                self._index_merged_at_least_once_clusters.append(index_other_cluster)

                is_merged_at_least_once_clusters = True


class Cluster:

    def __init__(self, color):
        self._color = color

        self._balls = []
        self._count_balls = 0

        self._index_priority_ball = -1

    def __getitem__(self, item):
        return self._balls[item]

    def get_color(self):
        return self._color

    def add_ball(self, ball):
        if not self._is_suit_by_color(ball):
            raise InvalidBallColorClusterException(ball.get_color().value, self._color.value)

        self._balls.append(ball)

        self._count_balls += 1

        self._if_need_set_index_priority_ball(self._count_balls - 1)

    def _is_suit_by_color(self, ball):
        return ball.get_color().value == self._color.value

    def _if_need_set_index_priority_ball(self, index_ball):
        if self._index_priority_ball == -1:
            self._index_priority_ball = index_ball

            return

        priority_ball = self._balls[self._index_priority_ball]
        ball = self._balls[index_ball]

        if ball.is_priority(priority_ball):
            self._index_priority_ball = index_ball

    def get_priority_ball(self):
        return self._balls[self._index_priority_ball]

    def get_count_balls(self):
        return self._count_balls

    def can_belong(self, other_cluster):
        if not self.is_equal_by_color(other_cluster):
            return False

        for index_other_cluster_ball in range(0, other_cluster.get_count_balls()):
            other_cluster_ball = other_cluster[index_other_cluster_ball]

            for cluster_ball in self._balls:
                if other_cluster_ball.is_nearby(cluster_ball):
                    return True

        return False

    def is_equal_by_color(self, other_cluster):
        return self._color.value == other_cluster.get_color().value

    def merge(self, other_cluster):
        for index_other_cluster_ball in range(0, other_cluster.get_count_balls()):
            other_cluster_ball = other_cluster[index_other_cluster_ball]

            if self.is_exist_ball(other_cluster_ball):
                continue

            self.add_ball(other_cluster_ball)

    def is_exist_ball(self, ball):
        for index_cluster_ball in range(0, self.get_count_balls()):
            cluster_ball = self[index_cluster_ball]

            if ball.is_equal(cluster_ball):
                return True

        return False


class Ball:

    def __init__(self, point, color):
        self._point = point
        self._color = color

    def get_point(self):
        return self._point

    def get_color(self):
        return self._color

    def is_priority(self, ball):
        if self._point.get_coordinate_x() > ball.get_point().get_coordinate_x():
            return False

        if self._point.get_coordinate_x() < ball.get_point().get_coordinate_x():
            return True

        if self._point.get_coordinate_y() < ball.get_point().get_coordinate_y():
            return True

        return False

    def is_equal(self, ball):
        if not self.is_equal_by_color(ball):
            return False

        return self._point.is_equal(ball.get_point())

    def is_equal_by_color(self, ball):
        return self._color.value == ball.get_color().value

    def shift_left_horizontally(self, offset):
        new_coordinate_x = self._point.get_coordinate_x() - offset

        self._point.set_coordinate_x(new_coordinate_x)

    def shift_bottom_vertically(self, offset):
        new_coordinate_y = self._point.get_coordinate_y() - offset

        self._point.set_coordinate_y(new_coordinate_y)

    def is_nearby(self, other_ball):
        ball_coordinate_x = self._point.get_coordinate_x()
        ball_coordinate_y = self._point.get_coordinate_y()

        other_ball_coordinate_x = other_ball.get_point().get_coordinate_x()
        other_ball_coordinate_y = other_ball.get_point().get_coordinate_y()

        if ball_coordinate_x == other_ball_coordinate_x and abs(ball_coordinate_y - other_ball_coordinate_y) == 1:
            return True

        if ball_coordinate_y == other_ball_coordinate_y and abs(ball_coordinate_x - other_ball_coordinate_x) == 1:
            return True

        return False


class Point:

    def __init__(self, coordinate_x, coordinate_y):
        self._coordinate_x = coordinate_x
        self._coordinate_y = coordinate_y

    def get_coordinate_x(self):
        return self._coordinate_x

    def get_coordinate_y(self):
        return self._coordinate_y

    def set_coordinate_x(self, coordinate_x):
        self._coordinate_x = coordinate_x

    def set_coordinate_y(self, coordinate_y):
        self._coordinate_y = coordinate_y

    def is_equal(self, point):
        return self._coordinate_x == point.get_coordinate_x() and self._coordinate_y == point.get_coordinate_y()


class CompressionAlgorithm:

    def __init__(self, board, cluster):
        self._board = board
        self._cluster = cluster

    def run(self):
        self._compress_vertically()
        self._compress_horizontally()

    def _compress_vertically(self):
        vertically_compressor = VerticallyCompressor(self._board, self._cluster)

        vertically_compressor.run()

    def _compress_horizontally(self):
        horizontally_compressor = HorizontallyCompressor(self._board, self._cluster)

        horizontally_compressor.run()


class Compressor:

    __metaclass__ = ABCMeta

    def __init__(self, board, cluster):
        self._board = board
        self._cluster = cluster

        self._accumulative_offset = 0

    def run(self):
        start_points = self._get_start_points_in_empty_ranges()

        for start_point in start_points:
            shift_range = self._build_shift_range(start_point)

            if shift_range is None:
                continue

            self._shift_balls(shift_range, start_point)

    @abstractmethod
    def _get_start_points_in_empty_ranges(self):
        pass

    @abstractmethod
    def _shift_balls(self, empty_range, start_point):
        pass

    def _build_shift_range(self, start_point):
        left_border = self._calc_left_border_shift_range(start_point)

        if left_border is None:
            return None

        fixed_coordinate = self._get_fixed_coordinate_by_point(start_point)

        start_point_for_right_border = self._build_parametric_point(left_border, fixed_coordinate)

        right_border = self._calc_right_border_shift_range(start_point_for_right_border)

        if right_border is None:
            return None

        offset = left_border - self._get_parametric_coordinate_by_point(start_point)

        return ShiftRange(left_border, right_border, offset)

    def _calc_left_border_shift_range(self, start_point):
        start_parametric_coordinate = self._get_parametric_coordinate_by_point(start_point)
        fixed_coordinate = self._get_fixed_coordinate_by_point(start_point)

        max_parametric_coordinate = self._get_max_parametric_coordinate()

        for parametric_coordinate in range(start_parametric_coordinate, max_parametric_coordinate + 1):
            if parametric_coordinate == max_parametric_coordinate:
                return None

            parametric_point = self._build_parametric_point(parametric_coordinate, fixed_coordinate)

            if self._board.is_located_ball(parametric_point):
                return parametric_coordinate

        return None

    def _calc_right_border_shift_range(self, start_point):
        start_parametric_coordinate = self._get_parametric_coordinate_by_point(start_point)
        fixed_coordinate = self._get_fixed_coordinate_by_point(start_point)

        max_parametric_coordinate = self._get_max_parametric_coordinate()

        for parametric_coordinate in range(start_parametric_coordinate + 1, max_parametric_coordinate + 1):
            parametric_point = self._build_parametric_point(parametric_coordinate, fixed_coordinate)

            if not self._board.is_located_ball(parametric_point):
                return parametric_coordinate - 1

            if parametric_coordinate == max_parametric_coordinate:
                return parametric_coordinate

        return None

    @abstractmethod
    def _get_max_parametric_coordinate(self):
        pass

    @abstractmethod
    def _build_parametric_point(self, parametric_coordinate, fixed_coordinate):
        pass

    @abstractmethod
    def _get_parametric_coordinate_by_point(self, point):
        pass

    @abstractmethod
    def _get_fixed_coordinate_by_point(self, point):
        pass

    def _shift_ball(self, ball):
        self._board.remove_ball_on_board(ball)

        self._shift_in_direction_ball(ball)

        self._board.set_ball_on_board(ball, ball.get_point())

    @abstractmethod
    def _shift_in_direction_ball(self, ball):
        pass


class VerticallyCompressor(Compressor):

    def __init__(self, board, cluster):
        super().__init__(board, cluster)

    def _get_start_points_in_empty_ranges(self):
        start_points = [self._cluster[0].get_point()]

        for index_ball in range(1, self._cluster.get_count_balls()):
            point = self._cluster[index_ball].get_point()

            start_points.append(point)

            for index_start_point, start_point in enumerate(start_points):
                if point.is_equal(start_point):
                    continue

                if point.get_coordinate_x() != start_point.get_coordinate_x():
                    continue

                if point.get_coordinate_y() < start_point.get_coordinate_y():
                    del start_points[index_start_point]
                else:
                    start_points.pop()

                break

        return start_points

    def _shift_balls(self, shift_range, start_point):
        fixed_coordinate = self._get_fixed_coordinate_by_point(start_point)

        self._accumulative_offset = shift_range.get_offset()

        start_coordinate = shift_range.get_left_border()

        for offset_coordinate in range(start_coordinate, self._get_max_parametric_coordinate() + 1):
            point = self._build_parametric_point(offset_coordinate, fixed_coordinate)

            ball = self._board.get_ball_by_point(point)

            if ball is None:
                self._accumulative_offset += 1

                continue

            self._shift_ball(ball)

    def _get_max_parametric_coordinate(self):
        return self._board.get_count_rows()

    def _build_parametric_point(self, parametric_coordinate, fixed_coordinate):
        return Point(fixed_coordinate, parametric_coordinate)

    def _get_parametric_coordinate_by_point(self, point):
        return point.get_coordinate_y()

    def _get_fixed_coordinate_by_point(self, point):
        return point.get_coordinate_x()

    def _shift_in_direction_ball(self, ball):
        ball.shift_bottom_vertically(self._accumulative_offset)


class HorizontallyCompressor(Compressor):

    def __init__(self, board, cluster):
        super().__init__(board, cluster)

    def _get_start_points_in_empty_ranges(self):
        start_points = []

        min_coordinate_x = self._cluster.get_priority_ball().get_point().get_coordinate_x()
        coordinate_y = 1

        if min_coordinate_x == 1:
            point = Point(1, 1)

            if not self._board.is_located_ball(point):
                start_points.append(point)

            min_coordinate_x = 2

        for coordinate_x in range(min_coordinate_x, self._board.get_count_columns()):
            point = Point(coordinate_x, coordinate_y)
            left_point = Point(coordinate_x - 1, coordinate_y)

            if self._board.is_located_ball(left_point) and not self._board.is_located_ball(point):
                start_points.append(point)

        return start_points

    def _shift_balls(self, shift_range, start_point):
        self._accumulative_offset += shift_range.get_offset()

        start_coordinate = shift_range.get_left_border()
        finish_coordinate = shift_range.get_right_border()

        for offset_coordinate in range(start_coordinate, finish_coordinate + 1):
            for coordinate_y in range(1, self._board.get_count_rows() + 1):
                point = self._build_parametric_point(offset_coordinate, coordinate_y)

                ball = self._board.get_ball_by_point(point)

                if ball is None:
                    break

                self._shift_ball(ball)

    def _get_max_parametric_coordinate(self):
        return self._board.get_count_columns()

    def _build_parametric_point(self, parametric_coordinate, fixed_coordinate):
        return Point(parametric_coordinate, fixed_coordinate)

    def _get_parametric_coordinate_by_point(self, point):
        return point.get_coordinate_x()

    def _get_fixed_coordinate_by_point(self, point):
        return point.get_coordinate_y()

    def _shift_in_direction_ball(self, ball):
        ball.shift_left_horizontally(self._accumulative_offset)


class ShiftRange:

    def __init__(self, left_border, right_border, offset):
        self._left_border = left_border
        self._right_border = right_border
        self._offset = offset

    def get_left_border(self):
        return self._left_border

    def get_right_border(self):
        return self._right_border

    def get_offset(self):
        return self._offset


class Strategy:

    __metaclass__ = ABCMeta

    def __init__(self, board):
        self._board = board

    @abstractmethod
    def get_best_cluster(self):
        pass


class SimpleStrategy(Strategy):

    def __init__(self, board):
        super().__init__(board)

    def get_best_cluster(self):
        best_cluster = None

        for cluster in self._board.get_clusters():
            if best_cluster is None:
                best_cluster = cluster

                continue

            if cluster.get_count_balls() == best_cluster.get_count_balls():
                best_cluster_priority_ball = best_cluster.get_priority_ball()
                cluster_priority_ball = cluster.get_priority_ball()

                if cluster_priority_ball.is_priority(best_cluster_priority_ball):
                    best_cluster = cluster
            elif cluster.get_count_balls() > best_cluster.get_count_balls():
                best_cluster = cluster

        return best_cluster


class Move:

    def __init__(self, number, ball, count_balls_removed, score):
        self._number = number
        self._ball = ball
        self._count_balls_removed = count_balls_removed
        self._score = score

    def get_number(self):
        return self._number

    def get_row(self):
        return self._ball.get_point().get_coordinate_y()

    def get_column(self):
        return self._ball.get_point().get_coordinate_x()

    def get_color(self):
        return self._ball.get_color().value

    def get_count_balls_removed(self):
        return self._count_balls_removed

    def get_score(self):
        return self._score
