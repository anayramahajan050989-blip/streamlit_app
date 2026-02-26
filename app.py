import streamlit as st

st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# SAFE COLORFUL STYLING
# -----------------------------
st.markdown("""
<style>

.hero {
    background: linear-gradient(135deg,#4f46e5,#9333ea);
    padding: 35px;
    border-radius: 16px;
    color: white;
}

.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 18px;
}

.chat-wrapper {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 340px;
}

.chat-box {
    background: white;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>DevOps Manager • Cloud Architect • 14+ Years Experience</h3>
<p>Expert in AWS, Kubernetes, CI/CD automation and cloud migration.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# MAIN CONTENT
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About")
    st.write(
        """
        Rajat Mahajan is a DevOps leader with 14+ years of experience
        in cloud infrastructure, automation, and enterprise DevOps platforms.
        He has worked with organizations like PwC, Nagarro, Accenture,
        Wipro, and HCL.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Professional Experience")
    st.write("""
    **PwC — DevOps Manager (2023–Present)**  
    Leading DevOps strategy and cloud automation.

    **Nagarro — DevOps Lead (2019–2023)**  
    AWS infrastructure automation and CI/CD pipelines.

    **Accenture — Senior Software Engineer (2017–2019)**

    **Wipro — Consultant (2015–2017)**

    **HCL — Analyst (2011–2015)**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Skills")
    st.write("""
    AWS  
    GCP  
    Terraform  
    Kubernetes  
    Docker  
    Jenkins  
    Datadog
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Education")
    st.write("B.Tech Computer Science — GGSIPU Delhi")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FLOATING CHATBOT
# -----------------------------
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

st.write("### AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input (this prevents loops)
prompt = st.chat_input("Ask about Rajat Mahajan")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # ---- YOUR RAG SYSTEM HERE ----
    answer = "AI response will appear here."
    # replace with your OpenAI response
    # ------------------------------

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
