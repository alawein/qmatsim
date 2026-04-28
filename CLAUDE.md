---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# CLAUDE.md — QMatSim

## Workspace identity

QMatSim is a research-library repo for strain engineering in 2D materials using
SIESTA and LAMMPS. The Python surface orchestrates those workflows; it does not
erase the DFT and MD boundaries that make the scientific workflow legible.

Shared voice and research-writing contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

## Directory structure

- `qmatsim/`: canonical Python package and CLI
- `siesta/`: DFT templates, materials, and supporting assets
- `lammps/`: MD inputs, potentials, and supporting assets
- `scripts/`: setup, validation, and SLURM automation
- `tests/`: required verification
- `docs/`: theory, API, development, and architecture material

## Governance rules

1. Keep the canonical Python import surface rooted at `qmatsim/`.
2. Do not introduce a parallel `src/` tree without an explicit migration
   decision.
3. Treat `siesta/` and `lammps/` as first-class scientific surfaces.
4. Keep both backends working where the repo claims dual support.
5. Do not hardcode machine-specific HPC paths into reusable workflows.
6. Preserve SLURM templates and resource assumptions as explicit configuration,
   not hidden constants.
7. The repo should describe what the solver stack is doing, not hide it behind
   vague automation language.

## Code conventions

- Public Python behavior lives under `qmatsim/`.
- Comments explain material, geometry, strain, or scheduler assumptions.
- Keep docs and commands explicit about which backend a workflow touches.
- Type hints and accurate docstrings on public Python surfaces.

## Build and test commands

```bash
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
black qmatsim/
flake8 qmatsim/
mypy qmatsim/
```
