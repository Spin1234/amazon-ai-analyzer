from textblob import TextBlob

def analyze(reviews):
    sentiments = []

    for r in reviews:
        sentiments.append(TextBlob(r).sentiment.polarity)

    avg = sum(sentiments)/len(sentiments) if sentiments else 0

    return {
        "sentiment": avg,
        "keywords": reviews[:5]
    }
