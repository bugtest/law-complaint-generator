from sqlalchemy import Column, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CaseStatus(str, enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    case_name = Column(String, nullable=False)
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    elements = relationship("ExtractedElements", back_populates="case", uselist=False, cascade="all, delete-orphan")
    generated_docs = relationship("GeneratedDocument", back_populates="case", cascade="all, delete-orphan")
