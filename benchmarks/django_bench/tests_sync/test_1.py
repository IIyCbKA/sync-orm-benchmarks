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


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def create_iteration(i: int) -> int:
  start = time.perf_counter_ns()

  Booking.objects.create(
    book_ref=generate_book_ref(i),
    book_date=get_curr_date(),
    total_amount=generate_amount(i),
  )

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(COUNT):
      results.append(create_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 1 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 1. Single create\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
