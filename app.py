import streamlit as st
from openai import OpenAI
from docx import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------
# Config
# -----------------------
st.set_page_config(page_title="Rajat Mahajan", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Free embedding model (very good + fast)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------
# Load resume
# -----------------------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text)
    return "\n".join(text)

resume_text = load_resume()

# -----------------------
# Chunking
# -----------------------
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(resume_text)

# -----------------------
# Embeddings
# -----------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(EMBED_MODEL)

embed_model = load_embedding_model()

@st.cache_resource
def create_vector_store(chunks):
    embeddings = embed_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings

index, embeddings = create_vector_store(chunks)

# -----------------------
# Retrieval
# -----------------------
def retrieve(query, top_k=4):
    query_embedding = embed_model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0]]
    return results

# -----------------------
# UI
# -----------------------
st.title("Rajat Mahajan")
st.subheader("AI Resume Assistant")

st.write("Ask anything about Rajat Mahajan's experience, skills, or career.")

st.divider()

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask about Rajat Mahajan...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    # Retrieve relevant chunks
    context_chunks = retrieve(question)
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant answering questions about Rajat Mahajan.
Use the provided resume context to answer accurately.

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    answer = response.output_text

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
