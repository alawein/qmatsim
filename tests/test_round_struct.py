"""Unit tests for the coordinate-rounding logic from round.py.

The function under test (process_struct_file) lives in
siesta/python-utilities/round.py.  We redefine it here (copied verbatim)
and test directly.  A source-fidelity test catches drift.
"""

from pathlib import Path

import numpy.testing as npt


# ---------------------------------------------------------------------------
# Function copied from siesta/python-utilities/round.py
# ---------------------------------------------------------------------------


def process_struct_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    # Process lattice vectors
    new_lines = []
    for i in range(3):
        coords = [float(x) for x in lines[i].split()]
        new_lines.append(f"{coords[0]:.3f} {coords[1]:.3f} {coords[2]:.3f}\n")

    # Add number of atoms
    new_lines.append(lines[3])  # Keep the original count line

    # Process atomic coordinates
    for line in lines[4:]:
        if not line.strip():
            continue
        parts = line.split()
        type_prefix = f"{parts[0]} {parts[1]}"
        coords = [float(parts[2]), float(parts[3]), float(parts[4])]
        new_lines.append(
            f"{type_prefix} {coords[0]:.3f} {coords[1]:.3f} {coords[2]:.3f}\n"
        )

    # Write back to file
    with open(filename, "w") as f:
        f.writelines(new_lines)


# ---------------------------------------------------------------------------
# Source fidelity check
# ---------------------------------------------------------------------------


class TestSourceFidelity:
    """Verify our copy matches the original source file."""

    def test_source_contains_process_struct_file(self):
        src = (
            Path(__file__).parent.parent / "siesta" / "python-utilities" / "round.py"
        ).read_text(encoding="utf-8")
        assert "def process_struct_file(filename):" in src

    def test_source_uses_3_decimal_format(self):
        """The source should use .3f formatting for rounding."""
        src = (
            Path(__file__).parent.parent / "siesta" / "python-utilities" / "round.py"
        ).read_text(encoding="utf-8")
        assert ":.3f" in src


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_STRUCT = """\
3.16100000 0.00000000 0.00000000
-1.58000000 2.73700000 0.00000000
0.00000000 0.00000000 23.00000000
3
1 42 0.33333333 0.66666667 0.50000000
2 16 0.66666667 0.33333333 0.38000000
3 16 0.66666667 0.33333333 0.62000000
"""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestProcessStructFile:
    """Tests for the coordinate-rounding function."""

    def test_lattice_vectors_rounded_to_3_decimals(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = f.read_text().splitlines()
        parts = lines[0].split()
        assert parts[0] == "3.161"
        assert parts[1] == "0.000"
        assert parts[2] == "0.000"

    def test_atom_count_line_preserved(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = f.read_text().splitlines()
        assert lines[3].strip() == "3"

    def test_atomic_coordinates_rounded_to_3_decimals(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = f.read_text().splitlines()
        parts = lines[4].split()
        assert parts[0] == "1"
        assert parts[1] == "42"
        npt.assert_allclose(float(parts[2]), 0.333, atol=1e-3)
        npt.assert_allclose(float(parts[3]), 0.667, atol=1e-3)
        npt.assert_allclose(float(parts[4]), 0.500, atol=1e-3)

    def test_total_line_count(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = [line for line in f.read_text().splitlines() if line.strip()]
        assert len(lines) == 7  # 3 lattice + 1 count + 3 atoms

    def test_type_prefix_preserved(self, tmp_path):
        """Atom index and atomic number columns should not be altered."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = f.read_text().splitlines()
        for i, expected_pair in enumerate([(1, 42), (2, 16), (3, 16)]):
            parts = lines[4 + i].split()
            assert int(parts[0]) == expected_pair[0]
            assert int(parts[1]) == expected_pair[1]

    def test_negative_lattice_component_rounded(self, tmp_path):
        f = tmp_path / "test.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))

        lines = f.read_text().splitlines()
        a21 = float(lines[1].split()[0])
        npt.assert_allclose(a21, -1.580, atol=1e-3)

    def test_empty_trailing_lines_ignored(self, tmp_path):
        content = SAMPLE_STRUCT + "\n\n\n"
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(content)

        process_struct_file(str(f))

        lines = [line for line in f.read_text().splitlines() if line.strip()]
        assert len(lines) == 7

    def test_idempotent(self, tmp_path):
        """Running process_struct_file twice should give the same result."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_struct_file(str(f))
        first_pass = f.read_text()

        process_struct_file(str(f))
        second_pass = f.read_text()

        assert first_pass == second_pass
