from config.basic_config import settings
from typing import List
from game_core.cells import Cell
from game_core.game_board import GameBoard


class WinnerChecker:
    def __init__(self, game_board: GameBoard):
        self._gb = game_board

    def got_winner(self) -> bool | Cell:
        """
        :return:
            Cell: Cell type (CROSS or ZERO) that has won if a winner is found.
            bool: False if there is no winner.
        """
        lines = self._get_rows(self._gb.game_board) + \
            self._get_columns(self._gb.game_board) + \
            self._get_diagonals(self._gb.game_board)
        for line in lines:
            winner = self._line_has_winner(line)
            if winner:
                return winner
        return False

    @staticmethod
    def _get_diagonals(game_board: List[List[Cell]]) -> List[List[Cell]]:
        n = len(game_board)
        diagonals = []
        for i in range(n):
            diagonals.append([game_board[j][j + i] for j in range(n - i)])
            if i != 0:
                diagonals.append([game_board[j + i][j] for j in range(n - i)])
        for i in range(n):
            diagonals.append([game_board[j][n - 1 - j - i] for j in range(n - i)])
            if i != 0:
                diagonals.append([game_board[j + i][n - 1 - j] for j in range(n - i)])
        return diagonals

    @staticmethod
    def _get_columns(game_board: List[List[Cell]]) -> List[List[Cell]]:
        columns = [[game_board[j][i] for j in range(len(game_board))] for i in range(len(game_board))]
        return columns

    @staticmethod
    def _get_rows(game_board: List[List[Cell]]) -> List[List[Cell]]:
        return game_board

    @staticmethod
    def _line_has_winner(line: List[Cell]) -> Cell | None:
        count = 0
        prev_cell = None
        for cell in line:
            if cell is prev_cell and cell is not Cell.EMPTY:
                count += 1
                if count == settings.game_settings.victory_condition - 1:
                    return cell
            else:
                count = 0
            prev_cell = cell
        return None
