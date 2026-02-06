from pony.orm import db_session, select
from core.models import Ticket, db
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


@db_session
def select_iteration() -> int:
  """
  order_by(1) equal order_by(ticket_no) in primitive notation
  """
  db.get_connection()
  start = time.perf_counter_ns()

  _ = list(select((
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
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 7. Find with limit and include parent\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()