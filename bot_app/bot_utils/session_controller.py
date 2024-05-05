from data_base.db_utils.session import Session
from data_base.tables import GameSession
from game_utils.game_state_handler import State, GameState


class SessionController:
    def __init__(self, session_id: str):
        self._session_id = session_id
        self._game_session = Session.get_game_session(self._session_id)

    def _get_game_state(self) -> State:
        return GameState(game_board=self._game_session.game_board).state

    def _game_session_last_message_and_delete_contoller(self, sent):
        self._game_session.last_message_id_user_one = sent.message_id
        Session.update_session(self._game_session)
        if self._get_game_state() is not State.IN_PROGRESS:
            Session.delete_session(self._game_session)

    def handle_state(self, sent):
        self._game_session_last_message_and_delete_contoller(sent)

    def get_session(self) -> GameSession:
        return self._game_session
