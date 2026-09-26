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

---

## Day 3 — Build the Doorway (2026-09-26)

**Built:** 
Built the API endpoints and utility layers: Base62 encoding/decoding helper (`utils.py`), Pydantic schemas for request validation and response formatting (`schemas.py`), `POST /shorten` endpoint (`routers/shorten.py`), and `GET /r/{short_code}` redirect endpoint (`routers/redirect.py`).

**Summary:**
Day 3 summary
this day was mainly undersanding how the FAST api works and building the same.
I also lookd into the pydantic schemas which act as a bouncer, mainly helps us to check whether the information being fed is approppriate or not.
I built the api post and get functions and also looked into the redirect component. Here i looked into the http redirect responses.
there were two options - HTTP 307 or HTTP 301.
I chosed HTTP 307 since it will help me to keep the accurate count of the number of visits.
Also the software will throw a HTTP 404 error if the short limk does not exist

**Learned:** 
- Base62 algorithm uses `divmod(num, 62)` iteratively to pick characters from `0-9a-zA-A`.
- Pydantic schemas validate types and prevent invalid or missing payloads from reaching PostgreSQL.
- HTTP 307 Temporary Redirect is non-negotiable for analytics tracking because HTTP 301 Permanent Redirect causes browsers to cache redirects locally on disk, skipping future server hits.

**Open Question:** 
What happens if a high volume of concurrent users click a link while background click analytics are being recorded?


