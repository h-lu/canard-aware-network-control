# Calibration model v0: weakly delayed van der Pol

This file fixes the first symbolic benchmark. It is not yet the network theorem.

## Fast-time equation

\[
\dot x=x-\frac{x^3}{3}+y
+J\bigl[x(t)-x(t-\tau)\bigr],
\qquad
\dot y=\varepsilon(a-x).
\tag{1}
\]

The right fold is \((x,y,a)=(1,-2/3,1)\). Introduce

\[
\delta=\sqrt\varepsilon,
\quad
x=1+\delta X,
\quad
y=-\frac23+\delta^2Y,
\quad
s=\delta t,
\tag{2}
\]

\[
J=\delta^2K,
\quad
\Theta=\delta\tau,
\quad
a=1+\delta^2\nu.
\tag{3}
\]

Then the transformation is exact:

\[
X'=Y-X^2
+\delta\left[-\frac{X^3}{3}
+K\bigl(X(s)-X(s-\Theta)\bigr)\right],
\qquad
Y'=-X+\delta\nu.
\tag{4}
\]

Primes denote \(d/ds\). The symbolic test in `tests/test_symbolic_blowup.py` verifies every power of \(\delta\).

## Consequences for the flagship analysis

1. Weak delayed feedback enters the fold chart at order \(\delta=\sqrt\varepsilon\).
2. The scaled delay \(\Theta\) is \(O(1)\), so a naive short-delay Taylor expansion of \(X(s-\Theta)\) is not justified.
3. A topology-weighted delay-moment law must come from the nonlocal center-manifold/history reduction and the adjoint Lin-gap functional, not from replacing \(\Theta\) by a fitted “effective delay.”
4. The network version inherits a sum of translated histories. Block-constant delays are sufficient for exact module closure but not necessary: it is enough that nodes in the same receiving module have the same row-weighted delay measure from every source module. Other edgewise-delay patterns are structural perturbations.

## First derivation task

Reproduce the leading center-manifold/history expansion in the same normalization as Zhang et al. (2026), then evaluate its contribution to the adjoint Lin-gap functional. Only after the coefficient is recovered for one oscillator should the calculation be lifted to the declared two-module network.

The scalar coefficients are now reproduced formally through \(O(\varepsilon^{3/2})\); see [leading delay-moment calibration](derivation-leading-moment.md). A uniform remainder and a well-posed Lin-gap interpretation remain to be proved before this becomes a threshold theorem. Only then is the network transfer addressed.
