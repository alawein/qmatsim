"""Unit tests for qmatsim.__main__.run_script_safely and workflow dispatchers.

Tests exercise run_script_safely, run_dft, run_md, and run_post by mocking
subprocess.run and filesystem access.  No real bash/SIESTA/LAMMPS calls.
"""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from qmatsim.__main__ import (
    run_script_safely,
    run_dft,
    run_md,
    run_post,
)


# ---------------------------------------------------------------------------
# run_script_safely
# ---------------------------------------------------------------------------


class TestRunScriptSafely:
    """Tests for the generic bash-script runner."""

    def test_success_prints_completed(self, tmp_path, capsys, monkeypatch):
        """Successful script execution prints the success message."""
        # Create a fake script file at the expected location
        script_rel = "scripts/fake.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("#!/bin/bash\necho ok")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        completed = subprocess.CompletedProcess(
            args=["bash", script_rel], returncode=0, stdout="all good\n", stderr=""
        )
        with patch("subprocess.run", return_value=completed):
            run_script_safely(script_rel, ["arg1"], "Fake job")

        out = capsys.readouterr().out
        assert "Fake job completed successfully" in out
        assert "all good" in out

    def test_nonzero_exit_calls_sys_exit(self, tmp_path, capsys, monkeypatch):
        """Non-zero return code from the script triggers sys.exit."""
        script_rel = "scripts/fail.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("#!/bin/bash\nexit 42")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        completed = subprocess.CompletedProcess(
            args=["bash", script_rel],
            returncode=42,
            stdout="",
            stderr="boom\n",
        )
        with patch("subprocess.run", return_value=completed):
            with pytest.raises(SystemExit) as exc:
                run_script_safely(script_rel, [], "Failing job")
        assert exc.value.code == 42

    def test_missing_script_exits(self, tmp_path, monkeypatch):
        """Missing script file triggers sys.exit(1)."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        with pytest.raises(SystemExit) as exc:
            run_script_safely("scripts/nonexistent.sh", [], "Ghost script")
        assert exc.value.code == 1

    def test_bash_not_found_exits(self, tmp_path, capsys, monkeypatch):
        """FileNotFoundError from subprocess (no bash) triggers sys.exit(1)."""
        script_rel = "scripts/ok.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("#!/bin/bash\ntrue")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        with patch("subprocess.run", side_effect=FileNotFoundError("bash")):
            with pytest.raises(SystemExit) as exc:
                run_script_safely(script_rel, [], "No-bash test")
        assert exc.value.code == 1

    def test_cwd_restored_after_success(self, tmp_path, monkeypatch):
        """Working directory is restored even after successful execution."""
        script_rel = "scripts/ok.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        original_cwd = os.getcwd()
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        with patch("subprocess.run", return_value=completed):
            run_script_safely(script_rel, [], "CWD test")

        assert os.getcwd() == original_cwd

    def test_cwd_restored_after_failure(self, tmp_path, monkeypatch):
        """Working directory is restored even after script failure."""
        script_rel = "scripts/fail.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        original_cwd = os.getcwd()
        completed = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr=""
        )
        with patch("subprocess.run", return_value=completed):
            with pytest.raises(SystemExit):
                run_script_safely(script_rel, [], "CWD fail test")

        assert os.getcwd() == original_cwd

    def test_args_forwarded_to_subprocess(self, tmp_path, monkeypatch):
        """Extra arguments are passed through to subprocess.run."""
        script_rel = "scripts/args.sh"
        script_abs = tmp_path / script_rel
        script_abs.parent.mkdir(parents=True, exist_ok=True)
        script_abs.write_text("")

        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)

        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        with patch("subprocess.run", return_value=completed) as mock_run:
            run_script_safely(script_rel, ["a", "b"], "Args test")

        mock_run.assert_called_once()
        actual_args = mock_run.call_args[0][0]
        assert actual_args == ["bash", script_rel, "a", "b"]


# ---------------------------------------------------------------------------
# run_dft
# ---------------------------------------------------------------------------


class TestRunDft:
    """Tests for the DFT workflow dispatcher."""

    def test_calls_run_script_safely_with_correct_args(self):
        args = MagicMock()
        args.material = "MoS2"
        args.structure = "1x10_rectangular"

        with patch("qmatsim.__main__.run_script_safely") as mock_rss:
            run_dft(args)

        mock_rss.assert_called_once_with(
            "scripts/run-DFT.sh",
            ["MoS2", "1x10_rectangular"],
            "DFT simulation",
        )


# ---------------------------------------------------------------------------
# run_post
# ---------------------------------------------------------------------------


class TestRunPost:
    """Tests for the postprocessing workflow dispatcher."""

    def test_calls_run_script_safely_with_correct_args(self):
        args = MagicMock()
        args.material = "WS2"
        args.structure = "1x1_primitive"

        with patch("qmatsim.__main__.run_script_safely") as mock_rss:
            run_post(args)

        mock_rss.assert_called_once_with(
            "scripts/run-postprocessing.sh",
            ["WS2", "1x1_primitive"],
            "Postprocessing analysis",
        )


# ---------------------------------------------------------------------------
# run_md
# ---------------------------------------------------------------------------


class TestRunMd:
    """Tests for the MD workflow dispatcher."""

    def _make_args(self, structure="1x10_rectangular", mode="all"):
        args = MagicMock()
        args.structure = structure
        args.mode = mode
        return args

    def test_compress_mode_calls_compress_script(self, tmp_path, monkeypatch):
        """Mode 'compress' delegates to compress-MD.sh."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        # Create the data file so validation passes
        data_dir = tmp_path / "lammps" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "mystruc.data").write_text("fake")

        # Create the compress input file
        in_dir = tmp_path / "lammps" / "in"
        in_dir.mkdir(parents=True)
        (in_dir / "compress_y.in").write_text("fake")

        args = self._make_args(structure="mystruc", mode="compress")
        with patch("qmatsim.__main__.run_script_safely") as mock_rss:
            run_md(args)

        mock_rss.assert_called_once_with(
            "scripts/compress-MD.sh", ["mystruc"], "MD compression simulation"
        )

    def test_all_mode_calls_run_md_script(self, tmp_path, monkeypatch):
        """Mode 'all' delegates to run-MD.sh."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        data_dir = tmp_path / "lammps" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "mystruc.data").write_text("fake")

        in_dir = tmp_path / "lammps" / "in"
        in_dir.mkdir(parents=True)
        for fname in ["compress_y.in", "deformation.in", "minimization.in"]:
            (in_dir / fname).write_text("fake")

        args = self._make_args(structure="mystruc", mode="all")
        with patch("qmatsim.__main__.run_script_safely") as mock_rss:
            run_md(args)

        mock_rss.assert_called_once_with(
            "scripts/run-MD.sh", ["mystruc"], "MD simulation suite"
        )

    def test_missing_data_file_exits(self, tmp_path, monkeypatch, capsys):
        """Missing LAMMPS data file triggers sys.exit(1)."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        # Do NOT create the data file
        (tmp_path / "lammps" / "data").mkdir(parents=True)

        args = self._make_args(structure="ghost", mode="all")
        with pytest.raises(SystemExit) as exc:
            run_md(args)
        assert exc.value.code == 1

    def test_missing_input_files_for_all_mode_exits(
        self, tmp_path, monkeypatch, capsys
    ):
        """Mode 'all' exits when required LAMMPS input files are missing."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        data_dir = tmp_path / "lammps" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "mystruc.data").write_text("fake")

        # Create lammps/in but omit required files
        (tmp_path / "lammps" / "in").mkdir(parents=True)

        args = self._make_args(structure="mystruc", mode="all")
        with pytest.raises(SystemExit) as exc:
            run_md(args)
        assert exc.value.code == 1

    def test_unknown_mode_exits(self, tmp_path, monkeypatch, capsys):
        """An unknown mode string triggers sys.exit(1)."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        data_dir = tmp_path / "lammps" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "mystruc.data").write_text("fake")

        args = self._make_args(structure="mystruc", mode="bogus")
        with pytest.raises(SystemExit) as exc:
            run_md(args)
        assert exc.value.code == 1

    def test_missing_compress_input_exits(self, tmp_path, monkeypatch):
        """Compress mode exits when compress_y.in is missing."""
        monkeypatch.setattr("qmatsim.__main__.get_project_root", lambda: tmp_path)
        data_dir = tmp_path / "lammps" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "mystruc.data").write_text("fake")

        # Create lammps/in but omit compress_y.in
        (tmp_path / "lammps" / "in").mkdir(parents=True)

        args = self._make_args(structure="mystruc", mode="compress")
        with pytest.raises(SystemExit) as exc:
            run_md(args)
        assert exc.value.code == 1
