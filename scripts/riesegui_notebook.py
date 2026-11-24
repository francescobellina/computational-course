"""Re-execute in place the notebooks that the CI build does not execute.

The heavy notebooks (and the OVITO ones) have ``execute: {skip: true}`` in
their metadata: the book shows the outputs saved in the file.  Run this script
after changing the code they use, then check the diff and commit the outputs.

    uv run python scripts/riesegui_notebook.py            # all skipped notebooks
    uv run python scripts/riesegui_notebook.py --list     # only list them
    uv run python scripts/riesegui_notebook.py cms5       # names containing "cms5"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def skipped_notebooks() -> list[Path]:
    found = []
    for path in sorted((ROOT / "notebooks").rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        meta = nbformat.read(path, as_version=4).metadata
        if meta.get("execute", {}).get("skip"):
            found.append(path)
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("filtro", nargs="*", help="keep paths containing one of these")
    parser.add_argument("--list", action="store_true", help="list and exit")
    args = parser.parse_args()

    notebooks = [
        p
        for p in skipped_notebooks()
        if not args.filtro or any(f in str(p) for f in args.filtro)
    ]
    for path in notebooks:
        rel = path.relative_to(ROOT)
        if args.list:
            print(rel)
            continue
        t0 = time.perf_counter()
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                "--ExecutePreprocessor.timeout=3600",
                str(path),
            ],
            check=False,
        )
        status = "OK" if result.returncode == 0 else f"ERRORE ({result.returncode})"
        print(f"{status:10s} {time.perf_counter() - t0:7.0f} s  {rel}")


if __name__ == "__main__":
    main()
