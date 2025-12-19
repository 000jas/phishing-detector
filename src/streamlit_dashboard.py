import streamlit as st
import requests

st.title("Phishing Detection Dashboard")

url = st.text_input("Enter URL:")
email_text = st.text_area("Email content:")
html = st.text_area("HTML code:")

if st.button("Analyze"):
    payload = {"url": url, "email_text": email_text, "html": html}
    result = requests.post("http://localhost:8000/predict", json=payload).json()
    st.success(result)