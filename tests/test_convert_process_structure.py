"""Unit tests for convert.process_structure() — the batch conversion orchestrator.

The existing test_convert.py covers struct_to_poscar(); this file tests
process_structure(), which coordinates file I/O around the converter.
All file operations use tmp_path — no HPC paths are accessed.
"""
import os
from pathlib import Path

import pytest

from convert import process_structure, struct_to_poscar


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_STRUCT_IN = """\
3.161 0.000 0.000
-1.580 2.737 0.000
0.000 0.000 23.000
3
1 42 0.333333 0.666667 0.500000
2 16 0.666667 0.333333 0.380000
3 16 0.666667 0.333333 0.620000
"""


def _build_struct_tree(base: Path, material: str, structure_type: str,
                       cell_type: str, supercell: str, strain: int) -> Path:
    """Create the directory tree and STRUCT_IN file, return the Structure dir."""
    struct_dir = (
        base / material / structure_type / cell_type / supercell / str(strain) / "Structure"
    )
    struct_dir.mkdir(parents=True, exist_ok=True)
    struct_file = struct_dir / f"{material}.STRUCT_IN"
    struct_file.write_text(SAMPLE_STRUCT_IN)
    return struct_dir


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestProcessStructure:
    """Tests for the per-configuration converter."""

    def test_creates_poscar_file(self, tmp_path):
        """A .POSCAR file should be written next to the .STRUCT_IN."""
        _build_struct_tree(tmp_path, "MoS2", "Monolayer", "rectangular", "1x10", 0)

        process_structure(str(tmp_path), "MoS2", "Monolayer", "rectangular", "1x10", 0)

        poscar = (
            tmp_path / "MoS2" / "Monolayer" / "rectangular" / "1x10" / "0"
            / "Structure" / "MoS2.POSCAR"
        )
        assert poscar.exists()

    def test_poscar_content_matches_converter(self, tmp_path):
        """Output should match what struct_to_poscar() produces."""
        struct_dir = _build_struct_tree(
            tmp_path, "MoS2", "Monolayer", "rectangular", "1x10", 5
        )
        struct_file = struct_dir / "MoS2.STRUCT_IN"

        process_structure(str(tmp_path), "MoS2", "Monolayer", "rectangular", "1x10", 5)

        poscar_file = struct_dir / "MoS2.POSCAR"
        expected = struct_to_poscar(str(struct_file), "MoS2")
        assert poscar_file.read_text() == expected

    def test_missing_struct_file_prints_not_found(self, tmp_path, capsys):
        """When STRUCT_IN is absent, should print 'File not found'."""
        # Create the directory but NOT the STRUCT_IN file
        struct_dir = (
            tmp_path / "WS2" / "Bulk" / "primitive" / "1x1" / "0" / "Structure"
        )
        struct_dir.mkdir(parents=True, exist_ok=True)

        process_structure(str(tmp_path), "WS2", "Bulk", "primitive", "1x1", 0)

        out = capsys.readouterr().out
        assert "File not found" in out

    def test_all_four_materials(self, tmp_path):
        """process_structure should handle all four TMD materials."""
        for material in ["MoS2", "MoSe2", "WS2", "WSe2"]:
            _build_struct_tree(tmp_path, material, "Monolayer", "rectangular", "1x1", 0)
            process_structure(
                str(tmp_path), material, "Monolayer", "rectangular", "1x1", 0
            )

            poscar = (
                tmp_path / material / "Monolayer" / "rectangular" / "1x1" / "0"
                / "Structure" / f"{material}.POSCAR"
            )
            assert poscar.exists(), f"POSCAR not created for {material}"

    def test_success_prints_converted_message(self, tmp_path, capsys):
        """Successful conversion should print a confirmation."""
        _build_struct_tree(tmp_path, "MoS2", "Bulk", "primitive", "1x1", 3)

        process_structure(str(tmp_path), "MoS2", "Bulk", "primitive", "1x1", 3)

        out = capsys.readouterr().out
        assert "Converted" in out
        assert "MoS2" in out

    @pytest.mark.parametrize("strain", [0, 10, 20])
    def test_multiple_strain_values(self, tmp_path, strain):
        """Various strain percentages should all produce POSCAR files."""
        _build_struct_tree(
            tmp_path, "MoS2", "Monolayer", "rectangular", "1x10", strain
        )
        process_structure(
            str(tmp_path), "MoS2", "Monolayer", "rectangular", "1x10", strain
        )

        poscar = (
            tmp_path / "MoS2" / "Monolayer" / "rectangular" / "1x10"
            / str(strain) / "Structure" / "MoS2.POSCAR"
        )
        assert poscar.exists()
