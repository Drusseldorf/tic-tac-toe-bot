from data_base.db_engine import SessionLocal
from data_base.tables import GameSession
from uuid import uuid4
from contextlib import contextmanager
from game_utils.field import GameBoard


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
    def new(user_1_id: str, user_2_id: str | None = None) -> str:
        game_board = GameBoard.get_new_game_board()
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
    def get_game_session(session_id) -> GameSession:
        with Session._get_db_session() as db:
            session = db.query(GameSession).filter(GameSession.game_session == session_id).first()
            return session

    @staticmethod
    def update_session(game_session: GameSession):
        with Session._get_db_session() as db:
            db.add(game_session)
            db.commit()
            db.refresh(game_session)

    @staticmethod
    def delete_session(game_session: GameSession):
        with Session._get_db_session() as db:
            db.delete(game_session)
            db.commit()
