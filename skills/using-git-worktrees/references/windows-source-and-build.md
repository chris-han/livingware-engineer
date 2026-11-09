# Shared source and native Windows build isolation

Use this reference when a native Windows build consumes source hosted on another filesystem, including WSL. It supplements workspace isolation; the consuming project's build skill and operator own concrete paths, shell versions, toolchain pins, signing, release targets and commands.

## Source and execution ownership

Keep one maintained source authority. If the existing native toolchain cannot reliably build from that filesystem, use an exact, source-bound temporary local stage. Make code changes at the authoritative source and restage; never turn the execution copy into a second development checkout. Do not require a copy when the complete existing build is already qualified against the shared source.

Keep reusable dependency caches and final artifacts outside disposable source stages. Reuse inputs only when the existing operator validates their source, lockfile, platform and toolchain bindings. A fresh stage does not justify reinstalling tools or rebuilding unchanged dependencies.

## Platform boundary

Distinguish WSL/Linux Bash from native Windows PowerShell. Use each environment's native paths and tools; do not assume drive aliases, Git configuration or installed binaries are shared. PowerShell and file readers can accept UNC paths, but cmd.exe cannot use a UNC working directory. Check the actual child-process path rather than inferring whole-build compatibility from a file-read probe.

The project owns supported PowerShell versions and any legacy Windows module boundary. Inspect that owner before selecting an executable; do not introduce a framework-wide shell version or modify persistent execution policy automatically.

## Temporary stage lifecycle

Before execution, bind the authoritative revision, exact local stage, persistent cache and output locations through the existing operator. Preserve foreign/dirty stages and concurrent work. Do not copy secrets or incompatible host dependencies into the stage.

After the attempt, preserve required artifacts, diagnostics and reusable state outside the stage. Remove only the owned stage once its processes have finished and recovery bindings are retained. Verify the resolved target is the exact owned child, never an ancestor, shared cache, source authority or link target. Keep Windows filesystem operations in native PowerShell and do not traverse junctions during cleanup.

Report access/preflight, build, installation, signing, publication and cleanup as separate verified outcomes. A WhatIf run does not qualify a build or release. Leave executable preflight and cleanup mechanics in the project operator; do not create a second builder or release controller in this skill.