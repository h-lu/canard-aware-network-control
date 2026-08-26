# Leaky periodic response in the physical control coordinates

The validated inner and outer periodic orbits belong to the autonomous
leaky-recovery RFDE

$$
\begin{aligned}
v'={}&v-\frac{v^3}{3}-w
 +\varepsilon\kappa _1\left(\frac{v_{\tau _0}+v_{\tau _1}}2-v\right)\\
&+\varepsilon\kappa _3\left(
 \frac{(v_{\tau _0}-1)^3+(v_{\tau _1}-1)^3}{2}-(v-1)^3
 \right),\\
w'={}&\varepsilon(v-a-w).
\end{aligned}
$$

The relevant controls are therefore $(a,\kappa _3)$, not the
$(\kappa _1,\kappa _3)$ coordinates used by the older non-leaky parameter
box.  This is a mathematical change rather than a relabeling: the first
parameter column is supported in the slow row.

## Bordered first variations

Write the phase-fixed periodic residual as

$$
\mathcal F(v,w,T;a,\kappa _3)=0
$$

and let $J=D_{(v,w,T)}\mathcal F$ at a finite Fourier-collocation orbit.
With

$$
C(v)=\frac{(v_{\tau _0}-1)^3+(v_{\tau _1}-1)^3}{2}-(v-1)^3,
$$

the two columns are

$$
\mathcal F_a=(0,T\varepsilon\mathbf 1,0),\qquad
\mathcal F_{\kappa _3}=(-T\varepsilon C(v),0,0).
$$

Consequently the finite first variations solve

$$
Jx_a=(0,-T\varepsilon\mathbf 1,0),\qquad
Jx_{\kappa _3}=(T\varepsilon C(v),0,0).
$$

These signs are independently checked against centered differences.  If the
voltage maximum and minimum are simple, then for
$F=T^{-1}$ and $A=v_{\max}-v_{\min}$,

$$
F_q=-\frac{T_q}{T^2},\qquad
A_q=v_q(\phi_{\max})-v_q(\phi_{\min}).
$$

No extremum-location term remains because $v_\phi$ vanishes at both extrema.

## Replayed numerical result

The source-bound artifact recomputes the bordered forward solves and an
independent adjoint contraction.  At the center
$(a,\kappa _3)=(1/4,1/200)$ it gives approximately

$$
D_{(a,\kappa _3)}(F,A)_{\rm inner}=
\begin{pmatrix}
-0.9505401&-0.00655107\\
47.6087&0.569149
\end{pmatrix},
\qquad \det\approx-0.229111,
$$

and

$$
D_{(a,\kappa _3)}(F,A)_{\rm outer}=
\begin{pmatrix}
-0.369988&-0.293633\\
-9.06410&-10.2051
\end{pmatrix},
\qquad \det\approx1.11424.
$$

For the inner orbit, 129-, 193-, and 257-node calculations are compared.
For the outer orbit, the independently stored 257- and 385-node parent
polynomials are compared.  A five-level centered-difference ladder checks the
analytic columns.  Finally, both branches are solved at the same $3\times3$
sample of the box

$$
|a-1/4|\le10^{-4},\qquad
|\kappa _3-1/200|\le10^{-4}.
$$

All sampled orbits have two simple voltage extrema, and every sampled
response determinant retains its branch-specific sign.  The artifact reports
the minimum sampled absolute determinant and subtracts the observed
determinant discrepancies from resolution and centered-difference checks to
form an explicit positive *numerical* margin.

## A strict common box for the orbits and extrema

There is also a much smaller, genuinely directed common box

$$
|a-1/4|\le10^{-10},\qquad
|\kappa _3-1/200|\le10^{-10}.
$$

Here the calculation does not sample the parameter rectangle.  It inserts
interval $a$ and $\kappa _3$ directly into the leaky residual and bordered
derivative and repeats the finite/tail radii argument.  The slow residual is
$D w-T\varepsilon(v-a-w)$ and its period column is
$-\varepsilon(v-a-w)$ throughout; the old non-leaky row is never used.

For each branch, the resulting negative radii polynomial proves a unique
phase-fixed periodic orbit in the declared Wiener ball and a uniformly
invertible bordered derivative for every parameter in the box.  A directed
phase partition then proves that the voltage derivative has exactly two
zeros: one lies in a window of strictly negative curvature and one in a
disjoint window of strictly positive curvature, while every complementary
cell is bounded away from zero.  The window rule
$\max\{3,\lfloor N/8192\rfloor\}$ is the same for both branches; it is not a
branch-specific hand-selected index list.  The two validated orbit balls are
also disjoint already in their period coordinate: their center periods are
approximately $18.1862$ and $26.6044$, whereas each period correction is at
most $10^{-5}$.  The tracked result records, separately for the two branches,
the directed residual bound $Y$, finite/tail defect $Z_0$, contraction $q$,
radii margin, derivative-error bound, curvature bounds, and the complementary
derivative gap.

## Exact claim boundary

The parameter-column formulas are exact algebraic identities.  The parent
existence of the two center RFDE orbits is rigorous.  The $10^{-10}$ common
box additionally gives rigorous uniform orbit, bordered-inverse, and
simple-extrema statements.  The response matrices, the $10^{-4}$ sampled
box, and their determinant margins remain source-bound binary64 diagnostics.
In particular, the artifact does **not** yet prove any of the following:

- an enclosure of the exact RFDE orbit sensitivities;
- a nonzero lower bound for the exact response determinant throughout a
  parameter box;
- a local frequency--amplitude inverse theorem.

The next proof gate is therefore not orbit continuation or extrema
persistence: those are closed on the $10^{-10}$ box.  It is a directed error
bound for the two first sensitivities, followed by a determinant lower bound.
A quantitative target ball additionally needs a Lipschitz bound for the
response derivative (equivalently, controlled second sensitivities).

The manifest binds the mixed arithmetic used here: binary64 for the response
diagnostics and 160-bit MPFR-directed endpoints for the uniform orbit and
extrema statements.  In particular, the recorded gmpy2 runtime is part of the
strict replay environment.
