import asyncio
import sys
import time
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from tests_async.db import AsyncSessionLocal
from core.models import Booking, Ticket
import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'



async def main() -> None:
    session = AsyncSessionLocal()
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        statement = (select(Booking)
                     .options(selectinload(Booking.tickets))
                     .where(Booking.book_ref.in_(refs)))
        result = await session.execute(statement)
        bookings = result.scalars().all()
    except Exception as e:
        print(f'[ERROR] Test 13 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        for booking in bookings:
            booking.total_amount += Decimal("10.00")
            await session.flush()
            for ticket in booking.tickets:
                ticket.passenger_name = "Nested update"
                await session.flush()
            await session.commit()
    except Exception as e:
        print(f'[ERROR] Test 13 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 13. Nested update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )

if __name__ == "__main__":
    asyncio.run(main())
