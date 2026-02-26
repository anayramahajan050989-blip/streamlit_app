import streamlit as st

st.set_page_config(
    page_title="Rajat Mahajan",
    page_icon="☁️",
    layout="wide"
)

# Header
st.title("Rajat Mahajan")
st.subheader("DevOps Engineer | Cloud Architect | 14+ Years Experience")

st.divider()

# About
st.header("About")
st.write(
"""
Experienced DevOps Engineer and Manager with over 14 years of experience
in cloud deployment, migration, automation, and infrastructure management.
Specialized in AWS, GCP, Kubernetes, and CI/CD automation.
"""
)

# Skills
st.header("Skills & Technologies")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Cloud")
    st.write("- AWS")
    st.write("- Google Cloud Platform")

with col2:
    st.subheader("DevOps Tools")
    st.write("- Terraform")
    st.write("- Jenkins")
    st.write("- Docker")
    st.write("- Kubernetes")

with col3:
    st.subheader("Monitoring")
    st.write("- Datadog")
    st.write("- Splunk")
    st.write("- OMi")

st.divider()

# Experience
st.header("Work Experience")

st.subheader("PwC (2023 – Present)")
st.write("DevOps Manager leading CI/CD, cloud automation, and Kubernetes deployments.")

st.subheader("Nagarro (2019 – 2023)")
st.write("DevOps Lead working on AWS infrastructure automation and cloud migration.")

st.subheader("Accenture (2017 – 2019)")
st.write("Senior Software Engineer handling monitoring and AWS administration.")

st.subheader("Wipro (2015 – 2017)")
st.write("Consultant working on monitoring and alerting systems.")

st.subheader("HCL (2011 – 2015)")
st.write("Analyst working on service assurance and automation.")

st.divider()

# Education
st.header("Education")
st.write("B.Tech (Computer Science) – GGSIPU, Delhi")

# Contact
st.header("Contact")
st.write("Email: rajatmahajan.89@gmail.com")
st.write("Phone: 8860511115")
