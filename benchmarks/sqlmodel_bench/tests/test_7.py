from sqlalchemy import select
from tests.database import SessionLocal
from core.models import Booking, Ticket
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  with SessionLocal() as session:
    start = time.perf_counter_ns()

    stmt = (
      select(
        Ticket.ticket_no,
        Ticket.book_ref,
        Ticket.passenger_id,
        Ticket.passenger_name,
        Ticket.outbound,
        Booking.book_ref,
        Booking.book_date,
        Booking.total_amount,
      )
      .join(Booking, Ticket.book_ref == Booking.book_ref)
      .order_by(Ticket.ticket_no)
      .limit(LIMIT)
    )
    _ = session.execute(stmt).all()

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
    f'SQLModel (sync). Test 7. Find with limit and include parent\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
