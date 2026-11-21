# Windows probe isolation

Baseline: 107827048a920e4a735c582fcc85d5e9c6ba99c8. Goal: preserve isolated probe state on Linux and Git Bash with a native Python interpreter; provide a disposable-profile PowerShell qualification runner. Terminal disposition: WSL_IMPLEMENTED_WINDOWS_QUAL_PENDING after focused WSL and packaging verification, local commit and explicit Windows handoff; otherwise BLOCKED_WITH_EVIDENCE. Native Windows qualification and release are outside this execution.

Owners: tests/codex/probe-isolation.sh and its two live callers; focused isolation tests; packaging manifest and tests if runner needs packaging. Use real probe wiring with disposable profiles, test exit/failure/concurrency/termination/orphan/retention. Resolve Python explicitly and translate native paths at the Git Bash boundary. Preserve Linux process identity behavior.

Lifecycle risks: PID reuse or wrong PID can remove live state (test identity/termination); path conversion can target wrong directory (test with spaces and disposable profile); children may recreate state after parent death (test delayed writes and bounded cleanup). Native behavior remains unqualified until the real Windows runner passes.
