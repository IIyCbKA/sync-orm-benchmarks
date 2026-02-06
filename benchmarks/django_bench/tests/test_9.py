from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def update_iteration(i: int) -> int:
  booking = Booking.objects.get(pk=generate_book_ref(i))

  start = time.perf_counter_ns()

  booking.total_amount /= Decimal('10.00')
  booking.book_date = get_curr_date()
  booking.save(update_fields=['total_amount', 'book_date'])

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(COUNT):
      results.append(update_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 9. Single update\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
