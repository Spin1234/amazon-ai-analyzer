from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from scraper import get_product_data, get_reviews
from analyzer import analyze
from revenue import estimate_revenue
from groq_ai import generate_product_insights, competitor_analysis, generate_listing
from utils import calculate_score, extract_asin


app = Flask(__name__)

def process_product(url):
    asin = extract_asin(url)
    if not asin:
        return None

    data = get_product_data(url)
    reviews = get_reviews(asin)

    analysis = analyze(reviews)
    sales, revenue, bsr = estimate_revenue(data["price"] or "0", data["bsr"])

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

        # 🔹 Process YOUR product
        main_product = process_product(main_url)

        # 🔹 Process competitors
        competitors = []
        for url in competitor_urls:
            url = url.strip()
            if not url:
                continue

            result = process_product(url)
            if result:
                competitors.append(result)

        # 🔥 AI Comparison
        comp_analysis = competitor_analysis({
            "your_product": main_product,
            "competitors": competitors
        })

        return render_template(
            "result.html",
            main=main_product,
            competitors=competitors,
            comp=comp_analysis
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)