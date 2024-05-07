from data_base.db_utils.session import Session
from data_base.tables import GameSession
from game_utils.game_state_handler import State, GameState
from exceptions.session_not_exists import SessionDoesntExist


class GameSessionController:
    def __init__(self, session: GameSession | str):
        """
    Args:
        session (GameSession | str): GameSession instanse or game session id
    """
        self._game_session = session
        if not isinstance(self._game_session, GameSession):
            self._game_session = Session.get_game_session(session)

    def handle_state(self):
        if GameState(game_board=self._game_session.game_board).state is State.IN_PROGRESS:
            Session.update_session(self._game_session)
        else:
            Session.delete_session(self._game_session)

    def get_session(self) -> GameSession:
        if not self._game_session:
            raise SessionDoesntExist
        return self._game_session
