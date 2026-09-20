from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Knowledge Portal Search API")

class SearchIn(BaseModel):
    query: str

@app.post("/search")
def search(req: SearchIn):
    # Production: vector/hybrid search over published Dataverse articles.
    return {
        "answer": "Blueprint answer: connect retrieval over published articles.",
        "citations": [{"article": "Getting started", "url": "/articles/getting-started"}],
        "confidence": "medium",
    }
