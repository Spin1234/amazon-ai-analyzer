from groq import Groq
import json
import re
import os

## client = Groq(api_key="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")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 Call Groq API
def call_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ✅ Updated working model
            messages=[
                {"role": "system", "content": "You are an expert Amazon business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content

        # 🔍 DEBUG (IMPORTANT - run once)
        print("\n=== GROQ RAW OUTPUT ===\n", output, "\n======================\n")

        return output

    except Exception as e:
        print("Groq Error:", e)
        return "{}"


# 🔥 FIXED JSON PARSER (MAIN ISSUE)
def safe_json_parse(text):
    try:
        # Extract JSON even if extra text exists
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("JSON Parse Error:", e)

    # fallback (so UI doesn't break)
    return {
    "purchase_criteria": ["No data"],
    "drivers": ["No data"],
    "pain_points": ["No data"],
    "recommendations": ["No data"],
    "marketing_angles": ["No data"]
}


# 🔹 PRODUCT INSIGHTS
def generate_product_insights(title, reviews, keywords):

    # handle empty reviews
    if not reviews:
        reviews = ["Good product", "Average quality", "Could be better"]

    reviews_sample = reviews[:25]

    prompt = f"""
You MUST return ONLY valid JSON.
No explanation. No extra text.

Analyze this Amazon product deeply.

Focus on REAL customer buying behavior.

Title: {title}
Keywords: {keywords}
Reviews: {reviews_sample}

IMPORTANT:
Identify the KEY PURCHASE CRITERIA:
- What factors customers consider BEFORE buying
- What influences their decision most

Return EXACT JSON format:

{{
 "purchase_criteria": [
  "Clear buying factor 1",
  "Clear buying factor 2",
  "Clear buying factor 3"
 ],
 "drivers": [
  "Positive reason 1",
  "Positive reason 2"
 ],
 "pain_points": [
  "Customer complaint 1",
  "Customer complaint 2"
 ],
 "recommendations": [
  "What to improve 1",
  "What to improve 2"
 ],
 "marketing_angles": [
  "How to sell better 1",
  "How to sell better 2"
 ]
}}
"""

    output = call_groq(prompt)
    return safe_json_parse(output)


# 🔹 COMPETITOR ANALYSIS
def competitor_analysis(data):

    prompt = f"""
You MUST return ONLY valid JSON.
No extra text.

Compare:

{data}

Return:

{{
 "gap_opportunities": ["..."],
 "winning_strategy": ["..."],
 "common_weakness": ["..."]
}}
"""

    output = call_groq(prompt)
    parsed = safe_json_parse(output)

    if not parsed:
        return {
            "gap_opportunities": ["No data"],
            "winning_strategy": ["No data"],
            "common_weakness": ["No data"]
        }

    return parsed


# 🔹 LISTING GENERATOR
def generate_listing(title, insights):

    prompt = f"""
You MUST return ONLY valid JSON.

Create high-converting Amazon listing.

Product: {title}
Insights: {insights}

Return:

{{
 "title": "...",
 "bullets": ["...", "...", "..."]
}}
"""

    output = call_groq(prompt)
    parsed = safe_json_parse(output)

    if "title" not in parsed:
        return {"title": "No title generated", "bullets": []}

    return parsed