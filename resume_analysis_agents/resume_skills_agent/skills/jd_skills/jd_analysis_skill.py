"""
JD分析Skill - 分析岗位描述，提取关键要求
"""

import re
from typing import Any, Dict, List, Optional

from ..base_skill import BaseSkill


class JDAnalysisSkill(BaseSkill):
    """
    JD分析Skill
    
    从岗位描述中提取关键要求（技能要求、经验要求、学历要求等）
    """
    
    name = "jd_analysis"
    description = "分析岗位描述(JD)，提取关键要求"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
        # 常见技能关键词
        self.skill_keywords = [
            "Python", "Java", "C++", "JavaScript", "Go", "Rust",
            "Vue", "React", "Angular", "Spring", "Django", "Flask",
            "MySQL", "Redis", "MongoDB", "PostgreSQL",
            "Docker", "Kubernetes", "AWS", "阿里云",
            "TensorFlow", "PyTorch", "机器学习", "深度学习", "NLP",
            "Git", "Linux", "Jira",
        ]
        # 学历要求关键词
        self.edu_keywords = ["本科", "硕士", "博士", "大专", "学士", "研究生"]
        # 经验要求关键词
        self.exp_keywords = [r"\d+年", "经验", "实习", "应届"]
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        jd_text = kwargs.get("jd_text")
        return bool(jd_text) and isinstance(jd_text, str)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行JD分析
        
        Args:
            jd_text: 岗位描述文本
            
        Returns:
            分析结果字典
        """
        jd_text = kwargs.get("jd_text", "")
        
        result = {
            "required_skills": self._extract_required_skills(jd_text),
            "education_requirement": self._extract_education_requirement(jd_text),
            "experience_requirement": self._extract_experience_requirement(jd_text),
            "job_title": self._extract_job_title(jd_text),
            "responsibilities": self._extract_responsibilities(jd_text),
            "raw_text": jd_text,
        }
        
        return result
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """提取要求的技能"""
        found_skills = []
        for skill in self.skill_keywords:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        return found_skills
    
    def _extract_education_requirement(self, text: str) -> Optional[str]:
        """提取学历要求"""
        for keyword in self.edu_keywords:
            if keyword in text:
                return keyword
        return None
    
    def _extract_experience_requirement(self, text: str) -> Optional[str]:
        """提取经验要求"""
        for pattern in self.exp_keywords:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    def _extract_job_title(self, text: str) -> Optional[str]:
        """提取岗位名称"""
        match = re.search(r"(?:岗位|职位|职位)[:：]?\s*([^\n]+)", text)
        if match:
            return match.group(1).strip()
        # 尝试从第一行获取
        first_line = text.strip().split("\n")[0].strip()
        if len(first_line) <= 20:
            return first_line
        return None
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """提取岗位职责"""
        responsibilities = []
        lines = text.split("\n")
        in_resp_section = False
        
        for line in lines:
            line = line.strip()
            if re.search(r"(岗位职责|工作职责|工作内容|职位描述)", line):
                in_resp_section = True
                continue
            
            if in_resp_section:
                if any(keyword in line for keyword in ["任职要求", "岗位要求", "要求", "技能"]):
                    in_resp_section = False
                    continue
                
                if line and (line.startswith("-") or line.startswith("•") or line.startswith("1") or line.startswith("2") or line.startswith("3")):
                    responsibilities.append(line.strip("-• "))
        
        return responsibilities