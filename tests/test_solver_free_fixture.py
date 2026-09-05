import json
import subprocess
import sys
from pathlib import Path


def test_solver_free_fixture_has_expected_output():
    result = subprocess.run(
        [sys.executable, "-m", "qmatsim", "verify-fixture"],
        capture_output=True,
        text=True,
        check=False,
    )
    expected_path = Path(__file__).parents[1] / "qmatsim" / "fixtures" / "solver_free_expected.json"
    assert result.returncode == 0, result.stderr
    assert result.stdout == json.dumps(json.loads(expected_path.read_text()), sort_keys=True) + "\n"
