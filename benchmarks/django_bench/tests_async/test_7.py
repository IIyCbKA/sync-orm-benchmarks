import asyncio
import time

import django
django.setup()

from core.models import Booking

async def main() -> None:
  start = time.perf_counter_ns()

  try:
    book = await Booking.objects.afirst()
    if book:
      _ = [t async for t in book.tickets.all()]
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 7. Nested find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  asyncio.run(main())
