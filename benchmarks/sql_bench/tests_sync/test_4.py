from datetime import datetime, UTC
from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
    return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.perf_counter_ns()
    curr_date = datetime.now(UTC)
    connection = get_connection()
    try:
        with connection as conn:
            with conn.cursor() as cur:
                for i in range(COUNT):
                    cur.execute(
                        """
                        INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                        VALUES (%s, %s, %s)
                        RETURNING book_ref
                        """,
                        (generate_book_ref(i), curr_date, generate_amount(i))
                    )
                    booking_id = cur.fetchone()[0]

                    cur.execute(
                        """
                        INSERT INTO bookings.tickets 
                        (ticket_no, book_ref, passenger_id, passenger_name, outbound)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            generate_ticket_no(i),
                            booking_id,
                            generate_passenger_id(i),
                            "Test",
                            True,
                        )
                    )
                    conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 4 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start
    print(
        f'Pure SQL (psycopg3). Test 4. Nested create. {COUNT} entities\n'
        f'elapsed_ns={elapsed};'
    )


if __name__ == "__main__":
    main()