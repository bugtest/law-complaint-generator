# 要素式起诉状生成系统实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个完整的 Web 应用系统，允许律师上传 PDF 证据和 Word 整理文档，通过 AI 自动提取案件要素，并使用 Word 模板生成符合国家标准的要素式起诉状。

**Architecture:** 前后端分离架构。后端使用 FastAPI 提供 REST API，负责文档解析、AI 要素提取、模板管理和文书生成；前端使用 Vue 3 + Element Plus 构建用户界面；数据库使用 SQLite（可升级到 PostgreSQL）存储用户、案件、文档和模板元数据；文件系统存储上传的文档和生成的文书。

**Tech Stack:**
- 后端：FastAPI, SQLAlchemy, JWT, bcrypt, pdfplumber, PyMuPDF, PaddleOCR, python-docx, Anthropic SDK
- 前端：Vue 3, Element Plus, Vite, Axios
- 数据库：SQLite / PostgreSQL
- 测试：pytest, pytest-asyncio, Playwright

---

## 项目目录结构

```
/root/code/law/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   ├── models/              # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── case.py
│   │   │   ├── document.py
│   │   │   ├── template.py
│   │   │   └── element.py
│   │   ├── schemas/             # Pydantic 模式
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── case.py
│   │   │   ├── document.py
│   │   │   ├── template.py
│   │   │   └── element.py
│   │   ├── routers/             # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── cases.py
│   │   │   ├── documents.py
│   │   │   ├── templates.py
│   │   │   └── generate.py
│   │   ├── services/            # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── word_parser.py
│   │   │   ├── ocr_engine.py
│   │   │   ├── ai_extractor.py
│   │   │   ├── template_engine.py
│   │   │   └── document_generator.py
│   │   ├── utils/               # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── file_validator.py
│   │   └── middleware/          # 中间件
│   │       ├── __init__.py
│   │       └── auth.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_cases.py
│   │   ├── test_documents.py
│   │   ├── test_templates.py
│   │   └── test_generation.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── stores/
│   │   │   ├── user.js
│   │   │   └── cases.js
│   │   ├── api/
│   │   │   └── index.js
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── cases/
│   │   │   ├── documents/
│   │   │   ├── elements/
│   │   │   └── templates/
│   │   └── views/
│   │       ├── Login.vue
│   │       ├── CaseList.vue
│   │       ├── CaseDetail.vue
│   │       ├── DocumentUpload.vue
│   │       ├── ElementReview.vue
│   │       ├── TemplateManage.vue
│   │       └── DocumentPreview.vue
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── superpowers/
│   │   ├── specs/
│   │   └── plans/
│   └── storage/                 # 文件存储目录
│       ├── uploads/
│       ├── templates/
│       └── generated/
└── README.md
```

---

## Phase 1: 后端基础架构

### Task 1: 项目初始化与配置

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env.example`
- Create: `backend/app/config.py`
- Create: `backend/app/database.py`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`

- [ ] **Step 1: 创建 requirements.txt**

```text
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
aiosqlite==0.19.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2

# Document Processing
pdfplumber==0.10.3
PyMuPDF==1.23.8
python-docx==1.1.0
paddlepaddle==2.6.1
paddleocr==2.7.3

# AI
anthropic==0.18.0

# Config
python-dotenv==1.0.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

- [ ] **Step 2: 创建 .env.example**

```bash
# 数据库
DATABASE_URL=sqlite:///./law_system.db

# JWT 配置
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_EXPIRE_HOURS=24
ALGORITHM=HS256

# 文件存储
FILE_STORAGE_PATH=./docs/storage
MAX_FILE_SIZE_MB=50

# AI 配置
ANTHROPIC_API_KEY=your-api-key
AI_MODEL=claude-sonnet-4-20250514

# OCR 配置
OCR_ENABLED=true
OCR_LANGUAGE=ch

# 日志
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

- [ ] **Step 3: 创建 config.py**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据库
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/law_system.db")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-me")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# 文件存储
FILE_STORAGE_PATH = Path(os.getenv("FILE_STORAGE_PATH", BASE_DIR / "docs" / "storage"))
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

# AI
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-20250514")

# OCR
OCR_ENABLED = os.getenv("OCR_ENABLED", "true").lower() == "true"
OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "ch")

# 日志
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = Path(os.getenv("LOG_FILE", BASE_DIR / "logs" / "app.log"))
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
```

- [ ] **Step 4: 创建 database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 5: 创建 app/__init__.py**

```python
# App package
```

- [ ] **Step 6: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import BASE_DIR
from .database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="要素式起诉状生成系统",
    description="律师专用 - AI 驱动的法律文书生成系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "要素式起诉状生成系统 API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

- [ ] **Step 7: 运行测试确保项目可以启动**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Expected: Server starts at http://localhost:8000

- [ ] **Step 8: Commit**

```bash
git add .
git commit -m "feat: initialize backend project structure"
```

---

### Task 2: 数据模型定义

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/case.py`
- Create: `backend/app/models/document.py`
- Create: `backend/app/models/template.py`
- Create: `backend/app/models/element.py`

- [ ] **Step 1: 创建 models/__init__.py**

```python
from .user import User
from .case import Case
from .document import Document
from .template import Template
from .element import ExtractedElements
from .audit import AuditLog

__all__ = ["User", "Case", "Document", "Template", "ExtractedElements", "AuditLog"]
```

- [ ] **Step 2: 创建 user.py**

```python
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

- [ ] **Step 3: 创建 case.py**

```python
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
```

- [ ] **Step 4: 创建 document.py**

```python
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
```

- [ ] **Step 5: 创建 template.py**

```python
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
```

- [ ] **Step 6: 创建 element.py**

```python
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
```

- [ ] **Step 7: 创建 audit.py**

```python
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip_address = Column(String)
```

- [ ] **Step 8: 运行数据库迁移验证模型**

```bash
cd backend
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine); print('Database tables created')"
```
Expected: "Database tables created"

- [ ] **Step 9: Commit**

```bash
git add backend/app/models/
git commit -m "feat: define database models"
```

---

### Task 3: Pydantic Schemas 定义

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/user.py`
- Create: `backend/app/schemas/case.py`
- Create: `backend/app/schemas/document.py`
- Create: `backend/app/schemas/template.py`
- Create: `backend/app/schemas/element.py`

- [ ] **Step 1: 创建 schemas/__init__.py**

```python
from .user import UserCreate, UserLogin, UserResponse
from .case import CaseCreate, CaseResponse, CaseUpdate
from .document import DocumentResponse, DocumentUploadResponse
from .template import TemplateResponse, TemplateUploadResponse
from .element import ElementResponse, ElementUpdate, PlaintiffInfo, DefendantInfo, ClaimItem, EvidenceItem

__all__ = [
    "UserCreate", "UserLogin", "UserResponse",
    "CaseCreate", "CaseResponse", "CaseUpdate",
    "DocumentResponse", "DocumentUploadResponse",
    "TemplateResponse", "TemplateUploadResponse",
    "ElementResponse", "ElementUpdate",
    "PlaintiffInfo", "DefendantInfo", "ClaimItem", "EvidenceItem"
]
```

- [ ] **Step 2: 创建 user.py**

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

- [ ] **Step 3: 创建 case.py**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .document import DocumentResponse
from .element import ElementResponse

class CaseStatusEnum(str):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"

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
```

- [ ] **Step 4: 创建 document.py**

```python
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
```

- [ ] **Step 5: 创建 template.py**

```python
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
```

- [ ] **Step 6: 创建 element.py**

```python
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
```

- [ ] **Step 7: Commit**

```bash
git add backend/app/schemas/
git commit -m "feat: define Pydantic schemas for API"
```

---

### Task 4: 安全工具与文件验证

**Files:**
- Create: `backend/app/utils/__init__.py`
- Create: `backend/app/utils/security.py`
- Create: `backend/app/utils/file_validator.py`

- [ ] **Step 1: 创建 utils/__init__.py**

```python
from .security import hash_password, verify_password, create_access_token
from .file_validator import validate_file_type, validate_file_size

__all__ = [
    "hash_password", "verify_password", "create_access_token",
    "validate_file_type", "validate_file_size"
]
```

- [ ] **Step 2: 创建 security.py**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..config import JWT_SECRET_KEY, ALGORITHM, JWT_EXPIRE_HOURS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

- [ ] **Step 3: 创建 file_validator.py**

```python
from pathlib import Path
from typing import Tuple, Optional
import mimetypes

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
ALLOWED_MIME_TYPES = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

def validate_file_type(filename: str, file_content: bytes) -> Tuple[bool, Optional[str]]:
    """
    Validate file type by extension and magic bytes
    Returns: (is_valid, error_message)
    """
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        return False, f"不支持的文件类型：{ext}，仅支持 PDF/DOC/DOCX"

    # 简单的魔术字节检查
    if ext == ".pdf" and not file_content.startswith(b"%PDF"):
        return False, "无效的 PDF 文件"

    if ext == ".docx":
        # DOCX 是 ZIP 格式
        if not (file_content.startswith(b"PK") or file_content.startswith(b"\xd0\xcf")):
            return False, "无效的 DOCX 文件"

    return True, None

def validate_file_size(file_size: int, max_size_mb: int = 50) -> Tuple[bool, Optional[str]]:
    """
    Validate file size
    Returns: (is_valid, error_message)
    """
    max_size = max_size_mb * 1024 * 1024
    if file_size > max_size:
        return False, f"文件大小超过限制 ({max_size_mb}MB)"
    if file_size == 0:
        return False, "空文件"
    return True, None
```

- [ ] **Step 4: 编写 security.py 的单元测试**

Create: `backend/tests/test_security.py`

```python
import pytest
from app.utils.security import hash_password, verify_password, create_access_token, verify_token

def test_hash_password():
    password = "testpassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 0

def test_verify_password_correct():
    password = "testpassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "testpassword123"
    hashed = hash_password(password)
    assert verify_password("wrongpassword", hashed) is False

def test_create_and_verify_token():
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_access_token(data)
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"

def test_verify_invalid_token():
    assert verify_token("invalid-token") is None
```

- [ ] **Step 5: 运行测试**

```bash
cd backend
pytest tests/test_security.py -v
```
Expected: All 5 tests pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/utils/ backend/tests/test_security.py
git commit -m "feat: add security utilities and file validator"
```

---

## Phase 2: 核心服务层

### Task 5: PDF 解析服务

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/pdf_parser.py`

- [ ] **Step 1: 创建 services/__init__.py**

```python
from .pdf_parser import PDFParser
from .word_parser import WordParser
from .ocr_engine import OCREngine
from .ai_extractor import AIExtractor
from .template_engine import TemplateEngine
from .document_generator import DocumentGenerator

__all__ = [
    "PDFParser", "WordParser", "OCREngine",
    "AIExtractor", "TemplateEngine", "DocumentGenerator"
]
```

- [ ] **Step 2: 创建 pdf_parser.py**

```python
from pathlib import Path
from typing import Optional, Dict, Any
import pdfplumber
import fitz  # PyMuPDF

class PDFParser:
    """PDF document parser with text extraction capabilities"""

    @staticmethod
    def extract_text(file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF file

        Returns:
            {
                "success": bool,
                "text": str,
                "pages": int,
                "is_scanned": bool,
                "error": Optional[str]
            }
        """
        try:
            text_parts = []
            is_scanned = False

            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                    else:
                        # No extractable text - might be scanned
                        is_scanned = True

            result = {
                "success": True,
                "text": "\n\n".join(text_parts),
                "pages": len(text_parts) if text_parts else 0,
                "is_scanned": is_scanned or len(text_parts) == 0,
                "error": None
            }

            # If completely empty, mark as scanned for OCR
            if not result["text"].strip():
                result["is_scanned"] = True

            return result

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "pages": 0,
                "is_scanned": False,
                "error": f"PDF 解析失败：{str(e)}"
            }

    @staticmethod
    def get_metadata(file_path: str) -> Dict[str, Any]:
        """Extract PDF metadata"""
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata
            doc.close()
            return {
                "success": True,
                "metadata": metadata
            }
        except Exception as e:
            return {
                "success": False,
                "metadata": {},
                "error": str(e)
            }
```

- [ ] **Step 3: 编写 PDFParser 单元测试**

Create: `backend/tests/test_pdf_parser.py`

```python
import pytest
import tempfile
import os
from pathlib import Path
from app.services.pdf_parser import PDFParser

# 创建一个简单的测试 PDF（使用 fitz）
def create_test_pdf(text_content: str = "Test PDF Content\nLine 2") -> str:
    """Create a temporary test PDF file"""
    import fitz
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_file.close()

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text_content)
    doc.save(temp_file.name)
    doc.close()

    return temp_file.name

def test_extract_text_from_pdf():
    pdf_path = create_test_pdf("Hello World\nTest Line")
    try:
        result = PDFParser.extract_text(pdf_path)
        assert result["success"] is True
        assert "Hello World" in result["text"]
        assert result["pages"] >= 1
        assert result["is_scanned"] is False
    finally:
        os.unlink(pdf_path)

def test_extract_text_nonexistent_file():
    result = PDFParser.extract_text("/nonexistent/file.pdf")
    assert result["success"] is False
    assert result["error"] is not None

def test_get_metadata():
    pdf_path = create_test_pdf("Metadata Test")
    try:
        result = PDFParser.get_metadata(pdf_path)
        assert result["success"] is True
        assert isinstance(result["metadata"], dict)
    finally:
        os.unlink(pdf_path)
```

- [ ] **Step 4: 运行测试**

```bash
cd backend
pytest tests/test_pdf_parser.py -v
```
Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/pdf_parser.py backend/tests/test_pdf_parser.py
git commit -m "feat: implement PDF parser service"
```

---

### Task 6: Word 文档解析服务

**Files:**
- Create: `backend/app/services/word_parser.py`

- [ ] **Step 1: 创建 word_parser.py**

```python
from pathlib import Path
from typing import Dict, Any, List
from docx import Document
from docx.oxml.ns import qn

class WordParser:
    """Word document parser with text extraction capabilities"""

    @staticmethod
    def extract_text(file_path: str) -> Dict[str, Any]:
        """
        Extract text from Word document

        Returns:
            {
                "success": bool,
                "text": str,
                "paragraphs": List[str],
                "has_styles": bool,
                "error": Optional[str]
            }
        """
        try:
            doc = Document(file_path)
            paragraphs = []
            has_styles = False

            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text.strip())
                    # Check if paragraph has special styling
                    if para.style and para.style.name != "Normal":
                        has_styles = True

            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        paragraphs.append(" | ".join(row_text))

            result = {
                "success": True,
                "text": "\n\n".join(paragraphs),
                "paragraphs": paragraphs,
                "has_styles": has_styles,
                "error": None
            }

            return result

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "paragraphs": [],
                "has_styles": False,
                "error": f"Word 解析失败：{str(e)}"
            }

    @staticmethod
    def extract_placeholders(file_path: str, placeholder_pattern: str = "{{") -> Dict[str, Any]:
        """
        Extract placeholders from Word template

        Returns:
            {
                "success": bool,
                "placeholders": List[str],
                "error": Optional[str]
            }
        """
        try:
            text_result = WordParser.extract_text(file_path)
            if not text_result["success"]:
                return {"success": False, "placeholders": [], "error": text_result["error"]}

            import re
            # Find all {{xxx}} patterns
            pattern = r"\{\{([^}]+)\}\}"
            matches = re.findall(pattern, text_result["text"])

            # Clean up placeholder names
            placeholders = list(set([m.strip() for m in matches]))

            return {
                "success": True,
                "placeholders": placeholders,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "placeholders": [],
                "error": f"占位符提取失败：{str(e)}"
            }
```

- [ ] **Step 2: 编写 WordParser 单元测试**

Create: `backend/tests/test_word_parser.py`

```python
import pytest
import tempfile
import os
from docx import Document
from app.services.word_parser import WordParser

def create_test_docx(paragraphs: list) -> str:
    """Create a temporary test DOCX file"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    temp_file.close()

    doc = Document()
    for para in paragraphs:
        doc.add_paragraph(para)
    doc.save(temp_file.name)

    return temp_file.name

def test_extract_text_from_docx():
    content = ["原告张三", "被告李四", "诉讼请求：偿还借款 10 万元"]
    docx_path = create_test_docx(content)
    try:
        result = WordParser.extract_text(docx_path)
        assert result["success"] is True
        assert "原告张三" in result["text"]
        assert len(result["paragraphs"]) == 3
    finally:
        os.unlink(docx_path)

def test_extract_placeholders():
    content = ["原告：{{原告姓名}}", "被告：{{被告姓名}}", "请求：{{诉讼请求}}"]
    docx_path = create_test_docx(content)
    try:
        result = WordParser.extract_placeholders(docx_path)
        assert result["success"] is True
        assert "原告姓名" in result["placeholders"]
        assert "被告姓名" in result["placeholders"]
        assert "诉讼请求" in result["placeholders"]
    finally:
        os.unlink(docx_path)

def test_extract_text_nonexistent_file():
    result = WordParser.extract_text("/nonexistent/file.docx")
    assert result["success"] is False
    assert result["error"] is not None
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_word_parser.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/word_parser.py backend/tests/test_word_parser.py
git commit -m "feat: implement Word parser service with placeholder extraction"
```

---

### Task 7: OCR 引擎服务

**Files:**
- Create: `backend/app/services/ocr_engine.py`

- [ ] **Step 1: 创建 ocr_engine.py**

```python
from pathlib import Path
from typing import Dict, Any, Optional
import fitz  # PyMuPDF
from ..config import OCR_ENABLED, OCR_LANGUAGE

class OCREngine:
    """OCR engine for scanned PDF documents"""

    def __init__(self):
        self.enabled = OCR_ENABLED
        self.language = OCR_LANGUAGE
        self._ocr = None

    def _init_ocr(self):
        """Lazy initialize PaddleOCR"""
        if self._ocr is None:
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.language,
                show_log=False
            )

    def extract_text_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from scanned PDF using OCR

        Returns:
            {
                "success": bool,
                "text": str,
                "confidence": float,
                "pages": int,
                "error": Optional[str]
            }
        """
        if not self.enabled:
            return {
                "success": False,
                "text": "",
                "confidence": 0,
                "pages": 0,
                "error": "OCR 功能未启用"
            }

        try:
            self._init_ocr()

            # Convert PDF pages to images and OCR
            pdf_doc = fitz.open(file_path)
            all_text = []
            confidences = []

            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                # Render page to image (72 DPI)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                img_data = pix.tobytes("png")

                # Perform OCR
                result = self._ocr.ocr(img_data, cls=True)

                page_text = []
                page_conf = []

                if result and result[0]:
                    for line in result[0]:
                        bbox, (text, confidence) = line
                        page_text.append(text)
                        page_conf.append(confidence)

                if page_text:
                    all_text.append("\n".join(page_text))
                    if page_conf:
                        confidences.extend(page_conf)

            pdf_doc.close()

            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            return {
                "success": True,
                "text": "\n\n".join(all_text),
                "confidence": avg_confidence,
                "pages": len(all_text),
                "error": None
            }

        except ImportError:
            return {
                "success": False,
                "text": "",
                "confidence": 0,
                "pages": 0,
                "error": "PaddleOCR 未安装，请运行：pip install paddlepaddle paddleocr"
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "confidence": 0,
                "pages": 0,
                "error": f"OCR 识别失败：{str(e)}"
            }

    def get_status(self) -> Dict[str, Any]:
        """Get OCR engine status"""
        return {
            "enabled": self.enabled,
            "language": self.language,
            "initialized": self._ocr is not None
        }
```

- [ ] **Step 2: 编写 OCREngine 单元测试**

Create: `backend/tests/test_ocr_engine.py`

```python
import pytest
from app.services.ocr_engine import OCREngine
from app.config import OCR_ENABLED

def test_ocr_engine_initial_state():
    engine = OCREngine()
    status = engine.get_status()
    assert "enabled" in status
    assert "language" in status
    assert status["initialized"] is False  # Not initialized yet

@pytest.mark.skipif(not OCR_ENABLED, reason="OCR not enabled in test environment")
def test_ocr_status():
    engine = OCREngine()
    status = engine.get_status()
    assert status["enabled"] is True
    assert status["language"] == "ch"
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_ocr_engine.py -v
```
Expected: Tests pass (OCR test may be skipped if not enabled)

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/ocr_engine.py backend/tests/test_ocr_engine.py
git commit -m "feat: implement OCR engine service for scanned documents"
```

---

### Task 8: AI 要素提取服务

**Files:**
- Create: `backend/app/services/ai_extractor.py`

- [ ] **Step 1: 创建 ai_extractor.py**

```python
import json
from typing import Dict, Any, Optional
from ..config import ANTHROPIC_API_KEY, AI_MODEL

class AIExtractor:
    """AI-powered element extraction from legal documents"""

    EXTRACTION_PROMPT = """你是一位专业的法律文书助手。请从以下文档中提取起诉状的要素信息。

【原始证据内容】
{evidence_text}

【律师整理内容】
{organized_text}

请提取以下要素，以 JSON 格式返回：

1. 原告信息 (plaintiff):
   - name: 姓名
   - id_number: 身份证号（如有）
   - address: 地址
   - phone: 联系电话

2. 被告信息 (defendant):
   - name: 姓名
   - id_number: 身份证号（如有）
   - address: 地址
   - phone: 联系电话

3. 诉讼请求 (claims): 数组，每项包含
   - order: 序号
   - content: 请求内容

4. 事实与理由 (facts_and_reasons): 详细叙述

5. 证据清单 (evidence_list): 数组，每项包含
   - name: 证据名称
   - purpose: 证明目的
   - page: 页码

请确保 JSON 格式正确，如果某些信息无法识别，对应字段留空或设为 null。
同时请给出置信度评分 (0-1)。

返回格式：
{{
    "plaintiff": {{...}},
    "defendant": {{...}},
    "claims": [...],
    "facts_and_reasons": "...",
    "evidence_list": [...],
    "confidence": 0.xx
}}
"""

    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.model = AI_MODEL
        self._client = None

    def _init_client(self):
        """Lazy initialize Anthropic client"""
        if self._client is None and self.api_key:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)

    def extract_elements(self, evidence_text: str, organized_text: str) -> Dict[str, Any]:
        """
        Extract legal elements from documents using AI

        Returns:
            {
                "success": bool,
                "elements": Dict,
                "confidence": float,
                "error": Optional[str]
            }
        """
        if not self.api_key:
            return {
                "success": False,
                "elements": {},
                "confidence": 0,
                "error": "未配置 Anthropic API Key"
            }

        try:
            self._init_client()

            prompt = self.EXTRACTION_PROMPT.format(
                evidence_text=evidence_text[:8000] if evidence_text else "",
                organized_text=organized_text[:8000] if organized_text else ""
            )

            response = self._client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the response
            response_text = response.content[0].text

            # Extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                elements = json.loads(json_match.group())
                confidence = elements.pop("confidence", 0.5)

                return {
                    "success": True,
                    "elements": elements,
                    "confidence": confidence,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "elements": {},
                    "confidence": 0,
                    "error": "无法解析 AI 返回结果"
                }

        except Exception as e:
            return {
                "success": False,
                "elements": {},
                "confidence": 0,
                "error": f"AI 提取失败：{str(e)}"
            }

    def get_status(self) -> Dict[str, Any]:
        """Get AI extractor status"""
        return {
            "api_key_configured": bool(self.api_key),
            "model": self.model,
            "initialized": self._client is not None
        }
```

- [ ] **Step 2: 编写 AIExtractor 单元测试**

Create: `backend/tests/test_ai_extractor.py`

```python
import pytest
from app.services.ai_extractor import AIExtractor
from app.config import ANTHROPIC_API_KEY

def test_ai_extractor_initial_state():
    extractor = AIExtractor()
    status = extractor.get_status()
    assert "api_key_configured" in status
    assert "model" in status
    assert status["initialized"] is False

def test_ai_extractor_missing_api_key():
    # Test behavior when API key is not configured
    extractor = AIExtractor()
    result = extractor.extract_elements("", "")
    # Should fail gracefully
    assert result["success"] is False or "error" in result

@pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="Anthropic API key not configured")
def test_ai_extractor_with_api_key():
    extractor = AIExtractor()
    # This would make a real API call, so we just check it doesn't crash
    status = extractor.get_status()
    assert status["api_key_configured"] is True
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_ai_extractor.py -v
```
Expected: Tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/ai_extractor.py backend/tests/test_ai_extractor.py
git commit -m "feat: implement AI element extraction service"
```

---

### Task 9: 模板引擎服务

**Files:**
- Create: `backend/app/services/template_engine.py`

- [ ] **Step 1: 创建 template_engine.py**

```python
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from docx import Document
from docx.shared import Inches
import io

class TemplateEngine:
    """Template management and placeholder filling engine"""

    @staticmethod
    def fill_template(
        template_path: str,
        elements: Dict[str, Any],
        output_path: str
    ) -> Dict[str, Any]:
        """
        Fill Word template with extracted elements

        Args:
            template_path: Path to the Word template
            elements: Extracted elements data
            output_path: Path to save the filled document

        Returns:
            {
                "success": bool,
                "output_path": str,
                "unmatched_placeholders": List[str],
                "error": Optional[str]
            }
        """
        try:
            doc = Document(template_path)
            unmatched = []

            # Build replacement map
            replacements = TemplateEngine._build_replacement_map(elements)

            # Replace in paragraphs
            for para in doc.paragraphs:
                TemplateEngine._replace_in_paragraph(para, replacements, unmatched)

            # Replace in tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            TemplateEngine._replace_in_paragraph(para, replacements, unmatched)

            # Save the document
            doc.save(output_path)

            return {
                "success": True,
                "output_path": output_path,
                "unmatched_placeholders": list(set(unmatched)),
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "output_path": "",
                "unmatched_placeholders": [],
                "error": f"模板填充失败：{str(e)}"
            }

    @staticmethod
    def _build_replacement_map(elements: Dict[str, Any]) -> Dict[str, str]:
        """Build a map of placeholder names to their values"""
        replacements = {}

        # Plaintiff
        if elements.get("plaintiff"):
            p = elements["plaintiff"]
            replacements["原告姓名"] = p.get("name", "")
            replacements["原告身份证号"] = p.get("id_number", "")
            replacements["原告地址"] = p.get("address", "")
            replacements["原告电话"] = p.get("phone", "")

        # Defendant
        if elements.get("defendant"):
            d = elements["defendant"]
            replacements["被告姓名"] = d.get("name", "")
            replacements["被告身份证号"] = d.get("id_number", "")
            replacements["被告地址"] = d.get("address", "")
            replacements["被告电话"] = d.get("phone", "")

        # Claims
        if elements.get("claims"):
            claims_text = "\n".join([
                f"{i+1}. {c.get('content', '')}"
                for i, c in enumerate(elements["claims"])
            ])
            replacements["诉讼请求"] = claims_text

        # Facts and Reasons
        replacements["事实与理由"] = elements.get("facts_and_reasons", "")

        # Evidence List
        if elements.get("evidence_list"):
            evidence_text = "\n".join([
                f"{e.get('name', '')}: {e.get('purpose', '')}"
                for e in elements["evidence_list"]
            ])
            replacements["证据清单"] = evidence_text

        return replacements

    @staticmethod
    def _replace_in_paragraph(para, replacements: Dict[str, str], unmatched: List[str]):
        """Replace placeholders in a paragraph"""
        if "{{" not in para.text:
            return

        # Find all placeholders in the paragraph
        import re
        placeholders = re.findall(r'\{\{([^}]+)\}\}', para.text)

        for placeholder in placeholders:
            placeholder_full = "{{" + placeholder + "}}"
            if placeholder in replacements:
                # Simple text replacement
                if replacements[placeholder]:
                    para.text = para.text.replace(placeholder_full, replacements[placeholder])
                else:
                    para.text = para.text.replace(placeholder_full, "[待填写]")
            else:
                unmatched.append(placeholder)
```

- [ ] **Step 2: 编写 TemplateEngine 单元测试**

Create: `backend/tests/test_template_engine.py`

```python
import pytest
import tempfile
import os
from docx import Document
from app.services.template_engine import TemplateEngine

def create_test_template(paragraphs: list) -> str:
    """Create a temporary test template with placeholders"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    temp_file.close()

    doc = Document()
    for para in paragraphs:
        doc.add_paragraph(para)
    doc.save(temp_file.name)

    return temp_file.name

def test_build_replacement_map():
    elements = {
        "plaintiff": {"name": "张三", "id_number": "110101199001011234"},
        "defendant": {"name": "李四"},
        "claims": [{"order": 1, "content": "偿还借款 10 万元"}],
        "facts_and_reasons": "2025 年 1 月 1 日，被告向原告借款...",
        "evidence_list": [{"name": "借条", "purpose": "证明借贷关系"}]
    }

    replacements = TemplateEngine._build_replacement_map(elements)
    assert "原告姓名" in replacements
    assert replacements["原告姓名"] == "张三"
    assert "诉讼请求" in replacements

def test_fill_template():
    content = ["原告：{{原告姓名}}", "被告：{{被告姓名}}", "请求：{{诉讼请求}}"]
    template_path = create_test_template(content)
    output_path = tempfile.NamedTemporaryFile(suffix=".docx", delete=False).name
    output_path.close() if hasattr(output_path, 'close') else None

    elements = {
        "plaintiff": {"name": "张三"},
        "defendant": {"name": "李四"},
        "claims": [{"order": 1, "content": "偿还借款"}],
        "facts_and_reasons": "",
        "evidence_list": []
    }

    try:
        result = TemplateEngine.fill_template(template_path, elements, output_path)
        assert result["success"] is True
        assert os.path.exists(output_path)
    finally:
        os.unlink(template_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_template_engine.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/template_engine.py backend/tests/test_template_engine.py
git commit -m "feat: implement template engine for document generation"
```

---

### Task 10: 文书生成服务

**Files:**
- Create: `backend/app/services/document_generator.py`

- [ ] **Step 1: 创建 document_generator.py**

```python
from pathlib import Path
from typing import Dict, Any, Optional
import fitz  # PyMuPDF
from .template_engine import TemplateEngine

class DocumentGenerator:
    """Document generation service - creates final legal documents"""

    @staticmethod
    def generate_word_document(
        template_path: str,
        elements: Dict[str, Any],
        output_path: str
    ) -> Dict[str, Any]:
        """
        Generate a Word document from template and elements

        Returns:
            {
                "success": bool,
                "file_path": str,
                "file_size": int,
                "error": Optional[str]
            }
        """
        result = TemplateEngine.fill_template(template_path, elements, output_path)

        if result["success"]:
            file_size = Path(output_path).stat().st_size
            return {
                "success": True,
                "file_path": result["output_path"],
                "file_size": file_size,
                "unmatched_placeholders": result["unmatched_placeholders"],
                "error": None
            }
        else:
            return {
                "success": False,
                "file_path": "",
                "file_size": 0,
                "unmatched_placeholders": [],
                "error": result["error"]
            }

    @staticmethod
    def convert_to_pdf(word_path: str, output_pdf_path: str) -> Dict[str, Any]:
        """
        Convert Word document to PDF

        Note: This requires LibreOffice or similar
        For now, we'll use a simple approach
        """
        try:
            from docx2pdf import convert
            convert(word_path, output_pdf_path)
            return {
                "success": True,
                "file_path": output_pdf_path,
                "error": None
            }
        except ImportError:
            return {
                "success": False,
                "file_path": "",
                "error": "docx2pdf 未安装，Word to PDF 转换不可用"
            }
        except Exception as e:
            return {
                "success": False,
                "file_path": "",
                "error": f"PDF 转换失败：{str(e)}"
            }

    @staticmethod
    def get_document_info(file_path: str) -> Dict[str, Any]:
        """Get document information"""
        try:
            ext = Path(file_path).suffix.lower()
            info = {
                "success": True,
                "file_path": file_path,
                "file_size": Path(file_path).stat().st_size,
                "extension": ext
            }

            if ext == ".pdf":
                doc = fitz.open(file_path)
                info["pages"] = len(doc)
                doc.close()
            elif ext == ".docx":
                from docx import Document
                doc = Document(file_path)
                info["paragraphs"] = len(doc.paragraphs)

            return info

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

- [ ] **Step 2: 编写 DocumentGenerator 单元测试**

Create: `backend/tests/test_document_generator.py`

```python
import pytest
import tempfile
import os
from app.services.document_generator import DocumentGenerator

def test_get_document_info_docx():
    from docx import Document
    temp_file = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    temp_file.close()

    doc = Document()
    doc.add_paragraph("Test content")
    doc.save(temp_file.name)

    try:
        info = DocumentGenerator.get_document_info(temp_file.name)
        assert info["success"] is True
        assert info["extension"] == ".docx"
        assert "paragraphs" in info
    finally:
        os.unlink(temp_file.name)

def test_get_document_info_nonexistent():
    info = DocumentGenerator.get_document_info("/nonexistent/file.docx")
    assert info["success"] is False
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_document_generator.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/document_generator.py backend/tests/test_document_generator.py
git commit -m "feat: implement document generation service"
```

---

## Phase 3: API 路由层

### Task 11: 认证路由

**Files:**
- Create: `backend/app/routers/__init__.py`
- Create: `backend/app/routers/auth.py`
- Create: `backend/app/middleware/__init__.py`
- Create: `backend/app/middleware/auth.py`

- [ ] **Step 1: 创建 routers/__init__.py**

```python
from .auth import router as auth_router
from .cases import router as cases_router
from .documents import router as documents_router
from .templates import router as templates_router
from .generate import router as generate_router

__all__ = [
    "auth_router", "cases_router", "documents_router",
    "templates_router", "generate_router"
]
```

- [ ] **Step 2: 创建 auth.py**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated
import uuid

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..utils.security import hash_password, verify_password, create_access_token, verify_token

router = APIRouter(prefix="/api/auth", tags=["认证"])

security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # Check if username exists
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # Check if email exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已被禁用")

    token = create_access_token({"sub": user.id, "email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@router.post("/logout")
def logout():
    """用户登出 (客户端删除 token)"""
    return {"message": "登出成功"}

@router.get("/me", response_model=UserResponse)
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
):
    """获取当前用户信息"""
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user

# Dependency for protected routes
async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Get current user ID from token"""
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")

    return payload["sub"]
```

- [ ] **Step 3: 创建 middleware/__init__.py**

```python
# Middleware package
```

- [ ] **Step 4: 创建 middleware/auth.py (可选的中间件方式认证)**

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from ..utils.security import verify_token

security = HTTPBearer(auto_error=False)

async def auth_middleware(request: Request, call_next):
    """Optional: Global auth middleware"""
    # Skip for public endpoints
    public_paths = ["/", "/health", "/api/auth/register", "/api/auth/login"]

    if request.url.path in public_paths:
        return await call_next(request)

    # Check authorization
    credentials = await security(request)
    if credentials:
        payload = verify_token(credentials.credentials)
        if payload:
            request.state.user_id = payload["sub"]
        else:
            # For non-public paths without valid auth, return 401
            if not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi"):
                raise HTTPException(status_code=401, detail="未授权")

    return await call_next(request)
```

- [ ] **Step 5: 编写认证路由测试**

Create: `backend/tests/test_auth.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from app.models.user import User
from app.utils.security import hash_password
import uuid

# Create test database
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_duplicate_username(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "another@example.com",
        "password": "password123"
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_user(client):
    # Register and login
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

- [ ] **Step 6: 更新 main.py 注册路由**

Read: `backend/app/main.py`

然后修改：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import BASE_DIR
from .database import engine, Base
from .routers import auth_router, cases_router, documents_router, templates_router, generate_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="要素式起诉状生成系统",
    description="律师专用 - AI 驱动的法律文书生成系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(cases_router)
app.include_router(documents_router)
app.include_router(templates_router)
app.include_router(generate_router)

@app.get("/")
def root():
    return {"message": "要素式起诉状生成系统 API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

- [ ] **Step 7: 运行认证测试**

```bash
cd backend
pytest tests/test_auth.py -v
```
Expected: All tests pass

- [ ] **Step 8: Commit**

```bash
git add backend/app/routers/ backend/app/middleware/ backend/tests/test_auth.py backend/app/main.py
git commit -m "feat: implement authentication routes"
```

---

## Phase 4: 业务 API 路由

由于完整的 API 路由实现代码量较大，以下任务将创建剩余的路由文件。

### Task 12: 案件管理路由

**Files:**
- Create: `backend/app/routers/cases.py`

- [ ] **Step 1: 创建 cases.py**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated, List
import uuid

from ..database import get_db
from ..models.user import User
from ..models.case import Case, CaseStatus
from ..schemas.case import CaseCreate, CaseResponse, CaseUpdate
from ..utils.security import verify_token

router = APIRouter(prefix="/api/cases", tags=["案件管理"])

security = HTTPBearer()

async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")
    return payload["sub"]

@router.get("", response_model=List[CaseResponse])
def get_cases(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有案件"""
    cases = db.query(Case).filter(Case.user_id == current_user_id).order_by(Case.created_at.desc()).all()
    return cases

@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    case_data: CaseCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """创建新案件"""
    case = Case(
        id=str(uuid.uuid4()),
        user_id=current_user_id,
        case_name=case_data.case_name,
        status=CaseStatus.DRAFT
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取案件详情"""
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    return case

@router.put("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: str,
    case_data: CaseUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新案件信息"""
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    if case_data.case_name is not None:
        case.case_name = case_data.case_name
    if case_data.status is not None:
        case.status = case_data.status

    db.commit()
    db.refresh(case)

    return case

@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(
    case_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除案件"""
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    db.delete(case)
    db.commit()

    return None
```

- [ ] **Step 2: 编写案件管理测试**

Create: `backend/tests/test_cases.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
import json

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    # Register and get token
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    return login_response.json()["access_token"]

def test_create_case(client, auth_token):
    response = client.post("/api/cases", json={
        "case_name": "张三诉李四借款纠纷案"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["case_name"] == "张三诉李四借款纠纷案"
    assert "id" in data

def test_get_cases(client, auth_token):
    # Create a case first
    client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.get("/api/cases", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_case(client, auth_token):
    create_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = create_response.json()["id"]

    response = client.get(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json()["id"] == case_id

def test_delete_case(client, auth_token):
    create_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = create_response.json()["id"]

    response = client.delete(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert get_response.status_code == 404
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_cases.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/routers/cases.py backend/tests/test_cases.py
git commit -m "feat: implement case management API"
```

---

### Task 13: 文档管理路由

**Files:**
- Create: `backend/app/routers/documents.py`

- [ ] **Step 1: 创建 documents.py**

```python
import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.case import Case, CaseStatus
from ..models.document import Document, DocumentType
from ..schemas.document import DocumentResponse, DocumentUploadResponse
from ..utils.security import verify_token
from ..utils.file_validator import validate_file_type, validate_file_size
from ..config import FILE_STORAGE_PATH, MAX_FILE_SIZE_MB
from ..services.pdf_parser import PDFParser
from ..services.word_parser import WordParser

router = APIRouter(prefix="/api/cases", tags=["文档管理"])

security = HTTPBearer()

async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")
    return payload["sub"]

@router.post("/{case_id}/documents", response_model=DocumentUploadResponse)
async def upload_document(
    case_id: str,
    file: UploadFile = File(...),
    doc_type: str = "evidence_pdf",
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """上传文档到案件"""
    # Verify case exists and belongs to user
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    # Validate file type
    content = await file.read()
    is_valid, error = validate_file_type(file.filename, content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Validate file size
    is_valid, error = validate_file_size(len(content), MAX_FILE_SIZE_MB)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Determine document type
    if doc_type not in ["evidence_pdf", "organized_word"]:
        raise HTTPException(status_code=400, detail="无效的文档类型")

    # Save file
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    storage_dir = FILE_STORAGE_PATH / "uploads" / case_id
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / unique_filename

    with open(file_path, "wb") as f:
        f.write(content)

    # Create database record
    document = Document(
        id=str(uuid.uuid4()),
        case_id=case_id,
        type=DocumentType(doc_type),
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=len(content)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return DocumentUploadResponse(
        id=document.id,
        case_id=document.case_id,
        type=document.type.value,
        original_filename=document.original_filename,
        file_size=document.file_size,
        uploaded_at=document.uploaded_at
    )

@router.get("/{case_id}/documents", response_model=List[DocumentResponse])
def get_documents(
    case_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取案件的所有文档"""
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    documents = db.query(Document).filter(Document.case_id == case_id).all()
    return documents

@router.get("/{case_id}/documents/{doc_id}", response_model=DocumentResponse)
def get_document(
    case_id: str,
    doc_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取文档详情"""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.case_id == case_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")

    return document

@router.delete("/{case_id}/documents/{doc_id}", status_code=204)
def delete_document(
    case_id: str,
    doc_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除文档"""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.case_id == case_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")

    # Delete file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return None

@router.post("/{case_id}/parse")
def parse_documents(
    case_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """触发案件文档解析和要素提取"""
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    # Get documents
    documents = db.query(Document).filter(Document.case_id == case_id).all()

    evidence_text = ""
    organized_text = ""

    for doc in documents:
        if doc.type == DocumentType.EVIDENCE_PDF and doc.parsed_text is None:
            # Parse PDF
            result = PDFParser.extract_text(doc.file_path)
            if result["success"]:
                doc.parsed_text = result["text"]
                evidence_text = result["text"]

        elif doc.type == DocumentType.ORGANIZED_WORD and doc.parsed_text is None:
            # Parse Word
            result = WordParser.extract_text(doc.file_path)
            if result["success"]:
                doc.parsed_text = result["text"]
                organized_text = result["text"]

    db.commit()

    return {
        "message": "解析完成",
        "evidence_text_length": len(evidence_text),
        "organized_text_length": len(organized_text)
    }
```

- [ ] **Step 2: 编写文档管理测试**

Create: `backend/tests/test_documents.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from docx import Document
import io

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    return login_response.json()["access_token"]

@pytest.fixture
def case_id(client, auth_token):
    response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    return response.json()["id"]

def create_test_docx_content() -> bytes:
    from io import BytesIO
    from docx import Document

    bio = BytesIO()
    doc = Document()
    doc.add_paragraph("原告张三")
    doc.add_paragraph("被告李四")
    doc.save(bio)
    return bio.getvalue()

def test_upload_word_document(client, auth_token, case_id):
    file_content = create_test_docx_content()
    files = {"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}

    response = client.post(
        f"/api/cases/{case_id}/documents",
        files=files,
        data={"doc_type": "organized_word"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_get_documents(client, auth_token, case_id):
    response = client.get(f"/api/cases/{case_id}/documents", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_parse_documents(client, auth_token, case_id):
    # Upload a document first
    file_content = create_test_docx_content()
    files = {"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    client.post(f"/api/cases/{case_id}/documents", files=files, data={"doc_type": "organized_word"}, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post(f"/api/cases/{case_id}/parse", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_documents.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/routers/documents.py backend/tests/test_documents.py
git commit -m "feat: implement document management API"
```

---

### Task 14: 模板管理路由

**Files:**
- Create: `backend/app/routers/templates.py`

- [ ] **Step 1: 创建 templates.py**

```python
import os
import uuid
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..database import get_db
from ..models.user import User
from ..models.template import Template
from ..schemas.template import TemplateResponse, TemplateUploadResponse
from ..utils.security import verify_token
from ..utils.file_validator import validate_file_type, validate_file_size
from ..config import FILE_STORAGE_PATH, MAX_FILE_SIZE_MB
from ..services.word_parser import WordParser

router = APIRouter(prefix="/api/templates", tags=["模板管理"])

security = HTTPBearer()

async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")
    return payload["sub"]

@router.get("", response_model=List[TemplateResponse])
def get_templates(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有模板"""
    templates = db.query(Template).filter(Template.user_id == current_user_id).all()
    return templates

@router.post("", response_model=TemplateUploadResponse)
async def upload_template(
    file: UploadFile = File(...),
    name: str = None,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """上传新模板"""
    # Validate file
    content = await file.read()
    is_valid, error = validate_file_type(file.filename, content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    is_valid, error = validate_file_size(len(content), MAX_FILE_SIZE_MB)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Extract placeholders
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        f.write(content)
        temp_path = f.name

    placeholder_result = WordParser.extract_placeholders(temp_path)
    os.unlink(temp_path)

    if not placeholder_result["success"]:
        raise HTTPException(status_code=400, detail=placeholder_result["error"])

    # Save file
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    storage_dir = FILE_STORAGE_PATH / "templates" / current_user_id
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / unique_filename

    with open(file_path, "wb") as f:
        f.write(content)

    # Check for existing templates with same name (versioning)
    existing = db.query(Template).filter(
        Template.user_id == current_user_id,
        Template.name == (name or file.filename)
    ).order_by(Template.version.desc()).first()

    version = 1
    parent_id = None
    if existing:
        version = existing.version + 1
        parent_id = existing.id
        # Unset default from previous version
        existing.is_default = False

    # Create database record
    template = Template(
        id=str(uuid.uuid4()),
        user_id=current_user_id,
        name=name or file.filename,
        version=version,
        parent_id=parent_id,
        original_filename=file.filename,
        file_path=str(file_path),
        placeholders=json.dumps(placeholder_result["placeholders"]),
        is_default=False
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return TemplateUploadResponse(
        id=template.id,
        name=template.name,
        version=template.version,
        placeholders=placeholder_result["placeholders"],
        message="模板上传成功"
    )

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取模板详情"""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    # Parse placeholders JSON
    if template.placeholders:
        template.placeholders = json.loads(template.placeholders)

    return template

@router.delete("/{template_id}", status_code=204)
def delete_template(
    template_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除模板"""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    # Delete file
    if os.path.exists(template.file_path):
        os.remove(template.file_path)

    db.delete(template)
    db.commit()

    return None

@router.put("/{template_id}/default", response_model=TemplateResponse)
def set_default_template(
    template_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """设为默认模板"""
    # Unset all defaults for this user
    db.query(Template).filter(
        Template.user_id == current_user_id,
        Template.is_default == True
    ).update({"is_default": False})

    # Set new default
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    template.is_default = True
    db.commit()
    db.refresh(template)

    if template.placeholders:
        template.placeholders = json.loads(template.placeholders)

    return template
```

- [ ] **Step 2: 编写模板管理测试**

Create: `backend/tests/test_templates.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from docx import Document
from io import BytesIO

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    return login_response.json()["access_token"]

def create_template_with_placeholders() -> bytes:
    bio = BytesIO()
    doc = Document()
    doc.add_paragraph("原告：{{原告姓名}}")
    doc.add_paragraph("被告：{{被告姓名}}")
    doc.add_paragraph("请求：{{诉讼请求}}")
    doc.save(bio)
    return bio.getvalue()

def test_upload_template(client, auth_token):
    file_content = create_template_with_placeholders()
    files = {"file": ("template.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}

    response = client.post(
        "/api/templates",
        files=files,
        data={"name": "民事起诉状模板"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "原告姓名" in data["placeholders"]

def test_get_templates(client, auth_token):
    response = client.get("/api/templates", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200

def test_set_default_template(client, auth_token):
    # Upload first
    file_content = create_template_with_placeholders()
    files = {"file": ("template.docx", file_content)}
    create_response = client.post("/api/templates", files=files, headers={"Authorization": f"Bearer {auth_token}"})
    template_id = create_response.json()["id"]

    # Set as default
    response = client.put(f"/api/templates/{template_id}/default", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json()["is_default"] is True
```

- [ ] **Step 3: 运行测试**

```bash
cd backend
pytest tests/test_templates.py -v
```
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add backend/app/routers/templates.py backend/tests/test_templates.py
git commit -m "feat: implement template management API"
```

---

### Task 15: 文书生成路由

**Files:**
- Create: `backend/app/routers/generate.py`

- [ ] **Step 1: 创建 generate.py**

```python
import os
import uuid
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db
from ..models.user import User
from ..models.case import Case
from ..models.template import Template
from ..models.element import ExtractedElements, GeneratedDocument
from ..utils.security import verify_token
from ..config import FILE_STORAGE_PATH
from ..services.document_generator import DocumentGenerator

router = APIRouter(prefix="/api/cases", tags=["文书生成"])

security = HTTPBearer()

async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的 token")
    return payload["sub"]

@router.post("/{case_id}/generate")
def generate_document(
    case_id: str,
    template_id: str = None,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """生成起诉状"""
    # Verify case
    case = db.query(Case).filter(Case.id == case_id, Case.user_id == current_user_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")

    # Get elements
    elements = db.query(ExtractedElements).filter(ExtractedElements.case_id == case_id).first()
    if not elements:
        raise HTTPException(status_code=400, detail="请先解析文档并提取要素")

    # Get template
    if template_id:
        template = db.query(Template).filter(
            Template.id == template_id,
            Template.user_id == current_user_id
        ).first()
    else:
        template = db.query(Template).filter(
            Template.user_id == current_user_id,
            Template.is_default == True
        ).first()

    if not template:
        raise HTTPException(status_code=400, detail="未指定模板且无默认模板")

    # Prepare elements dict
    elements_dict = {
        "plaintiff": json.loads(elements.plaintiff) if elements.plaintiff else {},
        "defendant": json.loads(elements.defendant) if elements.defendant else {},
        "claims": json.loads(elements.claims) if elements.claims else [],
        "facts_and_reasons": elements.facts_and_reasons or "",
        "evidence_list": json.loads(elements.evidence_list) if elements.evidence_list else []
    }

    # Generate document
    output_dir = FILE_STORAGE_PATH / "generated" / case_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = f"起诉状-{case.case_name}.docx"
    output_path = output_dir / output_filename

    result = DocumentGenerator.generate_word_document(
        template.file_path,
        elements_dict,
        str(output_path)
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    # Create database record
    generated_doc = GeneratedDocument(
        id=str(uuid.uuid4()),
        case_id=case_id,
        template_id=template.id,
        original_filename=output_filename,
        file_path=str(output_path)
    )

    db.add(generated_doc)

    # Update case status
    case.status = "completed"

    db.commit()
    db.refresh(generated_doc)

    return {
        "id": generated_doc.id,
        "file_path": result["file_path"],
        "file_size": result["file_size"],
        "unmatched_placeholders": result.get("unmatched_placeholders", []),
        "generated_at": generated_doc.generated_at
    }

@router.get("/{case_id}/documents/{doc_id}/download")
def download_document(
    case_id: str,
    doc_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """下载生成的文书"""
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == doc_id,
        GeneratedDocument.case_id == case_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="文书不存在")

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        doc.file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=doc.original_filename or "起诉状.docx"
    )
```

- [ ] **Step 2: 补充要素更新路由到 documents.py**

在 documents.py 中添加：

```python
@router.get("/{case_id}/elements", response_model=ElementResponse)
def get_elements(
    case_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取提取的要素"""
    elements = db.query(ExtractedElements).filter(
        ExtractedElements.case_id == case_id
    ).first()

    if not elements:
        raise HTTPException(status_code=404, detail="要素不存在")

    return elements

@router.put("/{case_id}/elements", response_model=ElementResponse)
def update_elements(
    case_id: str,
    element_data: ElementUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新/确认要素"""
    elements = db.query(ExtractedElements).filter(
        ExtractedElements.case_id == case_id
    ).first()

    if not elements:
        # Create new
        elements = ExtractedElements(
            id=str(uuid.uuid4()),
            case_id=case_id
        )
        db.add(elements)

    # Update fields
    if element_data.plaintiff:
        elements.plaintiff = json.dumps(element_data.plaintiff.model_dump())
    if element_data.defendant:
        elements.defendant = json.dumps(element_data.defendant.model_dump())
    if element_data.claims:
        elements.claims = json.dumps([c.model_dump() for c in element_data.claims])
    if element_data.facts_and_reasons:
        elements.facts_and_reasons = element_data.facts_and_reasons
    if element_data.evidence_list:
        elements.evidence_list = json.dumps([e.model_dump() for e in element_data.evidence_list])
    if element_data.reviewed is not None:
        elements.reviewed = element_data.reviewed

    db.commit()
    db.refresh(elements)

    return elements
```

- [ ] **Step 3: 编写文书生成测试**

Create: `backend/tests/test_generation.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    return login_response.json()["access_token"]

def test_generate_workflow(client, auth_token):
    # Create case
    case_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = case_response.json()["id"]

    # Try to generate without elements (should fail)
    response = client.post(f"/api/cases/{case_id}/generate", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 400
```

- [ ] **Step 4: 运行测试**

```bash
cd backend
pytest tests/test_generation.py -v
```
Expected: Tests pass

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/generate.py backend/tests/test_generation.py
git commit -m "feat: implement document generation API"
```

---

## Phase 5: 前端实现

### Task 16: 前端项目初始化

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "law-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.5",
    "element-plus": "^2.5.0",
    "@element-plus/icons-vue": "^2.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "vite": "^5.0.11"
  }
}
```

- [ ] **Step 2: 创建 vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/vite.svg">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>要素式起诉状生成系统</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 4: 创建 src/main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// Register icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus, { locale: zhCn })

app.mount('#app')
```

- [ ] **Step 5: 创建 src/App.vue**

```vue
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

body {
  margin: 0;
  padding: 0;
}
</style>
```

- [ ] **Step 6: 安装依赖并测试**

```bash
cd frontend
npm install
npm run dev
```
Expected: Vite dev server starts at http://localhost:5173

- [ ] **Step 7: Commit**

```bash
git add frontend/
git commit -m "feat: initialize Vue 3 frontend project"
```

---

### Task 17: 路由与状态管理

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/stores/user.js`
- Create: `frontend/src/api/index.js`

- [ ] **Step 1: 创建 router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    name: 'CaseList',
    component: () => import('@/views/CaseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id',
    name: 'CaseDetail',
    component: () => import('@/views/CaseDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/upload',
    name: 'DocumentUpload',
    component: () => import('@/views/DocumentUpload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/elements',
    name: 'ElementReview',
    component: () => import('@/views/ElementReview.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/templates',
    name: 'TemplateManage',
    component: () => import('@/views/TemplateManage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/preview',
    name: 'DocumentPreview',
    component: () => import('@/views/DocumentPreview.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
```

- [ ] **Step 2: 创建 stores/user.js**

```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(username, password) {
    const response = await api.post('/api/auth/login', { username, password })
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('token', token.value)
    api.setToken(token.value)
  }

  async function register(username, email, password) {
    await api.post('/api/auth/register', { username, email, password })
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // Set token on API if already logged in
  if (token.value) {
    api.setToken(token.value)
  }

  return { user, token, isLoggedIn, login, register, logout }
})
```

- [ ] **Step 3: 创建 api/index.js**

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: ''
})

// Request interceptor
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export function setToken(newToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
}

export default api
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/router/ frontend/src/stores/ frontend/src/api/
git commit -m "feat: setup Vue Router, Pinia store, and API client"
```

---

### Task 18: 登录页面

**Files:**
- Create: `frontend/src/views/Login.vue`

- [ ] **Step 1: 创建 Login.vue**

```vue
<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>要素式起诉状生成系统</h2>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" size="large" style="width: 100%">
            登录
          </el-button>
        </el-form-item>

        <div class="register-link">
          还没有账号？<el-link type="primary" @click="showRegister = true">立即注册</el-link>
        </div>
      </el-form>
    </el-card>

    <!-- Register Dialog -->
    <el-dialog v-model="showRegister" title="注册新账号" width="400px">
      <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
        <el-form-item prop="username" label="用户名">
          <el-input v-model="registerForm.username" />
        </el-form-item>

        <el-form-item prop="email" label="邮箱">
          <el-input v-model="registerForm.email" />
        </el-form-item>

        <el-form-item prop="password" label="密码">
          <el-input v-model="registerForm.password" type="password" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showRegister = false">取消</el-button>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const registerFormRef = ref(null)
const loading = ref(false)
const showRegister = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const registerForm = reactive({
  username: '',
  email: '',
  password: ''
})

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3-50 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少 8 位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!await formRef.value.validate()) return

  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!await registerFormRef.value.validate()) return

  try {
    await userStore.register(registerForm.username, registerForm.email, registerForm.password)
    ElMessage.success('注册成功，请登录')
    showRegister.value = false
    form.username = registerForm.username
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '注册失败')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
}

.login-card h2 {
  text-align: center;
  margin: 0;
  color: #303133;
}

.register-link {
  text-align: center;
  margin-top: 10px;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/Login.vue
git commit -m "feat: implement login page"
```

---

### Task 19: 案件列表页面

**Files:**
- Create: `frontend/src/views/CaseList.vue`

- [ ] **Step 1: 创建 CaseList.vue**

```vue
<template>
  <div class="case-list-container">
    <el-header class="page-header">
      <h2>案件列表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showNewCaseDialog = true">
          <el-icon><Plus /></el-icon>
          新建案件
        </el-button>
        <el-button @click="$router.push('/templates')">模板管理</el-button>
        <el-button @click="handleLogout">退出</el-button>
      </div>
    </el-header>

    <el-main>
      <el-table :data="cases" v-loading="loading" stripe>
        <el-table-column prop="case_name" label="案件名称" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/case/${row.id}`)">查看</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <!-- New Case Dialog -->
    <el-dialog v-model="showNewCaseDialog" title="新建案件" width="400px">
      <el-input v-model="newCaseName" placeholder="请输入案件名称" />
      <template #footer>
        <el-button @click="showNewCaseDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreateCase">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const cases = ref([])
const loading = ref(false)
const showNewCaseDialog = ref(false)
const newCaseName = ref('')

const fetchCases = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/cases')
    cases.value = response.data
  } catch (error) {
    ElMessage.error('加载案件列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreateCase = async () => {
  if (!newCaseName.value.trim()) {
    ElMessage.warning('请输入案件名称')
    return
  }

  try {
    const response = await api.post('/api/cases', { case_name: newCaseName.value })
    ElMessage.success('创建成功')
    showNewCaseDialog.value = false
    newCaseName.value = ''
    router.push(`/case/${response.data.id}`)
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除案件"${row.case_name}"吗？`, '确认删除', { type: 'warning' })
    await api.delete(`/api/cases/${row.id}`)
    ElMessage.success('删除成功')
    fetchCases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const getStatusType = (status) => {
  const map = { draft: '', processing: 'warning', completed: 'success' }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = { draft: '草稿', processing: '处理中', completed: '已完成' }
  return map[status] || status
}

const formatDate = (date) => new Date(date).toLocaleString('zh-CN')

onMounted(fetchCases)
</script>

<style scoped>
.case-list-container {
  height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
}

.page-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/CaseList.vue
git commit -m "feat: implement case list page"
```

---

### Task 20: 案件详情与文档上传页面

**Files:**
- Create: `frontend/src/views/CaseDetail.vue`
- Create: `frontend/src/views/DocumentUpload.vue`

- [ ] **Step 1: 创建 CaseDetail.vue**

```vue
<template>
  <div class="case-detail-container">
    <el-header class="page-header">
      <div class="breadcrumb">
        <el-link @click="$router.push('/')">案件列表</el-link>
        <span> / </span>
        <span>{{ caseDetail?.case_name }}</span>
      </div>
    </el-header>

    <el-main v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>已上传文档</span>
                <el-button type="primary" size="small" @click="$router.push(`/case/${caseId}/upload`)">上传</el-button>
              </div>
            </template>
            <el-empty v-if="documents.length === 0" description="暂无文档" />
            <el-table v-else :data="documents">
              <el-table-column prop="original_filename" label="文件名" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="{ row }">
                  {{ row.type === 'evidence_pdf' ? '证据 PDF' : '整理 Word' }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="80">
                <template #default="{ row }">
                  <el-button size="small" type="danger" @click="handleDeleteDoc(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>
              <span>已生成文书</span>
            </template>
            <el-empty v-if="generatedDocs.length === 0" description="暂无生成文书" />
            <el-table v-else :data="generatedDocs">
              <el-table-column prop="original_filename" label="文件名" />
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button size="small" @click="handleDownload(row)">下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>

      <el-card style="margin-top: 20px">
        <template #header>
          <span>操作</span>
        </template>
        <el-button type="primary" @click="handleParse">解析文档</el-button>
        <el-button type="success" @click="$router.push(`/case/${caseId}/elements`)">审核要素</el-button>
        <el-button type="warning" @click="handleGenerate">生成起诉状</el-button>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const caseId = route.params.id

const caseDetail = ref(null)
const documents = ref([])
const generatedDocs = ref([])
const loading = ref(false)

const fetchDetail = async () => {
  loading.value = true
  try {
    const [caseRes, docRes] = await Promise.all([
      api.get(`/api/cases/${caseId}`),
      api.get(`/api/cases/${caseId}/documents`)
    ])
    caseDetail.value = caseRes.data
    documents.value = docRes.data
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleParse = async () => {
  try {
    await api.post(`/api/cases/${caseId}/parse`)
    ElMessage.success('解析完成')
    fetchDetail()
  } catch (error) {
    ElMessage.error('解析失败')
  }
}

const handleGenerate = async () => {
  try {
    const response = await api.post(`/api/cases/${caseId}/generate`)
    ElMessage.success('生成成功')
    generatedDocs.value.push(response.data)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '生成失败')
  }
}

const handleDeleteDoc = async (row) => {
  await api.delete(`/api/cases/${caseId}/documents/${row.id}`)
  ElMessage.success('删除成功')
  fetchDetail()
}

const handleDownload = (row) => {
  window.open(`/api/cases/${caseId}/documents/${row.id}/download`, '_blank')
}

onMounted(fetchDetail)
</script>
```

- [ ] **Step 2: 创建 DocumentUpload.vue**

```vue
<template>
  <div class="upload-container">
    <el-header class="page-header">
      <el-link @click="$router.push(`/case/${caseId}`)">返回案件详情</el-link>
    </el-header>

    <el-main>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>上传证据 PDF</template>
            <el-upload
              drag
              :auto-upload="false"
              :on-change="(file) => handleFileSelect(file, 'evidence_pdf')"
              accept=".pdf"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">拖拽文件到此处或<em>点击上传</em></div>
            </el-upload>
            <el-button
              type="primary"
              :disabled="!selectedFiles.evidence_pdf"
              :loading="uploading"
              @click="handleUpload('evidence_pdf')"
              style="margin-top: 10px; width: 100%"
            >
              上传 PDF
            </el-button>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>上传整理 Word</template>
            <el-upload
              drag
              :auto-upload="false"
              :on-change="(file) => handleFileSelect(file, 'organized_word')"
              accept=".doc,.docx"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">拖拽文件到此处或<em>点击上传</em></div>
            </el-upload>
            <el-button
              type="primary"
              :disabled="!selectedFiles.organized_word"
              :loading="uploading"
              @click="handleUpload('organized_word')"
              style="margin-top: 10px; width: 100%"
            >
              上传 Word
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const caseId = route.params.id

const selectedFiles = ref({})
const uploading = ref(false)

const handleFileSelect = (file, type) => {
  selectedFiles.value[type] = file.raw
}

const handleUpload = async (type) => {
  const file = selectedFiles.value[type]
  if (!file) return

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  formData.append('doc_type', type)

  try {
    await api.post(`/api/cases/${caseId}/documents`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    ElMessage.success('上传成功')
    router.push(`/case/${caseId}`)
  } catch (error) {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/CaseDetail.vue frontend/src/views/DocumentUpload.vue
git commit -m "feat: implement case detail and document upload pages"
```

---

### Task 21: 要素审核与模板管理页面

**Files:**
- Create: `frontend/src/views/ElementReview.vue`
- Create: `frontend/src/views/TemplateManage.vue`

- [ ] **Step 1: 创建 ElementReview.vue**

```vue
<template>
  <div class="element-review-container">
    <el-header class="page-header">
      <el-link @click="$router.push(`/case/${caseId}`)">返回案件详情</el-link>
      <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
    </el-header>

    <el-main v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>原告信息</template>
            <el-form label-width="100px">
              <el-form-item label="姓名">
                <el-input v-model="elements.plaintiff.name" />
              </el-form-item>
              <el-form-item label="身份证号">
                <el-input v-model="elements.plaintiff.id_number" />
              </el-form-item>
              <el-form-item label="地址">
                <el-input v-model="elements.plaintiff.address" type="textarea" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="elements.plaintiff.phone" />
              </el-form-item>
            </el-form>
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>被告信息</template>
            <el-form label-width="100px">
              <el-form-item label="姓名">
                <el-input v-model="elements.defendant.name" />
              </el-form-item>
              <el-form-item label="身份证号">
                <el-input v-model="elements.defendant.id_number" />
              </el-form-item>
              <el-form-item label="地址">
                <el-input v-model="elements.defendant.address" type="textarea" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="elements.defendant.phone" />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>诉讼请求</template>
            <div v-for="(claim, index) in elements.claims" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px">
              <el-input v-model="claim.content" placeholder="请求内容" />
              <el-button type="danger" @click="elements.claims.splice(index, 1)">删除</el-button>
            </div>
            <el-button @click="elements.claims.push({ order: elements.claims.length + 1, content: '' })">添加请求</el-button>
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>事实与理由</template>
            <el-input v-model="elements.facts_and_reasons" type="textarea" :rows="10" />
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>证据清单</template>
            <div v-for="(evidence, index) in elements.evidence_list" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px">
              <el-input v-model="evidence.name" placeholder="证据名称" style="width: 100px" />
              <el-input v-model="evidence.purpose" placeholder="证明目的" />
              <el-button type="danger" @click="elements.evidence_list.splice(index, 1)">删除</el-button>
            </div>
            <el-button @click="elements.evidence_list.push({ name: '', purpose: '', page: null })">添加证据</el-button>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const caseId = route.params.id

const loading = ref(false)
const saving = ref(false)

const elements = reactive({
  plaintiff: { name: '', id_number: '', address: '', phone: '' },
  defendant: { name: '', id_number: '', address: '', phone: '' },
  claims: [],
  facts_and_reasons: '',
  evidence_list: []
})

const fetchElements = async () => {
  loading.value = true
  try {
    const response = await api.get(`/api/cases/${caseId}/elements`)
    const data = response.data
    if (data.plaintiff) Object.assign(elements.plaintiff, data.plaintiff)
    if (data.defendant) Object.assign(elements.defendant, data.defendant)
    if (data.claims) elements.claims = data.claims
    if (data.facts_and_reasons) elements.facts_and_reasons = data.facts_and_reasons
    if (data.evidence_list) elements.evidence_list = data.evidence_list
  } catch (error) {
    if (error.response?.status !== 404) {
      ElMessage.error('加载失败')
    }
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    await api.put(`/api/cases/${caseId}/elements`, {
      ...elements,
      reviewed: true
    })
    ElMessage.success('保存成功')
    router.push(`/case/${caseId}`)
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(fetchElements)
</script>
```

- [ ] **Step 2: 创建 TemplateManage.vue**

```vue
<template>
  <div class="template-manage-container">
    <el-header class="page-header">
      <el-link @click="$router.push('/')">返回案件列表</el-link>
      <el-button type="primary" @click="uploadDialogVisible = true">上传模板</el-button>
    </el-header>

    <el-main>
      <el-table :data="templates" v-loading="loading">
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="is_default" label="默认" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success">是</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="uploaded_at" label="上传时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.uploaded_at).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleSetDefault(row)" :disabled="row.is_default">设为默认</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-dialog v-model="uploadDialogVisible" title="上传模板" width="400px">
      <el-input v-model="templateName" placeholder="模板名称（可选）" style="margin-bottom: 10px" />
      <el-upload
        drag
        :auto-upload="false"
        :on-change="(file) => selectedFile = file.raw"
        accept=".doc,.docx"
      >
        <div class="el-upload__text">选择 Word 模板文件</div>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpload">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const templates = ref([])
const loading = ref(false)
const uploadDialogVisible = ref(false)
const templateName = ref('')
const selectedFile = ref(null)

const fetchTemplates = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/templates')
    templates.value = response.data
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  if (templateName.value) formData.append('name', templateName.value)

  try {
    await api.post('/api/templates', formData)
    ElMessage.success('上传成功')
    uploadDialogVisible.value = false
    fetchTemplates()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '上传失败')
  }
}

const handleSetDefault = async (row) => {
  try {
    await api.put(`/api/templates/${row.id}/default`)
    ElMessage.success('设置成功')
    fetchTemplates()
  } catch (error) {
    ElMessage.error('设置失败')
  }
}

const handleDelete = async (row) => {
  await api.delete(`/api/templates/${row.id}`)
  ElMessage.success('删除成功')
  fetchTemplates()
}

onMounted(fetchTemplates)
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/ElementReview.vue frontend/src/views/TemplateManage.vue
git commit -m "feat: implement element review and template management pages"
```

---

## Phase 6: 测试与部署

### Task 22: 运行完整测试套件

- [ ] **Step 1: 运行所有后端测试**

```bash
cd backend
pytest tests/ -v --cov=app
```
Expected: All tests pass, coverage > 70%

- [ ] **Step 2: 修复任何失败的测试**

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "test: all tests passing"
```

---

### Task 23: 创建 README 文档

**Files:**
- Create: `README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# 要素式起诉状生成系统

AI 驱动的法律文书生成系统，帮助律师快速生成符合国家标准的要素式起诉状。

## 功能特性

- 支持 PDF 证据文件和 Word 整理文档上传
- 自动解析文档并提取文本
- OCR 识别扫描件 PDF
- AI 自动提取案件要素（当事人信息、诉讼请求、事实理由、证据清单）
- 模板化管理起诉状格式
- 一键生成符合国标的起诉状

## 快速开始

### 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑.env 配置 ANTHROPIC_API_KEY 等
uvicorn app.main:app --reload
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 配置说明

编辑`backend/.env`:

```bash
# JWT 配置
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRE_HOURS=24

# 文件存储
FILE_STORAGE_PATH=./docs/storage
MAX_FILE_SIZE_MB=50

# AI 配置
ANTHROPIC_API_KEY=sk-...
AI_MODEL=claude-sonnet-4-20250514

# OCR 配置
OCR_ENABLED=true
OCR_LANGUAGE=ch
```

## API 文档

启动后端后访问 http://localhost:8000/docs

## 测试

```bash
cd backend
pytest tests/ -v
```

## 技术栈

- 后端：FastAPI, SQLAlchemy, JWT
- 前端：Vue 3, Element Plus, Pinia
- 数据库：SQLite / PostgreSQL
- 文档处理：pdfplumber, PyMuPDF, python-docx, PaddleOCR
- AI: Anthropic Claude API
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README documentation"
```

---

## 验收标准

完成以上所有任务后，系统应满足：

1. 用户可以注册登录
2. 可以创建、查看、删除案件
3. 可以上传 PDF 和 Word 文档到案件
4. 可以解析文档并提取文本
5. 可以通过 AI 提取案件要素
6. 可以审核和编辑提取的要素
7. 可以上传和管理 Word 模板
8. 可以使用模板和要素生成起诉状
9. 可以下载生成的文书
10. 所有 API 有单元测试覆盖

---

## 执行选择

计划已完成并保存到 `docs/superpowers/plans/2026-03-23-elemental-complaint-generator.md`。

**两个执行选项：**

**1. Subagent-Driven (推荐)** - 每个任务 dispatch 一个独立的 subagent 执行，任务之间有 review 检查点，迭代快速

**2. Inline Execution** - 在当前会话中使用 executing-plans skill 批量执行，适合快速完成

**选择哪种方式？**
