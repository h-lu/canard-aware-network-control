# Paper A: physical outer-history route after the layer theorem

Status: **the unprepared critical curve, formal truncated reduced actions,
the positive-`delta` frozen-resource voltage history splitting, physical
backtrack calculus, principal finite-endpoint Green splitting, and a sharp
nonselection obstruction are proved.  The exact nonlinear resource-defect
normal form and a raw-compatible endpoint-history collar chart are also
proved, together with a boundary-layer obstruction showing why they do not
yet close the nonlinear RFDE tracker.  The exact fixed-delay fold-time
tracker normal form is now proved and fixes the remaining construction
route.  Its finite method-of-steps buffer theorem, the nonlinear tracker, and the
phase-quotiented nonautonomous slow-history theorem remain open.**

This note refines the physical-identification part of
[Issue #32](https://github.com/h-lu/canard-aware-network-control/issues/32).
It concerns Paper A's finite shared-resource Markov networks.  Issue #11
concerns a different two-module leaky model and cannot supply this theorem.
The now-fixed mixed BVP, endpoint-gauge class, flat comparison, and exact
membership gap are specified in
[`paper-a-tracker-bvp-proof-program.md`](paper-a-tracker-bvp-proof-program.md).

## 1. What has now been proved

Proposition `prop:unprepared-outer-skeleton` in the main paper, with its
proof in Supplement D, gives the following objects without a preparation,
cutoff, or planar completion:

1. a unique local constant-history critical curve
   `(V_0,N(r), w_0,N(r))`, uniform in network size;
2. its cubic expansion

   ```text
   z_0,N(r) = g_N r^2 + g_3,N r^3 + O_unif(r^4),
   w_0,N(r) = 2/3 - alpha r^2 - kappa_N r^3 + O_unif(r^4);
   ```

3. a fold-continuing simple collective eigenvalue and an `N-1` dimensional
   stable complement for the leading frozen-voltage matrix;
4. the exact identity

   ```text
   lambda_c,N(r) = w_0,N'(r) / Theta_N(r),
   Theta_N(r) = 1 + O_unif(r^2),
   ```

   which fixes the attracting and repelling signs without assuming a sign
   for `kappa_N`;
5. a nonzero reduced speed and two positive formal truncated actions on
   `rho_delta <= |r| <= r_out`, with a common lower bound.

Supplementary Proposition `prop:backward-asymptotic-nonselection` proves
that backward completeness, boundedness, convergence in an unnormalized
history norm, a common phase row, fixed-`delta` smoothness, and even
superalgebraic strong-history closeness do not by themselves imply either a
unique history or tame parameter jets.  It is a generic RFDE obstruction to
that inference, not a model-specific nonexistence theorem.

These are genuine critical-layer inputs and a genuine logical obstruction.  They do not
construct a finite-`delta` slow-history representative.

Proposition `prop:frozen-voltage-history-splitting` now closes the first
positive-`delta` ambient-history gate for the **frozen-resource voltage
equation**.  In fold time `s=delta t` it proves, on the fixed history space,

- capped-rate stability of the full attracting voltage history space;
- on the repelling branch, an invariant codimension-one stable history
  space and a one-dimensional strong-unstable history line;
- constants and structural `C^2_eta` graph/projection bounds uniform in
  network size.

The fading phase norm uses exponent `2 kappa`, while the evolution estimate
uses `kappa`; this margin controls old-history translation.  The contraction
number is

```text
C delta^2 {1 + exp(2 kappa theta_m)} / a(r)
    <= C delta^(1-2 vartheta) / S_delta.
```

This is not the full voltage--resource theorem.  Remark
`rem:frozen-resource-phase-quotient` gives an admissible homogeneous
subclass in which the raw frozen repelling voltage--resource block has two
positive roots.  The correct next object is therefore a phase-quotiented
normal cocycle, not an unquotiented one-unstable dichotomy.

Proposition `prop:physical-history-phase-quotient` closes the algebraic part
of that quotient.  Along any already constructed physical history with
nonzero stationary-coordinate speed, it normalizes the exact transported
time tangent by `pi_N^T phi(0)=1` and proves that projection onto the fixed
stationary-coordinate gauge produces an exact representation of the
intrinsic quotient cocycle.  The gauge kernel need not itself be invariant.
This is not a slow-history existence or dual-phase theorem: its input is the
physical history that still has to be constructed.

Proposition `prop:exact-resource-gauge-quotient` now supplies the useful
normal coordinates once an exact tracker is given.  Dividing the resource
variation by the tracker slope `w_prime(r)` and subtracting the resulting
multiple of the genuine history tangent removes the raw
`-omega/delta` coupling exactly.  The quotient history is related to an
ordinary voltage history by

```text
psi_s = (I - K_s) u_s,
||K_s|| <= C / S_delta,
```

and the sign and Volterra correction in the resulting nonautonomous RFDE are
proved, not formal.  Uniformity requires the adapted resource norm
`|omega|/|w_prime(r)|`; the raw product norm generally loses a factor
`1/|r|`.  The proposition still assumes existence of the exact tracker,
`|w_prime(r)| comparable to |r|`, and a delay collar.

Proposition `prop:principal-tracker-endpoint-green` closes the principal
finite-dimensional endpoint BVP.  The cancellation coordinate
`mathfrak p=delta^2 Q+ell_N Z` yields a dimension-uniform slow Green inverse
on both branches, the correct mixed terminal orientation on the repelling
branch, and action-weighted homogeneous boundary lifts.  It also proves that
`Q` loses one slow derivative and that the loss is sharp under the listed
coefficient hypotheses.  This theorem does not construct the compatible
complete-history Green lift or solve the nonlinear tracker equation.

Proposition `prop:nonlinear-resource-defect-normal-form` identifies the
exact cancellation coordinate with the physical resource defect
`mathfrak p_nl=w_seed-w`, gives the full nonlinear normal form without
derivatives of the nonlinear collective remainders in the forcing, and
locally reconstructs `Q` in `C^0`.  Proposition
`prop:compatible-endpoint-jet-collar` constructs a dimension-uniform
raw-RFDE compatible collar chart; its collective history derives `q_old`,
and its first compatibility row is exactly the nonlinear endpoint
`mathfrak p_nl` reconstruction.  It is a chart of solution-manifold
histories, not a source-wise Green right inverse.  Proposition
`prop:endpoint-scale-not-slow-speed` proves sharply that an
`O(delta^2)` finite endpoint resource defect may still generate an
unbounded slow-speed boundary layer.  Thus the next gate is a hybrid
slow/action Green--collar coupling on a finite method-of-steps buffer.

Proposition `prop:fold-time-tracker-normal-form` proves the exact way around
that obstruction.  In fold time, `(r,Z,mathfrak p_nl)` satisfies a
fixed-delay system directly equivalent to the raw RFDE; `Q` is reconstructed
algebraically, and no `Q Z_s` or `Q p_s` term is created.  The collar chart
is an ordinary compatible initial history with trace `p_e`.  The old history
need not be a past orbit.  Once the fixed-delay mixed BVP proves `q<0`, the
interior reparameterizes to the exact `r`-tracker and the existing physical
backtrack calculus applies.  This equivalence is proved, but its mixed-buffer
contraction is not.  One maximal delay removes direct evaluation of the
prescribed history, not the narrow delayed echoes that it has already
generated.  At slow order `s` the current proof contract therefore uses an
integer `M_s` with `M_s(1-2 vartheta)>s` before bootstrapping to the slow
Green norm.

## 2. The exact curve-restricted physical equation

Proposition `prop:exact-outer-history-equation` now proves the statements
in this section as an if-and-only-if reduction.  A solution of the displayed
uncut invariance equation generates an actual orbit of the raw RFDE, and
every physical orbit lying on such an `r`-parameterized curve satisfies
the equation.  The proposition also identifies the derivative of the full
history embedding with the normalized time tangent used by the quotient
cocycle.  It does not prove that a solution of the invariance equation
exists.

Let a structural redistribution be

```text
L_k,N(eta) = B_k,N + E_k,
sum_k E_k = 0,
pi_N^T E_k = 0.
```

Use slow time `T=delta^2 t` and seek a history curve in the form

```text
V(r) = 1 + r 1 + z(r),        pi_N^T z(r) = 0,
q(r) = dr/dT.
```

If `Phi_q^T` is the scalar base flow, the physical delay
`theta_k/delta` in `t` becomes `delta theta_k` in `T`, so the delayed base
point is

```text
r_k(r) = Phi_q^(-delta theta_k)(r).
```

The exact, uncut voltage invariance equation is

```text
delta^2 q(r) {1 + z'(r)}
  = {2/3-w(r)} 1
    - c_N o {r 1 + z(r)}^2
    - (beta/3) {r 1 + z(r)}^3
    + A_N z(r)
    + delta^2 K sum_k L_k,N(eta)
        [{r-r_k(r)}1 + z(r)-z(r_k(r))].
```

Its collective and transverse projections are, exactly,

```text
delta^2 q
  = 2/3-w
    - pi_N^T[c_N o (r1+z)^2]
    - (beta/3) pi_N^T[(r1+z)^3]
    + delta^2 K sum_k pi_N^T L_k,N(eta)
        [{r-r_k}1 + z(r)-z(r_k)],

delta^2 q z'
  = A_N z
    - P_perp,N[c_N o (r1+z)^2 + (beta/3)(r1+z)^3]
    + delta^2 K P_perp,N sum_k L_k,N(eta)
        [{r-r_k}1 + z(r)-z(r_k)].
```

The resource equation is

```text
q(r) w'(r) = sigma_N(r) - delta^2 nu,
```

with `sigma_N(r)=r` for shared recovery and the sensed expression from
the main paper for the second return channel.

This formulation uses only forward RFDE information: delayed values are
evaluations of the same curve at a backward base-flow point.  It is the
equation that a physical outer-history theorem must solve.  It also shows
the first required resource correction: at the logarithmic matching radius,

```text
w_slow,N,delta(r)
  = w_0,N(r) + delta^2/(2 alpha) + E_delta(r).
```

because the critical curve itself lies at
`d=1/(2 alpha)+o(1)`, not in the retained `d=0` canard tube.
The displayed `delta^2/(2 alpha)` term is necessary, not sufficient.  At
`r=+/-rho_delta`, a sufficient resource-coordinate estimate would be
`E_delta=o(delta^(2+kappa))`, uniformly in all indices; exact overlap still
requires voltage and full-history estimates.

## 3. Correct boundary geometry

The two outer branches do not have the same boundary-value structure.

### Attracting branch

For `r in [rho_delta,r_out]`, a delayed base point lies farther out on the
attracting branch.  A construction therefore needs a compatible physical
history on an outer collar of `r_out` whose width is `O(delta Theta_*)`.
All principal normal directions contract toward the inner boundary.

### Repelling branch

For `r in [-r_out,-rho_delta]`, the instantaneous problem has one strong
collective unstable direction.  In the full RFDE phase space the stable
part is not merely the `N-1` Markov current modes: long delay supplies
infinitely many stable history modes.  The correct mixed boundary data are:

- a complete stable-history coordinate on an inner collar near
  `r=-rho_delta`;
- one scalar strong-unstable coordinate at the outer endpoint
  `r=-r_out`.

Schematically, after the frozen splitting has been transferred to a
phase-quotiented nonautonomous normal cocycle, the normal
Lyapunov--Perron equation must have the form

```text
n(T)
  = U(T,T_in) P_s beta_s
    + U(T,T_out) P_u beta_u
    + delta^(-2) integral_(T_in)^T U(T,S) P_s F(S) dS
    - delta^(-2) integral_T^(T_out) U(T,S) P_u F(S) dS.
```

Here `P_s` acts on a full stable history space and `P_u` is the one
dimensional strong collective coordinate.  The output is naturally a
codimension-one repelling history sheet, not a unique repelling trajectory
chosen by outer data alone.

The obstruction is already present without delay or nonlinearity.  For

```text
delta^2 n_perp,T = A_N n_perp,
```

recovering an inner stable coordinate from its outer value costs

```text
exp{D gamma (T_out-T_in)/delta^2}.
```

Thus an `N`-uniform outer-to-inner inverse preserving current evaluation
cannot exist.  The inner stable-history coordinate must be retained and
later fixed by exact gluing to the incoming physical history.

## 4. Candidate norms for the new theorem

This subsection records the proof design, not a proved estimate.

On either outer interval, the expected normal correction is `O(delta^2)`.
A scale-compatible curve norm is

```text
||n||_(k,delta)
  = max_(j<=k) sup_r delta^(-2) |r|^j ||D_r^j n(r)||,

||qhat||_(k,delta)
  = max_(j<=k) sup_r delta^(-2) |r|^(j+1)
      |D_r^j qhat(r)|.
```

At `rho_delta=delta S_delta/(2 alpha)`, one has
`r_k-r=O(delta)` and `delta/rho_delta=O(1/S_delta)`.  Delay composition
therefore has the candidate loss `1+O(1/S_delta)` in these norms.

A full fast-action weight is unsafe because evaluation across a long delay
can introduce `exp(c/delta)` inside the contraction constant.  A candidate
capped exponent density is

```text
a(r) = min{D gamma/2, c |r|},
L_delta = log(1/delta),
lambda_weight(r)
  = vartheta delta^(-2)
      min{a(r), delta L_delta/Theta_*},
0 < vartheta < 1/2.
```

Across one slow-time delay window its weight ratio is at most
`delta^(-vartheta)`.  The target contraction estimate is

```text
kappa_delta
  <= C {r_out + 1/S_delta
           + delta^(1-2 vartheta)/S_delta}.
```

If the required nonautonomous normal splitting and boundary-map estimates
are proved, this would close after first choosing `r_out` small and then
`delta` small.  The corresponding conservative boundary-forgetting scale is

```text
C delta^(-M) exp{-c log(1/delta)/delta},
```

which is still smaller than every algebraic power.  No such estimate is yet
claimed in the manuscript.

## 5. The next new analytic lemma

The frozen-resource voltage theorem is now proved.  The next proof must
construct a true positive-`delta` slow tracker, fix its time-shift direction,
and transfer the frozen bundles to the resulting nonautonomous normal
cocycle.  It must establish:

1. a parameter-coherent true slow tracker on both outer branches;
2. uniform bounds and parameter jets for the stationary-gauge normalized
   tangent history and quotient representation;
3. roughness of the frozen voltage bundles under the nonautonomous
   slow-curve and modulation terms;
4. the attracting representative and repelling mixed-boundary sheet;
5. joint `J_phys=(C^1_nu C^2_eta) intersect (C^2_nu C^1_eta)` Frechet
   bounds for the normal bundles, boundary maps, and fixed points, uniform
   in `N`.

Only after this lemma may the mixed Lyapunov--Perron equation in Section 3
be called an actual construction.

## 6. Two legitimate completion routes

### Exact physical anchor

Name a global invariant set, fix a phase and a wave/asymptotic coordinate,
construct its physical incoming and outgoing history objects, and prove
their exact connection root.  This would give an exact finite-`delta`
maximal-canard locus.

### Physical representative class

Construct a nonempty class of uncut invariant slow-history representatives,
prove that different normalized boundary representatives differ at the fold
by a superalgebraic amount in the full weighted `C^1` parameter norm, and
define the physical connection root only modulo that flat equivalence.  Then
prove that the resulting algebraic conormal jet equals `Lambda_N`.

The second route is acceptable only if nonemptiness, full-history gluing,
and flat `C^1` comparison are theorems.  Defining the class by the desired
comparison, or merely renaming the existing preparation-selected roots, is
not acceptable.

## 7. Gate ledger

- [x] Unprepared critical curve, cubic expansion, and dimension-uniform
      leading frozen-voltage splitting.
- [x] Positive attracting and repelling formal truncated reduced actions.
- [x] Exact proof that convergence in an unnormalized history norm and
      superalgebraic history closeness do not select a tame history jet.
- [x] Exact curve-restricted physical invariance equation and correct mixed
      boundary geometry recorded.
- [x] Positive-`delta` frozen-resource voltage history splitting, with one
      strong repelling unstable line and a full stable history complement.
- [x] Proof that the raw full voltage--resource one-unstable target is false
      before phase quotienting.
- [x] Exact stationary-coordinate quotient along any genuine monotone
      physical history; no frozen eigenvector is used as a phase direction.
- [x] Exact if-and-only-if uncut outer-history invariance equation and its
      normalized full-history tangent.
- [x] Exact resource-gauge normal equation and `O(S_delta^(-1))` Volterra
      conjugacy to a standard voltage-history RFDE.
- [x] Weighted physical-backtrack and delayed-composition calculus through
      the third Fréchet derivative required by the rectangular
      `J_phys` jet, with only `O(S_delta^(-1))` relative loss on the
      logarithmic collar.
- [x] Principal finite-endpoint Green splitting, including high-order
      critical coefficients, the mixed repelling terminal orientation, and
      action-weighted boundary layers in `(Z,mathfrak p)`.
- [x] Exact nonlinear resource-defect normal form and local `C^0` speed
      reconstruction.
- [x] Raw-compatible high-regularity endpoint collar chart with exact
      resource-defect/speed/backtrack bridge and fixed-history parameter
      jets.
- [x] Boundary-layer obstruction to deriving slow-speed control from a
      finite endpoint resource-defect scale alone.
- [x] Exact fixed-delay fold-time tracker normal form and compatible-collar
      initial-history interface, with no past-orbit assumption.
- [ ] Fold-time finite method-of-steps buffers, order-dependent
      buffer-to-slow bootstrap, and
      nonlinear tracker contraction on both outer branches.
- [ ] Phase-quotiented nonautonomous normal splitting along a true slow
      history.
- [ ] Attracting representative and repelling codimension-one history sheet
      with uniform parameter jets.
- [ ] The `delta^2/(2 alpha)` resource correction and exact overlap with the
      existing fold history graph.
- [ ] Exact incoming-history gluing that fixes the repelling stable-history
      coordinate.
- [ ] A physical gap/root, or a nonempty flat-equivalence class of roots.
- [ ] Weighted `C^1` selected-to-physical comparison and identification with
      `Lambda_N`.

Issue #32 remains open.
