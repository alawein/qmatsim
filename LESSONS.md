---
type: lessons
authority: observed
audience: [ai-agents, contributors, future-self]
last-verified: 2026-03-09
last-updated: 2026-03-04
---

# LESSONS — QMatSim

> Observed patterns only. Minimal initial entry — update as lessons accumulate.

## Patterns That Work

- **Anchoring to the published paper (Alawein et al., Phys. Rev. Materials 2025)**: Using the paper's methods and results as the primary correctness reference prevents simulation drift from the validated computational framework.
- **Separating DFT (SIESTA) and MD (LAMMPS) pipeline stages**: These tools have different input formats, execution environments, and output schemas; keeping them as distinct pipeline stages makes debugging and partial reruns straightforward.

## Anti-Patterns

- **Running SLURM jobs without resource accounting**: HPC jobs without explicit memory/CPU limits get killed by the scheduler or starve other users; always specify `--mem`, `--ntasks`, and `--time`.
- **Hard-coding lattice constants**: Strain engineering workflows require varying lattice parameters systematically; any hard-coded value blocks parametric sweeps.

## Pitfalls

- **SIESTA and LAMMPS version incompatibility**: Input file syntax and pseudopotential formats change between versions; document the exact versions used for each published result.
- **Flat band identification is sensitive to k-point sampling**: Insufficient k-point density can make dispersive bands appear flat; always converge the k-grid before reporting flat band results.
