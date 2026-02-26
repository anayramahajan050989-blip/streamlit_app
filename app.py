import streamlit as st
# (Keep your other imports: OpenAI, SentenceTransformer, etc.)

st.set_page_config(page_title="Rajat Mahajan", layout="wide")

# -------------------------------------------------
# UI Styling: Dark Blue & White Theme
# -------------------------------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0A192F; /* Deep Navy Blue */
        color: #E6F1FF;
    }

    /* Hero Section */
    .hero {
        padding: 60px;
        border-radius: 20px;
        background: linear-gradient(135deg, #112240 0%, #1d3557 100%);
        color: white;
        margin-bottom: 30px;
        border: 1px solid #233554;
        text-align: center;
    }

    /* Content Cards */
    .card {
        padding: 30px;
        border-radius: 12px;
        background-color: #112240; /* Slightly lighter navy */
        color: #CCD6F6;
        margin-bottom: 25px;
        border-left: 5px solid #64FFDA; /* Teal accent for "pop" */
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    }

    h1, h2, h3 {
        color: #64FFDA !important; /* Teal/Cyan headers */
    }

    /* Floating Chat Button Styling */
    .stButton > button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 70px;
        height: 70px;
        border-radius: 50% !important;
        background-color: #64FFDA !important; /* Bright Teal */
        color: #0A192F !important;
        font-size: 30px !important;
        border: none !important;
        z-index: 1000;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
        transition: transform 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.1);
        background-color: #52e0c4 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO SECTION
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <h1 style="font-size: 3.5rem; margin-bottom: 0;">Rajat Mahajan</h1>
    <p style="font-size: 1.2rem; color: #8892B0;">AI Engineer | Portfolio & Experience</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CONTENT (Cards)
# -------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📄 Professional Summary")
    st.markdown(f'<div class="card">{resume_text[:1200]}...</div>', unsafe_allow_html=True)
    
    st.markdown("## 💼 Experience")
    st.markdown(f'<div class="card">{resume_text[1200:2500]}...</div>', unsafe_allow_html=True)

with col2:
    st.markdown("## 🛠️ Skills")
    st.markdown(f'<div class="card">{resume_text[2500:3500]}</div>', unsafe_allow_html=True)

# -------------------------------------------------
# MODERN FLOATING CHATBOT LOGIC
# -------------------------------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# The Floating Action Button (FAB)
if st.button("💬"):
    st.session_state.chat_open = not st.session_state.chat_open

# The Chat Overlay (using Sidebar for a clean "App" feel)
if st.session_state.chat_open:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #64FFDA;'>AI Assistant</h2>", unsafe_allow_html=True)
        st.write("---")
        
        # Container for chat history
        chat_placeholder = st.container()
        
        with chat_placeholder:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Input at the bottom of sidebar
        if prompt := st.chat_input("How can Rajat help?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Logic for Retrieval and OpenAI...
            # (Insert your existing streaming/RAG logic here)
            
            # For demonstration, a placeholder response:
            with st.chat_message("assistant"):
                response = "I'm analyzing Rajat's resume for you..."
                st.write(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
