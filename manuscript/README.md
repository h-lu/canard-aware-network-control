# Manuscript workspaces

The repository keeps one shared development history and separates papers by
mathematical proof spine inside `manuscript/`. Paper workspaces are not
maintained as permanently divergent Git branches.

## Status

| Workspace | Role | Status |
| --- | --- | --- |
| `jns/` | Earlier two-module complete-history paper | Historical package |
| `flagship/` | Integrated network/pulse development ledger | Frozen provenance; not a submission manuscript |
| `network-root-transfer/` | Paper A: anchored network canard response | Complete submission candidate |
| `pulse-threshold/` | Paper B: delayed-FHN stable-sheet pulse threshold | Active; five proof gates remain open |
| `rfde-methods-notes/` | Paper C: selected-event RFDE methods | Notes; independent novelty gate remains open |

The split is intentional. Do not repair the historical `flagship/` draft by
recombining Paper A, the physical pulse problem, and the general RFDE tools.

## Paper A: anchored network canard response

For a declared class of fixed anchored retarded Markov networks, Paper A now
constructs intrinsic past-complete histories and proves a unique local
parameter root producing a complete heteroclinic canard. Projection-blind
delay redistribution is recovered through transverse dynamics, giving an
explicit, network-size-uniform response covector and conormal limit.

The result is independent of finite proof preparations for each fixed
anchored RFDE. Roots associated with different anchors need not agree. The
paper expressly does not claim an unanchored physical maximal canard: the
original recovery law lacks the outer equilibria required by that statement.

The manuscript is compact by design. Superseded proof ledgers are preserved
in the immutable tag `archive-paper-a-proof-ledgers-2026-08-31`, not in the
submission build.

## Paper B: physical pulse threshold

Paper B retains the model-specific delayed-FHN program. Its open proof spine
is:

```text
quantitative stable graph on the physical pulse domain
  -> stable-set identification
  -> unique pulse/stable-sheet crossing
  -> outer attachment and capture
  -> uniform two-sided routing and onset.
```

Until this chain closes, the repository makes no unconditional biological
onset or safety-coordinate claim.

## Paper C: RFDE methods notes

Paper C isolates eventual joint smoothing for selected complete-history
events and a direct-return stable-set-germ argument. It remains a notes
workspace until comparison with the primary RFDE literature establishes an
independent theorem beyond standard semiflow, Poincare-map, and
stable-manifold theory. If that novelty gate fails, the material remains a
tool for Paper B.

## Build

From this directory:

```sh
make split
```

Individual entry points are `make network`, `make pulse`, and `make methods`.
Paper A also provides its focused analytic/static check:

```sh
make -C network-root-transfer check
```

Generated PDFs and LaTeX intermediates remain ignored until a paper-specific
release is deliberately frozen.

## Version policy

`main` is the only long-lived branch. Short-lived task branches are merged
back into it; immutable paper snapshots are tags. The current Paper A
submission state is tagged `paper-a-complete-2026-08-31`.
