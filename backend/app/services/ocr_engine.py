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
            try:
                from paddleocr import PaddleOCR
                self._ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang=self.language,
                    show_log=False
                )
            except ImportError:
                pass

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

            if self._ocr is None:
                return {
                    "success": False,
                    "text": "",
                    "confidence": 0,
                    "pages": 0,
                    "error": "PaddleOCR 未安装，请运行：pip install paddlepaddle paddleocr"
                }

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
