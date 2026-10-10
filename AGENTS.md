# AGENTS.md

Guidance for agentic coding tools working in this repository.

## Project Overview

**Computational Material Science** — a Jupyter Book of course material on statistical
mechanics and computational methods, plus reusable Python code, numerical simulations, and theory.

Published automatically to GitHub Pages on push to `main`. Seven core topics: classical
statistical mechanics, adiabatic approximation, interatomic potentials, scientific coding,
molecular dynamics, kinetic Monte Carlo, and Metropolis Monte Carlo.

## Environment

Uses **uv** for dependency management (`pyproject.toml`). Python 3.12.x.

```bash
uv sync                         # install dependencies
source .venv/bin/activate       # activate env
```

## Common Commands

```bash
uv run jupyter book start --execute   # build + serve book at http://localhost:8000
uv run jupyter-book build .           # build for deployment -> _build/html/
uv run pytest                         # run all tests (testpaths=tests)
uv run pytest tests/test_root_finding.py   # single test file
uv run ruff check src/ tests/         # lint
uv run ruff format src/ tests/        # format
```

Always run `uv run pytest` and `uv run ruff check src/ tests/` after changing code.

## Repository Structure

```
book/                       # Theory chapters and exercises (Markdown/Jupyter)
├── 01_workflow.md
├── 02_basi_di_teoria/       # Foundational theory
├── 03_guide_examplenotebook/
├── 04_handson_Ag_cutoff/    # Hands-on simulations
├── 04_handson_Ag_cutoff.ipynb
├── 05_esercizio1.ipynb
└── references.bib
notebooks/                  # Standalone Jupyter notebooks with simulations
├── 02_root_finding/
└── 04_handson_Ag_cutoff/
src/computational_course/   # Reusable Python modules (import root)
├── root_finding.py
├── ovito_visualization.py
└── run_Ag_cutoff.py
tests/                      # Unit tests for src/
data/raw/                   # Original datasets (do not modify)
data/processed/             # Derived datasets
figures/                    # Saved figures and plots
myst.yml                    # Jupyter Book config (TOC, bibliography, styling)
```

## Key Conventions

- **Config:** `myst.yml` controls TOC, bibliography, styling, and include/exclude.
- **Imports:** Notebooks and code import from `computational_course`, e.g.
  `from computational_course.root_finding import newton`.
- **Bibliography:** entries in `book/references.bib`, cited with MyST citation syntax.
- **Adding a theory chapter:** create `book/{number}_{topic}/intro.md`, add to `myst.yml` toc.
- **Adding a notebook:** create `notebooks/{number}_{topic}/{name}.ipynb`, reference in `myst.yml`.
- **Adding reusable code:** create module in `src/computational_course/`, export in `__init__.py`,
  add tests in `tests/`.
- **Deployment:** push to `main` triggers GitHub Actions to rebuild and publish.

## Code Style

- Type hints and NumPy-style docstrings on new `src/computational_course/` functions.
- Ruff formatter (configured in VS Code; auto-format on save).
- Do not add comments unless the "why" is not obvious from the code.

Example signature style:

```python
def newton(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    *,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> tuple[float, list[float]]:
    """Solve ``f(x) = 0`` with Newton's method."""
```

## OVITO Visualization Module

`src/computational_course/ovito_visualization.py` analyzes and visualizes atomic structures
with OVITO in notebooks.

Key functions: `find_project_root`, `load_structure`, `convert_to_xyz`,
`compute_neighbor_distances`, `create_ovito_pipeline`, `create_viewport_grid`,
`print_analysis_report`.

```python
from computational_course.ovito_visualization import (
    load_structure,
    compute_neighbor_distances,
    create_viewport_grid,
)

txt_path, coords = load_structure("fcc100a864.txt")
results = compute_neighbor_distances(coords, reference_atom=200)
grid = create_viewport_grid(r_min=2.0, r_max=3.0, reference_atom=200)
```

See `notebooks/04_handson_Ag_cutoff/analysis.ipynb` for a complete example.
