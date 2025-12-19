import re
from urllib.parse import urlparse
import tldextract

def extract_url_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    feats = {
        "url_length": len(url),
        "domain_length": len(ext.domain),
        "subdomain_count": len(ext.subdomain.split(".")) if ext.subdomain else 0,
        "digit_count": sum(c.isdigit() for c in url),
        "is_https": 1 if parsed.scheme == "https" else 0,
        "has_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0
    }
    return feats
