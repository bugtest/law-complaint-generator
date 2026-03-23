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
