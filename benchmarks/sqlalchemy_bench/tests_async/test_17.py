import asyncio
import os
import sys
import time
from sqlalchemy import delete, select
from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking, Ticket

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


async def main() -> None:
    bookings_to_delete = [generate_book_ref(i) for i in range(COUNT)]

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Booking.book_ref)
            .where(Booking.book_ref.in_(bookings_to_delete))
        )
        bookings = result.scalars().all()

        await session.commit()

        start = time.perf_counter_ns()

        try:
            for book_ref in bookings:
                async with session.begin():
                    await session.execute(
                        delete(Ticket).where(Ticket.book_ref == book_ref)
                    )
                    await session.execute(
                        delete(Booking).where(Booking.book_ref == book_ref)
                    )
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
