import streamlit as st

st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="☁️",
    layout="wide"
)

# ------------------------
# Custom Styling
# ------------------------
st.markdown("""
<style>
.hero {
    padding: 40px;
    border-radius: 14px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.card {
    padding: 25px;
    border-radius: 12px;
    background: #f8fafc;
    margin-bottom: 20px;
    border: 1px solid #e2e8f0;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 10px;
}

.chat-button {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background-color: #2563eb;
    color: white;
    padding: 14px 20px;
    border-radius: 50px;
    font-weight: bold;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.2);
    cursor: pointer;
    z-index: 999;
}

.chat-box {
    position: fixed;
    bottom: 90px;
    right: 25px;
    width: 360px;
    height: 420px;
    background: white;
    border-radius: 12px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.25);
    padding: 15px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# HERO SECTION
# ------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>DevOps Engineer • Cloud Architect • 14+ Years Experience</h3>
<p>
Experienced DevOps leader specializing in cloud deployment, infrastructure automation,
and scalable cloud architecture using AWS and GCP.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ------------------------
# MAIN CONTENT
# ------------------------
col1, col2 = st.columns([2, 1])

with col1:

    st.markdown('<div class="section-title">Career Summary</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="card">
Rajat Mahajan is a seasoned DevOps Engineer and Manager with over 14 years of
experience working with large enterprises and cloud-native platforms.

He has led multiple cloud transformation initiatives, automated CI/CD pipelines,
and built scalable infrastructure using modern DevOps tools.

Key Expertise:
• AWS & GCP Cloud Architecture  
• Infrastructure as Code (Terraform)  
• Kubernetes & Docker Deployments  
• CI/CD Pipeline Automation  
• Cloud Migration & Optimization  
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Professional Experience</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<b>PWC — DevOps Manager (2023 – Present)</b>
<ul>
<li>Leading cloud automation initiatives</li>
<li>Managing CI/CD strategy and deployment pipelines</li>
<li>Terraform-based infrastructure automation</li>
<li>Kubernetes deployments and monitoring</li>
</ul>

<b>Nagarro — DevOps Lead (2019 – 2023)</b>
<ul>
<li>Cloud migration and AWS infrastructure design</li>
<li>Automated deployments using Jenkins and Kubernetes</li>
<li>Security and code quality automation</li>
</ul>

<b>Accenture — Senior Software Engineer (2017 – 2019)</b>
<ul>
<li>Cloud monitoring systems</li>
<li>AWS administration and scripting</li>
</ul>

<b>Wipro — Consultant (2015 – 2017)</b>

<b>HCL — Analyst (2011 – 2015)</b>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Technical Skills</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<b>Cloud Platforms</b><br>
AWS, Google Cloud Platform

<br><br>

<b>DevOps Tools</b><br>
Terraform, Jenkins, Docker, Kubernetes, Helm, Git, Rancher

<br><br>

<b>Monitoring</b><br>
Datadog, Splunk, OMi, NNMi

<br><br>

<b>Programming</b><br>
Shell, YAML, JSON, Groovy
</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="card">
<h3>Quick Info</h3>
<b>Experience:</b> 14+ Years<br>
<b>Current Role:</b> DevOps Manager<br>
<b>Cloud:</b> AWS / GCP<br>
<b>Location:</b> India<br>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<h3>Education</h3>
B.Tech – Computer Science<br>
GGSIPU, Delhi
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<h3>Strengths</h3>
• Leadership<br>
• Problem Solving<br>
• Cloud Architecture<br>
• Automation
</div>
""", unsafe_allow_html=True)

# ------------------------
# FLOATING CHATBOT BUTTON
# ------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if st.button("💬 Ask AI", key="chat_btn"):
    st.session_state.chat_open = not st.session_state.chat_open

if st.session_state.chat_open:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    st.write("### AI Assistant")
    st.write("Ask anything about Rajat Mahajan")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.write(f"**{msg['role']}**: {msg['content']}")

    user_input = st.text_input("Your question")

    if user_input:
        st.session_state.messages.append({"role": "You", "content": user_input})

        # (Here you will plug your RAG chatbot code)
        answer = "AI response will appear here."

        st.session_state.messages.append({"role": "AI", "content": answer})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
