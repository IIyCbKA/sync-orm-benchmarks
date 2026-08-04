from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking
from core.pg_manager import pg_timer
from django.utils import timezone

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def update_iteration(i: int) -> tuple[int, int]:
  pg_timer.reset()
  booking = Booking.objects.get(pk=generate_book_ref(i))

  start = time.perf_counter_ns()

  booking.total_amount /= Decimal('10.00')
  booking.book_date = get_curr_date()
  booking.save(update_fields=['total_amount', 'book_date'])

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

  return end - start, pg_sample


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for i in range(COUNT):
      elapsed_ns, pg_elapsed_ns = update_iteration(i)
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Django. Test 9. Single object update\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
