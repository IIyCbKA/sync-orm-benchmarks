from .models import db
from pg_manager import PgServerTimer, dbapi_execute, unwrap_connection
from pony.orm import rollback
from typing import Any, Sequence

def execute(sql: str, params: Sequence[Any] | None) -> list[tuple]:
  return dbapi_execute(db.get_connection(), sql, params)


def finish() -> None:
  connection = unwrap_connection(db.get_connection())
  if int(connection.info.transaction_status) != 0:
    rollback()


pg_timer = PgServerTimer(execute, finish)
