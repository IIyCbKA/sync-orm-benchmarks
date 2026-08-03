from __future__ import annotations
from dataclasses import dataclass
from statistics import median
from typing import Any, Callable, Sequence

Executor = Callable[[str, Sequence[Any] | None], list[tuple]]

_FLUSH_SQL = """
SELECT
  pg_stat_force_next_flush(),
  (SELECT query_id FROM pg_stat_get_activity(pg_backend_pid()))
"""

_SNAPSHOT_SQL = """
WITH totals AS (
  SELECT
    coalesce(sum(total_plan_time + total_exec_time), 0.0) AS query_ms,
    coalesce(sum(calls), 0) AS calls
  FROM pg_stat_statements
  WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
    AND userid = (SELECT oid FROM pg_roles WHERE rolname = current_user)
    AND queryid IS NOT NULL
    AND queryid <> ALL (%s::bigint[])
)
SELECT
  pg_backend_pid(),
  totals.query_ms,
  totals.calls,
  coalesce((
    SELECT sum(coalesce(write_time, 0) + coalesce(fsync_time, 0))
    FROM pg_stat_get_backend_io(pg_backend_pid())
    WHERE object = 'wal'
  ), 0.0),
  (SELECT query_id FROM pg_stat_get_activity(pg_backend_pid()))
FROM totals
"""


@dataclass(frozen=True)
class PgSample:
  total_ns: int
  query_ns: int
  wal_ns: int
  calls: int


@dataclass(frozen=True)
class _Snapshot:
  pid: int
  query_ms: float
  wal_ms: float
  calls: int


class PgServerTimer:
  def __init__(
    self,
    execute: Executor,
    finish: Callable[[], None] | None = None,
  ) -> None:
    self._execute = execute
    self._finish = finish or (lambda: None)
    self._probe_ids: set[int] = set()
    self._prepared = False
    self._start: _Snapshot | None = None
    self.samples: list[PgSample] = []

  def _remember(self, query_id: Any) -> None:
    if query_id is not None:
      self._probe_ids.add(int(query_id))

  def _snapshot(self) -> _Snapshot:
    self._remember(self._execute(_FLUSH_SQL, None)[0][1])
    row = self._execute(_SNAPSHOT_SQL, [sorted(self._probe_ids)])[0]
    self._remember(row[4])
    return _Snapshot(
      pid=int(row[0]),
      query_ms=float(row[1]),
      calls=int(row[2]),
      wal_ms=float(row[3]),
    )

  def _prepare(self) -> None:
    if self._prepared:
      return
    self._execute('CREATE EXTENSION IF NOT EXISTS pg_stat_statements', None)
    self._snapshot()
    self._snapshot()
    self._prepared = True

  def reset(self) -> None:
    if self._start is not None:
      raise RuntimeError('PostgreSQL timer is already running')
    self._prepare()
    self._start = self._snapshot()

  def collect(self) -> int:
    start = self._start
    if start is None:
      raise RuntimeError('PostgreSQL timer was not started')

    self._finish()
    end = self._snapshot()
    self._start = None

    if end.pid != start.pid:
      raise RuntimeError('PostgreSQL connection changed during measurement')

    query_ns = round((end.query_ms - start.query_ms) * 1_000_000)
    wal_ns = round((end.wal_ms - start.wal_ms) * 1_000_000)
    calls = end.calls - start.calls

    if query_ns < 0 or wal_ns < 0 or calls < 0:
      raise RuntimeError('PostgreSQL statistics changed during measurement')

    sample = PgSample(query_ns + wal_ns, query_ns, wal_ns, calls)
    self.samples.append(sample)
    return sample.total_ns

  def median_ns(self) -> int | float:
    return median(sample.total_ns for sample in self.samples)

  def median_query_ns(self) -> int | float:
    return median(sample.query_ns for sample in self.samples)

  def median_wal_ns(self) -> int | float:
    return median(sample.wal_ns for sample in self.samples)

  def median_calls(self) -> int | float:
    return median(sample.calls for sample in self.samples)


def unwrap_connection(connection: Any) -> Any:
  if hasattr(connection, 'info'):
    return connection
  for name in ('driver_connection', 'dbapi_connection', 'connection'):
    inner = getattr(connection, name, None)
    if inner is not None and hasattr(inner, 'info'):
      return inner
  raise TypeError(f'Unsupported connection: {type(connection)!r}')


def dbapi_execute(
  connection: Any,
  sql: str,
  params: Sequence[Any] | None,
) -> list[tuple]:
  connection = unwrap_connection(connection)
  if int(connection.info.transaction_status) != 0:
    raise RuntimeError('PostgreSQL timer requires an idle connection')

  restore = not connection.autocommit
  if restore:
    connection.autocommit = True
  try:
    with connection.cursor() as cursor:
      cursor.execute(sql, params)
      return cursor.fetchall() if cursor.description else []
  finally:
    if restore:
      connection.autocommit = False


class SessionPgTimer(PgServerTimer):
  def __init__(self) -> None:
    self._session = None
    super().__init__(self._execute, self._finish)

  def reset(self, session: Any) -> None:
    self._session = session
    super().reset()

  def collect(self) -> int:
    try:
      return super().collect()
    finally:
      if self._session is not None and self._session.in_transaction():
        self._session.rollback()
      self._session = None

  def _connection(self) -> Any:
    if self._session is None:
      raise RuntimeError('PostgreSQL timer has no ORM session')
    return unwrap_connection(self._session.connection().connection)

  def _execute(
    self,
    sql: str,
    params: Sequence[Any] | None,
  ) -> list[tuple]:
    return dbapi_execute(self._connection(), sql, params)

  def _finish(self) -> None:
    if self._session is not None and self._session.in_transaction():
      self._session.rollback()
