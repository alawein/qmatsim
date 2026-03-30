---
type: derived
source: ../../../README.md
sync: manual
sla: manual
---

# LDA Pseudopotentials

This directory contains pseudopotentials for SIESTA calculations using the Local Density Approximation (LDA) exchange-correlation functional.

## Contents

- **Elements Covered**: Complete periodic table coverage
- **Functional**: Perdew-Zunger LDA (Ceperley-Alder parameterization)
- **File Formats**: 
  - `.psf` - SIESTA native format
  - `.psml` - PSML (PSeudopotential Markup Language) format
  - `.upf` - UPF (Unified Pseudopotential Format)

## When to Use LDA

LDA pseudopotentials are recommended for:

- **Historical comparisons**: Reproducing older literature results
- **Tight-binding parameterization**: LDA often used as reference
- **Fast preliminary calculations**: LDA is computationally faster than GGA
- **Specific materials**: Some systems are better described by LDA

## Performance vs Accuracy Trade-offs

**Advantages:**
-  Faster calculations than GGA
-  Good for metallic systems
-  Reasonable for structural properties

**Limitations:**
- L Underestimates bond lengths (~2-3%)
- L Overestimates binding energies
- L Poor description of van der Waals interactions
- L Less accurate for molecular systems

## Usage

LDA calculations can be selected by setting the functional:

```bash
# Set LDA functional in template processor
export XC_FUNCTIONAL=LDA  
export XC_AUTHORS=PZ
scripts/template-processor.sh create MoS2 Relaxation 0 ./lda_calculation
```

## Comparison Guidelines

For systematic studies, consider running both LDA and GGA calculations:

| Property | LDA Trend | GGA Trend | Recommended |
|----------|-----------|-----------|-------------|
| Lattice Constants | Underestimate | Good | GGA |
| Band Gaps | Underestimate | Better | GGA |
| Bulk Modulus | Overestimate | Good | GGA |
| Surface Energy | Reasonable | Better | GGA |

## References

- Perdew and Zunger, Phys. Rev. B 23, 5048 (1981) - LDA functional
- Ceperley and Alder, Phys. Rev. Lett. 45, 566 (1980) - Quantum Monte Carlo parameterization
- "Self-interaction correction to density-functional approximations for many-electron systems" Phys. Rev. B 23, 5048 (1981)
