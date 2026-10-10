"""
build_exe.py - Build configuration.exe using PyInstaller.

Usage:
    pip install pyinstaller
    python build_exe.py

The resulting executable will be placed in the current directory.
"""

import subprocess
import sys
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ENTRY_POINT = SCRIPT_DIR / "config_gui.py"
EXE_NAME = "configuration"

# All Python modules that need to be bundled
HIDDEN_IMPORTS = ["config", "main", "xml_engine", "backup"]


def main():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--name={EXE_NAME}",
        f"--distpath={SCRIPT_DIR}",
        f"--workpath={SCRIPT_DIR / 'build'}",
        f"--specpath={SCRIPT_DIR / 'build'}",
    ]
    for mod in HIDDEN_IMPORTS:
        cmd += ["--hidden-import", mod]

    cmd.append(str(ENTRY_POINT))

    print(f"Building {EXE_NAME}.exe ...")
    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR))

    if result.returncode == 0:
        print(f"\nSuccess! {EXE_NAME}.exe created in {SCRIPT_DIR}")
    else:
        print(f"\nBuild failed (exit code {result.returncode})")
        sys.exit(1)

    # Cleanup build artifacts
    build_dir = SCRIPT_DIR / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)


if __name__ == "__main__":
    main()
