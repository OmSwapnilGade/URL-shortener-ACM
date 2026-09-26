from fastapi import FastAPI
from .database import engine, Base
from .routers import shorten, redirect, analytics

# Automatically create PostgreSQL tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="High-performance URL Shortener backend built with FastAPI, PostgreSQL, and Redis",
    version="1.0.0",
)

# Include API Routers
app.include_router(shorten.router)
app.include_router(redirect.router)
app.include_router(analytics.router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "URL Shortener API is running!"}
