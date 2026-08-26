# Stage 5G contract: centered endpoint gaps and one selected-event crossing

Status: **THEOREM DESIGN / OPEN numerical certificate.**  Stage 5F proves a
conditional derivative bridge.  Stage 5G must add the missing graph-domain
containment and endpoint signs in exactly the same coordinates.  Only then
may the selected late-window Route-C event be said to intersect the inner
stable sheet exactly once.  This contract does not identify that event as the
ordinal third crossing and does not prove biological onset or basin routing.

## 1. Frozen coordinate interface

Use the Stage-5F objects without renormalization:

\[
 Y=C([-\tau_{\max},0],\mathbb R)\times\mathbb R,
 \qquad
 \|(\phi,w)\|_Y=\max\{\|\phi\|_\infty,|w|\},
\]

\[
 \Sigma=\{y\in Y:y_v(0)=0\},\qquad
 f=f_{\rm phys},\qquad q=q_{\rm phys},\qquad
 f(q)=1,\qquad P_s=I-qf.
\]

The pulse interval and normalized parameter are

\[
 J_0=\frac{2409}{8000},\qquad h=\frac{3}{40000},\qquad
 I_J=\left[\frac{6021}{20000},\frac{753}{2500}\right],
 \qquad J=J_0+h\xi,\quad\xi\in[-1,1].                 \tag{1.1}
\]

Let $K(J)$ be the Stage-5C selected late-window event-aligned Route-C
history, and let $X_*$ be the exact inner periodic-orbit history at the
same section phase.  Define

\[
 \kappa(J)=K(J)-X_*\in\Sigma,
 \qquad
 H(J):=f(\kappa(J))-\psi(P_s\kappa(J)).               \tag{1.2}
\]

The Stage-5C/5D ingress must certify that $J\mapsto K(J)$ is one continuous
$C^1$ event branch throughout $I_J$: Stage 5C supplies the unique selected-
window event and Stage 5D supplies its continuous $Y$-valued derivative.
There is no switching inside that window.  Consequently $\kappa$ is $C^1$;
once (3.3) holds and $\psi$ is $C^1$, the scalar gap $H$ is continuous and
$C^1$.  Continuity is the premise used by the intermediate value theorem,
while the $C^1$ branch identity is the premise used by Stage 5F.

The quantitative graph certificate must define the local stable sheet by
$H=0$ in this registered chart.  Saying that the ambient chart contains
$\kappa(I_J)$ is not the same as saying that the pulse curve lies on the
stable sheet.

There is, however, no separate nonlinear coordinate-chart obstruction on
the affine Route-C section.  The fixed splitting gives the global bounded
linear isomorphism

\[
 \mathcal C:\Sigma\longrightarrow(P_s\Sigma)\times\mathbb R,
 \qquad \mathcal C(\kappa)=(P_s\kappa,f(\kappa)),
 \qquad \mathcal C^{-1}(z,u)=z+qu.                   \tag{1.3}
\]

Thus the crossing theorem needs a numerical domain check only for the stable
coordinate $P_s\kappa(I_J)$.  The endpoint unstable coordinates, which are
of order $10^{-2}$, need not lie in the much smaller internal unstable
sequence radius used to construct the graph.  At a root of $H$, the identity
$u=\psi(z)$ automatically places the pulse history on the local graph.

## 2. Directed endpoint functional coordinates

For $\sigma\in\{-,+\}$, put

\[
 J_-=\frac{6021}{20000},\qquad
 J_+=\frac{753}{2500},\qquad
 \kappa_\sigma=K(J_\sigma)-X_*.
\]

The endpoint certificate must evaluate the complete event history, not a
terminal state or finite mesh.  It must retain the Stage-5C event-time
remainder, the full voltage history, the current recovery coordinate, the
inner-orbit enclosure, and the common Stage-4D/4E atom--density row.

Choose a real residual center $c_\sigma$ and form

\[
 r_\sigma=\kappa_\sigma-c_\sigma q                 \tag{2.1}
\]

before applying an absolute value or separating numerator and denominator.
With the same complex row $\ell$ in both terms, prove

\[
 |\ell(r_\sigma)|\le R_\sigma,
 \qquad |\ell(q)|\ge b_->0.                           \tag{2.2}
\]

Reality of the simple real eigendirection and the Stage-5E physical phase
then give the rigorous scalar interval

\[
 f(\kappa_\sigma)
 \in F_\sigma:=
 \left[c_\sigma-\frac{R_\sigma}{b_-},
       c_\sigma+\frac{R_\sigma}{b_-}\right].          \tag{2.3}
\]

The direct and omitted density dictionaries, Neumann tail, orbit/root/period
errors, event translation, delay seams, and directed-rounding guard must stay
in one correlated ledger.  A finite-section left vector or the modulus bound

\[
 |f(\kappa_\sigma)|\le C
\]

cannot prove an endpoint sign.

## 3. Stable-coordinate and graph-domain containment

The same endpoint computation should retain a complete-history residual
norm $\|r_\sigma\|_Y\le E_\sigma$.  Identity

\[
 P_s\kappa_\sigma
 =r_\sigma+q\bigl(c_\sigma-f(\kappa_\sigma)\bigr)     \tag{3.1}
\]

gives

\[
 \|P_s\kappa_\sigma\|_Y
 \le E_\sigma+\|q\|_Y
       \sup|c_\sigma-F_\sigma|.                       \tag{3.2}
\]

Endpoint bounds alone are insufficient.  On every parameter shard, Stage 5G
must prove

\[
 P_s\kappa(J)\in\operatorname{dom}\psi,               \tag{3.3}
\]

where the graph certificate exposes an explicit stable-coordinate radius and
(3.3) uses the continuous $Y$ norm.  The affine isomorphism (1.3) supplies
the ambient coordinates; it does not supply (3.3).  A sampled mesh distance,
or an inference from the two endpoint norms, is only a diagnostic.

## 4. The graph-height gate

The future quantitative graph should provide

\[
 \psi(0)=0,\qquad D\psi(0)=0,
 \qquad
 \sup_{z\in\operatorname{dom}\psi}\|D\psi(z)\|\le16. \tag{4.1}
\]

For endpoint signs, the global Lipschitz estimate in (4.1) may be too coarse.
The certificate must also give either direct endpoint height bounds

\[
 |\psi(P_s\kappa_\sigma)|\le\eta_\sigma,              \tag{4.2}
\]

or a derivative-Lipschitz constant $C_\psi$ implying

\[
 |\psi(z)|\le\frac12 C_\psi\|z\|_Y^2.                \tag{4.3}
\]

Route (4.3) additionally requires proof that the complete segment
$\{tz:0\le t\le1\}$ is contained in $\operatorname{dom}\psi$ for each
endpoint stable coordinate.  A sufficient registered choice is a convex or
star-shaped $Y$-ball centered at zero.  Endpoint membership alone does not
justify integrating $D\psi$ along that segment.

The six-block Lyapunov--Perron majorant may instead supply a direct uniform
graph-height bound.  Whatever route is used must be byte-bound to the same
$(q,f,P_s,\Sigma,Y)$ normalization as Stage 5F.

The existing six-block pilot uses instead the unit-$Y$ unstable direction
$\widehat q=q/\alpha$, where $\alpha=\|q\|_Y$, and its dual coordinate
$\widehat f=\alpha f$.  Since $P_s=I-qf=I-\widehat q\widehat f$, a future
adapter may reuse those blocks only after the directed conversions

\[
\begin{array}{lll}
C_s^{ss}=\widehat C_s^{ss},&
C_s^{su}=\alpha\widehat C_s^{su},&
C_s^{uu}=\alpha^2\widehat C_s^{uu},\\
C_u^{ss}=\widehat C_u^{ss}/\alpha,&
C_u^{su}=\widehat C_u^{su},&
C_u^{uu}=\alpha\widehat C_u^{uu}.
\end{array}                                             \tag{4.4}
\]

The physical-coordinate graph height and derivative are the corresponding
unit-coordinate quantities divided by $\alpha$, and return-ball containment
is $R_s+\alpha\widehat R_u\le R_{\rm ret}$.  Both a positive directed lower
bound and an upper bound for $\alpha$ are required.  A change of normalization
without (4.4) is not admissible, even though the present numerical margins are
large.

## 5. Endpoint signs and uniqueness

Stage 5E fixes the orientation so that the functional action is negative.
The desired endpoint inequalities are therefore

\[
 \inf F_- -\eta_->0,
 \qquad
 \sup F_+ +\eta_+<0.                                  \tag{5.1}
\]

They imply

\[
 H(J_-)>0>H(J_+).                                      \tag{5.2}
\]

Stage 5F has already proved the following conditional implication on the
whole interval: if (3.3) and (4.1) hold in the registered normalization, then

\[
 H'(J)\in
 [-494.3877706434458168\ldots,
   -9.6122293565541831\ldots]
 \subset(-\infty,0).                                  \tag{5.3}
\]

Consequently (3.3), (4.1), and (5.1) prove that there is exactly one

\[
 J_c^{\rm sel}\in I_J
 \quad\text{with}\quad H(J_c^{\rm sel})=0.            \tag{5.4}
\]

The superscript “sel” is mandatory until the selected event is proved to be
the physically intended ordinal crossing.  Endpoint signs plus strict
monotonicity already prove existence and uniqueness; interval Newton is an
optional sharpening for a smaller registered enclosure of $J_c^{\rm sel}$,
not a substitute for missing graph or chart premises.

## 6. Required result fields and hostile tests

The endpoint arithmetic may be released first as a Stage-5G-a parent.  That
artifact may prove the two complete-history functional intervals, their
opposite signs, and endpoint bounds for $\|P_s\kappa_\sigma\|_Y$.  It must
not call those functional signs stable-gap signs and must keep graph,
full-interval containment, crossing, onset and routing flags false.

A Stage-5G artifact may set the selected-event stable-sheet crossing flag to
true only if it contains all of the following:

- exact hashes and normal validation of
  `experiments/results/leaky_inner_stable_projection_stage3.json` (the
  Route-C Grushin eigencolumn), Stages 4D, 4E, 5C, 5D, 5E, and 5F, plus the future
  quantitative graph parent;
- exact definitions of $Y,\Sigma,K,X_*,\kappa,q,f,P_s,\psi,H,I_J$;
- two source-bound endpoint residuals (2.1)--(2.3), formed before norms;
- the one-branch $C^1$ event statement, with no selected-window switching;
- full-interval stable graph-domain containment (3.3), obtained on parameter
  shards rather than inferred from the endpoints;
- graph derivative bound at most 16 and endpoint height bounds (4.2) or
  (4.3);
- strict directed endpoint margins in (5.1);
- import and validation of the Stage-5F derivative interval, without
  recomputing it in a different normalization;
- exact top-level and nested schemas, canonical certificate digest, current
  runtime equality, validate-before-write atomic generation, cleared caches,
  and a fresh independent replay.

Hostile tests must refresh the canonical digest after coordinated mutations
and still reject each of the following: uncentered $K$, a finite left row,
changed scaling of $q$, a different norm, omitted inner-orbit uncertainty,
separate numerator/denominator rows, endpoint modulus substituted for sign,
one endpoint only, sampled or endpoint-only graph-domain containment, graph membership substituted
for graph-domain containment, $L_\psi>16$, omitted graph height, selected
event switching, a quadratic height bound used without star-shaped domain
containment, selected event promoted to ordinal third, or selected crossing
promoted to routed onset.

## 7. Exact claim boundary and numerical feasibility

The current 192-bit endpoint pilot, after the exact event-time remainder and
the common atom--density row are retained, reports diagnostic functional
intervals

\[
 F_-\subset[0.01967718,0.02305590],\qquad
 F_+\subset[-0.01816450,-0.01478366].                 \tag{7.1}
\]

It also reports diagnostic endpoint stable-coordinate norms below
$0.008936$.  The six-block graph pilot, after a conservative normalization
conversion, still suggests a graph height far below $10^{-3}$.  None of
these pilot values is proof evidence until the endpoint artifact,
normalization adapter, graph and full-interval containment are source-bound
and independently replayed.

The endpoint norms plus the Stage-5F derivative bound do not prove the
full-interval domain gate.  Their sharp two-sided Lipschitz cone gives only
the diagnostic upper bound

\[
 \sup_{J\in I_J}\|P_s\kappa(J)\|_Y
 \lesssim0.0100364,                                   \tag{7.2}
\]

which is larger than the proposed $R_s=0.0095$.  Stage 5G must therefore
use a parameter-sharded complete-history enclosure or enlarge the graph and
return domain.

If all Stage-5G gates close, the following single statement becomes
**PROVED**: the Stage-5C selected late-window event history intersects the
quantitative inner stable sheet exactly once on $I_J$.  The following remain
**OPEN**:

- identification with the ordinal third post-release crossing;
- signed local exit from the stable-sheet cylinder;
- attachment of the two exit faces to the quiet and outer basins;
- equivalence between $J_c^{\rm sel}$ and biological pulse onset;
- asynchronous network routing and a frequency--amplitude--safety radius.
