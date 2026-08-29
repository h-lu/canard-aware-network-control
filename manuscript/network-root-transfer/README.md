# Two-delay blind controllability and selected fold-response readout

This directory contains the focused paper on selected complete-history roots
in heterogeneous retarded Markov networks.  It is independent of the physical
pulse-threshold program in `../pulse-threshold/`.  The integrated source draft
remains frozen in `../flagship/` as a provenance ledger.

The integrated flagship theorem proves that pure delay redistributions which
are invisible to the stationary projection generate every transverse forcing
direction when two delay locations are distinct.  An abstract two-atom moment
criterion isolates the portable source interface and its minimum probe cost.
The Markov realization gives a sharp right
inverse, an `N`-uniform dual reconstruction bound, and a matching one-delay
no-go theorem.  The RFDE realization turns the recovered return covector into
a network-size-uniform nonlinear complete-history root response.  It includes
fast-curvature and slow-sensing return channels, generator-supported probes,
and sparse directed chosen-base-layer-support-preserving rank-`N-1` examples.

For the shared-resource family, the manuscript proves that the exact
finite-parameter root is not determined by the present finite-section axioms.
Relative to a fixed physical family,
projection, matching datum, and parameter normalization, its
baseline-subtracted leading response germ agrees pairwise for any two fixed
admissible preparations on their common parameter box.  No uniform remainder
over the whole preparation class and no physical outer canard are claimed.
For both return channels, centering a selected connection curve at its own
baseline gives the raywise limiting conormal
`span{d xi-Lambda_N(R_N) d zeta}`.  For the shared-resource family only, a
structural-ball admissible selection rule upgrades these raywise statements:
the full `delta^(-3)`-weighted tangent hyperplane converges to the kernel of a
cokernel-valued hidden-return jet, while the calibrated conormal converges in
dual norm to `(1,-Lambda_N)`.  This removes dependence on a scalar gap
representative, but it remains a selected connection object.  The
preparation-free physical identification is tracked separately in Issue #32
and must be proved for this shared-resource Markov class; Issue #11 concerns a
different Paper III model.  The development manuscript now proves the exact
critical curve, leading frozen-voltage splitting, and truncated reduced
actions as precursors, together with a generic obstruction to selecting a
history from convergence in an unnormalized history norm alone.  Its
fixed-phase component analysis now includes high-order finite-generation
flushing on both outer branches, with a forward-transverse/future-scalar
first-exit construction on the repelling side.  It also closes the
high-order raw-compatible repelling `p(0)` feedback and proves the small
zeroth-order normal-to-phase action column.  In the reverse direction, the
exact phase-delay shift exposes the failure of a uniform old-normalized-state
bound, while the structured response has true-speed action
`O(r_out^2+delta/S_delta)`.  The moving-core collar supplies the exact
raw-compatible boundary column, including the repelling feedback, and the
affine-residual bulk source is controlled in the shifted response.  Together
these results close a fixed-reduced-base zeroth-order phase--normal inverse in
a graph/action norm, with total action
`O(r_out^2+delta/S_delta+delta^(2-2 vartheta))`.  The base raw-collar
correction is further shown to be `O(epsilon |e|)` (hence
`O(delta^3 S_delta)` at the inner sections).  An exact inner-anchored
nonlinear `q_0`-flow chart preserves the two same-sign branches, and its
one-row relative-phase linearization has a dimension-uniform Schur inverse
with pointwise action
`O(r_out(r_out+S_delta^(-2)+delta^(2-2 vartheta)))`.  The fixed-section
analysis now also proves an `O(delta)` relative phase-delay profile and
recovers the returned state and pointwise true action with the sharper factor
`O(r_out+S_delta^(-1))` in a uniformly equivalent relative graph--action
norm.  This uses the inner anchor and does not contradict the unrestricted
old-state obstruction.  The exact nonlinear formal `q_0`-history delay
functional is now also closed: its derivative is the linear phase-delay
column and its two-point remainder is `O(delta |r|)` in value and piecewise
derivative.  The nonlinear raw-compatible old-history assembler is now
constructed directly by the finite compatibility recursion on a
fixed-reference ball.  It includes the second endpoint jet and a
dimension-uniform normalized quadratic graph remainder, without comparing
the full fixed and moving fading norms.  These modules are now assembled into
an exact fixed-parameter, inner-anchored nonlinear graph--action residual.
Its derivative is precisely the existing raw-compatible Schur isomorphism,
its normalized base defect is
`O(r_out+S_delta^(-2))`, and it has a dimension-uniform quadratic/two-point
remainder.  A uniform contraction now closes the quantitative branch
solution pointwise at every fixed admissible parameter pair: each outer
branch has a unique small zero in its canonical graph slice, with a first
Newton jet and strict speed sign.  The zero reconstructs an exact finite
forward RFDE segment.  On every retained subsegment whose full delay collar
lies beyond the first maximal delay, the physical collective coordinate gives
an exact tracker representative, exact backtracks and uncut history
invariance, and the resource-gauge quotient has an `O(S_delta^(-1))`
Volterra realization.  This generated-interior result is not preparation
independent and does not provide either physical branch endpoint.  On the
common generated neighborhoods of the fixed sections
`r=+/-r_out/2`, the exact resource-gauge quotient now satisfies an
RFDE-specific finite-window Green/Lyapunov--Perron flushing estimate.  Its
superalgebraic action, combined with the exact stationary event quotient,
proves first-order raw-gauge equivalence modulo `O(delta^infinity)` for each
complete physical-hit history in the natural `epsilon^(-1)` event norm.
This is a local fixed-parameter fixed-section hit class, not exact finite-`delta`
gauge independence.  Higher gauge and parameter jets, original-endpoint
recutting, a past-complete outer history, the cross-branch handoff,
action-weighted global normal splitting, and the finite-`delta` physical
connection/root remain open.
The former leaky-network and
upper-triangular Lin-transfer companion has been removed from this paper; the
pre-refocus source is preserved by the Git tag
`paper-a-before-hidden-response-refocus`.

The acceptance criteria, theorem labels, proof locations, and exact scope
boundaries are indexed in [`CLAIM-MAP.md`](CLAIM-MAP.md).

The submission build is split into `main.pdf` and `supplement.pdf`.  The main
article keeps all hypotheses, theorem outputs, return formulas, and the
load-bearing proof mechanism.  The supplement contains the weighted Whitney
preparation, localized noncanonicity bump, complete special-flow history graph,
exact six-part finite-section ledger, critical-layer proof, and history-
selection counterexample.

Build with:

```bash
make
```

The build regenerates the vector mechanism figure with Python and Matplotlib,
then uses `latexmk` in a forced two-document cycle so that cross-document
references resolve in both PDFs.  LaTeX intermediates and the main manuscript
PDFs are ignored by the repository; the reproducible figure source and vector
PDF are retained.
