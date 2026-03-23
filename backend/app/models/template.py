from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    version = Column(Integer, default=1)
    parent_id = Column(String, ForeignKey("templates.id"), nullable=True)
    original_filename = Column(String)
    file_path = Column(String, nullable=False)
    placeholders = Column(Text)  # JSON 数组存储占位符列表
    is_default = Column(Boolean, default=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", backref="templates")
    generated_docs = relationship("GeneratedDocument", back_populates="template")
