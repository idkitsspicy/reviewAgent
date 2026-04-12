from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
def get_stats():
    return {
        "response_rate": "72%",
        "avg_rating": 4.3,
        "top_issue": "slow service"
    }
