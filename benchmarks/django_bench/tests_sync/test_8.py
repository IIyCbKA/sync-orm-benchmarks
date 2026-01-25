from datetime import timedelta
from decimal import Decimal
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

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))

NOW = timezone.now()
DATE_FROM = NOW - timedelta(days=30)
AMOUNT_LOW = Decimal('50.00')
AMOUNT_HIGH = Decimal('500.00')


def select_iteration() -> int:
  start = time.perf_counter_ns()

  _ = list(Booking.objects.filter(
    total_amount__gte=AMOUNT_LOW,
    total_amount__lte=AMOUNT_HIGH,
    book_date__gte=DATE_FROM
  ).order_by('total_amount')[OFFSET:OFFSET + LIMIT])

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 8. Find with filter, offset pagination and sort\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
