# Network root-transfer manuscript

This directory contains the focused paper on selected complete-history roots
in heterogeneous finite retarded networks.  It is independent of the physical
pulse-threshold program in `../pulse-threshold/`.  The integrated source draft
remains frozen in `../flagship/` as a provenance ledger.

The principal theorem is the heterogeneous shared-resource result: for a
common Dobrushin gap, fixed delay support, an atomwise row-neutral structural
direction, and one canonical preparation datum fixed across the family, it
constructs a unique local selected complete-history root with a nonzero
response coefficient uniform in network size.  The exact finite-parameter
root is not claimed to be preparation independent or to be a physical outer
canard.

Supporting results give a complete-line transverse inverse for the leaky
network and an exact upper-triangular transfer of any supplied scalar simple
Lin root.  The leaky scalar root itself is not constructed in this paper.

Build with:

```bash
make
```

The build first regenerates the vector mechanism figure with Python and
Matplotlib, then uses Tectonic when available and otherwise falls back to
`latexmk`.  LaTeX intermediates and the manuscript PDF are ignored by the
repository; the reproducible figure source and its vector PDF are retained.
