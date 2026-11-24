import numpy as np
import pytest

from computational_course.fcc_lattice import fcc_supercell
from computational_course.lennard_jones import (
    build_neighbor_list,
    lennard_jones_energy,
    lennard_jones_pair,
    lennard_jones_pair_derivative,
)
from computational_course.md import assign_vel
from computational_course.md_p7 import (
    lj_p7_model,
    max_force,
    production_stats,
    remove_angular_momentum,
    run_nve,
    steepest_descent,
)
from computational_course.poly7 import poly7

SIGMA, EPSILON, RC, RP = 2.644, 0.345, 4.5, 4.2
A_AG = 4.1604
MASS = 108.0 * 1.66e-27 / 16.0


def _course_p7() -> np.ndarray:
    lp = poly7(EPSILON, SIGMA, RC, RP)
    return np.array([lp.A, lp.B, lp.C, lp.D, lp.E, lp.F, lp.G, lp.H])


P7 = _course_p7()


@pytest.fixture(scope="module")
def cluster():
    pos, _ = fcc_supercell(A_AG, 3, 3, 3)
    rng = np.random.default_rng(7)
    return pos + 0.08 * rng.standard_normal(pos.shape)


def test_p7_matches_lj_at_rp_and_vanishes_at_rc():
    p = np.polynomial.polynomial
    assert p.polyval(RP, P7) == pytest.approx(
        lennard_jones_pair(RP, SIGMA, EPSILON), abs=1e-5
    )
    assert p.polyval(RP, p.polyder(P7)) == pytest.approx(
        lennard_jones_pair_derivative(RP, SIGMA, EPSILON), abs=1e-5
    )
    for k in range(4):
        assert abs(p.polyval(RC, p.polyder(P7, k))) < 1e-5


def test_sharp_model_matches_lennard_jones_module(cluster):
    epot, _, _ = lj_p7_model(SIGMA, EPSILON, RC)(cluster)
    nn, wn = build_neighbor_list(cluster, RC)
    assert epot == pytest.approx(
        lennard_jones_energy(cluster, SIGMA, EPSILON, nn, wn), rel=1e-12
    )


@pytest.mark.parametrize("smooth", [False, True])
def test_forces_are_minus_energy_gradient(cluster, smooth):
    model = lj_p7_model(SIGMA, EPSILON, RC, rp=RP if smooth else None, p7=P7)
    _, force, _ = model(cluster)
    # not smaller: the P7 coefficients (~1e8, alternating signs) carry a
    # cancellation noise in the energy that a tiny h would amplify
    h = 1e-3
    for atom, axis in [(0, 0), (13, 1), (40, 2), (77, 0)]:
        plus, minus = cluster.copy(), cluster.copy()
        plus[atom, axis] += h
        minus[atom, axis] -= h
        numeric = -(model(plus)[0] - model(minus)[0]) / (2 * h)
        assert force[atom, axis] == pytest.approx(numeric, abs=5e-4)


def test_cluster_has_no_net_force_or_torque(cluster):
    _, force, _ = lj_p7_model(SIGMA, EPSILON, RC, rp=RP, p7=P7)(cluster)
    np.testing.assert_allclose(force.sum(axis=0), 0.0, atol=1e-10)
    torque = np.cross(cluster - cluster.mean(axis=0), force).sum(axis=0)
    np.testing.assert_allclose(torque, 0.0, atol=1e-9)


def test_slab_periodic_only_in_x_and_y():
    pos, cell = fcc_supercell(A_AG, 4, 4, 3)
    box = np.diag(cell)
    bulk = lj_p7_model(SIGMA, EPSILON, RC, rp=RP, p7=P7, box=box, periodic=(True,) * 3)
    slab = lj_p7_model(
        SIGMA, EPSILON, RC, rp=RP, p7=P7, box=box, periodic=(True, True, False)
    )
    e_bulk, f_bulk, _ = bulk(pos)
    e_slab, f_slab, _ = slab(pos)
    assert max_force(f_bulk) < 1e-10
    assert e_slab > e_bulk
    assert max_force(f_slab[:, :2]) < 1e-10
    shifted = pos + np.array([box[0], 0.0, 0.0]) * (pos[:, :1] < box[0] / 2)
    assert slab(shifted)[0] == pytest.approx(e_slab, rel=1e-12)


def test_invalid_arguments():
    with pytest.raises(ValueError):
        lj_p7_model(SIGMA, EPSILON, RC, rp=RP)
    with pytest.raises(ValueError):
        lj_p7_model(SIGMA, EPSILON, RC, rp=4.6, p7=P7)
    with pytest.raises(ValueError):
        lj_p7_model(SIGMA, EPSILON, RC, periodic=(True, False, False))


def test_nve_conserves_energy_with_p7(cluster):
    model = lj_p7_model(SIGMA, EPSILON, RC, rp=RP, p7=P7)
    vel = assign_vel(len(cluster), MASS, 300.0)
    res = run_nve(cluster, vel, MASS, 2e-15, 600, model)
    assert res["stable"]
    stats = production_stats(res, ntherm=100)
    assert stats["dE_rel"] < 1e-5
    vmax = np.abs(res["vel"]).max()
    np.testing.assert_allclose(res["vel"].sum(axis=0) / vmax, 0.0, atol=1e-9)


def test_nve_flags_divergence(cluster):
    model = lj_p7_model(SIGMA, EPSILON, RC)
    vel = assign_vel(len(cluster), MASS, 3000.0)
    res = run_nve(cluster, vel, MASS, 60e-15, 400, model)
    assert not res["stable"]
    assert np.isnan(production_stats(res, ntherm=10)["dE_rel"])


def test_steepest_descent_converges_monotonically(cluster):
    model = lj_p7_model(SIGMA, EPSILON, RC, rp=RP, p7=P7)
    res = steepest_descent(cluster, model, c=0.005, ftol=1e-3)
    assert res["converged"]
    assert res["fmax"][-1] < 1e-3
    assert np.all(np.diff(res["energy"]) <= 1e-12)
    np.testing.assert_allclose(
        res["pos"].mean(axis=0), cluster.mean(axis=0), atol=1e-12
    )


def test_adaptive_steepest_descent_rejects_uphill_steps(cluster):
    model = lj_p7_model(SIGMA, EPSILON, RC, rp=RP, p7=P7)
    res = steepest_descent(cluster, model, c=0.2, ftol=1e-3, adaptive=True)
    assert res["converged"]
    assert np.all(np.diff(res["energy"]) <= 1e-12)
    assert res["c"].min() < 0.2


def test_remove_angular_momentum_keeps_linear_momentum(cluster):
    vel = assign_vel(len(cluster), MASS, 300.0)
    rel = cluster - cluster.mean(axis=0)
    assert np.linalg.norm(np.cross(rel, vel).sum(axis=0)) > 0
    new = remove_angular_momentum(cluster, vel, MASS)
    vmax = np.abs(vel).max()
    np.testing.assert_allclose(
        np.cross(rel, new).sum(axis=0) / (vmax * np.abs(rel).max()), 0.0, atol=1e-12
    )
    np.testing.assert_allclose((new - vel).sum(axis=0) / vmax, 0.0, atol=1e-12)
