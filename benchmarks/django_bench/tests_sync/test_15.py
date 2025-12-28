import os
import time

import django
django.setup()

from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  for i in range(COUNT):
    try:
      booking = Booking.objects.filter(book_ref=generate_book_ref(i)).first()
      if booking:
        booking.delete()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()