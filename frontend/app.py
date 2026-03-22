import streamlit as st
import requests
from datetime import datetime
import json

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="VeriNews AI - Fake News Detector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Root colors matching VeriNews design */
    :root {
        --bg: #080c10;
        --surface: #0e1318;
        --surface2: #141b22;
        --border: rgba(255,255,255,0.07);
        --accent: #00e5a0;
        --accent2: #00b8d9;
        --red: #ff4757;
        --yellow: #ffd32a;
        --text: #e8edf2;
        --muted: #6b7a8d;
    }
    
    /* Main page background */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #080c10;
        color: #e8edf2;
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    
    /* Remove Streamlit defaults */
    .main {
        padding: 0 !important;
    }
    
    /* Header styles */
    .header-container {
        background: linear-gradient(135deg, rgba(0,229,160,0.05), rgba(0,184,217,0.05));
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }
    
    .app-title .accent {
        background: linear-gradient(90deg, #00e5a0, #00b8d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-subtitle {
        color: #6b7a8d;
        font-size: 0.95rem;
        font-weight: 300;
        letter-spacing: 0.01em;
    }
    
    /* Input container */
    .input-section {
        background: #0e1318;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
    }
    
    .input-label {
        color: #e8edf2;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
        margin-bottom: 12px;
        display: block;
    }
    
    /* Text input */
    textarea {
        background-color: #141b22 !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        color: #e8edf2 !important;
        padding: 14px !important;
        font-size: 0.95rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    textarea:focus {
        border-color: #00e5a0 !important;
        box-shadow: 0 0 0 3px rgba(0,229,160,0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00e5a0, #00b8d9) !important;
        color: #000 !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        font-family: 'Syne', sans-serif !important;
    }
    
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(0,229,160,0.25) !important;
    }
    
    /* Result card */
    .result-container {
        background: #0e1318;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 28px;
        margin-top: 24px;
    }
    
    /* Result badge */
    .result-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.02em;
        margin-bottom: 16px;
        text-align: center;
        width: 100%;
    }
    
    .badge-true {
        background: rgba(0,229,160,0.12);
        border: 1px solid rgba(0,229,160,0.3);
        color: #00e5a0;
    }
    
    .badge-false {
        background: rgba(255,71,87,0.12);
        border: 1px solid rgba(255,71,87,0.3);
        color: #ff4757;
    }
    
    .badge-suspicious {
        background: rgba(255,211,42,0.12);
        border: 1px solid rgba(255,211,42,0.3);
        color: #ffd32a;
    }
    
    /* Confidence bar */
    .confidence-label {
        color: #6b7a8d;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
    }
    
    .confidence-bar {
        width: 100%;
        height: 8px;
        background: #141b22;
        border-radius: 100px;
        overflow: hidden;
        margin-bottom: 16px;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #00e5a0, #00b8d9);
        transition: width 0.6s ease;
    }
    
    /* Input echo */
    .input-echo {
        background: #141b22;
        border-left: 3px solid #00e5a0;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-style: italic;
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Info card */
    .info-card {
        background: rgba(0,229,160,0.05);
        border: 1px solid rgba(0,229,160,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-top: 20px;
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Timestamp */
    .timestamp {
        color: #6b7a8d;
        font-size: 0.78rem;
        margin-top: 12px;
        text-align: right;
    }
    
    /* Links back to landing */
    .nav-links {
        text-align: center;
        margin-top: 40px;
        padding-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.07);
        color: #6b7a8d;
        font-size: 0.85rem;
    }
    
    .nav-links a {
        color: #00e5a0;
        text-decoration: none;
        font-weight: 600;
        transition: opacity 0.2s;
    }
    
    .nav-links a:hover {
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="header-container">
    <div class="app-title">
        🔍 <span class="accent">VeriNews</span> AI
    </div>
    <div class="app-subtitle">
        Detect Fake News with AI Precision in Real Time
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- MAIN CONTAINER ----------
st.markdown('<div class="input-section">', unsafe_allow_html=True)

st.markdown('<label class="input-label">📝 Enter News or Claim to Verify</label>', unsafe_allow_html=True)

# Initialize session state for form persistence
if "news_input" not in st.session_state:
    st.session_state.news_input = ""

if "result" not in st.session_state:
    st.session_state.result = None

# Text input
news_text = st.text_area(
    label="claim_input",
    value=st.session_state.news_input,
    placeholder="e.g., '5G towers cause COVID-19' or 'The Earth is round'...",
    height=120,
    label_visibility="collapsed",
    key="news_input_textarea"
)

st.session_state.news_input = news_text

st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHECK BUTTON ----------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🚀 Check Fact", use_container_width=True):
        if news_text.strip():
            try:
                # Call the FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/check",
                    params={"text": news_text},
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.session_state.result = response.json()
                else:
                    st.error("❌ Backend error. Is the FastAPI server running on http://127.0.0.1:8000?")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please start FastAPI: `python -m uvicorn backend.api:app --reload`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a claim to check")

# ---------- RESULTS ----------
if st.session_state.result:
    res = st.session_state.result
    
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    # Input echo
    st.markdown(f"""
    <div class="input-echo">
        "{news_text[:120]}{'...' if len(news_text) > 120 else ''}"
    </div>
    """, unsafe_allow_html=True)
    
    # Verdict badge
    verdict = res.get("result", "unknown").upper()
    confidence = round(res.get("confidence", 0) * 100, 1)
    
    if verdict == "TRUE":
        st.markdown(f"""
        <div class="result-badge badge-true">
            ✅ TRUE NEWS ({confidence}%)
        </div>
        """, unsafe_allow_html=True)
    elif verdict == "FALSE":
        st.markdown(f"""
        <div class="result-badge badge-false">
            ❌ FAKE NEWS ({confidence}%)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-badge badge-suspicious">
            ⚠️ SUSPICIOUS ({confidence}%)
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence bar
    st.markdown(f"""
    <div class="confidence-label">
        <span>Confidence Score</span>
        <span style="color: #00e5a0; font-weight: 600;">{confidence}%</span>
    </div>
    <div class="confidence-bar">
        <div class="confidence-fill" style="width: {confidence}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info box
    if verdict == "TRUE":
        st.markdown("""
        <div class="info-card">
            ✓ This claim matches verified facts in our database with high confidence.
            The information aligns with credible sources and trusted databases.
        </div>
        """, unsafe_allow_html=True)
    elif verdict == "FALSE":
        st.markdown("""
        <div class="info-card">
            ✗ This claim contradicts verified facts or matches known misinformation patterns.
            Exercise strong skepticism and fact-check with credible sources.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            ⚠ This claim is partially similar to known facts but contains elements that
            cannot be fully verified. Additional context or sources are recommended.
        </div>
        """, unsafe_allow_html=True)
    
    # Timestamp
    st.markdown(f"""
    <div class="timestamp">
        Verified {datetime.now().strftime('%I:%M %p')}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="nav-links">
    <p>
        Back to <a href="http://localhost:5000" target="_self">landing page</a> • 
        View <a href="http://127.0.0.1:8000/docs" target="_blank">API Docs</a>
    </p>
</div>
""", unsafe_allow_html=True)

