from pony.orm import db_session, select
from core.models import Booking
import os
import sys

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


def main() -> None:
  """
  Pony ORM does not support true bulk delete.
  Therefore, Test 16 "Bulk delete" is skipped for Pony,
  and we mark it with a dash in benchmarks.

  To maintain dataset consistency with other ORMs and clean the table for subsequent tests,
  this script deletes the required Booking entities one by one.
  """

  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    with db_session:
      bookings = list(select(b for b in Booking if b.book_ref in refs))
  except Exception as e:
    print(f'[ERROR] Dataset preparation failed (instead of bulk delete): {e}')
    sys.exit(1)

  try:
    with db_session:
      for booking in bookings:
        booking.delete()
  except Exception as e:
    print(f'[ERROR] Dataset delete failed (instead of bulk delete): {e}')
    sys.exit(1)

  print(
    f'PonyORM. Test 16. Bulk delete. {COUNT} entries\n'
    f'Bulk delete is not supported — deleted individually for dataset cleanup'
  )


if __name__ == '__main__':
  main()
