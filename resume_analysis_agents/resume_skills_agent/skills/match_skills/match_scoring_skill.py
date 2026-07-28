"""
匹配评分Skill - 计算简历与JD的匹配度
"""

from typing import Any, Dict, List, Optional

from ..base_skill import BaseSkill


class MatchScoringSkill(BaseSkill):
    """
    匹配评分Skill
    
    计算候选人简历与岗位描述(JD)的匹配度
    """
    
    name = "match_scoring"
    description = "计算简历与JD的匹配度分数"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
        # 权重配置
        self.weights = {
            "skills_match": 0.4,      # 技能匹配权重
            "experience_match": 0.3,  # 经验匹配权重
            "education_match": 0.2,   # 学历匹配权重
            "other_match": 0.1,       # 其他匹配权重
        }
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        resume_data = kwargs.get("resume_data")
        jd_data = kwargs.get("jd_data")
        return bool(resume_data) and bool(jd_data)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行匹配评分
        
        Args:
            resume_data: 简历数据字典
            jd_data: JD数据字典
            
        Returns:
            匹配结果字典
        """
        resume_data = kwargs.get("resume_data", {})
        jd_data = kwargs.get("jd_data", {})
        
        # 计算各维度匹配度
        skills_score = self._calculate_skills_match(
            resume_data.get("skills", []),
            jd_data.get("required_skills", [])
        )
        
        experience_score = self._calculate_experience_match(
            resume_data.get("work_experience", []),
            jd_data.get("experience_requirement", "")
        )
        
        education_score = self._calculate_education_match(
            resume_data.get("education", []),
            jd_data.get("education_requirement", "")
        )
        
        # 计算总分
        total_score = (
            skills_score * self.weights["skills_match"] +
            experience_score * self.weights["experience_match"] +
            education_score * self.weights["education_match"] +
            50 * self.weights["other_match"]  # 默认其他匹配50分
        )
        
        # 匹配的技能
        matched_skills = self._get_matched_skills(
            resume_data.get("skills", []),
            jd_data.get("required_skills", [])
        )
        
        # 缺失的技能
        missing_skills = self._get_missing_skills(
            resume_data.get("skills", []),
            jd_data.get("required_skills", [])
        )
        
        return {
            "total_score": round(total_score, 1),
            "skills_score": round(skills_score, 1),
            "experience_score": round(experience_score, 1),
            "education_score": round(education_score, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_level": self._get_match_level(total_score),
        }
    
    def _calculate_skills_match(self, resume_skills: List[str], jd_skills: List[str]) -> float:
        """计算技能匹配度"""
        if not jd_skills:
            return 50.0
        
        matched = set(s.lower() for s in resume_skills) & set(s.lower() for s in jd_skills)
        return (len(matched) / len(jd_skills)) * 100
    
    def _calculate_experience_match(self, work_exp: List, exp_requirement: str) -> float:
        """计算经验匹配度"""
        if not exp_requirement:
            return 50.0
        
        # 简单判断：如果有工作经历就给基础分
        if work_exp:
            return 80.0
        return 30.0
    
    def _calculate_education_match(self, education: List, edu_requirement: str) -> float:
        """计算学历匹配度"""
        if not edu_requirement:
            return 50.0
        
        edu_levels = {"大专": 1, "本科": 2, "硕士": 3, "博士": 4}
        required_level = edu_levels.get(edu_requirement, 0)
        
        for edu in education:
            edu_raw = edu.get("raw", "")
            for level_str, level_val in edu_levels.items():
                if level_str in edu_raw and level_val >= required_level:
                    return 100.0
        
        return 40.0
    
    def _get_matched_skills(self, resume_skills: List[str], jd_skills: List[str]) -> List[str]:
        """获取匹配的技能"""
        resume_lower = {s.lower(): s for s in resume_skills}
        jd_lower = {s.lower(): s for s in jd_skills}
        matched_keys = set(resume_lower.keys()) & set(jd_lower.keys())
        return [resume_lower[k] for k in matched_keys]
    
    def _get_missing_skills(self, resume_skills: List[str], jd_skills: List[str]) -> List[str]:
        """获取缺失的技能"""
        resume_lower = {s.lower(): s for s in resume_skills}
        jd_lower = {s.lower(): s for s in jd_skills}
        missing_keys = set(jd_lower.keys()) - set(resume_lower.keys())
        return [jd_lower[k] for k in missing_keys]
    
    def _get_match_level(self, score: float) -> str:
        """获取匹配等级"""
        if score >= 80:
            return "非常匹配"
        elif score >= 60:
            return "较为匹配"
        elif score >= 40:
            return "一般匹配"
        else:
            return "不太匹配"