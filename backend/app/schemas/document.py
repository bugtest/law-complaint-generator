from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentTypeEnum(str):
    EVIDENCE_PDF = "evidence_pdf"
    ORGANIZED_WORD = "organized_word"

class DocumentUploadResponse(BaseModel):
    id: str
    case_id: str
    type: str
    original_filename: str
    file_size: Optional[int] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    case_id: str
    type: str
    original_filename: str
    file_size: Optional[int] = None
    parsed_text: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True
