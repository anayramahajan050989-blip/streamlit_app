import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from docx import Document
import numpy as np

st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# Bright & Colorful UI
# ---------------------------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
    background-size: 400% 400%;
}

.main {
    background: linear-gradient(120deg,#ffecd2,#fcb69f);
}

h1 {
    font-size: 60px;
    font-weight: 800;
    background: linear-gradient(90deg,#ff0080,#7928ca,#2afadf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2 {
    color: #5f27cd;
}

.hero {
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(135deg,#667eea,#764ba2);
    color: white;
    margin-bottom: 30px;
}

.card {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg,#ff758c,#ff7eb3);
    color: white;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.card2 {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg,#43e97b,#38f9d7);
    color: black;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.card3 {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg,#fa709a,#fee140);
    color: black;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

section[data-testid="stSidebar"] {
    width: 380px;
    background: linear-gradient(180deg,#667eea,#764ba2);
}

.chat-title {
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# OpenAI
# ---------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------------------------------
# Load Resume
# ---------------------------------------------------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text)
    return "\n".join(text)

resume_text = load_resume()

# ---------------------------------------------------
# Chunking
# ---------------------------------------------------
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

chunks = chunk_text(resume_text)

# ---------------------------------------------------
# Embedding Model
# ---------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# ---------------------------------------------------
# Vector DB
# ---------------------------------------------------
@st.cache_resource
def build_index(chunks):
    embeddings = model.encode(chunks)
    nn = NearestNeighbors(n_neighbors=4, metric="cosine")
    nn.fit(embeddings)
    return nn, embeddings

vector_db, embeddings = build_index(chunks)

# ---------------------------------------------------
# Retrieve context
# ---------------------------------------------------
def retrieve_context(query):
    query_vec = model.encode([query])
    distances, indices = vector_db.kneighbors(query_vec, n_neighbors=4)
    return "\n\n".join([chunks[i] for i in indices[0]])

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>DevOps Engineer | Cloud | Automation | AI Enthusiast</h3>
<p>This is an AI-powered interactive portfolio website.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# About Section
# ---------------------------------------------------
st.markdown("## About Rajat")

st.markdown(f"""
<div class="card">
{resume_text[:1200]}
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Experience Section
# ---------------------------------------------------
st.markdown("## Experience")

st.markdown(f"""
<div class="card2">
{resume_text[1200:2400]}
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Skills Section
# ---------------------------------------------------
st.markdown("## Skills & Technologies")

st.markdown(f"""
<div class="card3">
{resume_text[2400:3600]}
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Chatbot Sidebar
# ---------------------------------------------------
st.sidebar.markdown(
    '<div class="chat-title">🤖 AI Resume Assistant</div>',
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.sidebar.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

prompt = st.sidebar.chat_input("Ask about Rajat...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    context = retrieve_context(prompt)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are an AI assistant answering questions about Rajat Mahajan.

Resume Context:
{context}

Question:
{prompt}

Provide a clear professional answer.
If not found in resume, say you don't have that information.
"""
    )

    answer = response.output_text

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()
