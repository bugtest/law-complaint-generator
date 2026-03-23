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
