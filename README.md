# Power Pages AI Knowledge Portal

A customer/partner portal with AI-powered knowledge search over governed content: answers come with citations and a confidence score — and when the model isn't confident, it escalates to a ticket instead of hallucinating.

## When to use this

Portals expose static FAQs, but users still open tickets for answers buried in documents. This repo gives you the portal blueprint (Power Pages web roles, table permissions, auth) plus a companion search API that answers from approved Dataverse content, cites its sources, and knows when to say "I don't know — opening a ticket."

## How it works

1. **Search** — `POST /search` with `{"query": "..."}`.
2. **Retrieve** — `_retrieve()` finds the best matching article. (Starter: deterministic lookup —
   in production this is hybrid search over published Dataverse articles with ACL filtering.)
3. **Confidence gate** — if confidence is below `0.6`, the response sets `suggest_ticket: true`
   instead of presenting a weak answer as fact.
4. **Cache** — `src/cache.py` provides a 300-second TTL cache so repeat questions don't re-run retrieval.
5. **Power Pages renders it** — see `docs/ARCHITECTURE.md` for the portal blueprint: web roles,
   table permissions on the articles table, auth, and the content approval workflow that keeps
   the knowledge base governed.

## Project structure

```
src/main.py        FastAPI service: POST /search
src/cache.py       Tiny TTL cache for search responses (300s)
docs/ARCHITECTURE.md   Portal blueprint: web roles, table permissions, auth, analytics
docs/ADR-001.md        Why the confidence gate exists
Dockerfile           Container image
.github/workflows/ci.yml   CI on every push
```

## Prerequisites

- Python 3.11+

## Quickstart

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Ask a question the knowledge base can answer:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -d '{
  "query": "How do I reset my password?"
}'
```

Expected response:

```json
{
  "answer": "Use the self-service reset link on the login page.",
  "citations": [{"article": "Password reset", "url": "/articles/password-reset"}],
  "confidence": 0.9,
  "cached": false
}
```

Now ask something it can't answer — watch the confidence gate kick in:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -d '{
  "query": "What is the meaning of life?"
}'
```

Expected response:

```json
{
  "answer": "I could not find a confident answer; opening a ticket is recommended.",
  "citations": [],
  "confidence": 0.3,
  "suggest_ticket": true,
  "cached": false
}
```

Repeat the first query and `"cached": true` comes back — the TTL cache working.

## Running the tests / CI

Every push runs the test suite via `.github/workflows/ci.yml`. Run it locally:

```bash
python -m pytest  # add tests/ as the suite grows
```

## Deploy with Docker

```bash
docker build -t knowledge-portal .
docker run -p 8000:8000 knowledge-portal
```

## Taking this to production

- Replace `_retrieve()` with hybrid search (BM25 + vectors) over published Dataverse articles, filtered by the caller's web role ACLs.
- Track analytics: top queries, zero-result rate, and ticket-deflection estimate — the metrics that justify the portal.
- Swap the in-memory cache for Redis with per-article TTLs tied to the content approval workflow.

## Further reading

- `docs/ARCHITECTURE.md` — portal blueprint: web roles, table permissions, auth, analytics
- `docs/ADR-001.md` — why the confidence gate exists
