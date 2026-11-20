# Observation 01 — Semantier Qwen BYOK production recovery (2026-11-08)

**Status:** `PRODUCTION_GREEN` (source-qualified)  
**Comparison disposition:** `NOT_COMPARABLE` to the Windows model-discovery implementation baseline.  
**Purpose:** the first observed completed engineering goal after adoption of Livingware's token-efficiency guidance; preserve real numbers and acceptance scope without treating differences as causal proof.

## Evidence / provenance

- Authoritative Semantier execution owner: `docs/plans/archive/2026-11-08-qwen-byok-production-recovery-v1.md` in `/home/chris/repo/semantier-runtime`, especially frontmatter, checkpoints 1–3, terminal checkpoint and final accounting (lines 268–292).
- Historical benchmark: [2026-11-07 Windows Provider-query-only baseline](2026-11-07-windows-provider-query-only-baseline.md).
- Structured observation: [machine-readable receipt](2026-11-08-qwen-byok-production-recovery-receipt.yaml).
- Livingware method declared in the plan: **6.15.3**, commit `56d61a17490bb496c4f9bd3b37210ebadeeb949f`; the plan notes the installed cache had already advanced to 6.15.4, so distinguish the **declared/used methodology** from the installed cache's version.
- Semantier qualified app sources: parent `9683d791e948253bd94a15498a34564cefae7cee`, Workspace `cdf8dbf13e0ae6499cbd9707712b2c8ea099fbc8`, Hermes `232cc5168fe554555ff1b2dd8776f96b8c731b37`.
- Scoped recovery integration commit: `60b06063939802074a290458d99d0a9bdbb9491a`. Application images were **not rebuilt**; retained verified image objects were reused.

## Measured and reported totals

| Metric | Windows discovery historical baseline | Qwen production recovery |
| --- | ---: | ---: |
| Terminal scope | Local integrated development GREEN (native desktop synthetic) | Actual production rollout GREEN (Qwen BYOK, managed, Weixin, isolated controls) |
| Host-reported goal tokens | 860,727 | **301,595** |
| Active elapsed seconds | 8,640 | **3,931** |
| Active elapsed time | 144m | **65m31s** |
| Token accounting basis | Aggregate report only; details unknown | Final host-goal accounting; excludes subsequent bookkeeping |
| Model / reasoning effort | UNKNOWN | UNKNOWN |
| Input / output / cached tokens | UNKNOWN | UNKNOWN |
| Actual paid API cost | UNKNOWN | UNKNOWN |
| Comparable | **No** | **No** |
| Verdict | Historical denominator | **NOT_COMPARABLE** |

The smaller observed recovery totals are **not** an efficiency-effect estimate. The tasks differ in purpose, risk, code-change surface and acceptance: the recovery resumed previously qualified software and reused exact unchanged image artifacts; Windows discovery developed and integrated new cross-stack features.

This recovery run also **excludes** the earlier Qwen local repair (reported ~102m active time; no token total supplied) and the preceding rolled-back production attempt (the archived recovery plan identifies **188,963 tokens / 2,913s** for that separate run). Do **not** report recovery-run tokens as the full cost of Qwen BYOK delivery; do not aggregate incompatible runs as a matched comparison.

## Verified completion and recovery behavior

- Authenticated Qwen credential PATCH and scoped DashScope GET succeeded; real provider catalog included `qwen3.5-plus`; main selection survived reload, new chat and actual application restart.
- Managed-model selection succeeded after setting the already-authorized cloud public origin. Concurrent token cleanup, revision guard and financial invariants qualified.
- Weixin login control and decoded QR passed after a real application restart over trusted public HTTP/3. The evidence concerns a **serialized** browser acceptance; it does not qualify concurrent-browser load.
- Invalid key, provider outage, repeat save, 504 safe timeout with late commit, cross-workspace/anonymous denial and no-leak controls passed at the accepted scope.
- Existing Caddy/PostgreSQL, 12 nonfixture customer profiles, five measured financial tables and Winman were preserved. No paid inference or phone verification.
- Reused retained production Runtime image `sha256:f0f2505b10722dba305b438a649d85db34b19fa8be74e6457890a0193bbb77d3` and Workspace `sha256:691964e2c2974f06ab4a8815d398aeea5a4de2f0058ed93e25076c290cc7d25c`.
- **No rebuild** in this recovery run. **No rollback used** in this recovery run; older-image rollback occurred in the **previous** unsuccessful rollout and remains preserved as a tested recovery path.
- Production checks are retained in the Semantier archived plan and its private receipt paths. Do not duplicate private auth/key/QR artifacts in this public skills repository.

## What can and cannot be inferred

**Supported:** this run completed production acceptance in 3,931 seconds and 301,595 host-reported tokens with the selected Livingware methodology; it demonstrated artifact reuse, a targeted origin configuration repair and a bounded Weixin readiness-test fix.

**Not supported:** a precise output-token saving from silent narration; reduced read/context cost; lower average model reasoning cost; a controlled comparison to the prior Windows discovery goal; production concurrent-browser robustness; a causal percentage improvement attributable to Livingware 6.15.3. Original per-turn usage, cache split, agent model, reasoning-effort setting, tool log sizes, repeated source-read counts and exact post-integration rework-cycle counts were not retained.

## Next evaluation decision

Keep this as **Observation 01** without retroactively changing the baseline or bumping a published skill version for a data-only entry. For a next comparable R2/R3 task, capture the model/effort, host total-token accounting definition, prompt/output/cache split, planning-and-review share, source file read hashes, rationale for repeated test suites, tool times and terminal acceptance. Compare only when matched on outcome/scope/risk or report `NOT_COMPARABLE` again.

**Research verdict:** `NOT_COMPARABLE`, no token-economy improvement claim.
