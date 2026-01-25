import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def delete_iteration(i: int) -> int:
  booking = Booking.objects.get(pk=generate_book_ref(i))

  start = time.perf_counter_ns()

  booking.delete()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(COUNT):
      results.append(delete_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 12 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 12. Single delete\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()