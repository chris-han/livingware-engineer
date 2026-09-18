---
name: data-collection-pipeline
description: Use when building or repairing a reproducible public-data acquisition pipeline, especially when a target entry point is blocked by authentication, anti-bot behavior, redirects, missing links, or unstable download paths.
---

# Data Collection Pipeline

## Lifecycle

Entry: the task requires collecting a bounded external corpus or source set with reproducible acquisition evidence, or an existing acquisition path has failed.
Exit: the required source set is acquired and frozen with provenance, or remaining gaps are classified with evidence showing why they are currently unresolved.

Do not treat one blocked URL, login wall, search failure, or anti-bot response as evidence that the underlying source or dataset is unavailable.

## Core invariant

**An entry-point failure is evidence about that entry point, not about source existence.**

When the first path fails, preserve the failure evidence and split recovery into two independent search lanes:

1. **Alternate-source lane** — look for the same authoritative material through other official/public repositories, mirrors, publication channels, archives, or equivalent primary sources.
2. **Same-site alternate-entry lane** — stay on the original domain but search for different list pages, search endpoints, attachment paths, document detail pages, static-file URLs, API endpoints, or other reachable routes to the same material.

Run both lanes when they are cheap and independent. Do not serially exhaust one before trying the other unless source authority requires it.

## Acquisition workflow

1. Define the corpus boundary before downloading: source family, target document types, time/jurisdiction filters, minimum diversity, and stopping condition.
2. Use Crawlee Python as the default acquisition runtime when a reusable crawler/download layer is needed. Start with a one-request observation probe: `retry_on_blocked=False`, no session rotations, no ordinary request retries, and `401/403/429` exposed to the handler as observations.
3. Record the observed transport state. A `401`, `403`, or `429` is an observation about that route, not proof that the source is absent.
4. On a blocked entry point, run the alternate-source and same-site alternate-entry lanes.
5. If both lanes fail, allow one bounded blocked-retry escalation only when the status is eligible:
   - `401`: do not automatically switch to `retry_on_blocked=True`; treat it as `AUTH_REQUIRED` unless an authorized authentication flow exists.
   - `403`: `retry_on_blocked=True` is allowed only when evidence indicates a public resource blocked by session/bot handling rather than an access-control boundary.
   - `429`: honor `Retry-After` / rate backoff first; only then allow one bounded blocked-retry attempt.
6. For the escalation attempt, keep retries bounded and visible; do not silently turn it into open-ended proxy, credential, CAPTCHA, or access-control circumvention.
7. Prefer primary/official sources; when using a mirror or secondary host, retain enough provenance to trace back to the authoritative publication.
8. Download raw source bytes before AI-oriented conversion. Freeze accepted artifacts with original URL, resolved URL, retrieval time, HTTP/content metadata when available, byte size, and SHA-256.
9. Re-verify the frozen corpus offline: files exist, hashes match, manifest rows are complete, and the corpus still satisfies the declared boundary and diversity requirements.
10. Report unresolved gaps separately from acquired material; do not let a failed path erase evidence from successful branches.

## Tool ownership and economy

Livingware owns acquisition strategy, recovery routing, and evidence state. It does not own a crawler implementation.

- **Crawlee Python** owns the default HTTP/file-download/session/retry/browser transport mechanics. Read `references/crawlee-python-adapter.md` when reusable acquisition mechanics are needed.
- Search engines and site-scoped search are discovery tools, not proof that a document is absent.
- Browser inspection is appropriate when JavaScript navigation or generated attachment links hide the real public route.
- Use `scripts/freeze_artifact.py` after bytes have been acquired to create the Livingware provenance/hash record. Use `scripts/verify_frozen.py` to recheck frozen hashes offline.
- Scrapling or another browser/adaptive transport may be used as a conditional escalation when a public site demonstrably requires richer browser behavior; do not make that a default dependency.
- Crawl4AI-style Markdown/LLM conversion belongs after raw-source acquisition and freezing; derived representations are not substitutes for canonical source bytes.

Do not add a second HTTP client, crawler framework, browser stack, or retry engine inside this skill when Crawlee or an existing host capability already owns that mechanic.

## Evidence discipline

For every candidate or accepted artifact, distinguish:

- `DISCOVERED` — a plausible source/URL was found;
- `PROBED` — transport behavior was actually observed;
- `RECOVERY_SEARCHED` — alternate-source and/or same-site alternate-entry recovery ran;
- `BLOCKED_RETRY` — one explicit bounded `retry_on_blocked=True` escalation was attempted;
- `ACQUIRED` — bytes were downloaded;
- `FROZEN` — content hash and provenance were recorded;
- `OFFLINE_VERIFIED` — frozen bytes and manifest were rechecked without relying on the live source.

A search-result snippet or a page title is not acquisition evidence. A successful browser view is not a frozen corpus artifact. A downloaded file without provenance/hash is not reproducible collection evidence.

## Progressive disclosure

Read `references/access-recovery.md` when an initial route is blocked or source discovery is ambiguous. Read `references/crawlee-python-adapter.md` when Crawlee is the acquisition runtime. Keep AI-oriented transformation separate from raw-source acquisition and provenance.
