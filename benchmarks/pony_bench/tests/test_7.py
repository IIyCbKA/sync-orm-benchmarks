from pony.orm import db_session, select
from core.models import Ticket, db
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


@db_session
def select_iteration() -> tuple[int, int]:
  """
  order_by(1) equal order_by(ticket_no) in primitive notation
  """
  db.get_connection()

  pg_timer.reset()
  start = time.perf_counter_ns()

  results = list(select((
    t.ticket_no,
    t.book_ref.book_ref,
    t.passenger_id,
    t.passenger_name,
    t.outbound,
    t.book_ref.book_ref,
    t.book_ref.book_date,
    t.book_ref.total_amount
  ) for t in Ticket).order_by(1)[:LIMIT])

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

  if len(results) != LIMIT:
    raise AssertionError(f'Expected {LIMIT} results, got {len(results)}')

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns, pg_elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Pony. Test 7. Retrieval with limit including attributes of related record\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
