"""
简历解析智能体 - 负责解析简历文件并提取结构化信息
"""

from typing import Any, Dict

from .base_agent import BaseAgent
from skills.skills_manager import SkillsManager
from skills.parser_skills.file_parse_skill import FileParseSkill
from skills.parser_skills.text_extraction_skill import TextExtractionSkill


class ParserAgent(BaseAgent):
    """
    简历解析智能体
    
    负责:
        - 解析PDF/Word/TXT简历文件
        - 提取结构化信息（姓名、联系方式、教育背景、工作经历、技能等）
    """
    
    name = "parser_agent"
    description = "简历解析智能体，负责解析简历文件并提取结构化信息"
    
    def __init__(self, skills_manager: SkillsManager):
        super().__init__(skills_manager)
    
    def _register_skills(self):
        """注册Parser Agent的Skills"""
        self.skills_manager.register(self.name, FileParseSkill())
        self.skills_manager.register(self.name, TextExtractionSkill())
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行简历解析
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        resume_file = state.get("resume_file")
        
        if not resume_file:
            state["error"] = "未提供简历文件"
            return state
        
        # 步骤1: 解析文件
        file_parse_result = self.skills_manager.execute_skill(
            self.name, "file_parse", file_path=resume_file
        )
        
        if not file_parse_result or not file_parse_result.get("success"):
            state["error"] = f"文件解析失败: {file_parse_result.get('error', '未知错误')}"
            return state
        
        raw_text = file_parse_result["result"]["text"]
        
        # 步骤2: 提取结构化信息
        extraction_result = self.skills_manager.execute_skill(
            self.name, "text_extraction", text=raw_text
        )
        
        if extraction_result and extraction_result.get("success"):
            state["parsed_resume"] = extraction_result["result"]
        else:
            state["parsed_resume"] = {"raw_text": raw_text}
        
        return state