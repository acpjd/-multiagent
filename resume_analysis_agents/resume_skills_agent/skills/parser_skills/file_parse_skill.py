"""
文件解析Skill - 解析PDF/Word/TXT简历文件
"""

import os
from typing import Any, Dict

from ..base_skill import BaseSkill


class FileParseSkill(BaseSkill):
    """
    文件解析Skill
    
    支持格式: PDF, DOCX, TXT
    """
    
    name = "file_parse"
    description = "解析简历文件（PDF/Word/TXT），提取文本内容"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
        self.supported_formats = {".pdf", ".docx", ".txt"}
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        file_path = kwargs.get("file_path")
        if not file_path:
            return False
        if not os.path.exists(file_path):
            return False
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_formats
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行文件解析
        
        Args:
            file_path: 文件路径
            
        Returns:
            解析结果 {"text": str, "format": str, "success": bool}
        """
        file_path = kwargs.get("file_path", "")
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == ".pdf":
                text = self._parse_pdf(file_path)
            elif ext == ".docx":
                text = self._parse_docx(file_path)
            elif ext == ".txt":
                text = self._parse_txt(file_path)
            else:
                return {"success": False, "error": f"不支持的文件格式: {ext}"}
            
            return {
                "success": True,
                "text": text,
                "format": ext[1:],
                "file_name": os.path.basename(file_path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_pdf(self, file_path: str) -> str:
        """解析PDF文件"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except ImportError:
            return "错误: 请安装PyPDF2库 (pip install PyPDF2)"
    
    def _parse_docx(self, file_path: str) -> str:
        """解析Word文件"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except ImportError:
            return "错误: 请安装python-docx库 (pip install python-docx)"
    
    def _parse_txt(self, file_path: str) -> str:
        """解析TXT文件"""
        encodings = ["utf-8", "gbk", "gb2312", "latin-1"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"无法解析文件编码，尝试的编码: {encodings}")