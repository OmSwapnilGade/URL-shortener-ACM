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
