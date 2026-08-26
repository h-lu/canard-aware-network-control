# Stage 6A: a source-bound nonlinear outer return tube

## Outcome and scope

Stage 6A upgrades the Stage-3I phase-fixed **linear** contraction to a
nonlinear local return theorem on one explicit, nonzero ball.  On the exact
outer phase-zero section

\[
Y=C([-5\sqrt5,0],\mathbb R)_v\times\mathbb R_{w(0)},
\qquad h_v(0)=0,
\]

the proved section radius is

\[
r_6=10^{-335}.
\]

For every reduced history in this ball, the next positive local-section
event exists uniquely, depends (C^2) on the history, has no earlier hit of
the same local section disk, and defines a strict nonlinear contraction.
The compatible complete-history flow sweep remains in the radius
(10^{-3}) ambient tube and returns to it.  This is the first source-bound
nonlinear outer return tube in the chain.

The radius is intentionally reported without cosmetic reinterpretation.  It
comes from a global row-sum Gronwall estimate over a (26.6)-unit period and
is far too small to contain the directed (J=0.32) pulse attachment.  Thus
outer pulse capture, two-sided biological routing, and physical onset remain
false.  Stage 6A uses no inner stable graph.

The executable source is
[leaky_outer_nonlinear_tube_stage6a.py](../src/canard_control/leaky_outer_nonlinear_tube_stage6a.py),
the generator is
[leaky_outer_nonlinear_tube_stage6a.py](../experiments/leaky_outer_nonlinear_tube_stage6a.py),
and the registered result is
[leaky_outer_nonlinear_tube_stage6a.json](../experiments/results/leaky_outer_nonlinear_tube_stage6a.json).

## 1. Linear parent and local field remainder

Stage 3I proves on the arbitrary-(C^0) reduced section that

\[
\|DP_o(0)\|\le q_o,
\qquad
q_o=0.55051563144094195<1,
\]

with the recovery row bounded by
(0.028280815376548179).  These are exact-orbit row budgets, not sampled
finite-section norms.

The existing outer routing contract proves on the ambient radius-(0.01)
strip that

\[
\|F(\Gamma_o+\eta)-F(\Gamma_o)-DF(\Gamma_o)\eta\|
 \le C_R(R)\|\eta\|_X^2,
\]

and

\[
\|D^2F\|\le B_2(R).
\]

Stage 6A chooses (R=10^{-3}), recomposes both polynomial formulas from
their exact decimal model constants, and also derives a uniform Jacobian
row-sum bound (L) on the same strip.

## 2. Directed phase separation and event orientation

The exact binary64 outer Fourier coefficients are treated as dyadics.  The
normalized phase circle is split into 256 cells.  On every one of the 254
middle cells, degree-24 Fourier--Taylor polynomials are converted to
Bernstein form with 192-bit outward MPFR arithmetic.  Current voltage and
recovery are compared with their phase-zero values before the component
maximum is taken.

After subtracting twice the exact orbit coefficient radius, the middle arc
satisfies

\[
\inf_{x\in[1/256,255/256]}
 \max\{|V_o(x)-V_o(0)|,|W_o(x)-W_o(0)|\}
 >0.0912678.
\]

The two wrap cells are evaluated through the physical RFDE fast field,
including both delayed Fourier histories.  After the exact period/history
transfer is deducted, their positive speed remains strictly bounded away
from zero.  This establishes a local phase chart rather than silently
treating a sampled voltage crossing as a Poincare event.

The word *local* matters.  The affine voltage level can have an
opposite-orientation crossing elsewhere on the orbit.  A Stage-6A hit means
the affine voltage equality **and** membership in the radius-(r_6) reduced
disk.  The middle-arc separation proves that the other global crossing is
not an earlier hit of this local section.

## 3. Uniform ball, event map, and nonlinear remainder

Let (H) be the upper period plus one wrap cell.  On the full radius-(R)
tube the elementary comparison estimate gives

\[
G=e^{LH},
\qquad
\|\eta_t\|\le G\|\eta_0\|.
\]

The registered inequality (G r_6<R) closes by a strict margin.  If (a)
is the perturbed event-speed lower bound, first and second event-time
derivatives obey

\[
\|D\tau\|\le \frac{G}{a},
\]

\[
\|D^2\tau\|
\le
\frac{V_2+2LG\|D\tau\|+A_2\|D\tau\|^2}{a},
\]

where

\[
V_2\le B_2HG^2,
\qquad
A_2\le L F_{\rm tube}.
\]

The physical-time second derivative of the returned history is then bounded
by

\[
C_P=V_2+2LG\|D\tau\|+A_2\|D\tau\|^2
      +F_{\rm tube}\|D^2\tau\|.
\]

Consequently

\[
\|DP_o(h)-DP_o(0)\|\le C_P\|h\|,
\qquad
\|P_o(h)-DP_o(0)h\|\le \tfrac12 C_P\|h\|^2.
\]

The single nonlinear return inequality is

\[
q_o+C_Pr_6<1.
\]

The result file records the directed value of every term, the strict
contraction margin, and the strict self-map margin.

## 4. No earlier hit and complete histories

The proof divides one return into three pieces.

1. On the first wrap cell, the perturbed voltage speed is positive, so the
   initial section point cannot immediately recross.
2. On the 254 middle cells, the exact phase separation minus the uniform
   flow deviation remains much larger than the local section radius.
3. On the final wrap cell, opposite endpoint signs and the positive speed
   give exactly one event.

The lower endpoint of every returned history window is strictly positive:

\[
T_o(255/256)-5\sqrt5>0.
\]

Therefore the returned recovery history is generated entirely by the RFDE,
not borrowed from an arbitrary initial recovery trace.  The exact reduced
future factorization says that the future depends only on the voltage
history and current recovery.  Starting with a compatible complete history
whose reduced section coordinate is at most (r_6) and whose old recovery
trace is within (10^{-3}), the full sweep stays in the (10^{-3}) tube;
the returned reduced coordinate is at most
((q_o+C_Pr_6)r_6<r_6), and the returned complete history is again inside
the full tube.  Iteration gives quantitative local orbital attraction on
this forward tube.

## 5. Exact first biological failure

The directed (J=0.32) attachment parent proves an ambient complete-history
distance

\[
d_{.32}\le2.637078616900037\times10^{-5}.
\]

It does not place that history on the exact outer section.  More decisively,
even the optimistic comparison (d_{.32}<r_6) fails by roughly 330 orders
of magnitude.  Hence the first failed biological gate is

\[
\boxed{\text{ambient-to-section domain containment}.}
\]

This failure occurs before any capture inference and is independent of the
inner stable graph.  The next useful improvement is not another linear
Floquet calculation; it is a sharp intermediate-flow/second-variation
kernel that replaces the global (e^{LH}) loss and enlarges the nonlinear
section radius toward the (10^{-5}) attachment scale.  At
(r=d_{.32}), the contraction inequality requires approximately

\[
C_P<\frac{1-q_o}{d_{.32}}\approx1.7046\times10^4,
\]

whereas the present global estimate is about (1.1323\times10^{333}), a
gap of roughly 329 decimal orders.

## 6. Claim boundary

Stage 6A proves:

- an explicit nonzero reduced section ball;
- a directed (C^2) local event phase map;
- no earlier hit of that local section;
- a nonlinear return contraction and self-map;
- a compatible forward-invariant complete-history return tube.

It does **not** prove:

- a radius-(10^{-4}) return tube;
- entry of the (J=0.32) attachment into its phase chart;
- outer pulse capture;
- an inner stable-graph crossing;
- two-sided biological routing, physical onset, or safety control.
