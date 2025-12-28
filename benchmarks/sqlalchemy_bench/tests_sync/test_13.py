from decimal import Decimal
import os
import time
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    refs = [generate_book_ref(i) for i in range(COUNT)]
    session = SessionLocal()
    try:
        bookings = session.scalars(
            select(Booking)
            .options(joinedload(Booking.tickets))
            .where(Booking.book_ref.in_(refs))
        ).all()

        with session.begin():
            for booking in bookings:
                booking.total_amount += Decimal('10.00')
                session.flush()

                for ticket in booking.tickets:
                    ticket.passenger_name = 'Nested update'
                    session.flush()
    except Exception:
        pass

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy. Test 13. Nested batch update. {COUNT} entries\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
