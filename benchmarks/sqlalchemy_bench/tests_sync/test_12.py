from sqlalchemy import select
from tests_sync.db import SessionLocal
from core.models import Booking
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  with SessionLocal() as session:
    try:
      refs = [generate_book_ref(i) for i in range(COUNT)]
      stmt = select(Booking).where(Booking.book_ref.in_(refs))
      bookings = session.execute(stmt).scalars().all()
      session.commit()
    except Exception as e:
      print(f'[ERROR] Test 12 failed (data preparation): {e}')
      sys.exit(1)

    results: list[int] = []

    try:
      for booking in bookings:
        start = time.perf_counter_ns()

        session.delete(booking)
        session.commit()

        end = time.perf_counter_ns()
        results.append(end - start)
    except Exception as e:
      print(f'[ERROR] Test 12 failed (delete phase): {e}')
      sys.exit(1)

    elapsed = statistics.median(results)

    print(
      f'SQLAlchemy (sync). Test 12. Single delete\n'
      f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
  main()
