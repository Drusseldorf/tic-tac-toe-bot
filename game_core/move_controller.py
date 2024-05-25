from game_core.cells import Cell
from exceptions.illegal_move import IllegalMove
from game_core.game_board import GameBoard


class MoveController:

    def __init__(self, game_board: GameBoard):
        self._gb = game_board

    def whos_turn(self) -> Cell:
        count_entities = 0
        for row in self._gb.game_board:
            for cell in row:
                if cell is not Cell.EMPTY:
                    count_entities += 1
        return Cell.CROSS if count_entities % 2 == 0 else Cell.ZERO

    def last_turn(self) -> Cell:
        return Cell.CROSS if self.whos_turn() is Cell.ZERO else Cell.ZERO

    def make_move(self, pos_x: int, pos_y: int, initiator_cell: Cell) -> None:
        """
        :raise IllegalMove if move is not possible
        """
        if not self._is_move_possible(pos_x, pos_y, initiator_cell):
            raise IllegalMove
        else:
            self._gb.game_board[pos_x][pos_y] = self.whos_turn()

    def _is_move_possible(self, pos_x: int, pos_y: int, initiator_cell: Cell) -> bool:
        return self._gb.game_board[pos_x][pos_y] is Cell.EMPTY and initiator_cell is self.whos_turn()
