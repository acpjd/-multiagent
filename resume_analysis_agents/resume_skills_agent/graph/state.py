"""
LangGraph状态定义
"""

from typing import Any, Dict, List, Optional, TypedDict


class ResumeAnalysisState(TypedDict):
    """
    简历分析工作流状态
    
    包含整个分析流程中所有节点共享的数据
    """
    # 输入
    resume_file: Optional[str]           # 上传的简历文件路径
    jd_text: Optional[str]               # 岗位描述文本
    
    # Parser Agent输出
    parsed_resume: Optional[Dict[str, Any]]      # 解析后的简历数据
    
    # JD Analyzer Agent输出
    parsed_jd: Optional[Dict[str, Any]]          # 解析后的JD数据
    
    # Match Agent输出
    match_result: Optional[Dict[str, Any]]       # 匹配分析结果
    
    # Optimize Agent输出
    optimization_suggestions: Optional[List[Dict[str, Any]]]  # 优化建议列表
    
    # Report Agent输出
    final_report: Optional[Dict[str, Any]]       # 最终分析报告
    
    # 错误信息
    error: Optional[str]                         # 错误信息