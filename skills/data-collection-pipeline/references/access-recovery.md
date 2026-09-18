# Access Recovery Playbook

Use this reference only after a collection path is blocked, incomplete, or misleading.

## 1. Classify the observed failure

Capture the actual state before choosing recovery:

- `401` or explicit login challenge -> authentication-gated entry point;
- `403` -> access denied / anti-bot / policy restriction at that route;
- `404` or `410` -> stale or removed route;
- `429` -> rate-limited route;
- redirect to login/home/error -> route indirection or gated session;
- HTML returned for an expected PDF/ZIP -> likely wrapper, error page, or generated-link flow;
- search UI returns nothing -> discovery failure, not absence proof.

Preserve the original URL, final URL, status, and content type when possible.

## 2. Recovery lane A: alternate sources

Search for the same publication identity through other authoritative or provenance-preserving channels:

- official ministry/agency subdomains;
- public procurement/open-data portals;
- official attachment/CDN hosts;
- regulator or local-government mirrors;
- institutional archives;
- secondary mirrors only when authoritative provenance remains traceable.

Match on stable identifiers where available: notice number, project number, document title, issuing authority, date, attachment filename, or checksum.

## 3. Recovery lane B: same-site alternate entries

Search the original domain rather than repeatedly retrying the blocked URL:

- site search and domain-scoped web search;
- category/list/index pages;
- notice detail pages adjacent to the blocked route;
- attachment links embedded in accessible HTML;
- predictable static-file or CDN paths visible from neighboring pages;
- public JSON/API endpoints used by the accessible frontend;
- alternate mobile/legacy/public views when they are official and stable.

The point is not to bypass authentication controls. It is to discover whether the same public material has another legitimate public route.

## 4. Convergence rule

Stop widening the search when one of these is true:

- the declared corpus boundary and diversity target are satisfied with frozen, verified artifacts;
- both recovery lanes have produced independent evidence that a required source remains inaccessible;
- proceeding would require credentials, circumvention, or a new authority decision outside the task.

Record the stopping reason. Do not substitute "search blocked" for "source unavailable."
