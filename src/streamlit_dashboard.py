import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "https://phishing-detector-ketf.onrender.com")

st.set_page_config(
    page_title="Phishing Detector",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Phishing Detection Dashboard")
st.markdown("### Analyze URLs, Emails, and HTML for phishing attempts")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_endpoint = st.text_input("API Endpoint", value=API_URL, help="Enter your FastAPI backend URL")
    st.markdown("---")
    st.markdown("**About**")
    st.info("This dashboard uses machine learning to detect phishing attempts in URLs, emails, and HTML content.")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 URL Analysis")
    url = st.text_input("Enter URL:", placeholder="https://example.com")

with col2:
    st.subheader("📧 Email Analysis")
    email_text = st.text_area("Email content:", height=100, placeholder="Paste email content here...")

st.subheader("📄 HTML Analysis")
html = st.text_area("HTML code:", height=150, placeholder="Paste HTML code here...")

if st.button("🔍 Analyze for Phishing", type="primary", use_container_width=True):
    if not url and not email_text and not html:
        st.warning("⚠️ Please provide at least one input (URL, email, or HTML)")
    else:
        with st.spinner("Analyzing..."):
            try:
                payload = {"url": url, "email_text": email_text, "html": html}
                response = requests.post(f"{api_endpoint}/predict", json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    if isinstance(result, dict):
                        if result.get("is_phishing", False):
                            st.error(f"🚨 **PHISHING DETECTED!**")
                            st.markdown(f"**Confidence:** {result.get('confidence', 'N/A')}")
                        else:
                            st.success(f"✅ **LEGITIMATE**")
                            st.markdown(f"**Confidence:** {result.get('confidence', 'N/A')}")
                        
                        # Show additional details if available
                        if "details" in result:
                            with st.expander("📊 View Details"):
                                st.json(result["details"])
                    else:
                        st.success(result)
                else:
                    st.error(f"❌ Error: API returned status code {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to API at {api_endpoint}")
                st.info("💡 Make sure your FastAPI backend is running or update the API endpoint in the sidebar.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with Streamlit • Protected by ML 🛡️</p>
    </div>
    """,
    unsafe_allow_html=True
)