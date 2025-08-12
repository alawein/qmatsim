# QMatSim: Advanced Strain Engineering Framework for 2D Quantum Materials 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SIESTA](https://img.shields.io/badge/SIESTA-4.1+-green.svg)](https://siesta-project.org/siesta/)
[![LAMMPS](https://img.shields.io/badge/LAMMPS-stable-red.svg)](https://www.lammps.org/)
[![Physical Review Materials](https://img.shields.io/badge/Phys.Rev.Materials-2025-brightgreen.svg)](https://journals.aps.org/prmaterials/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing--validation)

**Multiscale simulation framework for strain engineering in 2D materials. Combines DFT and MD calculations to study flat bands, lateral heterostructures, and electronic phases in transition metal dichalcogenides.**

## Capabilities

- Strain-induced flat band emergence and hole localization in 2D materials
- DFT calculations with spin-orbit coupling and band engineering  
- LAMMPS-based mechanical deformation and systematic strain protocols
- Transition metal dichalcogenides (TMDCs) with comprehensive material libraries
- DFT-MD integration for strain-electronic property correlations

## 📋 Overview

QMatSim implements the computational framework from "Strain-induced lateral heterostructures: Hole localization and the emergence of flat bands in rippled MoS₂ monolayers" (Alawein et al., *Physical Review Materials* 2025). The framework combines SIESTA density functional theory calculations with LAMMPS molecular dynamics simulations for studying strain effects in 2D materials.

Provides workflows from atomic-scale deformation to electronic structure analysis, focusing on flat band physics and lateral heterostructures in transition metal dichalcogenides.

## Features

- Automated discovery of flat bands and lateral heterostructures
- DFT calculations with spin-orbit coupling for band engineering
- Systematic rippling and compression strain studies
- DFT-MD coupling for strain-electronic correlations
- SLURM automation with resource management
- Band structure and LDOS visualization tools
- Complete libraries for MoS₂, MoSe₂, WS₂, WSe₂ systems

## Installation

### Prerequisites
- **Python 3.9+** with NumPy, Matplotlib
- **SIESTA 4.1+** for DFT calculations
- **LAMMPS** (stable) for MD simulations
- **SLURM** (optional) for HPC job submission

### Setup
```bash
# Clone the repository
git clone https://github.com/alaweimm90/QMatSim.git
cd QMatSim

# Install in development mode
pip install -e .

# Install additional dependencies
pip install numpy matplotlib pytest

# Verify installation
qmatsim --help
```

## Usage

```bash
# Strain-Induced Electronic Structure (DFT)
qmatsim relax --material MoS2 --structure 1x10_rectangular

# Mechanical Deformation Studies (MD)
qmatsim minimize --structure ripple10 --mode compress
qmatsim minimize --structure ripple10 --mode all

# Flat Band Discovery & Analysis
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Directory Structure

```
QMatSim/
├── qmatsim/                    # Core Python CLI framework
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # CLI entry point and argument parsing
│   └── py.typed               # Type hints marker
├── scripts/                    # Bash automation tools
│   ├── run-DFT.sh             # SIESTA workflow automation
│   ├── run-MD.sh              # LAMMPS simulation control
│   ├── run-postprocessing.sh  # Analysis pipeline automation
│   ├── template-*.sh          # Input file generation scripts
│   └── config.sh              # Configuration management
├── siesta/                     # DFT calculation infrastructure
│   ├── io_templates/          # SIESTA input file templates
│   ├── pseudopotentials/      # Element pseudopotentials (GGA/LDA/SOC)
│   ├── materials/             # Material-specific calculation setups
│   ├── python-utilities/      # Analysis and plotting scripts
│   └── bin/                   # SIESTA utilities and tools
├── lammps/                     # MD simulation infrastructure
│   ├── data/                  # Atomic structure files (.data format)
│   ├── in/                    # LAMMPS input scripts and protocols
│   └── potentials/            # Interatomic potential files
├── tests/                      # Test suite
│   ├── test_cli_basic.py      # Basic CLI functionality tests
│   └── test_qmatsim_cli.py    # Advanced CLI integration tests
├── docs/                       # Documentation
│   ├── dev-guide.md           # Development guide and architecture
│   └── index.md               # Documentation index
├── pyproject.toml             # Modern Python build configuration
├── setup.py                   # Legacy Python setup
└── LICENSE                    # MIT License
```

## Testing

```bash
# Run complete test suite
pytest tests/

# Run specific test modules
pytest tests/test_cli_basic.py
pytest tests/test_qmatsim_cli.py

# Test CLI functionality
python -m qmatsim --help

# Integration tests (requires SIESTA/LAMMPS installations)
qmatsim relax --help
qmatsim minimize --help
qmatsim analyze --help
```

### Validation Examples
- Flat band physics: reproduces strain-induced emergence in rippled MoS₂ (*Phys. Rev. Materials* 2025)
- Lateral heterostructures: hole localization and electronic phase transitions
- Strain engineering: systematic deformation studies up to 20% strain
- Spin-orbit effects: SOC-dependent band modifications in TMDCs
- Multiscale coupling: DFT-MD correlation studies

## Documentation

The `docs/` folder contains:
- `dev-guide.md`: development guide with architecture overview and testing
- Template system documentation: SIESTA input file generation and variable substitution
- Material libraries: TMDC parameters and pseudopotential usage

## Plotting Standards

Uses UC Berkeley color scheme:
- Berkeley Blue `#003262` (primary)
- California Gold `#FDB515` (accent)  
- Neutral Gray `#888888` (secondary)
- Publication quality: serif fonts, inward ticks, no grid
- Saves plots as `.pdf` and `.png` to `/plots/` directories

## Citation

If you use QMatSim in your research, please cite:

```bibtex
@article{alawein2025strain,
  title={Strain-induced lateral heterostructures: Hole localization and the emergence of flat bands in rippled MoS₂ monolayers},
  author={Alawein, Meshal and Ager, Joel W and Javey, Ali and Chrzan, DC},
  journal={Physical Review Materials},
  volume={9},
  number={2},
  pages={L021002},
  year={2025},
  publisher={APS}
}

@software{alawein2025qmatsim,
  author = {Meshal Alawein},
  title = {QMatSim: Advanced Strain Engineering Framework for 2D Quantum Materials},
  url = {https://github.com/alaweimm90/QMatSim},
  year = {2025},
  institution = {University of California, Berkeley}
}
```

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  
© 2025 Meshal Alawein – All rights reserved.

## Author

<div align="center">
<strong>Meshal Alawein</strong><br/>
<em>Computational Physicist & Research Scientist</em><br/>
University of California, Berkeley

📧 <a href="mailto:meshal@berkeley.edu" style="color:#003262;">meshal@berkeley.edu</a>

<a href="https://www.linkedin.com/in/meshal-alawein" title="LinkedIn">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn" height="32" />
</a>
<a href="https://github.com/alaweimm90" title="GitHub">
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub" height="32" />
</a>
<a href="https://malawein.com" title="Website">
  <img src="https://img.shields.io/badge/Website-003262?style=flat&logo=googlechrome&logoColor=white" alt="Website" height="32" />
</a>
<a href="https://scholar.google.com/citations?user=IB_E6GQAAAAJ&hl=en" title="Google Scholar">
  <img src="https://img.shields.io/badge/Scholar-4285F4?style=flat&logo=googlescholar&logoColor=white" alt="Scholar" height="32" />
</a>
<a href="https://simcore.dev" title="SimCore">
  <img src="https://img.shields.io/badge/SimCore-FDB515?style=flat&logo=atom&logoColor=white" alt="SimCore" height="32" />
</a>
</div>

---


*Making computational materials science more accessible.*
