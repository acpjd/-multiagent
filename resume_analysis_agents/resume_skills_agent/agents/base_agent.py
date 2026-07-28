"""
智能体基类 - 所有Agent的抽象基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from skills.skills_manager import SkillsManager


class BaseAgent(ABC):
    """
    智能体基类
    
    属性:
        name: 智能体名称
        description: 智能体描述
        skills_manager: Skills管理器
    """
    
    name: str = "base_agent"
    description: str = "基础智能体"
    
    def __init__(self, skills_manager: SkillsManager):
        """
        初始化智能体
        
        Args:
            skills_manager: Skills管理器实例
        """
        self.skills_manager = skills_manager
        self._register_skills()
    
    @abstractmethod
    def _register_skills(self):
        """注册该智能体的Skills（子类必须实现）"""
        pass
    
    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行智能体任务
        
        Args:
            state: 工作流状态
            
        Returns:
            更新后的状态
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """获取智能体信息"""
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skills_manager.get_agent_skills_info(self.name),
        }