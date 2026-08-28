# Paper A flagship claim and proof map

This audit map tracks [Issue #31](https://github.com/h-lu/canard-aware-network-control/issues/31)
and the weighted-connection upgrade in
[Issue #32](https://github.com/h-lu/canard-aware-network-control/issues/32).
It is not part of the submitted paper.

## Central theorem package

```text
exact projection blindness
    + two separated delay moments span the transverse source
    + transverse full-history inverse and collective return
    = uniformly identifiable hidden-return covector
    -> nonlinear complete-history root readout.
```

In the shared-resource family, the exact finite-section root is not intrinsic
under the present axioms.  The relative-canonical selected object is the
baseline-subtracted response germ, its covector, and its weighted conormal,
with the physical model, projection, matching data, and parameter calibration
fixed.

| Flagship requirement | Statement | Proof location |
| --- | --- | --- |
| Integrated flagship theorem | `thm:flagship-synthesis` | Exact blindness, two-delay source dichotomy, selected-root readout, dual recovery, and the canonicity boundary |
| Abstract two-atom source criterion | `prop:abstract-two-atom-source` | General moment-source norm, explicit extreme-atom right inverse, minimum probe cost, dual isometry, and one-atom no-go |
| Sharp two-delay controllability | `thm:hidden-return-tomography` | Exact source norm, explicit right inverse, and merged-single-delay no-go |
| Dimension-uniform dual recovery | `thm:hidden-return-tomography` | `r(z)=Lambda(Q A z)` and condition bound `(2-gamma)/gamma` |
| Finite-scale curvature pairings | `cor:curvature-tomography` | Unit-probe-ball root remainder and weighted reconstruction |
| Finite-scale recovery pairings | `cor:recovery-tomography` | Second-model pairing formula and arbitrary fixed-`N` covector rays |
| Preparation-relative canonical response germ | `thm:canonical-response-germ` | Pairwise fixed-preparation expansion and uniform derivative limit |
| Selected weighted connection conormal | `thm:weighted-connection-jet`, `thm:structural-ball-connection`, `cor:schur-full-conormal`, `thm:joint-redistribution-conormal` | Both models raywise; shared-resource full structural ball under an admissible rule; cokernel-valued jet; pairwise preparation-independent limiting conormal; fixed-chart covariance with the front-face qualification for chart families |
| Physical-identification interface | `prop:physical-weighted-c1-transfer` | Weighted `C^1` root criterion, gap-level sufficient conditions, and conditional section/defining-function naturality; no physical root existence is asserted |
| Critical-layer precursor | `prop:unprepared-outer-skeleton` | Preparation-independent constant-history critical curve and dimension-uniform leading frozen-resource fast-voltage splitting |
| Positive-`delta` frozen voltage histories | `prop:frozen-voltage-history-splitting`, `rem:frozen-resource-phase-quotient` | Capped-rate full-history stability/splitting for the frozen-resource voltage RFDE, uniform structural `C^2` bounds, and an exact obstruction to the raw full-system one-unstable formulation; no nonautonomous slow tracker |
| Exact tracker/quotient interface | `prop:exact-outer-history-equation`, `prop:physical-history-phase-quotient`, `prop:exact-resource-gauge-quotient` | Uncut if-and-only-if tracker equation; genuine transported longitudinal history; exact stationary-gauge quotient; resource-gauge triangularization and $O(S_\delta^{-1})$ Volterra realization. Conditional on tracker existence and collar bounds; no tracker or dichotomy existence claim |
| Physical backtrack calculus | `prop:physical-backtrack-calculus` | Uniform weighted derivatives of the state-dependent physical delay map and the joint delayed composition/difference through three Fr\'{e}chet derivatives; raw backtrack variations are $O(\delta)$ and their relative contribution is $O(S_\delta^{-1})$ on the logarithmic collar, uniformly in $N$ and $\delta$ |
| Principal endpoint Green splitting | `prop:principal-tracker-endpoint-green` | Exact cancellation coordinate $\mathfrak p=\delta^2Q+\ell_NZ$; dimension-uniform slow right inverse, mixed repelling endpoint lift, action-weighted boundary layers, and sharp one-derivative loss in $Q$. Finite endpoint traces only: no compatible complete-history collar lift or nonlinear tracker |
| Exact nonlinear tracker normal form | `prop:nonlinear-resource-defect-normal-form` | The cancellation coordinate is exactly the physical resource defect $\mathfrak p_{\rm nl}=w_{\rm seed}-w$; exact nonlinear $(Z,\mathfrak p_{\rm nl},Q)$ identities, full Fr\'{e}chet differential, and a local dimension-uniform $C^0$ speed coordinate. No nonlinear tracker fixed point is asserted |
| Raw-compatible endpoint collars | `prop:compatible-endpoint-jet-collar`, `prop:endpoint-scale-not-slow-speed` | Dimension-uniform Hermite endpoint-jet chart satisfying the raw RFDE compatibility recursion; exact resource-defect/speed/backtrack bridge and fixed-history parameter jets, with no extra Fredholm row. The chart is not a Green right inverse, and a sharp scalar boundary layer proves that finite endpoint scale does not control the slow-speed norm |
| Exact fold-time tracker interface | `prop:fold-time-tracker-normal-form` | Direct fixed-delay $(r,Z,\mathfrak p_{\rm nl})$ normal form exactly equivalent to the raw fold-time RFDE; algebraic speed reconstruction and explicit compatible-collar initial-history map. Reparameterization is conditional on nonvanishing speed and makes no past-orbit claim for arbitrary old histories; no mixed-buffer BVP existence is asserted |
| Fixed-phase prescribed-history Green inverse | `prop:fixed-phase-green-collar-buffer` | Dimension-uniform fixed-parameter $C^0$ inverse for the $(Z,p)$ normal block with a prescribed old RFDE voltage-history segment, boundary traces $(Z(0),p(0))$ on the attracting branch or $(Z(0),p(S_r))$ on the repelling branch, and compatible $p(0)$-to-collar feedback. No backward RFDE is used. No high-order slow inverse, phase/event border, speed sign, tracker, or parameter jet is asserted |
| Scaled phase--event core | `prop:scaled-phase-event-core` | Explicit dimension-uniform inverse for the scalar collective phase equation with entry phase and terminal event rows, using the sharp scaled event-time variable $\widehat\tau=\delta\Delta S$. It proves the unscaled $\delta^{-1}$ loss and persistence of any net phase shift after compact speed forcing. The coupled phase--normal inverse and nonlinear moving-event chart are not asserted |
| Normal-to-phase action coupling | `prop:normal-to-phase-action-coupling` | The algebraically reconstructed speed of the normalized fixed-phase normal block, including endpoint/collar boundary layers, maps into $\mathsf H_\phi^0$ with norm $O(r_{\rm out}^2+\delta^{2-2\vartheta})$ and therefore produces a small bordered phase response. No higher phase-source jet, phase-to-normal column, moving-event column, or full coupled inverse is asserted |
| Formal delayed phase core and reverse column | `lem:reduced-flow-phase-defect`, `prop:delayed-phase-event-core` | Exact complete-history phase-delay differential, exact annihilation of constant phase, an $O(\delta[1+\log(r_{\rm out}/\rho_\delta)])$ action bound, and a dimension-uniform delayed scalar phase inverse. The two phase-induced normal sources are identified exactly, including the affine-residual derivative. The collar is the formal $q_0$-flow collar; no raw-compatible collar identification, affine-residual solution bound, or full Schur inverse is asserted |
| Event-aligned normal traces | `prop:event-aligned-normal-traces` | Exact triangularization of raw moving terminal traces by a fixed-$r$ quotient; the scaled event-time unknown disappears from homogeneous normal rows, and the reduced-base trace column is zero. A terminal-relative translation conjugacy preserves fixed-base kernel bounds. Raw trace differentiation instead costs one derivative and a sharp $\delta^{-2}$ strong-norm factor. No moving-family flushing or nonlinear tracker is asserted |
| Shifted phase-to-normal action response | `prop:phase-delay-action-shift`, `prop:structured-phase-action-green` | Exact shift $p^\sharp=p+\varepsilon P$, structured bulk sources including the affine-residual derivative, shifted attracting and repelling boundary rows, and dimension-uniform true-action bound $O(r_{\rm out}^2+\delta/S_\delta)$. The old normalized-state reverse column is explicitly not uniformly bounded |
| Raw-compatible zeroth-order phase--normal border | `lem:raw-phase-boundary-column-assembly`, `thm:raw-compatible-phase-normal-inverse` | Exact boundary column $E_0a\,\gamma_e^{\rm ph}$, repelling closed $p(0)$ feedback and shifted terminal row, total action $O(r_{\rm out}^2+\delta/S_\delta+\delta^{2-2\vartheta})$, and a dimension-uniform Schur inverse for $x=T_\sigma^{\rm rc}a+y$ in the graph norm controlling the normal operator domain, $a$, and the scaled event time. Fixed reduced base and order zero only; no higher jets, moving nonlinear family, tracker, speed sign, past orbit, or physical root |
| Attracting finite-generation flushing | `lem:current-absorbed-delay-splitting`, `prop:attracting-finite-generation-flushing` | Exact deletion of zero-delay differences, current absorption for positive delays, a fixed seam-partition Banach space, and an order-dependent finite-generation estimate taking arbitrary strong attracting collar data to a genuine slow exit history with dimension-uniform normalized operator norm tending to zero. Fixed parameter only; no phase coupling, tracker, or parameter jet |
| Repelling component-kernel flushing | `lem:repelling-component-generations`, `prop:repelling-component-flushing` | Weighted full-branch coefficient jets; a resummed current loop with forward transverse and future scalar kernels; exact recursive-delay generation count on one additive seam space; and inner-history/terminal-scalar handoff estimates obtained by oriented words and a localized terminal first-exit action. The normalized component traces tend to zero uniformly in network size. Fixed parameter and fixed phase only: no high-order compatible `p(0)`-collar feedback, coupled phase--normal inverse, nonlinear tracker, speed sign, or physical root |
| Compatible repelling-collar closure | `prop:compatible-repelling-collar-closure` | High-order closure of the raw-compatible scalar $p(0)$-to-history feedback, with no extra Fredholm row; separate closed-loop collar and terminal columns; and a cross-column action/generation estimate preserving both normalized handoff limits uniformly in network size. Fixed parameter and fixed phase only; no phase-to-normal/event border, nonlinear tracker, speed sign, or physical root |
| Truncated reduced actions | `cor:outer-reduced-actions` | Formal critical-curve speed and two positive truncated actions for the reduced critical-layer equation; not an invariant slow-history action |
| Weak-selection obstruction | `prop:backward-asymptotic-nonselection` | A common phase row, convergence in an unnormalized history norm, and superalgebraic strong-history closeness do not by themselves select a unique tame RFDE history family; generic logical counterexample, not a model-specific impossibility theorem |
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

- The principal contribution is the conjunction of exact atomwise projection blindness,
  pure-redistribution control of every transverse source by two separated
  delays, sharp `N`-uniform inverse bounds, and nonlinear complete-history
  root readout.
- Schur elimination, one-dimensional cokernel projection, and recovery of a
  finite-dimensional functional from a right inverse are standard operations
  and are not priority claims.
- The observation theorem reconstructs the compressed return covector for a
  known network skeleton.  It does not reconstruct the hidden network.
- Pairing estimates are uniform over the unit probe ball under the compatible
  base-layer and common preparation hypotheses stated in the corresponding
  corollaries.  Coordinate recovery
  from finitely many noisy probes is not `N`-uniform without a lower frame
  bound, and root measurement noise is amplified by
  `delta^(-3)|zeta|^(-1)`.
- The weighted conormal is a geometric realization of the proved selected
  response, not a novelty claim for conormal or Melnikov geometry in
  isolation.  The paper's principal conjunction remains exact projection blindness,
  transverse return, sharp two-delay recovery, and `N`-uniform nonlinear
  realization.

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
- The conormal theorem concerns selected complete-history connection loci
  centered at their own baselines.  A preparation-free physical connection
  locus and selected-to-physical weighted `C^1` identification remain open
  under Issue #32.  Issue #11 concerns a different Paper III model and is not
  an input to Paper A.
- The preparation-independent critical curve, frozen-resource
  positive-`delta` voltage-history splitting, truncated reduced actions,
  exact tracker/quotient identities, physical-backtrack calculus, and
  principal finite-endpoint Green splitting are proved precursors.  The exact
  nonlinear resource-defect normal form and raw-compatible endpoint collar
  chart are also proved.  The quotient identities assume an exact tracker,
  while the collar chart is not a right inverse for arbitrary Green sources;
  a proved boundary-layer obstruction forces a hybrid slow/action coupling
  on a finite method-of-steps buffer.  The exact fixed-delay fold-time normal
  form now identifies the correct system and collar interface for that
  coupling.  Its fixed-phase `C^0` complete-history Green inverse is proved,
  including the repelling collar feedback without an extra row.  The
  separately bordered scalar phase--event core is also explicit.  The
  attracting and repelling high-order finite-generation component buffers
  are now proved, including the repelling scalar-terminal first-exit
  localization.  The high-order compatible `p(0)`-collar feedback is now
  closed, and the normalized normal-to-phase action column is
  $O(r_{\rm out}^2+\delta^{2-2\vartheta})$.  The exact formal reverse
  phase-delay column, its scalar delayed inverse, and fixed-`r`
  event-aligned normal trace are also proved.  The exact phase-delay shift
  and structured action estimate are now proved.  The raw-compatible collar
  is assembled as a boundary column, the affine-residual bulk response is
  controlled in the shifted/action space, and their combination closes the
  fixed-reduced-base zeroth-order phase--normal inverse in a graph norm.
  This does not give a uniform inverse in the old normalized state norm,
  higher phase or parameter jets, a moving nonlinear tracker, speed sign, a
  past physical history, or a physical root.  These results do not yet
  construct an RFDE tracker or prove its normal dichotomy.  The generic
  nonselection example is a logical
  counterexample to weak selection criteria, not a model-specific
  impossibility theorem; tracker existence, quotient roughness, and all of
  G1 remain open.
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
