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

The manuscript proves that the exact finite-parameter root is not determined
by the present finite-section axioms.  Relative to a fixed physical family,
projection, matching datum, and parameter normalization, its
baseline-subtracted leading response germ agrees pairwise for any two fixed
admissible preparations on their common parameter box.  No uniform remainder
over the whole preparation class and no physical outer canard are claimed.
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
and exact six-part finite-section ledger.

Build with:

```bash
make
```

The build regenerates the vector mechanism figure with Python and Matplotlib,
then uses `latexmk` in a forced two-document cycle so that cross-document
references resolve in both PDFs.  LaTeX intermediates and the main manuscript
PDFs are ignored by the repository; the reproducible figure source and vector
PDF are retained.
