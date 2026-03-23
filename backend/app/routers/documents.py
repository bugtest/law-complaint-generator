import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated, List

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
