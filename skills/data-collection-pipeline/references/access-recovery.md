# Access Recovery Playbook

Use this reference only after a collection path is blocked, incomplete, or misleading.

## 1. Observe before escalating

Start the Crawlee acquisition pass with `retry_on_blocked=False`. Preserve the actual route outcome before attempting blocked-retry behavior.

Classify the observed state:

- `401` or explicit login challenge -> `AUTH_REQUIRED`; do not automatically enable blocked retry.
- `403` -> `ACCESS_DENIED_OR_BLOCKED`; may be access control, anti-bot behavior, or a bad entry route.
- `404` or `410` -> stale or removed route.
- `429` -> rate-limited route; honor `Retry-After` / backoff before escalation.
- redirect to login/home/error -> route indirection or gated session.
- HTML returned for an expected PDF/ZIP -> likely wrapper, error page, or generated-link flow.
- search UI returns nothing -> discovery failure, not absence proof.

Preserve the original URL, final URL, status, content type, and any stable source identifier when possible.

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

## 4. Bounded blocked-retry escalation

Only after the recovery lanes fail should the workflow consider a second transport attempt with `retry_on_blocked=True`.

Eligibility:

- `401`: not eligible by default. Authorized credentials or an explicit authenticated workflow are a separate path.
- `403`: eligible only when evidence supports a public-resource/session-or-bot-block interpretation rather than a permission boundary.
- `429`: eligible only after the server-requested or crawler-managed backoff has been respected.

The escalation must be bounded: use a small `max_session_rotations`, keep ordinary retries low, and record that `BLOCKED_RETRY` occurred. Do not silently add proxy rotation, credential guessing, CAPTCHA solving, or other access-control circumvention.

## 5. Convergence rule

Stop widening the search when one of these is true:

- the declared corpus boundary and diversity target are satisfied with frozen, verified artifacts;
- both recovery lanes and any eligible bounded blocked retry have failed with recorded evidence;
- proceeding would require credentials, circumvention, or a new authority decision outside the task.

Record the stopping reason. Do not substitute "search blocked" for "source unavailable."
