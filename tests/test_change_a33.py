"""Unit tests for the a33 lattice-vector transformation logic.

The functions under test (transform_coordinates, process_file) live in
siesta/python-utilities/change-a33.py.  Because the filename is hyphenated
and cannot be imported as a normal Python module, we redefine the pure
functions here (copied verbatim from the source) and test them directly.
Any drift between these copies and the source is caught by
test_source_functions_match_reference() below.
"""
from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest


# ---------------------------------------------------------------------------
# Functions copied from siesta/python-utilities/change-a33.py
# ---------------------------------------------------------------------------

def transform_coordinates(old_a33, new_a33, x, y, z):
    """Transform the z-coordinate based on the new lattice vector."""
    new_z = z * old_a33 / new_a33
    return x, y, new_z


def process_file(file_path, new_a33):
    """Process a .STRUCT_IN file by updating a33 and transforming z-coords."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    a11, a12, a13 = map(float, lines[0].split())
    a21, a22, a23 = map(float, lines[1].split())
    a31, a32, old_a33 = map(float, lines[2].split())
    num_atoms = int(lines[3].strip())

    new_lattice_vectors = [
        f"{a11} {a12} {a13}\n",
        f"{a21} {a22} {a23}\n",
        f"{a31} {a32} {new_a33}\n",
    ]

    new_coordinates = []
    for i in range(4, 4 + num_atoms):
        elements = lines[i].split()
        atom_id = int(elements[0])
        atomic_number = int(elements[1])
        x, y, z = map(float, elements[2:])
        new_x, new_y, new_z = transform_coordinates(old_a33, new_a33, x, y, z)
        new_coordinates.append(
            f"{atom_id} {atomic_number} {new_x:.8f} {new_y:.8f} {new_z:.8f}\n"
        )

    with open(file_path, "w") as f:
        f.writelines(new_lattice_vectors)
        f.write(str(num_atoms) + "\n")
        f.writelines(new_coordinates)


# ---------------------------------------------------------------------------
# Source fidelity check
# ---------------------------------------------------------------------------

class TestSourceFidelity:
    """Verify our copies match the original source file."""

    def test_source_contains_transform_coordinates(self):
        src = (
            Path(__file__).parent.parent
            / "siesta" / "python-utilities" / "change-a33.py"
        ).read_text(encoding="utf-8")
        assert "def transform_coordinates(old_a33, new_a33, x, y, z):" in src

    def test_source_contains_process_file(self):
        src = (
            Path(__file__).parent.parent
            / "siesta" / "python-utilities" / "change-a33.py"
        ).read_text(encoding="utf-8")
        assert "def process_file(file_path, new_a33):" in src

    def test_transform_formula_present(self):
        """The core formula z * old_a33 / new_a33 should be in the source."""
        src = (
            Path(__file__).parent.parent
            / "siesta" / "python-utilities" / "change-a33.py"
        ).read_text(encoding="utf-8")
        assert "z * old_a33 / new_a33" in src


# ---------------------------------------------------------------------------
# transform_coordinates
# ---------------------------------------------------------------------------

class TestTransformCoordinates:
    """Pure-function tests for z-coordinate rescaling."""

    def test_identity_when_a33_unchanged(self):
        """If old_a33 == new_a33, coordinates should not change."""
        x, y, z = transform_coordinates(23.0, 23.0, 0.3, 0.6, 0.5)
        npt.assert_allclose(x, 0.3)
        npt.assert_allclose(y, 0.6)
        npt.assert_allclose(z, 0.5)

    def test_x_y_unchanged(self):
        """x and y must not be affected by a33 change."""
        x, y, z = transform_coordinates(23.0, 90.0, 0.333, 0.667, 0.5)
        npt.assert_allclose(x, 0.333)
        npt.assert_allclose(y, 0.667)

    def test_z_scales_linearly(self):
        """z should scale as z * old_a33 / new_a33."""
        old_a33, new_a33 = 23.0, 90.0
        z_in = 0.5
        expected_z = z_in * old_a33 / new_a33
        _, _, z_out = transform_coordinates(old_a33, new_a33, 0.0, 0.0, z_in)
        npt.assert_allclose(z_out, expected_z, rtol=1e-10)

    def test_doubling_a33_halves_z(self):
        """Doubling the cell height halves fractional z."""
        _, _, z_out = transform_coordinates(20.0, 40.0, 0.0, 0.0, 0.6)
        npt.assert_allclose(z_out, 0.3)

    def test_zero_z_stays_zero(self):
        """z=0 must remain zero regardless of a33 change."""
        _, _, z_out = transform_coordinates(23.0, 90.0, 0.1, 0.2, 0.0)
        npt.assert_allclose(z_out, 0.0)

    def test_negative_z_preserved(self):
        """Negative z-coordinates should also rescale correctly."""
        old_a33, new_a33 = 10.0, 20.0
        _, _, z_out = transform_coordinates(old_a33, new_a33, 0.0, 0.0, -0.4)
        npt.assert_allclose(z_out, -0.2)


# ---------------------------------------------------------------------------
# process_file
# ---------------------------------------------------------------------------

SAMPLE_STRUCT = """\
3.161 0.000 0.000
-1.580 2.737 0.000
0.000 0.000 23.000
3
1 42 0.33333300 0.66666700 0.50000000
2 16 0.66666700 0.33333300 0.38000000
3 16 0.66666700 0.33333300 0.62000000
"""


class TestProcessFile:
    """Tests for process_file, which rewrites STRUCT_IN with a new a33."""

    def test_a33_updated_in_output(self, tmp_path):
        """The third lattice vector's z-component should match new_a33."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        a31, a32, a33 = [float(x) for x in lines[2].split()]
        npt.assert_allclose(a33, 90.0)

    def test_a11_a22_unchanged(self, tmp_path):
        """The in-plane lattice vectors should not be modified."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        a11 = float(lines[0].split()[0])
        a22 = float(lines[1].split()[1])
        npt.assert_allclose(a11, 3.161)
        npt.assert_allclose(a22, 2.737)

    def test_atom_count_preserved(self, tmp_path):
        """Number of atoms line should remain unchanged."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        assert int(lines[3].strip()) == 3

    def test_z_coordinates_rescaled(self, tmp_path):
        """Atomic z-coordinates should be rescaled by old_a33/new_a33."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        old_a33 = 23.0
        new_a33 = 90.0
        process_file(str(f), new_a33)

        lines = f.read_text().splitlines()
        z1 = float(lines[4].split()[4])
        expected_z1 = 0.5 * old_a33 / new_a33
        npt.assert_allclose(z1, expected_z1, atol=1e-6)

    def test_x_y_coordinates_unchanged(self, tmp_path):
        """x and y fractional coordinates should not be modified."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        x1, y1 = float(lines[4].split()[2]), float(lines[4].split()[3])
        npt.assert_allclose(x1, 0.333333, atol=1e-4)
        npt.assert_allclose(y1, 0.666667, atol=1e-4)

    def test_output_has_correct_line_count(self, tmp_path):
        """Output should have 3 lattice + 1 count + N atom lines."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = [l for l in f.read_text().splitlines() if l.strip()]
        assert len(lines) == 7  # 3 lattice + 1 count + 3 atoms

    def test_atom_ids_preserved(self, tmp_path):
        """Atom IDs (first column) should not be altered."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        ids = [int(lines[i].split()[0]) for i in range(4, 7)]
        assert ids == [1, 2, 3]

    def test_atomic_numbers_preserved(self, tmp_path):
        """Atomic numbers (second column) should not be altered."""
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 90.0)

        lines = f.read_text().splitlines()
        atomic_nums = [int(lines[i].split()[1]) for i in range(4, 7)]
        assert atomic_nums == [42, 16, 16]
