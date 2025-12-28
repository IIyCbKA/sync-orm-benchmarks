import asyncio
import os
import time

import django
django.setup()

from asgiref.sync import sync_to_async
from core.models import Booking
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@sync_to_async
def delete_booking_sync():
  try:
    with transaction.atomic():
      for i in range(COUNT):
        booking = Booking.objects.filter(book_ref=generate_book_ref(i)).first()
        if booking:
          booking.delete()
  except Exception:
    pass


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    await delete_booking_sync()
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 14. Batch delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  asyncio.run(main())