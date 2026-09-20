from fastapi import FastAPI
from pydantic import BaseModel
from .cache import get, set

app = FastAPI(title="Knowledge Portal Search API")

CONFIDENCE_THRESHOLD = 0.6

class SearchIn(BaseModel):
    query: str

def _retrieve(query: str) -> dict:
    # Production: hybrid search over published Dataverse articles with ACL filtering.
    q = query.lower()
    if "password" in q:
        return {"answer": "Use the self-service reset link on the login page.",
                "citations": [{"article": "Password reset", "url": "/articles/password-reset"}],
                "confidence": 0.9}
    return {"answer": "I could not find a confident answer; opening a ticket is recommended.",
            "citations": [], "confidence": 0.3}

@app.post("/search")
def search(req: SearchIn):
    cached = get(req.query)
    if cached:
        return {**cached, "cached": True}
    result = _retrieve(req.query)
    if result["confidence"] < CONFIDENCE_THRESHOLD:
        result["suggest_ticket"] = True
    set(req.query, result)
    return {**result, "cached": False}
