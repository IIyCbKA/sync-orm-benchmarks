from decimal import Decimal
from functools import lru_cache
import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
  value = i + 100
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


async def update_booking(i: int) -> None:
  try:
    await Booking.objects.filter(book_ref=generate_book_ref(i)).aupdate(
      total_amount=get_new_amount(i),
      book_date=get_curr_date()
    )
  except Exception as e:
    print(f'[ERROR] Test 12 failed: {e}')
    sys.exit(1)


async def main() -> None:
  start = time.perf_counter_ns()

  tasks = [update_booking(i) for i in range(COUNT)]
  await asyncio.gather(*tasks)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 12. Single update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())