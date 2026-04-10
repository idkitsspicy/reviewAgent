from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import agent

app = FastAPI()
class ReviewRequest(BaseModel):
    review: str
    place_name: str
    language: str = "English"   # default

@app.post("/respond")
def respond(req: ReviewRequest):
    result = agent.run(
    f"""
    Review: {req.review}
    Place: {req.place_name}
    Language: {req.language}
    """
)
    return {"response": result}
