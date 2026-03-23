from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TemplateResponse(BaseModel):
    id: str
    user_id: str
    name: str
    version: int
    original_filename: Optional[str] = None
    placeholders: Optional[List[str]] = None
    is_default: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True

class TemplateUploadResponse(BaseModel):
    id: str
    name: str
    version: int
    placeholders: List[str]
    message: str
