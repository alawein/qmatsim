"""Unit tests for siesta/python-utilities/convert.py.

Tests struct_to_poscar(), which converts SIESTA STRUCT_IN files to the
VASP POSCAR format.  The function is pure (read file → return string) so
every test below uses only tmp_path fixtures — no mocks, no subprocess.
"""
import pytest
from convert import struct_to_poscar


class TestPoscarOutputFormat:
    """POSCAR structural requirements independent of material."""

    def test_returns_string(self, mos2_struct_file):
        assert isinstance(struct_to_poscar(str(mos2_struct_file), "MoS2"), str)

    def test_title_line_contains_material(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        assert result.splitlines()[0] == "MoS2 structure"

    def test_scale_factor_is_1(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        assert result.splitlines()[1].strip() == "1.0"

    def test_direct_keyword_present(self, mos2_struct_file):
        assert "Direct" in struct_to_poscar(str(mos2_struct_file), "MoS2")

    def test_minimum_line_count(self, mos2_struct_file):
        # title + scale + 3 lattice vecs + species + counts + Direct + 3 atoms = 11
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        assert len(result.splitlines()) >= 11

    def test_lattice_vectors_preserved(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        # First lattice vector from the fixture
        assert "3.161 0.000 0.000" in result

    def test_coordinates_are_six_decimal_places(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        assert "0.333333" in result
        assert "0.666667" in result


class TestMaterialSpeciesAssignment:
    """Correct metal / nonmetal labels and ordering for all four TMDs."""

    def test_mos2_species_labels(self, mos2_struct_file):
        assert "Mo S" in struct_to_poscar(str(mos2_struct_file), "MoS2")

    def test_mose2_species_labels(self, mose2_struct_file):
        assert "Mo Se" in struct_to_poscar(str(mose2_struct_file), "MoSe2")

    def test_ws2_species_labels(self, ws2_struct_file):
        assert "W S" in struct_to_poscar(str(ws2_struct_file), "WS2")

    def test_wse2_species_labels(self, wse2_struct_file):
        assert "W Se" in struct_to_poscar(str(wse2_struct_file), "WSe2")

    def test_metal_listed_before_nonmetal(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        lines = result.splitlines()
        # Species label line: exactly 2 tokens, both purely alphabetic (e.g. "Mo S")
        # This distinguishes it from the title "MoS2 structure" which contains digits.
        label_idx = next(
            i for i, l in enumerate(lines)
            if len(l.split()) == 2 and all(p.isalpha() for p in l.split())
        )
        assert lines[label_idx].split()[0] == "Mo"


class TestAtomCounts:
    """Atom count line matches actual atoms parsed from STRUCT_IN."""

    def _parse_counts(self, poscar: str) -> tuple:
        """Return (metal_count, nonmetal_count) from the POSCAR count line."""
        lines = poscar.splitlines()
        # Species label line is after the 5th line (title+scale+3vecs)
        # Count line immediately follows
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) == 2:
                try:
                    return int(parts[0]), int(parts[1])
                except ValueError:
                    continue
        raise ValueError("Could not find atom count line in POSCAR")

    def test_mos2_counts(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        metal, nonmetal = self._parse_counts(result)
        assert metal == 1
        assert nonmetal == 2

    def test_wse2_counts(self, wse2_struct_file):
        result = struct_to_poscar(str(wse2_struct_file), "WSe2")
        metal, nonmetal = self._parse_counts(result)
        assert metal == 1
        assert nonmetal == 2


class TestAtomCoordinateOrdering:
    """Metal atoms must appear before nonmetal atoms in the coordinate block."""

    def _coord_lines_after_direct(self, poscar: str) -> list:
        lines = poscar.splitlines()
        idx = next(i for i, l in enumerate(lines) if l.strip() == "Direct")
        return [l for l in lines[idx + 1:] if l.strip()]

    def test_mos2_metal_first_z_near_half(self, mos2_struct_file):
        """Mo sits at z≈0.5 (mid-layer); S atoms at z≈0.38 and z≈0.62."""
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        coord_lines = self._coord_lines_after_direct(result)
        first_z = float(coord_lines[0].split()[2])
        assert abs(first_z - 0.5) < 0.01

    def test_total_atom_count_in_coord_block(self, mos2_struct_file):
        result = struct_to_poscar(str(mos2_struct_file), "MoS2")
        coord_lines = self._coord_lines_after_direct(result)
        assert len(coord_lines) == 3  # 1 Mo + 2 S
