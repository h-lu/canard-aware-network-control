# Manuscript workspaces

This repository is the single development source for the canard-network and
physical-pulse research program.  Papers are separated by mathematical proof
spine inside `manuscript/`; they are not maintained as permanently divergent
Git branches.

## Workspace status

| Workspace | Role | Current status |
| --- | --- | --- |
| `jns/` | Completed two-module complete-history paper | Historical submission package; preserve independently |
| `flagship/` | Integrated network/pulse research ledger | Frozen reference draft; not a submission manuscript |
| `network-root-transfer/` | Paper A: finite-network selected-root theory | Active rewrite; first publication target |
| `pulse-threshold/` | Paper B: model-specific stable-sheet pulse threshold | Active research draft; central proof gates remain open |
| `rfde-methods-notes/` | Paper C: selected-return regularity methods | Research notes; independent novelty not yet established |

The integrated `flagship/` draft remains the provenance record for the split.
It should not be repaired into a submission by recombining the three
workspaces.

## Mathematical boundaries

### Paper A: network root transfer

Its proof spine is

```text
Dobrushin diameter contraction
  -> causal, dimension-uniform transverse complete-line inverse
  -> upper-triangular Lin row reduction and corrected cokernel
  -> uniform selected-root perturbation theorem
  -> heterogeneous shared-resource realization with nonzero response
     and no nontrivial synchrony quotient.
```

The paper may claim a preparation-indexed selected complete-history root and
its dimension-uniform response under the stated hypotheses.  It must not call
that root a preparation-independent physical canard without a separate
zero-fiber or compatible-selection theorem.  It excludes the delayed-FHN
stable-sheet crossing, biological onset, safety coordinates, and all
model-specific pulse certificates.

### Paper B: physical pulse threshold

Its intended proof spine is

```text
event-aligned complete-history return
  -> quantitative stable graph on the physical pulse domain
  -> identification with the inner periodic orbit's stable-set germ
  -> graph-adjusted endpoint signs and a unique pulse crossing
  -> attachment of the two sides to quiet and outer attraction tubes.
```

The current draft proves important event, derivative, spectral, local-return,
and conditional-crossing ingredients.  It does not yet prove the quantitative
stable graph, the model-specific stable-set identification, the selected
stable-sheet crossing, outer attachment, or two-sided routing.  Until those
gates close, neither a biological-onset theorem nor a safety-coordinate claim
is permitted.

### Paper C: RFDE methods notes

These notes isolate the eventual joint smoothing of selected complete-history
events and a direct-return stable-set-germ lemma.  They remain notes until a
primary-literature comparison establishes an independent result beyond the
available RFDE semiflow, Poincare-map, and stable-manifold theory.  If that
novelty gate fails, the material stays as a tool in Paper B rather than being
submitted separately.

## Branch policy

- `main` is the only long-lived development branch and contains all paper
  workspaces, shared code, certificates, and tests.
- Use short-lived branches such as `paper/network-<task>` or
  `paper/pulse-<task>` for bounded edits, then merge them back into `main`.
- Do not maintain one permanent branch per paper.  Shared mathematical and
  certificate corrections must not require repeated cherry-picking.
- A paper release is represented by an immutable tag, not by an abandoned
  branch.

## Public-release policy

The private development repository is not itself the reviewer-facing
artifact.  Once a paper is mathematically and editorially ready, export a
minimal paper-specific public repository containing:

1. the manuscript source and final PDF;
2. only the source, generators, results, and tests needed by its theorems;
3. a locked and tested runtime, including arithmetic-library and thread
   requirements;
4. one theorem-to-artifact map and one end-to-end verification command;
5. a small independent certificate checker where feasible;
6. a license, immutable release tag, and permanent archive identifier.

The planned public repositories are provisionally named
`retarded-dobrushin-root-transfer` and `delayed-fhn-pulse-threshold`.  No
methods repository is created unless Paper C passes its novelty gate.

Before any export, audit relative paths and source manifests.  Copying or
renaming a source-bound artifact can invalidate its registered provenance even
when its numerical payload is unchanged.

## Build the split workspaces

From `manuscript/`, build all three current workspaces with

```sh
make split
```

or build one workspace with `make network`, `make pulse`, or `make methods`.
Generated PDFs and LaTeX intermediates are development artifacts and remain
ignored until a paper-specific release is deliberately frozen.
