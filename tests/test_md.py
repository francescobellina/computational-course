from pathlib import Path

import numpy as np

from computational_course.fcc_lattice import fcc_supercell
from computational_course.md import (
    analizza_traiettoria,
    assign_vel,
    instantaneous_T,
    kinetic_energy,
    radial_distribution,
    run_md,
)

SIGMA = 2.644
EPSILON = 0.345
RC = 4.5
RPRIME = 4.0
A_LJ = 2.0 ** (1.0 / 6.0) * SIGMA * np.sqrt(2.0)
MASS_AG = 108.0 * 1.66e-27 / 16.0


def _bulk(ncells, tini):
    pos, cell = fcc_supercell(A_LJ, ncells, ncells, ncells)
    box = np.diag(cell)
    vel = assign_vel(len(pos), MASS_AG, tini)
    return pos, vel, box


def test_assign_vel_zero_momentum_and_target_temperature() -> None:
    pos, _, _ = _bulk(2, 400.0)
    natoms = pos.shape[0]
    vel = assign_vel(natoms, MASS_AG, 400.0)

    assert np.abs(vel.mean(axis=0)).max() < 1e-9 * np.abs(vel).max()
    temp = instantaneous_T(kinetic_energy(vel, MASS_AG), natoms)
    assert abs(temp - 400.0) < 1e-9
    assert np.array_equal(vel, assign_vel(natoms, MASS_AG, 400.0))


def test_kinetic_temperature_roundtrip() -> None:
    natoms = 10
    vel = np.ones((natoms, 3))
    k = kinetic_energy(vel, 2.0)
    assert k == 0.5 * 2.0 * natoms * 3.0
    assert instantaneous_T(k, natoms) == 2.0 * k / (3 * natoms * (1.0 / 11603.0))


def test_run_md_conserves_energy_and_writes_csv(tmp_path: Path) -> None:
    pos, vel, box = _bulk(3, 300.0)
    dt = 1e-15
    out = tmp_path / "run.csv"
    res = run_md(
        pos,
        vel,
        MASS_AG,
        sigma=SIGMA,
        epsilon=EPSILON,
        rc=RC,
        box=box,
        rprime=RPRIME,
        dt=dt,
        nsteps=200,
        sample_every=50,
        out_file=out,
    )

    etot = res["etot"]
    d_e = float(np.std(etot) / np.abs(np.mean(etot)))
    assert d_e < 1e-5
    assert res["frames"].shape[0] == 4

    stats = analizza_traiettoria(out, ntherm=50)
    assert stats["nsteps_total"] == 200
    assert stats["nprod"] == 150
    assert (
        abs(stats["dE_rel"] - float(np.std(etot[50:]) / np.abs(np.mean(etot[50:]))))
        < 1e-12
    )


def test_run_md_is_reversible() -> None:
    pos, vel, box = _bulk(2, 200.0)
    dt = 2e-15
    kwargs = {
        "sigma": SIGMA,
        "epsilon": EPSILON,
        "rc": RC,
        "box": box,
        "rprime": RPRIME,
        "dt": dt,
        "nsteps": 40,
    }
    first = run_md(pos, vel, MASS_AG, **kwargs)
    back = run_md(first["pos"], -first["vel"], MASS_AG, **kwargs)

    assert np.abs(back["pos"] - pos).max() < 1e-6


def test_radial_distribution_of_uniform_gas_is_one() -> None:
    rng = np.random.default_rng(3)
    box = np.array([15.0, 15.0, 15.0])
    frames = rng.uniform(0.0, box[0], size=(20, 400, 3))
    r, g = radial_distribution(frames, box, nbins=40, dr=0.15)
    mid = (r > 1.5) & (r < box[0] / 2 - 0.2)
    assert abs(float(g[mid].mean()) - 1.0) < 0.05


def test_analizza_traiettoria_discards_thermalization(tmp_path: Path) -> None:
    file = tmp_path / "toy.csv"
    etot = np.concatenate([np.zeros(10), np.array([1.0, 2.0, 3.0, 4.0])])
    rows = ["step,time_ps,T,ekin,epot,etot"]
    for i, e in enumerate(etot):
        rows.append(f"{i + 1},{(i + 1) * 0.001:.3f},100.0,1.0,0.0,{e:.6f}")
    file.write_text("\n".join(rows) + "\n")

    stats = analizza_traiettoria(file, ntherm=10)
    assert stats["nprod"] == 4
    assert stats["E_mean"] == 2.5
    assert abs(stats["dE_rel"] - float(np.std([1.0, 2.0, 3.0, 4.0]) / 2.5)) < 1e-12
    assert stats["T_mean"] == 100.0
