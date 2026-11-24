"""LJ + 7th-degree polynomial junction, NVE dynamics and steepest descent (exam Exercise 1).

Same units as :mod:`computational_course.md`: eV, Angstrom, seconds, masses in
code units ``eV*s^2/A^2``.  The pair loop runs over all ``i < j`` pairs
(O(N^2), compiled with Numba) and handles periodicity per direction, so the
same code covers a free cluster (no PBC), a slab (PBC in x and y only) and a
bulk cell (PBC in all directions).

The P7 coefficients ``A, ..., H`` (degree 0, ..., 7) are not computed here:
the exercise asks to use the ones of the course file ``materials/poly7.py``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from numba import njit
from numpy.typing import ArrayLike, NDArray

from .md import instantaneous_T, kinetic_energy

#: ``energy_forces(pos) -> (epot, forces, inside)``; ``inside[m]`` tells whether
#: pair ``m`` (``np.triu_indices`` order) is closer than ``rc``.
EnergyForces = Callable[
    [NDArray[np.floating]], tuple[float, NDArray[np.floating], NDArray[np.bool_]]
]


@njit(cache=True)
def _lj_p7_kernel(pos, box, periodic, p7, dp7, sigma, epsilon, rp, rc, smooth):
    n = pos.shape[0]
    force = np.zeros_like(pos)
    inside = np.zeros(n * (n - 1) // 2, dtype=np.bool_)
    epot = 0.0
    rc2 = rc * rc
    m = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = pos[i, 0] - pos[j, 0]
            dy = pos[i, 1] - pos[j, 1]
            dz = pos[i, 2] - pos[j, 2]
            if periodic[0]:
                dx -= box[0] * np.rint(dx / box[0])
            if periodic[1]:
                dy -= box[1] * np.rint(dy / box[1])
            if periodic[2]:
                dz -= box[2] * np.rint(dz / box[2])
            r2 = dx * dx + dy * dy + dz * dz
            m += 1
            if r2 >= rc2:
                continue
            inside[m - 1] = True
            r = np.sqrt(r2)
            if smooth and r > rp:
                phi = p7[7]
                for q in range(6, -1, -1):
                    phi = phi * r + p7[q]
                dphi = dp7[6]
                for q in range(5, -1, -1):
                    dphi = dphi * r + dp7[q]
                f_over_r = -dphi / r
            else:
                sr6 = (sigma * sigma / r2) ** 3
                phi = 4.0 * epsilon * (sr6 * sr6 - sr6)
                f_over_r = 24.0 * epsilon * (2.0 * sr6 * sr6 - sr6) / r2
            epot += phi
            force[i, 0] += f_over_r * dx
            force[i, 1] += f_over_r * dy
            force[i, 2] += f_over_r * dz
            force[j, 0] -= f_over_r * dx
            force[j, 1] -= f_over_r * dy
            force[j, 2] -= f_over_r * dz
    return epot, force, inside


def lj_p7_model(
    sigma: float,
    epsilon: float,
    rc: float,
    *,
    rp: float | None = None,
    p7: ArrayLike | None = None,
    box: ArrayLike | None = None,
    periodic: Sequence[bool] = (False, False, False),
) -> EnergyForces:
    """Build the energy/force function of the Lennard-Jones model.

    Parameters
    ----------
    sigma, epsilon:
        Lennard-Jones parameters (Angstrom, eV).
    rc:
        Cutoff radius: pairs with ``r >= rc`` do not interact.
    rp:
        Start of the polynomial junction; ``None`` gives the sharp cutoff.
    p7:
        Coefficients ``A, ..., H`` of ``P7(r) = A + B r + ... + H r^7``,
        required when ``rp`` is given.
    box:
        Cell lengths ``(Lx, Ly, Lz)``, required if any direction is periodic.
    periodic:
        Minimum-image convention per direction, e.g. ``(True, True, False)``
        for a slab with free surfaces along z.

    Returns
    -------
    EnergyForces
        ``energy_forces(pos) -> (epot, forces, inside)``.
    """
    smooth = rp is not None
    if smooth:
        if p7 is None:
            raise ValueError("p7 is required when rp is given")
        if not 0.0 < rp < rc:
            raise ValueError("expected 0 < rp < rc")
        coeffs = np.asarray(p7, dtype=float)
        if coeffs.shape != (8,):
            raise ValueError("p7 must hold the 8 coefficients A, ..., H")
    else:
        coeffs = np.zeros(8)
    dcoeffs = np.polynomial.polynomial.polyder(coeffs)
    flags = np.asarray(periodic, dtype=np.bool_)
    if flags.shape != (3,):
        raise ValueError("periodic must have 3 entries (x, y, z)")
    if flags.any() and box is None:
        raise ValueError("box is required for periodic directions")
    cell = np.ones(3) if box is None else np.asarray(box, dtype=float)
    r_start = rp if smooth else rc

    def energy_forces(pos):
        return _lj_p7_kernel(
            np.ascontiguousarray(pos, dtype=float),
            cell,
            flags,
            coeffs,
            dcoeffs,
            sigma,
            epsilon,
            r_start,
            rc,
            smooth,
        )

    return energy_forces


def run_nve(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mass: float,
    dt: float,
    nsteps: int,
    energy_forces: EnergyForces,
    *,
    sample_every: int = 0,
    abort_factor: float = 0.5,
) -> dict:
    """NVE dynamics with velocity Verlet.

    Parameters
    ----------
    pos, vel:
        Initial positions and velocities, shape ``(N, 3)``.
    mass:
        Atomic mass in code units.
    dt:
        Time step in seconds.
    nsteps:
        Number of velocity-Verlet steps.
    energy_forces:
        Model built by :func:`lj_p7_model`.
    sample_every:
        If positive, store the positions every this many steps.
    abort_factor:
        Stop when ``|E(t) - E(0)| > abort_factor * |E(0)|`` or ``E`` is not
        finite (integration diverging); then ``stable`` is ``False`` and the
        arrays are filled up to the last good step (NaN after it).

    Returns
    -------
    dict
        ``time_ps``, ``ekin``, ``epot``, ``etot``, ``T`` (per step),
        ``n_cross`` (pairs crossing ``rc``, in either direction),
        ``stable``, ``frames`` and ``frame_steps`` (sampled positions),
        final ``pos`` and ``vel``.
    """
    pos = np.array(pos, dtype=float)
    vel = np.array(vel, dtype=float)
    natoms = pos.shape[0]
    epot, force, inside_prev = energy_forces(pos)
    e0 = kinetic_energy(vel, mass) + epot
    ekin = np.full(nsteps, np.nan)
    epot_h = np.full(nsteps, np.nan)
    frames, frame_steps = [], []
    n_cross = 0
    stable = True
    with np.errstate(all="ignore"):
        for step in range(nsteps):
            pos += vel * dt + 0.5 * (force / mass) * dt * dt
            epot, force_new, inside = energy_forces(pos)
            vel += (0.5 / mass) * (force + force_new) * dt
            force = force_new
            k = kinetic_energy(vel, mass)
            if not np.isfinite(k + epot) or abs(k + epot - e0) > abort_factor * abs(e0):
                stable = False
                break
            ekin[step] = k
            epot_h[step] = epot
            n_cross += int(np.count_nonzero(inside != inside_prev))
            inside_prev = inside
            if sample_every > 0 and (step + 1) % sample_every == 0:
                frames.append(pos.copy())
                frame_steps.append(step + 1)
    return {
        "time_ps": np.arange(1, nsteps + 1) * dt * 1e12,
        "ekin": ekin,
        "epot": epot_h,
        "etot": ekin + epot_h,
        "T": np.array([instantaneous_T(k, natoms) for k in ekin]),
        "n_cross": n_cross,
        "stable": stable,
        "frames": np.array(frames),
        "frame_steps": np.array(frame_steps, dtype=int),
        "pos": pos,
        "vel": vel,
    }


def remove_angular_momentum(
    pos: NDArray[np.floating], vel: NDArray[np.floating], mass: float
) -> NDArray[np.floating]:
    """Remove the rigid rotation ``omega x (r - r_cm)`` from the velocities.

    For an isolated cluster the angular momentum is conserved, so any
    initial value makes the whole cluster rotate for the entire run.  The
    total momentum is left unchanged; the temperature drops slightly and is
    usually rescaled afterwards.
    """
    rel = pos - pos.mean(axis=0)
    ang_mom = mass * np.cross(rel, vel).sum(axis=0)
    inertia = mass * (np.einsum("ij,ij->", rel, rel) * np.eye(3) - rel.T @ rel)
    omega = np.linalg.solve(inertia, ang_mom)
    return vel - np.cross(omega, rel)


def production_stats(res: dict, ntherm: int) -> dict:
    """Time averages after discarding the first ``ntherm`` steps.

    ``dE_rel`` is the course criterion ``delta E / |<E>|`` with ``delta E``
    the standard deviation of the total energy; NaN if the run diverged.
    """
    if not res["stable"]:
        return {"T_mean": np.nan, "E_mean": np.nan, "dE_rel": np.nan}
    temp = res["T"][ntherm:]
    etot = res["etot"][ntherm:]
    if etot.size == 0:
        raise ValueError(f"ntherm={ntherm} leaves no production steps")
    return {
        "T_mean": float(temp.mean()),
        "E_mean": float(etot.mean()),
        "dE_rel": float(etot.std() / abs(etot.mean())),
    }


def max_force(force: NDArray[np.floating]) -> float:
    """Largest force modulus ``max_k |F(k)|``."""
    return float(np.sqrt(np.einsum("ij,ij->i", force, force)).max())


def steepest_descent(
    pos: NDArray[np.floating],
    energy_forces: EnergyForces,
    *,
    c: float = 0.005,
    ftol: float = 1e-3,
    max_iter: int = 20_000,
    adaptive: bool = False,
    grow: float = 1.1,
    shrink: float = 0.5,
) -> dict:
    """Local minimization ``r(k) <- r(k) + C F(k)`` until ``max|F| < ftol``.

    Parameters
    ----------
    pos:
        Starting configuration, shape ``(N, 3)``.
    energy_forces:
        Model built by :func:`lj_p7_model`.
    c:
        Step coefficient ``C`` in ``A^2/eV`` (initial value if adaptive).
    ftol:
        Convergence threshold on the largest force modulus, in eV/A.
    max_iter:
        Maximum number of iterations (force evaluations).
    adaptive:
        If ``True``, a step that raises the energy is rejected and ``C`` is
        multiplied by ``shrink``; an accepted step multiplies ``C`` by ``grow``.

    Returns
    -------
    dict
        ``pos`` (final), ``energy`` and ``fmax`` (one value per iteration,
        starting configuration included), ``c`` (``C`` used at each
        iteration), ``converged``, ``n_iter``.
    """
    pos = np.array(pos, dtype=float)
    epot, force, _ = energy_forces(pos)
    energies, fmaxs, cs = [], [], []
    converged = False
    for _ in range(max_iter):
        fmax = max_force(force)
        energies.append(epot)
        fmaxs.append(fmax)
        cs.append(c)
        if fmax < ftol:
            converged = True
            break
        if not np.isfinite(epot + fmax):
            break
        trial = pos + c * force
        e_trial, f_trial, _ = energy_forces(trial)
        if adaptive and e_trial > epot:
            c *= shrink
            continue
        pos, epot, force = trial, e_trial, f_trial
        if adaptive:
            c *= grow
    return {
        "pos": pos,
        "energy": np.array(energies),
        "fmax": np.array(fmaxs),
        "c": np.array(cs),
        "converged": converged,
        "n_iter": len(energies) - 1,
    }
