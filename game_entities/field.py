from config.basic_config import settings
from game_entities.cells import Cell
import json


class GameBoard:

    @staticmethod
    def get_new_game_board() -> str:
        size = settings.game_settings.game_board_default_size
        game_board = [[Cell.EMPTY.name for _ in range(size)] for _ in range(size)]
        return json.dumps(game_board)

    @staticmethod
    def turn_into_list(game_board: str) -> list:
        board_list = json.loads(game_board)
        new_board = []
        for row in board_list:
            new_row = [getattr(Cell, cell) for cell in row]
            new_board.append(new_row)
        return new_board

    @staticmethod
    def turn_into_str(game_board: list) -> str:
        new_board = []
        for row in game_board:
            new_row = [cell.name for cell in row]
            new_board.append(new_row)
        return json.dumps(new_board)

