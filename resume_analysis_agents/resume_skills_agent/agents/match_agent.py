"""
人岗匹配智能体 - 负责计算简历与JD的匹配度
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager
from skills.match_skills.match_scoring_skill import MatchScoringSkill


class MatchAgent(BaseAgent):
    """
    人岗匹配智能体
    
    负责:
        - 对比简历与JD
        - 计算匹配度分数
        - 分析匹配/缺失技能
    """
    
    name = "match_agent"
    description = "人岗匹配智能体，负责计算简历与JD的匹配度"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """注册Match Agent的Skills"""
        self.skills_manager.register(self.name, MatchScoringSkill())
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行人岗匹配分析
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        parsed_resume = state.get("parsed_resume")
        parsed_jd = state.get("parsed_jd")
        
        if not parsed_resume:
            state["error"] = "未解析简历数据"
            return state
        
        if not parsed_jd:
            state["error"] = "未解析JD数据"
            return state
        
        # 执行匹配分析
        match_result = self.skills_manager.execute_skill(
            self.name, "match_scoring",
            resume_data=parsed_resume,
            jd_data=parsed_jd
        )
        
        if match_result and match_result.get("success"):
            state["match_result"] = match_result["result"]
        else:
            state["match_result"] = {"total_score": 0, "match_level": "分析失败"}
            state["error"] = f"匹配分析失败: {match_result.get('error', '未知错误')}"
        
        return state