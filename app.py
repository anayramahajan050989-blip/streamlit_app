import streamlit as st
from openai import OpenAI
from docx import Document

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Rajat Mahajan", layout="wide")

# -------- Load Resume --------
@st.cache_data
def load_resume():
    doc = Document("Resume.docx")
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

resume_text = load_resume()

# -------- Website Content --------
st.title("Rajat Mahajan")
st.subheader("DevOps Engineer | Cloud Architect | 14+ Years Experience")

st.divider()

st.header("About")
st.write(
"""
Experienced DevOps Engineer specializing in AWS, GCP, Kubernetes,
CI/CD automation, and cloud migration.
"""
)

st.divider()

# -------- Chatbot Section --------
st.header("Ask about Rajat Mahajan")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_question = st.chat_input("Ask something about Rajat Mahajan...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.write(user_question)

    prompt = f"""
You are a helpful assistant answering questions about Rajat Mahajan.
Use the resume information below to answer accurately.
If the answer is not in the resume, say you don't have that information.

RESUME:
{resume_text}

QUESTION:
{user_question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer questions about Rajat Mahajan."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
