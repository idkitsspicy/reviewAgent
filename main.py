
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from reviews.memory_engine import update_memory_profile
from firebase_config import db
from reviews.reply_live import post_reply
from reviews.memory_engine import get_memory_profile
from agent.workflow import run_live_agent

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    docs = db.collection("reviews").stream()

    reviews = []
    pending_count = 0
    auto_replied_count = 0

    for doc in docs:
        review = doc.to_dict()
        reviews.append(review)

        if review["status"] == "draft":
            pending_count += 1

        if review["status"] == "approved":
            auto_replied_count += 1

    # Fetch automation mode
    profile_doc = db.collection("business_profiles").document("69da50287dea335c2bd8718b").get()

    if profile_doc.exists:
        automation_mode = profile_doc.to_dict().get("automation_mode", "approval")
    else:
        automation_mode = "approval"

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "reviews": reviews,
            "pending_count": pending_count,
            "auto_replied_count": auto_replied_count,
            "automation_mode": automation_mode
        }
    )


# ==============================
# APPROVE REVIEW
# ==============================

@app.post("/approve/{doc_id}")
def approve_review(doc_id: str):
    doc_ref = db.collection("reviews").document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        review = doc.to_dict()

        # Post live reply
        post_reply(
            review["review_id"],
            review["account_id"],
            review["response"]
        )

        # Update Firestore status
        doc_ref.update({
            "status": "approved"
        })

    return RedirectResponse("/", status_code=303)


# ==============================
# edit REVIEW
# ==============================

@app.get("/edit/{doc_id}", response_class=HTMLResponse)
def edit_review_page(request: Request, doc_id: str):
    doc = db.collection("reviews").document(doc_id).get()

    if not doc.exists:
        return RedirectResponse("/", status_code=303)

    review = doc.to_dict()

    return templates.TemplateResponse(
        "edit_review.html",
        {
            "request": request,
            "review": review,
            "doc_id": doc_id
        }
    )
@app.post("/edit/{doc_id}")
def save_edited_review(doc_id: str, edited_response: str = Form(...)):
    doc_ref = db.collection("reviews").document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        review = doc.to_dict()

        original_response = review["response"]
        profile_id = "69da50287dea335c2bd8718b"

        # Save edit history
        db.collection("edit_history").add({
            "profile_id": profile_id,
            "review_id": review["review_id"],
            "original_response": original_response,
            "edited_response": edited_response
        })
        
        # Update review response
        doc_ref.update({
            "response": edited_response
        })
        print("Calling update_memory_profile now...")
        update_memory_profile(profile_id)

    return RedirectResponse("/", status_code=303)
#settings selection
@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    doc = db.collection("business_profiles").document("69da50287dea335c2bd8718b").get()

    if doc.exists:
        settings = doc.to_dict()
    else:
        settings = {"automation_mode": "approval"}

    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "settings": settings
        }
    )

@app.post("/settings")
def save_settings(automation_mode: str = Form(...)):
    db.collection("business_profiles").document("69da50287dea335c2bd8718b").set({
        "profile_id": "69da50287dea335c2bd8718b",
        "automation_mode": automation_mode
    })

    return RedirectResponse("/", status_code=303)

@app.post("/sync-reviews")
def sync_reviews():
    profile_id = "69da50287dea335c2bd8718b"

    run_live_agent(profile_id)

    return RedirectResponse("/", status_code=303)

@app.get("/onboarding", response_class=HTMLResponse)
def onboarding_page(request: Request):
    return templates.TemplateResponse(
        "onboarding.html",
        {"request": request}
    )
@app.post("/onboarding")
def save_onboarding(
    business_name: str = Form(...),
    email: str = Form(...),
    profile_id: str = Form(...),
    automation_mode: str = Form(...)
):
    db.collection("users").document(email).set({
        "business_name": business_name,
        "email": email,
        "profile_id": profile_id,
        "automation_mode": automation_mode
    })

    db.collection("business_profiles").document(profile_id).set({
        "profile_id": profile_id,
        "automation_mode": automation_mode
    })

    return RedirectResponse("/", status_code=303)

@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request):
    docs = db.collection("reviews").stream()
    reviews = [doc.to_dict() for doc in docs]

    total_reviews = len(reviews)

    positive_count = sum(
        1 for r in reviews if r["rating"] >= 4
    )

    negative_count = sum(
        1 for r in reviews if r["rating"] < 4
    )

    average_rating = (
        round(sum(r["rating"] for r in reviews) / total_reviews, 1)
        if total_reviews > 0 else 0
    )

    # Complaint frequency
    intents = [r["intent"] for r in reviews]
    most_common_intent = (
        max(set(intents), key=intents.count)
        if intents else "None"
    )

    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "total_reviews": total_reviews,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "average_rating": average_rating,
            "most_common_intent": most_common_intent
        }
    )
