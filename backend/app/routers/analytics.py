from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Link, Click
from ..schemas import AnalyticsResponse, ClickResponse

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/{short_code}", response_model=AnalyticsResponse)
def get_link_analytics(short_code: str, db: Session = Depends(get_db)):
    """Fetches total click count and recent click history for a given short_code."""
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    # Count total clicks for this link
    total_clicks = db.query(Click).filter(Click.link_id == link.id).count()

    # Fetch the 20 most recent clicks
    recent_clicks_db = (
        db.query(Click)
        .filter(Click.link_id == link.id)
        .order_by(Click.clicked_at.desc())
        .limit(20)
        .all()
    )

    recent_clicks = [
        ClickResponse(
            id=c.id,
            clicked_at=c.clicked_at,
            ip_address=c.ip_address,
            user_agent=c.user_agent,
        )
        for c in recent_clicks_db
    ]

    return AnalyticsResponse(
        short_code=link.short_code,
        original_url=link.original_url,
        created_at=link.created_at,
        total_clicks=total_clicks,
        recent_clicks=recent_clicks,
    )
