# Architecture

## Components
- Power Pages: public/authenticated pages, web roles, table permissions.
- Dataverse: knowledge articles with state (draft -> review -> published).
- Search API: retrieval over published articles, citations in every answer.
- Identity: Entra ID / B2C for external users.

## Key decisions
- Only `published` articles are searchable; drafts never leak.
- Table permissions enforce row-level access.
- Low-confidence answers suggest opening a ticket with context.

## Production hardening
- Add CDN, WAF, rate limiting, and search analytics.
