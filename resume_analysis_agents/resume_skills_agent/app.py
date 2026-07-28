"""
Streamlit Web界面 - 简历分析系统前端
"""

import os
import streamlit as st
from skills.skills_manager import SkillsManager
from agents.parser_agent import ParserAgent
from agents.jd_analyzer import JDAnalyzerAgent
from agents.match_agent import MatchAgent
from agents.optimize_agent import OptimizeAgent
from agents.report_agent import ReportAgent
from graph.workflow import create_workflow


# 页面配置
st.set_page_config(
    page_title="简历分析多智能体系统",
    page_icon="📄",
    layout="wide",
)


@st.cache_resource
def init_system():
    """初始化系统（缓存）"""
    skills_manager = SkillsManager()
    
    agents = {
        "parser_agent": ParserAgent(skills_manager),
        "jd_analyzer": JDAnalyzerAgent(skills_manager),
        "match_agent": MatchAgent(skills_manager),
        "optimize_agent": OptimizeAgent(skills_manager),
        "report_agent": ReportAgent(skills_manager),
    }
    
    workflow = create_workflow(skills_manager, agents)
    return skills_manager, agents, workflow


def run_analysis(workflow, resume_file, jd_text):
    """运行分析工作流"""
    initial_state = {
        "resume_file": resume_file,
        "jd_text": jd_text,
        "parsed_resume": None,
        "parsed_jd": None,
        "match_result": None,
        "optimization_suggestions": None,
        "final_report": None,
        "error": None,
    }
    
    result = workflow.invoke(initial_state)
    return result


def main():
    st.title("📄 简历分析多智能体系统")
    st.markdown("基于LangGraph的多智能体简历分析与人岗匹配系统")
    
    # 侧边栏
    with st.sidebar:
        st.header("系统信息")
        skills_manager, agents, workflow = init_system()
        
        st.subheader("已注册智能体")
        for name, agent in agents.items():
            info = agent.get_info()
            with st.expander(f"🤖 {name}"):
                st.write(f"**描述**: {info['description']}")
                skills = info.get("skills", [])
                if skills:
                    st.write("**Skills**:")
                    for skill in skills:
                        st.write(f"  - {skill['name']}")
    
    # 主区域
    tab1, tab2, tab3 = st.tabs(["📤 上传简历", "📊 分析结果", "📝 优化建议"])
    
    with tab1:
        st.header("上传简历和岗位描述")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 上传简历")
            uploaded_file = st.file_uploader(
                "选择简历文件",
                type=["pdf", "docx", "txt"],
                help="支持PDF、Word、TXT格式"
            )
            
            if uploaded_file:
                # 保存上传的文件
                upload_dir = "uploads"
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"文件已上传: {uploaded_file.name}")
        
        with col2:
            st.subheader("💼 岗位描述(JD)")
            jd_text = st.text_area(
                "粘贴岗位描述",
                height=300,
                placeholder="请粘贴岗位描述文本...",
                help="可选，不提供则只分析简历"
            )
        
        # 分析按钮
        if st.button("🚀 开始分析", type="primary", use_container_width=True):
            if not uploaded_file:
                st.error("请先上传简历文件")
            else:
                with st.spinner("正在分析中，请稍候..."):
                    result = run_analysis(workflow, file_path, jd_text)
                    st.session_state["analysis_result"] = result
        
        # 显示错误
        if st.session_state.get("analysis_result", {}).get("error"):
            st.error(f"分析出错: {st.session_state['analysis_result']['error']}")
    
    with tab2:
        st.header("分析结果")
        
        result = st.session_state.get("analysis_result")
        if not result:
            st.info("请先上传简历并点击开始分析")
        else:
            report = result.get("final_report")
            if report:
                # 匹配摘要
                match_summary = report.get("match_summary", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总匹配度", f"{match_summary.get('total_score', 0)}分")
                with col2:
                    st.metric("匹配等级", match_summary.get("match_level", "N/A"))
                with col3:
                    st.metric("技能匹配", f"{match_summary.get('skills_score', 0)}分")
                
                # 技能分析
                st.subheader("🔍 技能分析")
                skills_analysis = report.get("skills_analysis", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**已掌握技能**")
                    for skill in skills_analysis.get("candidate_skills", []):
                        st.write(f"✅ {skill}")
                
                with col2:
                    st.write("**缺失技能**")
                    missing = skills_analysis.get("missing_skills", [])
                    if missing:
                        for skill in missing:
                            st.write(f"❌ {skill}")
                    else:
                        st.success("无缺失技能！")
                
                # 总体评估
                st.subheader("📋 总体评估")
                st.write(report.get("overall_assessment", "暂无评估"))
            else:
                st.warning("暂无分析报告")
    
    with tab3:
        st.header("优化建议")
        
        result = st.session_state.get("analysis_result")
        if not result:
            st.info("请先上传简历并点击开始分析")
        else:
            report = result.get("final_report")
            if report:
                suggestions = report.get("optimization_suggestions", [])
                if suggestions:
                    for i, suggestion in enumerate(suggestions, 1):
                        priority = suggestion.get("priority", "low")
                        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                        
                        with st.expander(f"{priority_icon} {suggestion.get('title', f'建议{i}')}"):
                            st.write(suggestion.get("content", ""))
                            st.caption(f"优先级: {priority}")
                else:
                    st.success("暂无优化建议，简历质量良好！")
            else:
                st.warning("暂无优化建议")


if __name__ == "__main__":
    main()