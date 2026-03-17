"""Unit tests for qmatsim.__main__ utility functions and argument parsing.

Tests run in-process (no subprocess) by patching sys.argv and sys.exit.
This avoids the python3 / subprocess-hang issues that affect the existing
smoke tests on Windows and makes the suite ~100x faster.
"""
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

from qmatsim.__main__ import get_project_root, validate_file_exists, main


class TestGetProjectRoot:
    def test_returns_path_instance(self):
        assert isinstance(get_project_root(), Path)

    def test_qmatsim_package_dir_exists(self):
        assert (get_project_root() / "qmatsim").is_dir()

    def test_pyproject_toml_present(self):
        assert (get_project_root() / "pyproject.toml").exists()

    def test_consistent_across_calls(self):
        assert get_project_root() == get_project_root()


class TestValidateFileExists:
    def test_existing_file_returns_true(self, tmp_path):
        f = tmp_path / "real.txt"
        f.write_text("content")
        assert validate_file_exists(f, "real file") is True

    def test_missing_file_returns_false(self, tmp_path, capsys):
        # capsys provides a Unicode-capable stdout buffer (avoids CP1252 issue
        # with the emoji in the print statement on Windows)
        result = validate_file_exists(tmp_path / "ghost.txt", "ghost")
        capsys.readouterr()  # discard captured output
        assert result is False

    def test_missing_file_prints_file_path(self, tmp_path, capsys):
        f = tmp_path / "ghost.txt"
        validate_file_exists(f, "ghost")
        assert "ghost.txt" in capsys.readouterr().out

    def test_missing_file_prints_description(self, tmp_path, capsys):
        validate_file_exists(tmp_path / "x.txt", "my description")
        assert "my description" in capsys.readouterr().out


class TestArgParsing:
    """CLI argument parsing — no bash scripts are executed in these tests.

    Each test patches sys.argv so argparse sees the given arguments,
    then verifies the correct SystemExit is raised for invalid invocations.
    """

    def test_no_command_exits_1(self):
        with patch("sys.argv", ["qmatsim"]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 1

    def test_unknown_subcommand_exits(self):
        with patch("sys.argv", ["qmatsim", "launch"]):
            with pytest.raises(SystemExit):
                main()

    # --- relax ---

    def test_relax_missing_material_exits(self):
        with patch("sys.argv", ["qmatsim", "relax", "--structure", "1x10_rectangular"]):
            with pytest.raises(SystemExit):
                main()

    def test_relax_missing_structure_exits(self):
        with patch("sys.argv", ["qmatsim", "relax", "--material", "MoS2"]):
            with pytest.raises(SystemExit):
                main()

    # --- minimize ---

    def test_minimize_missing_structure_exits(self):
        with patch("sys.argv", ["qmatsim", "minimize"]):
            with pytest.raises(SystemExit):
                main()

    def test_minimize_invalid_mode_exits(self):
        with patch("sys.argv", [
            "qmatsim", "minimize",
            "--structure", "1x10_rectangular",
            "--mode", "explode",
        ]):
            with pytest.raises(SystemExit):
                main()

    def test_minimize_valid_modes_accepted(self):
        """compress and all are the only valid modes; argparse rejects others.

        Patches run_script_safely (not run_md) because argparse binds func=run_md
        at set_defaults() time, so patching run_md after the fact has no effect.
        run_script_safely is resolved via the module dict on every call, so it
        can be intercepted without breaking the argparse dispatch chain.
        """
        valid_modes = ["compress", "all"]
        for mode in valid_modes:
            with (
                patch("sys.argv", [
                    "qmatsim", "minimize",
                    "--structure", "1x10_rectangular",
                    "--mode", mode,
                ]),
                patch("qmatsim.__main__.run_script_safely"),
            ):
                # argparse should NOT raise SystemExit for valid modes
                try:
                    main()
                except SystemExit:
                    pytest.fail(f"argparse rejected valid mode '{mode}'")

    # --- analyze ---

    def test_analyze_missing_material_exits(self):
        with patch("sys.argv", ["qmatsim", "analyze", "--structure", "1x10_rectangular"]):
            with pytest.raises(SystemExit):
                main()

    def test_analyze_missing_structure_exits(self):
        with patch("sys.argv", ["qmatsim", "analyze", "--material", "MoS2"]):
            with pytest.raises(SystemExit):
                main()
