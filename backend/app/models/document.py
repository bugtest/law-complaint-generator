from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class DocumentType(str, enum.Enum):
    EVIDENCE_PDF = "evidence_pdf"
    ORGANIZED_WORD = "organized_word"

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    type = Column(SQLEnum(DocumentType), nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    parsed_text = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    case = relationship("Case", back_populates="documents")
