"""Project paths, without heavy dependencies (notebooks import this first)."""

from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find the project root by searching for pyproject.toml.

    Parameters
    ----------
    start:
        Starting directory for the search. Defaults to current working directory.

    Returns
    -------
    Path
        The project root directory.

    Raises
    ------
    FileNotFoundError
        If pyproject.toml is not found in the directory tree.
    """
    if start is None:
        start = Path.cwd()

    for folder in [start, *start.parents]:
        if (folder / "pyproject.toml").exists():
            return folder

    raise FileNotFoundError(
        "Non riesco a trovare la root del progetto (cerco pyproject.toml)."
    )
