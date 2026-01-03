import os
import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    session = SessionLocal()
    try:
        for i in range(COUNT):
            booking = session.scalars(
                select(Booking)
                .where(Booking.book_ref == generate_book_ref(i))
                .limit(1)
            ).first()

            if booking:
                session.delete(booking)
                session.flush()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 15. Single delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
