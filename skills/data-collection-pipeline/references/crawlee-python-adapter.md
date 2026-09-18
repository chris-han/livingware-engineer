# Crawlee Python Adapter Contract

Livingware uses Crawlee Python as the preferred reusable acquisition runtime. Crawlee owns HTTP/file download, session handling, request queues, ordinary retries, and browser transport. Livingware owns when those mechanics are used and how observations become corpus evidence.

## Current upstream semantics checked for this integration

The current Crawlee Python implementation defines:

- `retry_on_blocked=True` by default;
- `retry_on_blocked` as an attempt to bypass bot protections automatically;
- default session blocked status codes as `401`, `403`, and `429`;
- blocked-session rotations separately from `max_request_retries`;
- `FileDownloadCrawler` for raw binary download without parsing, including streaming for large bodies.

Because those defaults are broader than Livingware's evidence-first recovery policy, Livingware overrides the first pass.

Upstream: `https://github.com/apify/crawlee-python`.

## Stage 1 — observation-first acquisition

Use the appropriate Crawlee HTTP/file crawler with:

```python
retry_on_blocked=False
max_session_rotations=0
```

Keep ordinary network retry settings proportional to the source, but do not let blocked-session retry obscure the first observed `401/403/429`.

Interpretation:

- `401` -> `AUTH_REQUIRED`
- `403` -> `ACCESS_DENIED_OR_BLOCKED`
- `429` -> `RATE_LIMITED`

After a blocked observation, run the two recovery lanes in `access-recovery.md`.

## Stage 2 — one bounded blocked retry

If both recovery lanes fail and the status is eligible, run a second Crawlee attempt with blocked handling enabled:

```python
retry_on_blocked=True
max_session_rotations=1
max_request_retries=0
```

This is a single explicit escalation, not the default mode.

Eligibility rules:

- Never auto-escalate `401`.
- Escalate `403` only when the target is a public resource and evidence points to session/bot blocking rather than authorization.
- For `429`, honor rate backoff first. Do not use blocked retry to defeat a clear service-wide rate limit.

Do not add proxy rotation by default. If the environment already provides an authorized proxy/session policy, it remains an external capability and must be visible in the evidence.

## Raw files before derived representations

For PDFs, DOCX, images, archives, and other source artifacts, prefer `FileDownloadCrawler` so the canonical bytes are preserved. For large files, use its streaming mode.

After acquisition:

1. write the raw source bytes into the corpus directory;
2. run `../scripts/freeze_artifact.py` to record SHA-256 and provenance;
3. run `../scripts/verify_frozen.py` offline before claiming reproducibility;
4. only then produce Markdown/JSON/RAG representations with Crawl4AI or another transformation layer when useful.

## Browser escalation

If public content is reachable only through JavaScript-driven navigation, prefer Crawlee's browser crawler first so the acquisition runtime stays uniform. Scrapling may be selected as a conditional adaptive/browser transport when it has a demonstrated advantage for the target site.

Browser success does not replace raw-source freezing when a canonical downloadable artifact exists.
