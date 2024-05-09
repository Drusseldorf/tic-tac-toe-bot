import random

from data_base.db_engine import SessionLocal
from data_base.tables import GameSession, LinkedUsers
from uuid import uuid4
from contextlib import contextmanager

from game_utils.cells import Cell
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
    def new(user1_id: str, user1_chat_id: str, is_online: bool,
            user2_id: str | None = None, user2_chat_id: str | None = None) -> GameSession:
        game_board = GameBoard.get_new_game_board()
        with Session._get_db_session() as db:
            session_id = str(uuid4())
            if is_online:
                cell1 = random.choice([Cell.CROSS, Cell.ZERO]).name
                cell2 = Cell.CROSS.name if cell1 != Cell.CROSS.name else Cell.ZERO.name
            else:
                cell1 = None
                cell2 = None

            game_session = GameSession(game_board=game_board,
                                       game_session=session_id,
                                       user_one_id=user1_id,
                                       user_one_chat_id=user1_chat_id,
                                       user_two_id=user2_id,
                                       user_two_chat_id=user2_chat_id,
                                       is_online=is_online,
                                       user_one_cell=cell1,
                                       user_two_cell=cell2)
            db.add(game_session)
            print(datetime.now(), 'create new session')
            return game_session

    @staticmethod
    def get_game_session(session_id) -> GameSession:
        with Session._get_db_session() as db:
            session = db.query(GameSession).filter(GameSession.game_session == session_id).first()
            print(datetime.now(), 'get game session')
            return session

    @staticmethod
    def update_session(game_session: GameSession):
        with Session._get_db_session() as db:
            game_session.last_updated = datetime.now()
            db.add(game_session)
            db.commit()
            db.refresh(game_session)
            print(datetime.now(), 'update session')

    @staticmethod
    def delete_session(game_session: GameSession):
        with Session._get_db_session() as db:
            db.delete(game_session)
            db.commit()
            print(datetime.now(), 'delete session')

    @staticmethod
    def delete_sessions_older_than(timeout: timedelta):
        threshold_time = datetime.now() - timeout
        with Session._get_db_session() as db:
            sessions_to_delete = db.query(GameSession).filter(GameSession.last_updated < threshold_time).all()
            for session in sessions_to_delete:
                print(f'deleting session with id: {session.game_session}')
                db.delete(session)
            db.commit()

    @staticmethod
    def get_linked_users_session(user_id: str) -> LinkedUsers:
        with Session._get_db_session() as db:
            linked_users_session = db.query(LinkedUsers).filter(LinkedUsers.user_id == user_id).first()
            print(datetime.now(), 'get_linked_users')
            return linked_users_session

    @staticmethod
    def update_linked_users(session: LinkedUsers):
        with Session._get_db_session() as db:
            db.add(session)
            db.commit()
            db.refresh(session)
            print(datetime.now(), 'set_new_user fo linked users')

    @staticmethod
    def new_linked_users(user_id: str):
        with Session._get_db_session() as db:
            session = LinkedUsers(user_id=user_id)
            db.add(session)
            db.commit()
            db.refresh(session)
            print(datetime.now(), 'new_linked_user created')
            return session
