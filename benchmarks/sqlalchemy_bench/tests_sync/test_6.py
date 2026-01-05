import time
from sqlalchemy import select, asc
from tests_sync.db import SessionLocal
from core.models import Booking


def main() -> None:
    start = time.perf_counter_ns()

    session = SessionLocal()
    try:
        _ = session.scalars(
                select(Booking).order_by(asc(Booking.book_ref)).limit(1)
            ).first()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 6. Find first\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
