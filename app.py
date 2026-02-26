import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from docx import Document

st.set_page_config(page_title="Rajat Mahajan", layout="wide")

# -------------------------------------------------
# UI Styling
# -------------------------------------------------
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

/* Chat bubble */
.chat-button {
position: fixed;
bottom: 30px;
right: 30px;
width: 65px;
height: 65px;
border-radius: 50%;
font-size: 28px;
background: linear-gradient(135deg,#ff4ecd,#7a5cff);
color: white;
border: none;
box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
z-index: 1000;
}

/* Chat window */
.chat-window {
position: fixed;
bottom: 110px;
right: 30px;
width: 380px;
height: 520px;
background: white;
border-radius: 18px;
box-shadow: 0px 15px 40px rgba(0,0,0,0.25);
padding: 10px;
overflow: hidden;
z-index: 1000;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# OpenAI
# -------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------------------------
# Load Resume
# -------------------------------------------------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text)
    return "\n".join(text)

resume_text = load_resume()

# -------------------------------------------------
# Chunking
# -------------------------------------------------
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

chunks = chunk_text(resume_text)

# -------------------------------------------------
# Embedding model
# -------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# -------------------------------------------------
# Vector search
# -------------------------------------------------
@st.cache_resource
def build_index(chunks):
    embeddings = model.encode(chunks)
    nn = NearestNeighbors(n_neighbors=4, metric="cosine")
    nn.fit(embeddings)
    return nn

vector_db = build_index(chunks)

# -------------------------------------------------
# Retrieval
# -------------------------------------------------
def retrieve_context(query):
    query_vec = model.encode([query])
    distances, indices = vector_db.kneighbors(query_vec, n_neighbors=4)
    return "\n\n".join([chunks[i] for i in indices[0]])

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div class="hero">
<h1>Rajat Mahajan</h1>
<h3>AI Powered Portfolio</h3>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CONTENT
# -------------------------------------------------
st.markdown("## About")
st.markdown(f'<div class="card">{resume_text[:1500]}</div>', unsafe_allow_html=True)

st.markdown("## Experience")
st.markdown(f'<div class="card">{resume_text[1500:3000]}</div>', unsafe_allow_html=True)

st.markdown("## Skills")
st.markdown(f'<div class="card">{resume_text[3000:4500]}</div>', unsafe_allow_html=True)

# -------------------------------------------------
# CHATBOT STATE
# -------------------------------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# Chat bubble button
# -------------------------------------------------
col1, col2, col3 = st.columns([8,1,1])
with col3:
    if st.button("💬", key="chat_toggle"):
        st.session_state.chat_open = not st.session_state.chat_open

# -------------------------------------------------
# Chat window
# -------------------------------------------------
if st.session_state.chat_open:

    st.markdown('<div class="chat-window">', unsafe_allow_html=True)

    st.markdown("### AI Resume Assistant")

    # Show messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input (always last)
    prompt = st.chat_input("Ask about Rajat Mahajan")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        context = retrieve_context(prompt)

        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""

                stream = client.responses.stream(
                    model="gpt-4o-mini",
                    input=f"""
Answer questions about Rajat Mahajan using this resume.

Context:
{context}

Question:
{prompt}
"""
                )

                for event in stream:
                    if event.type == "response.output_text.delta":
                        full_response += event.delta
                        placeholder.markdown(full_response)

                stream.close()

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
