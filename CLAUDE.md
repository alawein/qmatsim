---
type: canonical
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-04-09
source: none
sync: none
sla: none
---

# CLAUDE.md — QMatSim

## Repository Context

**Name:** QMatSim
**Type:** research-library
**Purpose:** Multiscale simulation framework for strain engineering in 2D
materials. Combines DFT (SIESTA) and MD (LAMMPS) calculations to study flat
bands, lateral heterostructures, and electronic phases in transition metal
dichalcogenides. Implements the computational framework from Alawein et al.,
Physical Review Materials 2025.

---

## Tech Stack

- **Language:** Python 3.9+
- **Core deps:** NumPy, Matplotlib
- **Build:** setuptools via `pyproject.toml`
- **Testing:** pytest, pytest-cov
- **Linting:** black, flake8, mypy

<!-- EXTENSION SLOT: Toolchain
     Add project-specific toolchain details here (HPC tools, simulation
     engines, external solvers, GPU frameworks, etc.)
-->
- **DFT engine:** SIESTA 4.1+ (DFT calculations)
- **MD engine:** LAMMPS stable (molecular dynamics)
- **HPC scheduler:** SLURM (job submission and resource management)

---

## Commands

### Setup

```bash
pip install -e ".[dev]"
```

### Test

```bash
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
```

### Lint / Format

```bash
black qmatsim/
flake8 qmatsim/
mypy qmatsim/
```

<!-- EXTENSION SLOT: Additional Commands
     Add project-specific command sections here (benchmarks, agents,
     SSOT, simulation workflows, HPC job submission, etc.)
-->

### Validation

```bash
python scripts/validate-structure.py
python -m qmatsim --help
```

### Running Simulations

```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure 1x10_rectangular --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

---

## Architecture Overview

QMatSim is a Python CLI orchestrator layered on top of two domain surfaces:

- `siesta/` for DFT inputs, templates, and materials
- `lammps/` for MD inputs, data files, and potentials

The Python package coordinates those surfaces and delegates the heavy workflow
execution to shell automation under `scripts/`.

---

## Project Structure

```
qmatsim/
├── qmatsim/               # Canonical Python package and CLI module
├── scripts/               # Bash and Python automation for setup, SLURM, and validation
├── siesta/                # DFT calculation infrastructure and templates
├── lammps/                # MD simulation infrastructure and assets
├── tests/                 # CLI smoke tests
├── docs/                  # Theory, API, development, and architecture docs
└── pyproject.toml         # Package configuration
```

---

## Key Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Build, deps, tool config |
| `AGENTS.md` | Governance invariants (normative) |

---

## Important Notes / Known Quirks

<!-- Standard research library notes -->

**Deterministic seeds** -- All benchmark and experiment runs must use fixed seeds.
Reproducibility is a governance invariant. Never remove seed arguments from benchmark
or test code.

**Archive is read-only** -- If an `archive/` directory exists, it contains historical
data and papers. Never modify its contents.

**API stability** -- Breaking changes to the public API require a version bump and a
`CHANGELOG.md` entry.

**Pre-commit / linting** -- Run the project's format command before committing.

<!-- EXTENSION SLOT: Domain-Specific Notes
     Add project-specific quirks, numerical issues, data handling rules,
     dependency caveats, etc.
-->

**Canonical root package** -- The Python package is rooted at `qmatsim/`, not `src/`.
Do not introduce a parallel `src/` tree without an explicit migration decision. This
repo's documented structure exception is intentional.

**HPC path handling** -- Do not hardcode HPC paths; use configuration files and templates.

---

## Domain-Specific Rules

<!-- EXTENSION SLOT: Domain-Specific Rules
     Each project fills this section with rules unique to its research domain.
-->

- **No parallel `src/` tree**: The canonical Python import surface is `qmatsim/`; do not restructure without explicit migration decision
- **SIESTA and LAMMPS backends must both be supported**: New features should work with both DFT and MD surfaces
- **Domain assets stay in their directories**: Keep SIESTA assets under `siesta/` and LAMMPS assets under `lammps/`; do not scatter them
- **SLURM scripts require resource headers**: All SLURM job scripts must include proper resource management headers
- **HPC paths must use configuration**: Never hardcode cluster-specific paths; use templates and config files

---

## Data Integrity

<!-- EXTENSION SLOT: Data Integrity
     Define project-specific rules for data handling, reproducibility,
     and research artifact management.
-->

- **Simulation inputs are reference data**: DFT templates and MD potentials under `siesta/` and `lammps/` should not be casually modified
- **Simulation outputs must include parameter provenance**: Record material, structure, and calculation parameters for all results

---

## Governance

See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
