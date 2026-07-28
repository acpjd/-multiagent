"""
简历优化智能体 - 负责生成简历优化建议
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager
from skills.optimize_skills.optimize_writing_skill import OptimizeWritingSkill


class OptimizeAgent(BaseAgent):
    """
    简历优化智能体
    
    负责:
        - 根据匹配结果生成优化建议
        - 提供简历改进方向
    """
    
    name = "optimize_agent"
    description = "简历优化智能体，负责生成简历优化建议"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """注册Optimize Agent的Skills"""
        self.skills_manager.register(self.name, OptimizeWritingSkill())
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行简历优化建议生成
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        parsed_resume = state.get("parsed_resume")
        match_result = state.get("match_result")
        parsed_jd = state.get("parsed_jd")
        
        if not parsed_resume:
            state["error"] = "未解析简历数据"
            return state
        
        if not match_result:
            state["error"] = "未进行匹配分析"
            return state
        
        # 生成优化建议
        optimize_result = self.skills_manager.execute_skill(
            self.name, "optimize_writing",
            resume_data=parsed_resume,
            match_result=match_result,
            jd_data=parsed_jd or {}
        )
        
        if optimize_result and optimize_result.get("success"):
            state["optimization_suggestions"] = optimize_result["result"].get("suggestions", [])
        else:
            state["optimization_suggestions"] = []
            state["error"] = f"优化建议生成失败: {optimize_result.get('error', '未知错误')}"
        
        return state