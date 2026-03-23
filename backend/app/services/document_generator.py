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
