import sys
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from tests_sync.db import SessionLocal
from core.models import Booking


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()
    session: Session = SessionLocal()
    try:
        _ = session.get(Booking, generate_book_ref(1))
    except Exception as e:
        print(f'[ERROR] Test 8 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 8. Find unique\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
