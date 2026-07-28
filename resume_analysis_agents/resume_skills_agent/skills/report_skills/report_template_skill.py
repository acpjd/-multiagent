"""
报告模板Skill - 生成结构化分析报告
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from ..base_skill import BaseSkill


class ReportTemplateSkill(BaseSkill):
    """
    报告模板Skill
    
    生成结构化的简历分析报告
    """
    
    name = "report_template"
    description = "生成结构化分析报告"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        resume_data = kwargs.get("resume_data")
        match_result = kwargs.get("match_result")
        suggestions = kwargs.get("suggestions")
        return bool(resume_data) and bool(match_result)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行报告生成
        
        Args:
            resume_data: 简历数据字典
            jd_data: JD数据字典
            match_result: 匹配结果字典
            suggestions: 优化建议列表
            
        Returns:
            完整报告字典
        """
        resume_data = kwargs.get("resume_data", {})
        jd_data = kwargs.get("jd_data", {})
        match_result = kwargs.get("match_result", {})
        suggestions = kwargs.get("suggestions", [])
        
        report = {
            "report_id": self._generate_report_id(),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "candidate_info": self._build_candidate_info(resume_data),
            "job_info": self._build_job_info(jd_data),
            "match_summary": self._build_match_summary(match_result),
            "skills_analysis": self._build_skills_analysis(resume_data, match_result),
            "optimization_suggestions": suggestions,
            "overall_assessment": self._build_overall_assessment(match_result, suggestions),
        }
        
        return report
    
    def _generate_report_id(self) -> str:
        """生成报告ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"RPT-{timestamp}"
    
    def _build_candidate_info(self, resume_data: Dict) -> Dict[str, str]:
        """构建候选人信息"""
        return {
            "name": resume_data.get("name", "未知"),
            "phone": resume_data.get("phone", "未提供"),
            "email": resume_data.get("email", "未提供"),
        }
    
    def _build_job_info(self, jd_data: Dict) -> Dict[str, str]:
        """构建岗位信息"""
        return {
            "job_title": jd_data.get("job_title", "未知岗位"),
            "required_skills": ", ".join(jd_data.get("required_skills", [])),
            "education_requirement": jd_data.get("education_requirement", "未指定"),
            "experience_requirement": jd_data.get("experience_requirement", "未指定"),
        }
    
    def _build_match_summary(self, match_result: Dict) -> Dict[str, Any]:
        """构建匹配摘要"""
        return {
            "total_score": match_result.get("total_score", 0),
            "match_level": match_result.get("match_level", "未知"),
            "skills_score": match_result.get("skills_score", 0),
            "experience_score": match_result.get("experience_score", 0),
            "education_score": match_result.get("education_score", 0),
        }
    
    def _build_skills_analysis(self, resume_data: Dict, match_result: Dict) -> Dict[str, List[str]]:
        """构建技能分析"""
        return {
            "candidate_skills": resume_data.get("skills", []),
            "matched_skills": match_result.get("matched_skills", []),
            "missing_skills": match_result.get("missing_skills", []),
        }
    
    def _build_overall_assessment(self, match_result: Dict, suggestions: List) -> str:
        """构建总体评估"""
        score = match_result.get("total_score", 0)
        level = match_result.get("match_level", "未知")
        high_priority = sum(1 for s in suggestions if s.get("priority") == "high")
        
        assessment = f"总体匹配度: {score}分 ({level})。\n"
        if high_priority > 0:
            assessment += f"有{high_priority}项高优先级优化建议，建议优先处理。\n"
        if score >= 80:
            assessment += "候选人技能与岗位要求高度匹配，建议进入下一轮面试。"
        elif score >= 60:
            assessment += "候选人技能与岗位要求较为匹配，建议进一步评估。"
        else:
            assessment += "候选人技能与岗位要求存在一定差距，建议谨慎考虑。"
        
        return assessment