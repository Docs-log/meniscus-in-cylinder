# meniscus-in-cylinder

This repository provides a numerical solver for the axisymmetric meniscus shape
formed by a liquid inside a cylindrical container.

## Problem description

The solver computes the meniscus profile 

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
- The initial condition at the axis,
  
   $$z(0),$$
  
  is treated as an unknown shooting parameter.
- An initial guess for $z(0)$ is constructed from the linearized solution:
  
  $$z(0) \approx \frac{\cos\theta}{I_1(R / \ell_c)} ,$$
  
  where $I_1$ is the modified Bessel function of order one and
  $\ell_c$ is the capillary length.
- The shooting parameter is iteratively adjusted so that the boundary condition
  at the wall,
  
  $$z'(R) = \cot\theta ,$$

  is satisfied.

## Implementation notes

- The solver is written in pure Python and does **not** depend on SciPy.
- A custom Runge–Kutta (RK4) integrator is used for the resulting system of ODEs.
- The modified Bessel function $I_1$ is evaluated using a polynomial approximation,
  making the code compatible with browser-based execution (e.g. via Pyodide).

## Additional details

A detailed derivation of the governing equations and the numerical approach
is described in the following blog post (in Japanese):

- https://linx.hatenadiary.jp/entry/meniscus_volume
