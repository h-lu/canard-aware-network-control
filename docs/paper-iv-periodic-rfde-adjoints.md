# Periodic RFDE adjoints and the physical safety row

Status: **the abstract derivative and adjoint formulas in Sections 2--5 are
proved. Their algebraic specialization to the declared synchronous
FitzHugh--Nagumo RFDE is exact. Existence and nondegeneracy of the required
periodic branch, the physical separator, and a model-level response-rank
bound remain open.** This advances Paper IV from an abstract row-cancellation
theorem to a precise response calculation, but does not claim
three-coordinate controllability.

The executable sign and transpose checks are in
src/canard_control/periodic_rfde_sensitivity.py, with tests in
tests/test_periodic_rfde_sensitivity.py. The frozen JNS manuscript is not
used as evidence for any periodic-orbit or physical-separator hypothesis
below.

## 1. The normalized periodic problem

Consider the autonomous discrete-delay equation

\[
 \dot x(t)=f\bigl(x(t),x(t-\tau _1(p)),\ldots,
                    x(t-\tau _q(p));p\bigr),
 \qquad x(t)\in\mathbb R^d,\quad p\in P\subset\mathbb R^m,
 \tag{1.1}
\]

where \(f\) and the positive delays are \(C^2\). Suppose, for the moment,
that a \(C^1\) branch of nonconstant periodic solutions exists, with period
\(T(p)>0\). Put

\[
 X(\theta;p)=x(T(p)\theta;p),\qquad
 \alpha_j(p)=\frac{\tau_j(p)}{T(p)},\qquad
 (\mathcal S_{\alpha}X)(\theta)=X(\theta-\alpha),
 \tag{1.2}
\]

where every function of \(\theta\) is one-periodic. No reduction of
\(\alpha_j\) modulo one is needed: periodicity makes the shift well-defined,
and retaining its real value makes its derivative unambiguous. The
normalized orbit solves

\[
 \Phi(X,T,p):=
 X'-T f\bigl(X,\mathcal S_{\alpha_1}X,\ldots,
                \mathcal S_{\alpha_q}X;p\bigr)=0.
 \tag{1.3}
\]

Varying \(T\) changes every normalized delay \(\alpha_j=\tau_j/T\), even
when the physical delay is fixed. Thus the derivative of (1.3) with respect
to the period is not just \(-f\).

Fix a base orbit \((X,T,p)\). Along it, write

\[
 A_0(\theta)=D_0f(\theta),\qquad
 A_j(\theta)=D_jf(\theta),\quad 1\le j\le q,
 \tag{1.4}
\]

where \(D_jf\) differentiates the \(j\)-th delayed state. For a parameter
direction \(\zeta\in\mathbb R^m\), define

\[
\begin{aligned}
 \mathcal Ly
 &:=y'-TA_0y-T\sum_{j=1}^qA_j\mathcal S_{\alpha_j}y,\\
 b
 &:=f+\sum_{j=1}^q
       \alpha_jA_j\mathcal S_{\alpha_j}X',\\
 g_\zeta
 &:=T D_pf[\zeta]
   -\sum_{j=1}^qD_p\tau_j[\zeta]\,
       A_j\mathcal S_{\alpha_j}X'.
 \tag{1.5}
\end{aligned}
\]

Here \(D_pf\) is taken at fixed current and delayed arguments. The first
variation \(y=D_pX[\zeta]\) and \(T_\zeta=D_pT[\zeta]\) satisfy

\[
 \boxed{\mathcal Ly-bT_\zeta=g_\zeta.}
 \tag{1.6}
\]

Indeed,

\[
 D_p\alpha_j[\zeta]
 =\frac{D_p\tau_j[\zeta]}T
  -\frac{\alpha_j}{T}T_\zeta,
 \tag{1.7}
\]

and differentiating
\(\mathcal S_{\alpha_j}X=X(\theta-\alpha_j)\) gives
\(\mathcal S_{\alpha_j}y-
\mathcal S_{\alpha_j}X'\,\alpha_{j,\zeta}\).
Collecting the terms proportional to \(T_\zeta\) proves
(1.5)--(1.7). This calculation is exact for arbitrarily large physical
delays and does not use a small-delay expansion.

## 2. The advanced periodic adjoint

Use the pairing

\[
 \langle z,y\rangle
 =\int_0^1z(\theta)^Ty(\theta)\,d\theta.
 \tag{2.1}
\]

On \(H^1_{\rm per}\to L^2_{\rm per}\), the distributional adjoint of
\(\mathcal L\) is

\[
 \boxed{
 \mathcal L^\dagger z
 =-z'-TA_0^Tz
  -T\sum_{j=1}^q
     A_j(\theta+\alpha_j)^Tz(\theta+\alpha_j).}
 \tag{2.2}
\]

Thus the coefficient in an advanced term must also be evaluated at the
advanced point. Replacing it by
\(A_j(\theta)^Tz(\theta+\alpha_j)\) is wrong for a nonconstant orbit.
To prove (2.2), change variables \(\vartheta=\theta-\alpha_j\):

\[
 \int_0^1z(\theta)^TA_j(\theta)y(\theta-\alpha_j)\,d\theta
 =\int_0^1
  \{A_j(\vartheta+\alpha_j)^Tz(\vartheta+\alpha_j)\}^T
  y(\vartheta)\,d\vartheta.
 \tag{2.3}
\]

Periodicity removes the endpoint terms. The derivative
\(H^1_{\rm per}\to L^2_{\rm per}\) is Fredholm of index zero. Every
lower-order term in (1.5) is compact relative to it because
\(H^1(\mathbb T)\) embeds compactly into \(L^2(\mathbb T)\), and periodic
shifts preserve \(H^1\). Hence \(\mathcal L\) is Fredholm of index zero.

Fix the integral phase condition

\[
 \ell(y):=\int_0^1X'(\theta)^Ty(\theta)\,d\theta=0.
 \tag{2.4}
\]

It has \(\ell(X')>0\). The precise nondegeneracy needed below is

\[
 \ker\mathcal L=\operatorname{span}\{X'\},\qquad
 \ker\mathcal L^\dagger=\operatorname{span}\{z\},\qquad
 \langle z,b\rangle\ne0.
 \tag{2.5}
\]

Equivalently, the bordered operator

\[
 \mathcal A(y,\sigma)
 =\bigl(\mathcal Ly-b\sigma,\ell(y)\bigr)
 :H^1_{\rm per}\times\mathbb R
  \longrightarrow L^2_{\rm per}\times\mathbb R
 \tag{2.6}
\]

is an isomorphism. The equivalence follows from the two nonzero pairings in
(2.4)--(2.5) and the index-zero property. Condition (2.5), not a numerically
observed closed curve alone, is what must be enclosed for the declared FHN
orbit.

> **Theorem 2.1 (period and frequency response).** Assume (2.5) and
> normalize the periodic BVP adjoint by
>
> \[
>  \mathcal L^\dagger z=0,\qquad \langle z,b\rangle=1.
>  \tag{2.7}
> \]
>
> Then, for every parameter direction \(\zeta\),
>
> \[
> \boxed{
>  T_\zeta=-\langle z,g_\zeta\rangle,
>  \qquad
>  F_\zeta=\frac{\langle z,g_\zeta\rangle}{T^2},
>  \qquad F=T^{-1}.}
> \tag{2.8}
> \]

**Proof.** Pair (1.6) with \(z\). Equations (2.2) and (2.7) give
\(-T_\zeta=\langle z,g_\zeta\rangle\). Differentiating \(F=T^{-1}\)
gives the second identity. \(\square\)

The function \(z\) is the \(L^2\) adjoint of the normalized periodic BVP.
It is not the static network left mode and cannot be replaced by that mode.
Nothing here requires identifying it with a phase-response functional in a
sun--star dual space; the BVP and its pairing have already been specified.

## 3. A unique peak and its amplitude adjoint

Let \(h:\mathbb R^d\times P\to\mathbb R\) be \(C^2\), and set

\[
 H(\theta,p)=h(X(\theta;p),p).
 \tag{3.1}
\]

Assume that, on a parameter neighborhood, \(H\) has exactly one maximum
\(\theta_+(p)\) and one minimum \(\theta_-(p)\) modulo one, with

\[
 H_{\theta\theta}(\theta_+)<0,\qquad
 H_{\theta\theta}(\theta_-)>0.
 \tag{3.2}
\]

After choosing local lifts of the two points from the circle to one
parameter-independent coordinate chart, the implicit-function theorem gives
\(C^1\) extremum branches and excludes peak switching on a sufficiently
small neighborhood. Put

\[
 H_\pm=h(X(\theta_\pm),p),\qquad
 \Delta_h=H_+-H_-,\qquad
 R_h=\Delta_h^2.
 \tag{3.3}
\]

> **Theorem 3.1 (peak-envelope derivative).** Under (2.5) and (3.2),
>
> \[
> \begin{aligned}
> D_pH_\pm[\zeta]
> &=h_x^\pm y_\zeta(\theta_\pm)+h_p^\pm[\zeta],\\
> D_pR_h[\zeta]
> &=2\Delta_h\bigl[
>   h_x^+y_\zeta(\theta_+)-h_x^-y_\zeta(\theta_-)
>   +h_p^+[\zeta]-h_p^-[\zeta]
>   \bigr],
> \tag{3.4}
> \end{aligned}
> \]
>
> where \((y_\zeta,T_\zeta)\) is the unique solution of (1.6), (2.4).

**Proof.** Differentiating \(H_\pm\) also produces
\(H_\theta(\theta_\pm)D_p\theta_\pm[\zeta]\), which vanishes at either
extremum. The second formula follows from (3.3). \(\square\)

Formula (3.4) is independent of phase gauge. Adding a multiple of \(X'\)
to \(y_\zeta\) changes each evaluation by
\(h_x^\pm X'(\theta_\pm)=H_\theta(\theta_\pm)=0\).

The entire amplitude row can instead be obtained from one additional
adjoint. Define

\[
 c_+=2\Delta_h(h_x^+)^T,\qquad
 c_-=-2\Delta_h(h_x^-)^T,
 \tag{3.5}
\]

and let \((q_R,\chi_R)\) be the transposed bordered solution

\[
\boxed{
\begin{aligned}
 \mathcal L^\dagger q_R+\chi_RX'
   &=c_+\delta_{\theta_+}+c_-\delta_{\theta_-},\\
 \langle q_R,b\rangle&=0,
 \qquad q_R\text{ has periodic distributional trace}.
 \tag{3.6}
\end{aligned}}
\]

Equation (3.6) is distributional. Its unique solution belongs to \(L^2\)
and is \(H^1\) away from the two extrema. If the periodic seam is chosen
away from the extrema, the trace condition is simply
\(q_R(0^+)=q_R(1^-)\); if an extremum lies at the seam, its two one-sided
traces instead obey the same jump rule on the circle. With
\([q_R]_{\theta_e}=q_R(\theta_e^+)-q_R(\theta_e^-)\), the jumps are

\[
 [q_R]_{\theta_+}=-c_+,\qquad
 [q_R]_{\theta_-}=-c_-.
 \tag{3.7}
\]

The advanced terms in (2.2) remain present between the jumps. Existence and
uniqueness follow from invertibility of the adjoint of (2.6), since point
evaluation is continuous on \(H^1(\mathbb T)\).

> **Corollary 3.2 (amplitude response from one adjoint).** Under the same
> hypotheses,
>
> \[
> \boxed{
> D_pR_h[\zeta]
> =2\Delta_h\{h_p^+[\zeta]-h_p^-[\zeta]\}
>  +\langle q_R,g_\zeta\rangle.}
> \tag{3.8}
> \]

**Proof.** Pair (3.6) with \(y_\zeta\). Its right-hand side is the
state-dependent part of (3.4). Using (1.6), (2.4), and
\(\langle q_R,b\rangle=0\) converts it to
\(\langle q_R,g_\zeta\rangle\). \(\square\)

Unique extrema and their curvature are hypotheses. A collocation plot that
appears to have one maximum and one minimum does not prove (3.2) on a
parameter box.

## 4. A causal pulse experiment and its event adjoint

The periodic adjoints do not define the pulse-safety row. That row belongs
to the physical complete-history separator in Paper III. The following
finite-horizon formula gives an exact interface for its causal reset route.

Let a declared history
\(\phi_p:[-\tau_*,0]\to\mathbb R^d\) be held or reset and then released
into (1.1). Let \(x_p\) be the resulting solution. At a base parameter its
fixed-time sensitivity satisfies

\[
\begin{aligned}
 \dot y_\zeta(t)
 ={}&A_0(t)y_\zeta(t)
 +\sum_{j=1}^qA_j(t)
   \{y_\zeta(t-\tau_j)
      -\dot x(t-\tau_j)D_p\tau_j[\zeta]\}
 +D_pf(t)[\zeta],\\
 y_\zeta(s)={}&D_p\phi_p(s)[\zeta],
 \qquad -\tau_*\le s\le0.
 \tag{4.1}
\end{aligned}
\]

For a nonconstant reset history, the moving-delay term uses its time
derivative when \(t-\tau_j<0\).

Suppose a terminal time \(L(p)\) is determined by a transverse section

\[
 q(x_p(L(p)),p)=0,\qquad q_x\dot x(L)\ne0,
 \tag{4.2}
\]

and define a landing gap
\(\Gamma(p)=g(x_p(L(p)),p)\). Put

\[
 \beta=\frac{g_x\dot x(L)}{q_x\dot x(L)},\qquad
 \lambda_L=(g_x-\beta q_x)^T.
 \tag{4.3}
\]

The finite-horizon adjoint is the advanced terminal problem

\[
\boxed{
\begin{aligned}
 -\dot\lambda(t)
 ={}&A_0(t)^T\lambda(t)
 +\sum_{j:\,t+\tau_j\le L}
   A_j(t+\tau_j)^T\lambda(t+\tau_j),\\
 \lambda(L)={}&\lambda_L.
 \tag{4.4}
\end{aligned}}
\]

> **Theorem 4.1 (reset-to-landing derivative).** If the solution family is
> \(C^1\), (4.2) is transverse, and (4.1)--(4.4) are well-defined, then
>
> \[
> \begin{aligned}
> D_p\Gamma[\zeta]
> ={}&g_p[\zeta]-\beta q_p[\zeta]
> +\lambda(0)^TD_p\phi_p(0)[\zeta]\\
> &+\int_0^L\lambda(t)^T
> \left(D_pf(t)[\zeta]
> -\sum_{j=1}^qA_j(t)\dot x(t-\tau_j)
>                 D_p\tau_j[\zeta]\right)dt\\
> &+\sum_{j=1}^q
> \int_{-\tau_j}^{\min(0,L-\tau_j)}
> \lambda(s+\tau_j)^TA_j(s+\tau_j)
> D_p\phi_p(s)[\zeta]\,ds.
> \tag{4.5}
> \end{aligned}
> \]

**Proof.** Differentiating (4.2) gives

\[
 L_\zeta=-\frac{q_xy_\zeta(L)+q_p[\zeta]}
                    {q_x\dot x(L)}.
 \tag{4.6}
\]

Substitution in the derivative of \(g(x_p(L(p)),p)\) gives the direct terms
and terminal covector (4.3). Integrating
\(\frac d{dt}(\lambda^Ty_\zeta)\) on \([0,L]\), the positive-time delayed
terms cancel after \(s=t-\tau_j\). Their negative-time parts give the final
line of (4.5), and the remaining moving-delay and explicit forcing terms
give its middle line. \(\square\)

For a constant, parameter-independent reset history, every
history-derivative term in (4.5) vanishes. The moving-delay integral need
not vanish unless the sampled history and subsequent orbit are constant.
If the entry history is instead the compatible physical outer history, its
derivative terms are precisely where Gate P3-A\(^*\) is needed.

## 5. From a canard or event gap to the safety row

Let \(a\) be the scalar unfolding and \(u\in\mathbb R^m\) the actuator
vector. Suppose a physical signed channel gap is regular:

\[
 \Gamma(a_c(u),u)=0,\qquad
 |\partial_a\Gamma(a_c(u),u)|\ge m_\Gamma>0.
 \tag{5.1}
\]

For a possibly controlled operating value \(a_{\rm op}(u)\), define

\[
 S_c(u)=a_{\rm op}(u)-a_c(u).
 \tag{5.2}
\]

The implicit-function theorem gives the exact safety row

\[
 \boxed{
 D_uS_c
 =D_ua_{\rm op}
  +\frac{D_u\Gamma}{\partial_a\Gamma}.}
 \tag{5.3}
\]

For the reset protocol, \(D\Gamma\) may be evaluated by (4.5). For a
complete-history Lin gap, it must include the trace, endpoint, and history
terms of Paper II.

There is also an exact canard/event compatibility statement. Suppose a
channel-separation theorem proves that, in one neighborhood, the physical
canard gap \(\Gamma\) and an operational channel defining function
\(\mathcal E\) have the same zero set, and both gradients are nonzero.
Their kernels equal the common tangent space of that hypersurface. Hence

\[
 D\mathcal E=\gamma D\Gamma,\qquad \gamma\ne0,
 \tag{5.4}
\]

at every boundary point, and

\[
 -\frac{D_u\mathcal E}{\partial_a\mathcal E}
 =-\frac{D_u\Gamma}{\partial_a\Gamma}.
 \tag{5.5}
\]

Thus channel-event and canard definitions give the same safety row after
Paper III proves exact basin separation. Equation (5.5) cannot be invoked
before that zero-set equality is proved. A fixed-observable amplitude
detector generally has a different root; Theorem 5.2 of the Paper III note
only gives an exponentially close \(C^1\) row after its landing-chart
hypotheses have been verified.

## 6. Exact specialization to the declared FHN network

On a completely synchronous history, the dual-scaffold network in
two-module-reference.md reduces exactly to

\[
\begin{aligned}
 \dot V={}&V-\frac{V^3}{3}-W
 +\varepsilon\kappa_1
  \left(\frac{V_0+V_1}{2}-V\right)\\
 &+\varepsilon\kappa_3
  \left(\frac{(V_0-1)^3+(V_1-1)^3}{2}-(V-1)^3\right),\\
 \dot W={}&\varepsilon(V-a),
 \qquad V_j=V(t-\tau_j),\\
 \tau_j={}&\frac{\Theta_j^0+s}{\sqrt\varepsilon},
 \qquad j=0,1.
 \tag{6.1}
\end{aligned}
\]

Let \(x=(V,W)^T\). To avoid confusing the current derivative with the delay
indexed by \(j=0\), denote the current matrix by \(C_0\) and the delayed
matrices by \(B_j\):

\[
 C_0=
 \begin{pmatrix}
  1-V^2-\varepsilon\kappa_1
   -3\varepsilon\kappa_3(V-1)^2&-1\\
  \varepsilon&0
 \end{pmatrix},
 \tag{6.2}
\]

\[
 B_j=
 \begin{pmatrix}
  \dfrac{\varepsilon}{2}
  \{\kappa_1+3\kappa_3(V_j-1)^2\}&0\\
  0&0
 \end{pmatrix},\qquad j=0,1.
 \tag{6.3}
\]

At fixed state arguments,

\[
 f_{\kappa_1}
 =\varepsilon
 \begin{pmatrix}(V_0+V_1)/2-V\\0\end{pmatrix},
 \tag{6.4}
\]

\[
 f_{\kappa_3}
 =\varepsilon
 \begin{pmatrix}
 ((V_0-1)^3+(V_1-1)^3)/2-(V-1)^3\\0
 \end{pmatrix}.
 \tag{6.5}
\]

There is no explicit \(s\)-derivative of \(f\), but
\(\partial_s\tau_0=\partial_s\tau_1=\varepsilon^{-1/2}\). Thus

\[
\begin{aligned}
 g_{\kappa_1}&=Tf_{\kappa_1},\\
 g_{\kappa_3}&=Tf_{\kappa_3},\\
 g_s&=-\varepsilon^{-1/2}
 \{B_0\mathcal S_{\alpha_0}X'
   +B_1\mathcal S_{\alpha_1}X'\}.
 \tag{6.6}
\end{aligned}
\]

The fast component of \(g_s\) is

\[
 -\frac{\sqrt\varepsilon}{2}
 \sum_{j=0}^1
 \{\kappa_1+3\kappa_3(V_j-1)^2\}V_j',
\tag{6.7}
\]

Here

\[
 V_j'=X_V'(\theta-\alpha_j)
 \tag{6.7a}
\]

is the derivative with respect to normalized phase \(\theta\), not the
physical-time derivative of \(V(t-\tau_j)\).  The recovery component of
\(g_s\) is zero. Equations (6.2)--(6.7) have been checked
by symbolic differentiation. The negative sign and the
\(\sqrt\varepsilon\) scale in (6.7) come from moving the delayed argument;
they are not choices of adjoint normalization.

On synchrony, the declared observable
\(h_N=2\bar v_1/3+\bar v_2/3\) equals \(V\). Thus \(h_x=(1,0)\), the
explicit observable derivatives vanish, and (3.5) becomes

\[
 c_+=2\Delta_V(1,0)^T,\qquad
 c_-=-2\Delta_V(1,0)^T.
 \tag{6.8}
\]

The scalar reduction is exact for the synchronous periodic branch. It does
not prove that this branch is transversely stable in the full \(2N\)-state
RFDE. Full-network hyperbolicity is additionally required if the orbit is
to represent an attracting biological rhythm rather than merely an
invariant synchronous solution.

## 7. The concrete three-actuator response target

Order the actuators as

\[
 u=(\kappa_1,\kappa_3,s).
 \tag{7.1}
\]

Assume temporarily that (2.5), (3.2), and (5.1) hold. Normalize \(z\) by
(2.7), solve (3.6), and write \(g_j=g_{u_j}\). For fixed
\(a_{\rm op}\), the exact response matrix target is

\[
\boxed{
 M_\varepsilon=
 \begin{pmatrix}
  T^{-2}\langle z,g_{\kappa_1}\rangle&
  T^{-2}\langle z,g_{\kappa_3}\rangle&
  T^{-2}\langle z,g_s\rangle\\[2mm]
  \langle q_R,g_{\kappa_1}\rangle&
  \langle q_R,g_{\kappa_3}\rangle&
  \langle q_R,g_s\rangle\\[2mm]
  \Gamma_{\kappa_1}/\Gamma_a&
  \Gamma_{\kappa_3}/\Gamma_a&
  \Gamma_s/\Gamma_a
 \end{pmatrix}.}
 \tag{7.2}
\]

Its rows are \(D_uF,D_uR_h,D_uS_c\). The first two rows use one periodic
orbit and two adjoints, independent of the number of actuators. The last
row is not a periodic-orbit adjoint: it is the derivative of the physical
channel separator.

The local canard calculation predicts, but the physical transfer has not
yet proved, the leading safety entries

\[
 D_uS_c
 =\left(
   \frac{M_1^{(2)}}8\varepsilon^{3/2},
   0,
   \frac{\kappa_1}8\varepsilon^{3/2}
  \right)
  +O(\varepsilon^2),
 \qquad
 M_1^{(2)}=\frac{\Theta_0^0+\Theta_1^0}{2}+s.
 \tag{7.3}
\]

The zero in the cubic column means only that centering the cubic actuator
at the fold removes its \(O(\varepsilon^{3/2})\) local threshold
contribution. It does not say that the exact physical safety derivative
vanishes.

The quantitative target is not a determinant at one computed point. In
frozen input and output units it is a box \(U_*\) and enclosures

\[
 \inf_{u\in U_*}\sigma_{\rm sur}(M_\varepsilon(u))\ge\sigma_*>0,
 \qquad
 \operatorname{Lip}_{U_*}M_\varepsilon\le L_M,
 \tag{7.4}
\]

or, inside the sharp canard layer, verification of the hypotheses of
paper-iv-canard-conditioning-no-go.md.

### Minimal missing model certification

Promoting (7.2) to a positive or negative Paper IV theorem requires all of
the following:

1. a nonempty parameter box carrying a periodic branch and an enclosure of
   the bordered inverse (2.6), including the advanced adjoint (2.2);
2. unique nondegenerate maximum and minimum branches for \(V\), with a
   uniform curvature bound and exclusion of peak switching;
3. either Gate P3-A\(^*\) or the causal one-maximal-delay reset theorem,
   followed by the exit and two-channel separation theorem, so that
   \(\Gamma\) in (5.1) is a physical signed separator;
4. an enclosure of \(|\Gamma_a|^{-1}\) and of \(D_u\Gamma\), including
   reset-history or outer-history and endpoint terms;
5. if biological attraction is claimed, a full-network transverse Floquet
   enclosure rather than hyperbolicity only in the synchronous restriction;
6. discretization, delayed interpolation, orbit, adjoint, extrema, and
   separator error bounds small enough to prove either (7.4) or the stated
   conditioning inequality on the whole box.

No present test supplies these six items. Thus (7.2) is a derived response
target, not a rank certificate. Neither hyperbolicity nor a nonzero
model-level determinant is claimed here.

## 8. Executable regression evidence

The code checks three independent parts of the derivation.

1. SymPy differentiation of (6.1) reproduces (6.2)--(6.7).
2. Random nonconstant periodic coefficient arrays verify exactly that the
   retarded grid operator and the advanced formula with
   \(A_j(\theta+\alpha_j)^T\) are transposes. A deliberately unshifted
   coefficient fails this identity.
3. The delayed Stuart--Landau equation

   \[
    \dot z=(1-|z|^2)z+i\omega z+K\{z(t-\tau)-z(t)\}
    \tag{8.1}
   \]

   has a rotating wave \(z(t)=r e^{i\Omega t}\) satisfying

   \[
    \Omega-\omega+K\sin(\Omega\tau)=0,\qquad
    r^2=1+K\{\cos(\Omega\tau)-1\}.
    \tag{8.2}
   \]

   Its exact implicit period and squared-amplitude derivatives agree with
   (2.8), the forward bordered equation, and the transposed amplitude
   solve. The delay derivative is nonzero and checks the moving-delay sign.

4. A one-step linear DDE with a transverse clock event, a
   parameter-dependent reset history, and a moving delay has a closed-form
   landing map. Its two derivatives agree with (4.5), including the
   negative-time history integral and the nonconstant advanced adjoint.

These are algebraic and numerical regression tests for the formulas. The
manufactured equations are not evidence for the FHN hypotheses in Section 7.
