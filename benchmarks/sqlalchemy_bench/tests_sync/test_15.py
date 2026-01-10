import os
import sys
import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def main() -> None:
    session = SessionLocal()
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        statement = select(Booking).where(Booking.book_ref.in_(refs))
        bookings = session.execute(statement).scalars().all()
    except Exception as e:
        print(f'[ERROR] Test 15 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        for booking in bookings:
            session.delete(booking)
            session.commit()
    except Exception as e:
        print(f'[ERROR] Test 15 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 15. Single delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
