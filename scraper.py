import requests
from bs4 import BeautifulSoup
import time

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

def safe(soup, selector):
    tag = soup.select_one(selector)
    return tag.get_text(strip=True) if tag else None


def get_product_data(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "lxml")

    title = safe(soup, "#productTitle")
    price = safe(soup, ".a-price-whole")
    rating = safe(soup, ".a-icon-alt")

    bsr = None
    for li in soup.select("#detailBulletsWrapper_feature_div li"):
        if "Best Sellers Rank" in li.text:
            bsr = li.text.strip()

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "bsr": bsr
    }


def get_reviews(asin, pages=3):
    reviews = []

    for page in range(1, pages + 1):
        url = f"https://www.amazon.in/product-reviews/{asin}?pageNumber={page}"

        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.content, "lxml")

        for r in soup.select(".review-text-content span"):
            reviews.append(r.get_text(strip=True))

        time.sleep(1)

    return reviews