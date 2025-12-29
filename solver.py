import math

import numpy as np


def bessel_i1(x: float) -> float:
    """
    Modified Bessel function of the first kind, order 1: I1(x)
    Cephes-like approximation.
    """
    ax = abs(x)
    if ax < 3.75:
        y = x / 3.75
        y2 = y * y
        val = ax * (
            0.5
            + y2
            * (
                0.87890594
                + y2 * (0.51498869 + y2 * (0.15084934 + y2 * (0.02658733 + y2 * (0.00301532 + y2 * 0.00032411))))
            )
        )
        return val if x >= 0 else -val
    else:
        y = 3.75 / ax
        poly = 0.39894228 + y * (
            -0.03988024
            + y
            * (
                -0.00362018
                + y
                * (
                    0.00163801
                    + y * (-0.01031555 + y * (0.02282967 + y * (-0.02895312 + y * (0.01787654 + y * -0.00420059))))
                )
            )
        )
        val = (math.exp(ax) / math.sqrt(ax)) * poly
        return val if x >= 0 else -val


def rk4_dd(f, df, x, zmin):
    z = np.empty_like(x)
    u = np.empty_like(x)
    z[0] = zmin
    u[0] = 0.0
    h = np.diff(x)
    for j in range(x.size - 1):
        k1 = f(x[j], z[j], u[j])
        l1 = df(x[j], z[j], u[j])
        k2 = f(x[j] + 0.5 * h[j], z[j] + 0.5 * h[j] * k1, u[j] + 0.5 * h[j] * l1)
        l2 = df(x[j] + 0.5 * h[j], z[j] + 0.5 * h[j] * k1, u[j] + 0.5 * h[j] * l1)
        k3 = f(x[j] + 0.5 * h[j], z[j] + 0.5 * h[j] * k2, u[j] + 0.5 * h[j] * l2)
        l3 = df(x[j] + 0.5 * h[j], z[j] + 0.5 * h[j] * k2, u[j] + 0.5 * h[j] * l2)
        k4 = f(x[j + 1], z[j] + h[j] * k3, u[j] + h[j] * l3)
        l4 = df(x[j + 1], z[j] + h[j] * k3, u[j] + h[j] * l3)

        z[j + 1] = z[j] + h[j] / 6 * (k1 + 2 * (k2 + k3) + k4)
        u[j + 1] = u[j] + h[j] / 6 * (l1 + 2 * (l2 + l3) + l4)

    return z, u


def shoot(zmin, u_goal, x, itr_max=20, dzmin=2e-6, tol=1e-12):
    itr = 0
    while itr < itr_max:
        diff = dzmin / (bc(zmin + dzmin, u_goal, x) / bc(zmin, u_goal, x) - 1)
        if np.abs(diff) < tol:
            return zmin
        zmin -= diff
        itr += 1

    assert itr < itr_max, "fail to find zmin"


def bc(zmin, u_goal, x):
    _, u = rk4_dd(dz, du, x, zmin)
    return u[-1] - u_goal


def dz(x, z, u):  # u := dz/dx
    return u


def du(x, z, u):  # du/dx
    fct = 1 + u * u
    return (z * np.sqrt(fct) - u / x) * fct if x != 0 else z * np.sqrt(fct) * fct


def meniscus_shape(r, rho, gamma, theta_deg, R, g):
    theta = math.radians(theta_deg)
    u_goal = 1.0 / np.tan(theta)

    # capillary length (rough scale)
    lc = math.sqrt(gamma / (max(rho, 1e-12) * g))
    x = r / lc

    # initial guess
    zmin_init = math.cos(theta) / bessel_i1(R / lc)

    # find meniscus shape
    zmin = shoot(zmin_init, u_goal, x)
    z, _ = rk4_dd(dz, du, x, zmin)

    return z * lc


def solve(params):
    """
    Entry point called from JavaScript.

    params: JsProxy (when called from JS) -> convert to Python dict by params.to_py()

    Returns a dict: {"x": [...], "y": [...], "csv": "..."}
    """
    if hasattr(params, "to_py"):
        params = params.to_py()

    rho = float(params.get("rho", 1000.0))
    gamma = float(params.get("gamma", 0.072))
    theta_deg = float(params.get("theta_deg", 30.0))
    R = float(params.get("R", 0.01))
    g = float(params.get("g", 9.80665))
    n = int(params.get("n", 200))

    r = np.linspace(0.0, R, max(n, 2))
    z = meniscus_shape(r, rho, gamma, theta_deg, R, g)

    # Build CSV
    lines = ["# r, z"]
    for ri, zi in zip(r, z):
        lines.append(f"{ri:.12g},{zi:.12g}")
    csv = "\n".join(lines) + "\n"

    return {"x": r.tolist(), "y": z.tolist(), "csv": csv}
