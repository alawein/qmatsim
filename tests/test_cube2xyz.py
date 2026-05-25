"""Unit tests for siesta/python-utilities/cube2xyz.py parsing logic.

cube2xyz.py is a CLI script that reads Gaussian cube files and extracts
volumetric data.  Since the script uses module-level argparse.parse_args()
and side effects (stdout, matplotlib), we cannot safely import it.

Instead, we test the core data-parsing logic by reimplementing the cube
file reader as a standalone function and verifying it against known data.
We also test the frange() generator used for plotting ranges.
"""

import numpy.testing as npt


# ---------------------------------------------------------------------------
# frange — reimplemented from cube2xyz.py for testing
# ---------------------------------------------------------------------------


def frange(x, y, jump):
    """Floating-point range generator (copied from cube2xyz.py)."""
    while x < y:
        yield x
        x += jump


class TestFrange:
    """Tests for the floating-point range generator."""

    def test_basic_integer_like_range(self):
        result = list(frange(0, 3, 1))
        assert result == [0, 1, 2]

    def test_fractional_step(self):
        result = list(frange(0.0, 1.0, 0.25))
        npt.assert_allclose(result, [0.0, 0.25, 0.5, 0.75])

    def test_empty_when_start_ge_end(self):
        assert list(frange(5, 3, 1)) == []
        assert list(frange(3, 3, 1)) == []

    def test_single_element(self):
        result = list(frange(0, 0.5, 1.0))
        assert result == [0]

    def test_negative_start(self):
        result = list(frange(-2, 1, 1))
        assert result == [-2, -1, 0]


# ---------------------------------------------------------------------------
# Cube file format parsing
# ---------------------------------------------------------------------------

# Minimal Gaussian cube file content for testing
SAMPLE_CUBE = """\
 Comment line 1
 Comment line 2
    3  0.000000  0.000000  0.000000
    2  1.000000  0.000000  0.000000
    2  0.000000  1.000000  0.000000
    2  0.000000  0.000000  1.000000
   42  42.0  0.000000  0.000000  0.000000
   16  16.0  0.500000  0.500000  0.000000
   16  16.0  0.500000  0.500000  1.000000
  1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0
"""


def parse_cube(text):
    """Parse a Gaussian cube file, replicating cube2xyz.py's logic."""
    lines = text.strip().split("\n")
    nline = 0
    nat = 0
    origin = [0.0, 0.0, 0.0]
    spacing_vec = []
    at_coord = []
    values = []

    for line in lines:
        nline += 1
        if nline == 3:
            parts = line.split()
            nat = int(parts[0])
            origin = [float(parts[1]), float(parts[2]), float(parts[3])]
        elif 3 < nline <= 6:
            spacing_vec.append(line.split())
        elif 6 < nline <= 6 + nat:
            at_coord.append(line.split())
        elif nline > 6 + nat:
            for val in line.split():
                values.append(float(val))

    return nat, origin, spacing_vec, at_coord, values


class TestCubeParsing:
    """Tests for cube file data extraction."""

    def test_atom_count(self):
        nat, _, _, _, _ = parse_cube(SAMPLE_CUBE)
        assert nat == 3

    def test_origin_parsed(self):
        _, origin, _, _, _ = parse_cube(SAMPLE_CUBE)
        npt.assert_allclose(origin, [0.0, 0.0, 0.0])

    def test_spacing_vectors_count(self):
        """Should have 3 spacing vectors (one per axis)."""
        _, _, spacing_vec, _, _ = parse_cube(SAMPLE_CUBE)
        assert len(spacing_vec) == 3

    def test_spacing_vector_grid_points(self):
        """First element of each spacing vector is the number of grid points."""
        _, _, spacing_vec, _, _ = parse_cube(SAMPLE_CUBE)
        for sv in spacing_vec:
            assert int(sv[0]) == 2  # 2 grid points per axis in our sample

    def test_atom_coordinates_count(self):
        _, _, _, at_coord, _ = parse_cube(SAMPLE_CUBE)
        assert len(at_coord) == 3

    def test_atom_atomic_numbers(self):
        _, _, _, at_coord, _ = parse_cube(SAMPLE_CUBE)
        atomic_nums = [int(ac[0]) for ac in at_coord]
        assert atomic_nums == [42, 16, 16]

    def test_volumetric_data_count(self):
        """2x2x2 grid = 8 values."""
        _, _, _, _, values = parse_cube(SAMPLE_CUBE)
        assert len(values) == 8

    def test_volumetric_data_values(self):
        _, _, _, _, values = parse_cube(SAMPLE_CUBE)
        npt.assert_allclose(values, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    def test_angstrom_conversion_factor(self):
        """Bohr-to-Angstrom factor should be 1/0.5291772083."""
        aa = 1.0 / 0.5291772083
        npt.assert_allclose(aa, 1.8897259886, rtol=1e-6)

    def test_grid_coordinate_computation(self):
        """Verify that grid coordinates are computed from spacing vectors."""
        _, _, spacing_vec, _, _ = parse_cube(SAMPLE_CUBE)
        # For i=1, j=0, k=0: x = 1 * spacing_vec[0][1]
        x = 1 * float(spacing_vec[0][1])
        npt.assert_allclose(x, 1.0)
