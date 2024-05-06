from enum import Enum
from game_utils.cells import Cell
from game_utils.winner_checker import WinnerChecker
from game_utils.field import GameBoard


class State(Enum):
    DRAW = 0
    CROSS_WON = 1
    ZERO_WON = 2
    IN_PROGRESS = 3


class GameState:

    def __init__(self, game_board: str):
        self._state: State | None = None
        self._game_board = GameBoard.turn_into_list(game_board)
        self._winner_checker = WinnerChecker()

    def _no_empty_cells_left(self) -> bool:
        result = True
        for row in self._game_board:
            for cell in row:
                if cell == Cell.EMPTY:
                    result = False
        return result

    @property
    def state(self):
        if self._no_empty_cells_left() and not self._winner_checker.got_winner(self._game_board):
            self._state = State.DRAW

        elif not self._winner_checker.got_winner(self._game_board) and not self._no_empty_cells_left():
            self._state = State.IN_PROGRESS

        else:
            winner = self._winner_checker.got_winner(self._game_board)
            self._state = State.CROSS_WON if winner is Cell.CROSS else State.ZERO_WON

        return self._state
