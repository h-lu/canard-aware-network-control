# Network root-transfer manuscript

This directory contains the focused paper on dimension-uniform selected
complete-history roots in finite retarded networks.  It is independent of the
physical pulse-threshold program in `../pulse-threshold/`.  The integrated
source draft remains frozen in `../flagship/` as a provenance ledger.

The principal theorem is the heterogeneous shared-resource result: for a
common Dobrushin gap, fixed delay support, an atomwise row-neutral structural
direction, and a bounded class of preparations, it constructs a unique local
preparation-indexed complete-history root with a nonzero response coefficient
uniform in network size.  The exact finite-parameter root is not claimed to
be preparation independent or to be a physical outer canard.

Supporting results give a complete-line transverse inverse for the leaky
network, an exact upper-triangular transfer of any supplied scalar simple Lin
root, and an abstract dimension-uniform one-gap estimate.  The leaky scalar
root itself is not constructed in this paper.

Build with:

```bash
make
```

`make` uses Tectonic when available and otherwise falls back to `latexmk`.
Generated PDFs and LaTeX intermediates are ignored by the repository.
