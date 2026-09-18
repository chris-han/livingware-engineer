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
2. Probe candidate URLs and record the observed transport state instead of describing failure from memory.
3. On a blocked entry point, branch immediately into alternate-source and same-site alternate-entry recovery.
4. Prefer primary/official sources; when using a mirror or secondary host, retain enough provenance to trace back to the authoritative publication.
5. Download only after the candidate has passed source/identity checks appropriate to the task.
6. Freeze every accepted artifact with original URL, resolved URL, retrieval time, HTTP/content metadata, byte size, and SHA-256.
7. Re-verify the frozen corpus offline: files exist, hashes match, manifest rows are complete, and the corpus still satisfies the declared boundary and diversity requirements.
8. Report unresolved gaps separately from acquired material; do not let a failed path erase evidence from successful branches.

## Tool ownership and economy

Use search/browser tools for discovery and route recovery; use deterministic operators for transport verification and freezing.

- Search engines and site-scoped search are discovery tools, not proof that a document is absent.
- Browser inspection is appropriate when JavaScript navigation or generated attachment links hide the real download route.
- `curl`/HTTP probing is appropriate for redirects, status codes, content type, and direct-file confirmation.
- Use `scripts/fetch_and_freeze.py` when a stable URL has been identified and an artifact should be downloaded with a machine-verifiable manifest record. Use `scripts/verify_frozen.py` to recheck frozen hashes offline before declaring the corpus reproducible.

Do not add scraping frameworks, headless-browser stacks, or custom crawlers merely because the first URL failed. Escalate tooling only when the site behavior demonstrates that lighter discovery/probe methods are insufficient.

## Evidence discipline

For every candidate or accepted artifact, distinguish:

- `DISCOVERED` — a plausible source/URL was found;
- `PROBED` — transport behavior was actually observed;
- `ACQUIRED` — bytes were downloaded;
- `FROZEN` — content hash and provenance were recorded;
- `OFFLINE_VERIFIED` — frozen bytes and manifest were rechecked without relying on the live source.

A search-result snippet or a page title is not acquisition evidence. A successful browser view is not a frozen corpus artifact. A downloaded file without provenance/hash is not reproducible collection evidence.

## Progressive disclosure

Read `references/access-recovery.md` when an initial route is blocked or source discovery is ambiguous. Use the deterministic fetch/freeze operator only after discovery has produced a candidate URL worth preserving.
