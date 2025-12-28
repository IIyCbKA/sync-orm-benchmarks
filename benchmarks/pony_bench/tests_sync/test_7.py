from pony.orm import db_session, left_join
from core.models import Ticket
import time

def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      _ = left_join((t, b) for t in Ticket for b in t.book_ref).first()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 7. Nested find first\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()