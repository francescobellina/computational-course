"""Root-finding algorithms used in the course."""

from collections.abc import Callable


def newton(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    *,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> tuple[float, list[float]]:
    """Solve ``f(x) = 0`` with Newton's method.

    Parameters
    ----------
    f, df:
        Function and derivative.
    x0:
        Initial guess.
    tol:
        Absolute tolerance on the residual and relative step size.
    max_iter:
        Maximum number of Newton updates.

    Returns
    -------
    root, history:
        Approximate root and all iterates, including ``x0``.

    Raises
    ------
    ZeroDivisionError
        If the derivative is zero at an iterate.
    RuntimeError
        If convergence is not reached within ``max_iter`` updates.
    """
    if tol <= 0:
        raise ValueError("tol must be positive")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")

    x = float(x0)
    history = [x]

    for _ in range(max_iter):
        fx = float(f(x))
        if abs(fx) <= tol:
            return x, history

        dfx = float(df(x))
        if dfx == 0.0:
            raise ZeroDivisionError(f"zero derivative encountered at x={x!r}")

        x_new = x - fx / dfx
        history.append(x_new)

        if abs(x_new - x) <= tol * (1.0 + abs(x_new)):
            return x_new, history

        x = x_new

    raise RuntimeError(f"Newton's method did not converge in {max_iter} iterations")
