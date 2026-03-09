# QMatSim Structure Decision

## Decision

QMatSim intentionally uses a **rooted package** layout.

The canonical Python import and CLI surface is:

`qmatsim/`

This repository does **not** use `src/<package>/` as its primary package
boundary.

## Canonical Surfaces

- `qmatsim/` — Python package and CLI entrypoint
- `scripts/` — setup, validation, SLURM, and workflow automation
- `siesta/` — DFT templates, materials, pseudopotentials, and helper assets
- `lammps/` — MD input files, data files, and potentials
- `docs/` — theory, API, development, and architecture documentation
- `tests/` — CLI smoke tests

## Why This Is Intentional

QMatSim is a research and HPC workflow repository, not just a Python library.
The code package lives alongside large domain-specific simulation assets and
shell automation that are part of the canonical workflow surface.

For this repo shape, a rooted package is clearer than inserting an additional
`src/` boundary.

## Rules

- Keep Python importable code under `qmatsim/`.
- Do not create a second package root under `src/` without an explicit
  migration plan.
- Keep DFT assets under `siesta/` and MD assets under `lammps/`.
- Keep workflow automation under `scripts/`.
- Update this document if the package boundary changes.
