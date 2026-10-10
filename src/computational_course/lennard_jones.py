"""Lennard-Jones potential and neighbour list for the Ag cutoff hands-on."""

import numpy as np
from numpy.typing import NDArray


def lennard_jones_pair(r: float, sigma: float, epsilon: float) -> float:
    """Truncated, unshifted Lennard-Jones pair energy ``4*eps*((s/r)^12-(s/r)^6)``."""
    sr6 = (sigma / r) ** 6
    return 4.0 * epsilon * (sr6**2 - sr6)


def build_neighbor_list(
    positions: NDArray[np.floating],
    cutoff: float,
) -> tuple[NDArray[np.int_], NDArray[np.int_]]:
    """Build a neighbour list with a direct O(N^2) search.

    Parameters
    ----------
    positions:
        Atomic coordinates, shape ``(N, 3)``.
    cutoff:
        Neighbour distance cutoff, in the same units as ``positions``.

    Returns
    -------
    nnbrs, whichnbr
        ``nnbrs[i]`` is the number of neighbours of atom ``i``.
        ``whichnbr[i, :nnbrs[i]]`` holds their indices; the rest is zero padding.

    Notes
    -----
    No periodic boundary conditions: distances are the direct ones.
    """
    natoms = positions.shape[0]
    nnbrs = np.zeros(natoms, dtype=int)
    whichnbr = np.zeros((natoms, natoms), dtype=int)

    for i in range(natoms):
        for j in range(natoms):
            if i == j:
                continue
            if np.linalg.norm(positions[i] - positions[j]) < cutoff:
                whichnbr[i, nnbrs[i]] = j
                nnbrs[i] += 1

    return nnbrs, whichnbr


def lennard_jones_energy(
    positions: NDArray[np.floating],
    sigma: float,
    epsilon: float,
    nnbrs: NDArray[np.int_],
    whichnbr: NDArray[np.int_],
) -> float:
    """Total Lennard-Jones energy over the pairs in a neighbour list.

    Each pair ``(i, j)`` appears twice in ``whichnbr``, so the sum is halved.
    """
    epot = 0.0
    for i in range(positions.shape[0]):
        for k in range(nnbrs[i]):
            j = whichnbr[i, k]
            r = float(np.linalg.norm(positions[i] - positions[j]))
            epot += 0.5 * lennard_jones_pair(r, sigma, epsilon)
    return epot
