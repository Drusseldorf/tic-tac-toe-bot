from data_base.db_engine import SessionLocal
from data_base.tables import GameSession
from uuid import uuid4
from contextlib import contextmanager


class Session:

    @staticmethod
    @contextmanager
    def _get_db_session():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def new(game_board: str, user_1_id: str, user_2_id: str | None = None) -> str:
        with Session._get_db_session() as db:
            session_id = str(uuid4())
            game_session = GameSession(game_board=game_board,
                                       game_session=session_id,
                                       user_one_id=user_1_id,
                                       user_two_id=user_2_id)
            db.add(game_session)
            db.commit()
            return session_id

    @staticmethod
    def _get_game_session(session_id):
        with Session._get_db_session() as db:
            return db.query(GameSession).filter(GameSession.game_session == session_id).first()

    @staticmethod
    def update_board(session_id, game_board: str):
        with Session._get_db_session() as db:
            game_session = Session._get_game_session(session_id)
            game_session.game_board = game_board
            db.add(game_session)
            db.commit()
            db.refresh(game_session)

    @staticmethod
    def get_board(session_id) -> str:
        game_session = Session._get_game_session(session_id)
        return game_session.game_board

    @staticmethod
    def delete_session(session_id):
        with Session._get_db_session() as db:
            game_session = Session._get_game_session(session_id)
            db.delete(game_session)
            db.commit()

    @staticmethod
    def get_last_message(session_id):
        with Session._get_db_session() as db:
            game_session = Session._get_game_session(session_id)
            return game_session.last_message_id_user_one

    @staticmethod
    def set_last_message(session_id, message_id):
        with Session._get_db_session() as db:
            game_session = Session._get_game_session(session_id)
            game_session.last_message_id_user_one = message_id
            db.add(game_session)
            db.commit()
            db.refresh(game_session)
