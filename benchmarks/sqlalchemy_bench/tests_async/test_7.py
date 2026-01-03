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
            stmt = select(Ticket).limit(1)
            ticket = await session.scalar(stmt)

            if ticket:
                book_ref_value = ticket.book_ref

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
