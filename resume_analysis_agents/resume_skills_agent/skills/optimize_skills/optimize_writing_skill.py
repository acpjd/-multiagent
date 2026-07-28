"""
优化写作Skill - 生成简历优化建议
"""

from typing import Any, Dict, List, Optional

from ..base_skill import BaseSkill


class OptimizeWritingSkill(BaseSkill):
    """
    优化写作Skill
    
    根据简历和JD的对比，生成简历优化建议
    """
    
    name = "optimize_writing"
    description = "生成简历优化建议和改写"
    version = "0.1.0"
    
    def __init__(self):
        super().__init__()
    
    def validate_input(self, **kwargs) -> bool:
        """验证输入参数"""
        resume_data = kwargs.get("resume_data")
        match_result = kwargs.get("match_result")
        return bool(resume_data) and bool(match_result)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行优化建议生成
        
        Args:
            resume_data: 简历数据字典
            match_result: 匹配结果字典
            jd_data: JD数据字典（可选）
            
        Returns:
            优化建议列表
        """
        resume_data = kwargs.get("resume_data", {})
        match_result = kwargs.get("match_result", {})
        jd_data = kwargs.get("jd_data", {})
        
        suggestions = []
        
        # 技能优化建议
        missing_skills = match_result.get("missing_skills", [])
        if missing_skills:
            suggestions.append({
                "type": "skills",
                "title": "技能补充建议",
                "content": f"建议在简历中补充以下技能: {', '.join(missing_skills)}",
                "priority": "high",
            })
        
        # 工作经历优化建议
        work_exp = resume_data.get("work_experience", [])
        if not work_exp:
            suggestions.append({
                "type": "experience",
                "title": "工作经历补充",
                "content": "建议添加详细的工作经历描述，包括公司名称、职位、工作内容和成果",
                "priority": "high",
            })
        else:
            # 检查是否有量化成果
            suggestions.append({
                "type": "experience",
                "title": "量化成果",
                "content": "建议在工作经历中添加具体的量化成果（如提升了X%的性能、完成了X个项目等）",
                "priority": "medium",
            })
        
        # 教育背景优化
        education = resume_data.get("education", [])
        if not education:
            suggestions.append({
                "type": "education",
                "title": "教育背景补充",
                "content": "建议添加完整的教育背景信息",
                "priority": "medium",
            })
        
        # 格式优化建议
        raw_text = resume_data.get("raw_text", "")
        if len(raw_text) < 200:
            suggestions.append({
                "type": "format",
                "title": "内容充实",
                "content": "简历内容较为简单，建议添加更多项目经验和个人技能描述",
                "priority": "medium",
            })
        
        # 关键词优化
        if jd_data.get("required_skills"):
            suggestions.append({
                "type": "keywords",
                "title": "关键词优化",
                "content": f"建议在简历中突出以下关键词: {', '.join(jd_data['required_skills'][:5])}",
                "priority": "low",
            })
        
        return {
            "suggestions": suggestions,
            "total_count": len(suggestions),
            "high_priority": sum(1 for s in suggestions if s.get("priority") == "high"),
        }