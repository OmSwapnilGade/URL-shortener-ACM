from datetime import datetime
from pydantic import BaseModel, ConfigDict


class URLCreate(BaseModel):
    """Schema for incoming request when shortening a URL."""
    original_url: str


class URLResponse(BaseModel):
    """Schema for outgoing response after shortening a URL."""
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClickResponse(BaseModel):
    """Schema for individual click event analytics."""
    id: int
    clicked_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AnalyticsResponse(BaseModel):
    """Schema for aggregated link analytics summary."""
    short_code: str
    original_url: str
    created_at: datetime
    total_clicks: int
    recent_clicks: list[ClickResponse]

    model_config = ConfigDict(from_attributes=True)
