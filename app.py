import streamlit as st

st.set_page_config(page_title="Rajat Mahajan", layout="wide")

html_code = """
<style>
body {
    font-family: Arial;
}
.header {
    background: #0a2540;
    color: white;
    padding: 30px;
    text-align: center;
    border-radius: 10px;
}
.card {
    background: #f5f7fa;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
}
</style>

<div class="header">
    <h1>Rajat Mahajan</h1>
    <p>DevOps Engineer | Cloud Architect | 14+ Years Experience</p>
</div>

<div class="card">
<h2>About</h2>
<p>Experienced DevOps Engineer and Manager specializing in AWS, GCP, Kubernetes, and CI/CD automation.</p>
</div>

<div class="card">
<h2>Skills</h2>
<ul>
<li>AWS, GCP</li>
<li>Terraform, Jenkins</li>
<li>Docker, Kubernetes</li>
<li>Git, Helm</li>
<li>Datadog, Splunk</li>
</ul>
</div>

<div class="card">
<h2>Experience</h2>
<ul>
<li>PWC – DevOps Manager (2023–Present)</li>
<li>Nagarro – DevOps Lead (2019–2023)</li>
<li>Accenture – Sr. Software Engineer (2017–2019)</li>
<li>Wipro – Consultant (2015–2017)</li>
<li>HCL – Analyst (2011–2015)</li>
</ul>
</div>

<div class="card">
<h2>Contact</h2>
<p>Email: rajatmahajan.89@gmail.com</p>
<p>Phone: 8860511115</p>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
