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
