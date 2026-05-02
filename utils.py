import re
import requests

def extract_asin(url):
    try:
        res = requests.get(url, allow_redirects=True, timeout=5)
        final_url = res.url
    except:
        final_url = url

    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/product/([A-Z0-9]{10})"
    ]

    for p in patterns:
        match = re.search(p, final_url)
        if match:
            return match.group(1)

    return None


def calculate_score(sentiment, bsr):
    score = 50

    if sentiment > 0.5:
        score += 20
    elif sentiment < 0:
        score -= 20

    if bsr < 500:
        score += 20
    elif bsr > 5000:
        score -= 20

    return max(0, min(100, score))