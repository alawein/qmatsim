"""Shared fixtures for the qmatsim test suite.

Adds siesta/python-utilities to sys.path so tests can import convert, round,
etc. directly by module name without any packaging changes.
"""

import sys
import pytest
from pathlib import Path

# Make siesta/python-utilities importable in all test files
_UTIL_PATH = str(Path(__file__).parent.parent / "siesta" / "python-utilities")
if _UTIL_PATH not in sys.path:
    sys.path.insert(0, _UTIL_PATH)

# ---------------------------------------------------------------------------
# Minimal STRUCT_IN files for all four supported TMD materials.
# Format (SIESTA STRUCT_IN):
#   line 0-2 : lattice vectors (bohr)
#   line 3   : number of atoms
#   line 4+  : index  atomic_number  x  y  z  (fractional coords)
# ---------------------------------------------------------------------------

MOS2_STRUCT_IN = """\
3.161 0.000 0.000
-1.580 2.737 0.000
0.000 0.000 23.000
3
1 42 0.333333 0.666667 0.500000
2 16 0.666667 0.333333 0.380000
3 16 0.666667 0.333333 0.620000
"""

MOSE2_STRUCT_IN = """\
3.289 0.000 0.000
-1.644 2.849 0.000
0.000 0.000 23.000
3
1 42 0.333333 0.666667 0.500000
2 34 0.666667 0.333333 0.380000
3 34 0.666667 0.333333 0.620000
"""

WS2_STRUCT_IN = """\
3.153 0.000 0.000
-1.577 2.731 0.000
0.000 0.000 23.000
3
1 74 0.333333 0.666667 0.500000
2 16 0.666667 0.333333 0.380000
3 16 0.666667 0.333333 0.620000
"""

WSE2_STRUCT_IN = """\
3.282 0.000 0.000
-1.641 2.843 0.000
0.000 0.000 23.000
3
1 74 0.333333 0.666667 0.500000
2 34 0.666667 0.333333 0.380000
3 34 0.666667 0.333333 0.620000
"""


@pytest.fixture
def mos2_struct_file(tmp_path):
    f = tmp_path / "MoS2.STRUCT_IN"
    f.write_text(MOS2_STRUCT_IN)
    return f


@pytest.fixture
def mose2_struct_file(tmp_path):
    f = tmp_path / "MoSe2.STRUCT_IN"
    f.write_text(MOSE2_STRUCT_IN)
    return f


@pytest.fixture
def ws2_struct_file(tmp_path):
    f = tmp_path / "WS2.STRUCT_IN"
    f.write_text(WS2_STRUCT_IN)
    return f


@pytest.fixture
def wse2_struct_file(tmp_path):
    f = tmp_path / "WSe2.STRUCT_IN"
    f.write_text(WSE2_STRUCT_IN)
    return f


# ---------------------------------------------------------------------------
# LAMMPS data file fixture (minimal 1x1 primitive MoS2)
# ---------------------------------------------------------------------------

LAMMPS_DATA_1X1 = """\
# LAMMPS data file: 1x1 MoS2 primitive cell

3 atoms
2 atom types

0.0 3.18 xlo xhi
0.0 5.50 ylo yhi
0.0 40.0 zlo zhi

Masses

1 95.94  # Mo
2 32.065 # S

Atoms  # atomic

1 1 1.59 2.75 20.0       # Mo center
2 2 1.59 2.75 21.6       # S top
3 2 1.59 2.75 18.4       # S bottom
"""


@pytest.fixture
def lammps_data_file(tmp_path):
    """Minimal LAMMPS data file for 1x1 MoS2 primitive cell."""
    f = tmp_path / "1x1_primitive.data"
    f.write_text(LAMMPS_DATA_1X1)
    return f


# ---------------------------------------------------------------------------
# Project-root fixture for tests that need to mock the repo tree
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_project_root(tmp_path):
    """Create a minimal mock project root with scripts/ and lammps/ dirs."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    for script in [
        "run-DFT.sh",
        "run-MD.sh",
        "compress-MD.sh",
        "run-postprocessing.sh",
    ]:
        (scripts_dir / script).write_text("#!/bin/bash\ntrue")

    lammps_data = tmp_path / "lammps" / "data"
    lammps_data.mkdir(parents=True)

    lammps_in = tmp_path / "lammps" / "in"
    lammps_in.mkdir(parents=True)
    for inp in ["compress_y.in", "deformation.in", "minimization.in"]:
        (lammps_in / inp).write_text("# placeholder")

    return tmp_path
