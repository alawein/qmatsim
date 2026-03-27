---
type: canonical
source: none
sync: none
sla: none
---

# GGA Pseudopotentials

This directory contains pseudopotentials for SIESTA calculations using the Generalized Gradient Approximation (GGA) exchange-correlation functional.

## Contents

- **Elements Covered**: Complete periodic table coverage including transition metals and main group elements
- **Functional**: PBE-GGA 
- **File Formats**: 
  - `.psf` - SIESTA native format
  - `.psml` - PSML (PSeudopotential Markup Language) format  
  - `.upf` - UPF (Unified Pseudopotential Format)

## Usage

These pseudopotentials are automatically selected when running GGA calculations through the QMatSim framework:

```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
```

The framework automatically maps materials to their constituent elements and selects the appropriate pseudopotentials.

## Material Mappings

- **MoS2**: Mo.psf, S.psf
- **MoSe2**: Mo.psf, Se.psf  
- **WS2**: W.psf, S.psf
- **WSe2**: W.psf, Se.psf

## Quality and Validation

These pseudopotentials have been tested for:
- Convergence with respect to energy cutoff
- Transferability across different chemical environments
- Compatibility with 2D materials calculations

## References

Based on the pseudopotential library from the SIESTA project:
- https://siesta-project.org/siesta/
- "First-principles approach to material and nanosystem properties" Computer Physics Communications 180 (2009) 2582-2615