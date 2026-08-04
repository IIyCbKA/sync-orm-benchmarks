from .database import db
from pg_manager import PgServerTimer, dbapi_execute
from typing import Any, Sequence

def execute(sql: str, params: Sequence[Any] | None) -> list[tuple]:
  return dbapi_execute(db.connection(), sql, params)


pg_timer = PgServerTimer(execute)
