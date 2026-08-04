from django.db import connection
from pg_manager import PgServerTimer
from typing import Any, Sequence

def execute(sql: str, params: Sequence[Any] | None) -> list[tuple]:
  connection.ensure_connection()
  if connection.in_atomic_block or not connection.get_autocommit():
    raise RuntimeError('PostgreSQL timer requires an idle connection')

  with connection.cursor() as cursor:
    cursor.execute(sql, params)
    return cursor.fetchall() if cursor.description else []


pg_timer = PgServerTimer(execute)
