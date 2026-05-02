import re

def extract_asin(url):
    try:
        if not url:
            return None

        patterns = [
            r"/dp/([A-Z0-9]{10})",
            r"/gp/product/([A-Z0-9]{10})"
        ]

        for p in patterns:
            match = re.search(p, url)
            if match:
                return match.group(1)

        return None
    except:
        return None


def calculate_score(sentiment, bsr):
    score = 50

    if sentiment > 0.3:
        score += 20
    elif sentiment < 0:
        score -= 20

    if bsr:
        if bsr < 500:
            score += 20
        elif bsr > 5000:
            score -= 10

    return max(0, min(100, score))
