import os
import sys
import time
from sqlalchemy import select, delete

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def delete_booking():
    refs = [generate_book_ref(i) for i in range(COUNT)]
    with SessionLocal() as session:
        with session.begin():
            for ref in refs:
                stmt = delete(Booking).where(Booking.book_ref == ref)
                session.execute(stmt)


def main() -> None:
    start = time.perf_counter_ns()

    try:
        delete_booking()
    except Exception as e:
        print(f'[ERROR] Test 14 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (sync). Test 14. Transaction delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    main()

