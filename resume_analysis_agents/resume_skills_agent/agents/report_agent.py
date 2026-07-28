"""
报告生成智能体 - 负责生成综合分析报告
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager
from skills.report_skills.report_template_skill import ReportTemplateSkill


class ReportAgent(BaseAgent):
    """
    报告生成智能体
    
    负责:
        - 汇总各智能体分析结果
        - 生成结构化分析报告
    """
    
    name = "report_agent"
    description = "报告生成智能体，负责生成综合分析报告"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """注册Report Agent的Skills"""
        self.skills_manager.register(self.name, ReportTemplateSkill())
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行报告生成
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        parsed_resume = state.get("parsed_resume")
        parsed_jd = state.get("parsed_jd")
        match_result = state.get("match_result")
        suggestions = state.get("optimization_suggestions")
        
        if not parsed_resume:
            state["error"] = "未解析简历数据"
            return state
        
        if not match_result:
            state["error"] = "未进行匹配分析"
            return state
        
        # 生成报告
        report_result = self.skills_manager.execute_skill(
            self.name, "report_template",
            resume_data=parsed_resume,
            jd_data=parsed_jd or {},
            match_result=match_result,
            suggestions=suggestions or []
        )
        
        if report_result and report_result.get("success"):
            state["final_report"] = report_result["result"]
        else:
            state["final_report"] = {"error": "报告生成失败"}
            state["error"] = f"报告生成失败: {report_result.get('error', '未知错误')}"
        
        return state