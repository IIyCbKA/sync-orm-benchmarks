import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking
from core.pg_manager import pg_timer

from django.db import connection
connection.ensure_connection()

LARGE_LIMIT = int(os.environ.get('LARGE_LIMIT', '10000'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> tuple[int, int]:
  pg_timer.reset()
  start = time.perf_counter_ns()

  _ = list(Booking.objects.all()[:LARGE_LIMIT])

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
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Django. Test 4. Retrieval of a large record set\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
