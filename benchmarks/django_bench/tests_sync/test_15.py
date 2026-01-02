import os
import sys
import time

import django
django.setup()

from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    for i in range(COUNT):
      Booking.objects.filter(book_ref=generate_book_ref(i)).delete()
  except Exception as e:
    print(f'[ERROR] Test 15 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()