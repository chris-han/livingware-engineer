---
name: upstream-sync
description: Use when integrating a new upstream revision into a downstream fork, vendored dependency, or submodule that carries local adaptations; not for ordinary dependency installation.
---

# Upstream Sync

Entry: a downstream component must advance to an identified upstream revision. Exit: the candidate preserves required downstream behavior and has passed the owning project's applicable qualification, or a specific incompatibility is recorded.

1. Identify the current downstream revision, target upstream revision, repository instructions, and the existing owners of local adaptations and qualification. Preserve unrelated work.
2. Inventory downstream changes and behavior contracts before integration. Classify each as retained, already upstream, obsolete with evidence, or requiring a deliberate resolution; do not silently drop changes when resolving conflicts.
3. Integrate the pinned target in the appropriate workspace. Reapply required downstream adaptations through their existing owners, including product identity and prompt customizations when applicable. Preserve upstream attribution where accurate.
4. Run the downstream regression tests covering every retained adaptation, plus the project-required composition and integration checks. Add or update a focused regression when an adaptation lacks coverage. A green upstream suite alone does not establish downstream behavior.
5. Record the revisions, retained or retired adaptations, verification results, and unresolved limitations in the existing integration owner. Do not advance admission or activation beyond the authority granted by the project.
