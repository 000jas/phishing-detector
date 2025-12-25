# Phishing Detector - Deployment Guide

This repository contains a phishing detection system with a Streamlit dashboard and FastAPI backend.

## 🚀 Deployed Apps

- **Frontend Dashboard**: [Deploy on Streamlit Cloud]
- **Backend API**: https://phishing-detector-ketf.onrender.com

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

## 📦 Deployment

### Deploy FastAPI Backend on Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository: `000jas/phishing-detector`
   - Choose the repository

3. **Configure Service**
   - **Name**: `phishing-detector-api`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api_fastapi:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** (Optional)
   - `PYTHON_VERSION`: `3.11.0`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Copy your API URL (e.g., `https://phishing-detector-api.onrender.com`)

### Deploy Streamlit Frontend on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Repository: `000jas/phishing-detector`
   - Branch: `main`
   - Main file path: `src/streamlit_dashboard.py`

3. **Configure Secrets** (Add your Render API URL)
   - In app settings → Secrets
   - Add:
   ```toml
   API_URL = "https://phishing-detector-ketf.onrender.com"
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes

## 🌐 Configuration

### Local Development
Set the `API_URL` environment variable to point to your FastAPI backend:
```bash
export API_URL=https://your-api-endpoint.com
streamlit run src/streamlit_dashboard.py
```

### Production
The Streamlit dashboard automatically reads the `API_URL` from environment variables or Streamlit secrets.

## 🔧 Troubleshooting

### Render Deployment Issues
- Check build logs for errors
- Ensure `requirements.txt` includes all dependencies
- Verify Python version compatibility

### Streamlit Deployment Issues
- Check app logs in Streamlit Cloud dashboard
- Verify API_URL is correctly set in secrets
- Test API endpoint separately before connecting

## 📝 Notes

- **Free Tier**: Both Render and Streamlit Cloud offer free tiers
- **Cold Starts**: Free tier services may sleep after inactivity
- **CORS**: The API is configured to allow all origins for browser access
