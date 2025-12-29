import math

import numpy as np


def _rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def _example_meniscus_profile(r, rho, gamma, theta_deg, R, g):
    """
    Placeholder model (NOT a full Young–Laplace solver):
    Produces a smooth curve with boundary slope based on contact angle.
    Replace this function with your real numerical solver.
    """
    # Capillary length (rough scale)
    lc = math.sqrt(gamma / (max(rho, 1e-12) * g))

    # Simple shape: z(r) = A * (1 - (r/R)^2) with A scaled by capillary length
    theta = math.radians(theta_deg)
    # crude amplitude scale
    A = lc * (math.cos(theta) if abs(theta) <= math.pi else 1.0)

    rr = r / max(R, 1e-12)
    z = A * (1.0 - rr * rr)
    return z


def solve(params):
    """
    Entry point called from JavaScript.

    params: JsProxy (when called from JS) -> convert to Python dict by params.to_py()

    Returns a dict: {"x": [...], "y": [...], "csv": "..."}
    """
    # --- FIX for: TypeError: 'pyodide.ffi.JsProxy' object is not subscriptable
    if hasattr(params, "to_py"):
        params = params.to_py()

    rho = float(params.get("rho", 1000.0))
    gamma = float(params.get("gamma", 0.072))
    theta_deg = float(params.get("theta_deg", 30.0))
    R = float(params.get("R", 0.01))
    g = float(params.get("g", 9.80665))
    n = int(params.get("n", 200))

    r = np.linspace(0.0, R, max(n, 2))
    z = np.array([_example_meniscus_profile(ri, rho, gamma, theta_deg, R, g) for ri in r], dtype=float)

    # Build CSV
    lines = ["r,z"]
    for ri, zi in zip(r, z):
        lines.append(f"{ri:.12g},{zi:.12g}")
    csv = "\n".join(lines) + "\n"

    return {"x": r.tolist(), "y": z.tolist(), "csv": csv}
