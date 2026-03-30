---
type: derived
source: ../../../README.md
sync: manual
sla: manual
---

# GGA-SOC Pseudopotentials

This directory contains pseudopotentials for SIESTA calculations using the Generalized Gradient Approximation (GGA) with Spin-Orbit Coupling (SOC) effects included.

## Contents

- **Elements Covered**: Complete periodic table coverage with spin-orbit coupling
- **Functional**: PBE-GGA with relativistic corrections
- **SOC**: Fully relativistic pseudopotentials including spin-orbit coupling
- **File Formats**: 
  - `.psf` - SIESTA native format with SOC
  - `.psml` - PSML format with relativistic corrections
  - `.upf` - UPF format with spin-orbit coupling

## When to Use GGA-SOC

Use these pseudopotentials for calculations where spin-orbit coupling is important:

- **Heavy elements** (Z > 50): Significant SOC effects
- **2D materials with heavy atoms**: TMDCs containing Mo, W, etc.
- **Topological materials**: Where SOC drives topological phases
- **Accurate band gap calculations**: SOC often affects band gaps significantly

## Usage

SOC calculations can be enabled through the template processor:

```bash
# Set SOC=true in your calculation
export SOC_ENABLED=true
scripts/template-processor.sh create MoS2 Relaxation 0 ./soc_calculation
```

## Performance Notes

� **Warning**: SOC calculations are significantly more expensive than scalar-relativistic calculations:
- 2-4x longer computation time
- 2x memory usage
- Complex wavefunctions (double storage)

## Material Applications

Particularly important for:
- **MoS2, MoSe2**: Valence band splitting (~150 meV)
- **WS2, WSe2**: Larger SOC effects (~400 meV) 
- **Topological insulators**: Bi�Se�, Bi�Te�
- **Weyl semimetals**: TaAs, NbAs

## References

- "Spin-orbit coupling in transition metal dichalcogenides" Phys. Rev. B 84, 153402 (2011)
- "Giant spin-orbit-induced spin splitting in two-dimensional transition-metal dichalcogenide semiconductors" Phys. Rev. B 84, 153402 (2011)
