from decimal import Decimal
import os
import sys
import time

import django
django.setup()

from core.models import Booking, Ticket
from django.db import transaction
from django.db.models import F

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with transaction.atomic():
      for i in range(COUNT):
        book_ref = generate_book_ref(i)
        Booking.objects.filter(book_ref=book_ref).update(
          total_amount=F('total_amount') + Decimal('10.00')
        )

        Ticket.objects.filter(book_ref=book_ref).update(
          passenger_name='Nested update'
        )
  except Exception as e:
    print(f'[ERROR] Test 13 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()