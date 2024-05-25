from config.basic_config import settings
from game_core.cells import Cell


class GameBoard:
    def __init__(self, board_size: int = settings.game_settings.game_board_default_size):
        self._game_board = [[Cell.EMPTY for _ in range(board_size)] for _ in range(board_size)]

    @property
    def game_board(self) -> list[list[Cell]]:
        return self._game_board

    @game_board.setter
    def game_board(self, game_board: list[list[Cell]]):
        self._game_board = game_board
