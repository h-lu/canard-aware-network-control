# Paper A flagship claim and proof map

This audit map tracks [Issue #31](https://github.com/h-lu/canard-aware-network-control/issues/31).
It is not part of the submitted paper.

## Central theorem package

```text
exact projection blindness
    + two separated delay moments span the transverse source
    + transverse full-history inverse and collective return
    = uniformly identifiable hidden-return covector
    -> nonlinear complete-history root readout.
```

The exact finite-section root is not intrinsic under the present axioms.
The canonical object is the baseline-subtracted response germ and its
covector.

| Flagship requirement | Statement | Proof location |
| --- | --- | --- |
| Integrated flagship theorem | `thm:flagship-synthesis` | Exact blindness, two-delay source dichotomy, selected-root readout, dual recovery, and the canonicity boundary |
| Abstract two-atom source criterion | `prop:abstract-two-atom-source` | General moment-source norm, explicit extreme-atom right inverse, minimum probe cost, dual isometry, and one-atom no-go |
| Sharp two-delay controllability | `thm:hidden-return-tomography` | Exact source norm, explicit right inverse, and merged-single-delay no-go |
| Dimension-uniform dual recovery | `thm:hidden-return-tomography` | `r(z)=Lambda(Q A z)` and condition bound `(2-gamma)/gamma` |
| Finite-scale curvature pairings | `cor:curvature-tomography` | Unit-probe-ball root remainder and weighted reconstruction |
| Finite-scale recovery pairings | `cor:recovery-tomography` | Second-model pairing formula and arbitrary fixed-`N` covector rays |
| Preparation-relative canonical response germ | `thm:canonical-response-germ` | Pairwise fixed-preparation expansion and uniform derivative limit |
| Obstruction to exact root canonicity | `prop:finite-section-noncanonicity` | Shared-resource localized target-frozen completion bump plus trace/root IFT |
| Abstract mechanism beyond one model | `thm:hidden-return-schur` | Cokernel Schur quotient, coordinate/range invariance, uniform norm bound |
| Whole-line collective cokernel | `lem:fold-gaussian-cokernel` | Explicit fundamental pair and weighted Green inverse |
| Nonlinear persistence | `cor:schur-to-root` | Uniform range-to-root theorem plus Schur profile identity |
| First return channel | `thm:shared-resource` | Markov inverse followed by heterogeneous fast curvature |
| Second return channel | `thm:sensed-recovery-response` | Markov inverse followed by heterogeneous slow recovery sensing |
| Fixed-network genericity | `thm:response-directions`, `thm:sensed-recovery-response` | Nonzero bounded covectors; codimension-one kernels |
| Sparse/high-rank realization | `cor:reset-cycle-response`, `cor:pure-sensing-response` | Directed reset cycle, nonnegative chosen-base-layer-support-preserving perturbations, and rank-`N-1` directions |
| Graph/preparation logical closure | Selection convention `(S1)--(S4)`, `lem:graph-only-retained-expansion`, `lem:preparation-existence` | Concise main-text interface; graph-only retained-tube theorem and construction in the supplement |
| Exact finite-section bridge | `prop:finite-gap-bridge` | Endpoint, tail, moving-trace, parameter, graph-jet, and preparation errors |

## Main novelty boundary

- The new part is the conjunction of exact atomwise projection blindness,
  pure-redistribution control of every transverse source by two separated
  delays, sharp `N`-uniform inverse bounds, and nonlinear complete-history
  root readout.
- Schur elimination, one-dimensional cokernel projection, and recovery of a
  finite-dimensional functional from a right inverse are standard operations
  and are not priority claims.
- The observation theorem reconstructs the compressed return covector for a
  known network skeleton.  It does not reconstruct the hidden network.
- Pairing estimates are uniform over the unit probe ball.  Coordinate recovery
  from finitely many noisy probes is not `N`-uniform without a lower frame
  bound, and root measurement noise is amplified by
  `delta^(-3)|zeta|^(-1)`.

## Two model dictionaries

The common blind source is

```text
h_*(R) = (K/(2 alpha)) A_N^(-1) P_perp,N
         (sum_k theta_k R_k) 1.
```

The fast-curvature model returns

```text
Lambda_curv(R) = -(1/alpha) pi_N^T(c_N o h_*(R)).
```

The sensed-recovery model returns

```text
Lambda_rec(R) = pi_N^T((varpi_N-c_N/alpha) o h_*(R)).
```

The limits separate exactly:

- `varpi_N = 1` recovers pure curvature return;
- `c_N = alpha 1` kills curvature return but permits pure sensing return.

## Literature boundary

- Exact lumpability requires factorization through projected history; the
  paper proves equality at each common unreduced history without closure.
- Mori--Zwanzig theory is a conceptual baseline for unresolved return; the
  paper does not derive a memory kernel or generalized Langevin equation.
- Nonidentifiability is from the projected-functional summary, not structural
  input--output unidentifiability, nonlinear-delay observability, or recovery
  of unknown DDE parameters.
- Adjoint/covector sensitivity for time-lag systems is standard.  The new
  step is the exact blind-source factorization, dimension-uniform history
  return, and nonlinear complete-history root remainder.
- Delayed-network reconstruction literature recovers edges, delays, or
  dynamics from data.  Here the network and delays are known and only one
  compressed return covector is reconstructed.
- Existing network canard, Banach-space canard, RFDE Fredholm, and Lin results
  are neighboring tools; no priority claim is made for those theories.

## Quantifier boundaries

- Uniformity is over finite networks with common Dobrushin, delay-support,
  coefficient, direction, and fixed-preparation bounds.
- Preparation independence is pairwise for fixed preparations on intersected
  parameter boxes; it is not a single bound over an unbounded preparation
  class.
- The no-go theorem concerns the stated finite-section axioms.  It does not
  rule out a canard selected by physical outer invariant manifolds.
- A zero leading covector does not rule out higher-order response.
- The one-delay no-go applies only to the pure-redistribution leading source
  after coincident atoms have been merged.
- No pulse threshold, biological onset, infinite-network limit, moving delay
  support, or closing-gap theorem is claimed.

## Reproduction gate

From this directory, the command below builds both `main.pdf` and
`supplement.pdf`:

```bash
make
```

Before release, record the final commit, PDF hash, page count, clean-log
audit, embedded-font audit, figure-page review, and independent cold reads.
