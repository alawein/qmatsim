import subprocess
import sys

def test_help_menu():
    result = subprocess.run([sys.executable, "-m", "qmatsim", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "QMatSim CLI" in result.stdout
