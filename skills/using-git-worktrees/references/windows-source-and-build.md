# Windows builds from one shared source

Use this reference when developing, building, signing or publishing a Windows desktop application whose authoritative source is shared from WSL. User and repository path contracts override generic worktree defaults. This contract is usable from WSL/Linux Bash and native Windows PowerShell 5.1 or later; never assume one shell's syntax, drive visibility or installed binaries apply to the other.

## Source authority and local build state

Keep R:/UNC as the only maintained source. Make and commit every application, operator and build-script fix there. For the existing native Windows builder, create a temporary, exact source copy under D:\repo\deliverables\work for the build. This is disposable execution input, never an editable development checkout or integration target. Never edit, patch or commit code in D:. If a staged build fails because code needs changing, fix R:, freeze the new source identity and restage it. Generated build products are permitted; hand edits to staged source are not.

For the explicitly configured Semantier workspace:

| Owner | Location |
|---|---|
| Runtime source | `R:\` on Windows; `/home/chris/repo/semantier-runtime` in WSL |
| Same source through UNC | `\\wsl.localhost\Ubuntu-22.04\home\chris\repo\semantier-runtime` |
| Hermes source and operator | `<Runtime>/hermes-agent`; `<Hermes>/scripts/deploy-ecs.ps1` |
| Temporary source copy | `D:\repo\deliverables\work\<run>\source` (or the existing operator staging path, with exclusive ownership) |
| Windows dependencies, environments, caches, generated products, packaging, logs and checkpoints | `D:\repo\deliverables` on Windows; `/mnt/d/repo/deliverables` for WSL inspection |

`D:\repo\hermes-build` and `D:\repo\deliverables\work\ecs-build-source` are not authoritative sources. Preserve legacy artifacts and interrupted-run evidence; do not delete them or change their source bindings to manufacture compatibility. R: is a session-scoped alias of the UNC location, not a separate repository. Verify its target before use; never replace an occupied drive. Resolve UNC from the established mapping for Windows children that cannot see R:. Do not invent a second source if the mapping is unavailable.

## Native Windows PowerShell entry

Read the authoritative operator from R:/UNC; stage exact source for Windows tools on D:. Keep all maintained code on R:. Quoted UNC paths are supported by PowerShell `-File`, `-LiteralPath`, Python file reads and Node file reads. These capabilities do not by themselves qualify a complete build.

```powershell
$runtime = '\\wsl.localhost\Ubuntu-22.04\home\chris\repo\semantier-runtime'
$source = Join-Path $runtime 'hermes-agent'
$deploy = Join-Path $source 'scripts\deploy-ecs.ps1'
$localBuildRoot = 'D:\repo\deliverables'
if (!(Test-Path -LiteralPath $deploy -PathType Leaf)) { throw 'Shared source unavailable' }
# Read-only inspection; inspect supported parameters before choosing build arguments.
Get-Help $deploy -Full
# Planning only, not build qualification or publication authorization.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $deploy -WhatIf
```

Use process-scoped execution-policy handling only for inspected trusted scripts; never change machine/user policy. Scope native Git ownership exceptions to exact source roots for the invocation; never use `safe.directory=*`. Do not invoke WSL/Linux Git as a Windows build-process proxy.

## WSL/Linux entry

Use Linux paths, Bash and `/usr/bin/git` for source inspection, editing and commits. Keep Windows tool execution explicit and use interop only when available. Do not run Windows Git against this repository from WSL. If the declared distro or path differs, resolve the actual existing mapping rather than silently choosing another checkout.

```bash
runtime=/home/chris/repo/semantier-runtime
source_root="$runtime/hermes-agent"
test -f "$source_root/scripts/deploy-ecs.ps1" || exit 1
/usr/bin/git -C "$source_root" status --short
# Convert the existing source path for the Windows child, not to copy source.
command -v wslpath >/dev/null || exit 1
command -v powershell.exe >/dev/null || exit 1
operator_windows=$(wslpath -w "$source_root/scripts/deploy-ecs.ps1")
# A local working directory avoids cmd.exe's UNC-current-directory fallback.
(cd /mnt/d/repo/deliverables && powershell.exe -NoProfile -ExecutionPolicy Bypass \
  -File "$operator_windows" -WhatIf)
```

A Linux host without Windows interop can maintain source and instructions but cannot claim native Windows build, signing or Electron verification. Report that specific unavailable capability; do not install a replacement environment or claim Linux evidence as Windows evidence.

## Builder and toolchain requirements

Treat authoritative source, temporary staged source, dependencies, work/output and cache as distinct inputs. Stage code from R:/UNC; direct all native node_modules, Python environments, generated products, payload assembly, MakeAppx/signing inputs and outputs to local Windows paths under D:\repo\deliverables. Do not modify shared Linux node_modules or put Windows environments in the WSL source checkout. Keep source/commit, lockfile, platform and toolchain identities bound to prepared inputs and checkpoints.

`cmd.exe` cannot use a UNC current directory and silently falls back to the Windows directory. Launch any cmd/batch-dependent child with an explicit local working directory and absolute shared-source inputs, or invoke its existing native executable/JS entrypoint directly. Do not infer that PowerShell shares this limitation. Preserve source-relative import and module-resolution semantics when separating output/dependency roots; changing only the top-level source flag is insufficient.

Before expensive work, validate the existing selected tools and capabilities for the requested mode: native Windows architecture, pinned Python/Node/npm/uv, required Python imports, compiler/SDK/MSBuild, resource and packaging tools, Rust when used, signing certificate/private key, required Electron/native archives, and existing acceptance browser dependencies. Reuse validated persistent caches and tools; missing or invalid prerequisites fail early with the exact repair needed. Ordinary runs must not automatically download, reinstall, rebuild or copy toolchains. Explicit environment provisioning is a separate authorized action. Do not add a provider registry, environment installer or parallel build controller.

Use the repository's current operator, parameters and owning plan. The current builder requires local BuildSource; UNC support in PowerShell alone does not remove that restriction. Use the temporary D: source stage rather than requiring a no-copy builder refactor. Record authoritative and staged paths plus their exact identities in existing run metadata. Record this source/staging/cleanup decision in the existing plan or build contract, not chat alone.

## Temporary source lifecycle (required)

1. Before staging or expensive work, validate the exact intended operator arguments and existing Windows toolchain. A generic UNC file-read probe or WhatIf using default paths does not validate the selected BuildSource. Dry-run the actual local staging path and selected mode; keep WhatIf free of staging, version reservation, installs and publication.
2. Freeze the requested R: application commit and authoritative operator/tooling identity separately. Materialize only that source into an exclusively owned local stage using the existing builder's verified copy/export/independent-clone mechanism. Do not register a Windows worktree in the WSL repository or use cross-filesystem object alternates/hard links. Never mutate or delete a pre-existing dirty/foreign stage. Do not copy .env, private keys, live profiles or shared Linux dependencies into the source stage; credentials remain at their established owner.
3. Verify staged source identity before executing it. Native build children use a local working directory and the staged inputs. Source is never edited on D:, including quick fixes, generated patches or commits. Generated files required by the existing build are execution products, not maintained changes. If a fix is needed, change and commit R: first and create a newly bound stage.
4. Reuse toolchains and dependency caches outside the disposable source stage; do not reinstall or rebuild them merely because staging is fresh. Preserve compatible completed MSIX/signing checkpoints. Do not resume a prepared-source checkpoint after its stage was deleted without reconstructing and validating its source/configuration binding through the existing operator.
5. Before cleanup, preserve final packages, logs, receipts, checkpoints and reusable dependency state outside the source stage. The stage must not be the only home of a required artifact. Wait for all stage-owned build processes to finish, then remove only the workflow-owned temporary source after the build attempt, including failed attempts once diagnostics are preserved. Use try/finally or the operator's equivalent cleanup path; abrupt termination must leave enough ownership metadata for cleanup on resume. Do not silently retain the stage as a development checkout.
6. Before recursive deletion, verify the resolved absolute path is the exact owned child under D:\repo\deliverables\work, not the work root, an ancestor, a cache/output/profile directory, R:/UNC, or a reparse point. In PowerShell use Remove-Item -LiteralPath on that verified path; keep file operations in one shell. In WSL orchestration prefer the existing Windows operator for stage cleanup. A copy of source is disposable; shared caches, credentials, user files and release artifacts are not. If artifact preservation, ownership validation or cleanup fails, report that exact blocker and retained path rather than claiming successful cleanup.

The dry-run contract is source R:/UNC -> temporary source D: -> existing local Windows build inputs -> preserved outputs/cache -> verified stage deletion. Verify it through the actual operator configuration. Do not create a new controller just for this policy, run a release to test documentation, or claim lifecycle automation exists until the owning script implements it.

## Verification and resume

Verify both shell entries without deploying: PowerShell 5.1 UNC script/read probes; Windows Python and Node source reads; cmd/batch working-directory handling; Bash syntax/path conversion and Windows interop when available. Verify the exact staged-source configuration and cleanup lifecycle; validate the assembled native Windows build separately before declaring it qualified. Distinguish verified script access, staging/preflight, full build, publication and cleanup.

Resume existing source/configuration-bound artifacts and successful stages only when their bindings still match. Preserve run mode, version reservations, user profiles, credential ownership and publication checkpoints. Never rebuild or publish merely to validate this guidance. Secrets remain at their existing owner and must not appear in renderer data, logs, commits or documentation.
