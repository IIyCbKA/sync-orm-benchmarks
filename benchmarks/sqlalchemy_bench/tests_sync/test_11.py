import sys
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: Decimal) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    session: Session = SessionLocal()
    refs = [generate_book_ref(i) for i in range(COUNT)]
    statement = select(Booking).where(Booking.book_ref.in_(refs))
    bookings = session.execute(statement).scalars().all()
    session.commit()
    start = time.perf_counter_ns()
    try:
        with session.begin():
            for booking in bookings:
                if booking:
                    booking.total_amount = get_new_amount(booking.total_amount)
                    booking.book_date = get_curr_date()
                    session.flush()
    except Exception as e:
        print(f'[ERROR] Test 11 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 11. Transaction update. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
