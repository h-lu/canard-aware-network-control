# Stage 4P: fail-closed graph-closure arithmetic

**Status:** source-bound arithmetic/design artifact, not a stable-graph theorem.

Stage 4P binds the frozen Stage 4K, final Stage 4L, Stage 4M, Stage 4N
feasibility, Stage 5G-a, and Stage 5G-b results.  It answers three narrower questions:

1. what the exact six-block Lyapunov--Perron inequalities permit on the
   preferred-B box;
2. how a near-two-period selected map changes those budgets; and
3. which parts of Stage 4N's scalar \(K_{\rm ret}\) route are sufficient,
   necessary, or independent.

Every actual one-return \(D^2P\) and two-return \(D^2(P^2)\) block remains
null in strict ingress.  Numerical rows below are acceptance designs only.

## Frozen inputs and geometry

The preferred-B split box is

\[
 r=0.0094,\qquad R_s=0.0097,\qquad R_u=0.00025,
 \qquad R_s+R_u=0.00995,\qquad \beta=0.9999.
\]

Stage 5G-b proves the selected-pulse stable-coordinate cone lies in the
closed ball of radius \(47/5000=0.0094\).  Stage 4L proves, for the selected
phase-fixed linear return only,

\[
 K_s=1,\qquad
 \rho_s\le 0.0098964274816100002225<0.1.
\]

The inherited one-return unstable backward rate is
\(\rho_u\le0.549712198641302\), with \(K_u=1\).

## Exact feasible region

For output \(i\in\{s,u\}\), define

\[
 L_{i,s}=C_{i,ss}R_s+C_{i,su}R_u,
 \qquad
 L_{i,u}=C_{i,su}R_s+C_{i,uu}R_u,
\]

\[
 Q_i={1\over2}C_{i,ss}R_s^2+C_{i,su}R_sR_u
      +{1\over2}C_{i,uu}R_u^2,
\]

and

\[
 a_s={K_s\over\beta-\rho_s},\qquad
 a_u={K_u\rho_u\over1-\beta\rho_u},\qquad
 M=\operatorname{diag}(a_s,a_u)L.
\]

The exact gates replayed by Stage 4P are

\[
 m_{ss}<1,\quad m_{uu}<1,\quad \det(I-M)>0,
\]

\[
 K_s r+a_sQ_s\le R_s,qquad a_uQ_u\le R_u,
\qquad R_s+R_u\le R_{\rm return}.
\]

There is no componentwise-largest six-cap vector: increasing one block uses
budget needed by the others.  Consequently, the following axis frontiers set
the other five blocks to zero and **must not be mixed**.

| block | one-return graph axis | one-return graph + optional \(K_{\rm ret}\) axis | two-return graph axis | two-return graph + optional \(K_{{\rm ret},2}\) axis |
|---|---:|---:|---:|---:|
| \(C_{s,ss}\) | 6.3131 | 6.3131 | 6.3124 | 6.3124 |
| \(C_{s,su}\) | 122.4746 | 122.4746 | 122.4618 | 122.4618 |
| \(C_{s,uu}\) | 9504.03 | 188.9122 | 9503.04 | 178.6322 |
| \(C_{u,ss}\) | 4.3534 | 4.3534 | 12.2720 | 12.2720 |
| \(C_{u,su}\) | 84.4570 | 84.4570 | 238.0770 | 178.6322 |
| \(C_{u,uu}\) | 3276.93 | 188.9122 | 9237.39 | 178.6322 |

The graph-only bottleneck in a common proportional row is the unstable
self-map.  Within the reference shape, \(C_{u,ss}\) supplies the dominant
term because it carries the \(R_s^2/2\) weight.  The scalar return-tube
reconstruction has a different bottleneck: the \(uu\) pair sum.

## One-return joint row

Scaling the Stage-4A ratios by 5.532 gives a deliberately non-evidentiary,
simultaneously admissible row.  Exact replay gives

| quantity | certified arithmetic value |
|---|---:|
| Perron upper | 0.0675565 |
| stable self-map slack lower | 0.0002915029 |
| unstable self-map slack lower | 0.0001455074 |
| graph height upper | 0.000104480 |
| graph derivative upper | 0.0212975 |
| reconstructed pair-sum \(K_{\rm ret}\) | 188.882990 |
| Stage-4N conditional target lower | 188.9122238810816 |

Thus the arithmetic closes, including the optional pair-sum route, but no
row member is yet a directed continuous-history Hessian bound.

## Two-return route

For a near-two-period selected map, the conditional linear design uses

\[
 \rho_{s,2}\le0.1^2=0.01,
 \qquad \rho_{u,2}\le(0.549712198641302)^2.
\]

This squaring is valid only after the exact invariant splitting and
intertwining are transferred to the two-return map.  The second derivative is
not obtained by squaring one-return caps:

\[
 D^2(P^2)(x)[h,k]
 =D^2P(Px)[DP(x)h,DP(x)k]+DP(Px)D^2P(x)[h,k].
\]

A new source-bound correlated enclosure of this whole expression is required.
The independently reported \(N=180\) finite-section pilot is approximately

\[
(4.27\!\times\!10^{-8},5.20\!\times\!10^{-7},30.2781,
 0.59394,0.56667,158.5393).
\]

Stage 4P replays the conservative envelope
\((10^{-6},10^{-5},35,0.7,0.7,180)\), and also the recommended wide target
box \((1,10,1000,5,10,1000)\):

| two-return row | Perron upper | stable slack lower | unstable slack lower | height upper | \(\|D\psi\|\) upper |
|---|---:|---:|---:|---:|---:|
| conservative pilot envelope | 0.023558 | 0.000298895 | 0.000232569 | 0.000017431 | 0.003086 |
| recommended wide proof box | 0.193086 | 0.000196409 | 0.000124109 | 0.000125886 | 0.026559 |

Both rows close comfortably.  The wide box is the recommended target for a
future source-bound \(D^2(P^2)\) computation.  Its derivative arithmetic is
far below the conditional Stage-5G-b threshold 16; this does not prove a
graph, either endpoint stable-gap sign, or a crossing.

### Conditional downstream crossing arithmetic

**Normalization warning:** the wide-box values
\(H_{\widehat\psi}\le0.0001258851\) and
\(\|D\widehat\psi\|\le0.0265586\) are in the unit-\(q\) coordinate.  Stage
5G-a's endpoint functionals are in the physical \(q_{\rm phys}\) coordinate.
Comparing those numbers directly is forbidden.  With the transitive Stage-4E
bound

\[
 \alpha=\|q_{\rm phys}\|_Y
 \ge0.07755431589814009,
 \qquad
 \psi_{\rm phys}=\widehat\psi/\alpha,
\]

the correct bounds are

\[
 \|\psi_{\rm phys}\|\le0.001623186095,
 \qquad
 \|D\psi_{\rm phys}\|\le0.3424510530.
\]

The physical height is larger than Stage 5G-a's convenient target 0.001, but
that target was only sufficient, not maximal.  Direct use of the frozen
endpoint intervals still gives

\[
 H(J_-)\ge0.01805400129,
 \qquad
 H(J_+)\le-0.01316048384.
\]

Combining the adapted derivative with
\(\|P_sD_JK\|\le5.9793236648\) gives the sharper conditional interval

\[
 H'(I_J)\subset
 [-260.79414671,-243.20585329].
\]

Consequently, if the future two-return graph is actually certified in this
identical chart, contains the Stage-5G-b cone, and transfers to the physical
splitting, then opposite endpoint signs plus strict monotonicity give one
unique **selected** crossing automatically.  Stage 4P records this implication
only: the graph, crossing, physical onset, routing, and capture flags remain
false.

Holding the conservative pilot envelope fixed, the nonmixable isolated graph
ceilings are approximately

\[
(6.2892,122.0108,9503.0377,12.1163,222.1774,9209.9837).
\]

The two-return route also has a concrete smoothing advantage.  From the
frozen exact-orbit interval,

\[
 T-2\tau_{\max}>-4.17447,
 \qquad 2T-2\tau_{\max}>14.01174.
\]

Hence the exact two-period center clears the desired
\(T_2-\tau_{\max}>\tau_{\max}\) condition by a large margin.  A future proof
must still establish the directed full-ball event-window inequality
\(T_{2,-}>2\tau_{\max}\); the center calculation alone is not that proof.

## What \(K_{\rm ret}\) does and does not do

With the fixed unit split,

\[
 D^2P=P_sD^2P+\widehat q\,\widehat f(D^2P),
 \qquad \|\widehat q\|_Y=1.
\]

Therefore six projected caps imply the sufficient raw split bound

\[
 K_{\rm ret}^{\rm caps}
 =\max\{C_{s,ss}+C_{u,ss},
        C_{s,su}+C_{u,su},
        C_{s,uu}+C_{u,uu}\}.
\]

The converse is weaker: a raw scalar bound gives only
\(C_{s,ab}\le\|P_s\|K_{\rm ret}\) and
\(C_{u,ab}\le\|\widehat f\|K_{\rm ret}\).  Thus the Stage-4N target does not
replace the correlated six-block certificate.

More importantly, \(K_{\rm ret}\) is not a matrix Lyapunov--Perron input.  It
is one sufficient way to prove that the nonlinear selected map stays inside
the return ball.  A direct source-bound return-domain proof can replace it.
The two-return wide box makes this distinction visible: its pair-sum bound is
2000, well above either scalar target, while its split-correlated graph
majorant still closes.  The independently reported ambient Hessian diagnostic
\(H\approx337\) likewise has no authority to erase this correlation.

## Selected return versus first return

An abstract local stable graph needs a common \(C^2\) selected section map on
the full box, the invariant splitting, a validated return domain, and all six
projected Hessian blocks.  It does **not** need the selected event to be the
first positive return, and it does not need a no-earlier-hit proof.

No-earlier-hit becomes necessary when identifying the selected map with the
first Poincare return and when using the graph in the physical crossing/onset
pipeline.  At present even the full-ball selected nonlinear map is open, so
this logical separation does not promote a graph theorem.

## Decision

- One-return arithmetic design: **GO**; theorem release: **NO-GO**.
- Two-return arithmetic design: **conditional GO** and numerically more
  forgiving in the unstable blocks; theorem release: **NO-GO**.
- First new one-return hard gate: one source-bound signed event-aligned
  selected-return tube and all six correlated \(D^2P\) blocks.
- First new two-return hard gate: prove \(T_{2,-}>2\tau_{\max}\) on the full
  ball, then certify the complete-history correlated \(D^2(P^2)\) blocks.
- First-positive-return can be postponed until graph identification and the
  crossing/onset stage.

All nonlinear return, Hessian, graph, crossing, onset, routing, capture, and
safety flags remain false.
