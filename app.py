import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from docx import Document

# Initialize Page
st.set_page_config(page_title="Rajat Mahajan | AI Portfolio", layout="wide")

# -------------------------------------------------
# 1. UI Styling: Midnight Black, Electric Blue & Animations
# -------------------------------------------------
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* Hero Section */
    .hero {
        padding: 60px 20px;
        border-radius: 20px;
        background: radial-gradient(circle at center, #111 0%, #000 100%);
        border-bottom: 1px solid #222;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Glass Cards */
    .card {
        padding: 25px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #D1D1D1;
        margin-bottom: 20px;
    }

    /* Animated Progress Bars */
    .skill-container {
        width: 100%;
        background-color: #222;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .skill-bar {
        height: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, #0072FF, #00D4FF);
        animation: progress 2s ease-out forwards;
        width: 0%;
    }

    @keyframes progress {
        from { width: 0%; }
        to { width: var(--target-width); }
    }

    .project-card {
        border-radius: 15px;
        background: #0A0A0A;
        border: 1px solid #222;
        overflow: hidden;
        margin-bottom: 25px;
        transition: 0.3s;
    }
    
    .project-card:hover {
        border-color: #00D4FF;
        transform: translateY(-5px);
    }

    h1, h2, h3 {
        color: #00D4FF !important;
    }

    /* Floating Chat Button */
    div.stButton > button:first-child {
        position: fixed;
        bottom: 35px;
        right: 35px;
        width: 65px;
        height: 65px;
        border-radius: 50% !important;
        background: linear-gradient(45deg, #00D4FF, #0072FF) !important;
        color: white !important;
        border: none !important;
        z-index: 9999;
        box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 2. Helper for Skills
# -------------------------------------------------
def render_skill(name, level):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{name}</span>
            <span style="color: #00D4FF;">{level}%</span>
        </div>
        <div class="skill-container">
            <div class="skill-bar" style="--target-width: {level}%;"></div>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 3. Main Page Layout
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <h1 style="font-size: 4rem; letter-spacing: -1px; margin-bottom: 0;">RAJAT MAHAJAN</h1>
    <p style="font-size: 1.4rem; color: #666; font-weight: 300;">AI Explorer • Software Architect • Problem Solver</p>
</div>
""", unsafe_allow_html=True)

# Main Body
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.markdown("### 🚀 Areas of Interest")
    st.markdown("""
    <div class="card">
    Rajat is bridging the gap between static data and dynamic conversational interfaces using <b>Retrieval-Augmented Generation (RAG)</b>. 
    His journey involves mastering LLM orchestration, vector databases, and autonomous AI agents. 
    He is focused on 'Applied AI'—turning complex back-end logic into intuitive, impactful software solutions.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Featured Projects")
    p_col1, p_col2 = st.columns(2)
    # Project data
    projects = [
        {"title": "AI Document Analyzer", "desc": "Query complex documents with RAG.", "img": "https://via.placeholder.com/400x200/111/00D4FF?text=RAG+Analyzer"},
        {"title": "Autonomous Agent Lab", "desc": "Experimental reasoning agents.", "img": "https://via.placeholder.com/400x200/111/00D4FF?text=AI+Agents"}
    ]
    for i, col in enumerate([p_col1, p_col2]):
        with col:
            st.markdown(f"""
            <div class="project-card">
                <img src="{projects[i]['img']}" style="width:100%">
                <div style="padding:15px">
                    <h4 style="margin:0; color:#00D4FF">{projects[i]['title']}</h4>
                    <p style="color:#888; font-size:0.9rem; margin-top:5px">{projects[i]['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col_right:
    st.markdown("### ⚡ Technical Expertise")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_skill("Python / Machine Learning", 90)
        render_skill("LLMs & LangChain", 85)
        render_skill("Streamlit / Web UI", 80)
        render_skill("Vector DBs (Chroma/Pinecone)", 75)
        render_skill("API Integration (OpenAI/Anthropic)", 88)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# 4. Floating Chatbot Logic (Remains the same)
# -------------------------------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("💬"):
    st.session_state.chat_open = not st.session_state.chat_open

if st.session_state.chat_open:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #00D4FF;'>AI Assistant</h2>", unsafe_allow_html=True)
        st.write("---")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        if prompt := st.chat_input("Ask about Rajat..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Response logic placeholder
            response = f"Rajat has a {next(iter([90]), 0)}% proficiency in core AI technologies. He's currently expanding his portfolio with {prompt}."
            with st.chat_message("assistant"):
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
