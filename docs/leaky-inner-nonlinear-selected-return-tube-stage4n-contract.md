# Stage 4N: nonlinear selected-return tube and event-graph contract

Status: **OPEN NUMERICAL CONTRACT.**

Stage 4M shows that the enlarged six-block Hessian problem cannot begin with
the Hessian equations.  It first needs one nonlinear return family on the
entire anisotropic complete-history ball.  Stage 4N specifies that parent:
one common event window, a uniform positive event speed, a (C^2) moving-time
graph, a complete returned-history tube, and a proof that no earlier
admissible positive-oriented return enters the local Route-C section patch.

The executable source is
[leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py](../src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py),
the atomic generator is
[leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py](../experiments/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py),
and the source-bound result is
[leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json](../experiments/results/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json).

Stage 4N binds Stage 4M and inherits exactly

\[
 R_s=0.0097,qquad \widehat R_u=0.00025,qquad
 R_s+\widehat R_u=0.00995.
\]

It has no Stage-4L numerical parent.  A discrete linear terminal-row bound
contains neither the nonlinear base family nor the moving event and therefore
cannot fill any Stage-4N field.

## 1. Domain and local return

Let

\[
 \mathcal B=\{X_*+x_s+\widehat qx_u:
 x_s\in\ker\widehat f, \|x_s\|_Y\le0.0097,
 |x_u|\le0.00025\},
\]

where ((\widehat q,\widehat f)) is the fixed unit-(Y) pair from Stage 4M.
The stable variable ranges over arbitrary continuous histories, not a finite
node vector.

The affine event row is

\[
 g(\phi)=\phi_v(0)-X_{*,v}(0).
\]

The hyperplane (g=0) is larger than the local Poincare section.  The local
return patch is its intersection with a declared complete-history
neighborhood of (X_*), and an admissible return has positive orientation
(Dg[F(\phi)]>0).  This distinction matters: the periodic orbit may have an
earlier negative-oriented crossing of the same voltage level without making
that crossing the selected local return.

## 2. Common event window

A closing certificate must produce one interval

\[
 I_T=[T_-,T_+]
\]

valid for every (x\in\mathcal B), together with strict directed margins

\[
 \sup_{x\in\mathcal B}g(X_{T_-}(x))\le-\delta_-<0,
 \qquad
 \inf_{x\in\mathcal B}g(X_{T_+}(x))\ge\delta_+>0,
\]

and

\[
 \inf_{x\in\mathcal B,\,t\in I_T}
 Dg[F(X_t(x))]\ge a_*>0.
\]

These inequalities give exactly one selected event (T(x)\in I_T).  A mesh
of successful trajectories or endpoint values evaluated at finitely many
base points does not prove the quantified statement.

## 3. The nonlinear flow tube

The state family solves

\[
 \dot X(t;x)=F(X_t(x)),\qquad X_0(x)=x\in\mathcal B.
\]

The enclosure must be continuous in physical time and uniform over the full
infinite-dimensional ball through (T_+).  Before a delayed argument enters
the evolved part of the solution, the exact translation of the arbitrary
initial history must remain in the enclosure.  A method-of-steps proof must
cover every delay-activation face and every time/history seam.

The first missing numerical term is therefore

\[
 E_{\rm flow}^{Y}ge
 \sup_{x\in\mathcal B}\sup_{0\le t\le T_+}
 \|X_t(x)-\widehat X_t(x)\|_Y,
\]

for a declared correlated guide or radii construction.  No such bound is
presently available.  The endpoint signs, speed, event derivatives, returned
history and earlier-return exclusion all depend on this same family, so
freezing this term first prevents circular bookkeeping.

## 4. (C^2) moving-time graph

Once the common speed gate closes, the implicit-function theorem gives a
(C^2) event graph on a neighborhood of (mathcal B).  For first and second
variations (U_h,V_{hk}), it must be evaluated with one common event-speed
denominator:

\[
 T_h=-\frac{Dg[U_h(T)]}{Dg[\dot X(T)]},
\]

\[
\begin{aligned}
 W_{hk}(0)={}&V_{hk}(T)+\dot U_h(T)T_k+\dot U_k(T)T_h
                    +\ddot X(T)T_hT_k,\\
 T_{hk}={}&-\frac{Dg[W_{hk}(0)]}{Dg[\dot X(T)]}.
\end{aligned}
\]

Stage 4N must bound these derivatives uniformly.  Stage 4M will later use
them throughout the returned history when constructing the six Hessian
blocks; an endpoint-only event correction is not sufficient.

## 5. Complete returned-history tube

Define

\[
 R(x)=\left(\theta\mapsto v(T(x)+\theta;x),\ w(T(x);x)\right),
 \qquad -\tau_{\max}\le\theta\le0.
\]

A closing certificate must prove

\[
 \sup_{x\in\mathcal B}\|R(x)-X_*\|_Y\le R_{\rm return}
\]

and show that every (R(x)) lies in the declared local section patch.  The
underlying state cover must therefore include the whole physical interval
([T_--\tau_{\max},T_+]).  A bound only at (T(x)), or on finitely many
history nodes, does not control the RFDE return map.

## 6. No earlier admissible return

The desired exclusion concerns an admissible local return, not every zero of
the voltage event row.  For every (x\in\mathcal B), Stage 4N must exclude

\[
 g(X_t(x))=0,qquad Dg[F(X_t(x))]>0,qquad
 X_t(x)\in\Sigma_{\rm loc}
\]

for (0<t<T(x)).

The time cover begins with a launch collar that separates the initial
section point from later times.  It then partitions the compact middle
interval at every delay activation and candidate crossing.  On each slab it
must prove at least one of the following directed alternatives:

1. the event gap stays strictly away from zero;
2. every possible zero has nonpositive event speed;
3. every possible zero lies a positive (Y)-distance outside the local
   complete-history patch.

This disjunctive cover permits genuine negative-oriented crossings.  Requiring
one global sign of (g) over the whole period would generally be the wrong
geometric condition.  All slabs and seams must be covered continuously;
time sampling is not a substitute.

## 7. Handoff and claim boundary

Only a source-bound Stage-4N result with every displayed margin and coverage
gate closed may become the nonlinear-domain parent of Stage 4M.  It supplies
the common domain on which (D^2P(x)) can be enclosed.  It supplies no
Hessian block by itself: Stage 4M must still propagate the first/second
variations and form all six fixed projected outputs before norms.

The current result keeps null every event time, gap margin, speed, flow-tube
radius, returned-history radius, patch radius, launch collar, no-earlier-hit
margin and event-derivative bound.  It proves no selected or first return,
return map, Hessian block, stable graph, pulse/stable-sheet crossing,
biological onset, routing, capture, or network safety statement.

The generator validates the Stage-4M parent and this complete open ledger
before an fsynced atomic replacement.  Hostile tests reject finite-node
substitution, filled numerical fields, missing returned-history coverage,
promotion of a selected event to a first return, Stage-4L substitution, and
every downstream theorem promotion.
