from decimal import Decimal
from functools import lru_cache
import os
import sys
import time

import django
django.setup()

from core.models import Booking
from django.db.models import F
from django.utils import timezone

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 11 failed (data preparation): {e}')
    sys.exit(1)

  try:
    start = time.perf_counter_ns()

    Booking.objects.filter(book_ref__in=refs).update(
      total_amount=F('total_amount') + Decimal('10.00'),
      book_date=get_curr_date(),
    )

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 11 failed (update phase): {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (sync). Test 11. Bulk update. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
