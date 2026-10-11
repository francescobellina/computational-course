"""Tests for the ideal FCC lattice generator."""

import numpy as np

from computational_course.fcc_lattice import (
    check_fcc,
    fcc_basis,
    fcc_bonds,
    fcc_supercell,
    fcc_unit_cell,
)

A = 4.09  # Å, Ag-like lattice parameter


def test_basis_has_four_atoms_and_expected_distances():
    basis = fcc_basis(A)
    assert basis.shape == (4, 3)
    assert np.allclose(np.linalg.norm(basis - basis[0], axis=1)[1:], A / np.sqrt(2))


def test_unit_cell_has_14_distinct_sites():
    cell = fcc_unit_cell(A)
    assert cell.shape == (14, 3)
    assert len(np.unique(cell, axis=0)) == 14
    inside = (cell >= 0) & (cell <= A)
    assert inside.all()


def test_supercell_count_and_no_duplicates():
    for nx, ny, nz in [(1, 1, 1), (2, 2, 2), (3, 3, 1)]:
        coords, cell = fcc_supercell(A, nx, ny, nz)
        assert coords.shape == (nx * ny * nz * 4, 3)
        assert len(np.unique(np.round(coords, 6), axis=0)) == nx * ny * nz * 4
        assert np.allclose(np.diag(cell), np.array([nx, ny, nz]) * A)


def test_supercell_all_atoms_have_12_neighbors():
    coords, cell = fcc_supercell(A, 3, 3, 3)
    report = check_fcc(coords, A, cell=cell)
    assert report["max_cn"] == 12
    assert report["coordination"] == {12: len(coords)}
    assert abs(report["d_nn"] - A / np.sqrt(2)) < 0.05


def test_bonds_only_first_neighbors():
    coords, cell = fcc_supercell(A, 2, 2, 2)
    bonds = fcc_bonds(coords, A, cell=cell)
    assert bonds.shape[1] == 2
    assert len(bonds) == len(coords) * 12 // 2
    inv = np.linalg.inv(cell)

    def min_image(v):
        frac = v @ inv
        return (frac - np.round(frac)) @ cell

    dist = np.array([np.linalg.norm(min_image(coords[i] - coords[j])) for i, j in bonds])
    assert np.allclose(dist, A / np.sqrt(2), atol=0.05)


def test_unit_cell_bonds_without_pbc():
    cell14 = fcc_unit_cell(A)
    bonds = fcc_bonds(cell14, A, cell=None)
    dist = np.linalg.norm(cell14[bonds[:, 0]] - cell14[bonds[:, 1]], axis=1)
    assert len(bonds) > 0
    assert np.allclose(dist, A / np.sqrt(2), atol=0.05)


def test_check_fcc_rejects_disordered_structure():
    rng = np.random.default_rng(0)
    noise = rng.uniform(0.0, 4 * A, (200, 3))
    report = check_fcc(noise, A)
    assert report["max_cn"] < 8