from decimal import Decimal
from pony.orm import db_session
from core.models import Booking, db
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))

AMOUNT_LOW = Decimal('50.00')
AMOUNT_HIGH = Decimal('500.00')


@db_session
def select_iteration() -> tuple[int, int]:
  db.get_connection()

  pg_timer.reset()
  start = time.perf_counter_ns()

  _ = list(Booking.select(lambda b:
    b.total_amount >= AMOUNT_LOW and b.total_amount <= AMOUNT_HIGH
  ).order_by(lambda b: b.total_amount)[OFFSET: OFFSET + LIMIT])

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

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
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Pony. Test 8. Filtered retrieval with offset pagination and sorting\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
