from decimal import Decimal
import os
import time
from sqlalchemy import select
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def update_nested():
    refs = [generate_book_ref(i) for i in range(COUNT)]
    with SessionLocal() as session:
        with session.begin():
            stmt = select(Booking).where(Booking.book_ref.in_(refs))
            result = session.execute(stmt)
            bookings = result.scalars().all()

            for booking in bookings:
                booking.total_amount += Decimal("10.00")
                session.flush()

                ticket_stmt = select(Ticket).where(Ticket.book_ref == booking.book_ref)
                ticket_result = session.execute(ticket_stmt)
                tickets = ticket_result.scalars().all()

                for ticket in tickets:
                    ticket.passenger_name = "Nested update"

                session.flush()

def main() -> None:
    start = time.perf_counter_ns()

    try:
        update_nested()
    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (sync). Test 13. Nested batch update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == '__main__':
    main()
