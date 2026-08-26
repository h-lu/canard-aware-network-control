# A quantitative route from the inner cycle to physical-pulse onset

Status: **theorem design with proved upstream reductions, a proved center
inner Floquet index, and a qualitative center stable manifold.**  This note fixes the shortest quantitative argument
that would turn the validated leaky periodic branches and the physical pulse
curve into a local biological onset theorem.  At the center parameter the
inner orbit now has exactly one nontranslation unstable multiplier, and
classical RFDE theory plus the exact reduced-history factorization gives a
\(C^1\), codimension-one local stable manifold.  This does not yet validate a
parameter-box dichotomy, an explicit graph radius or defining covector, the
particular pulse-section intersection, outer capture, or onset threshold.

## 1. The phase space and the object to be separated

Let

\[
 X=C([-r,0],\mathbb R^2),\qquad
 Y=C([-r,0],\mathbb R)\times\mathbb R,
 \qquad r=5\sqrt5.
\]

The exact projection and compatible lift already proved for the leaky model
are

\[
 \pi(\phi_v,\phi_w)=(\phi_v,\phi_w(0)),\qquad
 \iota(q,\omega)=(q,\mathcal R(q,\omega)).                 \tag{1.1}
\]

For every \(t\ge r\), the full semiflow factors as

\[
 \Phi_t=\iota\Psi_t\pi.                                  \tag{1.2}
\]

Consequently all nonzero Floquet spectrum and the codimension of a stable
manifold can be calculated in \(Y\), while the resulting stable set pulls
back exactly to \(X\).  No old recovery-history coordinate may be introduced
as an additional crossing direction.

Let \(\xi=(a,\kappa _3)\) range in a closed parameter box and let
\(\Gamma_i(\xi)\) denote the inner periodic orbit.  The desired local
separator is

\[
 W^s_{\rm loc}(\Gamma_i(\xi))\subset Y.                  \tag{1.3}
\]

The physical one-unit voltage pulse produces a jointly smooth terminal
history

\[
 K_\xi(J)\in X,
 \qquad B_\xi(J)=\Psi_{t_\xi(J)}\pi K_\xi(J)\in\Sigma_\xi,\tag{1.4}
\]

where \(t_\xi(J)\) is a finite, phase-fixed entrance time into a Poincare
section \(\Sigma_\xi\) through \(\Gamma_i(\xi)\).  The pulse stage and
\(D_JK_\xi(J)\) are already exact objects; the entrance map in (1.4) still
has to be enclosed.

## 2. The Floquet conclusion actually needed

The spectral certificate must prove all of the following on one common
parameter box, or at the center followed by a separate continuation theorem:

1. the translation multiplier is algebraically simple;
2. there is exactly one nontranslation multiplier
   \(\mu_u(\xi)\in[\mu_-,\mu_+]\subset(1,\infty)\), and it is real and
   algebraically simple;
3. all remaining nonzero multipliers lie in \(|\mu|\le q_0<1\);
4. the corresponding Riesz projections and the phase section depend
   \(C^1\) on \(\xi\).

The first three conclusions determine a one-dimensional unstable space and
a split stable complement on the section.  A finite monodromy eigenvector or
a zero-free calculation on only part of the principal logarithmic strip does
not provide this dichotomy.

Choose coordinates \((u,z)\in\mathbb R\oplus E^s_\xi\) on the section, with
\(u\) oriented by the unstable left Riesz covector.  The return map then has
the form

\[
 P_\xi(u,z)=
 \bigl(\mu_u(\xi)u+f_\xi(u,z),\,
       A_\xi z+g_\xi(u,z)\bigr),                         \tag{2.1}
\]

where \(f_\xi(0,0)=g_\xi(0,0)=0\) and their first derivatives vanish at the
origin.  The rigorous calculation must enclose (2.1) on a product ball; the
linear Floquet count alone supplies no usable nonlinear neighborhood.

## 3. A forward Lyapunov--Perron construction

The RFDE semiflow is not inverted.  Fix numbers

\[
 q_0<\beta<1<\mu_-                                                   \tag{3.1}
\]

and suppose the stable powers satisfy

\[
 \|A_\xi^n\|\le C_s q_0^n\qquad(n\ge0).                \tag{3.2}
\]

For a prescribed stable coordinate \(z_0\), a forward orbit converging to
the periodic orbit must satisfy

\[
\begin{aligned}
 u_n&=-\sum_{k=n}^{\infty}
       \mu_u(\xi)^{n-k-1}f_\xi(u_k,z_k),\\
 z_n&=A_\xi^nz_0+
       \sum_{k=0}^{n-1}A_\xi^{n-1-k}g_\xi(u_k,z_k).
\end{aligned}                                             \tag{3.3}
\]

On the sequence space with norm

\[
 \|(u,z)\|_\beta=
 \sup_{n\ge0}\beta^{-n}
       \max\{|u_n|,\|z_n\|\},                           \tag{3.4}
\]

let \(L_f,L_g\) be directed Lipschitz bounds for the two nonlinear rows of
(2.1).  The two geometric-series estimates are

\[
 \frac{L_f}{\mu_- -\beta},\qquad
 \frac{C_sL_g}{\beta-q_0}.                              \tag{3.5}
\]

A source-bound self-map radius and

\[
 q_{\rm LP}:=
 \max\left\{
  \frac{L_f}{\mu_- -\beta},
  \frac{C_sL_g}{\beta-q_0}
 \right\}<1                                             \tag{3.6}
\]

make (3.3) a uniform contraction.  If separate block Lipschitz constants are
used, each numerator in (3.5) is replaced by the corresponding directed row
sum.  This is preferable when a single full-operator norm destroys the
margin.

The fixed point defines

\[
 h_\xi(z_0)=u_0,qquad
 W^s_{\rm loc}(\Gamma_i(\xi))\cap\Sigma_\xi
   =\{(h_\xi(z),z)\}.                                   \tag{3.7}
\]

Applying the same contraction argument to the differentiated equations
gives joint \(C^1\) dependence on \((\xi,z)\), with explicit bounds for
\(D_zh_\xi\) and \(D_\xi h_\xi\).  Equation (1.2) then pulls this
codimension-one sheet back to the complete two-component history space.

## 4. The pulse intersection and its orientation

Write the section coordinates of the entrance history as

\[
 B_\xi(J)=(u_\xi(J),z_\xi(J))
\]

and define the signed stable-manifold gap

\[
 H(\xi,J)=u_\xi(J)-h_\xi(z_\xi(J)).                    \tag{4.1}
\]

A physical onset certificate needs a rectangle
\(\Xi_0\times[J_-,J_+]\) on which

\[
 H(\xi,J_-)<0<H(\xi,J_+),\qquad
 \partial_JH(\xi,J)\ge m_J>0,                           \tag{4.2}
\]

after fixing the orientation.  Reversing all three signs is equivalent.
The derivative used in (4.2) is

\[
 \partial_JH=
 \partial_Ju_\xi-
 D_zh_\xi(z_\xi)\,\partial_Jz_\xi.                     \tag{4.3}
\]

Thus a nonzero pulse derivative by itself is insufficient: it must be paired
with the validated stable graph.  Conditions (4.2) and the intermediate
value theorem give a unique zero \(J_c(\xi)\), and the implicit-function
theorem gives

\[
 D_\xi J_c=-\frac{D_\xi H}{\partial_JH}.                \tag{4.4}
\]

### Event-aligned stable-sheet lemma

The section entrance in (1.4) must be differentiated on its event graph,
not at a fixed terminal time.  Write \(x(t,J)\) for the released scalar
trajectory, \(Z(t,J)=\partial_Jx(t,J)\), and

\[
 g(t,J)=h_C(x_t(J)).
\]

Suppose a time interval and pulse interval have a unique event
\(g(\tau(J),J)=0\), and suppose

\[
 |\partial_tg(t,J)|\ge\sigma_C>0                         \tag{4.5}
\]

there.  The implicit-function theorem then gives

\[
 \tau_J(J)=-\frac{\partial_Jg(\tau(J),J)}
                  {\partial_tg(\tau(J),J)}.             \tag{4.6}
\]

After the last pulse and delay breakpoints have been passed, the common-event
reduced history

\[
 B(J)=\left(
  \theta\mapsto v(\tau(J)+\theta,J),
  w(\tau(J),J)
 \right),\qquad -r\le\theta\le0,                        \tag{4.7}
\]

is differentiable as a \(Y\)-valued map, with

\[
 \begin{aligned}
 D_JB_v(J)(\theta)
   & =Z_v(\tau(J)+\theta,J)
      +\dot v(\tau(J)+\theta,J)\tau_J(J),\\
 D_JB_w(J)
   & =Z_w(\tau(J),J)+\dot w(\tau(J),J)\tau_J(J).
 \end{aligned}                                          \tag{4.8}
\]

Equation (4.8) is tangent to the section by (4.6).  Thus the derivative in
(4.3) is the derivative of the event-aligned history, including the return-
time term; a fixed-time variational history is not interchangeable with it.

### Phase-invariant orientation of the unstable action

There is no need to choose an absolute phase for a complex Fourier--Grushin
cokernel row.  Let \(\ell\) be any nonzero complex representative of the
one-dimensional left eigenspace associated with the simple real unstable
multiplier, and let \(q\) be a real unstable history with
\(\ell(q)\ne0\).  For every real history \(y\), the normalized action

\[
 f(y)=\frac{\ell(y)}{\ell(q)}                         \tag{4.9}
\]

is independent of the phase or scaling of \(\ell\).  Simplicity and the
reality of the RFDE imply that the exact quotient in (4.9) is real.  This
gives the following directed reduction.  Suppose common computations give

\[
 |\ell(y)-a_0|\le r_a,\qquad
 |\ell(q)-b_0|\le r_b,\qquad |b_0|>r_b .              \tag{4.10}
\]

Then, with \(c_0=a_0/b_0\),

\[
 f(y)\in
 \left[\Re c_0-r_c,\Re c_0+r_c\right],\qquad
 r_c=\frac{r_a+|c_0|r_b}{|b_0|-r_b}.                 \tag{4.11}
\]

The sharper residual form is often preferable.  For any real \(c\), if the
same row gives \(|\ell(y-cq)|\le r\) and
\(|\ell(q)|\ge b_->0\), then

\[
 f(y)\in[c-r/b_-,c+r/b_-].                            \tag{4.12}
\]

Indeed the complex quotient lies in the disk of radius \(r_c\) about
\(c_0\), and the exact quotient is real.  The residual form follows from
\[
 f(y)-c=\frac{\ell(y-cq)}{\ell(q)}.
\]
Thus (4.11)--(4.12), rather than separate
modulus or total-variation estimates for numerator and denominator, is the
correct way to certify the sign of \(f(D_JB)\).  The numerator and
denominator must use the same Fourier row, tail enclosure, orbit enclosure,
and normalization; otherwise the phase cancellation in (4.9) has been
destroyed.

If a quantitative stable graph gives \(\|Dh\|\le L_h\), and a common
enclosure gives \(\|P_sD_JB\|\le M_s\), then

\[
 \partial_JH
 \in [f(D_JB)] +[-L_hM_s,L_hM_s].                   \tag{4.13}
\]

Consequently a positive lower endpoint of \([f(D_JB)]\) exceeding
\(L_hM_s\) proves the second inequality in (4.2); the sign-reversed version
is equivalent.  Formula (4.13) identifies the exact interface between the
Stage-5 event derivative and the Stage-4 quantitative stable graph.  A large
bound on \(\|D_JB\|\) alone cannot replace either correlated term.

Now assume the validated Riesz chart and stable graph contain every history
in \(B(I_J)\), and let \([H'](I_J)\) be an inclusion interval for the exact
derivative computed from (4.8).  If the endpoint intervals have opposite
strict signs and \(0\notin[H'](I_J)\), then the exact stable gap has one and
only one zero in \(I_J\).  Equivalently, a verified interval-Newton image

\[
 N(I_J)=m-[H(m)]/[H'](I_J)
       \subset\operatorname{int}I_J,\qquad
 m=\operatorname{mid}I_J.                              \tag{4.14}
\]

gives existence and uniqueness when the interval extensions satisfy the
standard inclusion property.  This lemma is finite-dimensional only at its
last scalar step: its premises require continuous coverage of every history
cell in (4.7), the RFDE Riesz functional, and the stable graph.

At \(J=J_c(\xi)\), the released physical trajectory converges to the inner
periodic orbit.  This is a history-space statement, not a terminal-point or
finite-section classification.

At the center parameter, the source-bound diagnostic has now selected the
third-return bracket

\[
 I_J=[0.30113,0.30114].                               \tag{4.15}
\]

Its finite coordinate changes from approximately \(7.44\times10^{-5}\) to
\(-6.50\times10^{-5}\), the nine sampled derivatives lie below \(-13.9\),
and the largest endpoint mesh-sup displacement from the inner reference is
about \(1.05\times10^{-4}\).  These are numerical targets, not enclosures.
The exact Riesz/stable-graph error decomposition, the event-time derivative,
and one conservative set of requested directed budgets are fixed in
`docs/leaky-pulse-separator-validation-contract.md`.  This removes the
choice of section and return depth from the remaining proof search; it does
not promote the crossing claim.  The pulse interval itself should be chosen
only after the quantitative stable-graph radius is known.  The independent
source-bound tradeoff diagnostic in
`docs/leaky-pulse-separator-bracket-tradeoff.md` records that the wider
binary64 interval ([0.30105,0.30120]) has minimum sampled endpoint gap
(9.08\times10^{-4}) and maximum endpoint mesh-sup displacement
(1.659\times10^{-3}).  If directed continuous-history tubes fit inside a
stable-graph ball of that size, this interval permits an endpoint-error
budget over thirteen times larger than the narrow target.  Those values are
still finite-section observations, not a covector, graph, crossing, or onset
certificate.  A subsequent directed family contract rigorously rules out a
single zero-centered tube as the way to realize this diagnostic advantage:
the full interval closes only 730 of 1152 time cells.  A center member of an
exact 30,000-shard partition closes in the weighted state norm but converts
to reduced-history error \(1.0739434\times10^{-2}>10^{-2}\), while its
first/second parameter majorants are of order \(10^6\) and \(10^{13}\) and
remain so at zero shard width.  The crossing proof must therefore retain
parameter correlation in a cellwise Taylor jet, solve the section event as
an implicit jet, pull the full history to the common event graph, and apply
the validated unstable covector and stable graph only at that stage.

The event-aligned Stage-5 contract registers all of these gates.  Its center
pilot first showed that the scaled hierarchy is well conditioned.  Stage 5B
then promoted the fixed-common-time part to a theorem: a \(192\)-bit
Taylor--Bernstein enclosure propagates
\(b_k=h^k\partial_J^kz/k!\), \(0\le k\le4\), jointly on the exact
two-origin \(1152\)-cell grid and the full interval
\([0.30105,0.30120]\).  The maximum joint coefficient error is
\(8.57254\times10^{-19}\), the exact cubic degree-five through
degree-twelve tail forcing is at most \(2.05948\times10^{-9}\), and the
full-width fifth-order remainder satisfies
\(\|R_5\|_P\le1.72064\times10^{-8}\).  An independent full recomputation
reproduces the frozen certificate.  Thus the wide fixed-time parameter
family is proved.  Stage 5C now binds the corrected exact orbit-section
level and proves exactly one positive Route-C event in the common bracket
\([555\sqrt5/24,1+546\sqrt5/24]\) for every
\(J\in[0.30105,0.30120]\).  It gives event speed at least
\(0.2133519018\), a fourth-order event-time graph with uniform remainder
\(10^{-4}\), and a continuous common-event reduced-history tube of radius at
most \(0.008199932\).  Its independent replay reproduces the certificate;
the obsolete Fourier candidate voltage is rejected as an exact section
level.  Stage 5D then differentiates the exact RFDE family rather than the
Stage-5B remainder estimate.  On all 1152 cells it closes the comparison

\[
 E'=DF(z)E+(DF(z)-DF(B))\,\partial_\xi B
       +\partial_\xi\operatorname{Tail}_{\ge5}(B)
\]

with scaled \(P\)-radius at most \(8.72890\times10^{-8}\).  It proves

\[
 T_J\in[336.6243028,456.5740939],
 \qquad
 D_JK_w(0)\in[-17.3506565,-10.1427988],
\]

and \(\|D_JK\|_Y\le142.200203\), including the event-translation term.
The current Stage-4D total-variation reduction gives only
\(|f(D_JK)|\le1017.2731\), a disk containing zero.  The stored
Grushin-normalized right column \(\widetilde q\) is complex phased even
though the exact unstable multiplier is real.  If
\(\gamma=\chi(\widetilde q)/|\chi(\widetilde q)|\) for a nonzero real test
evaluation, then the physical history and action are
\[
 q=\gamma^{-1}\widetilde q,\qquad
 f_{\rm phys}(y)=\gamma\,\frac{\ell(y)}{\ell(\widetilde q)}.
\]
Omitting \(\gamma\) gives a complex gauge quotient, not an oriented scalar.
The Stage-5E source-bound certificate retains the physical-right-gauge-
corrected common same-row residual in (4.12), combines it with (4.13), and
proves at 192-bit precision, uniformly on the full parameter interval,
\[
 f_{\rm phys,J}(D_JK_J)\in
 [-258.746521015805,-245.253478984195]\subset(-\infty,0).
\]
The proof uses 128 parameter shards and 512 history cells; its total action
radius is at most \(6.746521015805\).  Thus the fixed Route-C functional has
a strict signed parameter action.  Stable-coordinate endpoint signs, the
stable-graph correction, derivative exclusion for the true stable gap,
interval Newton, the ordinal ``third crossing,'' and unique onset remain
open.

## 5. What turns the local separator into biological onset

The stable graph separates a small section cylinder, but spectral
hyperbolicity alone does not identify the destinations of its two sides.
The following two finite routing statements are additionally required.

1. **Signed local exit.**  Until a point leaves the local cylinder, the
   signed gap keeps its sign and grows by a directed factor greater than one.
   Equivalently, one may validate invariant unstable cones for the return
   map and show that the two sides leave through disjoint compact faces
   \(E_-\) and \(E_+\).
2. **Basin attachment.**  A finite method-of-steps enclosure maps all of
   \(E_-\) into the already proved quiet Razumikhin basin and maps all of
   \(E_+\) into an explicit attracting tube around the outer periodic orbit.
   The latter tube requires a quantitative nonlinear return contraction; a
   Floquet zero count alone is not an explicit basin certificate.

These statements yield, on the declared local pulse interval,

\[
 \begin{cases}
  J<J_c(\xi) &\Longrightarrow \Phi_tK_\xi(J)\to E_q(\xi),\\
  J=J_c(\xi) &\Longrightarrow
      \operatorname{dist}(\Phi_tK_\xi(J),\Gamma_i(\xi))\to0,\\
  J>J_c(\xi) &\Longrightarrow
      \operatorname{dist}(\Phi_tK_\xi(J),\Gamma_o(\xi))\to0.
 \end{cases}                                             \tag{5.1}
\]

The presently proved \(J=0.30\) complete-history capture supplies a strict
quiet-side anchor for this argument.  A corresponding directed outer-side
capture, and the connection of both anchors to the local exit faces, remain
open.

## 6. Frequency--amplitude--safety coordinates

Let \(F(\xi)\) be the autonomous outer-orbit frequency and let \(A(\xi)\)
be its unsquared peak-to-peak voltage amplitude.  Once (4.2)--(5.1) are
proved, define the signed pulse safety coordinate

\[
 S(a,\kappa_3,J)=J-J_c(a,\kappa_3),                     \tag{6.1}
\]

with the sign chosen so that \(S>0\) is the outer-pulse side.  The full
response map is

\[
 \mathcal Q(a,\kappa_3,J)=(F,A,S).
\]

Its derivative has the exact block-triangular form

\[
 D\mathcal Q=
 \begin{pmatrix}
  D_{(a,\kappa_3)}(F,A)&0\\
  -D_{(a,\kappa_3)}J_c&1
 \end{pmatrix},
 \qquad
 \det D\mathcal Q=
 \det D_{(a,\kappa_3)}(F,A).                            \tag{6.2}
\]

Hence nonsingularity of the two-output periodic response is the exact rank
condition.  The threshold derivatives in (4.4) do not affect the determinant
but do affect the inverse norm and therefore the radius of a certified
three-output target ball.  A valid quantitative inverse theorem must retain
that dependence and the inequalities keeping the commanded pulse inside the
two routed sides and the declared physical amplitude range.

## 7. Finite-network consequence and its boundary

For a finite balanced Dobrushin network, exact synchronous histories obey the
same scalar RFDE.  The proved complete-line transverse Green inverse supplies
a topology- and dimension-uniform invertible transverse block.  Therefore:

- the synchronous pulse curve, the three scalar cycles, and the scalar onset
  value lift exactly;
- once the scalar Fredholm canard root is proved, the canonical synchronized
  Lin realization has the same root, slope, and orientation;
- transverse spectral stability is uniform in the declared diameter norm.

This does not give a topology-uniform nonlinear basin radius for asynchronous
histories.  Such robustness requires a separate nonlinear transverse tube.
The general-network theorem should state exact synchronous control first and
add asynchronous residual robustness only when that tube has been quantified.

## 8. Evidence ledger

| Ingredient | Present status |
|---|---|
| Exact reduced-history factorization and stable-set pullback | Proved |
| Smooth, injective, positively oriented physical pulse curve | Proved |
| Explicit large quiet Razumikhin basin | Proved |
| Complete-history capture for \(J=0.30\) | Proved |
| Nonexplicit quiet pulse interval around \(J=0.30\) | Proved by strict interior capture and continuous dependence; no explicit endpoint is claimed |
| Inner/outer periodic orbit existence on a common parameter box | Proved |
| Neutral multiplier simplicity and infinite-tail Riesz reduction | Proved |
| Complete-line transverse inverse for every admitted finite network | Proved |
| Nonlinear network synchronization and quadratic collective defect | Proved conditionally on strip residence: \(M(t)\le M_0e^{-(t-t_0)/10}\), \(|R_{\rm coll}(t)|\le(703/200)\mathcal H_M(t)^2\) with the sharper componentwise delayed formula, and accumulated defect \(\le(703/40+27\sqrt5/800)M_0^2\le(56483/3200)M_0^2\) |
| Conditional asynchronous routing/threshold transfer | Proved as an implication: a scalar forced-route budget, strip margin and product-basin lift give the exact strict rational network budget \(R_0<\min\{d_{\rm strip},d_{\rm lift}\}\), \(L_0R_0+(56483/3200)R_0^2<\eta_{\rm route}\); monotone gap-response bounds give \(|J_{c,N}-J_c|\le\epsilon_H/m_J\).  Every scalar/lift/gap constant and every concrete radius remain open |
| Center inner one-unstable Floquet count | Proved: translation count (1), simple positive-root count (1), complementary keyhole count (0) |
| Qualitative center inner stable manifold | Proved: \(C^1\), codimension one in full history and in the reduced abstract phase section; no quantitative radius or pulse section |
| Center inner quantitative stable spectral gap | Proved: the source-bound base and extension trees give \(\rho_s\le e^{-0.01}=0.9900498337\ldots<1\).  The Route-C projection audit gives \(\|P_s\|\ge2\) and rejects the old scalar \(C_N=10\) row.  Stage 4C/4D prove the atom-plus-density adjoint, Fourier reversal, summable continuous measure, nonzero normalization and recovery-history action.  Stage 4E gives a 1042-cell physical-time \(V_{qq}\) tube and direct same-row deflation, proving the base-orbit block \(C^{uu}_{s,\mathrm{base}}\le7.905649079<12\) with total correlated action error \(1.50030\times10^{-6}\).  Stage 4G computes the required uniform Lipschitz cap \(2408.441719\) and rigorously rejects the positive scalar inflation route at cell 581.  Stage 4H proves the four-word support and forms the rank-one/event row before total variation; its small stable-row norm remains sampled.  Stage 4I proves the five local primitive residuals, the unprojected physical-frame inflation no-go, and a mixed-norm primitive ingress \(1.46355\times10^{-3}\), but not the common complete-history signed row.  Stage 4J specifies the noncircular projected-residual closure, including history transport and the terminal event factor.  Uniform split-ball inflation, the other five Hessian blocks, stable power, split-return tube and final six-block quantitative graph remain open |
| Explicit orbit-section admissibility | Proved: a phase-zero voltage section has speed at least \(0.2067539137\ldots\) on its radius-\(0.01\) section ball, and the old binary64 voltage level has a unique nearby true-orbit crossing; this is not a physical pulse/stable-sheet crossing |
| Wide Route-C physical-pulse family | The old zero-centered family fails after 730 of 1152 cells and its zero-width derivative wrapping remains structural.  Stage 5B replaces it with a correlated scaled parameter Taylor model and proves the full fixed-common-time family on all 1152 cells and \(J\in[0.30105,0.30120]\), with joint coefficient error below \(8.58\times10^{-19}\) and full-width \(R_5\) radius below \(1.73\times10^{-8}\) |
| Event-aligned pulse parameter jet | Stage 5C proves the corrected exact Route-C section level, a unique positive event in the common bracket for the full \(J\)-interval, speed at least \(0.2133519018\), a fourth-order event-time graph with remainder \(10^{-4}\), and a continuous common-event \(Y\)-history tube of radius at most \(0.008199932\).  Stage 5D directly encloses the first variational equation on all 1152 cells, proves \(T_J\in[336.6243028,456.5740939]\), retains the event-translation term, and proves a continuous event-aligned \(D_JK\) with \(\|D_JK\|_Y\le142.200203\).  Its total-variation output alone is only \(|f(D_JK)|\le1017.2731\).  Stage 5E fixes the physical real right gauge and proves with 128 parameter shards, 512 history cells and 192-bit outward arithmetic that \(f_{\rm phys,J}(D_JK_J)\in[-258.746521015805,-245.253478984195]\) uniformly on the full \(J\)-interval.  This proves strict signed action for the fixed Route-C functional.  The stable-graph correction, third-crossing identity, endpoint stable-gap signs, interval-Newton onset and routing remain open |
| Outer zero-unstable count and both common-box index continuations | Open.  The full bordered Grushin inverse closes on the local disk, but its scalar Rouch\'e comparison fails because of the bottom-row back-substitution.  A seam-free exact staircase still leaves a nonempty 5,000-cell complement frontier.  Outer capture is therefore being attacked directly through the phase-fixed return operator rather than waiting for a global zero count |
| Narrow third-return pulse bracket and explicit directed error budget | Source-bound numerical target; not directed |
| Quantitative Lyapunov--Perron stable graph and pulse crossing | Open.  A three-mesh long-double six-block pilot closes the structured \(2\times2\) majorant with Perron value \(0.04913\), positive self-map slack and graph height about \(8.25\times10^{-6}\).  It is not outward-rounded and has no continuous-history error bound; sensitivity identifies the stable-output/\(uu\)-input block as the strict priority |
| Outer local nonlinear ingredients | Proved on a radius-\(0.01\) history tube: \(\|R_F(\eta)\|\le3.50816330348\|\eta\|_X^2\) and \(\|D^2F\|\le7.02973994029\) |
| Directed \(J=0.32\) outer ambient attachment | Proved.  The unique third positive declared-section event lies in \([94.9619021653635192071,94.9619021653635201635]\), and the complete ambient \(X\)-history is within \(2.637078616900037\times10^{-5}\) of the exact outer phase-zero history, inside radius \(10^{-4}\) by \(7.362921383099962\times10^{-5}\).  It is explicitly not a same-exact-section or basin statement |
| Outer attracting tube and two-sided routing | Conditional contract proved: \(K_o\rho_o^m+C_mr_o<1\), the signed factor \(\delta_+=a(\delta,z)\delta\), correct overshoot slabs and both attachment inequalities are executable.  Stage 2 rigorously subtracts phase before total variation on the exact stored 360-step matrix and proves \(Q_{v,h}\le0.126907895\), \(Q_{w,h}\le0.002760008\), cancellation factor \(>40.73\), and margin \(>0.873092105\).  Stage 3 proves the first continuous Volterra shards; Stage 3B shows that direct positive global tiling would require roughly \(1.05\times10^6\) coarse tasks.  Stage 3C compresses the exact kernel to 21 depth-two words, Stage 3D reduces them to eight one-dimensional \(F,G,H,L\) primitives, and Stage 3E proves global exact-orbit \(F,G\) multiplicative errors below \(0.0051\).  Stage 3F proves the combined advanced-row identity, strict instantaneous Green/boundary bounds and exact coefficient/phase-ratio budgets.  The first Stage-3G/3H global runs are audit-retracted because their 730+20 rectangle geometry omitted the second terminal-clipped cell in every delta strip; the corrected target is 730+40 rectangles and 12,320 patches.  Their old residual, Green and row-size values are diagnostic only.  Global \(E_v,E_w\), nonlinear phase chart, return tube, exit cylinder and face attachments remain open |
| Directed \((a,\kappa_3)\mapsto(F,A)\) local inverse | Proved branchwise on the common box; the outer target radius is at least \(4.5363124943378087\times10^{-12}\) |
| \((F,A,S)\) target ball and concrete asynchronous network robustness | The exact block inverse, threshold-adapted product bijection, fixed actuator-box radius formula, pulse-interval containment and safety erosion \(|S_0|-\rho_S>\epsilon_H/m_J+e_J\) are proved in the biological-safety control contract.  The numerical radius is null because \(J_c,D_\xi J_c,m_J,\epsilon_H\), routing and product-lift constants are not yet all validated |

The theorem in (5.1), followed by the quantitative inverse based on (6.2),
is the required biological-control result.  None of the open rows can be
replaced by a sampled orbit, a finite-section eigenvector, or a pointwise
terminal classification.
