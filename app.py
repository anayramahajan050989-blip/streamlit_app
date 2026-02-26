import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from docx import Document

st.set_page_config(page_title="Rajat Mahajan", layout="wide")

# -----------------------------
# Bright UI
# -----------------------------
st.markdown("""
<style>

.main {
background: linear-gradient(120deg,#ffecd2,#fcb69f);
}

.hero {
padding:40px;
border-radius:20px;
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
margin-bottom:25px;
}

.card {
padding:25px;
border-radius:18px;
background: linear-gradient(135deg,#43e97b,#38f9d7);
margin-bottom:20px;
box-shadow:0px 10px 25px rgba(0,0,0,0.15);
}

section[data-testid="stSidebar"] {
width:420px;
background: linear-gradient(180deg,#667eea,#764ba2);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# OpenAI
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Load Resume
# -----------------------------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text)
    return "\n".join(text)

resume_text = load_resume()

# -----------------------------
# Chunking
# -----------------------------
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

chunks = chunk_text(resume_text)

# -----------------------------
# Embeddings
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# -----------------------------
# Vector Search
# -----------------------------
@st.cache_resource
def build_index(chunks):
    embeddings = model.encode(chunks)
    nn = NearestNeighbors(n_neighbors=4, metric="cosine")
    nn.fit(embeddings)
    return nn

vector_db = build_index(chunks)

# -----------------------------
# Retrieval
# -----------------------------
def retrieve_context(query):
    query_vec = model.encode([query])
    distances, indices = vector_db.kneighbors(query_vec, n_neighbors=4)
    return "\n\n".join([chunks[i] for i in indices[0]])

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>AI Powered Portfolio</h3>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Website Content
# -----------------------------
st.markdown("## About")
st.markdown(f'<div class="card">{resume_text[:1500]}</div>', unsafe_allow_html=True)

st.markdown("## Experience")
st.markdown(f'<div class="card">{resume_text[1500:3000]}</div>', unsafe_allow_html=True)

st.markdown("## Skills")
st.markdown(f'<div class="card">{resume_text[3000:4500]}</div>', unsafe_allow_html=True)

# -----------------------------
# CHATBOT (PROPER STREAMLIT FLOW)
# -----------------------------
st.sidebar.title("AI Resume Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render all messages FIRST
for msg in st.session_state.messages:
    with st.sidebar.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input always at bottom
prompt = st.sidebar.chat_input("Ask about Rajat Mahajan...")

if prompt:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate response
    context = retrieve_context(prompt)

    full_response = ""
    placeholder = st.sidebar.empty()

    stream = client.responses.stream(
        model="gpt-4o-mini",
        input=f"""
Answer questions about Rajat Mahajan using this resume context.

Context:
{context}

Question:
{prompt}
"""
    )

    with placeholder.container():
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            for event in stream:
                if event.type == "response.output_text.delta":
                    full_response += event.delta
                    message_placeholder.markdown(full_response)

    stream.close()

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

    st.rerun()
