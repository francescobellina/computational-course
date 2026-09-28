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

    from computational_course import newton

    root, _ = newton(lambda x: x**2 - 2, lambda x: 2 * x, 1.5)
    print(f"package import OK; sqrt(2) ≈ {root:.12f}")


if __name__ == "__main__":
    main()
