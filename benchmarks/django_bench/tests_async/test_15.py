import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


async def delete_booking(i: int) -> None:
  try:
    await Booking.objects.filter(book_ref=generate_book_ref(i)).adelete()
  except Exception as e:
    print(f'[ERROR] Test 15 failed: {e}')
    sys.exit(1)


async def main() -> None:
  start = time.perf_counter_ns()

  tasks = [delete_booking(i) for i in range(COUNT)]
  await asyncio.gather(*tasks)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())