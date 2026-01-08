import asyncio
import sys
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
            bookings = result.all()
    except Exception as e:
        print(f'[ERROR] Test 5 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 5. Find all\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())