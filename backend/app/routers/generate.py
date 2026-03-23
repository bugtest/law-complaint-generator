import os
import uuid
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..database import get_db
from ..models.user import User
from ..models.case import Case
from ..models.template import Template
from ..models.element import ExtractedElements, GeneratedDocument
from ..schemas.element import ElementResponse, ElementUpdate
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
