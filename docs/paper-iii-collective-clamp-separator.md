# A collective-recovery-clamped complete-history separator

Status: **Gate R-S for the unforced reset remains open.  It is neither
proved nor disproved here.  A frozen-saddle RFDE stable-manifold argument
does not apply to that protocol because the collective recovery coordinate
drifts after release, and fixed-layer persistence loses control in the
exponentially thin set that can reach the next fold before ejection.  For a
modified causal protocol that clamps only the collective recovery coordinate
until a channel is reached, the complete-history separator theorem below is
proved for every sufficiently small fixed positive \(\delta\); its local
neighborhood may depend on \(\delta\).  A delay-independent
small-gain test proves that the clamped RFDE has exactly one unstable
characteristic root.  Uniformity as \(\delta\downarrow0\) requires the
additional strong-unstable domination estimates stated in Theorem 5.2; it
does not require, and in general cannot have, a uniform stable spectral gap.**

The exact controller, equilibrium-IFT, spectral small-gain, finite-deadband,
and long-delay spectral identities are executable in
`src/canard_control/clamped_reset_separator.py`, with regressions in
`tests/test_clamped_reset_separator.py`.  This note does not modify the
frozen JNS manuscript.

## 1. Why the existing local argument stops

For the released physical system the recovery modes satisfy

\[
 \dot\rho=\varepsilon(\xi-\mu),
 \qquad
 \dot\kappa=\varepsilon\zeta-D_w\kappa .
\tag{1.1}
\]

Fix the bistable layer \(\rho_0=-1/2\), and let \(v^m(\rho_0)\) be its
singular fast saddle.  Its critical coordinate is denoted
\(\xi^m=\ell^T(v^m-v_*)\).  The constant saddle history used by a frozen
layer calculation has

\[
 \dot\rho(0)=\varepsilon(\xi^m-\mu).
\tag{1.2}
\]

Except at the exceptional tuning \(\mu=\xi^m\), this history is not an
equilibrium, a complete saddle orbit, or an invariant history.  At the
layer used in the paper \(\xi^m=-0.8551591\ldots\), whereas the local fold
unfolding is near zero.  The decimal is only diagnostic; the obstruction is
the exact identity (1.2).

This distinction matters arbitrarily close to a putative threshold.  In a
frozen saddle chart an unstable coordinate has the leading behavior

\[
 u(t)=u_0e^{\lambda_ut}(1+o(1)),
 \qquad \lambda_u>0,
\tag{1.3}
\]

so the time needed to reach a fixed exit face is

\[
 T_{\rm ex}(u_0)
 =\lambda_u^{-1}\log\frac{c}{|u_0|}+O(1).
\tag{1.4}
\]

During this time the recovery displacement is of order

\[
 \varepsilon T_{\rm ex}(u_0).
\tag{1.5}
\]

It is uniformly small only outside an exponentially thin layer.  If
\(|u_0|=e^{-A/\varepsilon}\), (1.5) is order one.  Such a trajectory can
reach the lower fold of the saddle critical branch before the frozen-layer
ejection argument decides its channel.  Determining its outcome is exactly
a slow-passage and exchange problem.

> **Proposition 1.1 (scope of a local saddle argument).**  The identities
> (1.2)--(1.5) imply the following.
>
> 1. The equilibrium stable-manifold theorem for the frozen fast RFDE
>    cannot be applied to the unforced released history unless an invariant
>    reference orbit replacing the frozen saddle is first constructed.
> 2. Fixed-fast-time persistence decides the pulse and quiet outcomes only
>    for offsets bounded away from the shrinking central layer.  It cannot
>    decide all nonzero offsets in a neighborhood of zero.
> 3. A proof based on a nonautonomous exponential trichotomy along a
>    saddle-tracking history would also need continuation to the fold,
>    signed passage through the exponentially thin layer, and capture by
>    the two channel blocks.  Those conclusions are Gate R-S rather than
>    consequences of a local stable-manifold theorem.

The proposition does **not** assert that the unforced transition set is
nonunique.  It identifies why the results currently proved for that
protocol do not imply uniqueness.  A full saddle-slow-manifold exchange
theorem could still close Gate R-S.

## 2. Long delay and the missing uniform stable gap

There is a second, independent uniformity issue.  Weak coupling does not
make the long-delay RFDE a regular perturbation in the stable spectral gap.
The scalar diffusive equation

\[
 \dot y(t)=-ay(t)+c_\delta[y(t)-y(t-\theta/\delta)],
 \qquad c_\delta=\delta^2kb,
\tag{2.1}
\]

with \(a,k,b,\theta>0\) is already enough to see this.  Put
\(a_0=a-c_\delta>0\), \(\tau=\theta/\delta\).  Its characteristic roots
include

\[
 \lambda_{j,\delta}
 =-a_0+\frac1\tau
 W_j\!\left(-c_\delta\tau e^{a_0\tau}\right),
\tag{2.2}
\]

where \(W_j\) is a Lambert branch.  Direct substitution proves (2.2).  For
small \(\delta\), the argument is real and less than \(-e^{-1}\).  With
the standard branch convention, \(W_0\) and \(W_{-1}\) are conjugate there,
so

\[
 \lambda_{-1,\delta}=\overline{\lambda_{0,\delta}}.
\tag{2.3}
\]

The elementary expansion
\(W_j(z)=\log_jz-\log(\log_jz)+o(1)\) gives

\[
 \frac{\operatorname{Re}\lambda_{j,\delta}}
 {\frac\delta\theta\log(\delta^2kb/a)}\longrightarrow1,
 \qquad j\in\{0,-1\}.
\tag{2.4}
\]

In particular both real parts are negative and converge to zero.  The
conjugacy, characteristic residual, and ratio in (2.4) are tested
independently in the executable audit.

Thus a claim of a \(\delta\)-independent stable decay rate cannot follow
from the scaling \(c_\delta=O(\delta^2)\) alone.  This is the elementary
version of the strong/pseudo-continuous spectral split for large-delay
equations.  It agrees with the large-delay spectral analysis of
[Lichtner--Wolfrum--Yanchuk](https://doi.org/10.34657/3362).

For every fixed \(\delta>0\), hyperbolicity still gives an ordinary RFDE
stable manifold.  What fails automatically is uniformity of the stable
decay constants as \(\delta\downarrow0\).  The exact separator below uses
the strong unstable direction; its uniform version is therefore stated in
terms of unstable domination over a center-stable complement, not a
uniformly negative stable gap.

## 3. The minimal causal repair

The neutral recovery mode in (1.1) is \(\rho\).  It is enough to control
that one scalar.  In the physical two-component recovery equation, apply
the actuator

\[
 u_w(t)=r u_\rho(t),
 \qquad
 u_\rho(t)=-\varepsilon(\xi(t)-\mu).
\tag{3.1}
\]

The dual modal identities \(\ell^Tr=1\) and \(m^Tr=0\) give

\[
 \ell^Tu_w=u_\rho,
 \qquad m^Tu_w=0.
\tag{3.2}
\]

Consequently

\[
 \dot\rho=\varepsilon(\xi-\mu)+u_\rho=0,
 \qquad
 \dot\kappa=\varepsilon\zeta(v)-D_w\kappa.
\tag{3.3}
\]

Thus the actuator does not directly drive \(\kappa\); the transverse
recovery remains physical.

The repaired protocol is:

1. choose \(\rho_0=-1/2\) and clamp \(\rho=\rho_0\);
2. for at least one maximal delay, clamp voltage at a declared setpoint and
   initialize \(\kappa=\varepsilon\zeta/D_w\), so the complete history is
   known and constant;
3. release voltage but retain only the scalar actuator (3.1);
4. remove the clamp when the trajectory first enters the pulse or quiet
   passage block.

This is causal: the controller uses only the current voltage coordinate.
It is also weaker than clamping both recovery variables.

With \(w=w_*+r\rho_0+q\kappa\), the decision-stage equation is

\[
\begin{aligned}
 \dot v={}&f(v,w_*+r\rho_0+q\kappa)
 +\varepsilon K\left[Bv(t)
 -\sum_{j=0}^1C_j^\eta v(t-\tau_j)\right],\\
 \dot\kappa={}&\varepsilon\zeta(v)-D_w\kappa,
 \qquad \rho(t)\equiv\rho_0.
\end{aligned}
\tag{3.4}
\]

At a constant history the diffusive delay term vanishes.  The equilibrium
equations are therefore

\[
 f(v,w_*+r\rho_0+q\kappa)=0,
 \qquad
 \varepsilon\zeta(v)-D_w\kappa=0.
\tag{3.5}
\]

> **Lemma 3.1 (exact clamped saddle branch).**  Let \(v^m(\rho_0)\) be the
> singular middle equilibrium and let
> \(A_m=D_vf(v^m,w_*+r\rho_0)\).  Since \(A_m\) is a saddle matrix,
> \(\det A_m\ne0\).  For all sufficiently small \(\varepsilon\), (3.5)
> has a unique smooth solution
> \((v^m_\varepsilon,\kappa^m_\varepsilon)\) near
> \((v^m,0)\), and
> \[
>  v^m_\varepsilon=v^m+O(\varepsilon),
>  \qquad
>  \kappa^m_\varepsilon
>  =\frac{\varepsilon}{D_w}\zeta(v^m_\varepsilon).
> \tag{3.6}
> \]
> The corresponding constant complete history is an exact equilibrium of
> (3.4), for every delay length, \(K\), and \(\eta\).

**Proof.**  At \(\varepsilon=0\), the Jacobian of (3.5) with respect to
\((v,\kappa)\) has determinant

\[
 -D_w\det A_m\ne0.
\tag{3.7}
\]

The implicit-function theorem gives (3.6).  The identity
\(B=C_0^\eta+C_1^\eta\) makes the delayed feedback zero on every constant
history, proving the last assertion. \(\square\)

Choose a \(C^2\) reset curve

\[
 \gamma_\varepsilon(0)=v^m_\varepsilon,
 \qquad
 \kappa_\varepsilon(a)
 =\frac{\varepsilon}{D_w}\zeta(\gamma_\varepsilon(a)).
\tag{3.8}
\]

After the final hold, the released complete history in
\(\mathcal X_\delta=C([ -\tau_*,0],\mathbb R^3)\) is

\[
 \mathcal R_{\varepsilon,\delta}(a)(s)
 =\bigl(\gamma_\varepsilon(a),\kappa_\varepsilon(a)\bigr),
 \qquad -\tau_*\le s\le0.
\tag{3.9}
\]

In particular, \(\mathcal R_{\varepsilon,\delta}(0)\) is exactly the
equilibrium history from Lemma 3.1.  There is no preparation error at the
candidate separator.

## 4. A checkable one-unstable-root condition

Let \(\mathcal A_\varepsilon\) be the non-delay linearization of the
\((v,\kappa)\) part of (3.4), excluding the diffusive feedback.  Embed
\(B,C_j^\eta\) in the voltage block of three-by-three matrices
\(\mathcal B,\mathcal C_j^\eta\).  The characteristic matrix is

\[
 \Delta_\delta(z)=zI-\mathcal A_\varepsilon
 -\varepsilon K\mathcal B
 +\varepsilon K\sum_j\mathcal C_j^\eta e^{-z\tau_j}.
\tag{4.1}
\]

Use any subordinate matrix norm and put

\[
 R_0=\sup_{\omega\in\mathbb R}
 \|(i\omega I-\mathcal A_\varepsilon)^{-1}\|,
 \qquad
 L=\|\mathcal B\|+\sum_j\|\mathcal C_j^\eta\|.
\tag{4.2}
\]

> **Lemma 4.1 (delay-independent unstable-index test).**  Suppose
> \(\mathcal A_\varepsilon\) has exactly one eigenvalue in
> \(\operatorname{Re}z>0\), no eigenvalue on the imaginary axis, and
> \[
>  \varepsilon|K|LR_0<1.
> \tag{4.3}
> \]
> Then (4.1) has exactly one characteristic root in
> \(\operatorname{Re}z>0\), counted with algebraic multiplicity, and none
> on the imaginary axis.  The unstable root is real and simple.  Condition
> (4.3) is independent of the delay lengths.

**Proof.**  Switch on the diffusive term with a homotopy parameter
\(s\in[0,1]\).  On \(z=i\omega\), factor the characteristic matrix as

\[
 (i\omega I-\mathcal A_\varepsilon)
 \left[I+(i\omega I-\mathcal A_\varepsilon)^{-1}E_s(i\omega)\right],
\]

where

\[
 \|E_s(i\omega)\|
 \le s\varepsilon|K|L.
\]

The second factor is invertible by (4.3), since
\(|e^{-i\omega\tau_j}|=1\).  On a sufficiently large right-half-plane
semicircle the \(zI\) term dominates uniformly in \(s\).  The argument
principle therefore preserves the unstable root count along the homotopy.
At \(s=0\) the count is one.  Real coefficients pair every nonreal root
with its conjugate, so a single unstable root is real; multiplicity one
makes it simple. \(\square\)

For the present model, the inequality is automatic in the declared
small-\(\delta\) regime.

> **Corollary 4.2 (one unstable root for the clamped FHN RFDE).**  Fix the
> bistable layer \(\rho_0\) a positive distance from both folds.  Let
> \(D_w\) range in a compact subset of \((0,\infty)\), let \(K\) and
> \(\eta\) range in compact sets for which the layer matrices are bounded,
> and allow arbitrary positive delay lengths
> \(\tau_j=\theta_j/\delta\).  There is \(\delta_0>0\) such that the exact
> clamped saddle in Lemma 3.1 has precisely one unstable RFDE root for
> \(0<\delta\le\delta_0\).

**Proof.**  At \(\varepsilon=0\), the non-delay linearization is block
triangular with the two eigenvalues of the frozen voltage saddle and the
eigenvalue \(-D_w\).  It therefore has one unstable eigenvalue and is
uniformly separated from the imaginary axis on the declared compact set.
The exact equilibrium and its non-delay linearization vary continuously
with \(\varepsilon\), so the unstable count persists and the resolvent
constant \(R_0\) in (4.2) stays bounded.  The matrix bound \(L\) and
\(|K|\) also stay bounded.  Since \(\varepsilon=\delta^2\), (4.3) holds
after reducing \(\delta_0\).  Lemma 4.1 is independent of the delay
lengths. \(\square\)

The two singular channel branches also persist in exactly the form needed
below.

> **Lemma 4.3 (capture of the clamped unstable exits).**  Retain the
> compact hypotheses of Corollary 4.2 and the two singular passage blocks
> from the singular channel theorem.  On any compact control set contained
> in a common fixed-delay \(C^1\) coefficient chart, the exit histories
> below depend continuously on the controls.  Then, after reducing \(\delta_0\),
> the two branches of the local unstable manifold of the exact clamped
> saddle have exit histories with neighborhoods whose forward orbits reach
> the pulse and quiet blocks, respectively, in bounded fast time,
> transversely and before the other block, with common time and crossing
> margins on that compact set.

**Proof.**  At \(\varepsilon=0\), the local unstable manifold is the
voltage saddle's one-dimensional unstable manifold with \(\kappa=0\); its
two branches are the retained singular heteroclinic pieces.  On the
backward weighted space

\[
 \|y\|_\alpha=\sup_{t\le0}e^{-\alpha t}|y(t)|,
 \qquad 0<\alpha<\lambda_u,
\]

delay translation has norm \(e^{-\alpha\tau_j}\le1\).  The delayed
operator is multiplied by \(\varepsilon\), while the local nonlinear
remainder has its usual quadratic bound.  The backward Lyapunov--Perron
map for the one-dimensional strong unstable manifold is therefore a
uniform contraction on a sufficiently small fixed piece, and that piece is
\(C^1\)-close to the singular unstable curve as
\(\varepsilon\downarrow0\).  Starting at its two exit histories, the
remaining passages take bounded fast time.  On such an interval the
delayed term is uniformly \(O(\varepsilon)\) for bounded histories and
\(\kappa=O(\varepsilon)\).  Gronwall's inequality and the fixed crossing
margins of the singular blocks give neighborhoods with the claimed
capture and ordering.  Compactness of the control set makes the passage
time and crossing margins common. \(\square\)

This lemma certifies the unstable **index**, not a
\(\delta\)-uniform decay rate for all stable roots.  The invariant-manifold
theory near RFDE equilibria used below is standard; a precise general
reference is Chapter 10 of
[Hale--Verduyn Lunel](https://doi.org/10.1007/978-1-4612-4342-7).

## 5. The exact clamped separator

For the parameter statement, fix an open set \(U^\circ\subset\mathbb R^p\)
and a compact connected set \(U\Subset U^\circ\); the precise regularity
on their common fixed-delay history neighborhood is stated in Theorem 5.1.

For fixed positive \(\delta\) and \(u\in U\), let
\(E^u_{\delta,u}\oplus E^s_{\delta,u}\) be the spectral splitting at the
equilibrium history, with \(\dim E^u_{\delta,u}=1\).  Let
\(\Lambda^u_{\delta,u}\) be a continuously normalized scalar
coordinate on the unstable spectral projection.  The reset is transverse
when

\[
 \Lambda^u_{\delta,u}
 \partial_a\mathcal R_{\varepsilon,\delta}(0,u)\ne0.
\tag{5.1}
\]

At \(\varepsilon=0\), (5.1) is exactly the requirement that
\(\gamma_0'(0)\) not lie in the stable eigenspace of the frozen voltage
saddle.  Hence it persists for small positive \(\varepsilon\) whenever
the unstable spectral projection varies continuously.

Choose a sufficiently small local product neighborhood
\(\mathcal N_\delta\) of the equilibrium.  The two branches of the local
unstable manifold meet its boundary at histories
\(e^-_{\delta,u},e^+_{\delta,u}\), continuous in \(u\).  Lemma 4.3 and
bounded-time parameter dependence give open tubes
\(\mathcal V^-_\delta,\mathcal V^+_\delta\) around the two compact graphs
\(\{(e^\pm_{\delta,u},u):u\in U\}\) such that:

- every \((\phi,u)\in\mathcal V^-_\delta\) reaches the pulse passage block
  transversely;
- every \((\phi,u)\in\mathcal V^+_\delta\) reaches the quiet passage block
  transversely;
- both bounded-time families of passages occur before any competing block.

They are the RFDE perturbations of the two singular heteroclinic pieces in
the singular channel theorem.  For a fixed \(\delta\), their verification
uses the local unstable manifold followed by the already proved
fixed-fast-time passage estimates.  They contain no assertion about a slow
passage to the next fold because \(\rho\) is fixed by (3.3).

For clarity, here is the controlled transition set used below.  On a
declared reset interval \(I_0=(-a_0,a_0)\), let

\[
 \tau_j^{\rm clamp}(a,u)
 =\inf\{t>0:\Phi_{\delta,u}^t
   (\mathcal R_{\varepsilon,\delta}(a,u))
   \in\mathfrak B_{j,M'}^\varepsilon\},
 \qquad j\in\{\mathrm p,\mathrm q\},
\]

with \(\inf\varnothing=+\infty\).  Define

\[
\begin{aligned}
 \mathcal P^{\rm clamp}_{\delta,u}
 &:=\left\{a\in I_0:
       \tau_{\rm p}^{\rm clamp}(a,u)<\tau_{\rm q}^{\rm clamp}(a,u),
       \ \tau_{\rm p}^{\rm clamp}(a,u)<\infty,
       \ \text{and the pulse hit is transverse}\right\},\\
 \mathcal Q^{\rm clamp}_{\delta,u}
 &:=\left\{a\in I_0:
       \tau_{\rm q}^{\rm clamp}(a,u)<\tau_{\rm p}^{\rm clamp}(a,u),
       \ \tau_{\rm q}^{\rm clamp}(a,u)<\infty,
       \ \text{and the quiet hit is transverse}\right\}.
\end{aligned}
\]

The unresolved controlled transition set is

\[
 \boxed{\mathcal S^{\rm clamp}_{\delta,u}
 =I_0\setminus
  \bigl(\mathcal P^{\rm clamp}_{\delta,u}
        \cup\mathcal Q^{\rm clamp}_{\delta,u}\bigr).}
\]

All hits in this definition occur while the collective actuator remains
active.  This is not the unforced transition set of the earlier protocol.

> **Theorem 5.1 (small positive \(\delta\), controlled channel-safety
> separator).**  Retain the model hypotheses of Corollary 4.2.  Let
> \(U^\circ\subset\mathbb R^p\) be open and let
> \(U\Subset U^\circ\) be compact and connected.  The controls \(u\in U\)
> may include \(K,\eta,D_w\), but the delay locations are fixed.  For each
> fixed \(\delta>0\), assume the controlled RFDE functional is defined on
> one open history neighborhood of the equilibrium family over
> \(U^\circ\), is \(C^2\) in history and \(C^1\) in \(u\), and that the
> reset family is \(C^1\) on \(I_0\times U^\circ\).  Center it on the exact
> clamped saddle,
> \(\gamma_\varepsilon(0,u)=v^m_\varepsilon(u)\), and require
> \[
>  \|\gamma_\varepsilon-\gamma_0\|_{C^1(I_0\times U)}\longrightarrow0.
> \tag{5.2}
> \]
> If \(p_0^{\rm u}(u)\) is a continuously normalized left unstable eigenvector
> of the singular voltage saddle, assume the explicit uniform
> transversality
> \[
>  \inf_{u\in U}
>  |(p_0^{\rm u}(u))^T\partial_a\gamma_0(0,u)|\ge2c_a>0.
> \tag{5.3}
> \]
> Then there is \(\delta_0>0\) such that, for every fixed
> \(0<\delta\le\delta_0\), there are an interval
> \(J_\delta=(-a_\delta,a_\delta)\) and a \(C^1\) complete-history scalar
> \(g_\delta:J_\delta\times U\to\mathbb R\) such that, after one
> orientation and for every \(u\in U\),
> \[
> \begin{aligned}
>  g_\delta(a,u)&<0
>    &&\Longleftrightarrow &&\text{the pulse block is reached first},\\
>  g_\delta(a,u)&>0
>    &&\Longleftrightarrow &&\text{the quiet block is reached first},\\
>  g_\delta(a,u)&=0
>    &&\Longleftrightarrow &&a=0.
> \end{aligned}
> \tag{5.4}
> \]
> Moreover \(\partial_ag_\delta(0,u)\ne0\), the unique zero-parameter reset
> history is the exact constant saddle history in (3.9), and
> \[
>  \mathcal S^{\rm clamp}_{\delta,u}\cap J_\delta=\{0\}.
> \tag{5.5}
> \]
> Thus the event-triggered collective-recovery clamp has a unique local
> \(C^1\) complete-history channel separator.

**Proof.**  Corollary 4.2 gives RFDE hyperbolicity with exactly one
unstable root.  The strong unstable characteristic root and its current
left and right eigenvectors converge to those of the singular voltage
saddle by (4.1): the current perturbation is \(O(\varepsilon)\) and
\(e^{-\lambda_u\tau_j}\to0\).  In the RFDE spectral-projection formula,
the additional action on a bounded history is at most
\(C\varepsilon\int_0^{\tau_*}e^{-\lambda_us}\,ds=O(\varepsilon)\).
Consequently the projection on a constant reset tangent converges as well,
and (5.2)--(5.3) give, after reducing \(\delta_0\),

\[
 \inf_{u\in U}
 \left|\Lambda^u_{\delta,u}
 \partial_a\mathcal R_{\varepsilon,\delta}(0,u)\right|
 \ge c_a.
\tag{5.3a}
\]

Thus (5.1) holds uniformly on \(U\).  Lemma 4.3 supplies the
channel-capture tubes.

The RFDE stable-manifold theorem now gives a codimension-one
\(C^1\) local stable manifold \(W^s_{\delta,u,{\rm loc}}\), tangent to
\(E^s_{\delta,u}\), together with a local scalar defining function
\(G_{\delta,u}\), depending \(C^1\) on the fixed-delay control family.  Its
zero set consists precisely of histories whose forward
orbits remain in the local saddle neighborhood and converge to the
equilibrium.  Histories on the two sides leave through the two local
unstable faces; this follows from the one-dimensional unstable coordinate
in the graph-transform chart.

The reset curve (3.9) passes through the equilibrium.  Equation (5.1),
compactness of \(U\), and the parameter-dependent implicit-function theorem
show that it intersects \(W^s_{\delta,u,{\rm loc}}\) only at \(a=0\), after shrinking
one common \(J_\delta\).  Put

\[
 g_\delta(a,u)=G_{\delta,u}
   (\mathcal R_{\varepsilon,\delta}(a,u)).
\]

Then \(\partial_ag_\delta(0,u)\ne0\), and its sign labels the two local
exits.  Here is the quantitative inclination step.  Let
\(t^\pm_\delta(a,u)\) be the first exit time from
\(\mathcal N_\delta\) on the side \(\pm g_\delta>0\).  For this fixed
\(\delta\), compactness of \(U\) and the local stable foliation give
constants \(C_\delta,r_\delta,\sigma_\delta>0\) such that

\[
\begin{aligned}
 t^\pm_\delta(a,u)
 &\le C_\delta
   \bigl(1+|\log|g_\delta(a,u)||\bigr),\\
 \left\|\Phi_{\delta,u}^{t^\pm_\delta(a,u)}
   (\mathcal R_{\varepsilon,\delta}(a,u))
   -e^\pm_{\delta,u}\right\|_{\mathcal X_\delta}
 &\le C_\delta|g_\delta(a,u)|^{\sigma_\delta},
 \qquad 0<\pm g_\delta(a,u)<r_\delta.
\end{aligned}
\tag{5.6}
\]

Indeed, choose a stable-fiber tracking rate \(\beta_{s,\delta}>0\), a
positive lower unstable rate, and an upper unstable rate
\(\lambda^+_{u,\delta}\), all uniform on \(U\) for this fixed
\(\delta\).  The unstable coordinate gives the logarithmic exit-time
bound and also the lower bound
\(t^\pm_\delta\ge
(\lambda^+_{u,\delta})^{-1}
\log(c_{{\rm ex},\delta}/|g_\delta|)-C_\delta\), for one local exit
constant \(c_{{\rm ex},\delta}>0\).  Exponential tracking of the stable
fiber to the local unstable manifold then yields the second line of (5.6)
with any
\(0<\sigma_\delta<
\beta_{s,\delta}/\lambda^+_{u,\delta}\).
The RFDE inclination construction used here is the fixed-delay result of
[Walther, *Inclination lemmas with dominated convergence*](https://doi.org/10.1007/BF00945417),
specialized to the local saddle chart; its RFDE semiflow implementation is
developed in Part II, Sections 6--10 of
[Walther, *Bifurcation from a saddle connection in functional differential
equations*](https://doi.org/10.22029/jlupub-16434).

The compact exit graphs have a positive tube margin inside
\(\mathcal V^-_\delta\) and \(\mathcal V^+_\delta\).  Equation (5.6)
therefore places the first-exit histories of both reset half-curves in the
corresponding capture tube after shrinking \(J_\delta\).  Those tubes carry
the histories to the pulse and quiet blocks without another first hit.  The
zero orbit stays at the saddle while the collective clamp is active and
reaches neither block.  This proves (5.4)--(5.5). \(\square\)

The theorem is a result about an actual RFDE stable manifold in the full
history space.  Replacing \(g_\delta\) by a sign of the current voltage
would lose the delayed endpoint terms and is not justified.

The precise uniform extension is as follows.

> **Theorem 5.2 (uniform clamped family under strong-unstable
> domination).**  Let \(0<\delta\le\delta_0\) and retain
> \(U\Subset U^\circ\) from Theorem 5.1.  Identify the varying physical
> history spaces by the fixed scaled interval
> \(\vartheta=\delta s\in[-\theta_*,0]\); no derivative with respect to
> \(\delta\) is asserted.  Suppose the RFDE coefficients and reset family
> have the stated \(C^2_\phi C^1_u\) bounds on one common scaled-history
> neighborhood.  In addition to the hypotheses of Theorem 5.1, assume
> there are constants \(M,c_a,c_b>0\) and
> \(0\le\alpha<\beta\), independent of \(\delta\), such that:
>
> 1. the linear solution operators have an invariant splitting with
>    \[
>      \|T^{cs}_\delta(t)\|\le Me^{\alpha t},\quad t\ge0,
>      \qquad
>      \|T^u_\delta(-t)\|\le Me^{-\beta t},\quad t\ge0;
>    \tag{5.7}
>    \]
> 2. the nonlinear RFDE remainders have uniform \(C^2\) bounds on one
>    common history neighborhood small enough for the dominated graph
>    transform;
> 3. the reset transversality has magnitude at least \(c_a\), and the two
>    exit-to-channel passages have distance and crossing margins at least
>    \(c_b\).
>
> Then \(J_\delta\) in Theorem 5.1 can be replaced by one common interval
> \(J\).  The defining functions may be normalized so that
> \[
>  |\partial_a g_\delta|\ge c_g>0
> \tag{5.8}
> \]
> on a common zero tube, and the separator and its parameter dependence are
> \(C^1\) with uniform bounds.

**Proof.**  The uniform gap \(\beta-\alpha\), the common nonlinear radius,
and the bounds in (5.7) give a uniform contraction for the
center-stable graph transform.  This produces a common local product box
and uniformly \(C^1\) defining functions.  Uniform reset transversality and
the parameter-dependent implicit-function theorem give (5.8) on a common
interval.  The fixed channel margins then propagate both exit faces to the
same two passage blocks. \(\square\)

Condition (5.7) is deliberately a **strong-unstable versus center-stable**
estimate.  It permits center-stable roots to approach the imaginary axis as
in (2.4).  Lemma 4.1 alone proves only the unstable root count and therefore
does not, by itself, prove all uniform constants in Theorem 5.2.

## 6. Why a fixed clamp deadline is not exact

The event-triggered rule in Section 3 keeps the clamp until one channel is
reached.  Every nonseparator history in Theorem 5.1 decides in finite time,
but the decision times are unbounded as \(a\to0\).

> **Lemma 6.1 (no finite deadline at a simple saddle threshold).**  Let
> the pulse and quiet blocks have positive distance from the saddle
> equilibrium.  For every finite \(T_R\), there is a neighborhood of
> \(a=0\) whose clamped trajectories reach neither block by \(T_R\).
> Consequently no fixed finite recovery-clamp duration produces a channel
> decision *before its deadline* for every nonzero reset parameter
> arbitrarily close to the exact separator.

**Proof.**  The separator history is the equilibrium and does not reach
either block.  Continuous dependence on the initial history, uniformly on
the compact interval \([0,T_R]\), keeps all sufficiently nearby reset
trajectories in a neighborhood disjoint from both blocks. \(\square\)

A fixed deadline is useful once an experimental resolution is declared.
If a local unstable coordinate satisfies

\[
 |u(0)|\ge c_a|a|,
 \qquad
 \frac{d}{dt}|u|\ge\lambda_-|u|
\tag{6.1}
\]

until the exit face \(|u|=u_{\rm ex}\), then every
\(|a|\ge a_{\min}>0\) exits by

\[
 T_{\rm dec}
 \le\frac1{\lambda_-}
 \log\frac{u_{\rm ex}}{c_aa_{\min}}.
\tag{6.2}
\]

Thus there are two honest protocol choices:

- **exact threshold:** clamp \(\rho\) until a channel is reached; the
  separator trajectory remains clamped indefinitely;
- **finite experiment:** choose \(T_R\) and report an unresolved deadband
  of logarithmically corresponding width.

Calling the second protocol exact without the deadband would be false.

## 7. Relation to Gate R-S and to a canard root

The controlled separator is not a proof of Gate R-S for the unforced RFDE.
The two experiments differ after release:

\[
 \dot\rho=\varepsilon(\xi-\mu)
 \quad\hbox{versus}\quad
 \dot\rho=0.
\tag{7.1}
\]

In the repaired protocol, the controlled channel-safety threshold is
\(a=0\) exactly because the reset family is centered on the exact clamped
saddle equilibrium.  It is a new operational safety coordinate, not the
unforced canard threshold.  In the unforced protocol, the exponentially
thin slow-passage layer can shift the transition, and its analysis requires
the missing exchange theorem.

No comparison with the preparation-indexed or physical maximal-canard root
is proved here.  Such a comparison would require a declared map from the
physical unfolding to the reset coordinate and a quantitative
reset-to-canard factorization with all complete-history endpoint terms.  A
memory flush, a stable manifold at a controlled equilibrium, and equality
of constant histories do not provide that factorization.

## 8. Theorem and status ledger

| Statement | Status | Exact scope |
|---|---|---|
| Frozen saddle history is invariant after the original unforced release | False generically | Exact drift (1.2) |
| A local frozen-saddle stable manifold closes unforced Gate R-S | False as an implication | It misses the exponentially thin drift-to-fold exchange |
| Unforced transition set is nonunique | Not asserted | No counterexample for the physical model is proved |
| Unforced Gate R-S | Open | Needs a saddle-slow-history exchange and two-channel capture theorem |
| Weak long delay has a uniform stable spectral gap | False in general | Exact conjugate scalar roots and asymptotic ratio (2.2)--(2.4) |
| Scalar collective clamp removes the drift | Proved exactly | Identities (3.1)--(3.3); the physical actuator has zero \(\kappa\)-projection |
| Exact clamped saddle history | Proved | Lemma 3.1 and diffusive cancellation |
| One unstable RFDE root | Proved under a checkable inequality | Lemma 4.1, fixed or parameter-uniform index only |
| Unique complete-history clamped separator | Proved for the compact clamped FHN class and a singular-transverse centered reset | Theorem 5.1 for every sufficiently small fixed \(\delta>0\); the interval may shrink with \(\delta\) |
| \(\delta\)-uniform separator tube and derivative | Conditional on explicit domination bounds | Theorem 5.2 |
| Fixed finite clamp reaches a decision before its deadline for all nonzero offsets | False | Lemma 6.1 |
| Finite clamp outside a declared deadband | Conditional quantitative bound | Equation (6.2) |
| Equality with a physical or canonical canard root | Not asserted | Requires a new reset-to-canard factorization |

The strongest current conclusion is therefore precise: a local
stable-manifold argument does not close the **unforced** Gate R-S, but one
additional causal scalar control closes an exact operational separator
problem.  Removing that scalar control while retaining exact channel
classification is the remaining canard exchange theorem, not a routine
perturbation of the clamped result.
