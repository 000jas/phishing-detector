from bs4 import BeautifulSoup

def extract_html_features(html):
    soup = BeautifulSoup(html, "lxml")

    feats = {
        "num_forms": len(soup.find_all("form")),
        "num_inputs": len(soup.find_all("input")),
        "num_pw_fields": len(soup.find_all("input", {"type": "password"})),
        "num_iframes": len(soup.find_all("iframe")),
        "num_scripts": len(soup.find_all("script"))
    }
    return feats
