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
