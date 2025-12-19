import requests, os, mailbox

def fetch_url_list(filename):
    with open(filename, "r") as f:
        return [u.strip() for u in f.readlines()]

def save_html(url, folder="data/raw/html/"):
    os.makedirs(folder, exist_ok=True)
    try:
        html = requests.get(url, timeout=10).text
        name = url.replace("http://", "").replace("https://", "").replace("/", "_")
        with open(f"{folder}/{name}.html", "w", encoding="utf-8") as f:
            f.write(html)
        return True
    except:
        return False

def collect_urls(url_file):
    urls = fetch_url_list(url_file)
    good, bad = 0, 0
    for url in urls:
        if save_html(url):
            good += 1
        else:
            bad += 1
    print("Downloaded:", good, "Failed:", bad)

def collect_emails(mbox_path, output="data/raw/emails/"):
    os.makedirs(output, exist_ok=True)
    box = mailbox.mbox(mbox_path)
    for i, msg in enumerate(box):
        with open(f"{output}/email_{i}.eml", "w") as f:
            f.write(str(msg))
