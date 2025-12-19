import pandas as pd
from src.feature_url import extract_url_features
from src.feature_email import extract_email_features
from src.feature_html import extract_html_features

def build_features(df):
    rows = []

    for _, row in df.iterrows():
        features = {}
        
        # Extract URL features if column exists
        if "url" in row and pd.notna(row["url"]):
            features.update(extract_url_features(row["url"]))
        
        # Extract email/text features if column exists (supports both 'text' and 'email_text')
        text_col = "email_text" if "email_text" in row else "text"
        if text_col in row and pd.notna(row[text_col]):
            features.update(extract_email_features(row[text_col]))
        
        # Extract HTML features if column exists
        if "html" in row and pd.notna(row["html"]):
            features.update(extract_html_features(row["html"]))
        
        rows.append(features)

    return pd.DataFrame(rows)