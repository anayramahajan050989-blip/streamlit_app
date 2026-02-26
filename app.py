import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="Emerging Technologies & Consultancy",
                   page_icon="🚀",
                   layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
                        ["Home", "About Us", "Services", "Projects", "Contact"])

# ================= HOME =================
if page == "Home":
    st.title("🚀 Emerging Technologies & Consultancy")
    st.subheader("Innovating Today. Transforming Tomorrow.")

    st.write("""
    Welcome to Emerging Technologies & Consultancy.
    We specialize in delivering cutting-edge technology solutions
    for modern businesses.
    """)

    st.image("https://images.unsplash.com/photo-1519389950473-47ba0277781c",
             use_column_width=True)

# ================= ABOUT =================
elif page == "About Us":
    st.title("About Us")

    st.write("""
    Emerging Technologies & Consultancy is a forward-thinking firm
    focused on digital transformation, AI solutions, cloud computing,
    and strategic technology consulting.
    """)

    st.write("### Our Mission")
    st.write("To empower organizations with innovative and scalable technology solutions.")

    st.write("### Our Vision")
    st.write("To become a global leader in emerging technology consulting.")

# ================= SERVICES =================
elif page == "Services":
    st.title("Our Services")

    st.markdown("""
    - 🤖 Artificial Intelligence & Machine Learning  
    - ☁️ Cloud Solutions & DevOps  
    - 📊 Data Analytics & Business Intelligence  
    - 🔐 Cybersecurity Consulting  
    - 🌐 Web & Application Development  
    """)

# ================= PROJECTS =================
elif page == "Projects":
    st.title("Our Projects")

    st.write("""
    Here are some of our key solution areas:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("AI Automation Platform")
        st.write("Enterprise automation using AI-driven workflows.")

    with col2:
        st.subheader("Cloud Migration Suite")
        st.write("Helping enterprises transition securely to the cloud.")

# ================= CONTACT =================
elif page == "Contact":
    st.title("Contact Us")

    st.write("📍 Location: Your City, Your Country")
    st.write("📧 Email: info@emergingtechconsult.com")
    st.write("📞 Phone: +123 456 7890")

    st.write("### Send us a message")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

    if st.button("Submit"):
        st.success("Thank you! We will get back to you soon.")


components.html("""
<script type="module">
  import Chatbot from "https://cdn.jsdelivr.net/gh/FlowiseAI/FlowiseChatEmbed/dist/web.js"
  Chatbot.init({
      chatflowid: "ac2a29aa-def6-428c-9d74-0e58b18b67cd",
      apiHost: "http://localhost:3000",
  })
</script>
""", height=600)
