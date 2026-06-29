---
type: canonical
last-reviewed: 2026-06-29
---

# Repository topology

**Archetype:** `python-research-package` (per [alawein fleet canon](https://github.com/alawein/alawein/blob/main/docs/governance/repo-topology-canon.md))

Rooted package layout (not `src/<pkg>/`). SIESTA and LAMMPS assets are first-class
workflow surfaces alongside the Python orchestration layer. See
[STRUCTURE_DECISION.md](STRUCTURE_DECISION.md).

## On-disk tree

```text
qmatsim/
├── qmatsim/                 # rooted Python package and CLI entrypoint
│   ├── __init__.py
│   └── __main__.py          # python -m qmatsim
├── scripts/                 # DFT/MD runners, SLURM, validation
├── siesta/                  # DFT templates, materials, pseudopotentials
│   ├── materials/
│   ├── io_templates/
│   └── python-utilities/
├── lammps/                  # MD inputs, data files, potentials
│   ├── in/
│   ├── data/
│   └── potentials/
├── docs/
│   ├── architecture.md      # solver boundaries (detail TBD)
│   └── architecture/
│       ├── topology.md      # this file
│       └── STRUCTURE_DECISION.md
├── tests/                   # CLI smoke tests
├── reports/
└── pyproject.toml
```

## Role boundaries

| Path | Role | Must not |
|------|------|----------|
| `qmatsim/` | Python orchestration and CLI | Replace SIESTA or LAMMPS solvers |
| `scripts/` | Shell automation, cluster jobs, validation | Become a second Python package root |
| `siesta/` | DFT inputs, materials, pseudopotentials | Hold private cluster credentials |
| `lammps/` | MD inputs, potentials, structure data | Mix unrelated Python modules |
| `tests/` | CLI and structure smoke tests | Require live HPC schedulers in CI |
| `docs/` | Theory, API, workflow documentation | Invent solver paths not on disk |

## Related

- [architecture.md](../architecture.md) — solver integration and workflow detail
- [STRUCTURE_DECISION.md](STRUCTURE_DECISION.md) — rooted-package rationale
- [README.research.md](https://github.com/alawein/alawein/blob/main/templates/scaffolding/README.research.md) — fleet research README contract
