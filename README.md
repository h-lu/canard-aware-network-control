# Canard-aware network dynamics and control

Private research repository for retarded fast--slow networks, complete-history
canards, and delayed FitzHugh--Nagumo pulse dynamics.

The completed Paper A manuscript is

> **Projection-Blind Delay Redistribution Moves Anchored Heteroclinic
> Canards in Retarded Markov Networks**

It is the current submission candidate.  Model-specific pulse thresholds and
general RFDE return-map methods are maintained as separate research units.

## Repository status

| Workspace | Role | Status |
| --- | --- | --- |
| [`manuscript/network-root-transfer`](manuscript/network-root-transfer) | Paper A: projection-blind delay redistribution and anchored complete-history canards | Complete compact manuscript: 60-page article plus 41-page supplement |
| [`manuscript/pulse-threshold`](manuscript/pulse-threshold) | Paper B: delayed-FHN stable-sheet pulse threshold | Active research draft; quantitative graph, crossing, and two-sided routing remain open |
| [`manuscript/rfde-methods-notes`](manuscript/rfde-methods-notes) | Paper C: selected-event RFDE return methods | Working notes; independent novelty and literature gates remain open |
| [`manuscript/jns`](manuscript/jns) | Original two-module paper | Historical submission package |
| [`manuscript/flagship`](manuscript/flagship) | Former integrated network/pulse draft | Frozen provenance only; not a submission manuscript |

The proof-spine split and release policy are described in
[`manuscript/README.md`](manuscript/README.md).

## Paper A result and boundary

For finite retarded Markov networks with a uniform Dobrushin gap, Paper A
constructs delay-layer redistributions that are invisible to the stationary
projection at every full history but produce a nonzero transverse-return
response.  Two distinct delay locations give a sharp, dimension-uniform
right inverse and dual reconstruction; merging the locations destroys the
leading redistribution source.

For every fixed member of a declared bounded anchor class, the paper further
constructs:

1. exact hyperbolic outer equilibria;
2. a past-complete incoming branch and an intrinsic future-decaying stable
   history sheet;
3. a unique complete-history heteroclinic-canard root; and
4. its full-dual response and centered conormal, uniformly in finite network
   size.

The physical root is intrinsic to each fixed anchored RFDE and independent of
the finite preparation used in the proof.  Exact roots for different global
anchors need not agree.  The original unanchored recovery law does not supply
the required outer equilibria, so no unanchored maximal-canard claim is made.

The theorem-to-proof map and all scope exclusions are in
[`CLAIM-MAP.md`](manuscript/network-root-transfer/CLAIM-MAP.md).

## Build and verify Paper A

Requirements are a recent TeX Live installation, Python 3.11 or newer, and
[`uv`](https://docs.astral.sh/uv/).  From the Paper A directory run:

```sh
cd manuscript/network-root-transfer
make
make check
```

`make` regenerates the vector mechanism figure and builds `main.pdf` and
`supplement.pdf` with cross-document references.  Generated article PDFs and
LaTeX intermediates are ignored by Git.

`make check` runs the focused analytic/static Paper A test slice.  It does not
replay the model-specific interval certificates belonging to Paper B.

To build all current manuscript workspaces:

```sh
make -C manuscript split
```

Historical fixed-epsilon certificate records remain available for provenance:

- [`docs/fixed-epsilon-frozen-graph-operator.md`](docs/fixed-epsilon-frozen-graph-operator.md)
  records a frozen operator enclosure: no graph fixed point, positive-amplitude hull open.
- [`docs/fixed-epsilon-singular-reachable-hull.md`](docs/fixed-epsilon-singular-reachable-hull.md)
  records the singular reachable-hull audit and its explicit scope limits.

## Repository map

- [`src/canard_control`](src/canard_control) -- symbolic, analytic, and
  certificate-building modules;
- [`tests`](tests) -- regression, contract, and source-binding tests;
- [`experiments`](experiments) -- reproducible drivers and tracked result
  records;
- [`docs`](docs) -- theorem contracts and validation records still relevant
  to active work;
- [`docs/literature-map.md`](docs/literature-map.md) -- primary-literature
  novelty boundary and closest mathematical baselines;
- [`docs/physical-root-literature-audit.md`](docs/physical-root-literature-audit.md)
  -- evidence map separating physical parameters, experimental thresholds,
  reduced or spectral roots, and complete-history connection roots;
- [`references/references.bib`](references/references.bib) -- shared primary
  bibliography;
- [`manuscript`](manuscript) -- submission units and historical manuscripts.

Many numerical artifacts bind exact source hashes and software versions.
Use the requirement file or command recorded beside each artifact rather than
assuming that the entire historical certificate archive replays under one
modern Python environment.

## Branch and release policy

`main` is the only long-lived branch.  Bounded work uses short-lived branches
which are merged and deleted.  Completed or superseded states are retained as
immutable tags rather than abandoned branches:

- `paper-a-complete-2026-08-31` -- completed compact Paper A source;
- `archive-paper-a-proof-ledgers-2026-08-31` -- superseded long Paper A proof
  ledgers excluded from the submission build.

The development repository remains private.  Before submission, Paper A must
be exported to a minimal public repository with a locked runtime, independent
checker where feasible, immutable release, and permanent archive identifier.
