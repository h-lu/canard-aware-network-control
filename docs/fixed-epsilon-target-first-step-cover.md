# The first method-of-steps cover of the target C4 chart

Status: **rigorous computer-assisted cover of the complete first method-of-steps rectangle**

\[
   P_1=[-3,1]\times[-1/20,1/20].
\]

At the frozen target anchor, the calculation encloses the physical state and
its true label derivative on all of $P_1$.  It proves there the three strict
P-matrix inequalities in the fixed output frame

\[
 L_P=\begin{pmatrix}-7&2\\3&1\end{pmatrix},\qquad \det L_P=-13.
\]

The proof consists of 400 time cells and 20 label cells, hence 8,000
time--label rectangles.  It uses directed MPFR rounding, exact polynomial
evaluation of the delayed C4 patch, Bernstein range bounds, strict Picard
inclusions, and a separate same-kernel 256-bit precision replay.  Binary64
RK4 values choose
the centers of local cubic predictors, but no binary64 state, sample, or sign
is used as an enclosure or as evidence for a margin.

This is not yet the full physical strip $[-3,3]$.  In particular it does not
cover the second method-of-steps interval $(1,3]$, the late cross-separation
condition through $t=3$, or an enlarged label collar.  Therefore it does
not by itself prove the glued global embedding, a target graph, or a
complete-history canard root.

## 1. Exact delayed forcing on the first step

The active delays are four and five.  If $-3\le t\le1$, then

\[
 t-5\in[-8,-4],\qquad t-4\in[-7,-3].
\]

The delay-five slot therefore remains in the affine far history.  The
delay-four slot is affine for $t\le1/2$, whereas for $1/2\le t\le1$ it
traverses exactly the compact C4 patch $[-3.5,-3]$.  Thus no value from a
previously integrated physical segment is needed on $P_1$.

Let $r=t-1\in[-1/2,0]$, $u=1+2r$, and

\[
 \chi_9(u)=126u^5-420u^6+540u^7-315u^8+70u^9,
 \qquad
 \phi_j(r)=\frac{r^j}{j!}\chi_9(1+2r).
\]

If $a_j^X(\lambda)$ denotes the exact recursively compatible endpoint jet
and $b_j^X(\lambda)$ the unpatched endpoint jet, then the patched delayed
coordinate is

\[
 X_4(t,\lambda)
 =-\frac{t-4+q}{2}
  +\sum_{j=1}^4
     \bigl(a_j^X(\lambda)-b_j^X(\lambda)\bigr)\phi_j(t-1).
\]

Every coefficient is evaluated over
$\mathbb Q(\sqrt5)[\lambda]$ before conversion to outward MPFR intervals.
The first two label derivatives are obtained by exact differentiation of
these polynomials.  A fourteen-defect symbolic audit verifies the four patch
coefficients, ties both state equations to the authoritative RFDE slot
algebra, checks the first and second variational equations and the cubic
Hermite endpoint identities, and confirms $\det L_P=-13$; every defect is
identically zero.

## 2. Why the second label variation is included

A direct interval propagation of the whole label cell repeatedly boxes a
rotating first-variation vector and eventually loses the determinant sign.
The proof instead fixes the binary64 label center $\lambda_c$ of each exact
decimal label cell and validates three objects:

\[
 z_c(t)=z(t,\lambda_c),\qquad
 v_c(t)=\partial_\lambda z(t,\lambda_c),\qquad
 w(t,\lambda)=\partial_{\lambda\lambda}z(t,\lambda).
\]

The full first-variation and state families then follow from the ordinary
mean-value theorem:

\[
\begin{aligned}
 \partial_\lambda z(t,\Lambda)
 &\subset v_c(t)+(\Lambda-\lambda_c)w(t,\Lambda),\\
 z(t,\Lambda)
 &\subset z_c(t)+(\Lambda-\lambda_c)
                    \partial_\lambda z(t,\Lambda).
\end{aligned}
\]

This is an enclosure identity, not a sampled finite-difference
approximation.  The second variational equation is differentiated exactly.
Writing $F$ for the fast field, its nonzero second derivatives are

\[
 F_{XX}=-2-2\rho X-\frac32\rho^3X,
 \qquad
 F_{X_jX_j}=\frac34\rho^3X_j,\qquad j\in\{4,5\}.
\]

Consequently

\[
 w_X'=F_Xw_X+w_Y+F_{XX}v_X^2
       +\sum_{j=4,5}\bigl(F_{X_j}w_{X_j}
                          +F_{X_jX_j}v_{X_j}^2\bigr),
 \qquad w_Y'=-w_X.
\]

The state, central first variation, and full-label second variation each
satisfy a separate strict Picard inclusion on every time cell.  The two
mean-value enclosures couple them without repeatedly replacing the whole
parameterized state family by an axis-aligned propagated box.

Formally, the continuation uses the maximal-interval argument for a smooth
parameter-dependent polynomial ODE.  On the common local existence interval,
differentiation in the label and the two mean-value identities are valid.  If
a state or variation were the first object to leave its asserted tube, the
corresponding strict Picard inclusion and mean-value enclosure would place it
in the interior instead.  The compact enclosures also rule out finite-time
escape, so the family extends across the cell.  Induction over the 400 cells
gives the claimed common interval; the mean-value identities are not assumed
beyond an already existing solution family.

## 3. Polynomial defect and Bernstein enclosure

On one time cell write $t=t_i+h\sigma$, $0\le\sigma\le1$, with
$h=10^{-2}$.  A binary64 RK4 trace supplies only two guide endpoints.  The
cubic Hermite polynomial $p_i(\sigma)$ is formed from those endpoints and
outward interval evaluations of the exact vector field at them.  Its
endpoint value and derivative identities are exact.

All current and delayed terms on the first method step are polynomials in
$\sigma$.  The residual

\[
 R_i(\sigma,E)=f(t_i+h\sigma,p_i(\sigma)+E)
                  -\frac1h\partial_\sigma p_i(\sigma)
\]

is therefore an interval-coefficient polynomial.  If
$R_i=\sum_{j=0}^n a_j\sigma^j$, the exact conversion

\[
 b_k=\sum_{j=0}^k
       \frac{\binom{k}{j}}{\binom{n}{j}}a_j,
       \qquad 0\le k\le n,
\]

puts it in the Bernstein basis.  The convex hull of the outward interval
coefficients $b_k$ encloses $R_i([0,1],E)$.  Hence the strict inclusion

\[
 e_i+[0,h]R_i([0,1],E)\subset\operatorname{int}E

\]

proves the complete continuous-time tube on that cell, while

\[
 e_{i+1}\in e_i+hR_i([0,1],E)

\]

provides its outward endpoint enclosure.  This integral residual is the
local truncation bound; rectangular dependency is retained explicitly as
wrapping.  The argument is applied successively to $z_c$, $v_c$, and
$w(\Lambda)$.

## 4. Certified inequalities and scope

For each cell the reconstructed state family gives $z_t=f(t,z,\lambda)$,
and the reconstructed first-variation family gives $z_\lambda$.  Bernstein
ranges then verify

\[
 (-7,2)z_t>0,\qquad
 (3,1)z_\lambda>0,\qquad
 -13\det(z_t,z_\lambda)>0

\]

on every one of the 8,000 rectangles.  The stored result contains outward
global lower bounds for these three quantities, an outward upper bound for
the raw negative determinant, the smallest Picard gaps, the largest error
radii, and a SHA-256 digest of the three tube polynomials, propagated
endpoints, and four sign intervals on every proof cell.  It also proves
$X_t<0$ on the early part
$[-3,-2]\times[-1/20,1/20]$, closing the first of the two scalar
cross-separation inequalities on its required domain.

The exact status is therefore:

| Statement | Status |
|---|---|
| C4 incoming-history P-matrix rectangle | proved independently by exact Bernstein coefficients |
| Physical P-matrix cover on $[-3,1]\times[-1/20,1/20]$ | **proved here** |
| Early inequality $X_t<0$ on $[-3,-2]\times[-1/20,1/20]$ | **proved here** |
| Physical cover on $(1,3]$ | open |
| Late entry-gap inequality on $[-2,3]$ | open |
| Enlarged label collar and glued global embedding | open |
| Target graph and complete-history root | open |

## 5. Reproduction

Run

```text
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_first_step_cover.py
```

The generator performs the 192-bit cover and a separate same-kernel 256-bit
precision replay, checks all exact identities and strict signs, records the
local source hashes, and writes the result JSON.  On the reference workstation
the calculation is CPU-bound and takes several minutes; it does not use a GPU
or an external interval solver.
