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
# CHATBOT STATE & UI
# -------------------------------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FLOATING BUTTON ---
# We use an empty container to inject the button into a fixed position via CSS
st.markdown("""
    <style>
    /* Target the specific button for floating */
    div.stButton > button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50px;
        z-index: 999;
        background-color: #7a5cff;
        color: white;
        border: none;
        box-shadow: 2px 5px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# This button stays fixed in the corner
if st.button("💬"):
    st.session_state.chat_open = not st.session_state.chat_open

# --- FLOATING CHAT WINDOW ---
if st.session_state.chat_open:
    # Use a container for the "Window" effect
    with st.container():
        st.markdown("""
            <div style="
                position: fixed; 
                bottom: 100px; 
                right: 30px; 
                width: 350px; 
                height: 500px; 
                background-color: white; 
                border-radius: 15px; 
                z-index: 1000; 
                box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                padding: 15px;
                border: 1px solid #eee;
            ">
                <h4 style="color: #333; margin-top: 0;">AI Assistant</h4>
                <hr style="margin: 10px 0;">
            </div>
        """, unsafe_allow_html=True)

        # To keep the chat interactive, we use a Sidebar for the actual input 
        # or a specific column. However, for a true "overlay," 
        # we'll use the main area with a vertical offset.
        
        # We'll use a sidebar for the chat to ensure it doesn't break page flow
        with st.sidebar:
            st.title("💬 Chat with Rajat's AI")
            st.info("Ask me anything about Rajat's experience or skills.")
            
            # Display chat messages
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            # Chat Input
            if prompt := st.chat_input("Ask a question..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)

                # RAG Logic
                context = retrieve_context(prompt)
                
                with st.chat_message("assistant"):
                    # Use your existing OpenAI streaming logic here
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": f"Answer based on context: {context}"},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    full_response = response.choices[0].message.content
                    st.write(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.rerun()
