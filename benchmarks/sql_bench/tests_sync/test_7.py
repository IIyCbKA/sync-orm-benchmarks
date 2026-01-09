import time
import sys
from tests_sync.db import get_connection


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                _ = cur.execute("""
                    SELECT 
                        tickets.ticket_no, 
                        tickets.book_ref, 
                        tickets.passenger_id, 
                        tickets.passenger_name, 
                        tickets.outbound, 
                        bookings.book_ref, 
                        bookings.book_date, 
                        bookings.total_amount 
                    FROM tickets 
                    INNER JOIN bookings ON (tickets.book_ref = bookings.book_ref) 
                    ORDER BY tickets.ticket_no LIMIT 1
                """).fetchone()
    except Exception as e:
        print(f'[ERROR] Test 7 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 7. Nested find first\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
