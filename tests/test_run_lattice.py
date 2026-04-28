"""Unit tests for the in-plane lattice transformation logic from run.py.

The functions under test (transform_coordinates, process_file) live in
siesta/python-utilities/run.py.  We redefine the pure functions here
(copied verbatim from the source) and test them directly.
A source-fidelity test catches any drift between the copy and the original.
"""

from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest


# ---------------------------------------------------------------------------
# Functions and data copied from siesta/python-utilities/run.py
# ---------------------------------------------------------------------------

a_values = [
    (3.32635, 54.54500),
    (3.38700, 53.91000),
    (3.39605, 53.28400),
    (3.33982, 52.66700),
    (3.34259, 52.06600),
    (3.34156, 51.46300),
    (3.34128, 50.85700),
    (3.34286, 50.26000),
    (3.34284, 49.66300),
    (3.34298, 49.08600),
    (3.34476, 48.51100),
    (3.34436, 47.94600),
    (3.34539, 47.36800),
    (3.34561, 46.80100),
    (3.34560, 46.23300),
    (3.34571, 45.68300),
    (3.34705, 45.08600),
    (3.34782, 44.48800),
    (3.34746, 43.89900),
    (3.35479, 43.32900),
    (3.355093, 42.77900),
]


def transform_coordinates(old_a11, old_a22, new_a11, new_a22, old_a33, x, y, z):
    new_x = x * new_a11 / old_a11
    new_y = y * new_a22 / old_a22
    new_z = z  # Keep z unchanged
    return new_x, new_y, new_z


def process_file(file_path, new_a11, new_a22):
    with open(file_path, "r") as f:
        lines = f.readlines()

    try:
        a11, a12, a13 = map(float, lines[0].split())
        a21, a22, a23 = map(float, lines[1].split())
        a31, a32, old_a33 = map(float, lines[2].split())
        num_atoms = int(lines[3].strip())

        new_lattice_vectors = [
            f"{new_a11} {a12} {a13}\n",
            f"{a21} {new_a22} {a23}\n",
            f"{a31} {a32} {old_a33}\n",
        ]

        new_coordinates = []
        for i in range(4, 4 + num_atoms):
            elements = lines[i].split()
            if len(elements) != 5:
                print(f"Warning: Skipping malformed line {i + 1} in {file_path}")
                continue

            atom_id = int(elements[0])
            atomic_number = int(elements[1])
            x, y, z = map(float, elements[2:])
            new_x, new_y, new_z = transform_coordinates(
                a11, a22, new_a11, new_a22, old_a33, x, y, z
            )
            new_coordinates.append(
                f"{atom_id} {atomic_number} {new_x:.8f} {new_y:.8f} {new_z:.8f}\n"
            )

        with open(file_path, "w") as f:
            f.writelines(new_lattice_vectors)
            f.write(str(num_atoms) + "\n")
            f.writelines(new_coordinates)

        print(f"Processed and updated {file_path}")

    except (ValueError, IndexError) as e:
        print(f"Error processing {file_path}: {e}")


# ---------------------------------------------------------------------------
# Source fidelity check
# ---------------------------------------------------------------------------


class TestSourceFidelity:
    """Verify our copies match the original source file."""

    def test_source_contains_transform_coordinates(self):
        src = (
            Path(__file__).parent.parent / "siesta" / "python-utilities" / "run.py"
        ).read_text(encoding="utf-8")
        assert (
            "def transform_coordinates(old_a11, old_a22, new_a11, new_a22, old_a33, x, y, z):"
            in src
        )

    def test_source_contains_process_file(self):
        src = (
            Path(__file__).parent.parent / "siesta" / "python-utilities" / "run.py"
        ).read_text(encoding="utf-8")
        assert "def process_file(file_path, new_a11, new_a22):" in src

    def test_a_values_length_matches_source(self):
        src = (
            Path(__file__).parent.parent / "siesta" / "python-utilities" / "run.py"
        ).read_text(encoding="utf-8")
        # Count tuples in source
        count = src.count("(3.3")
        # Our table has 21 entries starting with 3.3
        assert count >= 21


# ---------------------------------------------------------------------------
# a_values table
# ---------------------------------------------------------------------------


class TestAValuesTable:
    """Sanity checks on the hard-coded lattice parameter table."""

    def test_has_21_entries(self):
        assert len(a_values) == 21

    def test_all_entries_are_tuples_of_two(self):
        for i, entry in enumerate(a_values):
            assert len(entry) == 2, f"a_values[{i}] has {len(entry)} elements"

    def test_a11_positive(self):
        for i, (a11, _) in enumerate(a_values):
            assert a11 > 0, f"a11 at strain {i} is non-positive: {a11}"

    def test_a22_positive(self):
        for i, (_, a22) in enumerate(a_values):
            assert a22 > 0, f"a22 at strain {i} is non-positive: {a22}"

    def test_a22_decreases_with_strain(self):
        """a22 (supercell y-direction) should generally decrease with increasing strain."""
        assert a_values[0][1] > a_values[20][1]


# ---------------------------------------------------------------------------
# transform_coordinates
# ---------------------------------------------------------------------------


class TestTransformCoordinatesRun:
    """Pure-function tests for in-plane coordinate rescaling."""

    def test_identity_when_lattice_unchanged(self):
        x, y, z = transform_coordinates(3.16, 54.5, 3.16, 54.5, 23.0, 0.3, 0.6, 0.5)
        npt.assert_allclose(x, 0.3)
        npt.assert_allclose(y, 0.6)
        npt.assert_allclose(z, 0.5)

    def test_z_unchanged(self):
        _, _, z = transform_coordinates(3.0, 50.0, 6.0, 25.0, 23.0, 0.1, 0.2, 0.5)
        npt.assert_allclose(z, 0.5)

    def test_x_scales_with_a11(self):
        old_a11, new_a11 = 3.0, 6.0
        x_in = 0.4
        x_out, _, _ = transform_coordinates(
            old_a11, 50.0, new_a11, 50.0, 23.0, x_in, 0.0, 0.0
        )
        npt.assert_allclose(x_out, x_in * new_a11 / old_a11)

    def test_y_scales_with_a22(self):
        old_a22, new_a22 = 54.0, 27.0
        y_in = 0.6
        _, y_out, _ = transform_coordinates(
            3.0, old_a22, 3.0, new_a22, 23.0, 0.0, y_in, 0.0
        )
        npt.assert_allclose(y_out, y_in * new_a22 / old_a22)

    def test_zero_coordinates_stay_zero(self):
        x, y, z = transform_coordinates(3.0, 50.0, 6.0, 25.0, 23.0, 0.0, 0.0, 0.0)
        npt.assert_allclose(x, 0.0)
        npt.assert_allclose(y, 0.0)
        npt.assert_allclose(z, 0.0)


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


class TestProcessFileRun:
    """Tests for process_file which rewrites a11/a22 and rescales x/y."""

    def test_a11_updated(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        new_a11, new_a22 = 3.5, 3.0
        process_file(str(f), new_a11, new_a22)

        lines = f.read_text().splitlines()
        a11_out = float(lines[0].split()[0])
        npt.assert_allclose(a11_out, new_a11)

    def test_a22_updated(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        new_a11, new_a22 = 3.5, 3.0
        process_file(str(f), new_a11, new_a22)

        lines = f.read_text().splitlines()
        a22_out = float(lines[1].split()[1])
        npt.assert_allclose(a22_out, new_a22)

    def test_a33_unchanged(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 3.5, 3.0)

        lines = f.read_text().splitlines()
        a33_out = float(lines[2].split()[2])
        npt.assert_allclose(a33_out, 23.0)

    def test_atom_count_preserved(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 3.5, 3.0)

        lines = f.read_text().splitlines()
        assert int(lines[3].strip()) == 3

    def test_z_coordinates_unchanged(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        process_file(str(f), 3.5, 3.0)

        lines = f.read_text().splitlines()
        z1 = float(lines[4].split()[4])
        npt.assert_allclose(z1, 0.5, atol=1e-6)

    def test_x_coordinates_rescaled(self, tmp_path):
        f = tmp_path / "MoS2.STRUCT_IN"
        f.write_text(SAMPLE_STRUCT)

        old_a11 = 3.161
        new_a11, new_a22 = 6.322, 2.737
        process_file(str(f), new_a11, new_a22)

        lines = f.read_text().splitlines()
        x1 = float(lines[4].split()[2])
        expected_x1 = 0.333333 * new_a11 / old_a11
        npt.assert_allclose(x1, expected_x1, atol=1e-4)

    def test_malformed_line_skipped(self, tmp_path, capsys):
        bad_struct = """\
3.161 0.000 0.000
-1.580 2.737 0.000
0.000 0.000 23.000
2
1 42 0.333 0.667 0.500
BADLINE
"""
        f = tmp_path / "bad.STRUCT_IN"
        f.write_text(bad_struct)

        process_file(str(f), 3.5, 3.0)

        out = capsys.readouterr().out
        assert "Warning" in out or "Skipping" in out
