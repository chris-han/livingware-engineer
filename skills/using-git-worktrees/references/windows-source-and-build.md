# Windows builds from one shared source

Use this reference when developing, building, signing or publishing a Windows desktop application whose authoritative source is shared from WSL. User and repository path contracts override generic worktree defaults. This contract is usable from WSL/Linux Bash and native Windows PowerShell 5.1 or later; never assume one shell's syntax, drive visibility or installed binaries apply to the other.

## Source authority and local build state

Keep one maintained source checkout. Read scripts, application code, manifests and lockfiles from that source; make and commit all fixes there. A faster local disk, UNC working-directory error or missing dependency does not authorize another source checkout. Do not clone, copy, export, mirror or register a Windows worktree on D: to work around these problems. Never edit a D: operator copy and treat its commits as integrated source.

For the explicitly configured Semantier workspace:

| Owner | Location |
|---|---|
| Runtime source | `R:\` on Windows; `/home/chris/repo/semantier-runtime` in WSL |
| Same source through UNC | `\\wsl.localhost\Ubuntu-22.04\home\chris\repo\semantier-runtime` |
| Hermes source and operator | `<Runtime>/hermes-agent`; `<Hermes>/scripts/deploy-ecs.ps1` |
| Windows dependencies, environments, caches, generated products, packaging, logs and checkpoints | `D:\repo\deliverables` on Windows; `/mnt/d/repo/deliverables` for WSL inspection |

`D:\repo\hermes-build` and `D:\repo\deliverables\work\ecs-build-source` are not authoritative sources. Preserve legacy artifacts and interrupted-run evidence; do not delete them or change their source bindings to manufacture compatibility. R: is a session-scoped alias of the UNC location, not a separate repository. Verify its target before use; never replace an occupied drive. Resolve UNC from the established mapping for Windows children that cannot see R:. Do not invent a second source if the mapping is unavailable.

## Native Windows PowerShell entry

Use Windows tools against the shared source and local build state. Quoted UNC paths are supported by PowerShell `-File`, `-LiteralPath`, Python file reads and Node file reads. These capabilities do not by themselves qualify a complete build.

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

Treat source, dependencies, work/output and cache as distinct inputs. Read code from R:/UNC; direct all generated products, native node_modules, Python environments, payload assembly, MakeAppx/signing inputs and outputs to local Windows paths under D:\repo\deliverables. Do not modify shared Linux node_modules or put Windows environments in the WSL source checkout. Keep source/commit, lockfile, platform and toolchain identities bound to prepared inputs and checkpoints.

`cmd.exe` cannot use a UNC current directory and silently falls back to the Windows directory. Launch any cmd/batch-dependent child with an explicit local working directory and absolute shared-source inputs, or invoke its existing native executable/JS entrypoint directly. Do not infer that PowerShell shares this limitation. Preserve source-relative import and module-resolution semantics when separating output/dependency roots; changing only the top-level source flag is insufficient.

Before expensive work, validate the existing selected tools and capabilities for the requested mode: native Windows architecture, pinned Python/Node/npm/uv, required Python imports, compiler/SDK/MSBuild, resource and packaging tools, Rust when used, signing certificate/private key, required Electron/native archives, and existing acceptance browser dependencies. Reuse validated persistent caches and tools; missing or invalid prerequisites fail early with the exact repair needed. Ordinary runs must not automatically download, reinstall, rebuild or copy toolchains. Explicit environment provisioning is a separate authorized action. Do not add a provider registry, environment installer or parallel build controller.

Use the repository's current operator, parameters and owning plan. If the existing builder still hardcodes generated state under the source, correct those owning paths and run focused Windows verification before claiming no-copy build support. Do not restore a D: source clone as a fallback. Record the consequential source/output path decision in the existing plan or build contract, not chat alone.

## Verification and resume

Verify both shell entries without deploying: PowerShell 5.1 UNC script/read probes; Windows Python and Node source reads; cmd/batch working-directory handling; Bash syntax/path conversion and Windows interop when available. Validate the assembled native Windows build separately before declaring it qualified. Distinguish verified script access from a verified full build.

Resume existing source/configuration-bound artifacts and successful stages only when their bindings still match. Preserve run mode, version reservations, user profiles, credential ownership and publication checkpoints. Never rebuild or publish merely to validate this guidance. Secrets remain at their existing owner and must not appear in renderer data, logs, commits or documentation.
