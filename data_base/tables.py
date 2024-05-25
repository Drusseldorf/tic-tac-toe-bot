from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, PickleType
from data_base.engine import engine
from game_core.cells import Cell

Base = declarative_base()


class GameSession(Base):
    __tablename__ = 'game_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_one_id = Column(String)
    user_one_chat_id = Column(String)
    user_two_id = Column(String)
    user_two_chat_id = Column(String)
    session_uuid = Column(String, unique=True, index=True)
    game_board = Column(PickleType)
    last_message_id_user_one = Column(String)
    last_message_id_user_two = Column(String)
    is_online = Column(Boolean)
    user_one_cell = Column(Enum(Cell))
    user_two_cell = Column(Enum(Cell))
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LinkedUsers(Base):
    __tablename__ = 'linked_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    linked_users_id = Column(String)
    

Base.metadata.create_all(bind=engine)
