"""
文本提取Skill - 从简历文本中提取结构化信息
"""

import re
from typing import Any, Dict, List, Optional

from ..base_skill import BaseSkill


class TextExtractionSkill(BaseSkill):
    """
    文本提取Skill
    
    从简历文本中提取结构化信息（姓名、联系方式、教育背景、工作经历等）
    """
    
    name = "text_extraction"
    description = "从简历文本中提取结构化信息"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
        # 常见中文姓名模式
        self.name_pattern = re.compile(r"姓名[:：]?\s*([\u4e00-\u9fa5·]{2,4})")
        # 手机号
        self.phone_pattern = re.compile(r"(?:电话|手机|联系方式)[:：]?\s*(1[3-9]\d{9})")
        # 邮箱
        self.email_pattern = re.compile(r"(?:邮箱|Email|E-mail)[:：]?\s*([\w.-]+@[\w.-]+\.\w+)")
        # 教育背景关键词
        self.edu_keywords = ["学士", "硕士", "博士", "本科", "大专", "研究生", "大学", "学院", "学校"]
        # 常见教育相关学校
        self.edu_section_pattern = re.compile(r"(教育背景|教育经历|学习经历)")
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        text = kwargs.get("text")
        return bool(text) and isinstance(text, str)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行文本提取
        
        Args:
            text: 简历文本
            
        Returns:
            结构化信息字典
        """
        text = kwargs.get("text", "")
        
        result = {
            "name": self._extract_name(text),
            "phone": self._extract_phone(text),
            "email": self._extract_email(text),
            "education": self._extract_education(text),
            "work_experience": self._extract_work_experience(text),
            "skills": self._extract_skills(text),
            "raw_text": text,
        }
        
        return result
    
    def _extract_name(self, text: str) -> Optional[str]:
        """提取姓名"""
        match = self.name_pattern.search(text)
        if match:
            return match.group(1)
        # 尝试从第一行获取可能的姓名
        first_line = text.strip().split("\n")[0].strip()
        if len(first_line) <= 4 and all("\u4e00" <= c <= "\u9fa5" for c in first_line):
            return first_line
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """提取手机号"""
        match = self.phone_pattern.search(text)
        if match:
            return match.group(1)
        # 直接匹配手机号
        phone_match = re.search(r"(1[3-9]\d{9})", text)
        return phone_match.group(1) if phone_match else None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """提取邮箱"""
        match = self.email_pattern.search(text)
        if match:
            return match.group(1)
        # 直接匹配邮箱
        email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", text)
        return email_match.group(0) if email_match else None
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """提取教育背景"""
        education_list = []
        lines = text.split("\n")
        in_education_section = False
        
        for line in lines:
            line = line.strip()
            if self.edu_section_pattern.search(line):
                in_education_section = True
                continue
            
            if in_education_section:
                # 检查是否到达下一个部分
                if any(keyword in line for keyword in ["工作经历", "项目经验", "技能", "自我评价"]):
                    in_education_section = False
                    continue
                
                # 检查是否包含教育关键词
                if any(keyword in line for keyword in self.edu_keywords):
                    education_list.append({"raw": line})
        
        return education_list
    
    def _extract_work_experience(self, text: str) -> List[Dict[str, str]]:
        """提取工作经历"""
        work_list = []
        lines = text.split("\n")
        in_work_section = False
        
        for line in lines:
            line = line.strip()
            if re.search(r"(工作经历|工作经验|实习经历|工作)", line):
                in_work_section = True
                continue
            
            if in_work_section:
                if any(keyword in line for keyword in ["教育背景", "项目经验", "技能", "自我评价"]):
                    in_work_section = False
                    continue
                
                if line:
                    work_list.append({"raw": line})
        
        return work_list
    
    def _extract_skills(self, text: str) -> List[str]:
        """初步提取技能关键词"""
        # 常见技术技能关键词
        skill_keywords = [
            "Python", "Java", "C++", "JavaScript", "Go", "Rust",
            "Vue", "React", "Angular", "Spring", "Django", "Flask",
            "MySQL", "Redis", "MongoDB", "PostgreSQL",
            "Docker", "Kubernetes", "AWS", "阿里云",
            "TensorFlow", "PyTorch", "机器学习", "深度学习", "NLP",
            "Git", "Linux", "Jira",
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        
        return found_skills