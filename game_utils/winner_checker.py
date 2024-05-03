from config.basic_config import settings
from typing import List
from game_utils.cells import Cell


class WinnerChecker:

    @staticmethod
    def _get_diagonals(game_board) -> List[List[Cell]]:
        diagonals = []
        for i in range(len(game_board)):
            diagonal1 = [game_board[j][j + i] for j in range(len(game_board) - i)]
            diagonals.append(diagonal1)
        for i in range(len(game_board)):
            diagonal2 = [game_board[j][len(game_board) - 1 - i - j] for j in range(len(game_board) - i)]
            diagonals.append(diagonal2)
        for i in range(len(game_board)):
            diagonal3 = [game_board[len(game_board) - 1 - j][i + j] for j in range(len(game_board) - i)]
            diagonals.append(diagonal3)
        for i in range(len(game_board)):
            diagonal4 = [game_board[len(game_board) - 1 - j][len(game_board) - 1 - i - j] for j in
                         range(len(game_board) - i)]
            diagonals.append(diagonal4)
        return diagonals

    @staticmethod
    def _get_columns(game_board) -> List[List[Cell]]:
        columns = [[game_board[j][i] for j in range(len(game_board))] for i in range(len(game_board))]
        return columns

    @staticmethod
    def _get_rows(game_board) -> List[List[Cell]]:
        return game_board

    @staticmethod
    def _line_has_winner(line: List[Cell]) -> None | Cell:
        count = 0
        prev_cell = None
        for cell in line:
            if cell == prev_cell and cell != Cell.EMPTY:
                count += 1
                if count == settings.game_settings.victory_condition.value - 1:
                    return cell
            else:
                count = 0
            prev_cell = cell
        return None

    @staticmethod
    def got_winner(game_board: list) -> None | Cell:
        lines = WinnerChecker._get_rows(game_board) + \
                WinnerChecker._get_columns(game_board) + \
                WinnerChecker._get_diagonals(game_board)
        for line in lines:
            winner = WinnerChecker._line_has_winner(line)
            if winner:
                return winner
        return None
