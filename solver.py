import math

import numpy as np


def solve_meniscus(*, rho: float, gamma: float, theta_deg: float, g: float, R: float, N: int):
    """
    r, z: 1D numpy arrays
    """
    theta = math.radians(theta_deg)

    # dummy
    r = np.linspace(0.0, R, int(N))
    amp = 0.15 * R * math.cos(theta)
    z = amp * (1.0 - (r / R) ** 2)
    return r, z
