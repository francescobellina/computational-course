"""Scienza sul cluster reale: analisi del pattern FCC con OVITO + PTM.

Carica il cluster isolato di 108 atomi di Ag, identifica gli atomi con
struttura locale FCC tramite `PolyhedralTemplateMatchingModifier`, crea i
legami tra i primi vicini usando la prima shell di coordinazione misurata
dallo stesso PTM (nessun cutoff arbitrario), e produce una PNG ad alta
risoluzione con sfere 3D, legami sottili e la cella convenzionale FCC
orientata secondo il tensore di orientamento locale.

Uso:
    uv run python notebooks/04_handson_Ag_cutoff/fcc_pattern_ptm.py

Non aggiunge atomi virtuali, non impone periodicita' e non deforma le
coordinate: e' un'analisi del cluster com'e'.
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

import numpy as np
from ovito.io import import_file
from ovito.modifiers import (
    CreateBondsModifier,
    PolyhedralTemplateMatchingModifier,
    PythonScriptModifier,
)
from ovito.vis import Viewport

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from computational_course.ovito_visualization import (
    convert_to_xyz,
    load_structure,
    render_viewport_grid,
)

FILENAME = "fcc100a108.txt"
OUT_PNG = ROOT / "figures" / "fcc_pattern_ptm.png"

N_AXIS_COLORS = np.array([[1.0, 0.05, 0.05], [0.10, 0.75, 0.15], [0.15, 0.35, 1.0]])


def quaternion_to_matrix(q: np.ndarray) -> np.ndarray:
    """Convert a quaternion ``(w, x, y, z)`` to a 3x3 rotation matrix."""
    w, x, y, z = q
    return np.array(
        [
            [1 - 2 * (y**2 + z**2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x**2 + z**2), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x**2 + y**2)],
        ]
    )


def cluster_pipeline(xyz_path: Path, d_nn: float):
    """Pipeline: PTM (struttura + orientamento), bond primi vicini, stile."""
    pipeline = import_file(str(xyz_path))
    pipeline.modifiers.append(
        PolyhedralTemplateMatchingModifier(
            output_rmsd=True,
            output_interatomic_distance=True,
            output_orientation=True,
        )
    )
    pipeline.modifiers.append(
        CreateBondsModifier(
            cutoff=d_nn * 1.15, mode=CreateBondsModifier.Mode.Uniform
        )
    )

    def style(_frame, data):
        n = data.particles.count
        structure = data.particles["Structure Type"]
        colors = np.full((n, 3), [0.68, 0.68, 0.68])  # "Other"
        colors[structure.array == 1] = [0.05, 0.72, 0.40]  # FCC
        data.particles_.create_property("Radius", data=np.full(n, d_nn / 2 * 0.9))
        data.particles_.create_property("Color", data=colors)
        if data.particles.bonds is not None:
            data.particles.bonds.vis.width = 0.18
            data.particles.bonds.vis.color = (0.25, 0.25, 0.25)

    pipeline.modifiers.append(PythonScriptModifier(function=style))
    pipeline.compute()
    return pipeline


def cell_frame_pipeline(center: np.ndarray, rot: np.ndarray, a: float) -> tuple:
    """Overlay: 12 spigoli della cella convenzionale orientata da ``rot``.

    Corner sites are drawn with zero radius (invisible), only the edge bonds
    are visible. Edge colour encodes the direction (x rosso, y verde, z blu)
    so the local FCC orientation reads directly.
    """
    axes = rot * a
    corners = np.array(
        [(ix, iy, iz) for iz in (0, 1) for iy in (0, 1) for ix in (0, 1)], float
    ) @ axes + center

    topo: list[tuple[int, int]] = []
    colors: list = []
    for axis, nxt in enumerate((1, 2, 4)):  # offset in corner index per axis
        for u in (0, 1):
            for v in (0, 1):
                start = v * 4 + u * 2 if axis == 0 else (v * 4 + u) if axis == 1 else u * 2 + v
                topo.append((start, start + nxt))
                colors.append(N_AXIS_COLORS[axis])
    topo = np.array(topo, dtype=np.int64)
    colors = np.array(colors)

    xyz_path = convert_to_xyz(corners, "fcc_cell_frame", element="Ag")

    def style(_frame, data):
        n = data.particles.count
        data.particles_.create_property("Radius", data=np.zeros(n))
        data.particles_.create_property("Color", data=np.zeros((n, 3)))
        bonds_data = data.particles_.create_bonds()
        bonds_data.create_property("Topology", data=topo)
        bonds_data.create_property("Color", data=colors)
        bonds_data.vis.width = 2.5

    pipeline = import_file(str(xyz_path))
    pipeline.modifiers.append(PythonScriptModifier(function=style))
    pipeline.compute()
    return pipeline, corners


def main() -> int:
    txt_path, coords = load_structure(FILENAME, project_root=ROOT)
    xyz_path = convert_to_xyz(coords, txt_path.stem, element="Ag")

    probe = import_file(str(xyz_path))
    probe.modifiers.append(
        PolyhedralTemplateMatchingModifier(
            output_rmsd=True, output_interatomic_distance=True, output_orientation=True
        )
    )
    ptm_data = probe.compute()

    structure = ptm_data.particles["Structure Type"]
    interatomic = ptm_data.particles["Interatomic Distance"]
    rmsd = ptm_data.particles["RMSD"]
    orientation = ptm_data.particles["Orientation"]

    fcc_atoms = [int(i) for i, s in enumerate(structure) if int(s) == 1]
    report = {
        "n_atoms": len(coords),
        "ptm_counts": dict(
            collections.Counter(int(s) for s in structure)
        ),
        "n_fcc": len(fcc_atoms),
        "d_nn": float(np.median([interatomic[i] for i in fcc_atoms])) if fcc_atoms else None,
    }

    print(f"PTM struct. type counts: {report['ptm_counts']}")
    print(f"atomi FCC identificati : {report['n_fcc']}")
    if report["d_nn"]:
        print(f"prima shell misurata (PTM, mediana): {report['d_nn']:.4f} A")

    scene_pipelines = [cluster_pipeline(xyz_path, report["d_nn"])]

    if fcc_atoms:
        center = np.array(ptm_data.particles["Position"][fcc_atoms[0]])
        rot = quaternion_to_matrix(np.array(orientation[fcc_atoms[0]]))
        rmsd_best = float(rmsd[fcc_atoms[0]])
        a = report["d_nn"] * np.sqrt(2.0)
        print(f"orientazione (quaternione) atomo {fcc_atoms[0]}: {orientation[fcc_atoms[0]]}")
        print(f"RMSD del reticolo locale  : {rmsd_best:.3e}")
        print(f"cella convenzionale      : a = {a:.4f} A")

        if rmsd_best > 0.5:
            print("ATTENZIONE: RMSD alto, orientamento non affidabile; cella omessa.")
        else:
            frame, _ = cell_frame_pipeline(center, rot, a)
            scene_pipelines.append(frame)

    for pipe in scene_pipelines:
        pipe.add_to_scene()

    viewports = []
    for view_type in (Viewport.Type.Top, Viewport.Type.Front, Viewport.Type.Left, Viewport.Type.Perspective):
        vp = Viewport()
        vp.type = view_type
        vp.zoom_all()
        viewports.append(vp)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    out = render_viewport_grid(viewports, OUT_PNG, size=(1600, 1600))
    print(f"PNG esportato: {out}")

    for pipe in scene_pipelines:
        pipe.remove_from_scene()
    return 0


if __name__ == "__main__":
    sys.exit(main())