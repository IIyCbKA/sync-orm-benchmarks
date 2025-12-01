ORM & SQL Performance Bench (Python 3.12, Postgres)
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

**IMPORTANT NOTE:** On each fresh run of `docker-compose` you must clear all volumes and any references from previous runs.

Stack: Python 3.12, PostgreSQL.\
ORMs included: Pony ORM, Django ORM, SQLAlchemy, Tortoise ORM — plus raw SQL baseline.\
Authors: student research team.\
License: MIT.