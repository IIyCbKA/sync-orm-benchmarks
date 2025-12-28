import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = Booking.objects.first()
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 6. Find first\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()
