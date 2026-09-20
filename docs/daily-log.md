# Daily Log

## Day 1 — Understand & Plan (2026-09-18)

**Built / Planned:** 
Planned the system architecture (User → Waiter/FastAPI → Cache/Redis → Filing Cabinet/PostgreSQL). Decided to use sequential DB IDs encoded in Base62 for short code generation to prevent collisions and avoid repetitive database check loops.

**Broke / Debugged:** 
No code broken today — focused on first-principles system architecture planning and tradeoffs.

**Learned:** 
- Base62 (0-9, a-z, A-Z) is completely URL-safe unlike Base64 which uses `+` and `/`.
- Cache (Redis in RAM) sits in front of the Database (Postgres on disk) because reading from memory is ~20-50x faster than disk, protecting the database under high read traffic.

**Open Question:** 
How does PostgreSQL handle auto-incrementing sequential IDs efficiently under high concurrent write loads?

---

## Day 2 — Build the Memory (2026-09-20)

**Built:** 
Built the backend core: PostgreSQL connection engine & session dependency (`database.py`), SQLAlchemy ORM blueprints for `Link` and `Click` tables with two-way relationships (`models.py`), and Redis caching layer (`cache.py`) with 24-hour TTL and graceful degradation.

**Summary:**
Day 2 was mainly building majority of backend of the applications. Today i completed making the database, models and also putting a layer of cache using the redis.
The database was a PostgreSQl because postregs is a RDBMS, which was suitable for our project. I also looked into the SQLAlchemy engine which acts as ORM.
ORM(object relational mapper) helps to connect the classes and objects in programming languages like python with the database. The database folder mainly aimed to connect with the postgres whenever a session was called.

Models - It included the blueprint or simply the python classes required for database table which included the links and clicks table. I also developed a relationship between the tables.

the init_.py helps in creating a app or package.
The cache was brought into the picture using redis

**Learned:** 
- An ORM (Object-Relational Mapper) acts as a bridge connecting Python classes with relational database tables.
- Storing `link_id` (foreign key) in the `clicks` table normalizes data and prevents wasting massive storage space compared to duplicating the long URL string repeatedly.
- Wrapping Redis calls in `try...except` ensures graceful degradation so that if Redis crashes, the application falls back safely to PostgreSQL instead of breaking for the user.

**Open Question:** 
How does Redis manage memory eviction internally if maxmemory limit is reached before the 24-hour TTL expires?

