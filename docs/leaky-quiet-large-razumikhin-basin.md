# A 381-fold larger complete-history quiet basin

Status: **directed theorem at the declared center parameters and physical
delays.**  Let

\[
 E_q=(\alpha,\alpha-\tfrac14),\qquad
 \alpha=(3/4)^{1/3},\qquad
 V(z)=z^TPz,
\]

where

\[
 P=\begin{pmatrix}2823/100&-1351/50\\-1351/50&13759/100\end{pmatrix}.
\]

For the scalar RFDE with delays \((4\sqrt5,5\sqrt5)\), every continuous
initial history satisfying

\[
 M_0:=\sup_{-5\sqrt5\leq\theta\leq0}
 V(\phi(\theta)-E_q)\leq\frac1{125}
\]

obeys

\[
 V(z(t))\leq e^{-t/10000}M_0,\qquad t\geq0.
\]

In particular, the history sublevel is forward invariant and every history
in it converges to the quiet equilibrium.  Its level is
\(8000/21\), approximately \(380.95\), times the earlier level
\(21/10^6\).  This theorem does **not** prove that the physical \(J=0.30\)
pulse enters the sublevel, and it proves neither an onset threshold nor a
global quiet basin.

## Elliptic and radial reduction

Write \(z=(x,y)=q(X,Y)\), where \(0\leq q\leq1\), and parameterize the
boundary \(Z^TPZ=1/125\) by

\[
 X=r_x\cos\vartheta,
 \qquad
 Y=-\frac{p_{12}}{p_{22}}X+r_y\sin\vartheta,
\]

with

\[
 r_x^2=\frac{(1/125)p_{22}}{\det P},
 \qquad r_y^2=\frac{1/125}{p_{22}}.
\]

Completing the square proves this identity exactly.  Conversely, every
nonzero point of the ellipsoid has this representation with
\(q^2=125V(z)\).  The zero point is handled directly.

Suppose the two delayed states satisfy the Razumikhin inequalities

\[
 V(z(t-\tau_j))\leq\rho V(z(t)),
 \qquad \rho=\frac{101}{100},\quad j=0,1.
\]

For \(q>0\), write the delayed voltage deviations as \(qD_j\).  Minimizing
the quadratic form over the recovery coordinate gives

\[
 |D_j|\leq\sqrt\rho\,r_x.
\]

This is why the delayed radius is multiplied by \(\sqrt\rho\), not by
\(\rho\).

Put \(\beta=\alpha-1\).  After division by \(q\), the delayed contribution
from one slot is, apart from its positive common weight,

\[
 g_q(D)=\kappa_1D+\kappa_3
 \{3\beta^2D+3\beta qD^2+q^2D^3\}.
\]

It is strictly increasing because

\[
 \partial_Dg_q(D)=\kappa_1+3\kappa_3(\beta+qD)^2>0.
\]

The original RFDE contains the average of two slots.  They can be maximized
independently: if \((PZ)_1>0\), both take \(D_j=\sqrt\rho r_x\); if
\((PZ)_1<0\), both take \(D_j=-\sqrt\rho r_x\).  When an angular interval
does not determine the sign of \((PZ)_1\), the implementation retains the
whole delayed interval rather than selecting an endpoint.  Exactly two of
the 16,384 angular cells require this sign-indeterminate treatment.

With the maximizing endpoint inserted, define

\[
 G(q,Z)=\frac{\dot V}{2q^2}.
\]

The exact two-slot perturbation identity shows that \(G\) is a polynomial
of degree two in \(q\).  If its power coefficients are
\(c_0+c_1q+c_2q^2\), its Bernstein coefficients on \([0,1]\) are

\[
 c_0,\qquad c_0+\frac{c_1}{2},\qquad c_0+c_1+c_2.
\]

Their convex-hull property therefore bounds every radial value, including
the endpoints.

## Directed cover and decay rate

The implementation encloses \(\alpha=(3/4)^{1/3}\) with directed MPFR and
checks the two endpoint cubes against \(3/4\) as exact rational numbers.
It then covers the full angular circle with 16,384 outward-rounded,
160-bit MPFR cells.  Every degree-two Bernstein upper bound is negative.
The largest is

\[
 G\leq-8.9026059458613079\times10^{-6}.
\]

Since \(V=q^2/125\), the factor of two in \(\dot V=2z^TP\dot z\) gives

\[
 \dot V\leq-\underline\kappa V,
 \qquad
 \underline\kappa
 =0.0022256514864653269\ldots,
\]

whenever the two Razumikhin inequalities hold and \(V(z(t))\leq1/125\).
Thus \(\underline\kappa-10^{-4}>0.0021256514864653269\).

For \(r=5\sqrt5\) and \(\lambda=10^{-4}\), exact rational comparisons give

\[
 r<\frac{45}{4},\qquad
 \lambda r<\frac9{8000},\qquad
 e^{\lambda r}<\frac{1}{1-9/8000}
 =\frac{8000}{7991}<\frac{101}{100}=\rho.
\]

Here \(e^x\leq(1-x)^{-1}\) for \(0\leq x<1\).

For completeness, let \(W(t)=e^{\lambda t}V(z(t))\).  If
\(0<W(0)=M_0\), the Razumikhin conditions hold at \(t=0\) with ratio one,
so \(W'(0)<0\); hence \(W<M_0\) immediately afterward.  Thus any violation
of \(W(t)\leq M_0\), whether \(W(0)<M_0\) or \(W(0)=M_0\), has a first
positive return time \(t_*\) at which \(W(t_*)=M_0\), all earlier values are
at most \(M_0\), and \(W'(t_*)\geq0\).  For each delayed time
\(s=t_*-\tau_j\), one has

\[
 V(z(s))\leq e^{\lambda\tau_j}V(z(t_*))<\rho V(z(t_*)).
\]

For \(s\geq0\), this follows from the first-crossing property of \(W\); for
\(s<0\), it follows from the definition of \(M_0\) and
\(t_*<\tau_j\).  Also \(V(z(t_*))\leq M_0\leq1/125\).  The certified
derivative inequality then yields

\[
 W'(t_*)\leq-(\underline\kappa-\lambda)W(t_*)<0,
\]

contradicting a first upward crossing.  The case \(M_0=0\) is the equilibrium
solution by uniqueness.  This proves both forward invariance and the stated
exponential estimate, including initial histories on the boundary.

## Remaining physical routing gate

A binary64 trajectory is useful only as a guide for where to place a later
terminal-history enclosure.  Promotion of physical pulse capture requires a
directed method-of-steps proof of the entire retained history.  Until that
separate gate closes, the present artifact makes no claim about \(J=0.30\),
the separator, or physical-pulse onset.
