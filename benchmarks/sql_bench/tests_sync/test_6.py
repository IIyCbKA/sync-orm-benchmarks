from tests_sync.db import conn
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def select_iteration() -> int:
  start = time.perf_counter_ns()

  with conn.cursor() as cur:
    _ = cur.execute("""
      SELECT 
        bookings.book_ref,
        bookings.book_date,
        bookings.total_amount
      FROM bookings.bookings
      WHERE book_ref = %s
      LIMIT 1
    """, (generate_book_ref(1),)).fetchone()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Pure SQL (psycopg3). Test 6. Find unique record\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
