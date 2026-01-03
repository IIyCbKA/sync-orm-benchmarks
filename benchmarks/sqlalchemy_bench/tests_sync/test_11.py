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


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.perf_counter_ns()

    try:
        session: Session = SessionLocal()
        with session.begin():
            for i in range(COUNT):
                statement = select(Booking).where(Booking.book_ref == generate_book_ref(i)).order_by(Booking.book_ref).limit(1)
                booking = session.execute(statement).scalars().first()
                if booking:
                    booking.total_amount = get_new_amount(i)
                    booking.book_date = get_curr_date()
                    session.flush()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 11. Batch update. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
