Python sync ORMs performance bench [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/IIyCbKA/sql-orm-benchmarks/blob/main/LICENSE) [![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3120/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)](https://www.postgresql.org/)
==============

A reproducible benchmarking project to compare popular sync Python ORMs on PostgreSQL.

The primary database schema used in this project is based on the demonstration 
schema provided by Postgres Professional: https://postgrespro.ru/education/demodb. 
For reproducibility, each benchmark run is initialized from a trimmed 
three-month dump derived from `demo-20250901-3m.sql.gz` (original dump 
available at https://edu.postgrespro.ru/demo-20250901-3m.sql.gz).

To reduce dataset size and focus tests on the relevant domain, the trimmed dump 
included with this project contains only two tables: **Bookings** and 
**Tickets**. The trimmed dump is restored immediately prior to testing so that 
every run starts from the same reduced dataset. After restoration, 
VACUUM (ANALYZE) is run for the Bookings and Tickets tables to refresh 
planner statistics and the visibility map, ensuring that every benchmark 
starts from a consistent database state.

For convenience the trimmed dump has been incorporated into the database image 
and published on Docker Hub at:
https://hub.docker.com/r/denistred/sql-orm-bench-db.

---
### Server specifications:

**Minimum:**
- 4 × 3.3 GHz CPUs
- 8 GB RAM

**Recommended:**
- 4 × 3.5 GHz CPUs
- 16 GB RAM

---

### Running

For convenience, a ready-to-use `runner.sh` script is included in the repository root. 
It accepts the number of benchmark cycles and, optionally, the ORMs to run.
One cycle runs every ORM one after another, so all of them are measured within
a short time span and under comparable I/O conditions; results are compared
cycle by cycle rather than between runs made hours apart. Each ORM inside a
cycle starts from a fresh runtime copy of the golden database, and its
containers, networks and runtime volumes are removed before the next ORM
starts.

Each benchmark prints its result to stdout. The runner container logs remain
visible in the terminal and are also saved to `logs.txt`. This file is created
next to `runner.sh` and cleared before the first cycle. Every cycle is marked
there with an `iteration <k>` line, followed by the output of each ORM in the
order they ran.

Every supported test collects both client-observed and PostgreSQL-attributed
timings:

- `elapsed_ns` is the existing wall-clock measurement around the ORM operation.
- `pg_query_ns` is PostgreSQL planning plus execution time from
  `pg_stat_statements`.
- `pg_wal_ns` is WAL write and fsync time for the measured PostgreSQL backend.
- `pg_elapsed_ns` is `pg_query_ns + pg_wal_ns`.
- `pg_calls` is the number of statements, including explicit transaction
  commands tracked by PostgreSQL.

By default, each test prints only `elapsed_ns` and `pg_elapsed_ns`; the
underlying `pg_query_ns`, `pg_wal_ns`, and `pg_calls` values are collected
but not printed.

The PostgreSQL window includes the closing `COMMIT` or `ROLLBACK`, including
transactions created implicitly by an ORM. Probe queries run outside the
wall-clock window and are excluded from the PostgreSQL totals. Run only one
benchmark client against the database at a time because `pg_stat_statements`
stores cumulative database-wide statement statistics.

`pg_elapsed_ns` is server-attributed time, not a complete server wall clock.
PostgreSQL does not attribute protocol parsing and every part of transaction
bookkeeping to `pg_stat_statements`. For large writes, WAL writes performed
inside statement execution can also overlap with `pg_query_ns`; the separate
`pg_query_ns` and `pg_wal_ns` values make that visible.
Statement and planning statistics add instrumentation overhead, so compare
results only between runs made with the same PostgreSQL settings.

Usage example:
```bash
# from repo root
# run every ORM, ten cycles
./runner.sh 10
```

```bash
# from repo root
# restrict a cycle to the listed ORMs
./runner.sh 10 django sqlalchemy
```

List of existing ORMs (this is also the default order inside a cycle):
- django
- peewee
- pony
- sqlalchemy
- sqlmodel

**IMPORTANT NOTE:** After every ORM, `runner.sh` stops and removes the
containers, networks and runtime volumes before starting the next one.

**IMPORTANT NOTE:** For the correct functioning of the `runner.sh` script, you
need to have a ready-to-use `.env` in the project root with correct values.

**IMPORTANT NOTE:** The `runner.sh` script contains some complex logic: it checks
that a volume with the original database (golden) exists, and if necessary
deploys the dump into it. Then it cleans up the runtime volume from previous
runs if needed and creates a new runtime copy of the original database for the
current run. It also passes a subset of necessary arguments to docker-compose.
Therefore, it is recommended to run *exclusively* the ready `runner.sh`.

---

### Tests:

1. Single object creation
2. Creation of objects in a transaction
3. Bulk creation of objects
4. Retrieval of a large record set
5. Retrieval of the first record
6. Retrieval by primary key
7. Retrieval with limit including attributes of related record
8. Filtered retrieval with offset pagination and sorting
9. Single object update
10. Update of objects in a transaction
11. Bulk update of objects
12. Single object deletion
13. Deletion of objects in a transaction
14. Bulk deletion of objects

---

- Stack: Python 3.12, PostgreSQL 18, Psycopg 2.9.11/3.3.2.
- ORMs included: Django, Peewee, Pony, SQLAlchemy, SQLModel.
- Authors: student research team.
- License: MIT.