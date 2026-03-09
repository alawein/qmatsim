#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "SSOT.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "qmatsim/__init__.py",
    "qmatsim/__main__.py",
    "scripts/run-DFT.sh",
    "scripts/run-MD.sh",
    "scripts/run-postprocessing.sh",
    "siesta/",
    "lammps/",
    "docs/README.md",
    "docs/architecture/STRUCTURE_DECISION.md",
    "tests/test_cli_basic.py",
    "tests/test_qmatsim_cli.py",
]


def main() -> int:
    failures: list[str] = []

    for relative_path in REQUIRED_PATHS:
        target = ROOT / relative_path
        if relative_path.endswith("/"):
            if not target.is_dir():
                failures.append(f"{relative_path}: missing required directory")
        elif not target.exists():
            failures.append(f"{relative_path}: missing required file")

    if (ROOT / "src").exists():
        failures.append(
            "src/: unexpected parallel package root; QMatSim uses a rooted qmatsim/ package layout",
        )

    main_source = (ROOT / "qmatsim" / "__main__.py").read_text(encoding="utf-8")
    if "scripts/run-DFT.sh" not in main_source:
        failures.append("qmatsim/__main__.py: expected DFT workflow handoff to scripts/run-DFT.sh")
    if "scripts/run-MD.sh" not in main_source and "scripts/compress-MD.sh" not in main_source:
        failures.append("qmatsim/__main__.py: expected MD workflow handoff to scripts/run-MD.sh or scripts/compress-MD.sh")
    if "scripts/run-postprocessing.sh" not in main_source:
        failures.append("qmatsim/__main__.py: expected postprocessing handoff to scripts/run-postprocessing.sh")

    if failures:
        print("\n".join(failures))
        return 1

    print("structure: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
