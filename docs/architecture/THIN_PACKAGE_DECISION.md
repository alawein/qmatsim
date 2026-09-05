---
type: canonical
last-reviewed: 2026-09-05
---

# Thin-package boundary decision

## Decision

QMatSim distributes a **thin Python CLI package**. The installed wheel contains
only importable Python code, typed-package metadata, and the small solver-free
verification fixture. It does not contain SIESTA/LAMMPS executables, templates,
pseudopotentials, material workspaces, solver outputs, or scheduler-specific
configuration.

## Rationale

Those scientific assets have independent licensing, runtime, platform, and
storage requirements. Bundling them into the wheel would make `pip install
QMatSim` appear to provide a runnable scientific workspace when it cannot.
Keeping the boundary explicit makes the package useful for CLI and installation
verification without making unsupported claims about solver availability.

## Operational model

- Install the CLI with `pip install QMatSim` (or editable install from a clone).
- Run `qmatsim verify-fixture` to check the installed package without solvers.
- Obtain, version, checksum, and document any scientific workspace/data bundle
  separately before running `relax`, `minimize`, or `analyze`.
- Configure solver locations, SLURM account/partition/mail settings, scratch
  roots, and pseudopotential roots locally. Do not commit machine-specific
  values.

## Non-goals and follow-up

This change does not certify, redistribute, or delete third-party binaries,
pseudopotentials, or large scientific inputs whose license or runtime role is
unclear. Maintainers must inventory those assets and publish a separately
versioned, checksummed, license-reviewed workspace/data bundle before claiming
end-to-end scientific reproduction.
