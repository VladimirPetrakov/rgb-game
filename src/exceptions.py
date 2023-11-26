class CustomException(Exception):

    def __init__(self, message):
        self.message = message


class InvalidCountGamesException(CustomException):

    def __init__(self):
        message = 'Invalid count games'

        super().__init__(message)


class InvalidSeparatorGamesException(CustomException):

    def __init__(self):
        message = 'Invalid separator for games'

        super().__init__(message)


class InvalidColorException(CustomException):

    def __init__(self, color):
        message = 'Invalid color = {}. Necessary: R, G or B'.format(color)

        super().__init__(message)


class InvalidBallColorClusterException(CustomException):

    def __init__(self, color, necessary_color):
        message = 'Invalid color = {}. Necessary: {}'.format(color, necessary_color)

        super().__init__(message)


class InvalidCountBoardColumnsException(CustomException):

    def __init__(self, count, necessary_count):
        message = 'Invalid count of the board columns = {}. Necessary: {}'.format(count, necessary_count)

        super().__init__(message)


class InvalidCountBoardRowsException(CustomException):

    def __init__(self, count, necessary_count):
        message = 'Invalid count of the board rows = {}. Necessary: {}'.format(count, necessary_count)

        super().__init__(message)
