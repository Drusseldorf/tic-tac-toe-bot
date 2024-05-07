from game_utils.cells import Cell
from exceptions.illegal_move import IllegalMove
from game_utils.field import GameBoard


class Move:

    def __init__(self, game_board: str):
        self.game_board = GameBoard.turn_into_list(game_board)

    def _is_possible(self, pos_x, pos_y, cell_trying_to_move: Cell) -> bool:
        return self.game_board[pos_x][pos_y] is Cell.EMPTY and cell_trying_to_move is self.whos_turn()

    def whos_turn(self) -> Cell:
        count_entities = 0

        for row in self.game_board:
            for cell in row:
                if cell != Cell.EMPTY:
                    count_entities += 1

        return Cell.CROSS if count_entities % 2 == 0 else Cell.ZERO

    def last_turn(self) -> Cell:
        count_entities = 0

        for row in self.game_board:
            for cell in row:
                if cell != Cell.EMPTY:
                    count_entities += 1

        return Cell.CROSS if count_entities % 2 != 0 else Cell.ZERO

    def make(self, pos_x, pos_y, cell_trying_to_move: Cell):
        x, y = int(pos_x), int(pos_y)
        if not self._is_possible(x, y, cell_trying_to_move):
            raise IllegalMove
        else:
            self.game_board[x][y] = self.whos_turn()
        return GameBoard.turn_into_str(self.game_board)
