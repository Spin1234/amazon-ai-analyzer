from groq import Groq
import json
import os
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return res.choices[0].message.content


def safe_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        pass
    return {}


def generate_product_insights(title, reviews, keywords):

    prompt = f"""
Return ONLY JSON.

Title: {title}
Reviews: {reviews[:10]}
Keywords: {keywords}

{
"purchase_criteria": [],
"drivers": [],
"pain_points": [],
"recommendations": [],
"marketing_angles": []
}
"""

    return safe_json(call_groq(prompt))


def competitor_analysis(data):

    prompt = f"""
Return ONLY JSON.

Compare:
{data}

{
"gap_opportunities": [],
"winning_strategy": [],
"common_weakness": []
}
"""

    return safe_json(call_groq(prompt))


def generate_listing(title, insights):

    prompt = f"""
Return ONLY JSON.

Product: {title}
Insights: {insights}

{
"title": "",
"bullets": []
}
"""

    return safe_json(call_groq(prompt))
