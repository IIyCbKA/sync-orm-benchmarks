ORM & SQL Performance Bench [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/IIyCbKA/sql-orm-benchmarks/blob/main/LICENSE) [![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3120/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
==============

A reproducible benchmarking project to compare raw SQL and popular Python ORMs on PostgreSQL.

The primary database schema used in this project is the demonstration schema 
provided by Postgres Professional: https://postgrespro.ru/education/demodb. 
For reproducibility, each benchmark run is initialized from the one-year dump 
`demo-20250901-1y.sql.gz`, available at 
https://edu.postgrespro.ru/demo-20250901-1y.sql.gz. The dump is restored 
immediately prior to testing so that every run starts from the same dataset. 

For stability the dump has been incorporated into the database image and 
published on Docker Hub at: 
https://hub.docker.com/repository/docker/iiycbka/sql-orm-benchmarks-db.

---

### Running

For convenience (it's recommended), ready-to-use `start.sh`, `stop.sh` and 
`logs.sh` scripts are included in the repository root. Simply run them from 
the repo root. Specify the solution name (required) and the mode name 
(optional) for `start.sh`.

Each benchmark prints its result to stdout. These stdout lines are captured 
by Docker and can be viewed via the runner container logs.

Usage example:
```bash
# from repo root
# create and run containers
./start.sh <solution> <mode>

# follow live runner logs
./logs.sh

# stop and remove containers, networks and runtime volumes
./stop.sh
```

List of existing solutions available for start/stop/logs (use the solution 
name from this list for `./start.sh`):
- django
- pony
- sqlalchemy

List of modes for solutions (use the mode name from this list for `./start.sh`, 
with selected solution. Default is sync):
- sync: django | pony | sqlalchemy
- async: django | sqlalchemy

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
2. Batch create
3. Bulk create
4. Nested create
5. Find all
6. Find first
7. Nested find first
8. Find unique
9. Nested find unique
10. Filter, paginate & sort
11. Update batch
12. Update single
13. Nested batch update
14. Batch delete

---

- Stack: Python 3.12, PostgreSQL.
- ORMs included: Pony, Django, SQLAlchemy, Tortoise.
- Authors: student research team.
- License: MIT.