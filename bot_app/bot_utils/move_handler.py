from enum import Enum
from data_base.tables import GameSession
from exceptions.illegal_move import IllegalMove
from game_utils.make_move import Move


class MoveResult(Enum):
    SUCCESS = True
    FALSE = False


class MoveHandler:
    def __init__(self, pos_x: str, pos_y: str, game_session: GameSession):
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._game_session = game_session

    def make_move(self) -> MoveResult:
        try:
            new_position_on_board = Move(self._game_session.game_board).make(self._pos_x, self._pos_y)
        except IllegalMove:
            return MoveResult.FALSE
        self._game_session.game_board = new_position_on_board
        return MoveResult.SUCCESS
