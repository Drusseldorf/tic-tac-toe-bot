from enum import Enum
from data_base.tables import GameSession
from exceptions.illegal_move import IllegalMove
from game_utils.cells import Cell
from game_utils.make_move import Move


class MoveResult(Enum):
    SUCCESS = True
    FALSE = False


class MoveHandler:
    def __init__(self, pos_x: str, pos_y: str, user_who_triggered: str, game_session: GameSession):
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._user_who_triggered = str(user_who_triggered)
        self._game_session = game_session
        self._move = Move(self._game_session.game_board)

    def _get_initiating_move_cell(self) -> Cell:
        if not self._game_session.is_online:
            return self._move.whos_turn()
        cell = self._game_session.user_one_cell if self._user_who_triggered == self._game_session.user_one_id else self._game_session.user_two_cell
        return getattr(Cell, cell)

    def make_move(self) -> MoveResult:
        try:
            new_position_on_board = self._move.make(self._pos_x, self._pos_y, self._get_initiating_move_cell())
        except IllegalMove:
            return MoveResult.FALSE
        self._game_session.game_board = new_position_on_board
        return MoveResult.SUCCESS
