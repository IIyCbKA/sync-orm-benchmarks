import asyncio
import sys
import time

import django
django.setup()

from core.models import Booking

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = await Booking.objects.aget(pk=generate_book_ref(1))
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 8. Find unique\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
