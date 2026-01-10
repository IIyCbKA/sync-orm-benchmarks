import asyncio
import os
import sys
import time
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking, Ticket

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


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
        print(f'[ERROR] Test 17 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        for booking in bookings:
            for ticket in booking.tickets:
                await session.delete(ticket)
            await session.delete(booking)
            await session.commit()
    except Exception as e:
        print(f"[ERROR] Test 17 failed: {e}")
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f"SQLAlchemy (async). Test 17. Nested delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
