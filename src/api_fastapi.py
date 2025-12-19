from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os
import numpy as np
from urllib.parse import urlparse

app = FastAPI()

# Enable CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PredictionRequest(BaseModel):
    url: str
    email_text: str = ""
    html: str = ""

# Load model
model_path = "models/rf_model.pkl"
if not os.path.exists(model_path):
    print(f"Warning: Model file not found at {model_path}")
    model = None
else:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

def simple_url_features(url):
    """Enhanced phishing detection using multiple heuristics"""
    try:
        url_lower = url.lower()
        parsed = urlparse(url_lower)
        domain = parsed.netloc
        path = parsed.path
        
        risk_score = 0
        
        # 1. Suspicious keywords (banking, payment, verification)
        suspicious_keywords = [
            'paypal', 'bank', 'signin', 'login', 'verify', 'account', 
            'secure', 'update', 'confirm', 'password', 'billing', 'ebay',
            'amazon', 'apple', 'microsoft', 'google', 'facebook', 'netflix',
            'suspended', 'locked', 'unusual', 'alert', 'support-help'
        ]
        keyword_matches = sum(1 for word in suspicious_keywords if word in url_lower)
        if keyword_matches >= 2:
            risk_score += 3
        elif keyword_matches == 1:
            risk_score += 1
            
        # 2. Multiple domains in path (e.g., example.com/realbank.com/)
        if '/' in path and any(tld in path for tld in ['.com', '.net', '.org', '.co.uk', '.co.nz']):
            risk_score += 3
            
        # 3. IP address in URL
        ip_pattern = domain.replace('.', '').replace(':', '')
        if ip_pattern.isdigit() or any(c.isdigit() for c in domain.split('.')[0] if len(domain.split('.')[0]) > 0):
            if sum(c.isdigit() for c in domain) > len(domain) * 0.3:
                risk_score += 2
                
        # 4. Excessive subdomains
        subdomain_count = domain.count('.')
        if subdomain_count > 3:
            risk_score += 2
        elif subdomain_count > 2:
            risk_score += 1
            
        # 5. Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.link']
        if any(url_lower.endswith(tld) for tld in suspicious_tlds):
            risk_score += 2
            
        # 6. Excessive hyphens
        if domain.count('-') >= 3:
            risk_score += 2
        elif domain.count('-') >= 2:
            risk_score += 1
            
        # 7. Long URL
        if len(url) > 100:
            risk_score += 2
        elif len(url) > 75:
            risk_score += 1
            
        # 8. @ symbol in URL (often used in phishing)
        if '@' in url:
            risk_score += 3
            
        # 9. HTTPS but suspicious domain
        if url_lower.startswith('http://') and any(word in url_lower for word in ['secure', 'banking', 'paypal']):
            risk_score += 2
            
        # 10. Unusual port numbers
        if ':' in domain and any(port in domain for port in [':8080', ':8000', ':3000', ':5000']):
            risk_score += 1
            
        # 11. Blogspot, free hosting in financial context
        free_hosts = ['blogspot', 'wordpress', 'wixsite', 'weebly', 'tripod']
        if any(host in domain for host in free_hosts):
            if any(word in url_lower for word in ['paypal', 'bank', 'secure', 'account']):
                risk_score += 3
                
        # 12. Suspicious patterns
        if 'limited' in domain and any(num.isdigit() for num in domain):
            risk_score += 2
            
        # Classification threshold
        return 1 if risk_score >= 3 else 0
    except Exception as e:
        print(f"Error in url analysis: {e}")
        return 0

def analyze_text_content(text):
    """Analyze email/text content for phishing indicators"""
    if not text or len(text) < 10:
        return 0
        
    text_lower = text.lower()
    risk_score = 0
    
    # Spam/phishing keywords
    spam_keywords = [
        'urgent', 'winner', 'congratulations', 'free money', 'lottery', 
        'viagra', 'cialis', 'weight loss', 'enlarge', 'click here',
        'act now', 'limited time', 'expire', 'suspended account',
        'verify your account', 'confirm your identity', 'unusual activity',
        'security alert', 'your account will be closed', 'reset password',
        'prize', 'million dollars', 'inheritance', 'beneficiary',
        'toll-free', 'call now', 'click below', 'update payment'
    ]
    
    keyword_count = sum(1 for word in spam_keywords if word in text_lower)
    if keyword_count >= 3:
        risk_score += 3
    elif keyword_count >= 2:
        risk_score += 2
    elif keyword_count == 1:
        risk_score += 1
        
    # Excessive exclamation marks
    if text.count('!') > 3:
        risk_score += 1
        
    # ALL CAPS text (common in spam)
    words = text.split()
    caps_words = sum(1 for w in words if len(w) > 3 and w.isupper())
    if caps_words > len(words) * 0.3:
        risk_score += 2
        
    return risk_score

def analyze_html_content(html):
    """Analyze HTML content for phishing indicators"""
    if not html or len(html) < 10:
        return 0, False
        
    html_lower = html.lower()
    risk_score = 0
    has_password_field = False
    
    # Check for password input fields (CRITICAL - immediate phishing indicator)
    if 'type=\'password\'' in html_lower or 'type="password"' in html_lower or 'password' in html_lower:
        risk_score += 10  # Very high score
        has_password_field = True
        
    # Check for forms
    if '<form' in html_lower:
        risk_score += 1
        
    # Check for iframes (can be used to hide content)
    if '<iframe' in html_lower:
        risk_score += 2
        
    # Suspicious form actions
    suspicious_actions = ['submit', 'login', 'signin', 'verify', 'update']
    if any(action in html_lower for action in suspicious_actions):
        risk_score += 1
        
    # Hidden inputs (can be malicious)
    if 'type="hidden"' in html_lower or "type='hidden'" in html_lower:
        risk_score += 1
        
    # JavaScript suspicious patterns
    if '<script' in html_lower:
        if 'document.location' in html_lower or 'window.location' in html_lower:
            risk_score += 2
            
    return risk_score, has_password_field

@app.get("/")
def root():
    return {"status": "API is running", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        # Analyze all three components
        url_risk = simple_url_features(data.url)
        text_risk = analyze_text_content(data.email_text)
        html_risk, has_password = analyze_html_content(data.html)
        
        # Simple rule: If ANY component indicates phishing, classify as phishing
        
        # CRITICAL: If HTML contains password field, it's ALWAYS phishing
        if has_password:
            return {"prediction": "phishing"}
        
        # If URL is phishing
        if url_risk == 1:
            return {"prediction": "phishing"}
        
        # If text has ANY phishing indicators (text_risk >= 1)
        if text_risk >= 2:
            return {"prediction": "phishing"}
        
        # If HTML has significant phishing indicators
        if html_risk >= 3:
            return {"prediction": "phishing"}
        
        # Otherwise legitimate
        return {"prediction": "legitimate"}
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
