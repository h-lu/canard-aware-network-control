# Stage 4O: analytic contract for the event-aligned return Hessian

Status: **OPEN ANALYTIC CONTRACT.** All numerical theorem ingress is null,
and every return, Hessian, graph, crossing, onset, routing, capture, and safety
claim remains false.

Stage 4O gives the exact analytic spine needed between the Stage-4N nonlinear
event family and the six Stage-4M projected Hessian blocks. It also isolates a
previously implicit regularity gate: the one-period moving-history return is
not automatically $C^2$ on the full ball of arbitrary continuous histories.
The recommended repair is a selected near-two-period return with a uniform
$T_2>2\tau_{\max}$ smoothing margin, followed by a new two-period six-block
majorant.

The executable source is
[leaky_inner_event_aligned_return_hessian_stage4o_contract.py](../src/canard_control/leaky_inner_event_aligned_return_hessian_stage4o_contract.py),
the atomic generator is
[leaky_inner_event_aligned_return_hessian_stage4o_contract.py](../experiments/leaky_inner_event_aligned_return_hessian_stage4o_contract.py),
and the source-bound result is
[leaky_inner_event_aligned_return_hessian_stage4o_contract.json](../experiments/results/leaky_inner_event_aligned_return_hessian_stage4o_contract.json).

Stage 4O byte-binds and normally validates Stage 4I, Stage 4L, Stage 4M,
Stage 4N, and the Stage-4N feasibility diagnostic. The formulas below are
exact conditional identities. They do not fill any numerical field.

## 1. Reduced model and fixed-time flow jets

The reduced history space is

\[
Y=C([-\tau_{\max},0],\mathbb R)_v\times\mathbb R_w,
\qquad
S_t(x)=\bigl(\theta\mapsto v_x(t+\theta),w_x(t)\bigr).
\]

For $\phi=(\phi_v,w)\in Y$, the physical-time field is

\[
\begin{aligned}
F_v(\phi,w)={}&\phi_v(0)-\frac{\phi_v(0)^3}{3}-w
 +\varepsilon\kappa_1
 \left\{\frac{\phi_v(-\tau_0)+\phi_v(-\tau_1)}2-\phi_v(0)\right\}\\
&+\varepsilon\kappa_3
 \left\{\frac{(\phi_v(-\tau_0)-1)^3+(\phi_v(-\tau_1)-1)^3}{2}
 -(\phi_v(0)-1)^3\right\},\\
F_w(\phi,w)={}&\varepsilon(\phi_v(0)-a-w).
\end{aligned}
\]

Write $v_0=\phi_v(0)$ and $v_j=\phi_v(-\tau_j)$. The first derivative is

\[
\begin{aligned}
[DF(\phi,w)h]_v={}&
\left[1-v_0^2-\varepsilon\kappa_1
-3\varepsilon\kappa_3(v_0-1)^2\right]h_v(0)-h_w\\
&+\sum_{j=0}^1\frac{\varepsilon}{2}
 \left[\kappa_1+3\kappa_3(v_j-1)^2\right]h_v(-\tau_j),\\
[DF(\phi,w)h]_w={}&\varepsilon(h_v(0)-h_w).
\end{aligned}
\]

The only nonzero second derivative is the fast row:

\[
D^2F_v(\phi,w)[h,k]
=c_0(\phi)h_v(0)k_v(0)
 +\sum_{j=0}^1c_j(\phi)h_v(-\tau_j)k_v(-\tau_j),
\tag{1.1}
\]

where

\[
c_0=-2v_0-6\varepsilon\kappa_3(v_0-1),
\qquad
c_j=3\varepsilon\kappa_3(v_j-1).
\tag{1.2}
\]

The corresponding third derivatives are

\[
-2-6\varepsilon\kappa_3,
\qquad
3\varepsilon\kappa_3
\quad(j=0,1),
\tag{1.3}
\]

with all mixed and slow-row entries zero.

For initial directions $h,k\in\Sigma_0$, the fixed-time jets solve

\[
\begin{aligned}
\dot U_h(t)&=DF(X_t)U_{h,t},\qquad U_{h,0}=h,\\
\dot V_{hk}(t)&=DF(X_t)V_{hk,t}
 +D^2F(X_t)[U_{h,t},U_{k,t}],\qquad V_{hk,0}=0.
\end{aligned}
\tag{1.4}
\]

The zero second initial jet is essential: the injection of the initial
history is affine. The fast quadratic forcing is exactly

\[
b_{hk}(t)=c_0(t)u_h(t)u_k(t)
 +\sum_{j=0}^1c_j(t)u_h(t-\tau_j)u_k(t-\tau_j),
\tag{1.5}
\]

and the slow forcing is zero. If $\mathcal U_x(r,s)$ denotes the retarded
fixed-time propagator, then

\[
V_{hk}(r)=\int_0^r\mathcal U_x(r,s)e_v b_{hk}(s)\,ds.
\tag{1.6}
\]

Equations (1.1)--(1.6) give the exact fixed-time $D^2$ formula. They still
need a common regular flow domain and directed kernel enclosure.

## 2. Implicit selected-event derivatives

Let

\[
G(t,x)=v_x(t)-X_{*,v}(0),
\qquad
\ell_0(y)=y_v(0),
\]

and let $T(x)$ be one selected event branch in a common window. Set

\[
a(x)=\partial_tG(T(x),x)=\dot v_x(T(x)).
\]

A uniform lower bound (a(x)\ge a_*>0) is the single denominator gate. With

\[
n_h=\ell_0(U_h^T)=u_{h,v}(T),
\]

the first derivative is

\[
T_h=-\frac{n_h}{a}.
\tag{2.1}
\]

For every returned-history coordinate, define terminal histories by

\[
Y^T(\theta)=Y(T+\theta),
\qquad -\tau_{\max}\le\theta\le0,
\]

with the recovery coordinate always evaluated at the current returned time
$T$. Form

\[
Z_{hk}
=V_{hk}^T
-\frac{\dot U_h^T n_k+\dot U_k^T n_h}{a}
+\frac{\ddot X_T n_hn_k}{a^2}.
\tag{2.2}
\]

Equivalently,

\[
Z_{hk}=V_{hk}^T+\dot U_h^T T_k+\dot U_k^T T_h
 +\ddot X_TT_hT_k.
\]

The second event derivative is

\[
T_{hk}=-\frac{\ell_0(Z_{hk})}{a}.
\tag{2.3}
\]

If (2.2)--(2.3) are fully expanded, inverse powers through $a^{-3}$ occur
in the returned Hessian. A validator must therefore retain one correlated,
strictly positive enclosure of the same denominator; separately rounded
quotients are not a faithful substitute.

## 3. Complete terminal translation and one phase projection

Define the moving event-phase projection

\[
\Pi_xY=Y-\dot X_T\frac{\ell_0(Y)}{a(x)}.
\tag{3.1}
\]

Then the two exact return derivatives are

\[
DP(x)h=\Pi_xU_h^T,
\qquad
D^2P(x)[h,k]=\Pi_xZ_{hk}.
\tag{3.2}
\]

Equivalently, for every $\theta\in[-\tau_{\max},0]$,

\[
D^2P(x)[h,k](\theta)
=Z_{hk}(\theta)+\dot X(T+\theta)T_{hk}.
\tag{3.3}
\]

The phase projection in (3.1) is applied exactly once. Applying it again to
(3.3) double-counts the moving-event correction. The identities

\[
\ell_0(DP(x)h)=0,
\qquad
\ell_0(D^2P(x)[h,k])=0
\]

are exact consistency checks. The event-phase projection $\Pi_x$ is not the
fixed stable deflation $P_s$.

## 4. Fixed splitting and the six blocks

Use the Stage-4M fixed unit-$Y$ pair

\[
\widehat q=\frac{q}{\|q\|_Y},
\qquad
\widehat f=\|q\|_Yf,
\qquad
P_s=I-\widehat q\widehat f,
\qquad
E_s=\ker\widehat f.
\]

For $a,b\in\{s,u\}$, inject stable inputs as themselves and the unstable
scalar as $\widehat q$, and set

\[
H_{ab}(x)=\Pi_xZ_{I_a,I_b}.
\]

The required six outputs are

\[
\begin{array}{lll}
B_s^{ss}=P_sH_{ss},&B_s^{su}=P_sH_{su},&B_s^{uu}=P_sH_{uu},\\
B_u^{ss}=\widehat f(H_{ss}),&
B_u^{su}=\widehat f(H_{su}),&
B_u^{uu}=\widehat f(H_{uu}).
\end{array}
\tag{4.1}
\]

Input symmetry identifies $su$ and $us$, but it does not identify the two
output rows. Thus all six blocks remain necessary. The correct order is

\[
\text{fixed-time source}
\longrightarrow\text{event quotient}
\longrightarrow\Pi_x
\longrightarrow(P_s\text{ or }\widehat f)
\longrightarrow\text{one final norm}.
\tag{4.2}
\]

In particular, the raw Hessian, event correction, and rank-one stable
deflation may not be normed separately.

## 5. Direct signed-kernel route

Let $L_{x,m}(s)$ be the first-variation row

\[
L_{x,m}(s)h=u_{h,v}(s-\tau_m),
\qquad \tau_{\mathrm{current}}=0.
\]

The quadratic source is the signed tensor kernel

\[
\sum_m c_m(x,s)L_{x,m}(s)\otimes L_{x,m}(s).
\tag{5.1}
\]

Substitute (5.1) into (1.6), retain $n_h,n_k,a,\dot U,\ddot X$ in the same
object, apply (3.1), and finally apply one of the two rows in (4.1). This
produces a signed atom--density--bimeasure representation of each projected
bilinear block. Only after all these correlations are formed is a total
variation or operator norm taken.

This route has an important logical consequence:

- a standalone scalar certificate
  $\sup_{x,t}\|U_x(t,0)P_s\|$ is not necessary;
- the old scalar $K_{\rm ret}<188.9122238810$ target is also only a
  sufficient cancellation-blind ambient route, not a necessary condition;
- nevertheless, the first-variation rows $L_{x,m}(s)$ must be validated for
  every intermediate source time and delayed slot. The scalar norm can be
  avoided; the continuous correlated kernel cannot.

Stage 4I supplies the exact center four-word algebraic skeleton
$F,G,C_0,C_1,C_{00}$. It does not supply the nonlinear uniform kernel.
Stage 4L supplies a center terminal linear row and the fixed normalization. It
does not supply the intermediate rows inside (5.1).

## 6. The one-period $C^2$ obstruction

The Stage-4M domain contains arbitrary continuous stable histories. For a
moving return, (2.2) contains

\[
\ddot v_x(T(x)+\theta)T_hT_k
\quad\text{for every }\theta\in[-\tau_{\max},0].
\tag{6.1}
\]

Stage 4L proves both

\[
T-\tau_{\max}>0,
\qquad
T<\tau_0+\tau_1,
\qquad \tau_{\max}=\tau_1.
\]

The first inequality removes the unadvanced identity block from the *linear*
returned history. It does not imply the $C^2$ time smoothing needed in
(6.1). At $\theta=-\tau_1$, differentiating the field at $T-\tau_1$
reads the $\tau_0$-slot at

\[
T-\tau_1-\tau_0<0.
\]

An arbitrary $C$-history has no controlled derivative at that point.
Consequently the current one-period contract may not assert that the moving
complete-history return is $C^2$ on the whole arbitrary-$C$ ball.

Possible repairs are:

1. transfer the splitting and graph theorem to a compatible $C^1$
   solution-history manifold with a norm controlling translation;
2. use a later return whose whole returned history lies beyond the necessary
   smoothing time;
3. construct an equivalent fixed-phase quadratic-remainder theorem that does
   not invoke the unsupported moving translation derivative.

No repair is validated here.

## 7. Recommended near-two-period route

For a second selected event time $T_2$, the exact smoothing threshold is

\[
T_2-\tau_{\max}>\tau_{\max},
\qquad\text{equivalently}\qquad
T_2>2\tau_{\max}.
\tag{7.1}
\]

This threshold, not merely $T_2>\tau_{\max}$, is what places every output
history coordinate beyond the time at which $\ddot X$ is available for
arbitrary continuous initial histories. The frozen center intervals give the
strict directed margin

\[
2T_- -2\tau_{\max,+}
>14.0117401232539450216096720156478351743.
\]

Thus the center two-period branch has ample smoothing room. A nonlinear
theorem still needs a common window satisfying $T_{2,-}>2\tau_{\max}$ on
the full anisotropic ball.

One sufficient algebraic transfer route uses nested local domains
$D_0,D_1$ on which $P$ is defined, with $P(D_0)\subset D_1$, and proves

\[
Q=P\circ P\quad\hbox{on }D_0,
\qquad
T_2(x)=T_1(x)+T_1(P(x)).
\tag{7.2}
\]

No forward-invariant full neighborhood of a saddle is required or expected.
Under (7.2), $DQ(X_*)=A^2$. Moreover,

\[
W^s(Q)=W^s(P).
\]

convergence of the even iterates implies convergence of the odd iterates by
continuity of $P$. Local graph uniqueness therefore gives the same stable
sheet germ.

Identity (7.2) is sufficient but not necessary for the intrinsic stable
sheet. A direct $Q$ also suffices if it is proved to be the unique near-
$2P$ section return of the same semiflow, its return times are uniformly
positive and bounded, and convergence of its iterates is proved equivalent
to convergence to the periodic orbit along all intervening flow arcs. This
semiflow stable-set identification constructs the same stable-set germ
without first proving $Q=P^2$. The composition identity is still needed if
one wants literal identity with the chosen one-period branch or its ordinal
label.

The Stage-4M one-step caps cannot simply be reused. The two-period proof must
recompute the squared stable and inverse-unstable rates, all six projected
$D^2Q$ caps, and their common majorant. No-earlier-hit is still unnecessary
for the selected $Q$-graph; it is needed only to call a branch the physical
first local return.

An unbound $N=180$ finite-section calculation gives the encouraging row

\[
(4.27\!\times\!10^{-8},\;5.20\!\times\!10^{-7},\;30.2781,
 0.59394,\;0.56667,\;158.5393),
\]

with tentative caps
$(10^{-6},10^{-5},35,0.7,0.7,180)$. With squared rates, the same pilot
reports Perron bound $0.02356$, graph height $1.743\times10^{-5}$, and
$\|D\psi\|\approx0.003086$. Its ambient row sum is about $337$, above the
old scalar $K_{\rm ret}$ target, while the split-correlated six-block
majorant still closes. These numbers are heuristic design evidence only; no
one enters the Stage-4O theorem ledger.

## 8. Minimum sufficient certificate

For the six selected-branch Hessian blocks, a closing certificate needs:

1. a Banach domain on which the moving complete-history return is $C^2$,
   preferably supplied by (7.1);
2. one nonlinear base-flow tube over every source time, delayed slot, output
   phase, activation face, and seam;
3. a common selected-event bracket, strict endpoint signs, a uniform positive
   speed denominator, and returned local-patch containment;
4. signed first-variation kernels for arbitrary unit stable inputs and the
   fixed $\widehat q$;
5. the $ss,su,uu$ quadratic source/response kernels with the $D^3F$
   perturbation remainder;
6. correlated enclosures of (a,n_s,n_u,\dot U,\ddot X,Z,
   \ell_0Z);
7. complete-history phase projection followed by fixed $P_s/\widehat f$
   output, including normalization and tails;
8. all six strict cap tests from one run and one recalibrated majorant.

A launch collar and the Stage-4N disjunctive no-earlier cover are an additional
ninth condition only for the *first physical local return* label. They are not
needed to define the Hessian of a unique selected event branch.

## 9. Executable next task

The next numerical task should be a Stage-4P near-two-period signed
bilinear-kernel pilot:

- extend the method-of-steps kernel cover through (2T);
- assemble the direct $ss,su,uu$ kernels over every source and output-phase
  cell;
- apply the event phase projection once, then $P_s$ or $\widehat f$, before
  directed bimeasure norms;
- report the six center $Q$-blocks, dominant cells, denominator ledger,
  squared-rate majorant, and headroom below new $Q$-specific caps;
- do not infer a nonlinear-ball theorem from the center pilot.

The uniform successor must then validate a common selected $T_2$ branch,
the strict smoothing gate $T_{2,-}>2\tau_{\max}$, either the identity
$Q=P^2$ on nested domains or the direct semiflow stable-set alternative,
and the nonlinear base/kernel perturbation cover.

## 10. Claim boundary

Stage 4O proves only the formal chain-rule identities, their dependency
order, the selected-versus-first-return distinction, and the source-bound
diagnosis of the missing regularity adapter. It proves none of the following:

- a $C^2$ moving return on the enlarged arbitrary-$C$ ball;
- a common one- or two-period selected event branch;
- a nonlinear return tube or no-earlier-hit cover;
- any signed kernel or any one of the six Hessian bounds;
- a quantitative stable graph, crossing, onset, routing, capture, or safety
  theorem.

The generator validates all five parents and the complete false/null ledger
before an fsynced atomic replacement. Hostile tests reject any filled numeric
field, duplicated phase correction, promotion of one Hessian block, reuse of
one-step caps without recalibration, or conflation of a selected event with a
first physical return.
