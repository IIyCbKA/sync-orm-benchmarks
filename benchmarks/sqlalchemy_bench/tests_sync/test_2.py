from datetime import datetime, UTC
from decimal import Decimal
from tests_sync.db import SessionLocal
from models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


def main() -> None:
    start = time.time()

    with SessionLocal() as session:
        for i in range(COUNT):
            try:
                item = Booking(
                    book_ref=generate_book_ref(i),
                    book_date=datetime.now(UTC),
                    total_amount=generate_amount(i),
                )
                session.add(item)
                session.commit()
            except Exception:
                pass

    end = time.time()
    elapsed = end - start

    print(
        f'SQLAlchemy. Test 2. Transaction insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
