import time
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with SessionLocal() as session:
            stmt = (
                select(
                    Ticket.ticket_no,
                    Ticket.book_ref,
                    Ticket.passenger_id,
                    Ticket.passenger_name,
                    Ticket.outbound,
                    Booking.book_ref,
                    Booking.book_date,
                    Booking.total_amount,
                )
                .join(Booking, Ticket.book_ref == Booking.book_ref)
                .order_by(Ticket.ticket_no)
                .limit(1)
            )
            ticket = session.execute(stmt).first()

            if ticket:
                book_ref_value = ticket.book_ref

    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 7. Nested find first\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
