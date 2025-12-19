import pandas as pd
from bs4 import BeautifulSoup

def clean_html(ht):
    try:
        return BeautifulSoup(ht, "lxml").get_text()
    except:
        return ""

def preprocess(input_csv="data/dataset.csv", output="data/processed/dataset_clean.csv"):
    # Try multiple encodings to handle various file formats
    encodings = ['utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(input_csv, encoding=encoding, on_bad_lines='skip')
            print(f"Successfully read file with encoding: {encoding}")
            break
        except (UnicodeDecodeError, Exception) as e:
            print(f"Failed with {encoding}: {str(e)[:50]}")
            continue
    
    if df is None:
        raise ValueError("Could not read CSV file with any supported encoding")
    
    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Fill NaN values with appropriate defaults
    if 'url' in df.columns:
        df['url'].fillna('', inplace=True)
    if 'text' in df.columns:
        df['text'].fillna('', inplace=True)
    if 'html' in df.columns:
        df['html'].fillna('', inplace=True)
    if 'label' in df.columns:
        df['label'].fillna(0, inplace=True)

    if 'url' in df.columns:
        df["url"] = df["url"].str.lower().str.strip()
    if 'html' in df.columns:
        df["clean_html"] = df["html"].apply(clean_html)
    df.to_csv(output, index=False)
    print("Pre-processed dataset saved:", output)
