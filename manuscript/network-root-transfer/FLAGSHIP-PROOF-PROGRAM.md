# Flagship proof program: two-delay hidden-return identification

This document records the flagship upgrade associated with Issue #31.  The
obstruction theorem, canonical germ, abstract Schur theorem, sharp two-delay
source theorem, finite-scale covector recovery, sparse topology, and
sensed-recovery model have now been inserted in the manuscript.  Items
below retain the design history; the final checklist records the current
verification state.

The separate physical-history implementation under Issue #32 now has a fixed
mixed-BVP and representative-class contract in
[`../../docs/paper-a-tracker-bvp-proof-program.md`](../../docs/paper-a-tracker-bvp-proof-program.md).
That contract concerns the still-open terminal-to-terminal family; the
raw-gauge fixed-section zero family and its pointwise generated-interior
tracker statement, together with the fixed-interior weak-C1 physical-section
hit maps and their common time-\(C_\delta^3\), gauge-\(C^1\) strong
generated buffers, are now proved separately.  On those local buffers, the
exact quotient also has a finite-window RFDE Lyapunov--Perron flushing
estimate.  A fixed-reference rough residual now gives parameter-coherent
local hit families, and differentiation on one centered fading space proves
full rectangular-jet raw-gauge equivalence modulo
\(O(\delta^\infty)\) in the normalized event norm.  These classes remain
relative to one reference chart and two separate interior sections; they do
not supply the terminal-to-terminal physical relation.  The scalar
endpoint-recut obstruction now proves that the inner-anchored estimates,
strict speed sign, and interior windows alone cannot be promoted to the
original endpoints by literal recutting.  The exact scalar replacement is
now proved: on the receding collar
\(r_{{\rm out},\delta}=\varkappa_{\rm ep}(\delta S_\delta^3)^{1/2}\),
the prescribed Eulerian flight-time phase gives a causal scalar-coordinate
hit at the original endpoint, \(O(S_\delta)\) duration correction, and a
normalized scalar terminal Schur inverse.  Every prescribed structured
reference-coordinate source in the stated class is now exactly conjugated
to that Eulerian endpoint problem, and the
fixed-reference raw-compatible phase--normal graph inverse is uniform at
order zero on the same diagonal.  The moving-duration normal column,
arbitrary-source strong-terminal inverse, and full terminal Schur factor
remain open, including proof that their generated source belongs to the
structured class.

## 1. Exact selection cannot be intrinsic under the present hypotheses

The current theorem fixes an admissible preparation
`p = (P_gr,P_pl)`.  Two distinct choices enter the selected root.

1. `P_gr` completes the planar backward flow used in the Lyapunov--Perron
   formula for the invariant history graph.  The physical and prepared fields
   agree on the retained depth-two hull, but the exact global fixed point is
   not asserted to be independent of the completion.
2. `P_pl` supplies the two outer planar strips.  The condition
   `H_alpha = 0` is an endpoint normalization, not membership in a physical
   attracting or repelling slow manifold.  The resulting outer pieces are
   explicitly selection devices.

Consequently the local RFDE and the current preparation axioms do not specify
an exact finite-`delta` connection.  An intrinsic maximal canard would require
additional, physical outer data: for example, uniquely selected invariant
manifolds with asymptotic boundary conditions, together with a proof that
their complete-history intersection enters the retained chart.

### Obstruction proposition implemented

Let `P` be the class of admissible preparations for one fixed physical RFDE.
For each sufficiently small fixed `delta`, there exist `p_0,p_1 in P`, equal
on the entire required physical agreement hull, for which the corresponding
locally unique baseline roots are different.

Implemented proof mechanism:

- perturb `P_pl` by a small parameter-independent smooth vector-field bump
  supported strictly inside one outer preparation strip;
- use the already proved trace--phase--endpoint isomorphism to differentiate
  the selected trace with respect to the bump amplitude;
- choose the bump so that its image under the nonzero scalar endpoint-to-gap
  functional is nonzero;
- divide by the already proved nonzero `nu`-slope of the gap.

This proves a no-go statement for exact preparation independence under
the present axioms.  It would not rule out an intrinsic canard after physical
outer invariant manifolds are added.

## 2. Canonical response germ supported by the current estimates

For a fixed admissible preparation `p`, write

```text
Delta_mu[p,N](delta,zeta)
  = mu_c[p,N](delta,zeta) - mu_c[p,N](delta,0).
```

Let `G_N` be the space of continuous two-variable germs on
`0 < delta < delta_0`, `|zeta| < zeta_0` which vanish at `zeta=0`, with
constants uniform in `N`.  Define the response-negligible ideal

```text
J_N = { r : |r(delta,zeta)|
              <= C (delta^4 |zeta| + delta^3 zeta^2) }.
```

The current main theorem and two-preparation comparison already imply

```text
[Delta_mu[p,N]] in G_N/J_N
       = [ C_N delta^3 zeta ],
```

independently of every fixed admissible preparation.  Equivalently,

```text
Resp_N(R)
  := lim_(delta -> 0+) delta^(-3)
       partial_zeta mu_c[p,N](delta,0)
   = Lambda_N(R),
```

and the convergence is uniform in `N` for any family with common preparation
bounds.  This quotient germ/covector, rather than the exact selected root, is
the relative-canonical selected object already supported by the proof, with
the physical family, projection, matching data, and parameter normalization
fixed.

### Quantifier boundary retained

- the preparation comparison is pairwise for any two fixed admissible data on
  their common parameter box; the remainder constant may depend on that pair,
  so no uniform estimate over the whole preparation class is asserted;
- distinguish pairwise preparation independence from uniformity over the
  whole class;
- decide whether to use a fixed algebraic quotient as above or a flat-germ
  quotient obtained from a super-Gaussian receding section;
- if the flat-germ formulation is used, replace
  `S_delta = sqrt(2 p log(1/delta))` by a scale such as
  `S_delta = log(1/delta)^(3/4)` and recheck every graph, trace, and tail
  estimate.  This scale satisfies

```text
delta exp(c S_delta) S_delta^m -> 0,
exp(-S_delta^2/2 + c S_delta) S_delta^m = O(delta^q)
```

for every fixed `c,m,q`.

The fixed algebraic quotient is the conservative theorem.  The flat-germ
version is stronger and must not be claimed until the preparation-difference
estimates, not merely the individual tail estimates, have been proved.

## 3. Abstract hidden-return theorem

The present range-to-root theorem assumes the structural gap derivative and
therefore does not derive the hidden-return mechanism.  The replacement
should have the following Schur-complement form.

Let a family of matching problems have collective and stable transverse
spaces `C_N` and `E_N`, output projection `Pi_N`, structural direction space
`T_N`, and a complete-history lift `I_N,eta`.  Assume:

1. **Exact blindness:** `Pi_N F_N,eta = Pi_N F_N,0` on the full history
   domain for every admitted `eta`.
2. **Transverse solvability:** the differentiated history-graph equation has
   a uniformly invertible transverse operator `L_perp,N` and source map
   `S_N:T_N -> Y_perp,N`.
3. **Return map:** differentiating the projected unperturbed field with
   respect to the transverse history defines a bounded map
   `B_N:X_perp,N -> Y_c,N`.
4. **Matching cokernel:** the collective matching operator has normalized
   cokernel `ell_N`, and the matching parameter has coefficient
   `a_N = ell_N f_nu,N` with `inf_N |a_N| > 0`.
5. **Uniform range and remainder estimates:** the graph, traces, phase rows,
   finite-section tails, and second derivatives satisfy the uniform bounds
   needed to pass from the linear response to the actual root.

Then the direct structural term vanishes by exact blindness, while the lift
changes by

```text
h_N(R) = L_perp,N^(-1) S_N R.
```

The effective collective forcing and root-response covector are

```text
f_hidden,N(R) = B_N h_N(R),
b_N(R) = ell_N B_N L_perp,N^(-1) S_N R,
Lambda_N(R) = -b_N(R)/a_N.
```

The root increment has the appropriate scaled leading term
`Lambda_N(R) delta^(q+1) eta`.  If `Lambda_N` is nonzero on an admissible
finite-dimensional tangent space, its zero-response set is a codimension-one
hyperplane and its complement is open and dense.  Common operator bounds give
dimension-uniform response and remainder estimates.

The manuscript now proves the chain from exact blindness to the displayed
Schur complement.  The ordinary implicit-function step is only the final
bridge.  In the curvature-return model the dictionary is

```text
L_perp,N  -> A_N on the first stable graph jet,
S_N R     -> (K/(2 alpha)) P_perp,N dot(M_1,N) 1,
B_N h     -> mixed curvature term -2 X pi_N^T diag(c_N) h,
ell_N     -> Gaussian adjoint pairing,
a_N       -> sqrt(2 pi).
```

## 4. A sparse directed, high-rank network family

This family is designed to be genuinely different from the complete-mixing,
rank-one witness already in the paper while remaining inside the current
one-step Dobrushin hypothesis.

Fix `q in (0,1)`, put `rho = 1-q`, and let `S_N` be the cyclic forward
shift.  Define the reset-cycle Markov matrix

```text
P_N = rho S_N + q 1 e_1^T.
```

Each row has at most two nonzero entries, all rows share reset mass `q` in
column one, and

```text
tau(P_N) <= rho.
```

Its strictly positive stationary distribution is

```text
pi_(i,N) = q rho^(i-1)/(1-rho^N),  i=1,...,N.
```

Choose `0 < eta < 1/4` and

```text
f_(i,N) = (-1)^i + eta i/N,
m_N = pi_N^T f_N,
s_N = f_N - m_N 1,
c_N = 1 + sigma s_N
```

with `0 < sigma < (2+eta)^(-1)`.  The entries of `f_N`, hence of
`c_N`, are pairwise distinct, `pi_N^T c_N=1`, and

```text
Var_pi(c_N) = sigma^2 Var_pi(f_N)
            >= sigma^2 pi_(1,N) pi_(2,N)
                 (f_(1,N)-f_(2,N))^2
            >= 4 sigma^2 q^2 rho.
```

Take `theta_0=0<theta_1=theta`, put

```text
B_(0,N)=B_(1,N)=(I+P_N)/2,
Q_N=(P_N-I)diag(c_N),
R_(0,N)=lambda Q_N,
R_(1,N)=-lambda Q_N,
```

where `lambda` is nonzero.  Then

```text
pi_N^T R_(k,N)=0,
R_(0,N)+R_(1,N)=0,
dot(M_1,N) 1 = -theta lambda (P_N-I)c_N.
```

Since `A_N=D(P_N-I)|E_N`, the current response formula gives

```text
Lambda_N(R_N)
  = (K lambda theta/(2D)) Var_pi(c_N),
```

and hence

```text
|Lambda_N(R_N)|
  >= 2 |K lambda| theta sigma^2 q^2 rho/D.
```

The reset cycle is primitive, `diag(c_N)` is invertible, and therefore

```text
rank(Q_N)=rank(P_N-I)=N-1.
```

The support of `Q_N` is contained in that of `P_N+I`, and
`|Q_ij| <= c_+(P_ij+delta_ij)`.  Thus
`|zeta| < (2 |lambda| c_+)^(-1)` keeps both perturbed layers entrywise
nonnegative with the same sparse chosen-base-layer support.  The matrices have uniform operator
bounds in the stationary oscillation norm.  Pairwise distinct curvatures
destroy every nonsingleton synchrony polydiagonal by testing the vector field
on a fully synchronous constant history.  Moreover, with
`g_N=A_N^(-1)(c_N-1)`, the matched orbit satisfies an `N`-uniform
asynchrony lower bound because

```text
osc(c_N) <= D(1+rho) osc(g_N),
delta^(-2) P_perp,N v_c,N(-delta^(-1))
  = g_N/4 + O(delta).
```

### Verification points carried out before insertion

- audit the row convention for the stationary distribution;
- record an explicit uniform positivity radius for the perturbed layers;
- prove `rank(P_N-I)=N-1` from primitivity and verify that multiplication by
  `diag(c_N)` preserves the rank;
- verify the operator norm of multiplication by `c_N` in the manuscript's
  stationary oscillation norm;
- decide whether the family starts at `N=2` or `N=3` when advertising
  high-rank perturbations.

## 5. Completion gates

- [x] Reject exact preparation independence under the current axioms by an explicit outer
      bump argument.
- [x] State the canonical response germ/covector as a main theorem with the
      correct preparation-class quantifiers.
- [x] Add the hidden-return Schur
      complement theorem and a short root-transfer corollary.
- [x] Verify the sparse reset-cycle family line by line and insert it as a
      support-preserving high-rank application.
- [x] Verify a genuinely different sensed-recovery return channel, including
      the homogeneous-curvature pure-sensing limit.
- [x] Prove the two-delay blind source is onto with a sharp `N`-uniform right
      inverse and prove the merged one-delay no-go.
- [x] Prove coordinate-free dual reconstruction, finite-scale weighted pairing
      recovery, and the precise limitations of noisy finite-frame recovery.
- [x] Complete theorem-level comparison with exact lumpability/closure,
      Mori--Zwanzig memory, output identifiability, network canards, and RFDE
      Lin/Fredholm theory.
- [x] Change the title, abstract, introduction, and conclusion to foreground
      blind controllability and selected fold-response readout.
- [x] Split the proof ledgers into a cross-referenced supplementary PDF while
      retaining all theorem hypotheses and load-bearing mechanisms in the main
      article.
- [x] Complete the redesigned mechanism figure and final visual audit.
- [x] Complete fresh hostile proof audits of the graph-only retained-tube
      repair and sensed-recovery extension.
- [x] Complete fresh JNS and Nonlinearity desk simulations on the rebuilt PDF.
- [x] Record the work in logical commit batches and push the branch.

## 6. Weighted connection-conormal continuation

Issue #32 starts after the preceding gates.  The current estimates prove the
selected connection locus in

```text
xi = delta^(-3) (mu-mu_c^p(delta,0))
```

has limiting conormal `span{d xi-Lambda_N d zeta}`, and that its
cokernel-valued first-order connection/normal map, relative to the fixed
matching data, is

```text
J_N(xi,R) = xi [f_nu,N] + [B_N L_perp,N^(-1) S_N R].
```

This is a strict geometric consequence of the completed root theorem and is
pairwise preparation independent after separate baseline centering.  It is
not the conormal of an independently defined physical maximal-canard locus.

- [x] Prove the selected weighted connection-curve estimates and conormal
      convergence.
- [x] Identify the limiting hyperplane as `ker J_N` in the collective
      cokernel.
- [x] Record defining-function independence and parameter covariance for
      fixed nonsingular charts, with the front-face qualification for chart
      families.
- [x] Upgrade scalar structural rays to a joint Frechet theorem on a common
      perturbation ball.
- [x] State and prove a quantitative weighted-`C^1` selected-to-physical
      transfer criterion, including a gap-level sufficient condition.  This
      is an interface theorem and does not supply the physical histories.
- [x] Prove the preparation-independent critical curve, leading frozen-
      voltage splitting, and positive truncated reduced actions.
- [x] Upgrade the frozen voltage layer to a positive-`delta`, capped-rate
      full-history splitting and prove why the raw voltage--resource
      one-unstable formulation must be phase-quotiented.
- [x] Prove that convergence in an unnormalized history norm, even with a
      fixed phase row and superalgebraic strong-history closeness, does not
      select tame history jets by itself.
- [x] Derive the exact uncut tracker equation, genuine longitudinal history
      cocycle, stationary-coordinate quotient, and resource-gauge Volterra
      realization conditional on tracker existence.
- [x] Prove the physical-backtrack parameter calculus, principal
      finite-endpoint Green splitting, exact nonlinear resource-defect
      normal form, and raw-compatible endpoint-history collar chart.
- [x] Prove that finite endpoint resource-defect scale alone does not control
      the slow-speed class.
- [x] Prove the exact fixed-delay fold-time tracker normal form, direct raw
      RFDE equivalence, and compatible-collar initial-history interface.
- [x] Prove the fixed-phase `C^0` complete-history Green--collar inverse,
      including the repelling scalar feedback without an extra boundary row.
- [x] Prove the exact scaled scalar phase--event core, its sharp event-time
      scaling, and the persistence obstruction to phase echo contraction.
- [x] Prove the fixed-parameter high-order finite-generation
      buffer-to-slow component bootstrap on both branches, including the
      repelling forward-transverse/future-scalar kernel split and terminal
      first-exit sum.
- [x] Close the high-order compatible repelling p(0)-collar feedback and
      prove the zeroth-order normal-to-phase action estimate, including
      endpoint and collar boundary layers.
- [x] Derive the exact reduced-flow phase-delay defect, its constant-mode
      cancellation and zeroth-order action bound; invert the formal delayed
      phase--event core and identify both phase-induced normal sources.
- [x] Triangularize the scaled moving-event normal traces on fixed
      `r`-sections and prove the sharp `delta^(-2)` raw-translation loss.
- [x] Construct the terminal-relative nonlinear $C^2$ strong-to-weak
      moving-window coordinates at a nonzero base, including the derived
      fixed-section event row, nonzero terminal columns, mixed second
      derivatives, and sharp first/second translation losses.
- [x] Prove the exact phase-delay shift and old-state-norm obstruction,
      control the structured affine-residual response in true action, assemble
      the raw-compatible phase boundary column, and close the fixed-reduced-base
      zeroth-order graph/action phase--normal inverse.
- [x] Prove the vanishing $O(\varepsilon|e|)$ base raw-collar correction,
      construct the fold-side anchored nonlinear $q_0$-flow phase chart with
      a controlled scalar reduced-speed sign, and close its fixed-base
      one-row relative-phase Schur inverse.
- [x] Prove the relative $O(\delta)$ phase-delay profile, recover the
      returned normalized state and pointwise true action with factor
      $O(r_{\rm out}+S_\delta^{-1})$, and close the equivalent relative
      graph--action norm.
- [x] Prove the exact nonlinear phase-only delay remainder in the relative
      norm and its two-point Lipschitz estimate.
- [x] Construct a uniformly graph-tame $C^2$ raw-compatible old-history
      assembler, including the endpoint/collar second jet.
- [x] Prove a fixed-section nonlinear graph/action residual with a
      dimension-uniform quadratic remainder.
- [x] Solve the fixed-section residual by a dimension-uniform contraction,
      with canonical-slice uniqueness, first Newton jet, strict speed sign,
      and exact finite forward RFDE reconstruction on both outer branches.
- [x] Extend the zero-core solution to a nonempty, infinite-dimensional
      raw-compatible gauge ball on both branches, with uniform slice
      uniqueness, fixed-graph C1/Lipschitz dependence, first gauge jet,
      inverse persistence, strict speed sign, and exact raw-RFDE
      reconstruction.
- [x] Reparameterize every retained generated-interior subsegment of every
      raw-gauge zero whose delay collar lies beyond the first maximal delay as
      an exact tracker, and verify the uncut quotient and resource-gauge
      Volterra hypotheses there.
- [x] On a common generated buffer, construct the fixed interior
      physical-section hits at $r=\pm r_{\rm out}/2$, with joint weak-history
      C1 dependence, dimension-uniform scaled hit/history derivatives, and
      the exact stationary phase-quotient formula.
- [x] Upgrade the same interior neighborhoods to common
      time-$C_\delta^3$, gauge-C1 strong generated buffers with
      dimension-uniform annular bounds, an $O(\delta^{-1})$ fixed-reference
      chart enlargement, and the safe $O(\delta^{-2})$ moving-recut loss.
- [x] Prove RFDE-specific finite-window quotient flushing on each actual
      fixed physical-hit buffer, including the attracting left-boundary and
      repelling stable-left/one-dimensional-unstable-right estimates.
- [x] Convert that flushing through the exact resource/event quotient into
      $O(\delta^\infty)$ first-order raw-gauge equivalence of each complete
      fixed-section hit history in the normalized event norm.
- [x] Construct one fixed-reference rough residual and the parameter-coherent
      physical-hit family with the rectangular parameter jet, fixed-parameter
      $C_g^3$ jet, mixed $\mathcal K_{\rm phys}$ staircase, triangular time
      ledger, and complete-history event reconstruction.
- [x] Differentiate the centered local quotient and prove
      $\mathcal J_{\rm phys}$ raw-gauge equivalence for uniformly tame
      $(N,\delta,\sigma)$ gauge families, without a $D_g^4$ assumption.
- [x] Prove the scalar endpoint-recut nonimplication, including the
      wrong-sided outer endpoints and algebraic bordered fold-time scale
      exceeding every fixed $O(S_\delta)$ interior window.
- [x] Prove the exact Eulerian scalar causal-entry/terminal-event theorem
      on a receding outer collar, including the nonlinear flight-time
      moment, $O(\rho_\delta)$ duration, $O(S_\delta)$ fold-time window,
      analytic source map, and normalized scalar terminal Schur inverse.
- [x] Prove the exact reference-pulled/Eulerian endpoint conjugacy for every
      prescribed source in the stated structured class and the fixed-reference
      order-zero diagonal phase--normal inverse; expose the
      attracting evolution-kernel rate $cR_\delta/\delta$ through one
      endpoint derivative and one zeroth-order positive-delay Duhamel
      generation of size $\varepsilon/R_\delta$, together with the
      repelling outer-interval terminal scalar-kernel rate scale.
- [ ] Prove the moving-duration phase--normal terminal theorem and its
      action-weighted parameter/gauge jets at the original endpoints.  This
      requires a higher-order diagonal calculus, a hybrid arbitrary-source
      strong-terminal/weak-middle inverse, a structured/localized source
      split, raw-compatible endpoint histories, and the complete normal
      terminal column before the terminal-to-terminal nonlinear outer
      tracker.
- [ ] Prove the global action-weighted phase-quotiented normal splitting,
      mixed-boundary outer history construction, and fold-graph overlap for
      Paper A itself.
- [ ] Prove weighted `C^1` selected-to-physical identification.
- [ ] Prove a nontrivial passage-jet composition law beyond the exact-holonomy
      re-cutting naturality already contained in the transfer proposition, or
      another reusable consequence.

The frozen-voltage part of G0, the exact algebra of the quotient, fixed-phase
component flushing on both outer branches, repelling compatible feedback,
exact phase-delay shift, structured reverse action estimate, raw-compatible
boundary-column assembly, and fixed-reduced-base zeroth-order graph/action
phase--normal inverse are now closed.  The base collar correction vanishes
at the fold-side scale, and the inner-anchored nonlinear phase chart and
relative one-row Schur inverse remove the constant-phase obstruction to a
same-sign tube at the scalar phase/fixed-base linear level.  On the anchored
relative subspace, the exact delay profile now yields a uniform returned-state
bound and pointwise true action in an equivalent graph--action norm; the
unrestricted old-state obstruction remains.  The endpoint-recut obstruction
additionally proves that this scalar package permits wrong-sided original
endpoints and a formal bordered duration scale much longer than the local
hit buffers.  The receding-collar flight-time theorem now closes the exact
Eulerian scalar endpoint problem and its normalized terminal row; it also
shows that cancellation of only the linear duration moment is insufficient.
The reference-pulled theorem closes the scalar coordinate-conjugacy seam
for every prescribed structured source of the algebraic form used by the
RFDE phase row; it does not prove membership of the source generated by the
open moving RFDE BVP.  The fixed-reference order-zero normal/collar inverse
is now diagonal-uniform.  The next valid construction is its moving-duration
arbitrary-source strong-terminal extension and complete terminal column,
not transport of the interior chart.  The fixed-reference $C^2$
old-history assembler, including its endpoint/collar second jet and normalized
quadratic remainder, is now closed.  Its exact fixed-section assembly with the
nonlinear phase-delay and normal equations is also closed: the base defect is
$O(r_{\rm out}+S_\delta^{-2})$, the differential is the uniform anchored
Schur block, and the remainder is uniformly quadratic in two-point form.
Its pointwise fixed-parameter zero is now obtained by a uniform contraction
on each canonical outer graph slice, with a first Newton jet, strict speed
sign, and finite forward RFDE reconstruction.  This zero extends uniformly
to a nonempty, infinite-dimensional raw-compatible gauge ball, with a first
gauge jet and fixed-graph C1/Lipschitz dependence.  The sufficiently deep
generated interior of each gauge zero is now an exact physical-coordinate
tracker with the uncut quotient and Volterra realization.  The fixed interior
sections $r=\pm r_{\rm out}/2$ now also have common-buffer weak-history C1
hit maps with uniform scaled first gauge derivatives and the exact phase
quotient.  Their common strong buffers now support an RFDE-specific
finite-window quotient flushing argument, and each complete hit history is
first-order raw-gauge equivalent modulo $O(\delta^\infty)$ in the
normalized event norm.  The fixed-reference rough chart now upgrades this
local result to the full rectangular parameter jet and the exact mixed gauge
staircase, while retaining the pure parameter response of one representative.
This does not compare different reference charts, the full gauge-dependent
tracker domains, or the original endpoints.  The scalar terminal Schur row,
reference-coordinate conjugacy for every prescribed source in the stated
structured class, and fixed-reference diagonal order-zero inverse are now
closed, but the moving-duration full phase--normal terminal
estimate, the original-endpoint action-weighted parameter theorem, the full RFDE
moving-event residual/inverse, terminal-to-terminal nonlinear tracker
existence, global action-weighted quotient roughness, and the remaining
parts of G1 stay open.  The generic
nonselection example is not a model-specific impossibility theorem.
This zeroth-order border does not close Issue #32 and does not
authorize `physical maximal canard` or `scattering map` terminology.

### Editorial simulation snapshot

These are hostile internal screens, not acceptance predictions.  The second
JNS simulation rated the focused draft narrowly on the send side
(`55%` send / `45%` decline); its two desk-level requests---a concrete
scientific entry point and a formally explicit hypothesis block for the
flagship theorem---were then implemented.  The Nonlinearity simulation rated
it `42%` send / `58%` decline, chiefly because the measured object remains a
selected local response germ rather than a preparation-independent physical
maximal canard.  Both screens agreed that the exact-blindness--source--history-
return--nonlinear-readout chain is no longer a mere assembly of standard
tools.
