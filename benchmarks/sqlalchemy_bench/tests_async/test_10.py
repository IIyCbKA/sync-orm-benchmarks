import asyncio
import time
from datetime import datetime, timedelta, UTC
from decimal import Decimal
from sqlalchemy import select, asc
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


async def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal("50.00")
    amount_high = Decimal("500.00")
    start = time.perf_counter_ns()

    try:
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Booking)
                .where(
                    Booking.total_amount >= amount_low,
                    Booking.total_amount <= amount_high,
                    Booking.book_date >= date_from,
                )
                .order_by(asc(Booking.total_amount))
                .offset(OFFSET)
                .limit(LIMIT)
            )
            result = await session.scalars(stmt)
            bookings = [b for b in result]

    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 10. Filter, paginate & sort\n"
        f"elapsed_ns={elapsed:.0f};"
    )

if __name__ == "__main__":
    asyncio.run(main())
