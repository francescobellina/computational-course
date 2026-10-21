"""Molecular dynamics (velocity Verlet) for the CMS course.

Units: energies in eV, distances in Angstrom, time in s (fs/ps used in
plots and output).  Masses are in code units ``eV*s^2/A^2`` (1 unit = 16 kg),
temperatures in K with ``kB = 1/11603 eV/K``.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from .lennard_jones import (
    build_neighbor_list,
    lennard_jones_energy,
    lennard_jones_forces,
)

#: Boltzmann constant in eV/K (course value).
KB_EV = 1.0 / 11603.0

#: Default seed for reproducible initial velocities.
DEFAULT_SEED = 33282739


def assign_vel(
    natoms: int,
    mass: float,
    tini: float,
    *,
    seed: int = DEFAULT_SEED,
    zero_momentum: bool = True,
) -> NDArray[np.floating]:
    """Assign random velocities from a uniform distribution in ``[-C, C]``.

    ``C = sqrt(3 * kB * T / mass)`` gives the correct mean kinetic energy.
    The total momentum is then removed and the temperatures rescaled to
    ``tini`` (in that order: removing momentum changes the temperature).
    """
    rng = np.random.default_rng(seed)
    cc = (3.0 * KB_EV * tini / mass) ** 0.5
    vel = rng.uniform(-cc, cc, size=(natoms, 3))
    if zero_momentum:
        vel -= vel.mean(axis=0)
    tprime = instantaneous_T(kinetic_energy(vel, mass), natoms)
    return vel * (tini / tprime) ** 0.5


def kinetic_energy(vel: NDArray[np.floating], mass: float) -> float:
    """Total kinetic energy ``K = (1/2) sum_i m |v_i|^2`` in eV."""
    return 0.5 * mass * float(np.sum(vel**2))


def instantaneous_T(k: float, natoms: int, kb: float = KB_EV) -> float:
    """Instantaneous temperature ``T = 2K / (N_dof * kB)`` with ``N_dof = 3N``."""
    return 2.0 * k / (3 * natoms * kb)


def run_md(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mass: float,
    *,
    sigma: float,
    epsilon: float,
    rc: float,
    box: NDArray[np.floating],
    rprime: float | None = None,
    dt: float,
    nsteps: int,
    sample_every: int = 10,
    out_file: str | Path | None = None,
) -> dict:
    """NVE molecular dynamics with velocity Verlet.

    Parameters
    ----------
    pos, vel:
        Initial positions and velocities, shape ``(N, 3)``.
    mass:
        Atomic mass in code units.
    sigma, epsilon:
        Lennard-Jones parameters (Angstrom, eV).
    rc:
        Cutoff radius; neighbour lists are rebuilt every step with it.
    box:
        Orthorhombic periodic box ``(Lx, Ly, Lz)``.
    rprime:
        Start of the polynomial smooth-cutoff tail (``None`` = sharp).
    dt:
        Time step in seconds.
    nsteps:
        Number of velocity-Verlet steps.
    sample_every:
        Store positions every this many steps (for g(r) analysis).
    out_file:
        If given, per-step observables are appended to this CSV file
        (columns: step, time_ps, T, ekin, epot, etot).

    Returns
    -------
    dict
        ``time_ps``, ``T``, ``ekin``, ``epot``, ``etot`` (per step),
        ``frames`` (sampled positions), ``frame_steps``, ``pos``, ``vel``.
    """
    pos = pos.copy()
    vel = vel.copy()
    natoms = pos.shape[0]
    shift = {"rc": rc, "rprime": rprime}

    nnbrs, whichnbr = build_neighbor_list(pos, rc, box=box)
    epot = lennard_jones_energy(pos, sigma, epsilon, nnbrs, whichnbr, box=box, **shift)
    force = lennard_jones_forces(pos, sigma, epsilon, nnbrs, whichnbr, box=box, **shift)

    time_ps = np.empty(nsteps)
    temp = np.empty(nsteps)
    ekin = np.empty(nsteps)
    epot_h = np.empty(nsteps)
    frames: list[NDArray[np.floating]] = []
    frame_steps: list[int] = []

    for step in range(nsteps):
        # (1) positions at t+dt from v(t) and a(t) = f(t)/m
        for i in range(natoms):
            for j in range(3):
                pos[i, j] = (
                    pos[i, j] + vel[i, j] * dt + 0.5 * (force[i, j] / mass) * dt * dt
                )
        # (2) forces at t+dt on the new positions (neighbour lists rebuilt)
        nnbrs, whichnbr = build_neighbor_list(pos, rc, box=box)
        epot = lennard_jones_energy(
            pos, sigma, epsilon, nnbrs, whichnbr, box=box, **shift
        )
        forcenew = lennard_jones_forces(
            pos, sigma, epsilon, nnbrs, whichnbr, box=box, **shift
        )
        # (3) velocities at t+dt from the mean of a(t) and a(t+dt)
        for i in range(natoms):
            for j in range(3):
                vel[i, j] = (
                    vel[i, j] + (0.5 / mass) * (force[i, j] + forcenew[i, j]) * dt
                )
        # (4) the next step starts from the forces just computed
        force = forcenew.copy()

        k = kinetic_energy(vel, mass)
        ekin[step] = k
        epot_h[step] = epot
        temp[step] = instantaneous_T(k, natoms)
        time_ps[step] = (step + 1) * dt * 1e12
        if (step + 1) % sample_every == 0:
            frames.append(pos.copy())
            frame_steps.append(step + 1)

    if out_file is not None:
        steps = np.arange(1, nsteps + 1, dtype=float)
        table = np.column_stack([steps, time_ps, temp, ekin, epot_h, ekin + epot_h])
        np.savetxt(
            out_file,
            table,
            delimiter=",",
            header="step,time_ps,T,ekin,epot,etot",
            comments="",
            fmt=["%d", "%.6f", "%.6f", "%.8f", "%.8f", "%.8f"],
        )

    return {
        "time_ps": time_ps,
        "T": temp,
        "ekin": ekin,
        "epot": epot_h,
        "etot": ekin + epot_h,
        "frames": np.array(frames),
        "frame_steps": np.array(frame_steps),
        "pos": pos,
        "vel": vel,
    }


def radial_distribution(
    frames: NDArray[np.floating],
    box: NDArray[np.floating],
    nbins: int,
    dr: float,
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """Radial distribution function g(r) from sampled configurations.

    All minimum-image pair distances of every frame are binned with width
    ``dr`` and normalized by the ideal-gas count of each spherical shell
    (finite-size consistent: ``N*(N-1)`` instead of ``N^2``).

    Returns
    -------
    r, g
        Bin centers and g(r), valid up to ``nbins*dr`` (``<= L_min/2``).
    """
    natoms = frames.shape[1]
    volume = float(np.prod(box))
    counts = np.zeros(nbins)
    for frame in frames:
        delta = frame[:, None, :] - frame[None, :, :]
        delta -= box * np.round(delta / box)
        dist = np.sqrt(np.einsum("ijk,ijk->ij", delta, delta))
        iu = np.triu_indices(natoms, k=1)
        counts += np.histogram(dist[iu], bins=nbins, range=(0.0, nbins * dr))[0]
    edges = np.arange(nbins + 1) * dr
    r = 0.5 * (edges[:-1] + edges[1:])
    shell = 4.0 * np.pi * r**2 * dr
    expected = len(frames) * natoms * (natoms - 1) / 2.0 * shell / volume
    return r, counts / expected


def analizza_traiettoria(file: str | Path, ntherm: int) -> dict:
    """Read a ``run_md`` CSV, discard the first ``ntherm`` steps, average.

    Means and fluctuations are time averages over the production window
    (population standard deviation, ``ddof = 0``).
    """
    data = np.loadtxt(file, delimiter=",", skiprows=1)
    prod = data[ntherm:]
    if prod.size == 0:
        raise ValueError(f"ntherm={ntherm} leaves no production steps in {file}")
    temp = prod[:, 2]
    etot = prod[:, 5]
    return {
        "nsteps_total": int(data.shape[0]),
        "nprod": int(prod.shape[0]),
        "T_mean": float(temp.mean()),
        "dT_rel": float(temp.std() / temp.mean()),
        "E_mean": float(etot.mean()),
        "dE_rel": float(etot.std() / abs(etot.mean())),
        "ekin_mean": float(prod[:, 3].mean()),
        "epot_mean": float(prod[:, 4].mean()),
    }
