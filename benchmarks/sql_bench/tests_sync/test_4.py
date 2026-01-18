from tests_sync.db import conn
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  with conn.cursor() as cur:
    _ = cur.execute("""
      SELECT 
        bookings.book_ref,
        bookings.book_date,
        bookings.total_amount
      FROM bookings
    """).fetchall()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Pure SQL (psycopg3). Test 4. Find all\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
    main()
