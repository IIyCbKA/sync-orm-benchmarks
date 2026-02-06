from sqlmodel import create_engine, Session, select, literal
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_NAME = os.getenv('POSTGRES_DB')
DB_PORT = os.getenv('POSTGRES_PORT')

DATABASE_URL = f'postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DEBUG = 'debug' if os.environ.get('DEBUG', 'False') == 'True' else False

engine = create_engine(DATABASE_URL, echo=DEBUG, future=True)


class PreconnectedSession(Session):
  def __enter__(self):
    session = super().__enter__()
    session.exec(select(literal(1)))
    session.rollback()
    return session


SessionLocal = sessionmaker(
  bind=engine,
  class_=PreconnectedSession,
  autoflush=False,
  expire_on_commit=False,
  future=True
)
