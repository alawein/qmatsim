# QMatSim

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SIESTA](https://img.shields.io/badge/SIESTA-4.1+-green.svg)](https://siesta-project.org/siesta/)
[![LAMMPS](https://img.shields.io/badge/LAMMPS-stable-red.svg)](https://www.lammps.org/)

Multiscale simulation framework for strain engineering in 2D materials. Combines DFT (SIESTA) and MD (LAMMPS) calculations to study flat bands, lateral heterostructures, and electronic phases in transition metal dichalcogenides. Implements the computational framework from Alawein et al., *Physical Review Materials* 2025.

## Features

- Automated discovery of flat bands and lateral heterostructures
- DFT calculations with spin-orbit coupling for band engineering
- Systematic rippling and compression strain studies
- DFT-MD coupling for strain-electronic correlations
- SLURM automation with resource management
- Band structure and LDOS visualization tools
- Complete libraries for MoS2, MoSe2, WS2, WSe2 systems

## Installation

### Prerequisites
- Python 3.9+ with NumPy, Matplotlib
- SIESTA 4.1+ for DFT calculations
- LAMMPS (stable) for MD simulations
- SLURM (optional) for HPC job submission

### Setup
```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e .
qmatsim --help
```

## Usage

```bash
# Strain-Induced Electronic Structure (DFT)
qmatsim relax --material MoS2 --structure 1x10_rectangular

# Mechanical Deformation Studies (MD)
qmatsim minimize --structure ripple10 --mode compress

# Flat Band Discovery and Analysis
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Project Structure

```
qmatsim/
├── qmatsim/       # Core Python CLI framework
├── scripts/       # Bash automation tools
├── siesta/        # DFT calculation infrastructure
├── lammps/        # MD simulation infrastructure
├── tests/         # Test suite
└── docs/          # Documentation
```

## Testing

```bash
pytest tests/
python -m qmatsim --help
```

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

MIT License -- see [LICENSE](LICENSE).

## Author

**Meshal Alawein**
- Email: [contact@meshal.ai](mailto:contact@meshal.ai)
- GitHub: [github.com/alawein](https://github.com/alawein)
- LinkedIn: [linkedin.com/in/alawein](https://linkedin.com/in/alawein)
