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
high-order raw-compatible repelling p(0) feedback and proves a small
zeroth-order normal-to-phase action column.  In the reverse direction it
derives the exact formal phase-delay defect, closes its delayed scalar
phase--event inverse, and identifies the phase-induced normal residual.  A
fixed-`r` event-aligned trace theorem removes the scaled terminal-time
unknown from normal rows at the reduced base.  The raw-compatible phase
collar, affine-residual normal bound, complete border, nonlinear tracker,
and finite-`delta` physical slow-history relation remain open.
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
