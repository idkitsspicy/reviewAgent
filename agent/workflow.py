from reviews.fetch_live import get_live_reviews
from reviews.classify import classify_review
from reviews.respond import generate_response
from firebase_config import db
from reviews.reply_live import post_reply
from reviews.detect_language import detect_language_style
from reviews.memory_engine import get_memory_profile


def save_review(review_id, text, rating, intent, response, account_id,status):
    safe_review_id = review_id.replace("/", "_")

    db.collection("reviews").document(safe_review_id).set({
        "doc_id": safe_review_id,
        "review_id": review_id,
        "account_id": account_id,
        "text": text,
        "rating": rating,
        "intent": intent,
        "response": response,
        "status": status
    })


def run_live_agent(profile_id):
    reviews = get_live_reviews(profile_id)

    results = []

    for r in reviews.get("data", []):
        review_id = r["id"]
        text = r["text"]
        rating = r["rating"]
        intent = classify_review(text)
        language_style = detect_language_style(text)
        memory = get_memory_profile(profile_id)
        if rating >= 4:
            tone = "friendly"
        else:
            tone = "apologetic"

        response = generate_response(
            text,
            tone=tone,
            intent=intent,
            language_style=language_style,
            memory=memory
        )
        mode = get_business_mode(profile_id)
        if mode == "smart_auto":
          if rating >= 4:
           post_reply(review_id, profile_id, response)
           status = "approved"
          else:
           status = "draft"
        else:
           status = "draft"
        post_reply(review_id, profile_id, response)
        save_review(
            review_id,
            text,
            rating,
            intent,
            response,
            profile_id,
            status
        )

        results.append({
            "review_id": review_id,
            "review": text,
            "rating": rating,
            "intent": intent,
            "response": response
        })

    return results

def get_business_mode(profile_id):
    doc = db.collection("business_profiles").document(profile_id).get()

    if doc.exists:
        return doc.to_dict().get("automation_mode", "approval")

    return "approval"
