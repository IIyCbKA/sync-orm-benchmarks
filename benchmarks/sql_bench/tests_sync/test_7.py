from tests_sync.db import conn
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  with conn.cursor() as cur:
    _ = cur.execute("""
      SELECT 
        tickets.ticket_no,
        tickets.book_ref,
        tickets.passenger_id,
        tickets.passenger_name,
        tickets.outbound,
        bookings.book_ref,
        bookings.book_date,
        bookings.total_amount
      FROM tickets
      INNER JOIN bookings ON (tickets.book_ref = bookings.book_ref)
      ORDER BY tickets.ticket_no 
      LIMIT %s
    """, (LIMIT, )).fetchall()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Pure SQL (psycopg3). Test 7. Find with limit and include parent\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
