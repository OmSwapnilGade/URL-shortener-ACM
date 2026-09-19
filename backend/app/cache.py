import os
import redis

# 1. Redis Connection URL (defaulting to local Redis port 6379)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 2. Redis Client Instance (decode_responses=True returns strings instead of raw bytes)
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# 3. Default TTL: 24 hours (86400 seconds)
DEFAULT_TTL = 86400


def get_cached_url(short_code: str) -> str | None:
    """Look up a short code in Redis cache. Returns original_url or None."""
    try:
        return redis_client.get(short_code)
    except Exception as e:
        # Graceful degradation: if Redis is down, log warning and return None (fallback to DB)
        print(f"Redis Cache Warning: {e}")
        return None


def set_cached_url(short_code: str, original_url: str, ttl: int = DEFAULT_TTL) -> bool:
    """Store a short_code -> original_url mapping in Redis with 24h TTL."""
    try:
        return redis_client.setex(short_code, ttl, original_url)
    except Exception as e:
        # Graceful degradation
        print(f"Redis Cache Warning: {e}")
        return False
