import pickle
from uuid import uuid4
import random
from data_base.db_utils.table_structures import GameSessionData
from data_base.session_operations import SessionOperations
from data_base.tables import GameSession
from game_core.cells import Cell
from game_core.game_board import GameBoard
from game_core.game_state_checker import State, GameState
from exceptions.session_not_exist import SessionDoesntExist


class GameSessionController:
    def __init__(self, session: GameSession | str):
        """
        Args:
            session (GameSession | str): GameSession ORM instanse or game session id as string
        """
        self._game_session = session
        if not isinstance(self._game_session, GameSession):
            self._game_session = SessionOperations.get_game_session(session)

    @staticmethod
    def start_new_session(user_one_id: str, user_one_chat_id: str,
                          is_online: bool, user_two_id: str | None = None,
                          user_two_chat_id: str | None = None) -> GameSession:
        """
        Creates new game session in DB
        """
        game_board_bytes = pickle.dumps(GameBoard())
        user_one_cell = random.choice([Cell.ZERO, Cell.CROSS])
        user_two_cell = Cell.CROSS if user_one_cell is Cell.ZERO else Cell.ZERO
        game_session_data = GameSessionData(user_one_id=user_one_id, user_one_chat_id=user_one_chat_id,
                                            game_board=game_board_bytes, session_uuid=str(uuid4()),
                                            is_online=is_online, user_two_id=user_two_id,
                                            user_two_chat_id=user_two_chat_id, user_one_cell=user_one_cell,
                                            user_two_cell=user_two_cell)
        return SessionOperations.new_game_session(game_session_data)

    def update_game_session(self):
        """
        Updating game session in the DB or deleting it if the game is over
        """
        game_board_obj = pickle.loads(self._game_session.game_board)
        if GameState(game_board_obj).state is State.IN_PROGRESS:
            SessionOperations.update_session(self._game_session)
        else:
            SessionOperations.delete_session(self._game_session)

    def get_session(self) -> GameSession:
        """
        Raises: SessionDoesntExist: If there is no game session
        :returns:
            GameSession: ORM object representing game session
        """
        if not self._game_session:
            raise SessionDoesntExist
        return self._game_session
