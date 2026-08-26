# Inner stable manifold: qualitative theorem and quantitative Stage 1

## Status

There are two deliberately separate conclusions.

1. **Qualitative theorem (proved).**  The validated inner periodic orbit has a
   local (C^1) stable manifold of codimension one in the full history space.
   The exact split reduced-history factorization transfers this to a local
   (C^1), codimension-one stable sheet in a centered reduced-history
   transverse section.
2. **Quantitative graph and pulse onset (open).**  No explicit graph radius,
   graph norm, pulse-section transversality bound, separator crossing, unique
   pulse onset, or two-sided basin-routing statement is proved.  Every such
   flag in the registered result is false.

The distinction matters: existence of an abstract local stable manifold is
not a numerical enclosure of the particular voltage section used by the
third-return pulse experiment.

## Qualitative stable-manifold audit

The invoked result is Hale and Verduyn Lunel, *Introduction to Functional
Differential Equations*, Chapter 10, Section 10.3, Theorem 3.3, p. 319
([chapter DOI](https://doi.org/10.1007/978-1-4612-4342-7_11)).  In the notation
of that theorem, a (C^k) retarded vector field and a hyperbolic periodic
orbit have (C^k) local stable and unstable manifolds; the stable-manifold
codimension is the unstable index.

The source-bound hypothesis match is as follows.

| Theorem input | Registered evidence | Consequence |
|---|---|---|
| (C^1) or smoother RFDE | The vector field is polynomial in finitely many continuous point evaluations; hence it is (C^\infty) on the history space | Smooth-semiflow hypothesis matched |
| Nonconstant periodic orbit | The validated nonconstant Fourier-mode lower bound is positive | A genuine periodic orbit, not an equilibrium |
| Compact/smoothing return derivative | The validated period satisfies (T>r), and compact monodromy is registered | Compact Poincare derivative after one period |
| Simple autonomous phase multiplier | The multiplier (1) is algebraically simple | The phase direction is the only neutral direction |
| Hyperbolicity off phase | The total right-half count gives exactly one nontranslation multiplier outside the unit circle and no other multiplier on or outside it | Unstable index (i(\gamma)=1) |

It follows that the full-history local stable manifold is (C^1) and has
codimension one.  A qualitative transverse section exists because the orbit
tangent is nonzero; a bounded linear functional nonzero on that tangent gives
an affine (C^\infty) section.

For the reduced space

\[
Y=C([-r,0],\mathbb R)\times\mathbb R,
\]

the already proved map \(\pi:X\to Y\) has a continuous split right inverse,
the semiflow factors exactly through \(\pi\), and the old recovery-history
fiber contributes only zero spectrum.  Moreover
\(W_X^s=\pi^{-1}(W_Y^s)\).  In split coordinates
\(X=\iota(Y)\oplus\ker\pi\), this full stable manifold is locally saturated
along \(\ker\pi\).  Intersecting with \(\iota(Y)\), or equivalently factoring
a local defining submersion through \(\pi\), therefore yields a (C^1)
codimension-one reduced stable manifold.  Intersecting it with the centered
abstract transverse section removes the phase direction and leaves one
unstable transverse direction, so its stable sheet is again codimension one
inside that section.

This does **not** identify the abstract section with the particular pulse
section (v(0)=v_i(0)), \(\dot v_i(0)>0\).  The latter currently has only a
binary64 observed crossing speed, not a directed continuous-RFDE lower bound.

## Quantitative Lyapunov--Perron contract

On a phase-fixed section write the return map as

\[
P(x)=Lx+N(x),\qquad N(0)=DN(0)=0,
\]

with the Riesz splitting (E^s\oplus E^u).  Every norm below must be the same
declared continuous reduced-history section norm.  The next certificate must
supply

\[
\begin{aligned}
 \|L_s^n\|&\le K_s\rho_s^n, &0<\rho_s<1,\\
 \|L_u^{-n}\|&\le K_u\rho_u^n, &0<\rho_u<1,\\
 \|P_s\|&\le p_s, &\|P_u\|\le p_u,
\end{aligned}
\]

as well as a weight \(\rho_s<\beta<1\), a directed section-event speed lower
bound, section and return-map (C^2) bounds, a validated return-map ball
(R_0), and a nonlinear coefficient (C_N) satisfying on that ball

\[
\|DN(x)\|\le C_N\|x\|,\qquad
\|N(x)\|\le \tfrac12 C_N\|x\|^2.
\]

In the weighted sequence norm
\(\|x\|_\beta=\sup_{n\ge0}\beta^{-n}\|x_n\|\), the disclosed Green-kernel
majorant is

\[
C_\beta=
\frac{K_sp_s}{\beta-\rho_s}
+\frac{K_up_u\rho_u}{1-\beta\rho_u}.
\]

For a sequence ball of radius (R), the contraction and invariance tests are

\[
q(R)=C_NC_\beta R<1,
\qquad
K_s r+\frac12 C_NC_\beta R^2\le R,
\]

where (r) is the stable seed radius.  Set

\[
\Delta=1-2K_sC_NC_\beta r,
\qquad
R_{\min}=\frac{2K_sr}{1+\sqrt{\Delta}}.
\]

Within this stated scalar majorant—not as a necessary condition for the
underlying RFDE itself—there exists some (R\le R_0) satisfying both tests
if and only if

\[
2K_sC_NC_\beta r<1
\quad\text{and}\quad
R_{\min}\le R_0.
\]

The strict inequality is essential: equality gives (q=1).  The executable
contract also reports conservative graph estimates

\[
 C_h\le \frac{C_N}{2}
 \frac{K_up_u\rho_u}{1-\beta\rho_u}
 \left(\frac{K_s}{1-q}\right)^2,
\qquad
 L_h\le C_NR
 \frac{K_up_u\rho_u}{1-\beta\rho_u}
 \frac{K_s}{1-q}.
\]

## What is known and what is missing

The parent certificates already supply the unstable inverse rate

\[
\rho_u\le
0.549712198641301272665939640423769383243380071590153,
\]

derived from the directed unstable-multiplier lower bound.  They also prove
qualitatively that the stable spectral radius is below one.  They do **not**
yet supply a numerical \(\rho_s<1\), Riesz projection norms, dichotomy
constants, section-event lower bound, return (C^2) bound, nonlinear
remainder coefficient, or a validated continuous-history return ball.
Consequently the actual-evidence evaluation has no numerical (q) or
candidate radius and cannot close a graph theorem.

The result contains one complete **design row, not evidence**, to make the
next interface executable:

\[
\rho_s=0.9,\quad \rho_u=\rho_u^{\rm proved},\quad
p_s=p_u=K_s=K_u=2,\quad \beta=0.95,
\]
\[
\text{event speed}=0.01,\quad M_2=C_N=10,\quad
r=2\times10^{-4},\quad R_0=5.2\times10^{-4}.
\]

For that hypothetical row the arithmetic gives

\[
C_\beta\le84.60228372404556,
\quad R_{\min}\le5.100444495314209\times10^{-4},
\quad q\le0.431509252311320,
\]

and the strict critical budget is

\[
C_N<14.77501486930578.
\]

These numbers are a target for a future directed certificate and must never
be substituted for RFDE evidence.

## Claim boundary and next certificate

The next certificate must bind the declared norm, the stable spectral annulus
or left-shift gap, both Riesz projections, forward/backward dichotomy power
bounds, the exact phase section and event-speed enclosure, return-map (C^2)
control, the nonlinear Taylor remainder, and the continuous-history ball on
which all of them hold.  Only after those inputs close the displayed strict
gate may the quantitative local graph flag become true.

Even that graph theorem would not by itself prove the physical pulse onset.
The pulse terminal curve must additionally be enclosed in the same norm,
shown to enter the graph neighborhood, cross the graph transversely in the
specific voltage section, and route to opposite basins on its two sides.
Accordingly separator, onset, and routing remain outside Stage 1.
