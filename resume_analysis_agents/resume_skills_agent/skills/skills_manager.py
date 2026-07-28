"""
Skills管理器 - 负责Skills的注册、管理和调度
"""

from typing import Any, Dict, List, Optional
from .base_skill import BaseSkill


class SkillsManager:
    """
    Skills注册和调度管理器
    
    功能:
        - 注册Skill到指定Agent
        - 获取Agent的可用Skills
        - 执行指定Agent的指定Skill
        - 动态扩展Skills
    """
    
    def __init__(self):
        """初始化Skills管理器"""
        self._skills: Dict[str, Dict[str, BaseSkill]] = {}
    
    def register(self, agent_name: str, skill: BaseSkill) -> None:
        """
        注册Skill到指定Agent
        
        Args:
            agent_name: Agent名称
            skill: Skill实例
        """
        if agent_name not in self._skills:
            self._skills[agent_name] = {}
        self._skills[agent_name][skill.name] = skill
    
    def unregister(self, agent_name: str, skill_name: str) -> bool:
        """
        注销指定Agent的指定Skill
        
        Args:
            agent_name: Agent名称
            skill_name: Skill名称
            
        Returns:
            是否成功注销
        """
        if agent_name in self._skills and skill_name in self._skills[agent_name]:
            del self._skills[agent_name][skill_name]
            return True
        return False
    
    def get_skills(self, agent_name: str) -> Dict[str, BaseSkill]:
        """
        获取Agent的所有Skills
        
        Args:
            agent_name: Agent名称
            
        Returns:
            Skills字典
        """
        return self._skills.get(agent_name, {})
    
    def get_skill(self, agent_name: str, skill_name: str) -> Optional[BaseSkill]:
        """
        获取指定Agent的指定Skill
        
        Args:
            agent_name: Agent名称
            skill_name: Skill名称
            
        Returns:
            Skill实例，如果不存在则返回None
        """
        return self._skills.get(agent_name, {}).get(skill_name)
    
    def execute_skill(self, agent_name: str, skill_name: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        执行指定Agent的指定Skill
        
        Args:
            agent_name: Agent名称
            skill_name: Skill名称
            **kwargs: 执行参数
            
        Returns:
            执行结果，如果Skill不存在则返回None
        """
        skill = self.get_skill(agent_name, skill_name)
        if skill is None:
            return {"success": False, "error": f"Skill '{skill_name}' not found for agent '{agent_name}'"}
        
        if not skill.validate_input(**kwargs):
            return {"success": False, "error": "Input validation failed"}
        
        try:
            result = skill.execute(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_agent_skills_info(self, agent_name: str) -> List[Dict[str, str]]:
        """
        获取Agent所有Skills的信息
        
        Args:
            agent_name: Agent名称
            
        Returns:
            Skills信息列表
        """
        skills = self.get_skills(agent_name)
        return [skill.get_info() for skill in skills.values()]
    
    def list_agents(self) -> List[str]:
        """
        列出所有已注册Skills的Agent
        
        Returns:
            Agent名称列表
        """
        return list(self._skills.keys())
    
    def clear_agent_skills(self, agent_name: str) -> None:
        """
        清空指定Agent的所有Skills
        
        Args:
            agent_name: Agent名称
        """
        if agent_name in self._skills:
            self._skills[agent_name] = {}