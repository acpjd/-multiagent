"""
任务协调智能体 - 负责任务分发和流程控制
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager


class CoordinatorAgent(BaseAgent):
    """
    任务协调智能体
    
    负责:
        - 接收用户请求
        - 分发任务给各子智能体
        - 汇总结果
    """
    
    name = "coordinator"
    description = "任务协调智能体，负责任务分发和流程控制"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """Coordinator不需要注册Skills"""
        pass
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行协调任务
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        # 验证输入
        if not state.get("resume_file") and not state.get("jd_text"):
            state["error"] = "请提供简历文件或JD文本"
            return state
        
        # 初始化状态
        state["parsed_resume"] = state.get("parsed_resume")
        state["parsed_jd"] = state.get("parsed_jd")
        state["match_result"] = state.get("match_result")
        state["optimization_suggestions"] = state.get("optimization_suggestions")
        state["final_report"] = state.get("final_report")
        
        return state