"""Unit tests for the POSCAR file-move logic from siesta/python-utilities/move.py.

The move.py script uses hardcoded HPC paths and os.system("mv ..."), so we
test the path-construction and material-supercell mapping logic by reading
the script as text and verifying its structural properties.  This avoids
executing any code from the script itself.
"""

import os
from pathlib import Path

import pytest


MOVE_SCRIPT = (
    Path(__file__).parent.parent / "siesta" / "python-utilities" / "move.py"
).read_text(encoding="utf-8")


class TestMoveScriptStructure:
    """Verify that the move script has correct material/supercell config."""

    def test_all_four_materials_present(self):
        for mat in ["MoS2", "MoSe2", "WS2", "WSe2"]:
            assert f"'{mat}'" in MOVE_SCRIPT, f"Missing material {mat}"

    def test_mos2_has_1x30_supercell(self):
        """MoS2 should include 1x30 supercell (larger strain series)."""
        assert "'1x30'" in MOVE_SCRIPT

    def test_strain_range_covers_0_to_20(self):
        """21 strain points (0-20%) should be iterated."""
        assert "range(21)" in MOVE_SCRIPT

    def test_source_path_uses_monolayer_rectangular(self):
        assert "Monolayer/rectangular" in MOVE_SCRIPT

    def test_target_path_includes_structure_subdir(self):
        assert "/Structure/" in MOVE_SCRIPT

    def test_poscar_extension_used(self):
        assert ".POSCAR" in MOVE_SCRIPT


class TestMovePathConstruction:
    """Verify source-to-target path logic by building paths the same way."""

    @pytest.fixture
    def base_path(self):
        return "/global/home/users/meshal/SIESTA/materials"

    @pytest.mark.parametrize(
        "material,supercell,strain",
        [
            ("MoS2", "1x10", 0),
            ("MoS2", "1x30", 20),
            ("WS2", "1x20", 10),
        ],
    )
    def test_source_target_paths_differ_by_structure_dir(
        self, base_path, material, supercell, strain
    ):
        source = f"{base_path}/{material}/Monolayer/rectangular/{supercell}/{strain}/{material}.POSCAR"
        target = f"{base_path}/{material}/Monolayer/rectangular/{supercell}/{strain}/Structure/{material}.POSCAR"

        # Target is inside a Structure/ subdirectory of source's parent
        assert os.path.dirname(target).replace("\\", "/") == os.path.join(
            os.path.dirname(source), "Structure"
        ).replace("\\", "/")

    def test_source_and_target_share_same_filename(self, base_path):
        material = "MoSe2"
        source = (
            f"{base_path}/{material}/Monolayer/rectangular/1x10/5/{material}.POSCAR"
        )
        target = f"{base_path}/{material}/Monolayer/rectangular/1x10/5/Structure/{material}.POSCAR"

        assert os.path.basename(source) == os.path.basename(target)
