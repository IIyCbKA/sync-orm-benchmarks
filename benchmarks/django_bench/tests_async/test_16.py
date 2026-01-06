import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


async def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 16 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    await Booking.objects.filter(book_ref__in=refs).adelete()
  except Exception as e:
    print(f'[ERROR] Test 16 failed (delete phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 16. Bulk delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
