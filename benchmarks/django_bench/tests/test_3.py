from decimal import Decimal
from functools import lru_cache
import os
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
  return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def main() -> None:
  try:
    start = time.perf_counter_ns()

    objs = [
      Booking(
        book_ref=generate_book_ref(i),
        book_date=get_curr_date(),
        total_amount=generate_amount(i),
      ) for i in range(COUNT)
    ]

    Booking.objects.bulk_create(objs)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 3 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (sync). Test 3. Bulk create. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
