from math import isclose

import numpy as np

from computational_course.fcc_lattice import fcc_supercell
from computational_course.lennard_jones import (
    _poly_coefficients,
    build_neighbor_list,
    lennard_jones_energy,
    lennard_jones_forces,
    lennard_jones_pair,
    lennard_jones_pair_derivative,
)
from computational_course.ovito_visualization import load_structure

SIGMA = 2.644
EPSILON = 0.345
RC = 4.5
RPRIME = 4.0
A_LJ = 2.0 ** (1.0 / 6.0) * SIGMA * np.sqrt(2.0)


def _reference_neighbor_list(pos, cutoff, box=None):
    """Original CMS 4 double loop, kept as the layout reference."""
    natoms = pos.shape[0]
    nnbrs = np.zeros(natoms, dtype=int)
    whichnbr = np.zeros((natoms, natoms), dtype=int)
    for i in range(natoms):
        for j in range(natoms):
            if i == j:
                continue
            d = pos[i] - pos[j]
            if box is not None:
                d -= box * np.round(d / box)
            if np.linalg.norm(d) < cutoff:
                whichnbr[i, nnbrs[i]] = j
                nnbrs[i] += 1
    return nnbrs, whichnbr


def _reference_energy(pos, sigma, epsilon, rc, box):
    """Independent brute-force pair sum with minimum image."""
    energy = 0.0
    n = pos.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            d = pos[i] - pos[j]
            d -= box * np.round(d / box)
            r = float(np.linalg.norm(d))
            if r < rc:
                energy += lennard_jones_pair(r, sigma, epsilon)
    return energy


def test_lennard_jones_pair_minimum() -> None:
    r_min = 2.0 ** (1.0 / 6.0) * SIGMA
    assert isclose(lennard_jones_pair(r_min, SIGMA, EPSILON), -EPSILON, abs_tol=1e-12)
    assert isclose(lennard_jones_pair(SIGMA, SIGMA, EPSILON), 0.0, abs_tol=1e-12)


def test_ag_energy_matches_reference() -> None:
    _, pos = load_structure("fcc100a108.txt")
    nnbrs, whichnbr = build_neighbor_list(pos, cutoff=3.0)

    energy = lennard_jones_energy(pos, SIGMA, EPSILON, nnbrs, whichnbr)

    assert isclose(float(np.mean(nnbrs)), 8.333333333333334, abs_tol=1e-9)
    assert isclose(energy, -154.7957616328464, abs_tol=1e-6)


def test_forces_conserve_momentum_and_vanish_in_bulk() -> None:
    _, pos = load_structure("fcc100a108.txt")
    nnbrs, whichnbr = build_neighbor_list(pos, cutoff=3.0)

    forces = lennard_jones_forces(pos, SIGMA, EPSILON, nnbrs, whichnbr)
    fmag = np.linalg.norm(forces, axis=1)

    assert float(np.abs(forces.sum(axis=0)).max()) < 1e-9
    assert fmag[nnbrs == 12].max() < 1e-6
    assert fmag[nnbrs < 12].max() > 1e-3


def test_neighbor_list_matches_loop_reference() -> None:
    _, pos = load_structure("fcc100a108.txt")
    box = np.array([30.0, 30.0, 30.0])

    for test_box in (None, box):
        nnbrs, whichnbr = build_neighbor_list(pos, RC, box=test_box)
        ref_n, ref_w = _reference_neighbor_list(pos, RC, box=test_box)
        assert (nnbrs == ref_n).all()
        assert (whichnbr == ref_w).all()


def test_pbc_energy_and_forces_on_perfect_lattice() -> None:
    pos, cell = fcc_supercell(A_LJ, 3, 3, 3)
    box = np.diag(cell)
    natoms = pos.shape[0]

    nnbrs, whichnbr = build_neighbor_list(pos, RC, box=box)
    energy = lennard_jones_energy(pos, SIGMA, EPSILON, nnbrs, whichnbr, box=box)
    forces = lennard_jones_forces(pos, SIGMA, EPSILON, nnbrs, whichnbr, box=box)

    ref = _reference_energy(pos, SIGMA, EPSILON, RC, box)
    assert isclose(energy, ref, abs_tol=1e-8)
    assert np.all(nnbrs == 18)
    assert float(np.abs(forces).max()) < 1e-10
    assert energy / natoms < -2.0


def test_neighbor_list_crosses_periodic_boundary() -> None:
    pos, cell = fcc_supercell(A_LJ, 3, 3, 3)
    box = np.diag(cell)
    nnbrs, whichnbr = build_neighbor_list(pos, 3.1, box=box)

    crossed = 0
    for i in range(pos.shape[0]):
        for j in whichnbr[i, : nnbrs[i]]:
            raw = pos[j] - pos[i]
            mic = raw - box * np.round(raw / box)
            if np.abs(raw - mic).max() > 1e-9:
                crossed += 1
    assert (nnbrs == 12).all()
    assert crossed > 0


def test_smooth_shift_is_continuous() -> None:
    a_coef, b_coef, c_coef, d_coef = _poly_coefficients(SIGMA, EPSILON, RPRIME, RC)

    def p(r):
        return a_coef + b_coef * r + c_coef * r**2 + d_coef * r**3

    def dp(r):
        return b_coef + 2 * c_coef * r + 3 * d_coef * r**2

    assert isclose(p(RPRIME), lennard_jones_pair(RPRIME, SIGMA, EPSILON), abs_tol=1e-12)
    assert isclose(
        dp(RPRIME), lennard_jones_pair_derivative(RPRIME, SIGMA, EPSILON), abs_tol=1e-12
    )
    assert isclose(p(RC), 0.0, abs_tol=1e-12)
    assert isclose(dp(RC), 0.0, abs_tol=1e-12)


def test_smooth_forces_match_finite_differences() -> None:
    pos, cell = fcc_supercell(A_LJ, 2, 2, 2)
    box = np.diag(cell)
    rng = np.random.default_rng(7)
    pos = pos + 0.05 * rng.standard_normal(pos.shape)

    nnbrs, whichnbr = build_neighbor_list(pos, RC, box=box)
    forces = lennard_jones_forces(
        pos, SIGMA, EPSILON, nnbrs, whichnbr, box=box, rprime=RPRIME, rc=RC
    )

    h = 1e-5
    max_err = 0.0
    for i in (0, 3, 7):
        for comp in range(3):
            p_plus = pos.copy()
            p_minus = pos.copy()
            p_plus[i, comp] += h
            p_minus[i, comp] -= h
            e = []
            for p in (p_plus, p_minus):
                n_p, w_p = build_neighbor_list(p, RC, box=box)
                e.append(
                    lennard_jones_energy(
                        p, SIGMA, EPSILON, n_p, w_p, box=box, rprime=RPRIME, rc=RC
                    )
                )
            numerical = -(e[0] - e[1]) / (2 * h)
            max_err = max(max_err, abs(numerical - forces[i, comp]))
    assert max_err < 1e-6
