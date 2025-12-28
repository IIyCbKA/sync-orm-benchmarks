import time
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with SessionLocal() as session:
            _ = session.scalars(
                select(Ticket).options(joinedload(Ticket.booking)).limit(1)
            ).first()
    except Exception:
        pass

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy. Test 7. Nested find first\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
