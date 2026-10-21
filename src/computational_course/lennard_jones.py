"""Lennard-Jones potential and neighbour list for the Ag hands-on and molecular dynamics.

Energies in eV, distances in Angstrom.  All routines accept the optional
``box`` vector (Lx, Ly, Lz) for periodic boundary conditions with the
minimum-image convention, and the optional polynomial shift
(``rprime``, ``rc``) that makes ``phi`` and ``phi'`` continuous at ``rc``.
With no optional argument the behaviour is the sharp-cutoff one used by the
CMS 4 hands-on.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def lennard_jones_pair(r: float, sigma: float, epsilon: float) -> float:
    """Truncated, unshifted Lennard-Jones pair energy ``4*eps*((s/r)^12-(s/r)^6)``."""
    sr6 = (sigma / r) ** 6
    return 4.0 * epsilon * (sr6**2 - sr6)


def lennard_jones_pair_derivative(r: float, sigma: float, epsilon: float) -> float:
    """Derivative ``d phi / dr`` of the unshifted Lennard-Jones pair energy."""
    sr6 = (sigma / r) ** 6
    return 4.0 * epsilon * (6.0 * sr6 - 12.0 * sr6**2) / r


def _poly_coefficients(sigma: float, epsilon: float, rprime: float, rc: float):
    """Cubic tail coefficients (A, B, C, D) of the CMS 4 smooth cutoff.

    The cubic ``P(r) = A + B*r + C*r**2 + D*r**3`` matches ``phi`` and
    ``phi'`` at ``rprime`` and vanishes with its derivative at ``rc``.
    """
    e0 = lennard_jones_pair(rprime, sigma, epsilon)
    f0 = lennard_jones_pair_derivative(rprime, sigma, epsilon)
    u = rprime - rc
    beta = (f0 - 2.0 * e0 / u) / u**2
    alpha = e0 / u**2 - beta * rprime
    a_coef = rc**2 * alpha
    b_coef = rc**2 * beta - 2.0 * rc * alpha
    c_coef = alpha - 2.0 * rc * beta
    return a_coef, b_coef, c_coef, beta


def _pair_terms(
    r2: NDArray[np.floating],
    sigma: float,
    epsilon: float,
    shift: tuple[float, float, float, float, float, float] | None,
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """Pair energy ``phi`` and force coefficient for ``F_i += coef * rij``.

    ``shift`` is ``(rprime, rc, A, B, C, D)``; ``None`` keeps the sharp
    Lennard-Jones form for every pair.
    """
    r = np.sqrt(r2)
    sr6 = (sigma * sigma / r2) ** 3
    phi = 4.0 * epsilon * (sr6**2 - sr6)
    coef = 24.0 * epsilon * (2.0 * sr6**2 - sr6) / r2
    if shift is not None:
        rprime, rc, a_coef, b_coef, c_coef, d_coef = shift
        tail = r > rprime
        if np.any(tail):
            phi_p = a_coef + b_coef * r + c_coef * r**2 + d_coef * r**3
            dphi_p = b_coef + 2.0 * c_coef * r + 3.0 * d_coef * r**2
            phi = np.where((r >= rprime) & (r < rc), phi_p, np.where(r >= rc, 0.0, phi))
            coef = np.where(
                (r >= rprime) & (r < rc), -dphi_p / r, np.where(r >= rc, 0.0, coef)
            )
    return phi, coef


def build_neighbor_list(
    positions: NDArray[np.floating],
    cutoff: float,
    *,
    box: NDArray[np.floating] | None = None,
) -> tuple[NDArray[np.int_], NDArray[np.int_]]:
    """Build a neighbour list with a direct O(N^2) search.

    Parameters
    ----------
    positions:
        Atomic coordinates, shape ``(N, 3)``.
    cutoff:
        Neighbour distance cutoff, in the same units as ``positions``.
    box:
        Optional orthorhombic periodic box ``(Lx, Ly, Lz)``; with ``None``
        (default) distances are the direct ones (no PBC).

    Returns
    -------
    nnbrs, whichnbr
        ``nnbrs[i]`` is the number of neighbours of atom ``i``.
        ``whichnbr[i, :nnbrs[i]]`` holds their indices in ascending order;
        the rest is zero padding.
    """
    natoms = positions.shape[0]
    delta = positions[:, None, :] - positions[None, :, :]
    if box is not None:
        delta -= box * np.round(delta / box)
    r2 = np.einsum("ijk,ijk->ij", delta, delta)
    np.fill_diagonal(r2, np.inf)
    mask = r2 < cutoff * cutoff
    nnbrs = mask.sum(axis=1).astype(int)
    sentinel = np.where(mask, np.arange(natoms)[None, :], natoms)
    order = np.sort(sentinel, axis=1)
    whichnbr = np.where(order < natoms, order, 0)
    return nnbrs, whichnbr


def _gather_valid_pairs(
    nnbrs: NDArray[np.int_], whichnbr: NDArray[np.int_]
) -> tuple[NDArray[np.int_], NDArray[np.int_]]:
    """Flat (i, j) index arrays of all valid neighbour-list entries."""
    mask = np.arange(whichnbr.shape[1])[None, :] < nnbrs[:, None]
    i_idx = np.nonzero(mask)[0]
    return i_idx, whichnbr[mask]


def lennard_jones_energy(
    positions: NDArray[np.floating],
    sigma: float,
    epsilon: float,
    nnbrs: NDArray[np.int_],
    whichnbr: NDArray[np.int_],
    *,
    box: NDArray[np.floating] | None = None,
    rprime: float | None = None,
    rc: float | None = None,
) -> float:
    """Total Lennard-Jones energy over the pairs in a neighbour list.

    Each pair ``(i, j)`` appears twice in ``whichnbr``, so the sum is halved.
    With ``rprime`` and ``rc`` the tail between them is replaced by the
    polynomial of the CMS 4 smooth cutoff (the list must be built with the
    same ``rc``).
    """
    shift = _md_shift(sigma, epsilon, rprime, rc)
    i_idx, j_idx = _gather_valid_pairs(nnbrs, whichnbr)
    rij = positions[i_idx] - positions[j_idx]
    if box is not None:
        rij -= box * np.round(rij / box)
    r2 = np.einsum("ij,ij->i", rij, rij)
    phi, _ = _pair_terms(r2, sigma, epsilon, shift)
    return float(0.5 * phi.sum())


def lennard_jones_forces(
    positions: NDArray[np.floating],
    sigma: float,
    epsilon: float,
    nnbrs: NDArray[np.int_],
    whichnbr: NDArray[np.int_],
    *,
    box: NDArray[np.floating] | None = None,
    rprime: float | None = None,
    rc: float | None = None,
) -> NDArray[np.floating]:
    """Net Lennard-Jones force on each atom from a neighbour list.

    For a pair ``(i, j)`` the force on ``i`` is
    ``24*eps/r**2 * (2*(sigma/r)**12 - (sigma/r)**6) * (r_i - r_j)``.
    With ``rprime`` and ``rc`` the polynomial tail of the smooth cutoff is
    used between them (the list must be built with the same ``rc``).

    Returns
    -------
    force
        Array of shape ``(N, 3)``; ``force[i]`` is the net force on atom ``i``.
    """
    shift = _md_shift(sigma, epsilon, rprime, rc)
    i_idx, j_idx = _gather_valid_pairs(nnbrs, whichnbr)
    rij = positions[i_idx] - positions[j_idx]
    if box is not None:
        rij -= box * np.round(rij / box)
    r2 = np.einsum("ij,ij->i", rij, rij)
    _, coef = _pair_terms(r2, sigma, epsilon, shift)
    force = np.zeros_like(positions, dtype=float)
    np.add.at(force, i_idx, coef[:, None] * rij)
    return force


def _md_shift(sigma: float, epsilon: float, rprime: float | None, rc: float | None):
    """Assemble the shift tuple, validating the ``rprime``/``rc`` pair."""
    if rprime is None:
        return None
    if rc is None:
        raise ValueError("rc is required when rprime is given")
    if not 0.0 < rprime < rc:
        raise ValueError("expected 0 < rprime < rc")
    a_coef, b_coef, c_coef, d_coef = _poly_coefficients(sigma, epsilon, rprime, rc)
    return (rprime, rc, a_coef, b_coef, c_coef, d_coef)
