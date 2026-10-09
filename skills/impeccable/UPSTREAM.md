# Upstream Impeccable Snapshot

Livingware Engineer vendors Impeccable as its generic frontend craft and anti-slop design layer.

- Repository: https://github.com/pbakaus/impeccable
- Imported commit: `b0594c72d18006b5865c70eb3a97e8b04064e600`
- Imported source path: `.agents/skills/impeccable`
- Upstream skill version: `4.1.2`
- Imported on: `2026-08-29`
- Imported file count: `168`
- Original upstream tree SHA256: `e0121aaeb04b7c43cdc788d1ee15e15c53220a7101d49c4954af8ad4793f8cd2`
- Tree SHA256: `89f240d32accbb8f0c43e0c95d44d920e1e95149075236a4b832fe959a0ed61d`
- License: Apache-2.0; see `LICENSE.upstream`
- Notice: see `NOTICE.upstream`

The snapshot contains 168 files. `SKILL.md` has two historical Livingware adaptations: commit `bba7da9` added the Fast-to-Aha law, and commit `2b652ae` narrowed the activation description and normalized the final newline. The original upstream digest is retained above; Tree SHA256 binds the currently bundled adapted tree. All other upstream files remain unchanged. Further Livingware-specific design behavior belongs in `skills/frontend-design/SKILL.md`, not in the vendored tree. To update Impeccable, replace the complete upstream snapshot from a selected commit, update this record, and rerun the frontend-design tests plus the cross-harness plugin tests.
