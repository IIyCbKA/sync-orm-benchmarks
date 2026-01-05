import time

from sqlalchemy import select
from tests_sync.db import SessionLocal
from core.models import Booking


def main() -> None:
    start = time.perf_counter_ns()
    session = SessionLocal()
    try:
        _ = session.scalars(select(Booking)).all()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 5. Find all\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
