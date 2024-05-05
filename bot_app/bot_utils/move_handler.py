from data_base.db_utils.session import Session
from data_base.tables import GameSession
from exceptions.illegal_move import IllegalMove
from game_utils.make_move import Move


class MoveHandler:
    def __init__(self, pos_x: str, pos_y: str, game_session: GameSession):
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._game_session = game_session

    def make_move(self):
        try:
            new_position_on_board = Move(self._game_session.game_board).make(self._pos_x, self._pos_y)
            self._game_session.game_board = new_position_on_board
            Session.update_session(self._game_session)
        except IllegalMove:
            return
