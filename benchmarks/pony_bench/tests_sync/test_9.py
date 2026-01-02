from pony.orm import db_session, select
from core.models import Ticket
import sys
import time

def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      _ = list(
        select((
        t.ticket_no,
        t.book_ref,
        t.passenger_id,
        t.passenger_name,
        t.outbound,
        b.book_ref,
        b.book_date,
        b.total_amount
        ) for t in Ticket for b in t.book_ref if b.book_ref == generate_book_ref(1))
      )
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 9. Nested find unique\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()