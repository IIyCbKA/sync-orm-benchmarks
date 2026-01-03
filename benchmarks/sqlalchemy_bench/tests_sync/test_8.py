import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with SessionLocal() as session:
            _ = session.scalars(
                select(Booking).where(Booking.book_ref == generate_book_ref(1)).order_by(Booking.book_ref).limit(1)
            ).first()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 8. Find unique\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
