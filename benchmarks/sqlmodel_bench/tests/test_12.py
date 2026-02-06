from sqlalchemy import select
from tests.database import SessionLocal
from core.models import Booking
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def delete_iteration(i: int) -> int:
  with SessionLocal() as session:
    booking = session.scalar(
      select(Booking).where(Booking.book_ref == generate_book_ref(i))
    )

    start = time.perf_counter_ns()

    session.delete(booking)
    session.commit()

    end = time.perf_counter_ns()
    return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(COUNT):
      results.append(delete_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 12 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'SQLModel (sync). Test 12. Single delete\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
