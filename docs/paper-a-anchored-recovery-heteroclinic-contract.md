# Paper A: anchored-recovery complete-history heteroclinic contract

Status: mathematical gates A0--A9 closed on 2026-08-31 in the main article
and supplement.  Editorial/release gate A10 remains open until the compact
main-paper rewrite, final tests, and PDF audit are complete.

## 1. Why we choose a globally anchored model class

For the original shared-resource law

```text
w_dot = delta^2 (pi_N^T v - 1 - delta^2 nu),
```

every equilibrium has outer coordinate

```text
r = pi_N^T(v-1) = delta^2 nu.
```

It therefore has no equilibrium on either outer branch used by the physical
tracker.  In the homogeneous delay-free admitted subclass, the collective
linearization at the near-fold equilibrium has characteristic polynomial

```text
lambda^2 - lambda_c(delta^2 nu) lambda + delta^2.
```

At the target canard scale `nu < 0`, this gives a two-dimensional real
unstable focus for small `delta`.  Convergence to that equilibrium in the
past, followed by one phase condition, leaves a one-parameter family and
does not select the repelling history.  Thus the results proved for the
original model do not yet supply the exact physical connection claimed in
Issue #32; additional global dynamical data are required.

This no-go is deliberately limited.  It does not exclude a separately proved
periodic or heteroclinic anchor, nor the possible construction of an incoming
half-line selected by a normalized `r -> +infinity` asymptotic condition for
the original global polynomial law.  No such theorem is presently available,
and it would not by itself select the repelling target.

The repair below is a new globally completed model class.  It is not a preferred
preparation and must never be described as proving an exact root for the
unmodified recovery law.

## 2. Anchored recovery law

Let

```text
r(v) = pi_N^T(v-1),        epsilon = delta^2,
```

and choose fixed radii

```text
0 < r_loc < r_A < r_0.
```

The anchor multiplier `a_anc` belongs to a fixed admissible model class with

```text
a_anc in C^12(R),
a_anc(r) = 1                         for |r| <= r_loc,
a_anc(r) > 0                         for -r_A < r < r_A,
a_anc(+/-r_A) = 0,
a_anc'(-r_A) > 0 > a_anc'(+r_A).
```

The class is fixed before any root is sought.  It has a common `C^12` bound,
common lower bounds on the two simple-zero slopes, and common positive lower
bounds on every fixed compact subannulus of `(-r_A,r_A)`.  A displayed smooth
cutoff supplies one explicit member, but no theorem is tied to that particular
interpolation.  All smallness thresholds and estimates are uniform over this
bounded class.

The zeros are crossed; `a_anc` is not frozen to zero outside the anchor
interval.  Replace only the recovery equation by

```text
w_dot = epsilon sigma_anc(r;nu),
sigma_anc(r;nu) = (r-epsilon nu) a_anc(r).
```

The voltage RFDE and every delay layer are unchanged.  On the entire retained
fold tube, including its depth-two delay hull, the anchored and original
physical equations agree literally once the common diagonal wedge is small
enough that all retained `r` values lie in `|r| < r_loc`.

Consequences that are exact rather than asymptotic:

1. stationary-projection blindness is unchanged;
2. the singular orbit, finite-section gap calculation, two-delay inverse,
   merged-delay no-go, and hidden-return covector `Lambda_N` are unchanged;
3. the constant critical histories

   ```text
   E_+ = (constant V_0,N(+r_A), w_0,N(+r_A)),
   E_- = (constant V_0,N(-r_A), w_0,N(-r_A))
   ```

   are equilibria for every structural redistribution, because every
   current-minus-delay term vanishes on a constant history and
   `sigma_anc(+/-r_A;nu)=0`.

## 3. Anchor spectrum and invariant manifolds

Put `s'_+ = partial_r sigma_anc(+r_A;nu)` and
`s'_- = partial_r sigma_anc(-r_A;nu)`.  Uniformly for
`|epsilon nu| < r_A/2`,

```text
s'_+ = (+r_A-epsilon nu) a_anc'(+r_A) < 0,
s'_- = (-r_A-epsilon nu) a_anc'(-r_A) < 0.
```

The critical-curve identity

```text
J_fv(r) V_0,N'(r) = w_0,N'(r) 1,
pi_N^T V_0,N'(r) = 1
```

gives one slow characteristic root at each anchor:

```text
lambda_s,+ = epsilon s'_+ / w_0,N'(+r_A) + O(epsilon^2) > 0,
lambda_s,- = epsilon s'_- / w_0,N'(-r_A) + O(epsilon^2) < 0.
```

The proof must use the full long-delay characteristic Schur complement

```text
A_+/-(lambda)
  = J_fv(+/-r_A)
    + epsilon K sum_k L_k(1-exp(-lambda theta_k/delta)),

Delta_+/-(lambda)
  = lambda
    + epsilon s'_+/- pi_N^T
        (lambda I-A_+/-(lambda))^{-1} 1,
```

together with the capped fading-space resolvent from the frozen-voltage
splitting.  A two-by-two current-state heuristic is not a proof because the
physical delays have length `theta_k/delta`.

The required exact root counts are:

```text
Morse index(E_+) = 1  (the slow root),
Morse index(E_-) = 1  (the strong voltage root).
```

Hence RFDE invariant-manifold theory gives a one-dimensional
`W^u(E_+)` and a codimension-one `W^s(E_-)`, with the full rectangular
parameter regularity and dimension-uniform charts established by the
resolvent proof.  The inward branch of `W^u(E_+)` is the unique
past-complete attracting history.  The repelling target is a future-complete
stable sheet, not an independently selected past-complete orbit.  At a
physical root their intersection produces one orbit complete in both time
directions.

## 4. Anchor collars, finite outer continuation, and capped forgetting

The local equilibrium manifolds must be continued through the actual raw
RFDE; no backward ambient RFDE semiflow may be invoked.  The anchor collars
are first constructed on the genuine long-delay phase space with the scaled
local radius

```text
rho_A,delta = c_A delta^4,       d_A,delta = rho_A,delta/2.
```

The local graph norms and their parameter derivatives may lose a fixed
polynomial power of `delta`.  The proof must expose that loss in the
Lyapunov--Perron contraction rather than claim a common unscaled spectral gap
or a fixed local radius.  In collar coordinates the exact slopes are

```text
chi_+,delta =  lambda_s,+ / delta^2,
chi_-,delta = -lambda_s,- / delta^2,
```

with the critical-curve quotients only as `O(delta^2)` approximations.  Delay
feet are obtained from the smooth local flow and remain regular at the anchor;
no division by the vanishing reduced speed is allowed.

Between the collar sections and the central tube, use fold time `s=delta t`
on the fixed history space `C([-theta_m,0];R^N)`.  The phase-normal map removes
the slow tangent by the nonvanishing resource component `w_0'(r)`, without a
`q^{-1}` quotient.  The attracting problem has left history data; the
repelling problem has left stable data and one right terminal stable-sheet
row.  Its inverse uses backward propagation only on the one-dimensional
unstable line.  The raw current-path variation-of-constants proof must treat
generated and prescribed old-history pieces separately and then reassemble
sliding histories.

The correct full-history forgetting envelope is

```text
f_delta = C delta^(-M)
          exp[-c_anc log(1/delta)/delta].
```

The generated current core may decay faster, but the stronger
`exp(-A/delta^2)` rate is not asserted for arbitrary continuous histories.
State and graph differences have the three value/first-parameter operators
`1`, `partial_nu`, and `D_eta`; normalized conormals have the same `C^1`
operators.  No second parameter derivative of the global passage is part of
the present closure.  The conormal estimate
comes from a dual row pullback with a separately proved nonzero normalization
denominator, not from primal history contraction alone.  A channel bootstrap
establishes all off-root events and delay feet before the gap is defined.

## 5. Exact anchored membership gap

Use the common central section `Sigma_0={X=0}` and an exact nonlinear tubular
chart `phi=C_0,p(psi,u)`.  Its `psi` variable contains the full
normal-history defect `h-H_p(z)` and all remaining compatible-history
coordinates, while

```text
u = c_mathscrH H_alpha(z(phi)),   c_mathscrH = 2/(alpha e).
```

The chart is `C^2` in state, `C^1` in the parameter, and holds `psi`
exactly fixed when `u` varies.  The infinite half-line problem first gives
an intrinsic entry graph `u_ent=F_ent^-(psi_ent)` and its exact membership
function `m_ent`.  Let `P_0toent,p` be the forward first-hit map along the
declared physical tube.  Define

```text
M_0,p(psi,u) = m_ent(P_0toent,p(C_0,p(psi,u))).
```

No inverse semiflow occurs.  The direct transported-column splitting proves
`|partial_u M_0,p| >= c_tr`; the central sheet is therefore the exact
forward preimage `u=F_0^-(psi)`.  Pair the physical incoming point with the unique stable-sheet
point having the same complete `psi` coordinate, and define the physical gap
directly as the normalized first-integral difference of their exact planar
images:

```text
G_phys = c_mathscrH [H_alpha(z_a(0))-H_alpha(z_r(0))].
```

The chart identity gives `G_phys=u_A-F_0^-(psi_A)` and
`partial_u G_phys=1` exactly.  Thus no curvature error from a linear tangent
fiber is hidden in the central normal defect, and no domain column is
identified with a cokernel row.  The zero fiber is equivalent to the exact
complete-history heteroclinic `E_+ -> E_-`.

The exact finite-gap identity retains the endpoint terms.  The endpoint
first-integral values, together with the two finite outer-strip integrals,
supply the missing Gaussian Melnikov tails.  Only the anchor-forgetting part
is bounded by `f_delta`; the endpoint values themselves are not flat.  The
remaining local algebraic errors must be estimated explicitly in the value,
`nu`, and `eta` derivative norms.  The finite derivative-loss exponent is fixed first;
only then is the cutoff exponent chosen large enough to absorb all losses.

No comparison with an unspecified preparation-selected gap, and no arbitrary
orientation multiplier, is used to manufacture the root.  The bracket,
parameter transversality, and hidden-return response follow directly from the
normalized finite-gap identity plus the endpoint-tail completion.

## 6. Model-intrinsic anchored root and completion-universal response

The direct anchored gap estimates imply, on the declared local parameter
window and channel,

```text
G_phys(nu_- ,eta) < -c_b delta,
G_phys(nu_+ ,eta) >  c_b delta,
partial_nu G_phys >= c delta,
```

so a unique local anchored root exists:

```text
mu_c^anc(delta,eta) = delta^2 nu_c^anc(delta,eta).
```

It is exact and preparation-independent for each fixed anchored RFDE.  It is
not a root of the original unanchored recovery law, and no global uniqueness
outside the declared channel is claimed.
With

```text
Xi_anc(delta,eta)
  = delta^(-3) [mu_c^anc(delta,eta)-mu_c^anc(delta,0)],
```

the full dual-norm estimates are

```text
||D_eta mu_c^anc-delta^3 Lambda_N||
  <= C(delta^4+delta^3||eta||)+flat,
```

No Hessian of the physical root is asserted until a separate `C^2`
strong-to-weak parameter theorem is proved for the complete outer passage.
The weighted conormal converges uniformly in network size to

```text
(1,-Lambda_N).
```

The root and its conormal line are invariant under phase section, intermediate
cut, and nonzero defining-function multipliers for the same model.  Changing
`a_anc` changes the global model and may change the exact finite-`delta`
baseline; equality or flat closeness of exact roots across arbitrary
completions is not asserted.  What is universal over the bounded completion
class is the centered weighted limiting response and conormal
`(1,-Lambda_N)`, with the theorem's stated uniform `O(delta)` error.  This is
the reusable invariant: projection-blind delay redistribution is detected by
the transverse-return covector even though its stationary projection vanishes.

## 7. No-circularity audit

The implementation is rejected if it does any of the following:

1. includes existence of a connection in the anchor hypotheses;
2. defines `W^s(E_-)` by the finite-core row `Q_e=0`;
3. treats the already proved state transversality
   `alpha <= mu_p <= 3 alpha` as the missing parameter slope
   `|partial_nu G_phys| >= c delta`;
4. tunes either anchor using the desired root;
5. infers pure parameter-jet flatness from endpoint state flatness;
6. identifies the linear finite-core row `lambda_ent` with the nonlinear
   physical stable sheet without a graph-transform comparison;
7. pulls the stable sheet backward with an ambient RFDE inverse;
8. calls the result an exact root for the original unanchored recovery law.
9. treats endpoint first-integral values as flat instead of combining them
   with the outer-strip integrals to recover the Gaussian tails;
10. chooses the cutoff exponent before the polynomial parameter-jet loss is
    known;
11. defines a membership gap only up to a multiplier and then silently calls
    it the normalized finite Lin residual;
12. asserts flat equality of exact roots for two different global completions.

## 8. Proof gates

- [x] A0. Original-recovery equilibrium/nonselection no-go.
- [x] A1. Anchored law and exact central-coincidence theorem.
- [x] A2. Full long-delay anchor root counts and parameter-uniform resolvent.
- [x] A3. `W^u(E_+)`, `W^s(E_-)`, section hits, and outer continuation.
- [x] A4. Nonlinear stable-sheet graph and normalized conormal comparison.
- [x] A5. Exact raw fold holonomy and complete-history membership gap.
- [x] A6. Direct normalized finite-gap bridge and endpoint-tail completion.
- [x] A7. Root bracket, uniqueness, parameter slope, and `C^1` response modulus.
- [x] A8. Identification of the intrinsic conormal with `Lambda_N`.
- [x] A9. Preparation/phase/section/cut naturality and composition.
- [ ] A10. Main/supplement rewrite, independent audit, tests, build, and visual
      verification.
