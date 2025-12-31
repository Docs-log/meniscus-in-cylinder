# meniscus-in-cylinder

This repository provides a numerical solver for the axisymmetric meniscus shape
formed by a liquid inside a cylindrical container under gravity.

A browser-based interactive demo is available via GitHub Pages:
- **Live demo**: https://docs-log.github.io/meniscus-in-cylinder/

## Problem description

The solver computes the meniscus shape

$$z = z(r), \qquad 0 \le r \le R ,$$

where:

- $r$ is the radial coordinate measured from the cylinder axis,
- $z$ is the vertical displacement measured from the reference level at which  
  the Laplace pressure equals the atmospheric pressure,
- $R$ is the cylinder radius.

The liquid–air interface satisfies the Young–Laplace equation under gravity, with
a prescribed contact angle $\theta$ at the cylinder wall.

## Numerical method

- The governing equation is solved as a boundary-value problem using a **shooting method**.
- The shooting parameter is iteratively adjusted so that the boundary condition
  at the wall,
  
  $$z'(R) = \cot\theta ,$$

  is satisfied.
- The initial condition at the axis,
  
   $$z(0),$$
  
  is treated as an unknown shooting parameter.
- An initial guess for $z(0)$ is obtained from the small-slope linearization of the Young–Laplace equation, which reduces to a modified Bessel equation:
  
  $$z(0) \approx \frac{\cos\theta}{I_1(R / \ell_c)} ,$$
  
  where $I_1$ is the modified Bessel function of order one and
  $\ell_c$ is the capillary length. In practice, I found that replacing $\cot\theta$ by $\cos\theta$ in the initial guess for $z(0)$ yields significantly better convergence for the full nonlinear problem. The reason for this empirical improvement is not fully understood, but it appears to reflect the geometric nature of the contact-angle condition in the nonlinear regime.

## Implementation notes

- The solver is written in pure Python and does **not** depend on SciPy.
- A custom Runge–Kutta (RK4) integrator is used for the resulting system of ODEs.
- The modified Bessel function $I_1$ is evaluated using a polynomial approximation,
  making the code compatible with browser-based execution (e.g. via Pyodide).

## Additional details

A detailed derivation of the governing equations and the numerical approach
is described in the following blog post (in Japanese):

- https://linx.hatenadiary.jp/entry/meniscus_volume
