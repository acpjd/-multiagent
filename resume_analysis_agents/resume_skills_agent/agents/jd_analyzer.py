"""
JD分析智能体 - 负责分析岗位描述
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager
from skills.jd_skills.jd_analysis_skill import JDAnalysisSkill


class JDAnalyzerAgent(BaseAgent):
    """
    JD分析智能体
    
    负责:
        - 分析岗位描述(JD)
        - 提取关键要求（技能、经验、学历等）
    """
    
    name = "jd_analyzer"
    description = "JD分析智能体，负责分析岗位描述并提取关键要求"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """注册JD Analyzer Agent的Skills"""
        self.skills_manager.register(self.name, JDAnalysisSkill())
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行JD分析
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        jd_text = state.get("jd_text")
        
        if not jd_text:
            state["error"] = "未提供JD文本"
            return state
        
        # 执行JD分析
        analysis_result = self.skills_manager.execute_skill(
            self.name, "jd_analysis", jd_text=jd_text
        )
        
        if analysis_result and analysis_result.get("success"):
            state["parsed_jd"] = analysis_result["result"]
        else:
            state["parsed_jd"] = {"raw_text": jd_text}
            state["error"] = f"JD分析失败: {analysis_result.get('error', '未知错误')}"
        
        return state