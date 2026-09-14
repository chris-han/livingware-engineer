# Codex Progressive Skill Token Baseline — 2026-09-14

## Purpose

Record the empirical baseline for Livingware Engineer's Codex progressive skill-loading and token-cost work after the 6.8.x refactor. This benchmark is a regression reference, not a deterministic performance SLA; model execution paths vary between runs.

## Fixture

The live probe creates an isolated temporary Git repository containing a minimal `normalizePath` implementation and regression test. This avoids contaminating the measurement with a large host repository, codebase-memory indexes, unrelated Git history, or project-specific instructions.

Run:

```bash
CODEX_PROBE_RETRIES=1 \
CODEX_PROBE_TIMEOUT=180 \
bash tests/codex/live-progressive-skill-probe.sh
```

The probe records input, cached input, uncached input, output, reasoning output, latency, selected-skill evidence, JSONL, and stderr per scenario.

## Stable 6.8.3 three-run baseline

All 12 scenario executions passed. Skill selection was correct in every workflow scenario.

| Scenario | Median latency | Median uncached input | Observed uncached range |
| --- | ---: | ---: | ---: |
| baseline | 10 s | 5,611 | 5,611–5,611 |
| systematic-debugging | 40 s | 24,747 | 17,294–26,648 |
| test-driven-development | 38 s | 20,055 | 16,708–20,250 |
| verification-before-completion | 31 s | 14,437 | 8,522–41,147 |

### Routing invariants observed

- Native Codex matching selected `systematic-debugging` for unexplained failure.
- Native Codex matching selected `test-driven-development` for authorized implementation with established diagnosis.
- Native Codex matching selected `verification-before-completion` for the explicit completion/merge claim.
- The bounded implementation trace did not activate completion verification merely to report implementation results.
- Bounded debugging/TDD traces after the tool-economy refactor can complete without codebase-memory.

## Comparison to isolated 6.8.0 single-run baseline

| Scenario | 6.8.0 uncached input | 6.8.3 median | Approx. reduction |
| --- | ---: | ---: | ---: |
| baseline | 7,889 | 5,611 | 29% |
| debugging | 37,296 | 24,747 | 34% |
| TDD | 36,787 | 20,055 | 45% |
| verification | 41,115 | 14,437 | 65% |

Do not treat one run as a release gate. Compare medians and inspect trace behavior before attributing a regression to skill text.

## Variance finding

Verification showed the largest variance. The high 41,147-uncached run performed `codebase-memory` index-status and coverage calls; the lower runs did not. This is an activation/tool-choice variance rather than a larger verification root body. Version 6.8.4 therefore makes the bounded/local verification boundary explicit: use focused existing evidence and do not activate codebase-memory unless the claim genuinely crosses unresolved structural boundaries.

## Optimization boundary

The 6.8.x work established that the highest-value changes were architectural rather than lexical:

1. native matcher instead of a mandatory meta-router;
2. current-state skill loading instead of future-state preloading;
3. compact root contracts with detailed playbooks behind progressive disclosure;
4. bounded tool use instead of automatic repository/index discovery;
5. reuse of existing evidence rather than ceremonial verification work.

Further prompt minification should not weaken root-cause discipline, TDD behavioral oracles, real-component integration requirements, real-browser UI evidence, or claim/evidence correctness. Future optimization should prioritize serial tool-turn reduction, bounded tool output, evidence reuse, and fixed Codex session-context cost.
