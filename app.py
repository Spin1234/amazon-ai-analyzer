from flask import Flask, render_template, request
from scraper import get_product_data, get_reviews
from analyzer import analyze
from revenue import estimate_revenue
from groq_ai import generate_product_insights, competitor_analysis, generate_listing
from utils import extract_asin, calculate_score

app = Flask(__name__)


def process_product(url):
    print("INPUT URL:", url)

    asin = extract_asin(url)
    print("EXTRACTED ASIN:", asin)

    if not asin:
        return {
            "title": "Invalid Product URL",
            "price": "0",
            "sales": 0,
            "revenue": 0,
            "sentiment": 0,
            "keywords": [],
            "insights": {},
            "listing": {},
            "score": 0
        }

    data = get_product_data(url)
    print("SCRAPED DATA:", data)

    reviews = get_reviews(asin)

    analysis = analyze(reviews)

    sales, revenue, bsr = estimate_revenue(data["price"], data["bsr"])

    insights = generate_product_insights(data["title"], reviews, analysis["keywords"])

    listing = generate_listing(data["title"], insights)

    score = calculate_score(analysis["sentiment"], bsr)

    return {
        "title": data["title"],
        "price": data["price"],
        "sales": sales,
        "revenue": revenue,
        "sentiment": analysis["sentiment"],
        "keywords": analysis["keywords"],
        "insights": insights,
        "listing": listing,
        "score": score
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        main_url = request.form.get("main_url")
        competitor_urls = request.form.get("competitor_urls").split("\n")

        main_product = process_product(main_url)

        competitors = []
        for url in competitor_urls:
            url = url.strip()
            if url:
                competitors.append(process_product(url))

        comp = competitor_analysis({
            "your_product": main_product,
            "competitors": competitors
        })

        return render_template("result.html",
                               main=main_product,
                               competitors=competitors,
                               comp=comp)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)