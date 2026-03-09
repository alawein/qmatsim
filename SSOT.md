---
type: normative
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# SSOT — qmatsim

**Status:** Active research

## Purpose

QMatSim is the canonical source for the multiscale strain-engineering framework
that combines DFT (SIESTA) and MD (LAMMPS) workflows for 2D quantum materials.

## Current State

- Python research library and CLI: active
- DFT and MD workflow assets: active
- Published-method implementation: active

## Canonical Layout

QMatSim uses a rooted Python package layout.

| Surface | Role |
|---------|------|
| `qmatsim/` | Canonical Python package and CLI module |
| `scripts/` | Setup, SLURM, validation, and workflow automation |
| `siesta/` | DFT templates, materials, and helper assets |
| `lammps/` | MD inputs, data files, and potentials |
| `docs/` | Theory, API, development, and architecture documentation |
| `tests/` | CLI and package smoke tests |

`src/` is not the canonical import boundary for this repository.

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
for the explicit structure decision.

## Governance Documents

| Document | Purpose |
|----------|---------|
| [AGENTS.md](AGENTS.md) | Root contributor and agent rules |
| [CLAUDE.md](CLAUDE.md) | Repo-specific engineering guidance |
| [README.md](README.md) | User-facing overview and usage |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution workflow |

See [CLAUDE.md](CLAUDE.md) | [AGENTS.md](AGENTS.md)
