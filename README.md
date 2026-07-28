# 📄 简历分析多智能体系统

基于 **LangGraph** 的多智能体简历分析与人岗匹配系统。

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    📄 简历分析多智能体系统                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐                                           │
│  │  Coordinator     │  ← 任务协调智能体                          │
│  │  Agent           │                                           │
│  └────────┬─────────┘                                           │
│           │                                                     │
│     ┌─────┴─────┬───────────┬───────────┬───────────┐          │
│     ▼           ▼           ▼           ▼           ▼          │
│  ┌──────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │Parser│  │  JD    │  │ Match  │  │Optimize│  │ Report │     │
│  │Agent │  │ Analyzer│  │ Agent  │  │ Agent  │  │ Agent  │     │
│  └──┬───┘  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘     │
│     │          │           │           │           │           │
│     ▼          ▼           ▼           ▼           ▼           │
│  ┌──────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │Skills│  │Skills  │  │Skills  │  │Skills  │  │Skills  │     │
│  └──────┘  └────────┘  └────────┘  └────────┘  └────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 智能体说明

| 智能体 | 职责 | Skills |
|--------|------|--------|
| **Parser Agent** | 解析简历文件 | FileParseSkill, TextExtractionSkill |
| **JD Analyzer** | 分析岗位描述 | JDAnalysisSkill |
| **Match Agent** | 人岗匹配分析 | MatchScoringSkill |
| **Optimize Agent** | 生成优化建议 | OptimizeWritingSkill |
| **Report Agent** | 生成分析报告 | ReportTemplateSkill |

## 📦 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

## 🚀 运行

```bash
streamlit run app.py
```

## 📁 项目结构

```
resume_skills_agent/
├── app.py                    # Streamlit Web界面
├── config.py                 # 配置文件
├── requirements.txt          # 依赖列表
├── .env.example              # 环境变量示例
│
├── agents/                   # 智能体模块
│   ├── base_agent.py         # 智能体基类
│   ├── coordinator.py        # 任务协调智能体
│   ├── parser_agent.py       # 简历解析智能体
│   ├── jd_analyzer.py        # JD分析智能体
│   ├── match_agent.py        # 人岗匹配智能体
│   ├── optimize_agent.py     # 简历优化智能体
│   └── report_agent.py       # 报告生成智能体
│
├── skills/                   # Skills模块
│   ├── base_skill.py         # Skill基类
│   ├── skills_manager.py     # Skills管理器
│   ├── parser_skills/        # Parser Skills
│   ├── jd_skills/            # JD Skills
│   ├── match_skills/         # Match Skills
│   ├── optimize_skills/      # Optimize Skills
│   └── report_skills/        # Report Skills
│
└── graph/                    # LangGraph工作流
    ├── state.py              # 状态定义
    └── workflow.py           # 工作流定义
```

## 🔧 扩展Skills

每个智能体的Skills可以按需扩展：

```python
# 在对应skills目录下创建新的Skill类
from skills.base_skill import BaseSkill

class MyNewSkill(BaseSkill):
    name = "my_new_skill"
    description = "我的新Skill"
    
    def execute(self, **kwargs):
        # 实现你的逻辑
        return {"result": "success"}

# 在对应Agent的_register_skills方法中注册
self.skills_manager.register(self.name, MyNewSkill())
```

## 📝 许可证

MIT License
