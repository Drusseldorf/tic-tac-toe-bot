from enum import Enum
from game_entities.cells import Cell
from game_entities.utils.winner_checker import WinnerChecker
from game_entities.field import GameBoard


class State(Enum):
    DRAW = 0
    CROSS_WON = 1
    ZERO_WON = 2
    IN_PROGRESS = 3


class GameState:

    def __init__(self, game_board: str):
        self.__state: State | None = None
        self.__game_board = GameBoard.turn_into_list(game_board)
        self.__winner_checker = WinnerChecker()

    def __no_empty_cells_left(self) -> bool:
        result = True
        for row in self.__game_board:
            for cell in row:
                if cell == Cell.EMPTY:
                    result = False
        return result

    @property
    def state(self):
        if not self.__no_empty_cells_left() and not self.__winner_checker.got_winner(self.__game_board):
            self.__state = State.IN_PROGRESS

        elif self.__winner_checker.got_winner(self.__game_board):
            winner = self.__winner_checker.got_winner(self.__game_board)
            self.__state = State.CROSS_WON if winner == Cell.CROSS else State.ZERO_WON

        elif not self.__winner_checker.got_winner(self.__game_board) and self.__no_empty_cells_left():
            self.__state = State.DRAW

        return self.__state
