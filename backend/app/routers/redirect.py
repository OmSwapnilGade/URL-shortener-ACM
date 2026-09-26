from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Link
from ..cache import get_cached_url, set_cached_url
from ..utils import decode_base62
from ..services.analytics import record_click_event

router = APIRouter(tags=["Redirect"])


@router.get("/r/{short_code}")
def redirect_to_url(
    short_code: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Redirects short_code to original URL using HTTP 307 Temporary Redirect.
    Records click analytics in the background without blocking the visitor.
    """
    # Extract client IP and browser User-Agent
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    # 1. Check Redis cache first (Fast path ~0.8ms)
    cached_url = get_cached_url(short_code)
    if cached_url:
        try:
            link_id = decode_base62(short_code)
            background_tasks.add_task(
                record_click_event,
                link_id=link_id,
                ip_address=ip_address,
                user_agent=user_agent,
            )
        except Exception:
            pass

        return RedirectResponse(
            url=cached_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    # 2. Cache MISS: Query PostgreSQL database (~15ms)
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    # 3. Write back to Redis cache for future requests
    set_cached_url(short_code, link.original_url)

    # 4. Schedule background analytics task
    background_tasks.add_task(
        record_click_event,
        link_id=link.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # 5. Return HTTP 307 Temporary Redirect
    return RedirectResponse(
        url=link.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
