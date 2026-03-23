from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

CaseStatusEnum = Literal["draft", "processing", "completed"]

class CaseCreate(BaseModel):
    case_name: str = Field(..., min_length=1, max_length=200)

class CaseUpdate(BaseModel):
    case_name: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[CaseStatusEnum] = None

class CaseResponse(BaseModel):
    id: str
    user_id: str
    case_name: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
