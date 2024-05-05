from data_base.db_engine import Base, engine
from sqlalchemy import Column, Integer, String


class GameSession(Base):
    __tablename__ = 'game_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_one_id = Column(String)
    user_two_id = Column(String)
    game_session = Column(String, unique=True, index=True)
    game_board = Column(String)
    last_message_id_user_one = Column(String)
    last_message_id_user_two = Column(String)
    last_updated = Column(String)


Base.metadata.create_all(bind=engine)
