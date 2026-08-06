from sqlalchemy import select
from core.database import SessionLocal
from core.models import Booking, Ticket
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> tuple[int, int]:
  with SessionLocal() as session:
    pg_timer.reset(session)
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
    pg_sample = pg_timer.collect()

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns, pg_elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'SQLAlchemy. Test 7. Retrieval with limit including attributes of related record\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
