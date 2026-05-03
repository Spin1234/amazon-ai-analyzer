import requests
from bs4 import BeautifulSoup

# HEADERS = {
#     "User-Agent": "Mozilla/5.0",
#     "Accept-Language": "en-US,en;q=0.9"
# }

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
}


def get_product_data(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.content, "lxml")

        title_tag = soup.select_one("#productTitle")
        price_tag = soup.select_one(".a-price-whole")

        title = title_tag.get_text(strip=True) if title_tag else "Not Found"
        price = price_tag.get_text(strip=True) if price_tag else "0"

        bsr = None
        for li in soup.select("#detailBulletsWrapper_feature_div li"):
            if "Best Sellers Rank" in li.text:
                bsr = li.text.strip()

        print("TITLE:", title)

        return {
            "title": title,
            "price": price,
            "bsr": bsr
        }

    except Exception as e:
        print("SCRAPER ERROR:", e)
        return {
            "title": "Error",
            "price": "0",
            "bsr": None
        }


def get_reviews(asin):
    if not asin:
        return ["No reviews available"]

    try:
        url = f"https://www.amazon.in/product-reviews/{asin}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.content, "lxml")

        reviews = []
        for r in soup.select(".review-text-content span"):
            reviews.append(r.text.strip())

        return reviews if reviews else ["No reviews found"]

    except:
        return ["No reviews available"]
