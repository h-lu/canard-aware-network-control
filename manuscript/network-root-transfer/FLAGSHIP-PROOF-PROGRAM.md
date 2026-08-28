# Flagship proof program: two-delay hidden-return identification

This document records the flagship upgrade associated with Issue #31.  The
obstruction theorem, canonical germ, abstract Schur theorem, sharp two-delay
source theorem, finite-scale covector recovery, sparse topology, and
sensed-recovery model have now been inserted in the manuscript.  Items
below retain the design history; the final checklist records the current
verification state.

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
- [ ] Import or prove the preparation-free physical outer-history relation
      owned by Issue #11.
- [ ] Prove weighted `C^1` selected-to-physical identification.
- [ ] Prove a nontrivial passage-jet composition law beyond the exact-holonomy
      re-cutting naturality already contained in the transfer proposition, or
      another reusable consequence.

Completing the five checked items does not close Issue #32 and does not
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
