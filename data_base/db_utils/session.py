from data_base.db_engine import SessionLocal
from data_base.tables import GameSession
from uuid import uuid4
from contextlib import contextmanager
from game_utils.field import GameBoard
from datetime import datetime, timedelta


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
    def new(user_1_id: str, user_2_id: str | None = None) -> GameSession:
        game_board = GameBoard.get_new_game_board()
        with Session._get_db_session() as db:
            session_id = str(uuid4())
            game_session = GameSession(game_board=game_board,
                                       game_session=session_id,
                                       user_one_id=user_1_id,
                                       user_two_id=user_2_id)
            db.add(game_session)
            print(datetime.now(), 'Session.new')
            return game_session

    @staticmethod
    def get_game_session(session_id) -> GameSession:
        with Session._get_db_session() as db:
            session = db.query(GameSession).filter(GameSession.game_session == session_id).first()

            print(datetime.now(), 'get_game_session')
            return session

    @staticmethod
    def update_session(game_session: GameSession):
        with Session._get_db_session() as db:
            game_session.last_updated = datetime.now()
            db.add(game_session)
            db.commit()
            db.refresh(game_session)
            print(datetime.now(), 'update_session')

    @staticmethod
    def delete_session(game_session: GameSession):
        with Session._get_db_session() as db:
            db.delete(game_session)
            db.commit()
            print(datetime.now(), 'delete_session')

    @staticmethod
    def delete_sessions_older_than(timeout: timedelta):
        threshold_time = datetime.now() - timeout
        with Session._get_db_session() as db:
            sessions_to_delete = db.query(GameSession).filter(GameSession.last_updated < threshold_time).all()
            for session in sessions_to_delete:
                print(f'Удаляется сессию с id: {session.game_session}')
                db.delete(session)
            db.commit()
