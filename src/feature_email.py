import re

SPAM_WORDS = ["account", "verify", "urgent", "login", "click", "update"]

def extract_email_features(text):
    text = text.lower()
    feats = {
        "word_count": len(text.split()),
        "link_count": len(re.findall(r"http[s]?://\S+", text)),
        "spam_word_count": sum(1 for w in SPAM_WORDS if w in text),
    }
    return feats
