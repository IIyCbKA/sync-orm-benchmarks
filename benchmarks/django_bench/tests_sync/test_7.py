import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.perf_counter_ns()

  try:
    book = Booking.objects.first()
    if book:
      _ = list(book.tickets.all())

  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 7. Nested find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()
