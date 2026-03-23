from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class ExtractedElements(Base):
    __tablename__ = "extracted_elements"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.id"), unique=True, nullable=False)

    # 原告信息 (JSON)
    plaintiff = Column(Text)  # JSON 存储：{"name", "id_number", "address", "phone"}

    # 被告信息 (JSON)
    defendant = Column(Text)  # JSON 存储：{"name", "id_number", "address", "phone"}

    # 诉讼请求 (JSON 数组)
    claims = Column(Text)  # JSON 存储：[{"order", "content"}]

    # 事实与理由
    facts_and_reasons = Column(Text)

    # 证据清单 (JSON 数组)
    evidence_list = Column(Text)  # JSON 存储：[{"name", "purpose", "page"}]

    # 审核状态
    reviewed = Column(Boolean, default=False)
    ai_confidence = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    case = relationship("Case", back_populates="elements")

class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    template_id = Column(String, ForeignKey("templates.id"), nullable=False)
    original_filename = Column(String)
    file_path = Column(String, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    case = relationship("Case", back_populates="generated_docs")
    template = relationship("Template", back_populates="generated_docs")
