# Network root-transfer manuscript

This directory contains the focused paper on selected complete-history roots
in heterogeneous finite retarded networks.  It is independent of the physical
pulse-threshold program in `../pulse-threshold/`.  The integrated source draft
remains frozen in `../flagship/` as a provenance ledger.

The principal theorem concerns a projection-invisible perturbation of a
heterogeneous shared-resource network.  Atomwise stationary-row neutrality
makes the projected RFDE right-hand side identical at every full history, yet
the selected complete-history root moves through a transverse-resolvent and
curvature-return mechanism.  The manuscript proves a network-size-uniform
response expansion, classifies zero leading-response directions, gives a robust
non-synchrony witness with an asynchronous root orbit, and shows that the
leading response increment is shared by any two fixed canonical
preparations.

The exact finite-parameter baseline root is not claimed to be preparation
independent or to be a physical outer canard.  The former leaky-network and
upper-triangular Lin-transfer companion has been removed from this paper; the
pre-refocus source is preserved by the Git tag
`paper-a-before-hidden-response-refocus`.

The acceptance criteria, theorem labels, proof locations, and exact scope
boundaries are indexed in [`CLAIM-MAP.md`](CLAIM-MAP.md).

Build with:

```bash
make
```

The build first regenerates the vector mechanism figure with Python and
Matplotlib, then uses Tectonic when available and otherwise falls back to
`latexmk`.  LaTeX intermediates and the manuscript PDF are ignored by the
repository; the reproducible figure source and its vector PDF are retained.
