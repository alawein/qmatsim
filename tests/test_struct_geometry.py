"""Unit tests for STRUCT_IN geometry and structure utilities.

Tests the structural properties of the TMD materials defined in conftest.py
fixtures, verifying lattice parameters, atomic positions, and geometric
relationships expected for monolayer transition metal dichalcogenides.
"""

import numpy as np
import numpy.testing as npt
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_struct_in(text):
    """Parse SIESTA STRUCT_IN format into structured data.

    Returns:
        dict with keys: lattice_vectors (3x3 array), num_atoms (int),
        atoms (list of dicts with id, atomic_number, x, y, z).
    """
    lines = [line for line in text.strip().split("\n") if line.strip()]

    lattice = np.array(
        [
            [float(x) for x in lines[0].split()],
            [float(x) for x in lines[1].split()],
            [float(x) for x in lines[2].split()],
        ]
    )

    num_atoms = int(lines[3].strip())

    atoms = []
    for line in lines[4 : 4 + num_atoms]:
        parts = line.split()
        atoms.append(
            {
                "id": int(parts[0]),
                "atomic_number": int(parts[1]),
                "x": float(parts[2]),
                "y": float(parts[3]),
                "z": float(parts[4]),
            }
        )

    return {"lattice_vectors": lattice, "num_atoms": num_atoms, "atoms": atoms}


# ---------------------------------------------------------------------------
# TMD lattice constants (expected values in Bohr, from literature)
# ---------------------------------------------------------------------------

EXPECTED_A = {
    "MoS2": 3.161,
    "MoSe2": 3.289,
    "WS2": 3.153,
    "WSe2": 3.282,
}

METAL_Z = {
    "Mo": 42,
    "W": 74,
}

NONMETAL_Z = {
    "S": 16,
    "Se": 34,
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestParseStructIn:
    """Tests for the STRUCT_IN parser itself."""

    def test_parse_lattice_shape(self, mos2_struct_file):
        data = parse_struct_in(mos2_struct_file.read_text())
        assert data["lattice_vectors"].shape == (3, 3)

    def test_parse_atom_count(self, mos2_struct_file):
        data = parse_struct_in(mos2_struct_file.read_text())
        assert data["num_atoms"] == 3

    def test_parse_atoms_length(self, mos2_struct_file):
        data = parse_struct_in(mos2_struct_file.read_text())
        assert len(data["atoms"]) == 3


class TestLatticeParameters:
    """Verify in-plane lattice constants for all four TMDs."""

    @pytest.mark.parametrize(
        "fixture_name,material",
        [
            ("mos2_struct_file", "MoS2"),
            ("mose2_struct_file", "MoSe2"),
            ("ws2_struct_file", "WS2"),
            ("wse2_struct_file", "WSe2"),
        ],
    )
    def test_a11_matches_expected(self, fixture_name, material, request):
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        a11 = data["lattice_vectors"][0, 0]
        npt.assert_allclose(a11, EXPECTED_A[material], atol=0.001)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_vacuum_layer_height(self, fixture_name, request):
        """All fixtures should have a33 = 23.0 (vacuum slab)."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        a33 = data["lattice_vectors"][2, 2]
        npt.assert_allclose(a33, 23.0)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_hexagonal_lattice_angle(self, fixture_name, request):
        """Second lattice vector should be at 120 degrees (hexagonal)."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        a1 = data["lattice_vectors"][0, :2]  # in-plane a1
        a2 = data["lattice_vectors"][1, :2]  # in-plane a2
        cos_angle = np.dot(a1, a2) / (np.linalg.norm(a1) * np.linalg.norm(a2))
        angle_deg = np.degrees(np.arccos(cos_angle))
        npt.assert_allclose(angle_deg, 120.0, atol=1.0)


class TestAtomicPositions:
    """Verify atom positions and species for the TMD monolayer fixtures."""

    def test_mos2_has_one_mo_two_s(self, mos2_struct_file):
        data = parse_struct_in(mos2_struct_file.read_text())
        z_nums = [a["atomic_number"] for a in data["atoms"]]
        assert z_nums.count(42) == 1  # Mo
        assert z_nums.count(16) == 2  # S

    def test_mose2_has_one_mo_two_se(self, mose2_struct_file):
        data = parse_struct_in(mose2_struct_file.read_text())
        z_nums = [a["atomic_number"] for a in data["atoms"]]
        assert z_nums.count(42) == 1  # Mo
        assert z_nums.count(34) == 2  # Se

    def test_ws2_has_one_w_two_s(self, ws2_struct_file):
        data = parse_struct_in(ws2_struct_file.read_text())
        z_nums = [a["atomic_number"] for a in data["atoms"]]
        assert z_nums.count(74) == 1  # W
        assert z_nums.count(16) == 2  # S

    def test_wse2_has_one_w_two_se(self, wse2_struct_file):
        data = parse_struct_in(wse2_struct_file.read_text())
        z_nums = [a["atomic_number"] for a in data["atoms"]]
        assert z_nums.count(74) == 1  # W
        assert z_nums.count(34) == 2  # Se

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_metal_at_midplane(self, fixture_name, request):
        """Metal atom should be at z = 0.5 (center of the slab)."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        metal_atoms = [a for a in data["atoms"] if a["atomic_number"] in (42, 74)]
        for atom in metal_atoms:
            npt.assert_allclose(atom["z"], 0.5, atol=0.01)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_chalcogens_symmetric_about_metal(self, fixture_name, request):
        """Chalcogen atoms should be symmetrically placed around z = 0.5."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        nonmetal_atoms = [a for a in data["atoms"] if a["atomic_number"] in (16, 34)]
        z_values = sorted([a["z"] for a in nonmetal_atoms])
        # Should be symmetric: z[0] + z[1] = 1.0
        npt.assert_allclose(z_values[0] + z_values[1], 1.0, atol=0.01)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_atom_ids_sequential(self, fixture_name, request):
        """Atom IDs should be 1, 2, 3 in order."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        ids = [a["id"] for a in data["atoms"]]
        assert ids == [1, 2, 3]

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_fractional_coords_in_unit_cell(self, fixture_name, request):
        """All fractional coordinates should be between 0 and 1."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        for atom in data["atoms"]:
            assert 0.0 <= atom["x"] <= 1.0, f"x out of range: {atom['x']}"
            assert 0.0 <= atom["y"] <= 1.0, f"y out of range: {atom['y']}"
            assert 0.0 <= atom["z"] <= 1.0, f"z out of range: {atom['z']}"


class TestLatticeVectorOrthogonality:
    """Verify expected orthogonality between lattice vectors."""

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_a3_orthogonal_to_a1(self, fixture_name, request):
        """Out-of-plane vector a3 should be perpendicular to a1."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        a1 = data["lattice_vectors"][0]
        a3 = data["lattice_vectors"][2]
        dot = np.dot(a1, a3)
        npt.assert_allclose(dot, 0.0, atol=1e-10)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "mos2_struct_file",
            "mose2_struct_file",
            "ws2_struct_file",
            "wse2_struct_file",
        ],
    )
    def test_a3_orthogonal_to_a2(self, fixture_name, request):
        """Out-of-plane vector a3 should be perpendicular to a2."""
        struct_file = request.getfixturevalue(fixture_name)
        data = parse_struct_in(struct_file.read_text())
        a2 = data["lattice_vectors"][1]
        a3 = data["lattice_vectors"][2]
        dot = np.dot(a2, a3)
        npt.assert_allclose(dot, 0.0, atol=1e-10)
