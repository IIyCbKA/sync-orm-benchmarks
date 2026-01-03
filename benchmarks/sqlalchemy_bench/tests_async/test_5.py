import asyncio
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking

async def main() -> None:
    start = time.perf_counter_ns()

    try:
        async with AsyncSessionLocal() as session:
            stmt = select(Booking)
            result = await session.scalars(stmt)
            bookings = [b for b in result]
    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 5. Find all\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())