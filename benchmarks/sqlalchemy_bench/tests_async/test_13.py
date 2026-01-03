import asyncio
import time
from decimal import Decimal
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking, Ticket
import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'



async def update_nested_async():
    refs = [generate_book_ref(i) for i in range(COUNT)]
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Booking).where(Booking.book_ref.in_(refs))
            result = await session.execute(stmt)
            bookings = result.scalars().all()

            for booking in bookings:
                booking.total_amount += Decimal("10.00")
                await session.flush()

                ticket_stmt = select(Ticket).where(Ticket.book_ref == booking.book_ref)
                ticket_result = await session.execute(ticket_stmt)
                tickets = ticket_result.scalars().all()

                for ticket in tickets:
                    ticket.passenger_name = "Nested update"

                await session.flush()

async def main() -> None:
    start = time.perf_counter_ns()

    try:
        await update_nested_async()
    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 13. Nested batch update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )

if __name__ == "__main__":
    asyncio.run(main())
