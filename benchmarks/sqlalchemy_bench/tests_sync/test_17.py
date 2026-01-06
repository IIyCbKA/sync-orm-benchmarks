import os
import sys
import time
from sqlalchemy import delete, select

from tests_sync.db import SessionLocal
from core.models import Booking, Ticket

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def main() -> None:
    bookings_to_delete = [generate_book_ref(i) for i in range(COUNT)]
    session = SessionLocal()
    bookings = session.execute(
        select(Booking).where(Booking.book_ref.in_(bookings_to_delete))
    ).scalars().all()
    session.commit()
    start = time.perf_counter_ns()
    try:
        for booking in bookings:
            with session.begin():
                session.execute(
                    delete(Ticket).where(Ticket.book_ref == booking.book_ref)
                )
                session.delete(booking)
    except Exception as e:
        print(f'[ERROR] Test 17 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 17. Nested delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
