# Phishing Detection System (Multi-Modal ML)

## Overview

This project implements a **phishing detection system** using a **multi-modal machine learning approach**. It analyzes **URLs**, **email text**, and **HTML content** to classify inputs as **phishing** or **legitimate**.

The system includes:
- Data preprocessing
- Feature extraction
- Model training
- A **FastAPI** backend for real-time predictions
- A **Streamlit** dashboard for user interaction
- **Explainable AI (SHAP)** for model transparency

---

## Features
- Accurate Detection
- URL, Email, and HTML feature extraction  
- Random Forest–based phishing classification  
- Real-time prediction using FastAPI  
- Interactive UI using Streamlit  
- Explainable ML support (SHAP)

---

## Demo Video

*(Add link here)*

---

## Project Structure
```
phishing-detector/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── dataset.csv
│
├── src/
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── feature_url.py
│   ├── feature_email.py
│   ├── feature_html.py
│   ├── multimodal_feature_builder.py
│   ├── train_ml.py
│   ├── train_dl.py
│   ├── api_fastapi.py
│   ├── streamlit_dashboard.py
│   ├── explainability.py
│   └── utils.py
│
├── model/
│   └── rf_model.pkl
│
└── README.md
```

⸻

Dataset Format

The dataset must be a CSV file with the following columns:

url,email_text,html,label

	•	url – Website URL
	•	email_text – Email content (can be empty)
	•	html – HTML page content
	•	label – Target class
	•	1 → Phishing
	•	0 → Legitimate

Model Used
	•	Random Forest Classifier
	•	Supervised binary classification
	•	Chosen for robustness, non-linearity handling, and explainability

⸻

Explainability

SHAP is used to explain feature importance and model predictions for transparency.

⸻

Future Improvements
	•	Integrate deep learning models fully
	•	Add browser-level phishing detection
	•	Improve real-time HTML fetching

⸻

Author

# Ojas Dhapse
# github: 000jas
