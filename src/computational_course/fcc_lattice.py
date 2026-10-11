"""Generation and verification of ideal FCC lattices (pure geometry, no OVITO).

The rendering of these structures belongs in ``ovito_visualization`` or the
notebook; this module only produces coordinates, bonds and consistency checks.
"""

from __future__ import annotations

import numpy as np

#: Fractional coordinates of the 4-site FCC basis (conventional cell, one
#: atom at the origin plus the three nearest face centers). This is the
#: primitive content of the conventional cell: 4 atoms per cell.
_FRAC = np.array(
    [
        (0.0, 0.0, 0.0),
        (0.0, 0.5, 0.5),
        (0.5, 0.0, 0.5),
        (0.5, 0.5, 0.0),
    ]
)

_BOND_TOL = 0.05  # Å, tolerance band around the ideal first-neighbor distance


def fcc_basis(a: float) -> np.ndarray:
    """Return the 4 atoms of one conventional FCC cell in Cartesian units ``a``.

    The four sites are the corner ``(0,0,0)`` and the three face centers that
    remove the translational redundancy of the 14-site conventional cell.
    Together they tile the lattice without duplicating atoms on the borders.
    """
    return _FRAC * a


def fcc_unit_cell(a: float) -> np.ndarray:
    """Return the explicit 14-site conventional cell (8 corners + 6 face centers).

    Used only for drawing the conventional cell, never for building a periodic
    lattice: the border atoms are shared with the neighbouring cells.
    """
    corners = np.array([(x, y, z) for x in (0.0, a) for y in (0.0, a) for z in (0.0, a)])
    faces = np.array(
        [
            (a / 2, a / 2, 0.0),
            (a / 2, a / 2, a),
            (a / 2, 0.0, a / 2),
            (a / 2, a, a / 2),
            (0.0, a / 2, a / 2),
            (a, a / 2, a / 2),
        ]
    )
    return np.vstack([corners, faces])


def fcc_supercell(a: float, nx: int = 1, ny: int = 1, nz: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """Generate ``nx`` by ``ny`` by ``nz`` periodic FCC cells.

    Returns ``(coords, cell_matrix)``. Atoms are wrapped into the box, so there
    are exactly ``nx*ny*nz*4`` atoms and no duplicates on the borders.
    """
    basis = fcc_basis(a)
    shifts = np.array([(i, j, k) for k in range(nz) for j in range(ny) for i in range(nx)], float)
    shifts_ang = shifts * a
    coords = (shifts_ang[:, None, :] + basis[None, :, :]).reshape(-1, 3)
    box = np.array([nx, ny, nz], float) * a
    coords = np.mod(coords, box)
    cell = np.diag(box)
    return coords, cell


def fcc_bonds(
    coords: np.ndarray,
    a: float,
    cell: np.ndarray | None = None,
    tol: float = _BOND_TOL,
) -> np.ndarray:
    """Return first-neighbor bond pairs ``(i, j)`` at distance ``a/sqrt(2)``.

    With ``cell`` the minimum-image convention is used (the structure is
    periodic); with ``cell=None`` only in-box distances are considered. The
    result has one row per pair, shape ``(n_bonds, 2)``.
    """
    r0 = a / np.sqrt(2.0)
    inv = np.linalg.inv(cell) if cell is not None else None
    pairs: list[tuple[int, int]] = []
    for i in range(len(coords)):
        delta = coords - coords[i]
        if inv is not None:
            frac = delta @ inv
            delta = (frac - np.round(frac)) @ cell
        for j in range(i + 1, len(coords)):
            if abs(np.linalg.norm(delta[j]) - r0) < tol:
                pairs.append((i, j))
    return np.array(pairs, dtype=np.int64).reshape(-1, 2)


def check_fcc(
    coords: np.ndarray,
    a: float,
    cell: np.ndarray | None = None,
    *,
    tol: float = _BOND_TOL,
) -> dict:
    """Check whether ``coords`` are consistent with an ideal FCC lattice.

    Parameters
    ----------
    coords:
        Atomic positions.
    a:
        Expected lattice parameter (``a = sqrt(2) * d_nn``).
    cell:
        Periodic box for the minimum-image distance; ``None`` (default) treats
        the system as a finite cluster without periodic boundary conditions.
    tol:
        Distance tolerance in Å.

    Returns
    -------
    dict
        With keys ``n_atoms``, ``d_nn`` (measured), ``a_measured``,
        ``coordination`` (dict CN -> count), ``max_cn`` and ``verdict``.
    """
    r0 = a / np.sqrt(2.0)
    n = len(coords)
    cn = np.zeros(n, dtype=int)
    inv = np.linalg.inv(cell) if cell is not None else None

    for i in range(n):
        delta = coords - coords[i]
        if inv is not None:
            frac = delta @ inv
            delta = (frac - np.round(frac)) @ cell
        d = np.linalg.norm(delta, axis=1)
        cn[i] = int(np.sum((d > r0 - tol * 2) & (d < r0 + tol * 2)))

    coord = {int(v): int(c) for v, c in zip(*np.unique(cn, return_counts=True))}
    max_cn = int(max(coord)) if coord else 0
    center = np.argmax(cn)
    d_nn = float(np.min(np.linalg.norm(coords - coords[center], axis=1)[np.linalg.norm(coords - coords[center], axis=1) > 1e-9]))

    if max_cn == 12 and n >= 12:
        verdict = "FCC coerrente: bulk con 12 primi vicini a d_nn = a/sqrt(2)"
    elif max_cn >= 8:
        verdict = "Compatibile con FCC(100): bulk assente o superfici dominate (CN max < 12)"
    else:
        verdict = "Non compatibile con FCC: coordinazione massima troppo bassa"

    return {
        "n_atoms": n,
        "d_nn": d_nn,
        "a_measured": np.sqrt(2.0) * d_nn,
        "coordination": coord,
        "max_cn": max_cn,
        "verdict": verdict,
    }