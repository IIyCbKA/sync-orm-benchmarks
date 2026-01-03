from decimal import Decimal
from datetime import datetime, UTC
import os
from sqlalchemy import select

from core.models import Booking, Ticket
from db import SessionLocal

COUNT = int(os.environ.get("WARMUP_ITERATIONS", '20'))

def warmup() -> None:
    for i in range(COUNT):
        try:
            session = SessionLocal()
            with session.begin():
                b = Booking(
                    book_ref=f'warm{i:02d}',
                    book_date=datetime.now(UTC),
                    total_amount=Decimal('5.00')
                )
                session.add(b)
                session.flush()
                t = Ticket(
                    ticket_no=f'warm{i:09d}',
                    book_ref=b.book_ref,
                    passenger_id=f'warm{i:05d}',
                    passenger_name='Warm',
                    outbound=True
                )
                session.add(t)
                session.flush()

                _ = session.scalar(
                    select(Booking).where(Booking.book_ref == f'warm{i:02d}')
                )
                __ = session.scalar(
                    select(Ticket).where(Ticket.ticket_no == f'warm{i:09d}')
                )

                b.total_amount = Decimal('2.00')
                t.passenger_name = 'WarmUpdate'

                session.delete(t)
                session.flush()
                session.delete(b)

        except Exception as e:
            print(e)

    print("Warmup done")

if __name__ == "__main__":
    warmup()