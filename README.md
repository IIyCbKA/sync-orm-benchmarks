Python sync ORMs performance bench [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/IIyCbKA/sql-orm-benchmarks/blob/main/LICENSE) [![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3120/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)](https://www.postgresql.org/)
==============

A reproducible benchmarking project to compare popular sync Python ORMs on PostgreSQL.

The primary database schema used in this project is based on the demonstration 
schema provided by Postgres Professional: https://postgrespro.ru/education/demodb. 
For reproducibility, each benchmark run is initialized from a trimmed one-year 
dump derived from `demo-20250901-1y.sql.gz` (original dump available at 
https://edu.postgrespro.ru/demo-20250901-1y.sql.gz).

To reduce dataset size and focus tests on the relevant domain, the trimmed dump 
included with this project contains only two tables: **Bookings** and 
**Tickets**. The trimmed dump is restored immediately prior to testing so that 
every run starts from the same reduced dataset. After trimming, the dump is 
compacted and planner statistics are refreshed by running `VACUUM FULL ANALYZE` 
so that query plans are up-to-date and each benchmark starts from a clean, 
consistent state.

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

For convenience (it's recommended), ready-to-use `start.sh`, `stop.sh` and 
`logs.sh` scripts are included in the repository root. Simply run them from 
the repo root. Specify the ORM name (required) for `start.sh`.

Each benchmark prints its result to stdout. These stdout lines are captured 
by Docker and can be viewed via the runner container logs.

Usage example:
```bash
# from repo root
# create and run containers
./start.sh <ORM>

# follow live runner logs
./logs.sh

# stop and remove containers, networks and runtime volumes
./stop.sh
```

List of existing ORMs available for start/stop/logs (use the ORM 
name from this list for `./start.sh`):
- django
- peewee
- pony
- sqlalchemy
- sqlmodel

**IMPORTANT NOTE:** On each fresh run of `docker-compose` (this is done 
in `stop.sh`) you must clear all runtime volumes from previous runs.

**IMPORTANT NOTE:** For the correct functioning of the `start.sh` script, you 
need to have a ready-to-use `.env` in the project root with correct values.

**IMPORTANT NOTE:** The `start.sh` script contains some complex logic: it checks 
that a volume with the original database (golden) exists, and if necessary 
deploys the dump into it. Then it cleans up the runtime volume from previous 
runs if needed and creates a new runtime copy of the original database for the 
current run. It also passes a subset of necessary arguments to docker-compose. 
Therefore, it is recommended to run *exclusively* the ready `start.sh`.

---

### Tests:

1. Single create
2. Transaction create
3. Bulk create
4. Find all
5. Find first
6. Find unique record
7. Find with limit and include parent
8. Find with filter, offset pagination and sort
9. Single update
10. Transaction update
11. Bulk update
12. Single delete 
13. Transaction delete
14. Bulk delete

---

- Stack: Python 3.12, PostgreSQL 17, Psycopg 2.9.11/3.3.2.
- ORMs included: Django, Peewee, Pony, SQLAlchemy, SQLModel.
- Authors: student research team.
- License: MIT.