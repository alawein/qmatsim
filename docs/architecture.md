---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Architecture Overview -- qmatsim

QMatSim is a multiscale strain-engineering framework for 2D quantum materials. The Python
package and CLI (`qmatsim/`) are the orchestration layer; the actual computations run inside
SIESTA (DFT) and LAMMPS (MD), which are external scientific dependencies that must be installed
separately.

## Components

The repository has six canonical surfaces:

| Surface | Role |
|---|---|
| `qmatsim/` | Python package and CLI entrypoint (`__main__.py`, argparse subcommands) |
| `scripts/` | Bash automation: `run-DFT.sh`, `run-MD.sh`, `run-postprocessing.sh`, SLURM helpers |
| `siesta/` | DFT templates, structure files, and pseudopotentials (GGA, LDA, GGA-SOC) |
| `lammps/` | MD input scripts, atomic data files, and interatomic potentials |
| `docs/` | Theory, API, development, and architecture documentation |
| `tests/` | CLI smoke tests via subprocess |

The CLI exposes three subcommands: `relax` (delegates to `run-DFT.sh`), `minimize` (delegates to
`run-MD.sh`), and `analyze` (delegates to `run-postprocessing.sh`). Each script checks for the
required solver executable before running and exits with a descriptive message if it is missing.

## Data Flow

1. The user calls `qmatsim relax` or `qmatsim minimize` with a material and structure argument.
2. `qmatsim/__main__.py` resolves the correct bash script and passes the arguments.
3. The bash script locates the matching template in `siesta/io_templates/` or input file in
   `lammps/in/`, substitutes variables, and invokes the solver (`siesta` or `lmp_mpi`).
4. Outputs land in the strain-indexed directory under `siesta/materials/` or the working directory
   for LAMMPS runs. `qmatsim analyze` extracts results for postprocessing.

## Dependencies

Runtime dependencies (not bundled):

- **SIESTA 4.1+** -- DFT solver; the `siesta` executable must be on `PATH`.
- **LAMMPS** -- MD solver; the `lmp_mpi` executable must be on `PATH`.
- Python packages: `numpy`, `matplotlib` (see `pyproject.toml` for the full list).

Development dependencies: `pytest`, `black`, `flake8`, `mypy`.

## Constraints

- The package root is `qmatsim/`, not `src/qmatsim/`. See
  [architecture/STRUCTURE_DECISION.md](architecture/STRUCTURE_DECISION.md) for the explicit
  rationale.
- SIESTA and LAMMPS are external; their executables and associated data files are not committed to
  this repository.
- Private cluster paths, scheduler credentials, and machine-local outputs must not appear in
  committed examples.
- The material-structure-strain directory hierarchy (`siesta/materials/{material}/{type}/{structure}/{strain}/`)
  is intentional and must be preserved for the template substitution scripts to function.
