from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from core.database import SessionLocal
from core.models import Booking
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  try:
    with SessionLocal() as session:
      start = time.perf_counter_ns()

      with session.begin():
        for i in range(COUNT):
          session.add(Booking(
            book_ref=generate_book_ref(i),
            book_date=get_curr_date(),
            total_amount=generate_amount(i),
          ))

      end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 2 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'SQLAlchemy (sync). Test 2. Transaction create. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
