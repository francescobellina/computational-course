from math import isclose

import numpy as np

from computational_course.lennard_jones import (
    build_neighbor_list,
    lennard_jones_energy,
    lennard_jones_forces,
    lennard_jones_pair,
)
from computational_course.ovito_visualization import load_structure

SIGMA = 2.644
EPSILON = 0.345


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
