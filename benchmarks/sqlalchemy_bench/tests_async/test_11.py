import asyncio
import sys
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os
from sqlalchemy import update, select

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)



async def main() -> None:
    session = AsyncSessionLocal()
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        statement = select(Booking).where(Booking.book_ref.in_(refs))
        result = await session.execute(statement)
        bookings = result.scalars().all()
        await session.commit()
    except Exception as e:
        print(f'[ERROR] Test 11 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        async with session.begin():
            for booking in bookings:
                if booking:
                    booking.total_amount = get_new_amount(booking.total_amount)
                    booking.book_date = get_curr_date()
                    await session.flush()
    except Exception as e:
        print(f'[ERROR] Test 11 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 11. Transaction update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
