from textblob import TextBlob
from collections import Counter
import re

def clean(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

def analyze(reviews):
    sentiments = []
    words = []

    for r in reviews:
        sentiments.append(TextBlob(r).sentiment.polarity)
        words.extend(clean(r).split())

    avg_sentiment = sum(sentiments)/len(sentiments) if sentiments else 0
    keywords = Counter(words).most_common(15)

    return {
        "sentiment": round(avg_sentiment, 2),
        "keywords": keywords
    }