from pathlib import Path
from sqlalchemy import create_engine


DB_DIR = Path(__file__).parent.resolve()
DB_NAME = 'app.db'
SQLLITE_DB_PATH = DB_DIR.joinpath(DB_NAME)

SQLALCHEMY_DATABASE_URL = f'sqlite:///{SQLLITE_DB_PATH}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
