import os
import sys
import time
from sqlalchemy import delete

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    bookings_to_delete = [generate_book_ref(i) for i in range(COUNT)]
    session = SessionLocal()
    try:
        statement = delete(Booking).where(Booking.book_ref.in_(bookings_to_delete))
        result = session.execute(statement)
        session.commit()
    except Exception as e:
        print(f'[ERROR] Test 16 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 16. Bulk delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
