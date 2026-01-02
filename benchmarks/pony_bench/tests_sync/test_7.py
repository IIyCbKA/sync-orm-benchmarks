from pony.orm import db_session, select
from core.models import Ticket
import sys
import time

def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      # order by first row - t.ticket_no
      _ = select((
        t.ticket_no,
        t.book_ref,
        t.passenger_id,
        t.passenger_name,
        t.outbound,
        b.book_ref,
        b.book_date,
        b.total_amount
      ) for t in Ticket for b in t.book_ref).order_by(1).first()
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 7. Nested find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()