import asyncio
import os
import sys
import time

import django
django.setup()

from asgiref.sync import sync_to_async
from core.models import Booking
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


@sync_to_async
def delete_nested_sync(bookings: list[Booking]) -> None:
  for booking in bookings:
    with transaction.atomic():
      booking.tickets.all().delete()
      booking.delete()


async def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(
      Booking.objects
      .filter(book_ref__in=refs)
      .prefetch_related('tickets')
    )
  except Exception as e:
    print(f'[ERROR] Test 17 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    await delete_nested_sync(bookings)
  except Exception as e:
    print(f'[ERROR] Test 17 failed (delete phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 17. Nested delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())