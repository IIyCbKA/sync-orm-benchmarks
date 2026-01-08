import sys
import time

import django
django.setup()

from core.models import Booking

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = Booking.objects.get(pk=generate_book_ref(1))
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 8. Find unique\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
