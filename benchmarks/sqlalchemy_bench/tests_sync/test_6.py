import time
from sqlalchemy import select
from tests_sync.db import SessionLocal
from core.models import Booking


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with SessionLocal() as session:
            _ = session.scalars(
                select(Booking).limit(1)
            ).first()
    except Exception:
        pass

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy. Test 6. Find first\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
