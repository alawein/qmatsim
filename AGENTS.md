<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->
---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — qmatsim

> **Status: Normative.** Do not modify without maintainer review.

This repository is governed by clear engineering and documentation standards
aligned with the **Morphism Categorical Governance Framework** principles.

## Governance Source

| Authority | Location |
|-----------|----------|
| Root governance | [AGENTS.md](AGENTS.md) (this file) |
| Contributing guide | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

## Repository Scope

Python CLI framework combining DFT (SIESTA) and MD (LAMMPS) calculations to
study flat bands, lateral heterostructures, and electronic phases in transition
metal dichalcogenides (MoS2, MoSe2, WS2, WSe2). Based on Alawein et al.,
Physical Review Materials 2025.

## Directory Layout

| Directory | Purpose | Governance Level |
|-----------|---------|-----------------|
| `qmatsim/` | Canonical Python package and CLI entrypoint | **Primary** -- all changes require tests |
| `scripts/` | Bash and Python automation for setup, SLURM, and validation | **Tooling** -- document changes |
| `siesta/` | DFT calculation infrastructure and templates | **Domain asset** -- do not scatter |
| `lammps/` | MD simulation infrastructure and assets | **Domain asset** -- do not scatter |
| `tests/` | CLI and package test suite | **Required** -- never delete without replacement |
| `docs/` | Theory, API, development, and structure documentation | **Supplementary** |

## Invariants (Must Always Hold)

<!-- STANDARD INVARIANTS — do not remove or weaken these -->

1. **Tests pass**: All tests must pass before merging to main
2. **Lint clean**: Linter must exit 0 on the primary source directories
3. **Imports work**: The package must be importable after install
4. **No secrets**: API keys or credentials must never appear in source
5. **Reproducibility**: Experiment and benchmark results must be deterministic (fixed seeds)
6. **README accurate**: README code examples must match actual API signatures

<!-- EXTENSION SLOT: Additional Invariants
     Add project-specific invariants here.
-->
7. **Canonical root package**: Python import surface must remain rooted at `qmatsim/`, not `src/`
8. **Dual-backend support**: Both SIESTA and LAMMPS backends must be supported

## Agent Rules

When this repository is modified by an AI agent or automated tool:

<!-- STANDARD AGENT RULES — do not remove or weaken these -->

- **Read** `AGENTS.md` and `CONTRIBUTING.md` before making changes
- **Never** skip the test suite -- run tests before committing
- **Always** update `CHANGELOG.md` when changing public API or behavior
- **Always** keep docstrings and type hints accurate
- **Prefer** small, focused commits with conventional commit messages
- **Never** modify validated benchmark results or reference data

### Research-Specific Agent Rules

- **Data integrity**: Do not modify, rename, or delete files in immutable data
  directories (e.g., `data/`, `archive/`). Populate data directories via
  provided scripts; treat them as read-only afterward.
- **Numerical precision**: When comparing floating-point results, use tolerance-based
  comparisons. Do not tighten tolerances without verifying against known reference
  values. Document the precision requirements of any new numerical method.
- **Citation / attribution**: Update `CITATION.cff` for release-grade changes.
  Preserve author attribution in file headers. Reference the originating paper
  when implementing published algorithms.
- **Reproducibility**: All experiments, benchmarks, and simulations must be
  reproducible. Use fixed random seeds, pin dependency versions for published
  results, and record full parameter provenance for simulation outputs.

<!-- EXTENSION SLOT: Project-Specific Agent Rules
     Add rules unique to this project's domain.
-->
- Keep the canonical Python import surface rooted at `qmatsim/`
- Do not introduce a parallel `src/` tree without an explicit migration decision
- Support both SIESTA and LAMMPS backends
- Keep domain assets under `siesta/` and `lammps/`; do not scatter them across new root directories
- SLURM scripts must include proper resource management headers
- Do not hardcode HPC paths; use configuration files and templates
- Use `black` for formatting, `flake8` for linting, `mypy` for type checking

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **CLI commands**: `kebab-case`

## Commit Message Format

```
type(scope): short description

feat(siesta): add new material template
fix(lammps): correct potential file path resolution
docs(readme): update installation instructions
test(cli): add smoke test for analyze command
refactor(core): extract validation to shared utility
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`, `chore`

## Dependency Policy

- **Core deps**: Keep minimal -- NumPy, Matplotlib
- **Optional deps**: SIESTA and LAMMPS are external tools, not Python deps
- **Dev deps**: pytest, black, flake8, mypy -- no production code may import dev deps
- **Version pins**: Minimum versions only (no upper bounds unless proven necessary)

---

*Aligned with Morphism Systems governance principles.*

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
