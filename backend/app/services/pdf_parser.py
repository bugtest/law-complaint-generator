from pathlib import Path
from typing import Dict, Any, Optional
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
