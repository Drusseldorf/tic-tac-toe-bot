from contextlib import contextmanager
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from data_base.tables import GameSession, LinkedUsers
from data_base.engine import engine
from data_base.db_utils.table_structures import GameSessionData
from logger.logger import log, Level


SessionLocal = sessionmaker(autoflush=False, bind=engine)


class SessionOperations:

    @staticmethod
    @contextmanager
    def _get_db_session():
        db = SessionLocal()
        try:
            yield db
        except Exception as e:
            log.write(Level.ERROR, f'DB ERROR: {e}')
        finally:
            db.close()

    @staticmethod
    def new_game_session(data: GameSessionData) -> GameSession:
        with SessionOperations._get_db_session() as db:
            game_session = GameSession(game_board=data.game_board,
                                       session_uuid=data.session_uuid,
                                       user_one_id=data.user_one_id,
                                       user_one_chat_id=data.user_one_chat_id,
                                       user_two_id=data.user_two_id,
                                       user_two_chat_id=data.user_two_chat_id,
                                       is_online=data.is_online,
                                       user_one_cell=data.user_one_cell,
                                       user_two_cell=data.user_two_cell)
            db.add(game_session)
            db.commit()
            db.refresh(game_session)
            log.write(Level.INFO, f'new session was created with id: {data.session_uuid}')
            return game_session

    @staticmethod
    def get_game_session(session_id: str) -> GameSession:
        with SessionOperations._get_db_session() as db:
            log.write(Level.INFO, f'get_game_session was called for id: {session_id}')
            session = db.query(GameSession).filter(GameSession.session_uuid == session_id).first()
            return session

    @staticmethod
    def update_session(game_session: GameSession):
        with SessionOperations._get_db_session() as db:
            log.write(Level.INFO, f'update_session was called for id: {game_session.session_uuid}')
            db.add(game_session)
            db.commit()
            db.refresh(game_session)

    @staticmethod
    def delete_session(game_session: GameSession):
        with SessionOperations._get_db_session() as db:
            log.write(Level.INFO, f'delete_session was called with id: {game_session.session_uuid}')
            db.delete(game_session)
            db.commit()

    @staticmethod
    def delete_sessions_older_than(timeout: timedelta):
        threshold_time = datetime.utcnow() - timeout
        log.write(Level.INFO, f'delete_sessions_older_than was called with timedelta: {timeout}')
        with SessionOperations._get_db_session() as db:
            sessions_to_delete = db.query(GameSession).filter(GameSession.last_updated < threshold_time).all()
            for session in sessions_to_delete:
                log.write(Level.INFO, f'deleting game session with id: {session.session_uuid}')
                db.delete(session)
            db.commit()

    @staticmethod
    def get_linked_users_session(user_id: str) -> LinkedUsers:
        with SessionOperations._get_db_session() as db:
            linked_users_session = db.query(LinkedUsers).filter(LinkedUsers.user_id == user_id).first()
            log.write(Level.INFO, f'get_linked_users_session was called for userID: {user_id}')
            return linked_users_session

    @staticmethod
    def update_linked_users(session: LinkedUsers):
        with SessionOperations._get_db_session() as db:
            log.write(Level.INFO, f'update_linked_users was called for userID: {session.user_id}')
            db.add(session)
            db.commit()
            db.refresh(session)

    @staticmethod
    def new_linked_users(user_id: str):
        with SessionOperations._get_db_session() as db:
            log.write(Level.INFO, f'new_linked_users was called fo userID: {user_id}')
            session = LinkedUsers(user_id=user_id)
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
