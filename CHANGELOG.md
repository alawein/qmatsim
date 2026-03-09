# Changelog

All notable changes to QMatSim will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- `docs/README.md` and `docs/architecture/STRUCTURE_DECISION.md` to document the
  canonical rooted-package research layout
- `scripts/validate-structure.py` to verify the repo’s package, domain, docs,
  and workflow boundaries

### Changed

- Standardized governance docs around the rooted `qmatsim/` package surface
- Documented `siesta/`, `lammps/`, and `scripts/` as intentional specialized
  surfaces, not layout drift

---

## [1.1.0] — 2026-03-06

### Added

- Workspace standardization (P1-P20) — governance files, CI, documentation

### Changed

- Consolidated configuration to `pyproject.toml`
- Added AGENTS.md governance rules
- Improved parameter documentation and error messages

---

## [1.0.0] — 2026-01-01

### Added

- QMatSim modular quantum materials simulation framework
- CLI interface for simulation configuration
- Comprehensive test suite
- Physical Review Materials citation reference
- Development guide and professional documentation

[Unreleased]: https://github.com/alawein/qmatsim/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/alawein/qmatsim/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/alawein/qmatsim/releases/tag/v1.0.0
