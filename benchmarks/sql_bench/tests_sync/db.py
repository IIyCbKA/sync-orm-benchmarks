from dotenv import load_dotenv
import atexit
import os
import psycopg

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")

CONNINFO = (
    f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} "
    f"host={DB_HOST} port={DB_PORT}"
)

conn = psycopg.connect(CONNINFO, autocommit=True, prepare_threshold=0)

@atexit.register
def _close():
    try:
        conn.close()
    except Exception:
        pass
