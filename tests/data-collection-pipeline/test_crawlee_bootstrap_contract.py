#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[2]
BOOT = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "bootstrap_crawlee.py"


def load_bootstrap():
    spec = importlib.util.spec_from_file_location("bootstrap_crawlee", BOOT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    bootstrap = load_bootstrap()
    assert bootstrap.SUPPORTED_CRAWLEE_VERSION == "1.10.1"
    assert bootstrap.CORE_REQUIREMENT == "crawlee==1.10.1"
    assert bootstrap.BROWSER_REQUIREMENT == "crawlee[playwright]==1.10.1"
    assert bootstrap.MIN_PYTHON == (3, 10)

    with tempfile.TemporaryDirectory() as td:
        runtime = Path(td) / "runtime"
        python = bootstrap.venv_python(runtime)
        assert not python.exists()
        assert runtime.name == "runtime"

    print("PASS: Crawlee bootstrap pins core and browser requirements separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
