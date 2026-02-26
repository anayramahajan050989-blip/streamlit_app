import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from docx import Document
import numpy as np

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="🚀",
    layout="wide"
)

# -------------------------
# OPENAI
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# STYLING
# -------------------------
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

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD RESUME
# -------------------------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text)
    return "\n".join(text)

resume_text = load_resume()

# -------------------------
# CHUNKING
# -------------------------
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

chunks = chunk_text(resume_text)

# -------------------------
# EMBEDDING MODEL
# -------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# -------------------------
# VECTOR STORE
# -------------------------
@st.cache_resource
def build_index(chunks):
    embeddings = model.encode(chunks)
    nn = NearestNeighbors(n_neighbors=4, metric="cosine")
    nn.fit(embeddings)
    return nn, embeddings

vector_db, embeddings = build_index(chunks)

# -------------------------
# RETRIEVAL
# -------------------------
def retrieve_context(query):
    query_vec = model.encode([query])
    distances, indices = vector_db.kneighbors(query_vec, n_neighbors=4)
    return "\n\n".join([chunks[i] for i in indices[0]])

# -------------------------
# HERO
# -------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>DevOps Manager • Cloud Architect • 14+ Years Experience</h3>
<p>
Expert in AWS, Kubernetes, Terraform, CI/CD automation and cloud transformation.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------
# MAIN CONTENT
# -------------------------
col1, col2 = st.columns([2,1])

with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About Rajat Mahajan")
    st.write("""
Rajat Mahajan is a seasoned DevOps Engineer and Manager with more than 14 years of experience 
in cloud infrastructure, automation, and enterprise DevOps transformation.

He has worked with organizations including PwC, Nagarro, Accenture, Wipro, and HCL.
His expertise includes AWS cloud architecture, Kubernetes deployments, CI/CD automation,
and infrastructure as code using Terraform.
""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Professional Experience")
    st.write("""
**PwC — DevOps Manager (2023 – Present)**  
Leading DevOps transformation and cloud automation initiatives.

**Nagarro — DevOps Lead (2019 – 2023)**  
Implemented CI/CD pipelines and AWS infrastructure automation.

**Accenture — Senior Software Engineer (2017 – 2019)**  
Cloud monitoring and AWS administration.

**Wipro — Consultant (2015 – 2017)**

**HCL — Analyst (2011 – 2015)**
""")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Key Skills")
    st.write("""
AWS  
GCP  
Terraform  
Kubernetes  
Docker  
Jenkins  
Datadog  
Splunk
""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Education")
    st.write("B.Tech Computer Science — GGSIPU Delhi")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CHATBOT SIDEBAR
# -------------------------
st.sidebar.title("AI Resume Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.sidebar.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.sidebar.chat_input("Ask about Rajat Mahajan")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.sidebar.chat_message("user"):
        st.write(prompt)

    context = retrieve_context(prompt)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
Answer the question about Rajat Mahajan using the resume context below.

Context:
{context}

Question:
{prompt}

If the answer is not in the resume, say you don't have that information.
"""
    )

    answer = response.output_text

    with st.sidebar.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
