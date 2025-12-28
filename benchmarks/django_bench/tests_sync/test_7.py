import time

import django
django.setup()

from core.models import Ticket

def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = Ticket.objects.select_related('book_ref').first()

  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 7. Nested find first\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()
