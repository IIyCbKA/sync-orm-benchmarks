from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from core.database import SessionLocal
from core.models import Booking
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def create_iteration(i: int) -> int:
  with SessionLocal() as session:
    start = time.perf_counter_ns()

    booking = Booking(
      book_ref=generate_book_ref(i),
      book_date=get_curr_date(),
      total_amount=generate_amount(i),
    )
    session.add(booking)
    session.commit()

    end = time.perf_counter_ns()

  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(COUNT):
      results.append(create_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 1 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'SQLModel (sync). Test 1. Single create\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
