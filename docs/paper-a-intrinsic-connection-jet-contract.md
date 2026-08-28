# Paper A: weighted complete-history connection conormal

Status: **the selected-connection front-face theorem is supported by the
current estimates; the exact nonlinear tracker normal form and a
raw-compatible endpoint collar chart are now proved, but their hybrid Green
coupling, the physical tracker, and the physical identification gate remain
open.  The exact fixed-delay fold-time formulation now identifies the
correct remaining coupling.**

This note tracks
[Issue #32](https://github.com/h-lu/canard-aware-network-control/issues/32).
It separates the geometric theorem that follows from the present Paper A
proof from the new outer-history theorem required for an intrinsic physical
maximal canard.  It is a proof contract, not a source of additional claims.

## 1. Contribution map

The current paper proves, for each fixed admissible preparation, a selected
complete-history connection root and the response law

```text
exact projection blindness
    -> transverse delay-moment source
    -> stable complete-history lift
    -> collective cokernel return
    -> selected nonlinear root response.
```

For the shared-resource family, it also proves that admissible changes of the
artificial outer completion can move the exact finite-`delta` root.  The
strongest geometric object already
supported is therefore not that root.  It is the limiting conormal of the
baseline-centered, weighted selected-connection loci.

The desired flagship bridge is longer:

```text
physical attracting/repelling complete-history objects
    -> preparation-free connection locus
    -> weighted front-face conormal
    -> identification with the hidden-return Schur covector Lambda_N
    -> two-delay recovery and N-uniform consequences.
```

The first arrow must be proved for the shared-resource Markov class inside
this project.  [Issue #11](https://github.com/h-lu/canard-aware-network-control/issues/11)
concerns a different two-module leaky model and cannot be imported as a
Paper A theorem.  Issue #32 therefore owns both the Paper A physical-history
construction and the subsequent front-face identification.

## 2. The selected connection locus that is already proved

Fix a preparation `p`, a network size `N`, and a structural ray `zeta R_N`.
Let

```text
C^p_(N,delta)(R_N)
 = {(nu,zeta): the two selected complete RFDE histories agree}.
```

The zero-fiber theorem and the uniform implicit-function theorem make this a
local `C^2` curve.  Center it at its own unperturbed baseline and use the
weighted parameter

```text
nu_b,N^p(delta) = nu_c,N^p(delta,0),
xi = delta^(-1) (nu-nu_b,N^p(delta))
   = delta^(-3) (mu-mu_c,N^p(delta,0)).
```

Writing its graph as `xi = Xi^p_(N,delta)(zeta)`, the proved root estimates
give

```text
|Xi^p_(N,delta)(zeta) - zeta Lambda_N(R_N)|
    <= C_p (delta |zeta| + zeta^2),

|D_zeta Xi^p_(N,delta)(zeta) - Lambda_N(R_N)|
    <= C_p (delta + |zeta|),

|D_zeta^2 Xi^p_(N,delta)(zeta)| <= C_p.
```

The constants are uniform in `N` for a uniformly bounded direction family
and one fixed preparation.  For two fixed preparations the limiting first
jet is the same after each curve is centered at its own baseline; there is no
single remainder constant over the whole preparation class.

Consequently the \(d\xi\)-calibrated conormal line at the selected baseline,

```text
span{d xi - D_zeta Xi^p_(N,delta)(0) d zeta},
```

converges uniformly in `N` to

```text
span{d xi - Lambda_N(R_N) d zeta}.
```

This is a weighted normal jet of a selected complete-history connection
relation.  It is not yet the conormal of a preparation-free physical
connection locus.

## 3. Cokernel-valued formulation

The scalar-representative-free linear object, relative to the fixed matching
data and collective/transverse splitting, lives in the one-dimensional
collective cokernel.  With

```text
K_N(R) = [B_N L_perp,N^(-1) S_N R]
         in coker L_parallel,N,
```

define

```text
J_N(xi,R) = xi [f_nu,N] + K_N(R).
```

The hidden-return theorem gives

```text
ker J_N = {(Lambda_N(R),R): R in T_N}.
```

Thus `ker J_N` is the limiting tangent hyperplane, and its annihilator is the
limiting conormal line after a physical parameter calibration is fixed.  This
formulation is unchanged by:

- rescaling a scalar cokernel functional;
- adding a collective range term;
- the block-preserving transverse coordinate changes already admitted in the
  Schur theorem;
- replacing a regular scalar defining function of the same connection locus
  by another one.

At finite `delta`, under a parameter chart change the conormal pulls back by
the derivative of the chart.  The limiting weighted jet is covariant for a
fixed nonsingular chart, or for a chart family whose derivative and inverse
derivative converge uniformly to a nonsingular front-face derivative.
Singular `delta`-dependent rescalings can alter the limit and are excluded.

## 4. What is still needed for the physical theorem

For the shared-resource Markov RFDE, the unprepared critical curve, leading
frozen-voltage splitting, and two positive formal truncated reduced actions are
now proved in Proposition `prop:unprepared-outer-skeleton`.  Proposition
`prop:frozen-voltage-history-splitting` upgrades the voltage layer to a
positive-`delta`, capped-rate splitting on the fixed full-history space,
uniformly in network size and twice Frechet in the structural layer tuple.
It freezes the resource and does not construct a slow tracker.  Supplementary
Proposition `prop:backward-asymptotic-nonselection` proves that bounded
complete backward extension, convergence in an unnormalized history norm,
and even superalgebraic strong-history closeness do not select a unique tame
history jet.  Proposition `prop:physical-history-phase-quotient` now proves
one exact bridge: once a monotone physical history exists, its time tangent
has a stationary-gauge normalization and the projected variational evolution
is an exact representation of the intrinsic quotient cocycle.  Proposition
`prop:exact-outer-history-equation` proves the uncut if-and-only-if
invariance equation for such a history.  Proposition
`prop:exact-resource-gauge-quotient` then removes the apparently large
resource coupling exactly and conjugates the quotient to a standard voltage
RFDE with an `O(S_delta^(-1))` Volterra correction in the adapted norm.
Proposition `prop:nonlinear-resource-defect-normal-form` now upgrades the
principal cancellation to the exact physical resource defect and proves a
local `C^0` speed coordinate.  Proposition
`prop:compatible-endpoint-jet-collar` constructs the raw-compatible
endpoint-history chart and exact `p_e`-to-speed/backtrack bridge without an
extra Fredholm row.  Proposition `prop:endpoint-scale-not-slow-speed` proves
that this chart cannot simply be attached to the finite endpoint Green
theorem: a hybrid slow/action estimate on a finite method-of-steps buffer is
necessary.  A single maximal delay clears direct old-history evaluations but
does not erase their generated narrow echoes.
Proposition `prop:fold-time-tracker-normal-form` then proves the exact
fixed-delay system in which that buffer must be constructed, including its
direct equivalence with the raw RFDE and the collar initial-history
interface.  It does not prove the mixed buffer estimate or tracker
existence.
These results still neither construct the tracker nor prove a dichotomy for
the quotient.  The following
finite-`delta` items remain unproved uniformly in `N`:

1. a phase-quotiented, nonautonomous outer normal splitting along a true
   positive-`delta` slow tracker; the raw voltage--resource one-unstable
   formulation is false in an admissible homogeneous subclass;
2. a parameter-coherent
   `J_phys=(C^1_nu C^2_eta) intersect (C^2_nu C^1_eta)` attracting
   representative and repelling codimension-one history sheet;
3. the finite-`delta` resource correction needed for entry into the receding
   logarithmic fold chart, with all delayed
   backtracks contained in the physical tube;
4. exact common-history-graph overlap, rather than current-state or
   exponentially close shadowing;
5. a physical connection gap with the same weighted `C^1` jet as the selected
   Lin gap;
6. construction and verification of physical section holonomy, plus a
   nontrivial passage-jet composition law beyond exact-holonomy re-cutting.

The proved exact curve equation and quotient identities, together with the
correct mixed boundary geometry and next dichotomy estimates, are tracked in
[`paper-a-physical-outer-history-route.md`](paper-a-physical-outer-history-route.md).
The concrete two-unknown tracker system, principal block operator, mixed
Green boundary conditions, admissible raw endpoint gauges, flat-equivalence
estimate, and exact physical membership gap are fixed in
[`paper-a-tracker-bvp-proof-program.md`](paper-a-tracker-bvp-proof-program.md).
The remaining tracker/dichotomy construction there is a proof design, not an
additional manuscript claim.

The frozen-voltage part of G0 is closed.  The phase quotient, true slow
tracker, and nonautonomous roughness part of G0, as well as G1, remain open.
The generic nonselection example is not a model-specific impossibility
theorem for the shared-resource RFDE.

## 5. Stop/go rules

The following changes count as progress but do **not** close Issue #32:

- inserting the selected weighted-conormal theorem;
- rewriting the Schur quotient as the cokernel-valued jet `J_N`;
- proving defining-function and parameter-coordinate covariance;
- giving a conditional theorem that transfers a physical gap once a weighted
  `C^1` comparison has been proved.

Issue #32 closes only after a connection relation is defined independently of
the preparation and its weighted conormal is identified with `Lambda_N`.

Do not:

- rename the current selected gap a physical transition map;
- call the exact selected root a maximal canard;
- prescribe a preferred artificial cutoff and call it dynamical canonicity;
- use the term `scattering map` without normally hyperbolic invariant
  manifolds, wave maps, and a genuine homoclinic or heteroclinic channel;
- infer a biological threshold or basin separator.

## 6. Implementation stages

- [x] Audit the repository for a completed physical outer-history theorem.
- [x] Record the selected weighted connection locus and cokernel jet.
- [x] Insert and prove the selected weighted-conormal theorem in Paper A.
- [x] Upgrade the raywise structural response to a joint Frechet theorem.
- [x] State the physical weighted-`C^1` transfer theorem with exact
      hypotheses and no implied existence.
- [x] Prove the unprepared outer critical curve, leading frozen-voltage
      splitting, and positive formal truncated reduced actions.
- [x] Prove the positive-`delta` frozen-resource voltage full-history
      splitting with a capped rate, and isolate the raw full-system
      two-unstable obstruction.
- [x] Prove that bounded backward convergence in an unnormalized history norm
      and superalgebraic history closeness do not select a unique tame
      parameterized history.
- [x] Prove the exact stationary-coordinate phase quotient conditional only
      on existence of a genuine monotone physical history.
- [x] Prove the exact uncut outer-history equation, genuine longitudinal
      cocycle, resource-gauge quotient, and Volterra history conjugacy.
- [x] Prove weighted third-order calculus for the state-dependent physical
      backtrack and delayed composition, sufficient for the rectangular
      `J_phys` jet and with relative loss `O(S_delta^(-1))`.
- [x] Prove the principal finite-endpoint Green splitting with the exact
      cancellation coordinate, mixed repelling orientation, action-weighted
      boundary lifts, and sharp regularity loss.
- [x] Prove the exact nonlinear resource-defect normal form and local `C^0`
      speed reconstruction.
- [x] Construct the raw-compatible endpoint-history collar chart with its
      exact speed/backtrack bridge, and prove the finite-endpoint slow-speed
      obstruction.
- [x] Prove the exact fixed-delay fold-time tracker normal form and direct
      collar-to-initial-history interface.
- [ ] Prove the fixed-delay mixed first-buffer inverse, buffer-to-slow
      bootstrap, and close the nonlinear outer tracker.
- [ ] Prove the phase-quotiented nonautonomous normal splitting, mixed
      outer-history Lyapunov--Perron construction, and exact fold-graph
      overlap for Paper A.
- [ ] Identify the physical front-face conormal with `Lambda_N`.
- [ ] Prove a nontrivial passage-jet composition law beyond the conditional
      exact-holonomy re-cutting naturality already proved, or another genuinely
      reusable consequence.
- [ ] Retitle and rewrite the abstract to advertise a physical/intrinsic
      connection only after the physical identification is proved; the
      present selected-conormal description is allowed.
