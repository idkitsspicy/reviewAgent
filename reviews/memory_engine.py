from firebase_config import db
from reviews.detect_language import detect_language_style


def update_memory_profile(profile_id):
    docs = db.collection("edit_history") \
             .where("profile_id", "==", profile_id) \
             .stream()
    print("Running memory engine for:", profile_id)

    edits = [doc.to_dict() for doc in docs]

    if not edits:
        return

    emoji_count = 0
    short_count = 0
    language_styles = []

    for edit in edits:
        edited = edit["edited_response"]

        # Detect emoji preference
        if "😊" in edited or "🙏" in edited or "👍" in edited:
            emoji_count += 1

        # Detect short reply preference
        if len(edited.split()) <= 15:
            short_count += 1

        # Detect language preference
        language_style = detect_language_style(edited)
        language_styles.append(language_style)

    emoji_usage = emoji_count > len(edits) / 2
    reply_length = "short" if short_count > len(edits) / 2 else "normal"

    preferred_language = max(set(language_styles), key=language_styles.count)

    db.collection("business_memory").document(profile_id).set({
        "profile_id": profile_id,
        "preferred_tone": "warm casual",
        "emoji_usage": emoji_usage,
        "reply_length": reply_length,
        "language_preference": preferred_language
    })
def get_memory_profile(profile_id):
    doc = db.collection("business_memory").document(profile_id).get()

    if doc.exists:
        return doc.to_dict()

    return {
        "preferred_tone": "warm casual",
        "emoji_usage": False,
        "reply_length": "normal",
        "language_preference": "english"
    }