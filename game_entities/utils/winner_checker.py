from config.basic_config import settings
from typing import List
from game_entities.cells import Cell


class WinnerChecker:

    @staticmethod
    def __get_diagonals(game_board) -> List[List[Cell]]:
        diagonals = [[game_board[i][i] for i in range(len(game_board))],
                     [game_board[i][len(game_board) - 1 - i] for i in range(len(game_board))]]
        return diagonals

    @staticmethod
    def __get_columns(game_board) -> List[List[Cell]]:
        columns = [[game_board[j][i] for j in range(len(game_board))] for i in range(len(game_board))]
        return columns

    @staticmethod
    def __get_rows(game_board) -> List[List[Cell]]:
        return game_board

    @staticmethod
    def __line_has_winner(line: List[Cell]) -> None | Cell:
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
        lines = WinnerChecker.__get_rows(game_board) + \
                WinnerChecker.__get_columns(game_board) + \
                WinnerChecker.__get_diagonals(game_board)
        for line in lines:
            winner = WinnerChecker.__line_has_winner(line)
            if winner:
                return winner
        return None
