from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def create(session, obj):
    session.add(obj)
    session.flush()
    return obj

def main() -> None:
    start = time.perf_counter_ns()
    session = SessionLocal()
    try:
        for i in range(COUNT):
            booking = Booking(
                book_ref=generate_book_ref(i),
                book_date=get_curr_date(),
                total_amount=generate_amount(i),
            )
            session.add(booking)
            session.commit()

    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 1. Single create. {COUNT} entities\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
