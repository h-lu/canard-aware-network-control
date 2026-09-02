# Projection-blind delay redistribution moves anchored heteroclinic canards

This directory contains Paper A, the focused network-theory successor to the
integrated research draft in `../flagship/`.  It is independent of the
model-specific pulse-threshold program in `../pulse-threshold/`.

## Main result

For finite retarded Markov networks with a common Dobrushin gap, the paper
constructs delay-layer redistributions that are exactly invisible to the
stationary projection of the RFDE vector field at every full history.  Two
distinct delay locations nevertheless make their first moment span the whole
transverse space, with an explicit sharp right inverse and an `N`-uniform dual
reconstruction bound.  With one merged delay location, that leading source is
identically zero on the pure-redistribution class.

The shared-resource model is globally completed by a fixed anchor multiplier
which equals one on the entire retained fold-history tube.  For every fixed
member of the declared bounded anchor class, the paper proves:

1. exact hyperbolic anchor equilibria with
   `dim W^u(E_N^+)=1` and `codim W^s(E_N^-)=1`;
2. a past-complete incoming branch and an intrinsic nonlinear stable history
   sheet constructed by a half-line Lyapunov--Perron problem;
3. a unique local parameter root giving a complete heteroclinic orbit from
   `E_N^+` to `E_N^-`;
4. quantitative attracting-to-repelling slow-history tracking, so the orbit
   is a canard;
5. the full-dual-norm response law

   ```text
   D_eta mu_c(delta,eta)
     = delta^3 Lambda_N + O(delta^4 + delta^3 ||eta||),
   ```

   uniformly in network size; and
6. modelwise-centered conormal convergence to `(1,-Lambda_N)`, uniformly over
   the bounded anchor class.

The exact root is intrinsic to each fixed anchored RFDE and independent of
finite proof preparations.  Exact roots for different anchors need not agree.
The original unanchored recovery law is proved not to supply the required
outer equilibria, so the paper makes no maximal-canard claim for that law.

## Manuscript architecture

- `main.tex` contains the flagship theorem, precise literature/novelty
  boundary, source and dual-recovery results, local RFDE mechanism, compact
  local-to-global interface, and the anchored complete-history theorem.
- `supplement.tex` contains only the preparation, invariant-history,
  finite-gap, compressed outer-passage, stable-sheet, and complete-history
  proofs required by the flagship theorem.
- `CLAIM-MAP.md` maps theorem claims to proof locations and records scope
  boundaries.
- `../../docs/paper-a-flagship-figure-contract.md` records the semantics and
  review contract for the main mechanism figure.
- `../../docs/physical-root-literature-audit.md` separates the anchored
  connection root proved here from experimental thresholds, spectral roots,
  and reduced-model tipping points in the closest application literature.

The selected finite-core roots retained in the paper are comparison devices
and secondary readouts.  They are not substituted for the fixed-model
heteroclinic root.  The recovery-sensing companion and the long development
ledgers are excluded from the submission build, so the article has one model
and one flagship geometric object.

## Build

From this directory, run:

```bash
make
make check
```

The build regenerates the vector mechanism figure from
`figures/root_mechanism.py`, then forces a two-document `latexmk` cycle so
that cross-document references resolve in both PDFs.  The second command runs
the 16-file analytic/static Paper A test slice; it does not invoke the
model-specific interval certificates belonging to the pulse-threshold
project.

Useful checks include:

```bash
rg -n 'Warning|undefined|Overfull|Underfull' main.log supplement.log
pdfinfo main.pdf
pdfinfo supplement.pdf
pdffonts main.pdf
pdffonts supplement.pdf
```

The result is analytic and does not rely on a numerical certificate.  A
paper-specific public source release and immutable archive are required before
submission.
