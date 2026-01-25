import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Ticket

from django.db import connection
connection.ensure_connection()

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  _ = list(
    Ticket.objects
      .values_list(
        'ticket_no',
        'book_ref',
        'passenger_id',
        'passenger_name',
        'outbound',
        'book_ref__book_ref',
        'book_ref__book_date',
        'book_ref__total_amount',
    ).order_by('ticket_no')[:LIMIT]
  )

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
    f'Django ORM (sync). Test 7. Find with limit and include parent\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
