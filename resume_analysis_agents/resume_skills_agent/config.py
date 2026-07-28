"""
配置文件 - 简历分析系统配置
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM配置
LLM_CONFIG = {
    "api_key": os.getenv("LLM_API_KEY", ""),
    "base_url": os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
    "model": os.getenv("LLM_MODEL", "gpt-4o"),
    "temperature": 0.1,
}

# 系统配置
SYSTEM_CONFIG = {
    "max_retries": 3,
    "timeout": 60,
    "enable_logging": True,
}

# Skills配置
SKILLS_CONFIG = {
    "parser_agent": {
        "enabled_skills": ["file_parse", "text_extraction"],
    },
    "jd_analyzer": {
        "enabled_skills": ["jd_analysis"],
    },
    "match_agent": {
        "enabled_skills": ["match_scoring"],
    },
    "optimize_agent": {
        "enabled_skills": ["optimize_writing"],
    },
    "report_agent": {
        "enabled_skills": ["report_template"],
    },
}