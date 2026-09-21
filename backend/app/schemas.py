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
