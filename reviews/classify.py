from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def classify_review(text):
    result = classifier(text)[0]
    
    if result['label'] == "NEGATIVE":
        return "complaint"
    elif result['label'] == "POSITIVE":
        return "praise"
    else:
        return "neutral"
