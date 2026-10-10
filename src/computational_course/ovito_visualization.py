"""Visualization utilities for OVITO in Jupyter notebooks."""

from pathlib import Path

import numpy as np
import ovito
from ipywidgets import HTML, GridBox, Layout, VBox
from ovito.gui import create_ipywidget
from ovito.io import import_file
from ovito.modifiers import PythonScriptModifier
from ovito.vis import Viewport

# =========================================================
# Project utilities
# =========================================================


def find_project_root(start: Path | None = None) -> Path:
    """Find the project root by searching for pyproject.toml.

    Parameters
    ----------
    start:
        Starting directory for the search. Defaults to current working directory.

    Returns
    -------
    Path
        The project root directory.

    Raises
    ------
    FileNotFoundError
        If pyproject.toml is not found in the directory tree.
    """
    if start is None:
        start = Path.cwd()

    for folder in [start, *start.parents]:
        if (folder / "pyproject.toml").exists():
            return folder

    raise FileNotFoundError(
        "Non riesco a trovare la root del progetto (cerco pyproject.toml)."
    )


def load_structure(
    filename: str, project_root: Path | None = None
) -> tuple[Path, np.ndarray]:
    """Load atomic coordinates from a text file.

    Parameters
    ----------
    filename:
        Name of the file in data/raw/.
    project_root:
        Project root directory. If None, automatically detected.

    Returns
    -------
    txt_path, coords
        Path to the loaded file and coordinate array (N, 3).

    Raises
    ------
    FileNotFoundError
        If the data file does not exist.
    """
    if project_root is None:
        project_root = find_project_root()

    txt_path = project_root / "data" / "raw" / filename

    if not txt_path.exists():
        data_dir = project_root / "data" / "raw"
        available = sorted(p.name for p in data_dir.glob("*.txt"))
        raise FileNotFoundError(
            f"File non trovato:\n{txt_path}\n\n"
            f"File .txt disponibili:\n" + "\n".join(available)
        )

    coords = np.loadtxt(txt_path)

    # Handle single-row case
    if coords.ndim == 1:
        coords = coords.reshape(1, -1)

    # Keep only x, y, z
    if coords.shape[1] < 3:
        raise ValueError(
            f"Il file deve contenere almeno 3 colonne x y z; trovate {coords.shape[1]}."
        )

    coords = coords[:, :3]

    return txt_path, coords


def convert_to_xyz(coords: np.ndarray, output_name: str, element: str = "Ag") -> Path:
    """Convert coordinates to XYZ format for OVITO.

    Parameters
    ----------
    coords:
        Atomic coordinates (N, 3).
    output_name:
        Base name for the output XYZ file.
    element:
        Element symbol (default: Ag).

    Returns
    -------
    Path
        Path to the created XYZ file.
    """
    OUT = Path("generated")
    OUT.mkdir(exist_ok=True)

    xyz_path = OUT / f"{output_name}.xyz"
    natoms = len(coords)

    with xyz_path.open("w", encoding="utf-8") as f:
        f.write(f"{natoms}\n")
        f.write(f"{element} structure\n")

        for x, y, z in coords:
            f.write(f"{element} {x:.8f} {y:.8f} {z:.8f}\n")

    return xyz_path


# =========================================================
# Geometric analysis
# =========================================================


def compute_neighbor_distances(
    coords: np.ndarray,
    reference_atom: int,
    r_min: float = 2.0,
    r_max: float = 3.0,
) -> dict:
    """Compute distances and neighbor information for a reference atom.

    Parameters
    ----------
    coords:
        Atomic coordinates (N, 3).
    reference_atom:
        Reference atom index (1-based, human counting).
    r_min, r_max:
        Distance range for first coordination shell.

    Returns
    -------
    dict
        Dictionary with:
        - 'neighbor_indices': indices of neighbors in first shell
        - 'neighbor_distances': distances to neighbors
        - 'coordination_number': number of neighbors
        - 'd_nn': median nearest-neighbor distance
        - 'atomic_radius': geometric radius (d_nn / 2)
        - 'a_fcc': estimated FCC lattice parameter
        - 'environment': human-readable environment description
    """
    natoms = len(coords)

    if not 1 <= reference_atom <= natoms:
        raise ValueError(f"reference_atom={reference_atom} out of range [1, {natoms}]")

    reference_index = reference_atom - 1
    reference_position = coords[reference_index]

    # Compute distances
    dr = coords - reference_position
    distances = np.linalg.norm(dr, axis=1)

    # First coordination shell
    neighbor_mask = (distances > r_min) & (distances < r_max)
    neighbor_indices = np.where(neighbor_mask)[0]
    neighbor_distances = distances[neighbor_mask]

    if len(neighbor_distances) == 0:
        raise ValueError(
            f"Nessun vicino trovato nell'intervallo {r_min} < d < {r_max} Å."
        )

    # Geometric quantities
    d_nn = np.median(neighbor_distances)
    atomic_radius = d_nn / 2.0
    a_fcc = np.sqrt(2.0) * d_nn

    # Environment classification
    cn = len(neighbor_indices)
    if cn == 12:
        environment = "FCC bulk"
    elif cn == 8:
        environment = "superficie FCC(100)"
    elif cn == 4:
        environment = "singolo layer FCC(100)"
    elif cn < 4:
        environment = "fortemente sottocoordinato"
    elif cn < 8:
        environment = "sottocoordinato / bordo"
    elif cn < 12:
        environment = "sottocoordinato rispetto al bulk"
    else:
        environment = "coordinazione anomala"

    return {
        "neighbor_indices": neighbor_indices,
        "neighbor_distances": neighbor_distances,
        "coordination_number": cn,
        "d_nn": d_nn,
        "atomic_radius": atomic_radius,
        "a_fcc": a_fcc,
        "environment": environment,
    }


def create_ovito_pipeline(
    xyz_path: Path,
    coords: np.ndarray,
    neighbor_mask: np.ndarray,
    reference_index: int,
    atomic_radius: float,
    background_radius_scale: float = 0.38,
    background_transparency: float = 0.85,
):
    """Create an OVITO pipeline with colored and sized atoms.

    Parameters
    ----------
    xyz_path:
        Path to the XYZ file.
    coords:
        Original coordinates array.
    neighbor_mask:
        Boolean array indicating first-shell neighbors.
    reference_index:
        Index of the reference atom (0-based).
    atomic_radius:
        Geometric radius of the atom.
    background_radius_scale:
        Scale factor for background atom visual radius.
    background_transparency:
        Transparency for background atoms (0=opaque, 1=transparent).

    Returns
    -------
    pipeline
        The configured OVITO pipeline.
    """
    natoms = len(coords)

    pipeline = import_file(str(xyz_path))

    def highlight_neighbors(_frame, data):
        n = data.particles.count

        if n != natoms:
            raise ValueError(f"OVITO contains {n} particles, expected {natoms}.")

        # Visual radii
        radii = np.full(n, atomic_radius * background_radius_scale, dtype=np.float32)
        radii[neighbor_mask] = atomic_radius
        radii[reference_index] = atomic_radius

        # Colors: gray background, red neighbors, yellow reference
        colors = np.full((n, 3), [0.72, 0.72, 0.72], dtype=np.float32)
        colors[neighbor_mask] = [1.00, 0.05, 0.05]
        colors[reference_index] = [1.00, 0.72, 0.00]

        # Transparency
        transparencies = np.full(n, background_transparency, dtype=np.float32)
        transparencies[neighbor_mask] = 0.0
        transparencies[reference_index] = 0.0

        data.particles_.create_property("Color", data=colors)
        data.particles_.create_property("Radius", data=radii)
        data.particles_.create_property("Transparency", data=transparencies)

    pipeline.modifiers.append(PythonScriptModifier(function=highlight_neighbors))
    pipeline.compute()

    return pipeline


# =========================================================
# Visualization panels
# =========================================================


def make_panel(
    view_type: Viewport.Type,
    title: str,
    plane: str,
    axis_html: str,
    camera_dir: tuple[float, float, float] | None = None,
    camera: dict | None = None,
    width: str = "100%",
    height: str = "310px",
) -> tuple[VBox, Viewport]:
    """Create a viewport panel with header and footer.

    Parameters
    ----------
    view_type:
        OVITO viewport type (Top, Front, Left, Perspective).
    title:
        Title to display in the header.
    plane:
        Plane identifier (e.g., "XY", "XZ").
    axis_html:
        HTML string for axis legend.
    camera_dir:
        Initial camera direction for the perspective view.
    camera:
        Full camera state from :func:`viewport_cameras`. When given, it
        overrides ``camera_dir`` and no automatic framing is applied, so the
        saved view is reproduced exactly.
    width, height:
        Panel dimensions.

    Returns
    -------
    tuple[VBox, Viewport]
        The Jupyter widget and the linked OVITO viewport. The widget is
        permanently linked to the viewport: user interaction updates it and
        vice versa.
    """
    vp = Viewport(type=view_type)
    if camera is not None:
        vp.camera_dir = tuple(camera["camera_dir"])
        vp.camera_pos = tuple(camera["camera_pos"])
        vp.camera_up = tuple(camera["camera_up"])
        vp.fov = camera["fov"]
    else:
        if camera_dir is not None:
            vp.camera_dir = camera_dir
        vp.zoom_all()

    viewer = create_ipywidget(
        vp,
        antialiasing=True,
        picking=False,
        layout=Layout(width=width, height=height),
    )

    header = HTML(
        value=f"""
        <div style="
            background:#202225;
            color:#f2f2f2;
            padding:7px 10px;
            font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size:14px;
            border-bottom:1px solid #444;
            display:flex;
            align-items:center;
            justify-content:space-between;
        ">
            <span style="font-weight:600;">{title}</span>
            <span style="color:#aaa; font-size:12px;">{plane}</span>
        </div>
    """
    )

    footer = HTML(
        value=f"""
        <div style="
            background:#202225;
            color:#ddd;
            padding:6px 10px;
            font-family:Menlo, Monaco, monospace;
            font-size:12px;
            border-top:1px solid #444;
            display:flex;
            align-items:center;
            justify-content:space-between;
        ">
            <span>{axis_html}</span>
            <span style="color:#888;">OVITO</span>
        </div>
    """
    )

    panel = VBox(
        [header, viewer, footer],
        layout=Layout(width=width, border="1px solid #444", overflow="hidden"),
    )
    return panel, vp


# Grid cell rectangles in normalized coordinates: Top, Front, Left, Perspective.
GRID_CELLS = [
    (0.0, 0.0, 0.5, 0.5),
    (0.5, 0.0, 0.5, 0.5),
    (0.0, 0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5, 0.5),
]

# Axis legend templates
TOP_AXES = """<span style="color:#ff5555;">x →</span> <span style="color:#55cc55;">y ↑</span> <span style="color:#888;">view −z</span>"""
FRONT_AXES = """<span style="color:#ff5555;">x →</span> <span style="color:#668cff;">z ↑</span> <span style="color:#888;">view −y</span>"""
LEFT_AXES = """<span style="color:#55cc55;">y →</span> <span style="color:#668cff;">z ↑</span> <span style="color:#888;">view +x</span>"""
PERSPECTIVE_AXES = """<span style="color:#ff5555;">x</span> <span style="color:#55cc55;">y</span> <span style="color:#668cff;">z</span> <span style="color:#888;">3D</span>"""


def create_viewport_grid(
    r_min: float,
    r_max: float,
    reference_atom: int,
    show_context: bool = True,
    cameras: list[dict] | None = None,
) -> tuple[GridBox, list[Viewport]]:
    """Create a 2×2 grid of viewport panels (Top, Front, Left, Perspective).

    The four viewports are returned alongside the widget so the same camera
    objects can later be rendered with :func:`render_viewport_grid`. User
    interactions in the widget update these viewport objects live.

    Parameters
    ----------
    r_min, r_max:
        Distance range for neighbor visualization.
    reference_atom:
        Reference atom number (for legend).
    show_context:
        Whether to show "context" in legend.
    cameras:
        Optional list of 4 camera states from :func:`viewport_cameras`, applied
        in panel order. Use this to freeze the views chosen interactively so
        the static render (and the built book) reproduces them.

    Returns
    -------
    tuple[GridBox, list[Viewport]]
        The Jupyter grid widget and the four linked OVITO viewports.
    """
    del show_context  # Parameter for future use

    # Note: Do not remove pipelines here. The notebook manages the pipeline lifecycle:
    # - the pipeline is added to the scene before this function is called
    # Removing pipelines here would leave the viewports empty.

    specs = [
        {
            "view_type": Viewport.Type.Top,
            "title": "Top",
            "plane": "XY",
            "axis_html": TOP_AXES,
        },
        {
            "view_type": Viewport.Type.Front,
            "title": "Front",
            "plane": "XZ",
            "axis_html": FRONT_AXES,
        },
        {
            "view_type": Viewport.Type.Left,
            "title": "Left",
            "plane": "YZ",
            "axis_html": LEFT_AXES,
        },
        {
            "view_type": Viewport.Type.Perspective,
            "title": "Perspective",
            "plane": "XYZ",
            "axis_html": PERSPECTIVE_AXES,
            "camera_dir": (1.0, 1.0, -0.8),
        },
    ]
    cameras = cameras if cameras is not None else [None] * len(specs)

    panels = []
    viewports = []
    for spec, camera in zip(specs, cameras):
        panel, vp = make_panel(**spec, camera=camera)
        panels.append(panel)
        viewports.append(vp)

    grid = GridBox(
        panels,
        layout=Layout(
            width="100%",
            grid_template_columns="repeat(2, minmax(0, 1fr))",
            grid_gap="8px",
        ),
    )
    return grid, viewports


def viewport_cameras(viewports: list[Viewport]) -> list[dict]:
    """Export the camera state of each viewport as plain Python data.

    The result can be pasted back into the notebook and passed to
    :func:`create_viewport_grid` (``cameras=...``) to reproduce the views the
    user picked interactively. ``camera_dir``, ``camera_pos``, ``camera_up``
    and ``fov`` fully determine a viewport's camera.
    """
    return [
        {
            "camera_dir": [float(v) for v in vp.camera_dir],
            "camera_pos": [float(v) for v in vp.camera_pos],
            "camera_up": [float(v) for v in vp.camera_up],
            "fov": float(vp.fov),
        }
        for vp in viewports
    ]


def render_viewport_grid(
    viewports: list[Viewport],
    output_path: Path,
    *,
    size: tuple[int, int] = (720, 720),
    background: tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> Path:
    """Render four viewports as a single 2×2 PNG for Jupyter Book.

    Static counterpart of :func:`create_viewport_grid`: pass the viewports
    returned by that function so the image reflects the current camera state
    (including any interactive changes made in the widget). The scene pipeline
    must already be attached (see :func:`create_ovito_pipeline`).

    Parameters
    ----------
    viewports:
        The four viewports in Top, Front, Left, Perspective order.
    output_path:
        Destination PNG path; parent directories are created if missing.
    size:
        Total image size in pixels; each of the four panels gets half.
    background:
        RGB background color in ``[0, 1]``.

    Returns
    -------
    Path
        The path of the written PNG file.
    """
    layout = list(zip(viewports, GRID_CELLS))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    viewports[0].render_image(
        size=size,
        layout=layout,
        background=background,
        filename=str(output_path),
    )
    return output_path


# =========================================================
# Report utilities
# =========================================================


def print_analysis_report(
    reference_atom: int,
    reference_position: np.ndarray,
    r_min: float,
    r_max: float,
    results: dict,
    max_print: int = 20,
) -> None:
    """Print a formatted analysis report.

    Parameters
    ----------
    reference_atom:
        Reference atom number (1-based).
    reference_position:
        Reference atom coordinates.
    r_min, r_max:
        Distance range used.
    results:
        Dictionary from compute_neighbor_distances.
    max_print:
        Maximum number of neighbors to print.
    """
    print("=" * 65)
    print(" ANALISI GEOMETRICA LOCALE")
    print("=" * 65)

    print(f"\nAtomo di riferimento : {reference_atom}")
    print(
        f"Posizione [Å]        : "
        f"({reference_position[0]:.4f}, {reference_position[1]:.4f}, {reference_position[2]:.4f})"
    )
    print(f"Intervallo           : {r_min:.2f} < d < {r_max:.2f} Å")
    print(f"Numero di vicini     : {results['coordination_number']}")
    print(f"Ambiente locale      : {results['environment']}")
    print(f"d_nn                 : {results['d_nn']:.4f} Å")
    print(f"R geometrico FCC     : {results['atomic_radius']:.4f} Å")
    print(f"a FCC stimato        : {results['a_fcc']:.4f} Å")

    print("\nPrimi vicini:")
    for i in results["neighbor_indices"][:max_print]:
        print(f"  Atom {i + 1:5d}")

    if results["coordination_number"] > max_print:
        print(f"  ... altri {results['coordination_number'] - max_print} atomi")


# =========================================================
# Static visualization for Jupyter Book (py3dmol)
# =========================================================


def create_py3dmol_view(
    xyz_path: Path,
    width: int = 600,
    height: int = 400,
    style: str = "cartoon",
    colorscheme: str = "Jmol",
) -> "py3Dmol.view":
    """Create an interactive py3dmol viewer for static Jupyter Book.

    This function generates an interactive 3D visualization that works
    in static HTML contexts (GitHub, web, PDF) where OVITO widgets
    cannot render.

    Parameters
    ----------
    xyz_path:
        Path to the XYZ file.
    width, height:
        Viewer dimensions in pixels.
    style:
        Atom representation style ('cartoon', 'sphere', 'stick').
    colorscheme:
        Color scheme for atoms ('Jmol', 'spectrum', 'ssCartoon').

    Returns
    -------
    py3Dmol.view
        Interactive viewer object that renders in Jupyter Book.

    Examples
    --------
    >>> from pathlib import Path
    >>> xyz_file = Path("book/generated/fcc100a864.xyz")
    >>> viewer = create_py3dmol_view(xyz_file, width=700, height=500)
    >>> viewer._make_html()  # Renders in notebook/book
    """
    import py3Dmol

    view = py3Dmol.view(width=width, height=height)

    # Load XYZ file
    with open(xyz_path) as f:
        xyz_content = f.read()

    view.addModel(xyz_content, "xyz")

    # Set rendering style
    if style == "cartoon":
        view.setStyle({}, {"cartoon": {"color": colorscheme}})
    elif style == "sphere":
        view.setStyle({}, {"sphere": {"colorscheme": colorscheme}})
    elif style == "stick":
        view.setStyle({}, {"stick": {"radius": 0.15, "colorscheme": colorscheme}})
    else:
        raise ValueError(
            f"Unknown style: {style}. Use 'cartoon', 'sphere', or 'stick'."
        )

    view.zoomTo()
    return view


def create_py3dmol_view_with_highlight(
    xyz_path: Path,
    neighbor_indices: np.ndarray | None = None,
    reference_index: int | None = None,
    width: int = 600,
    height: int = 400,
) -> "py3Dmol.view":
    """Create a py3dmol viewer with highlighted reference and neighbor atoms.

    Mimics the OVITO visualization: gray background atoms, red neighbors,
    yellow reference atom.

    Parameters
    ----------
    xyz_path:
        Path to the XYZ file.
    neighbor_indices:
        Array of neighbor atom indices (0-based).
    reference_index:
        Index of the reference atom (0-based). If None, no reference highlighting.
    width, height:
        Viewer dimensions in pixels.

    Returns
    -------
    py3Dmol.view
        Interactive viewer with atom highlighting.

    Examples
    --------
    >>> viewer = create_py3dmol_view_with_highlight(
    ...     xyz_file,
    ...     neighbor_indices=np.array([0, 2, 4]),
    ...     reference_index=1
    ... )
    """
    import py3Dmol

    view = py3Dmol.view(width=width, height=height)

    with open(xyz_path) as f:
        xyz_content = f.read()

    view.addModel(xyz_content, "xyz")

    # Default: all atoms gray
    view.setStyle({}, {"sphere": {"colorscheme": "Jmol", "scale": 0.3}})

    # Highlight neighbors (red)
    if neighbor_indices is not None:
        for idx in np.atleast_1d(neighbor_indices):
            view.setStyle(
                {"serial": int(idx) + 1}, {"sphere": {"color": "red", "scale": 0.5}}
            )

    # Highlight reference (yellow)
    if reference_index is not None:
        view.setStyle(
            {"serial": reference_index + 1},
            {"sphere": {"color": "yellow", "scale": 0.5}},
        )

    view.zoomTo()
    return view


# Export public API
__all__ = [
    "FRONT_AXES",
    "GRID_CELLS",
    "LEFT_AXES",
    "PERSPECTIVE_AXES",
    "TOP_AXES",
    "compute_neighbor_distances",
    "convert_to_xyz",
    "create_ovito_pipeline",
    "create_py3dmol_view",
    "create_py3dmol_view_with_highlight",
    "create_viewport_grid",
    "find_project_root",
    "load_structure",
    "make_panel",
    "print_analysis_report",
    "render_viewport_grid",
    "viewport_cameras",
]
