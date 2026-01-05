import sys
import time

import django
django.setup()

from core.models import Ticket

def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = list(Ticket.objects.select_related('book_ref').filter(
      book_ref=generate_book_ref(1))
    )
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 9. Nested find\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
