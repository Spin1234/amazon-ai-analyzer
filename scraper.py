# import requests
# from bs4 import BeautifulSoup
# import time

# HEADERS = {
#     "User-Agent": "Mozilla/5.0",
#     "Accept-Language": "en-US,en;q=0.9"
# }

# def safe(soup, selector):
#     tag = soup.select_one(selector)
#     return tag.get_text(strip=True) if tag else None


# def get_product_data(url):
#     res = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(res.content, "lxml")

#     title = safe(soup, "#productTitle")
#     price = safe(soup, ".a-price-whole")
#     rating = safe(soup, ".a-icon-alt")

#     bsr = None
#     for li in soup.select("#detailBulletsWrapper_feature_div li"):
#         if "Best Sellers Rank" in li.text:
#             bsr = li.text.strip()

#     return {
#         "title": title,
#         "price": price,
#         "rating": rating,
#         "bsr": bsr
#     }


# def get_reviews(asin, pages=3):
#     reviews = []

#     for page in range(1, pages + 1):
#         url = f"https://www.amazon.in/product-reviews/{asin}?pageNumber={page}"

#         res = requests.get(url, headers=HEADERS)
#         soup = BeautifulSoup(res.content, "lxml")

#         for r in soup.select(".review-text-content span"):
#             reviews.append(r.get_text(strip=True))

#         time.sleep(1)

#     return reviews







from playwright.sync_api import sync_playwright
import time


def get_product_data(url):
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        try:
            title = page.locator("#productTitle").inner_text()
        except:
            title = "Title not found"

        try:
            price = page.locator(".a-price span").first.inner_text()
        except:
            price = "0"

        try:
            rating = page.locator(".a-icon-alt").first.inner_text()
        except:
            rating = "0"

        try:
            bsr = page.locator("#detailBulletsWrapper_feature_div").inner_text()
        except:
            bsr = None

        browser.close()

        return {
            "title": title.strip(),
            "price": price.strip().replace("₹", "").replace(",", ""),
            "rating": rating,
            "bsr": bsr
        }


def get_reviews(asin, pages=3):
    reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(1, pages + 1):
            url = f"https://www.amazon.in/product-reviews/{asin}?pageNumber={i}"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)

            review_elements = page.locator(".review-text-content span").all()

            for r in review_elements:
                try:
                    reviews.append(r.inner_text())
                except:
                    continue

            time.sleep(1)

        browser.close()

    return reviews
