"""
LangGraph工作流定义
"""

from langgraph.graph import StateGraph, END
from typing import Any, Dict

from .state import ResumeAnalysisState


def create_workflow(skills_manager, agents: Dict[str, Any]) -> StateGraph:
    """
    创建简历分析工作流
    
    Args:
        skills_manager: Skills管理器实例
        agents: 智能体字典
        
    Returns:
        编译后的工作流图
    """
    workflow = StateGraph(ResumeAnalysisState)
    
    # 添加节点
    workflow.add_node("parse_resume", agents["parser_agent"].run)
    workflow.add_node("analyze_jd", agents["jd_analyzer"].run)
    workflow.add_node("match_analysis", agents["match_agent"].run)
    workflow.add_node("optimize_resume", agents["optimize_agent"].run)
    workflow.add_node("generate_report", agents["report_agent"].run)
    
    # 设置入口点（并行开始解析简历和分析JD）
    workflow.set_entry_point("parse_resume")
    workflow.add_edge("parse_resume", "analyze_jd")
    
    # JD分析完成后进行匹配分析
    workflow.add_edge("analyze_jd", "match_analysis")
    
    # 匹配完成后生成优化建议
    workflow.add_edge("match_analysis", "optimize_resume")
    
    # 优化建议完成后生成最终报告
    workflow.add_edge("optimize_resume", "generate_report")
    
    # 报告生成完成后结束
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()