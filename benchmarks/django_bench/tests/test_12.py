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

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def delete_iteration(i: int) -> tuple[int, int]:
  booking = Booking.objects.get(pk=generate_book_ref(i))

  pg_timer.reset()
  start = time.perf_counter_ns()

  booking.delete()

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for i in range(COUNT):
      elapsed_ns, pg_elapsed_ns = delete_iteration(i)
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 12 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Django. Test 12. Single object deletion\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
