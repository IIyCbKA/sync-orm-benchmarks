import os
import sys
from decimal import Decimal
from datetime import datetime, UTC
from tests_sync.db import get_connection

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))

def warm_up() -> None:
    try:
        with get_connection() as conn:
            for i in range(COUNT):
                with conn.transaction():
                    with conn.cursor() as cur:
                        book_ref = f"warm{i:02d}"
                        ticket_no = f"warm{i:09d}"

                        cur.execute(
                            """
                            INSERT INTO bookings.bookings
                            (book_ref, book_date, total_amount)
                            VALUES (%s, %s, %s)
                            """,
                            (book_ref, datetime.now(UTC), Decimal("5.00")),
                        )

                        cur.execute(
                            """
                            INSERT INTO bookings.tickets
                            (ticket_no, book_ref, passenger_id, passenger_name, outbound)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                ticket_no,
                                book_ref,
                                f"warm{i:05d}",
                                "Warm",
                                True,
                            ),
                        )

                        cur.execute(
                            """
                            SELECT book_ref, total_amount
                            FROM bookings.bookings
                            WHERE book_ref = %s
                            """,
                            (book_ref,),
                        )
                        _ = cur.fetchone()

                        cur.execute(
                            """
                            SELECT ticket_no, passenger_name
                            FROM bookings.tickets
                            WHERE ticket_no = %s
                            """,
                            (ticket_no,),
                        )
                        __ = cur.fetchone()

                        cur.execute(
                            """
                            UPDATE bookings.bookings
                            SET total_amount = %s
                            WHERE book_ref = %s
                            """,
                            (Decimal("2.00"), book_ref),
                        )

                        cur.execute(
                            """
                            UPDATE bookings.tickets
                            SET passenger_name = %s
                            WHERE ticket_no = %s
                            """,
                            ("WarmUpdate", ticket_no),
                        )

                        cur.execute(
                            "DELETE FROM bookings.tickets WHERE ticket_no = %s",
                            (ticket_no,),
                        )

                        cur.execute(
                            "DELETE FROM bookings.bookings WHERE book_ref = %s",
                            (book_ref,),
                        )

    except Exception as e:
        print(f"[ERROR] Warm-up failed: {e}")
        sys.exit(1)

    print("Warm-up done")
