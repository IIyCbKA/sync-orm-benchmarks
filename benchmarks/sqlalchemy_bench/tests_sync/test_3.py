from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from sqlalchemy import insert
from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)

def main() -> None:
    start = time.perf_counter_ns()

    objs = [
        Booking(
            book_ref=generate_book_ref(i),
            book_date=get_curr_date(),
            total_amount=generate_amount(i),
        )
        for i in range(COUNT)
    ]

    session = SessionLocal()
    try:
        with session.begin():
            session.bulk_save_objects(objs)
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 3. Bulk create. {COUNT} entities\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
