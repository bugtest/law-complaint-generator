from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PlaintiffInfo(BaseModel):
    name: Optional[str] = None
    id_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class DefendantInfo(BaseModel):
    name: Optional[str] = None
    id_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class ClaimItem(BaseModel):
    order: int
    content: str

class EvidenceItem(BaseModel):
    name: str
    purpose: Optional[str] = None
    page: Optional[int] = None

class ElementResponse(BaseModel):
    id: str
    case_id: str
    plaintiff: Optional[PlaintiffInfo] = None
    defendant: Optional[DefendantInfo] = None
    claims: Optional[List[ClaimItem]] = None
    facts_and_reasons: Optional[str] = None
    evidence_list: Optional[List[EvidenceItem]] = None
    reviewed: bool
    ai_confidence: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ElementUpdate(BaseModel):
    plaintiff: Optional[PlaintiffInfo] = None
    defendant: Optional[DefendantInfo] = None
    claims: Optional[List[ClaimItem]] = None
    facts_and_reasons: Optional[str] = None
    evidence_list: Optional[List[EvidenceItem]] = None
    reviewed: Optional[bool] = None
