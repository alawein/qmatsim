"""Unit tests for qmatsim package metadata and configuration.

Verifies __version__, __author__, pyproject.toml consistency, and that
the package is properly structured for import.
"""

from pathlib import Path

import pytest

import qmatsim


class TestPackageMetadata:
    """Tests for qmatsim.__init__ metadata."""

    def test_version_is_string(self):
        assert isinstance(qmatsim.__version__, str)

    def test_version_is_semver(self):
        """Version should follow X.Y.Z pattern."""
        parts = qmatsim.__version__.split(".")
        assert len(parts) == 3, f"Expected 3-part semver, got: {qmatsim.__version__}"
        for part in parts:
            assert part.isdigit(), f"Non-numeric version component: {part}"

    def test_author_is_set(self):
        assert hasattr(qmatsim, "__author__")
        assert len(qmatsim.__author__) > 0

    def test_package_is_importable(self):
        """The package should import without error."""
        import qmatsim

        assert qmatsim is not None

    def test_main_module_importable(self):
        """qmatsim.__main__ should be importable."""
        from qmatsim import __main__

        assert hasattr(__main__, "main")


class TestPyprojectToml:
    """Tests verifying pyproject.toml is consistent with the package."""

    @pytest.fixture
    def pyproject_text(self):
        return (Path(__file__).parent.parent / "pyproject.toml").read_text(
            encoding="utf-8"
        )

    def test_name_matches_package(self, pyproject_text):
        """Project name in pyproject.toml should reference qmatsim."""
        assert 'name = "QMatSim"' in pyproject_text

    def test_version_matches_init(self, pyproject_text):
        """pyproject.toml version should match __init__.__version__."""
        assert f'version = "{qmatsim.__version__}"' in pyproject_text

    def test_pytest_configured(self, pyproject_text):
        assert "[tool.pytest.ini_options]" in pyproject_text

    def test_testpaths_set_to_tests(self, pyproject_text):
        assert 'testpaths = ["tests"]' in pyproject_text

    def test_numpy_in_dependencies(self, pyproject_text):
        assert "numpy" in pyproject_text

    def test_matplotlib_in_dependencies(self, pyproject_text):
        assert "matplotlib" in pyproject_text

    def test_python_requires_39(self, pyproject_text):
        assert ">=3.9" in pyproject_text

    def test_entry_point_defined(self, pyproject_text):
        assert 'qmatsim = "qmatsim.__main__:main"' in pyproject_text

    def test_setuptools_find_packages(self, pyproject_text):
        """Package discovery should include qmatsim* and exclude tests*."""
        assert 'include = ["qmatsim*"]' in pyproject_text
        assert 'exclude = ["tests*"]' in pyproject_text


class TestProjectLayout:
    """Tests verifying the canonical project layout."""

    @pytest.fixture
    def repo_root(self):
        return Path(__file__).parent.parent

    def test_no_src_directory(self, repo_root):
        """qmatsim/ is the root package; src/ should not exist."""
        assert not (repo_root / "src").exists()

    def test_qmatsim_package_exists(self, repo_root):
        assert (repo_root / "qmatsim").is_dir()

    def test_init_py_exists(self, repo_root):
        assert (repo_root / "qmatsim" / "__init__.py").exists()

    def test_main_py_exists(self, repo_root):
        assert (repo_root / "qmatsim" / "__main__.py").exists()

    def test_tests_directory_exists(self, repo_root):
        assert (repo_root / "tests").is_dir()

    def test_conftest_exists(self, repo_root):
        assert (repo_root / "tests" / "conftest.py").exists()
