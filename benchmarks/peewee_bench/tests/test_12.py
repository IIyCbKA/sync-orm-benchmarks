from core.models import Booking
from core.database import db
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def delete_iteration(i: int) -> int:
  with db.connection_context():
    booking = Booking.get_by_id(generate_book_ref(i))

    start = time.perf_counter_ns()

    booking.delete_instance()

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
    f'Peewee ORM (sync). Test 12. Single delete. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
