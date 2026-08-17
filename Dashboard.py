import streamlit as st
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SalesPilot AI | Intelligent Business Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS FOR TARGET DESIGN
# ==========================================================

st.markdown("""
<style>
/* Hide Streamlit default headers & footers */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Base App Background */
.stApp {
    background-color: #0B0F19;
    color: #F8FAFC;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0D1322;
    border-right: 1px solid #1E293B;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #1E293B;
    margin-bottom: 20px;
}

.sidebar-brand-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

.sidebar-brand-title {
    font-size: 20px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1.1;
}

.sidebar-brand-subtitle {
    font-size: 11px;
    color: #94A3B8;
    font-weight: 500;
}

/* Sidebar Action Cards */
.sidebar-card {
    background: #131B2E;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
}

.sidebar-card h4 {
    font-size: 14px;
    color: #F8FAFC;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.sidebar-card p {
    font-size: 12px;
    color: #94A3B8;
    margin-bottom: 12px;
    line-height: 1.3;
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, #0F2B7B 0%, #1D4ED8 40%, #1E1B4B 100%);
    border-radius: 20px;
    padding: 35px 40px;
    color: #FFFFFF;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
    margin-bottom: 30px;
}

.hero-brand-name {
    font-size: 52px;
    font-weight: 900;
    font-family: 'Outfit', 'Inter', system-ui, sans-serif;
    background: linear-gradient(135deg, #60A5FA 0%, #38BDF8 50%, #FFFFFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 6px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 15px;
    letter-spacing: -1px;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 16px;
    color: #E2E8F0;
    margin-bottom: 25px;
    max-width: 900px;
    line-height: 1.5;
}

.hero-badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* Hero Mini Mockup Widgets */
.hero-mockup-card {
    background: rgba(13, 19, 35, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 14px;
    color: #FFFFFF;
}

.hero-mockup-title {
    font-size: 11px;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.hero-mockup-val {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
}

/* Section Titles */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 700;
    color: #F8FAFC;
    margin: 25px 0 18px 0;
}

/* Capability Cards */
.capability-card {
    background: #131B2E;
    border-radius: 16px;
    padding: 22px;
    border: 1px solid #1E293B;
    height: 100%;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.capability-card:hover {
    border-color: #2563EB;
    transform: translateY(-3px);
}

.capability-icon-box {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 16px;
}

.icon-blue { background: rgba(37, 99, 235, 0.2); color: #3B82F6; border: 1px solid rgba(37, 99, 235, 0.3); }
.icon-green { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
.icon-purple { background: rgba(139, 92, 246, 0.2); color: #A78BFA; border: 1px solid rgba(139, 92, 246, 0.3); }
.icon-orange { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }

.capability-title {
    font-size: 17px;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.capability-desc {
    font-size: 13px;
    color: #94A3B8;
    line-height: 1.4;
    margin-bottom: 16px;
    min-height: 38px;
}

.capability-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #CBD5E1;
    margin-bottom: 6px;
}

.capability-item span {
    color: #34D399;
    font-weight: bold;
}

/* Workflow Section */
.workflow-container {
    background: #131B2E;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 24px;
    margin-top: 15px;
}

.workflow-step {
    text-align: center;
    position: relative;
}

.workflow-num {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #2563EB;
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px auto;
    box-shadow: 0 0 12px rgba(37, 99, 235, 0.5);
}

.step-2 { background: #10B981; box-shadow: 0 0 12px rgba(16, 185, 129, 0.5); }
.step-3 { background: #3B82F6; box-shadow: 0 0 12px rgba(59, 130, 246, 0.5); }
.step-4 { background: #8B5CF6; box-shadow: 0 0 12px rgba(139, 92, 246, 0.5); }
.step-5 { background: #EC4899; box-shadow: 0 0 12px rgba(236, 72, 153, 0.5); }
.step-6 { background: #06B6D4; box-shadow: 0 0 12px rgba(6, 182, 212, 0.5); }

.workflow-title {
    font-size: 14px;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 4px;
}

.workflow-desc {
    font-size: 11px;
    color: #94A3B8;
}

/* Tech Stack Badges */
.tech-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1E293B;
    border: 1px solid #334155;
    color: #F8FAFC;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
}

/* Bottom Footer Bar */
.footer-bar {
    border-top: 1px solid #1E293B;
    padding-top: 20px;
    margin-top: 35px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #64748B;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR HEADER & NAVIGATION BRAND
# ==========================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">📈</div>
        <div>
            <div class="sidebar-brand-title">SalesPilot AI</div>
            <div class="sidebar-brand-subtitle">Intelligent Business Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Navigation")
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("📤 Upload", use_container_width=True):
            st.switch_page("pages/1_Upload_Data.py")
    with col_nav2:
        if st.button("📊 Analysis", use_container_width=True):
            st.switch_page("pages/2_Data_Analysis.py")

    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("📈 Forecast", use_container_width=True):
            st.switch_page("pages/4_Forecasting.py")
    with col_nav4:
        if st.button("🤖 Assistant", use_container_width=True):
            st.switch_page("pages/6_Insight Talk.py")

    if st.button("📑 Executive Report", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Reports.py")

    st.markdown("""
    <div class="sidebar-card">
        <h4>✨ Get Started</h4>
        <p>Upload your sales dataset to unlock automated analytics and forecasts.</p>
    </div>
    
    <div class="sidebar-card">
        <h4>🤖 AI Assistant</h4>
        <p>Ask natural language questions about your business metrics anytime.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Open AI Assistant →", use_container_width=True):
        st.switch_page("pages/6_Insight Talk.py")
        
    st.caption("AI-Powered • Data-Driven • Smart Decisions")

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero-container">
    <div class="hero-brand-name">SalesPilot AI</div>
    <div class="hero-title">Find Insights & Analyze Sales</div>
    <div class="hero-subtitle">
        Transform raw sales data into meaningful business insights with advanced analytics, 
        machine learning, and conversational AI.
    </div>
</div>
""", unsafe_allow_html=True)

btn_col1, btn_col2, btn_spacer = st.columns([1, 1, 2])
with btn_col1:
    if st.button("🚀 Get Started", type="primary", use_container_width=True):
        st.switch_page("pages/1_Upload_Data.py")
with btn_col2:
    if st.button("🤖 Ask AI Assistant", use_container_width=True):
        st.switch_page("pages/6_Insight Talk.py")




# ==========================================================
# CORE CAPABILITIES SECTION
# ==========================================================

st.markdown("""
<div class="section-header">
    🚀 Core Capabilities
</div>
""", unsafe_allow_html=True)

cap1, cap2, cap3, cap4 = st.columns(4)

with cap1:
    st.markdown("""
    <div class="capability-card">
        <div class="capability-icon-box icon-blue">📂</div>
        <div class="capability-title">Data Processing</div>
        <div class="capability-desc">Upload, clean, and preprocess your data automatically for accurate analysis.</div>
        <div class="capability-item"><span>✓</span> CSV & Excel Support</div>
        <div class="capability-item"><span>✓</span> Automated Cleaning</div>
        <div class="capability-item"><span>✓</span> Missing Value Handling</div>
        <div class="capability-item"><span>✓</span> Feature Engineering</div>
    </div>
    """, unsafe_allow_html=True)

with cap2:
    st.markdown("""
    <div class="capability-card">
        <div class="capability-icon-box icon-green">📊</div>
        <div class="capability-title">Business Analytics</div>
        <div class="capability-desc">Explore KPIs, trends, and patterns with interactive visualizations and insights.</div>
        <div class="capability-item"><span>✓</span> KPI Dashboard</div>
        <div class="capability-item"><span>✓</span> Interactive Charts</div>
        <div class="capability-item"><span>✓</span> Category Analysis</div>
        <div class="capability-item"><span>✓</span> Regional Insights</div>
    </div>
    """, unsafe_allow_html=True)

with cap3:
    st.markdown("""
    <div class="capability-card">
        <div class="capability-icon-box icon-purple">🧠</div>
        <div class="capability-title">Machine Learning</div>
        <div class="capability-desc">Train, compare, and select the best ML models for accurate sales forecasting.</div>
        <div class="capability-item"><span>✓</span> Multiple ML Models</div>
        <div class="capability-item"><span>✓</span> Model Comparison</div>
        <div class="capability-item"><span>✓</span> Performance Metrics</div>
        <div class="capability-item"><span>✓</span> Best Model Selection</div>
    </div>
    """, unsafe_allow_html=True)

with cap4:
    st.markdown("""
    <div class="capability-card">
        <div class="capability-icon-box icon-orange">📈</div>
        <div class="capability-title">Forecasting</div>
        <div class="capability-desc">Generate accurate future sales forecasts with confidence intervals and insights.</div>
        <div class="capability-item"><span>✓</span> Future Prediction</div>
        <div class="capability-item"><span>✓</span> Forecast Visualization</div>
        <div class="capability-item"><span>✓</span> Historical vs Predicted</div>
        <div class="capability-item"><span>✓</span> Export Results</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PROJECT WORKFLOW SECTION
# ==========================================================

st.markdown("""
<div class="section-header">
    🎯 Project Workflow
</div>
""", unsafe_allow_html=True)

wf1, wf2, wf3, wf4, wf5, wf6 = st.columns(6)

with wf1:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num">1</div>
            <div class="workflow-title">📁 Upload Data</div>
            <div class="workflow-desc">Upload your sales dataset</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with wf2:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num step-2">2</div>
            <div class="workflow-title">🧹 Process Data</div>
            <div class="workflow-desc">Clean & preprocess data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with wf3:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num step-3">3</div>
            <div class="workflow-title">📊 Analyze Data</div>
            <div class="workflow-desc">Explore insights & charts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with wf4:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num step-4">4</div>
            <div class="workflow-title">🧠 Train Models</div>
            <div class="workflow-desc">Train & evaluate models</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with wf5:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num step-5">5</div>
            <div class="workflow-title">📈 Forecast Sales</div>
            <div class="workflow-desc">Generate future predictions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with wf6:
    st.markdown("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="workflow-num step-6">6</div>
            <div class="workflow-title">📑 Generate Report</div>
            <div class="workflow-desc">Export PDF & AI reports</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# BOTTOM TECH STACK & WHY US SECTION
# ==========================================================

st.write("")
bot_col1, bot_col2 = st.columns([1, 1])

with bot_col1:
    st.markdown("""
    <div class="section-header">
        &lt;/&gt; Technology Stack
    </div>
    <div style="background: #131B2E; border: 1px solid #1E293B; border-radius: 16px; padding: 20px;">
        <span class="tech-badge">🐍 Python</span>
        <span class="tech-badge">🐼 Pandas</span>
        <span class="tech-badge">🔢 NumPy</span>
        <span class="tech-badge">🤖 Scikit-learn</span>
        <span class="tech-badge">📊 Plotly</span>
        <span class="tech-badge">👑 Streamlit</span>
        <span class="tech-badge">✨ Google Gemini</span>
        <span class="tech-badge">📑 ReportLab</span>
    </div>
    """, unsafe_allow_html=True)

with bot_col2:
    st.markdown("""
    <div class="section-header">
        🛡️ Why SalesPilot AI?
    </div>
    <div style="background: #131B2E; border: 1px solid #1E293B; border-radius: 16px; padding: 20px; display: flex; flex-wrap: wrap; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;">
            <span style="color: #38BDF8; font-size: 18px;">🎯</span> Accurate Predictions
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;">
            <span style="color: #10B981; font-size: 18px;">📊</span> Data-Driven Insights
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;">
            <span style="color: #8B5CF6; font-size: 18px;">🧠</span> AI-Powered Analysis
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;">
            <span style="color: #F59E0B; font-size: 18px;">⚡</span> Interactive Experience
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;">
            <span style="color: #EC4899; font-size: 18px;">📥</span> Export & Share
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# FOOTER BAR
# ==========================================================

st.markdown("""
<div class="footer-bar">
    <div>✨ Empowering businesses with AI-driven analytics and intelligent forecasting.</div>
</div>
""", unsafe_allow_html=True)