"""Fast local smoke checks for the course environment."""

from importlib import import_module

PACKAGES = [
    "numpy",
    "scipy",
    "matplotlib",
    "pandas",
    "sympy",
    "jupyter",
    "jupyter_book",
    "pytest",
]


def main() -> None:
    for name in PACKAGES:
        module = import_module(name)
        version = getattr(module, "__version__", "installed")
        print(f"{name:12s} {version}")

    from computational_course import lennard_jones_pair

    phi_min = lennard_jones_pair(2 ** (1 / 6), 1.0, 1.0)
    print(f"package import OK; phi_LJ at the minimum = {phi_min:.6f} eps (expected -1)")


if __name__ == "__main__":
    main()
