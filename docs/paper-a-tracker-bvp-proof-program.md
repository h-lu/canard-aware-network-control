# Paper A: mixed tracker BVP and physical representative class

Status: **proof contract, not a proved tracker theorem.**

Proposition `prop:principal-tracker-endpoint-green` now proves the principal
linear Green splitting for finite endpoint traces, including the exact
cancellation coordinate, dimension-uniform slow bounds, action-weighted
boundary lifts, and the sharp one-derivative loss in `Q`.  It does not lift a
compatible complete RFDE collar and therefore does not construct the
nonlinear tracker targeted by this contract.  Proposition
`prop:nonlinear-resource-defect-normal-form` now proves the exact nonlinear
cancellation coordinate and its local `C^0` speed reconstruction, while
`prop:compatible-endpoint-jet-collar` constructs the dimension-uniform
raw-compatible endpoint-history chart with the exact resource-defect/speed
bridge.  The latter is not a right inverse for arbitrary Green sources.
Proposition `prop:endpoint-scale-not-slow-speed` proves that the remaining
Green--collar coupling needs a hybrid slow/action estimate or a first-delay
buffer: a finite `mathfrak p=O(delta^2)` trace alone does not control the
slow-speed norm.  Proposition `prop:fold-time-tracker-normal-form` now
proves the exact structural repair: in fold time the tracker is a
fixed-delay defect system, the compatible collar is an ordinary initial
history, and neither `Q Z_s` nor `Q p_s` occurs.  Once `q<0` has been proved,
the solution can be reparameterized by `r`; no preparation or cutoff enters
this equivalence.  The fixed-delay mixed buffer estimate and nonlinear
contraction are still open.

This is the implementation target for the open physical-history part of
[Issue #32](https://github.com/h-lu/canard-aware-network-control/issues/32).
It starts from the exact, uncut identities already proved in Propositions
`prop:exact-outer-history-equation`, `prop:physical-history-phase-quotient`,
and `prop:exact-resource-gauge-quotient`.  The purpose of this note is to fix
the unknowns, boundary geometry, norms, and acceptance estimates before the
remaining Lyapunov--Perron argument is written.

The target is not a unique finite-`delta` slow history.  With no named global
anchor in the model, the strongest honest physical object is

```text
raw finite-branch representatives / uniform flat equivalence.
```

Exact roots belonging to two representatives may differ by a flat amount.
The algebraic root jet and its calibrated conormal must be independent of
the representative.

Everything below is restricted to Paper A's shared-resource structural-ball
equation, \(\eta\in\mathfrak T_N^{\rm red}\), a fixed compact
\((\nu,\eta)\)-window, sufficiently small positive \(\delta\), and
delay-enlarged collars on which \(q<0\), \(q\) is separated from zero, and
every physical backtrack remains defined.  The fading-rate exponent is the
one fixed in the frozen theorem, \(0<\vartheta<1/4\).  No statement here
applies to the sensed-recovery companion or to arbitrary layer perturbations.

## 1. Exact two-unknown tracker system

Write

```text
x(r,z) = r 1 + z(r),                 pi_N^T z(r) = 0,
F_N(r,z) = pi_N^T N_N(x(r,z)).
```

For nonzero `q`, define the physical delayed base point by

```text
integral_(r_k(r))^r du / q(u) = delta theta_k.
```

This is exactly `r_k(r)=Phi_q^(-delta theta_k)(r)`.  Put

```text
D_N(r,z,q,eta)
  = K sum_k L_k,N(eta)
      [{r-r_k(r)}1 + z(r)-z(r_k(r))],

D_c = pi_N^T D_N,              D_perp = P_perp,N D_N.
```

Projection of the proved uncut invariance equation eliminates the resource:

```text
delta^2 q z'
  = A_N z - P_perp,N N_N(r1+z) + delta^2 D_perp,       (T_z)

q d_r[2/3 - F_N(r,z) + delta^2 D_c - delta^2 q]
  = r - delta^2 nu.                                    (T_q)
```

After solving `(T_z),(T_q)`, reconstruct

```text
w(r) = 2/3 - F_N(r,z) + delta^2 D_c(r,z,q,eta)
       - delta^2 q(r).
```

Thus a solution of this two-unknown system is an actual solution of the raw
RFDE, not of a cutoff or prepared completion.  Conversely, every monotone
physical tracker in the fixed `r`-phase satisfies this system.

### The fixed-delay form used for existence

The global fixed point is **not** to be closed directly in the preceding
`r`-slow equations.  Proposition `prop:fold-time-tracker-normal-form` proves
the exact equivalent formulation on

```text
I_s = [s_-,s_+],          J_s = [s_- - theta_m,s_+].
```

For

```text
r(s) = pi_N^T(v(s)-1),
Z(s) = P_perp,N(v(s)-1)-z_0,N(r(s)),
p(s) = w_seed,N(r(s))-w(s),
```

let `D_N^ft[r,Z](s)` be the raw fixed-delay difference formed from
`(r,Z)(s)` and `(r,Z)(s-theta_k)`, and put
`Delta D_N^ft=D_N^ft-D_0,N(r(s))`.  Then

```text
Q = delta^(-2){p-ell_N Z-h_c} + Delta D_c^ft,
q = q_0(r)+Q,
r_s = delta q,

delta Z_s
  = mathcal C_N Z-z_0' p-R_z+z_0' h_c-h_perp
    +delta^2{Delta D_perp^ft-z_0' Delta D_c^ft},

delta p_s
  = w_0' p-w_0' ell_N Z-w_0' h_c
    +delta^2 w_0' Delta D_c^ft
    +delta^4 q(D_0,c-q_0)'.
```

This system is directly equivalent, term by term, to the raw fold-time RFDE.
It does not assume that the prescribed old history is a past orbit.  If the
whole delay-enlarged collective history has a nonvanishing monotone speed,
or after the first-delay window has flushed the prescribed history, the
solution reparameterizes to the exact `r`-tracker equations.  This is the
form in which the first-delay buffers and the nonlinear mixed BVP must be
proved.

## 2. Seed, residual, and principal linear operator

Let `z_0,N`, `w_0,N` be the proved critical curve and set

```text
q_0(r) = {r-delta^2 nu}/w_0,N'(r).
```

On `rho_delta <= |r| <= r_out`, `q_0` is negative and uniformly separated
from zero.  Evaluate the delay terms at `(z_0,q_0)` and use the seed

```text
z_seed = z_0,
w_seed = w_0 + delta^2 D_c(r,z_0,q_0,eta) - delta^2 q_0.
```

Its exact residuals are

```text
R_z = delta^2 {q_0 z_0' - D_perp(r,z_0,q_0,eta)},
R_q = delta^2 q_0 d_r{D_c(r,z_0,q_0,eta)-q_0}.
```

At the logarithmic interfaces this seed already has the necessary leading
resource displacement

```text
w_seed-w_0
  = delta^2/(2 alpha)
    + O(delta^2|r| + delta^3 + delta^4/|r|).
```

Set `Z=z-z_0`, `Q=q-q_0`, and define

```text
B_N(r)
  = A_N - P_perp,N D N_N(r1+z_0,N(r))|E_N,

ell_N(r)
  = pi_N^T D N_N(r1+z_0,N(r))|E_N.
```

The proved critical-layer bounds give a dimension-uniform stable inverse for
`B_N(r)` and `||ell_N(r)|| <= C|r|`.  The principal coupled operator is

```text
L_z(Z,Q)
  = delta^2 q_0 Z' - B_N(r)Z + delta^2 z_0,N'(r)Q,

L_q(Z,Q)
  = -delta^2 q_0 Q' + w_0,N'(r)Q
    - q_0 d_r{ell_N(r)Z(r)}.
```

All state-dependent backtrack terms, seed corrections, and nonlinear
remainders stay on the right.  The proved endpoint Green theorem uses
`mathfrak p=delta^2 Q+ell_N Z`: its `Z` and `mathfrak p` diagonal Green
operators are the main inverse, and the two off-diagonal terms close by a
block Neumann argument.  Algebraic recovery of `Q` loses one slow derivative,
and the theorem proves by counterexample that this loss cannot be removed
from the stated coefficient hypotheses.

The cancellation is now exact beyond the principal block.  With
`mathfrak p_nl=w_seed-w`, Proposition
`prop:nonlinear-resource-defect-normal-form` proves

```text
mathfrak p_nl
  = delta^2 Q + ell_N Z + h_c - delta^2 Delta D_c,
```

and rewrites both projected tracker equations without derivatives of `h_c`,
`Delta D_c`, or `Q` in the forcing.  The retained differential block is the
proved principal Green system; the full Fréchet derivative also contains
the explicitly displayed `delta^2`-weighted delay/backtrack terms.  Around
each admissible base point, `Q` is locally reconstructed in `C^0` because
`D_Q Delta D_c=O(delta)`.

## 3. Mixed boundary geometry

The physical speed is negative on both outer branches, so time moves toward
smaller `r`.

### Attracting branch

On `[rho_delta,r_out]`, prescribe a compatible, tame raw-RFDE history on an
outer collar

```text
[r_out, r_out + ell_delta],
ell_delta >= C delta theta_m.
```

Both principal normal coordinates are forward stable.  The curve BVP is
solved from `r_out` toward `rho_delta`.  Changing a fixed tame outer collar
may change the exact inner history, but the target comparison at the inner
section is flat.

### Repelling branch

Stage I first needs its own tracker BVP on `[-r_out,-rho_delta]`.  Prescribe a
compatible delay-enlarged inner collar at `-rho_delta` for the transverse
voltage history and one bounded scalar terminal row at `-r_out`,

```text
B_tr^r(Z,Q)
  = (Tr_in^hist Z,
     b_out^Q Q(-r_out) + b_out^Z Tr_out^hist Z)
  = (gamma_in,b_q).
```

The row must be uniformly transverse to the homogeneous principal `Q` mode,
and the inner collar must lie in the high-regularity compatible
solution-manifold history space fixed in Section 4.  The raw-compatible
endpoint chart and its exact finite trace count are now proved.  The missing
Green lemma must couple that chart to `Tr_in^hist` and the terminal history
row, and prove that `(L_z,L_q,B_tr^r)` is a dimension-uniform hybrid
isomorphism after the compatible collar lift is split off.  Proposition
`prop:principal-tracker-endpoint-green` already proves the corresponding
finite endpoint trace, mixed terminal orientation, and boundary-layer
estimates.  No quotient stable sheet or outer graph may enter this Stage-I
boundary operator.

There is one further causal datum.  For `r` within one delay of
`-rho_delta`, the physical backtrack samples the old side of the branch.
The old speed is not an independently anchored scalar function.  Proposition
`prop:compatible-endpoint-jet-collar` constructs a raw-compatible history

```text
(phi_e,omega_e)
  = Gamma_e^h[Z_e,p_e,hat_gamma;nu,eta],
```

where `p_e=w_seed(e)-omega_e`, the endpoint derivative jets are determined
by the raw RFDE compatibility recursion, and `hat_gamma` is a collar gauge,
not a Fredholm row.  The collective history derives the speed through

```text
r_phi(theta) = pi_N^T(phi_e(theta)-1),
q_old(r_phi(theta)) = delta^(-1) r_phi'(theta),
r_phi(theta) = Phi_(q_old)^(delta theta)(e).
```

The first compatibility row proves exactly

```text
delta^2 {q_old(e)-q_0(e)}
 = p_e - ell_N(e) Z_e - h_c(e,Z_e)
   + delta^2 {D_c[phi_e]-D_0,c(e)},
```

so `p_e` is the nonlinear tracker trace and not a second scalar boundary
condition.  The chart carries the full rectangular parameter jet in fixed
`theta` coordinates.  Eulerian fixed-`r` parameter differentiation loses
history derivatives, so the first-delay collar must remain in the pullback
chart or be treated by a new hybrid right inverse.  The proved chart does
not imply that an arbitrary Green source has those compatibility jets.

Only after that tracker exists does Stage II retain the stable
voltage-history coordinate at the inner collar and prescribe the scalar
strong-unstable coordinate at `-r_out`.  In quotient coordinates the
nonlinear mixed Lyapunov--Perron equation must have the form

```text
n_g^r(s)
  = Uhat^s(s,s_in) xi
    + Uhat^u(s,s_out) b_u
    + integral_(s_in)^s Uhat^s(s,sigma) N_s^r(sigma,n) d sigma
    - integral_s^(s_out) Uhat^u(s,sigma) N_u^r(sigma,n) d sigma.
```

The terminal scalar is closed by a tame outer graph

```text
b_u = g_out^r(P^s(s_out)n_g^r(s_out); nu, eta).
```

Here \(\widehat U^s\) is the forward quotient process restricted to the
stable bundle, while \(\widehat U^u(s,t)\), \(s<t\), denotes only the inverse
of the forward process on the one-dimensional strong-unstable bundle.
\(\mathcal N_{s/u}^r\) are the stable/unstable projections of the nonlinear
remainder after the exact fold-time rescaling; their powers of \(\delta\)
must be fixed when the graph theorem is stated.  There is no ambient backward
RFDE semiflow.  The output at the inner section
is a codimension-one sheet

```text
W^(r,g) = { beta_u = F^(r,g)(beta_s) },
```

not a unique repelling orbit.  The stable-history coordinate `beta_s` is
fixed later by exact membership of the incoming attracting history.

This construction is Stage II, not part of the tracker fixed point itself.
Stage I first solves the curve BVP in Sections 1--5 and transfers the frozen
splitting to the quotient along that already constructed tracker.  Only then
may Stage II use the quotient dichotomy to construct the nonlinear
codimension-one sheet.  No sheet estimate may be used circularly to prove
the tracker.

## 4. Fixed Banach spaces and target inverse estimate

For `k>=3`, use the scale-compatible curve norms

```text
||Z||_(k,delta)
  = delta^(-2) max_(j<=k) sup_r |r|^j ||D_r^j Z(r)||_N,

||Q||_(k,delta)
  = delta^(-2) max_(j<=k) sup_r |r|^(j+1)|D_r^j Q(r)|.
```

History directions use a Banach scale built from the capped fading norm in
`prop:frozen-voltage-history-splitting`.  At the top rung it must be the
delay-compatible solution-manifold space `H_cap^(k+3)`: histories have the
required strong derivatives, satisfy the raw RFDE compatibility identities
at the collar endpoint, and possess bounded trace maps into the residual and
boundary spaces.  Its order-zero member is the proved capped history space;
that order-zero theorem alone does not supply this higher-regularity lift.
The resource direction uses the proved adapted coordinate
`|omega|/|w'(r)|`.  The parameter jet class required by the physical
conormal comparison is

```text
J_phys = (C^1_nu C^2_eta) intersect (C^2_nu C^1_eta).
```

The first factor contains the mixed `nu eta eta` derivative; the second
contains `nu nu` and `nu nu eta`, which are needed to compare first
conormals at slightly different roots.  All derivatives are taken on fixed
Banach charts and bounded uniformly in the finite network size.

The fixed-point proof must use an explicit regularity ladder.  Put
`s=k+3` for one fixed `k>=3` and use the exact cancellation coordinate

```text
mathfrak p = delta^2 Q + ell_N Z.
```

The correct uniform endpoint Green transfer is

```text
residual order s
  -> (Z,mathfrak p) slow order s and Q slow order s-1.
```

Thus `Q` has order `k+2`, exactly what the physical-backtrack theorem needs,
while the delayed voltage input `Z` has order `k+3`.  If a downstream claim
requires `Q` itself at order `s`, the residual and coefficient inputs must be
raised to at least order `s+1`.  There is no uniform recovery from residual
order `s-1` to the full order-`s` slow norm: high-frequency forcing already
contradicts it for `epsilon y'+y=f`.  The proved endpoint Green theorem
includes this no-gain statement, uses singular boundary-layer norms for
arbitrary finite endpoint mismatches, and establishes the required uniform
`r`-regularity of `z_0,w_0,B_N,ell_N`.  Compatible complete-history collar
lifts now exist as raw endpoint charts at these orders.  What remains is a
bounded Green-to-collar coupling in the fixed-delay fold-time system.  The
old collar is retained in the fixed `theta` chart for the first-delay buffer;
only after it has left the delay window is the interior correction measured
in the Eulerian `r`-slow ladder.

The backtrack is differentiated through

```text
D_q r_k[h]
  = q(r_k) integral_r^(r_k) h(u)/q(u)^2 du.
```

It also satisfies the exact identity

```text
r_k'(r) = q(r_k(r))/q(r),
```

Because `|r|>=rho_delta`, every backtrack and composition estimate must lose
at most

```text
delta/|r| <= C/S_delta.
```

The exact fold-time normal form fixes the hybrid decomposition.  Choose once
and for all

```text
L_b > 2 theta_m + 1.
```

Use action/strong-history control on the attracting outer buffer
`[0,L_b]`, the repelling causal inner buffer `[0,L_b]`, and the repelling
scalar terminal buffer `[S_r-L_b,S_r]`.  Use the existing slow Green norm
only on the middle intervals.  With `T=delta s`,

```text
epsilon^j partial_T^j = delta^j partial_s^j,
```

so the proved endpoint Green boundary-layer derivatives match exactly the
`delta^j partial_theta^j` collar norm.  The complete nonlinear map must have
the target contraction number

```text
C { a_boundary + r_out + 1/S_delta
    + delta^(1-2 vartheta)/S_delta
    + exp(-c L_b/delta) } < 1/2.
```

The order of choices is: first fix `L_b`, then take `a_boundary` and
`r_out` small, and finally take `delta` small.

The displayed slow norms cannot be imposed directly on an arbitrary
`O(delta^2)` collar mismatch.  Such a mismatch creates an `O(delta^2)`
boundary layer in `r` and may have an `O(1)` derivative.  Every branch must
therefore be written as

```text
(Z,Q) = (Z_slow,Q_slow) + B_boundary b,
```

where `B_boundary b` is the explicit homogeneous Green boundary layer,
measured in `(Z,mathfrak p)` rather than the top slow `Q` norm.
Here `b` is generally a compatible complete collar history in
`H_cap^(k+3)`, together with the scalar resource compatibility row; it is not
merely a finite-dimensional endpoint amplitude.  The missing Green lemma
is now specifically the hybrid coupling: the raw collar chart constructs
compatible histories and fixes the exact trace count, but it does not turn
arbitrary Green data into a compatible lift.  The new lemma must couple its
bounded trace to the fold-time mixed Green inverse through the first-delay
buffers, prove buffer-to-slow bootstrap, and control the event time.  The
slow norms apply only to `(Z_slow,Q_slow)`; the boundary layer is measured by
its history amplitude and the capped Green weight.  Restricting all gauges
to artificially matched slow boundary values would defeat the
representative-class comparison.

## 5. The eight estimates that close the tracker and fold entry

The tracker and its entry into the retained fold chart are not closed until
all eight items below are proved.

1. Prove a dimension-uniform fold-time mixed Green/Lyapunov--Perron theorem
   on the three first-delay buffers, couple it to the raw-compatible collar
   chart, and bootstrap its middle trace into the existing slow Green
   ladder.  The repelling strong scalar uses only its one-dimensional future
   Green operator; backward RFDE evolution and forward shooting remain
   forbidden.
2. After the speed sign and event time are closed, apply the weighted `C^k`
   bounds for `q -> r_k(q)` and all delayed compositions, including every
   derivative in `J_phys`, to the reparameterized interior.
3. Bounds for `R_z,R_q` and the nonlinear remainder giving the displayed
   contraction number.
4. Compatible attracting collars and repelling terminal charts with common
   tame parameter jets.
5. Reconstruction estimates

   ```text
   |w'-w_0'| <= C delta^2,
   q<0,
   c|r| <= |w'(r)| <= C|r|.
   ```

6. Along the resulting tracker,

   ```text
   ||J_*(r)-J_fv(r)|| <= C delta^2,
   ||J_*-J_fv||/a_N(r) <= C delta/S_delta = o(1),
   ```

   This is only the first roughness input.  To transfer the frozen bundles,
   one must additionally control the Volterra conjugacy, the
   `-delta H_s pi_N^T` row, moving frozen projections and their derivatives,
   all delay terms, the `q` modulation, and the action-weighted evolution.
   In particular, prove relative bounds for `w'` and all required
   `J_phys` jets.  A separate nonautonomous roughness theorem must
   then produce the exact phase-quotiented dichotomy with uniform parameter
   derivatives; the two displayed generator bounds alone do not imply it.

7. At both logarithmic interfaces, sharpen the seed expansion to

   ```text
   w(+/-rho_delta)-w_0(+/-rho_delta)
     = delta^2/(2 alpha) + E_delta^(+/-),
   E_delta^(+/-) = o(delta^(2+kappa)),
   ```

   uniformly in the parameter jets used by the gap.  The derivative estimate
   in item 5 alone does not imply this interface value.
8. Prove voltage and complete-history overlap with the existing raw fold
   graph on one common history section.  Matching only the resource
   coordinate is insufficient.

## 6. Physical representative class and flat forgetting

An admissible physical endpoint gauge `g` consists only of raw-RFDE data:

- an attracting compatible history on the fixed outer collar;
- the repelling Stage-I data `(gamma_in,hat_gamma,b_q)`, including the raw
  compatible collar whose collective history derives the old speed, and the
  scalar terminal tracker row;
- a transverse strong-unstable terminal graph on the repelling outer
  section, retaining all stable-history coordinates;
- one common `r`-phase and one common slow-history tube;
- uniform tame `J_phys` jets.

Relative to the critical seed, the zeroth-order collar and terminal
amplitudes are at most `C_g delta^2` in the natural `(Z,mathfrak p)`
boundary-layer norm, where `mathfrak p=delta^2 Q+ell_N Z`.  For one fixed
gauge its parameter jets may lose at most
`C_g delta^(-M_g) exp(c_g S_delta)` relative to that scale.  Cutoff
completion, projected endpoint equality, or parameter oscillations of size
`exp(c/delta^2)` are not admissible gauges.  The construction theorem must
exhibit at least one compatible raw gauge satisfying these bounds; a
definition whose admissible class could be empty is insufficient.

For every two fixed admissible gauges, the theorem must prove

```text
||A^(g1)-A^(g2)||_(J_phys; Y_N)
 + ||F^(r,g1)-F^(r,g2)||_(C^2_beta_s J_phys)
 <= C_12 delta^(-M_12) exp(c_12 S_delta)
      exp{-c_0 log(1/delta)/delta}.
```

Both graph maps must be written on the same stable-coordinate ball, in the
same uniformly bounded history chart, with one common parameter domain.  The
norm on the attracting point includes every rectangular mixed jet, not only
its phase-space value.

The right-hand side is smaller than every algebraic power of `delta`.  This
estimate must come from the exact tracker quotient dichotomy and a
differentiated graph transform.  The formal reduced action alone does not
imply full-history forgetting.

Formally, two representative families \(H^{g_1},H^{g_2}\) are
uniformly flat-equivalent if, in the displayed common jet norm, for every
\(m>0\) there is a pair-dependent \(C_m\), independent of \(N\), such that
\[
 \sup_N\|H^{g_1}-H^{g_2}\|\le C_m\delta^m.
\]
The preceding exponential envelope implies this relation.  Constants need
not be uniform over the entire gauge class.

## 7. Exact fold passage, physical gap, and root class

The attracting object arrives at \(+\rho_\delta\), whereas the repelling
sheet is based at \(-\rho_\delta\).  Before a common chart can be used,
Stage III must construct an exact, uncut raw-RFDE forward fold passage (or
equivalent forward flow holonomy) carrying the attracting point from the
positive interface to the repelling sheet's common section at or beyond the
negative interface, with the same rectangular parameter jets and uniform
chart bounds.  It must not transport the repelling history sheet backward
through an RFDE semiflow.  This is an independent theorem gate; it is not
contained in outer flat forgetting.

Only after that passage has been proved, write the transported attracting
point in the common chart as

```text
A^g = (A_s^g,A_u^g)
```

and the transported repelling sheet as
`beta_u=F^(r,g)(beta_s)`.  Define the exact membership gap

```text
G^g(nu,eta) = A_u^g - F^(r,g)(A_s^g).
```

Then `G^g=0` if and only if the complete incoming physical history belongs
to the repelling sheet.  No voltage-event or endpoint projection may replace
this membership condition.

Root existence requires more than a slope.  On one common window
\([\nu_-,\nu_+]\), the theorem must prove the uniform bracket and
transversality

```text
G^g(nu_-,eta) <= -c_b delta,
G^g(nu_+,eta) >=  c_b delta,
|partial_nu G^g| >= c delta,
```

after fixing the common gap orientation.  Flat independence of even the
first conormal also requires the nonoptional gap-level bounds from
`prop:physical-weighted-c1-transfer`:

```text
|G_nunu^g| + ||D_eta G_nu^g|| <= C delta^2,
delta^(-1)|G_nu^(g1)-G_nu^(g2)|
  + delta^(-2)||D_eta G^(g1)-D_eta G^(g2)|| = uniformly flat,
|nu_c^(g1)-nu_c^(g2)| = uniformly flat.
```

The first line supplies the uniform `nu` modulus needed to evaluate the two
ratios `-D_eta G/G_nu` at slightly different roots; it is part of the
flagship gate, not an optional second-jet assumption.  If flat equivalence of
second structural root jets is later claimed, one must additionally prove
and compare `G_etaeta` together with the already required `G_nunu` and
`G_nueta`, with the stronger continuity moduli needed by twice implicit
differentiation.  Paper A's present flagship target is only the first
structural conormal, not this optional second root jet.  With the physical
normalization
`mu=delta^2 nu`, the intrinsic first-jet object is

```text
[mu_c^g]_flat,

Xi^g(eta)
  = delta^(-3){mu_c^g(eta)-mu_c^g(0)},

[(1,-D_eta Xi^g(0))]_flat.
```

Flat independence among physical gauges does not by itself identify the
hidden-return covector.  For at least one physical representative, a separate
physical-to-selected weighted comparison must prove the hypotheses of
`prop:physical-weighted-c1-transfer`.  The final identification target is

```text
D_eta Xi^g(0) -> Lambda_N
```

in \((\mathfrak T_N^{\rm red})^*\), uniformly in `N`.  This gives a
preparation-independent algebraic physical connection/conormal class.  It
does not claim equality of the finite-`delta` roots for different endpoint
gauges.

## 8. Acceptance ledger

- [x] Exact raw tracker invariance equation.
- [x] Exact physical time-tangent quotient.
- [x] Exact resource gauge and Volterra history coordinate.
- [x] Principal finite-endpoint Green splitting with dimension-uniform slow
      bounds, mixed repelling orientation, action-weighted boundary lifts,
      and the sharp regularity ladder.
- [x] Exact nonlinear resource-defect normal form, full linearization, and
      local `C^0` reconstruction of the physical speed.
- [x] Dimension-uniform raw-compatible endpoint-jet collar chart, including
      the exact `p_e`-to-speed/backtrack bridge and fixed-`theta` `J_phys`
      parameter jets.
- [x] Sharp obstruction showing that finite endpoint `mathfrak p` scale does
      not control the slow-speed class.
- [x] Exact fixed-delay fold-time tracker normal form, direct equivalence
      with the raw RFDE, conditional reparameterization, and explicit
      `Gamma_e^h` initial-history interface.
- [ ] Repelling Stage-I Green trace/terminal operator coupled to the raw
      collar chart through the fixed-delay mixed first-buffer inverse.
- [x] Uniform high-order `r` regularity of `z_0,w_0,B_N,ell_N` at the Green
      ladder orders.
- [x] Backtrack/composition parameter jets through the weighted third
      Fréchet derivative needed for `J_phys`.
- [ ] Nonlinear tracker contraction and Green--collar reconstruction.
- [ ] Full action-weighted nonautonomous quotient roughness theorem,
      including Volterra, phase-row, moving-projection, delay, `q`, and
      parameter-jet terms.
- [ ] Attracting point and repelling codimension-one sheet.
- [ ] At least one compatible raw gauge with the stated scale, and uniform
      flat forgetting through `J_phys` for every fixed gauge pair.
- [ ] Resource interface remainder and complete-history overlap with the raw
      fold graph.
- [ ] Exact uncut fold passage to one common history chart.
- [ ] Uniform gap bracket and nonzero root slope.
- [ ] Nonoptional `G_nunu`, `D_eta G_nu`, cross-gauge gap, and root-location
      moduli needed for first-conormal comparison.
- [ ] Exact membership gap and physical root class.
- [ ] Physical-to-selected weighted comparison for one representative.
- [ ] Identification of the flat conormal class with `Lambda_N`.

Until the unchecked items are proved, Paper A must continue to say that the
physical tracker, gap, and root do not yet exist as theorems.
