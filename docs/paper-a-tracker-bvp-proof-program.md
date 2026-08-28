# Paper A: mixed tracker BVP and physical representative class

Status: **proof contract, not a proved tracker theorem.**

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
remainders stay on the right.  The diagonal `Z` and `Q` Green operators are
the main inverse; the two off-diagonal terms are closed by a block Neumann
argument.  The `Q -> Z` feedback carries `delta^2`; the `Z -> Q` feedback is
triangular and uses `ell_N=O(r)` together with the derivative weight.

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
solution-manifold history space fixed in Section 4.  The missing Green lemma
must define `Tr_in^hist`, the terminal row, their compatibility conditions,
and prove that `(L_z,L_q,B_tr^r)` is a dimension-uniform isomorphism after the
explicit collar lift is split off.  No quotient stable sheet or outer graph
may enter this Stage-I boundary operator.

There is one further causal datum.  For `r` within one delay of
`-rho_delta`, the physical backtrack samples `q` on the old-side extension of
the branch.  Fix an anchored old-speed collar

```text
q_old = Gamma_q^old[Q(-rho_delta), hat_gamma_q]
        on [-rho_delta,-rho_delta+ell_delta].
```

Its value at the endpoint is the unknown `Q(-rho_delta)` produced by the
mixed BVP, not a second scalar boundary condition.  The shape datum
`hat_gamma_q`, its raw-equation compatibility rows, and the uniformly bounded
anchored extension operator `Gamma_q^old` are part of the collar space and
must be compared between gauges.  Equivalently one may solve `Q` on the
delay-enlarged interval, but then the Green theorem must supply the same
trace count and may not impose both an independent inner value and the outer
terminal row.

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

The fixed-point proof must use an explicit regularity ladder.  For a fixed
\(k\ge3\), take the curve unknowns in weighted order \(k+3\), the equation
residuals in weighted order \(k+2\), and prove that the first-order mixed
Green operator maps the residual space back to the unknown space.  The
physical-backtrack theorem then uses \(q\)-directions through weighted order
\(k+2\) and delayed inputs through order \(k+3\).  This one-derivative
recovery is part of the missing Green lemma; it may not be hidden under a
generic smooth-dependence assertion.  Before using this ladder one must also
prove uniform \(r\)-regularity of `z_0,w_0,B_N,ell_N` through the required
orders (or lower the ladder and every downstream claim consistently); the
currently recorded low-order critical-curve estimates cannot silently be
promoted.

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

After the diagonal Green inverses are established, the complete nonlinear
map must have contraction number

```text
C { r_out + 1/S_delta + delta^(1-2 vartheta)/S_delta } < 1/2.
```

The order of choices is: first fix `r_out` small, then take `delta` small.

The displayed slow norms cannot be imposed directly on an arbitrary
`O(delta^2)` collar mismatch.  Such a mismatch creates an `O(delta^2)`
boundary layer in `r` and may have an `O(1)` derivative.  Every branch must
therefore be written as

```text
(Z,Q) = (Z_slow,Q_slow) + B_boundary b,
```

where `B_boundary b` is the explicit homogeneous Green boundary layer.
Here `b` is generally a compatible complete collar history in
`H_cap^(k+3)`, together with the scalar resource compatibility row; it is not
merely a finite-dimensional endpoint amplitude.  The missing Green lemma
must construct its bounded trace and lift at every rung of the scale.  The
slow norms apply only to `(Z_slow,Q_slow)`; the boundary layer is measured by
its history amplitude and the capped Green weight.  Restricting all gauges
to artificially matched slow boundary values would defeat the
representative-class comparison.

## 5. The eight estimates that close the tracker and fold entry

The tracker and its entry into the retained fold chart are not closed until
all eight items below are proved.

1. A dimension-uniform Green inverse, including the explicit boundary-layer
   coordinate, for the attracting BVP and for the repelling mixed BVP.  The
   repelling strong scalar uses its terminal Green operator; forward shooting
   is forbidden.
2. Weighted `C^k` bounds for `q -> r_k(q)` and for all delayed compositions,
   including every derivative in `J_phys`.
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
- the repelling Stage-I data `(gamma_in,hat_gamma_q,b_q)`, including the
  anchored old-speed collar and the scalar terminal tracker row;
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
- [ ] Principal mixed Green inverse with dimension-uniform bounds.
- [ ] Repelling Stage-I tracker trace/terminal operator and compatible
      high-regularity collar lift.
- [ ] Uniform high-order `r` regularity of `z_0,w_0,B_N,ell_N` at the Green
      ladder orders.
- [x] Backtrack/composition parameter jets through the weighted third
      Fréchet derivative needed for `J_phys`.
- [ ] Nonlinear tracker contraction and collar reconstruction.
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
