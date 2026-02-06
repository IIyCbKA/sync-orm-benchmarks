import os
import sys
import time

import django
django.setup()

from core.models import Booking
from django.db import transaction

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(Booking.objects.filter(book_ref__in=refs))
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  try:
    start = time.perf_counter_ns()

    with transaction.atomic():
      for booking in bookings:
        booking.delete()

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 13 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (sync). Test 13. Transaction delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()