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
