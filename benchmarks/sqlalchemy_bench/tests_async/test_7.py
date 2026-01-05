import asyncio
import time
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from tests_async.db import AsyncSessionLocal
from core.models import Booking, Ticket


async def main() -> None:
    start = time.perf_counter_ns()

    try:
        async with AsyncSessionLocal() as session:
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
            result = await session.execute(stmt)
            ticket = result.first()

    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 7. Nested find first\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
