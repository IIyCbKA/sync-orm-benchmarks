from dotenv import load_dotenv
from psycopg_pool import ConnectionPool
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")

pool = ConnectionPool(
    conninfo=f'dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}',
    min_size=1,
    max_size=25,
    timeout=30,
    max_lifetime=3600,
    max_idle=600,
)

def get_connection():
    return pool.getconn()
