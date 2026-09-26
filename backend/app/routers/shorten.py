from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Link
from ..schemas import URLCreate, URLResponse
from ..utils import encode_base62
from ..cache import set_cached_url

router = APIRouter(tags=["Shorten"])


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate, request: Request, db: Session = Depends(get_db)):
    """Creates a short link from a long URL."""
    if not payload.original_url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # 1. Create initial Link row in Postgres to get assigned primary key id
    new_link = Link(original_url=payload.original_url)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    # 2. Encode assigned integer ID to Base62 short_code
    short_code = encode_base62(new_link.id)
    new_link.short_code = short_code
    db.commit()
    db.refresh(new_link)

    # 3. Cache short_code -> original_url in Redis
    set_cached_url(short_code, payload.original_url)

    # 4. Construct full short URL (e.g. http://localhost:8000/r/q0U)
    base_url = str(request.base_url).rstrip("/")
    short_url = f"{base_url}/r/{short_code}"

    return URLResponse(
        short_code=new_link.short_code,
        short_url=short_url,
        original_url=new_link.original_url,
        created_at=new_link.created_at,
    )
