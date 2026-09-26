from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Click


def record_click_event(link_id: int, ip_address: str | None, user_agent: str | None):
    """Background task function to record a click event in PostgreSQL.
    Runs asynchronously AFTER the HTTP 307 redirect response is sent to the visitor.
    """
    db: Session = SessionLocal()
    try:
        click_entry = Click(
            link_id=link_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(click_entry)
        db.commit()
    except Exception as e:
        print(f"Error recording background click event: {e}")
        db.rollback()
    finally:
        db.close()
