from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time
from tests_sync.db import conn

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
  start = time.perf_counter_ns()

  with conn.cursor() as cur:
    cur.execute("""
      INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
      VALUES (%s, %s, %s)
    """, (generate_book_ref(i), get_curr_date(), generate_amount(i)))

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
    f'Pure SQL (psycopg3). Test 1. Single create\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
