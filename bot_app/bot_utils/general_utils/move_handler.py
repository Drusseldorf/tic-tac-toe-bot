import pickle
from enum import Enum
from data_base.tables import GameSession
from exceptions.illegal_move import IllegalMove
from game_core.cells import Cell
from game_core.move_controller import MoveController


class MoveResult(Enum):
    SUCCESS = True
    FALSE = False


class MoveHandler:
    def __init__(self, pos_x: str, pos_y: str, user_who_triggered: str, game_session: GameSession):
        self._pos_y = int(pos_y)
        self._pos_x = int(pos_x)
        self._user_who_triggered = str(user_who_triggered)
        self._game_session = game_session
        self._game_board_obj = pickle.loads(self._game_session.game_board)
        self._move_controller = MoveController(self._game_board_obj)

    def make_move(self) -> MoveResult:
        try:
            self._move_controller.make_move(self._pos_x, self._pos_y, self._get_initiating_move_cell())
            self._game_session.game_board = pickle.dumps(self._game_board_obj)
        except IllegalMove:
            return MoveResult.FALSE
        return MoveResult.SUCCESS

    def _get_initiating_move_cell(self) -> Cell:
        if not self._game_session.is_online:
            return self._move_controller.whos_turn()
        cell = self._game_session.user_one_cell if self._user_who_triggered == self._game_session.user_one_id \
            else self._game_session.user_two_cell
        return cell
