import streamlit as st

st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="🚀",
    layout="wide"
)

# -------------------------
# COLORFUL STYLE
# -------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(120deg,#eef2ff,#f0f9ff);
}

.hero {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    padding: 40px;
    border-radius: 18px;
    color: white;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.chat-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 360px;
    z-index: 1000;
}

.chat-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0px 12px 40px rgba(0,0,0,0.25);
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO
# -------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>DevOps Manager • Cloud Architect • 14+ Years Experience</h3>
<p>
Expert in AWS, Kubernetes, CI/CD automation and cloud transformation.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------
# MAIN CONTENT
# -------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="card"><h3>About</h3>'
    'Rajat Mahajan is a DevOps leader with 14+ years of experience '
    'in cloud automation, infrastructure design and scalable systems.'
    '</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>Experience</h3>'
    '<b>PwC</b> – DevOps Manager<br>'
    '<b>Nagarro</b> – DevOps Lead<br>'
    '<b>Accenture</b> – Sr Software Engineer<br>'
    '<b>Wipro</b> – Consultant<br>'
    '<b>HCL</b> – Analyst'
    '</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>Skills</h3>'
    'AWS<br>GCP<br>Terraform<br>Kubernetes<br>Docker<br>Jenkins'
    '</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>Education</h3>'
    'B.Tech – Computer Science<br>GGSIPU Delhi'
    '</div>', unsafe_allow_html=True)

# -------------------------
# FLOATING CHATBOT
# -------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    st.subheader("AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.write(f"**{msg['role']}**: {msg['content']}")

    user_input = st.text_input("Ask about Rajat")

    if user_input:
        st.session_state.messages.append(
            {"role": "You", "content": user_input}
        )

        # Replace with your RAG answer
        answer = "AI response will appear here."

        st.session_state.messages.append(
            {"role": "AI", "content": answer}
        )

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
