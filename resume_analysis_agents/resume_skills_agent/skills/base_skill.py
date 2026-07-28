"""
Skill基类 - 所有Skills的抽象基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseSkill(ABC):
    """
    Skill基类，所有具体Skill的父类
    
    属性:
        name: Skill名称
        description: Skill描述
        version: Skill版本
    """
    
    name: str = "base_skill"
    description: str = "基础Skill"
    version: str = "0.1.0"
    
    def __init__(self):
        """初始化Skill"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行Skill
        
        Args:
            **kwargs: 执行参数
            
        Returns:
            执行结果字典
        """
        pass
    
    def validate_input(self, **kwargs) -> bool:
        """
        验证输入参数
        
        Args:
            **kwargs: 输入参数
            
        Returns:
            验证是否通过
        """
        return True
    
    def get_info(self) -> Dict[str, str]:
        """
        获取Skill信息
        
        Returns:
            Skill信息字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
        }