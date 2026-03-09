# QMatSim

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SIESTA](https://img.shields.io/badge/SIESTA-4.1+-green.svg)](https://siesta-project.org/siesta/)
[![LAMMPS](https://img.shields.io/badge/LAMMPS-stable-red.svg)](https://www.lammps.org/)

Multiscale simulation framework for strain engineering in 2D materials.
QMatSim combines DFT (SIESTA) and MD (LAMMPS) calculations to study flat
bands, lateral heterostructures, and electronic phases in transition metal
dichalcogenides. It implements the computational framework from Alawein et al.,
*Physical Review Materials* 2025.

## Features

- Automated discovery of flat bands and lateral heterostructures
- DFT calculations with spin-orbit coupling for band engineering
- Systematic rippling and compression strain studies
- DFT-MD coupling for strain-electronic correlations
- SLURM automation with resource management
- Band structure and LDOS visualization tools
- Libraries for MoS2, MoSe2, WS2, and WSe2 systems

## Installation

### Prerequisites

- Python 3.9+ with NumPy and Matplotlib
- SIESTA 4.1+ for DFT calculations
- LAMMPS (stable) for MD simulations
- SLURM for HPC job submission when running cluster workflows

### Setup

```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e ".[dev]"
python -m qmatsim --help
python scripts/validate-structure.py
```

## Layout Model

QMatSim intentionally uses a **rooted package** layout rather than `src/`.

- `qmatsim/` is the canonical Python package and CLI surface.
- `siesta/` stores DFT templates, materials, and supporting utilities.
- `lammps/` stores MD inputs, data files, and potentials.
- `scripts/` stores workflow automation and setup helpers.
- `docs/` stores theory, API, development, and structure references.

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
for the canonical structure decision.

## Usage

```bash
# Strain-induced electronic structure (DFT)
qmatsim relax --material MoS2 --structure 1x10_rectangular

# Mechanical deformation studies (MD)
qmatsim minimize --structure 1x10_rectangular --mode compress

# Flat-band discovery and analysis
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Project Structure

```text
qmatsim/
├── qmatsim/            # Canonical Python package and CLI entrypoint
├── scripts/            # Setup, SLURM, and workflow automation
├── siesta/             # DFT infrastructure, templates, and materials
├── lammps/             # MD inputs, data files, and potentials
├── docs/               # Theory, API, development, and architecture docs
│   └── architecture/   # Structure decisions
└── tests/              # CLI smoke tests
```

## Validation

```bash
python scripts/validate-structure.py
python -m qmatsim --help
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
```

## Documentation

- [docs/README.md](docs/README.md)
- [docs/api.md](docs/api.md)
- [docs/dev-guide.md](docs/dev-guide.md)
- [docs/theory.md](docs/theory.md)

## Citation

```bibtex
@article{alawein2025strain,
  title={Strain-induced lateral heterostructures: Hole localization and the emergence of flat bands in rippled MoS2 monolayers},
  author={Alawein, Meshal and Ager, Joel W and Javey, Ali and Chrzan, DC},
  journal={Physical Review Materials},
  volume={9},
  number={2},
  pages={L021002},
  year={2025},
  publisher={APS}
}
```

## License

MIT License. See [LICENSE](LICENSE).
