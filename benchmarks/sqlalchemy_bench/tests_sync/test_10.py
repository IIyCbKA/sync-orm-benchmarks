from datetime import datetime, timedelta, UTC
from decimal import Decimal
import os
import time
from sqlalchemy import select, asc
from sqlalchemy.sql.functions import session_user

from tests_sync.db import SessionLocal
from core.models import Booking

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.perf_counter_ns()
    session = SessionLocal()
    try:
        stmt = (
            select(Booking)
            .where(
                Booking.total_amount.between(amount_low, amount_high),
                Booking.book_date >= date_from
            )
            .order_by(asc(Booking.total_amount))
            .limit(LIMIT)
            .offset(OFFSET)
        )

        results = session.scalars(stmt).all()
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy (sync). Test 10. Filter, paginate & sort\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
