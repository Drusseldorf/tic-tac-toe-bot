from data_base.db_engine import Base, engine
from sqlalchemy import Column, Integer, String, Boolean


class GameSession(Base):
    __tablename__ = 'game_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_one_id = Column(String)
    user_one_chat_id = Column(String)
    user_two_id = Column(String)
    user_two_chat_id = Column(String)
    game_session = Column(String, unique=True, index=True)
    game_board = Column(String)
    last_message_id_user_one = Column(String)
    last_message_id_user_two = Column(String)
    is_online = Column(Boolean)
    user_one_cell = Column(String)
    user_two_cell = Column(String)
    last_updated = Column(String)


class LinkedUsers(Base):
    __tablename__ = 'linked_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    linked_users_id = Column(String)


Base.metadata.create_all(bind=engine)
