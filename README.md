# Power Pages AI Knowledge Portal

Customer/partner portal with AI-powered knowledge search over governed content.

## Problem
Portals expose static FAQs; users still open tickets for answers hidden in documents.

## What it includes
- Power Pages portal blueprint: web roles, table permissions, auth
- AI search companion API with citations and confidence
- Dataverse as the content source with approval workflow
- Analytics: top queries, zero-result rate, ticket deflection estimate

## Architecture
See `docs/ARCHITECTURE.md`.

## Quickstart
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```
