# URL Shortener with Analytics Dashboard

A high-performance URL shortener built with FastAPI, PostgreSQL, Redis, and React.
Designed as part of the ACM VNIT Project & Mentorship Track (Team BongaGPT).

## Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (Permanent storage)
- **Cache**: Redis (Fast in-memory cache)
- **Frontend**: React (Analytics dashboard)

## Architecture & Design Decisions
- **Short Code Generation**: Sequential auto-incrementing Database ID encoded in Base62 (`0-9`, `a-z`, `A-Z`) to guarantee zero collisions without repeated DB lookup queries.
- **Cache Layer**: Redis sits in front of PostgreSQL to serve read-heavy redirect queries in sub-millisecond latency (~0.8ms).
- **Asynchronous Analytics**: Non-blocking background workers record click metadata so visitors experience instant redirection.
