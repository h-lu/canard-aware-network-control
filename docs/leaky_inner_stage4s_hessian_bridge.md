# Stage 4S-B: a fail-closed Hessian bridge for complete histories

Status: **proved bridge design and sampling no-go; no Banach Hessian block is
validated.**

This artifact audits the signed near-two-period finite-section calculation in
Stage 4Q and identifies the exact additional estimates needed to turn a
computed tensor into the six complete-history blocks of $D^2Q$.  It proves
several functional-analytic and arithmetic subcertificates.  It does **not**
give an outward error bar for any Stage-4Q row, a common full-ball return, a
stable graph, a crossing, or biological onset.

The executable record is
[`leaky_inner_stage4s_hessian_bridge.py`](../src/canard_control/leaky_inner_stage4s_hessian_bridge.py),
the atomic generator is
[`leaky_inner_stage4s_hessian_bridge.py`](../experiments/leaky_inner_stage4s_hessian_bridge.py),
and the source-bound result is
[`leaky_inner_stage4s_hessian_bridge.json`](../experiments/results/leaky_inner_stage4s_hessian_bridge.json).

## 1. What Stage 4Q does and does not supply

Stage 4Q correctly preserves the following algebraic order on each finite
section:

1. propagate the first and second physical variations;
2. form both event-time derivatives with one common event denominator;
3. translate every returned-history coordinate at that event time;
4. insert the fixed stable or unstable input directions;
5. apply the fixed unstable row and subtract its rank-one output; and
6. take the six finite tensor norms only after those signed combinations.

It also records the $N=120,180,240$ mesh ladder, the direct-versus-composed
two-return consistency oracle, and the corrected one-sided endpoint adapter.
These are useful diagnostics.  They do not provide any of the following:

- outward rounding of the generated tensor;
- an operator-norm discretization error on
  $C([-\tau_{\max},0])$;
- a continuous source-time or output-phase supremum;
- a directed error for the finite $q/f$ adapter;
- a common selected event on the full anisotropic ball; or
- center-to-ball Hessian inflation.

All nineteen Stage-4Q theorem flags therefore remain false.

## 2. The finite-sampling obstruction

Let $K$ be a nontrivial compact interval and
$X=C(K)$ with the supremum norm.  For any finite nodes
$t_1,\ldots,t_N$, define

\[
 S_Nh=(h(t_1),\ldots,h(t_N)).
\]

Let $R_N:\mathbb R^N\to X$ be any bounded linear reconstruction.  Choose
$t_*\notin\{t_1,\ldots,t_N\}$.  There is a continuous function $h$ with

\[
 \|h\|_\infty=1,
 \qquad h(t_j)=0,
 \qquad h(t_*)=1.
\]

Then $S_Nh=0$, so

\[
 (I-R_NS_N)h=h,
 \qquad \|I-R_NS_N\|\ge 1.                 \tag{2.1}
\]

This holds for every finite $N$.  Thus nodal interpolation cannot converge
to the identity in operator norm on the arbitrary continuous-history unit
ball.  The same blindness occurs for bilinear forms: for a unit vector $y_*$,

\[
 B_*(h,k)=h(t_*)k(t_*)y_*
\]

has norm one, while its off-grid action is not determined by the nodal data.

Equation (2.1) is the decisive audit result.  It rules out any proof that
relabels the Stage-4Q three-grid trend as a Banach-space error estimate.  There
are only two legitimate repairs:

1. work with signed atom--density measures and bimeasures in the physical
   history coordinate and bound their residual directly; or
2. change the domain to an equicontinuous or smoother history class with a
   proved common modulus of continuity.

The second route changes the present Stage-4M arbitrary-$C$ graph domain.
The first route is therefore the recommended one.

## 3. What can be lifted rigorously

Suppose a finite tensor $A=(a_{oij})$ has *directed* coefficient intervals
and its input nodes are interpreted as exact physical evaluation atoms.
Define

\[
 B_N(h,k)
 =R_{\rm out}\left(
   \left(\sum_{i,j}a_{oij}h(t_i)k(t_j)\right)_o
  \right),                                             \tag{3.1}
\]

where $R_{\rm out}$ is piecewise-linear reconstruction on an
endpoint-complete output grid.  The input sampler and $R_{\rm out}$ both
have norm one.  Hence

\[
 \|B_N\|
 \le \max_o\sum_{i,j}|a_{oij}|.                        \tag{3.2}
\]

Thus a rigorously enclosed finite tensor can be lifted to a genuine atomic
bimeasure operator on $C(K)\times C(K)$.  The tensor row-$\ell^1$ norm used
by Stage 4Q is the correct *shape* for (3.2).  The missing
step is a directed coefficient enclosure and, more importantly, a bound on
$\lVert D^2Q-B_N\rVert$.

For the continuous output phase, if a bimeasure row is Lipschitz in
$\theta$ with operator-norm constant $L_\theta$, then an
endpoint-complete mesh of width $\Delta$ gives

\[
 \sup_\theta\|B(\theta)\|
 \le \max_j\|B(\theta_j)\|+{\Delta\over2}L_\theta.     \tag{3.3}
\]

The quantity $L_\theta$ is one of the still-missing interval inputs.

## 4. Exact stencil subcertificates

Stage 4Q uses two cubic interpolation patterns.  For the interior pattern
with normalized nodes $(-1,0,1,2)$ and $x\in[0,1]$, the exact Lebesgue
constant is

\[
 \Lambda_{\rm int}={5\over4}.                          \tag{4.1}
\]

Indeed, the four weights have signs $(-,+,+,-)$ on the open cell, so
their absolute sum reduces to $1+x-x^2$ and is maximized at $x=1/2$.
If all functions lie in a common Lipschitz class with constant $L$, the
interpolation error is at most

\[
 {3\over4}\Delta L.                                   \tag{4.2}
\]

Here the signed distance-weighted sum is
$\frac43x(x-2)(x-1)(x+1)\Delta L$ and has its cell maximum at
$x=1/2$.

For the one-sided right-endpoint pattern with nodes
$(-3,-2,-1,0)$ and $x\in[-1,0]$, the weights are

\[
 -{x(x+1)(x+2)\over6},\quad
 {x(x+1)(x+3)\over2},\quad
 -{x(x+2)(x+3)\over2},\quad
 {(x+1)(x+2)(x+3)\over6}.
\]

Their exact Lebesgue constant is

\[
 \Lambda_{\rm end}={7+14\sqrt7\over27}
 =1.631130309440898\ldots,                              \tag{4.3}
\]

The weight signs are $(+,-,+,+)$, and their absolute sum is
$1-3x-4x^2-x^3$.  Its unique interior maximum occurs at
$x=(-4+\sqrt7)/3$.  The exact common-Lipschitz error constant is

\[
 {4\over3}\Delta L.                                   \tag{4.4}
\]

The corresponding distance-weighted polynomial is
$-\frac43x(x+1)(x+2)(x+3)\Delta L$, maximized at
$x=(-3+\sqrt5)/2$.

No positive-time node occurs in this endpoint stencil.  Equations
(4.1)--(4.4) rigorously prove stability and conditional approximation on a
common Lipschitz class.  They do not defeat (2.1), because the Stage-4M stable
ball contains arbitrary continuous histories and has no common Lipschitz
constant.  For a specified individual modulus $\omega_h$, the corresponding
bounds are

\[
 |h-I_{\rm int}h|\le {5\over4}\omega_h(2\Delta),
 \qquad
 |h-I_{\rm end}h|\le
 {7+14\sqrt7\over27}\omega_h(3\Delta).                 \tag{4.5}
\]

## 5. Continuous projection factors

Use the exact continuous-history unit pair

\[
 \|\widehat q\|_Y=1,
 \qquad \widehat f(\widehat q)=1,
 \qquad P_s=I-\widehat q\widehat f.
\]

Stage 4L proves on the restricted section

\[
 \|\widehat f\|\le
 21.8105001598406993275915906586\ldots,
\]

and therefore

\[
 \|P_s\|\le22.8105001598406993275915906586\ldots.      \tag{5.1}
\]

If a raw continuous Hessian approximation satisfies

\[
 \|H-\widetilde H\|_{\rm bil}\le\eta,
\]

then the six projected errors are bounded by

\[
 \begin{array}{c|cccccc}
 &s,ss&s,su&s,uu&u,ss&u,su&u,uu\\ \hline
 \text{factor}
 &\|P_s\|^3&\|P_s\|^2&\|P_s\|
 &\|\widehat f\|\|P_s\|^2
 &\|\widehat f\|\|P_s\|
 &\|\widehat f\|
 \end{array}.                                          \tag{5.2}
\]

The exact decimal factors are frozen in the JSON.  The largest is
(11868.7347517620\ldots).  This explains why the direct projected route is
essential: form the event quotient, apply (P_s) or (widehat f), retain
the signed correlations, and only then take total variation.  A raw ambient
error certificate would need to be extremely small before (5.2).

Stage 4D already proves that the continuous adjoint is an atom--density
measure with a summable Fourier tail, and Stage 4L supplies the exact
restricted normalized row used in (5.1).  Those facts solve the existence and
normalization of the output covector.  They do not yet evaluate that covector
on all six second-return bimeasures.

## 6. Per-block wide-box budgets

The following targets are independent future acceptance slots.  The
Stage-4Q column is displayed only to show scale; it is not an ingress bound.
The “usable error” column allocates $90\%$ of the gap after the core target,
and $10\%$ remains unused as strict reserve.

| block | Stage-4P cap | Stage-4Q heuristic | directed Banach core target | usable projected-error budget | strict reserve | one-raw-error ceiling from (5.2) |
|---|---:|---:|---:|---:|---:|---:|
| $C_{s,ss}$ | 1 | $2.35230\times10^{-6}$ | 0.0001 | 0.89991 | 0.09999 | $7.58219\times10^{-5}$ |
| $C_{s,su}$ | 10 | 0.00872968 | 0.02 | 8.982 | 0.998 | 0.0172625 |
| $C_{s,uu}$ | 1000 | 32.117788 | 40 | 864 | 96 | 37.8773 |
| $C_{u,ss}$ | 5 | 0.596928 | 0.75 | 3.825 | 0.425 | $3.37052\times10^{-4}$ |
| $C_{u,su}$ | 10 | 0.577596 | 0.75 | 8.325 | 0.925 | 0.0167334 |
| $C_{u,uu}$ | 1000 | 158.531779 | 180 | 738 | 82 | 33.8369 |

For each block, the usable $90\%$ is split into final *projected-block*
contributions as follows:

| contribution | fraction of cap minus core target |
|---|---:|
| base orbit and coefficient error | 0.10 |
| first-variation signed-kernel residual | 0.15 |
| second-variation signed-bimeasure residual | 0.20 |
| event quotient and complete-history translation | 0.15 |
| continuous (q/f) action and output-phase completion | 0.10 |
| full-ball inflation and return-domain error | 0.20 |
| unused strict reserve | 0.10 |

Every exact per-block decimal allocation is stored in the result.  If one
instead spends all six usable slots on a single raw Hessian remainder before
projection, (5.2) gives the simultaneous ceiling

\[
 \eta_{\rm raw}<7.5821898359165\times10^{-5}.           \tag{6.1}
\]

Equation (6.1) is only a fallback design.  A signed projected residual should
use the much larger individual budgets in the table.

## 7. Required interval certificate

A strict computation must supply all of the following in one source-bound
coordinate system.

### A. Full-ball domain and event

- a common solution tube through $T_{2,+}$;
- $T_{2,-}>2\tau_{\max}$;
- strict endpoint event signs and a common $a_* >0$;
- returned split-ball and graph-domain containment.

### B. Base history and field jets

- $X,\dot X,\ddot X$ on all source and output cells;
- $D F,D^2F,D^3F$ in every current and delayed slot;
- every delay activation face, short cell, and seam.

### C. First-variation signed measures

- the initial translation atoms at their physical history locations;
- stable-input and $\widehat q$-input rows at every intermediate time;
- measure residual integrals, initial trace errors, and seam jumps.

### D. Second-variation signed bimeasures

- the $(ss,su,uu)$ source bimeasures;
- the retarded terminal response for every output phase;
- residual integrals, symmetry, seams, outward quadrature, and rounding.

### E. Event quotient and history translation

- one correlated positive denominator, including inverse powers through
  $a_*^{-3}$;
- $n_s,n_u,\dot U,\ddot X,T_h,T_k,T_{hk}$ without independent norming;
- all translated history coordinates followed by exactly one phase
  projection.

### F. Continuous (q/f) and output phase

- the exact complete-history $\widehat q$ and atom--density
  $\widehat f$, their pairing and tails;
- the action of that same row on each correlated output bimeasure;
- a continuous $\theta$-supremum such as (3.3), including both endpoints.

### G. Center-to-ball inflation

- changes in coefficients, first kernels, second kernels, event time, and
  denominator on the full split ball;
- the resulting uniform projected remainder for every block.

Every numerical field corresponding to A--G is `null` in the current result.

## 8. Fail-closed decision

Stage 4Q cannot be promoted by mesh trends, by its direct-versus-composed
oracle, or by the fact that all six diagnostic values are far below the wide
box.  The active route is a two-period physical-coordinate
atom--density-bimeasure residual, carrying event and $q/f$ correlations
through to the six final rows.  The existing arithmetic leaves large room for
such a certificate, but Stage 4S-B proves only that route and its exact
budgets—not the missing estimates.

Reproduce with:

```bash
PYTHONPATH=src /usr/bin/python3 \
  experiments/leaky_inner_stage4s_hessian_bridge.py
```
