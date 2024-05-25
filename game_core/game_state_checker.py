from game_core.game_states import State
from game_core.cells import Cell
from game_core.winner_checker import WinnerChecker
from game_core.game_board import GameBoard


class GameState:
    def __init__(self, game_board: GameBoard):
        self._gb = game_board
        self._state = None

    def _no_empty_cells_left(self) -> bool:
        for row in self._gb.game_board:
            for cell in row:
                if cell is Cell.EMPTY:
                    return False
        return True

    @property
    def state(self) -> State:
        """
        Returns: State type that defines game state.
        """
        win_check = WinnerChecker(self._gb)
        if self._no_empty_cells_left() and not win_check.got_winner():
            self._state = State.DRAW
        elif not win_check.got_winner() and not self._no_empty_cells_left():
            self._state = State.IN_PROGRESS
        else:
            winner = win_check.got_winner()
            self._state = State.CROSS_WON if winner is Cell.CROSS else State.ZERO_WON
        return self._state
