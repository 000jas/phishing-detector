# Phishing Detector - Streamlit Deployment Guide

This repository contains a phishing detection system with a Streamlit dashboard.

## 🚀 Deployed App

Access the live dashboard: [Your App URL will be here]

## 📋 Features

- **URL Analysis**: Detect phishing attempts in URLs
- **Email Analysis**: Analyze email content for phishing indicators
- **HTML Analysis**: Check HTML code for malicious patterns
- **Real-time Detection**: Powered by machine learning models

## 🛠️ Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run src/streamlit_dashboard.py
```

3. Run the FastAPI backend (optional for full functionality):
```bash
uvicorn src.api_fastapi:app --reload
```

## 🌐 Configuration

Set the `API_URL` environment variable to point to your FastAPI backend:
```bash
export API_URL=https://your-api-endpoint.com
```

## 📦 Deployment

This app is configured for deployment on Streamlit Community Cloud.
