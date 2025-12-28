import asyncio
import time

import django
django.setup()

from core.models import Booking

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = await Booking.objects.filter(book_ref=generate_book_ref(1)).afirst()
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 8. Find unique\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  asyncio.run(main())
