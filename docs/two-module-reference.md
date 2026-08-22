# Two-module FHN reference and transverse feasibility audit

Status: **concrete control benchmark frozen; weak-only uniform one-gap
assumption rejected.** Exact reductions and the inner formal calculations are
checked algebraically. The model-specific RFDE Fredholm estimate remains open.

## 1. Proof-oriented FHN benchmark

Let \(C_1,C_2\) have sizes \(n_1,n_2\). Define the rank-one row-stochastic
averaging matrix

\[
 P_{ij}=\frac{1}{2n_b},
 \qquad i\in C_a,\quad j\in C_b.
 \tag{1}
\]

There are two scaled delays,

\[
 \Theta_{ab}(s)=
 \begin{cases}
 \Theta_0^0+s,&a=b,\\
 \Theta_1^0+s,&a\ne b,
 \end{cases}
 \qquad
 \tau_{ab}=\Theta_{ab}(s)/\sqrt\varepsilon.
 \tag{2}
\]

The frozen node model is

\[
\begin{aligned}
 \dot v_i={}&v_i-\frac{v_i^3}{3}-w_i
 +D\sum_jP_{ij}(v_j-v_i)\\
 &+\varepsilon\sum_jP_{ij}
 \left\{
 \kappa_1[v_j(t-\tau_{ij})-v_i]
 +\kappa_3[(v_j(t-\tau_{ij})-1)^3-(v_i-1)^3]
 \right\},\\
 \dot w_i={}&\varepsilon(v_i-a).
\end{aligned}
\tag{3}
\]

Here \(D>0\) is a fixed instantaneous synchronization scaffold, not an
actuator. It vanishes on the collective history. The three weak delayed
actuators are

\[
 u=(\kappa_1,\kappa_3,s).
 \tag{4}
\]

The right fold is normalized to \((v,w,a)=(1,2/3,1)\). Centering the cubic
actuator at \(v_*=1\) keeps it out of the first local threshold coefficient
while allowing it to affect the full periodic orbit.

A symbolic parameter wedge is

\[
 D\in[D_0,D_1],\quad
 \kappa_1\in[\kappa_-,\kappa_+]\subset(0,\infty),\quad
 |\kappa_3|\le\kappa_3^*,\quad |s|\le s^*,
 \tag{5}
\]

with all scaled delays in \((0,\Theta_{\max})\). Numerical values are not
frozen until the periodic branch and unique-extrema conditions are checked.

## 2. Exact history reductions

For \(i\in C_a\), the row-weighted delay measure from source module \(C_b\)
is exactly

\[
 \sum_{j\in C_b}P_{ij}\delta_{\Theta_{ij}(s)}
 =\frac12\delta_{\Theta_{ab}(s)},
 \tag{6}
\]

independent of the receiving node. Hence the block-synchronous history space
is invariant. For \(b\ne a\), its restriction is

\[
\begin{aligned}
 \dot V_a={}&V_a-\frac{V_a^3}{3}-W_a
 +\frac D2(V_b-V_a)\\
 &+\frac\varepsilon2\left[
 \Psi(V_a,V_a(t-\tau_0))
 +\Psi(V_a,V_b(t-\tau_1))
 \right],\\
 \dot W_a={}&\varepsilon(V_a-a),
\end{aligned}
\tag{7}
\]

where

\[
 \Psi(x,y)=\kappa_1(y-x)+\kappa_3[(y-1)^3-(x-1)^3].
 \tag{8}
\]

The completely synchronous history space is also invariant. It gives the
scalar two-delay RFDE

\[
\begin{aligned}
 \dot V={}&V-\frac{V^3}{3}-W
 +\varepsilon\kappa_1
 \left[\frac{V(t-\tau_0)+V(t-\tau_1)}2-V\right]\\
 &+\varepsilon\kappa_3
 \left[
 \frac{(V(t-\tau_0)-1)^3+(V(t-\tau_1)-1)^3}{2}
 -(V-1)^3
 \right],\\
 \dot W={}&\varepsilon(V-a).
\end{aligned}
\tag{9}
\]

These invariance statements follow directly from substitution and RFDE
uniqueness; no approximation or spectral closure is used.

## 3. Collective mode and first delay moment

At module level,

\[
 r_c=(1,1)^\top,
 \qquad
 \ell_c=\frac12(1,1)^\top,
 \qquad \ell_c^\top r_c=1.
 \tag{10}
\]

The operator-valued delay measure is

\[
 \mathbb B(d\theta)
 =\frac12
 \begin{pmatrix}
 \delta_{\Theta_0}(d\theta)&\delta_{\Theta_1}(d\theta)\\
 \delta_{\Theta_1}(d\theta)&\delta_{\Theta_0}(d\theta)
 \end{pmatrix}.
 \tag{11}
\]

It preserves \(r_c\) as a measure identity, and

\[
 M_1^{(2)}=\frac{\Theta_0+\Theta_1}{2},
 \qquad \partial_sM_1^{(2)}=1.
 \tag{12}
\]

The actuator sign in (3) is delayed-minus-current. Relative to the
current-minus-delayed calibration, \(K=-\kappa_1\). The formal collective law
is therefore

\[
 a_c
 =1-\frac18\varepsilon
 -\frac{\kappa_1}{8}M_1^{(2)}\varepsilon^{3/2}
 +O(\varepsilon^2),
 \tag{13}
\]

and

\[
 \partial_s a_c
 =-\frac{\kappa_1}{8}\varepsilon^{3/2}
 +O(\varepsilon^2).
 \tag{14}
\]

The operating point must have \(\kappa_1^0\ne0\); otherwise the leading delay
column of the safety response vanishes.

This symmetric model is intentionally simple enough for Corollary C, but its
collective dynamics reduce exactly to (9). It is **not** the nontrivial
two-module example for Proposition B. A genuinely modular moment law needs
nonidentical module-pair measures or critical modes and must retain any
same-order transverse resolvent term.

## 4. One fast fold direction in the concrete benchmark

At the synchronous fold, the instantaneous fast voltage Jacobian contributed
by the scaffold is

\[
 D(P-I).
 \tag{15}
\]

Since \(P\) is a rank-one projection, (15) has eigenvalue zero on the
collective voltage mode and eigenvalue \(-D\) on all \(N-1\) transverse
voltage modes. Thus the layer problem has one fast fold direction. The weak
delayed terms perturb the transverse fast spectrum only by \(O(\varepsilon)\)
on compact parameter sets.

This algebra does not prove a uniform bound for the complete Lin operator:
transverse recovery variables and the entry/exit passage still enter
\(G_\perp(\delta)\). It does remove the immediate multi-fold contradiction
present in the weak-only identical-module reference.

## 5. Output and safety coordinates

Fix

\[
 \bar v_a=\frac1{n_a}\sum_{i\in C_a}v_i,
 \qquad
 h_N=\frac23\bar v_1+\frac13\bar v_2.
 \tag{16}
\]

The output is deliberately different from the collective adjoint weight. On
a declared hyperbolic periodic branch with unique nondegenerate extrema, use

\[
 F=1/T,
 \qquad
 R_h=(\max h_N-\min h_N)^2.
 \tag{17}
\]

If \(a>a_c\) is the nonpulsatile side in the selected wedge, the positive
safety margin is

\[
 S_c=a_{\rm op}-a_c.
 \tag{18}
\]

The earlier notation \(\Delta_c=a_c-a_{\rm op}\) equals \(-S_c\); it should
not be described as increasing safety. The Lin root defines \(a_c\), while
\(h_N\) defines amplitude and experimental validation.

## 6. Why weak delayed coupling alone fails the uniform gate

For the diagnostic weak-only model, set \(D=0\), use current-minus-delayed
coupling \(J=\varepsilon K\), and let \(\lambda\) be a network eigenvalue.
With \(\delta=\sqrt\varepsilon\), the fold-scaled variational equation is

\[
 u'=-2Xu+v
 +\delta[-X^2u+K(u-\lambda u(s-\Theta))],
 \qquad v'=-u.
 \tag{19}
\]

The topology, gain, and delay disappear at \(\delta=0\). On the canonical
leading canard \(X_0=-s/2\), every network mode has

\[
 A_0(s)=\begin{pmatrix}s&1\\-1&0\end{pmatrix},
 \quad
 \phi_0=(-1,s)^\top,
 \quad
 \psi_0=e^{-s^2/2}(s,1)^\top.
 \tag{20}
\]

Thus the singular problem contains a relative-canard copy in every network
mode. If the post-phase transverse family satisfies
\(L_{\perp,\delta}=L_{\perp,0}+O(\delta)\) and becomes invertible for
\(\delta>0\), then a normalized kernel vector gives the conditional lower
bound

\[
 G_\perp(\delta)\ge c\delta^{-1}.
 \tag{21}
\]

This rules out an assumed \(O(1)\) inverse, but it does not determine the
actual exponent.

## 7. Canonical inner splitting: first order cancels

Let \(\kappa=K(1-\lambda)\). In the symmetric whole-line inner problem, the
first relative operator sends the tangent to a constant fast forcing. Its
adjoint projection is

\[
 M_{1,\lambda}
 =\kappa\int_{-\infty}^{\infty}s e^{-s^2/2},ds=0.
 \tag{22}
\]

The forcing is in the range: with
\(L_0(U,V)=(U'-sU-V,V'+U)\),

\[
 r_1=(0,\kappa),
 \qquad L_0r_1=(-\kappa,0).
 \tag{23}
\]

For the generalized slow equation
\(Y'=-X+\delta(\nu-bY)\), the resulting formal second reduced coefficient is

\[
 \boxed{
 M_{2,\lambda}
 =K(1-\lambda)\frac{1+2b}{4}\sqrt{2\pi}.
 }
 \tag{24}
\]

Hence the canonical symmetric whole-line inner calculation predicts

\[
 G_\perp(\varepsilon)
 \asymp
 \frac{1}{\varepsilon|K|\,\min\{1,p+q\}}
 \tag{25}
\]

for the collective, module-difference, and within-module decomposition, if
the second reduced matrix is the only obstruction and is nonsingular.
Equation (25) is a formal diagnostic, not a theorem.

Finite or asymmetric sections can restore an order-\(\delta\) interior term,

\[
 \int_{s_-}^{s_+}s e^{-s^2/2},ds
 =e^{-s_-^2/2}-e^{-s_+^2/2},
 \tag{26}
\]

and the complete coefficient also contains boundary and phase terms. The
actual exponent must therefore be computed from the frozen BVP in the
[Lin-gap specification](lin-gap-feasibility.md).

The executable identities are in
`src/canard_control/transverse_modes.py`. A separate nonlinear scalar-mode
surrogate can produce an order-\(\delta\) canard-parameter shift, but that
surrogate is not an invariant transverse network subsystem and is not used as
evidence for \(G_\perp\).

## 8. Residual normalization and decision

Let \(\eta_W\) denote a raw weight residual. In (19), its blown-up operator
size is \(O(\delta|K|\eta_W)\), not \(O(\eta_W)\). The perturbative condition
is therefore

\[
 G_\perp(\delta)\,\delta|K|\eta_W\ll1.
 \tag{27}
\]

Under the formal scaling (25), this already suggests
\(\eta_W=o(\sqrt\varepsilon)\). The exact threshold-error requirement must be
derived in the physical parameter after the dynamic adjoint and
\(\partial_\nu d\) are normalized; no stronger raw-residual exponent is
claimed here.

The project decision is:

1. Corollary C uses the proof-oriented scaffolded model (3).
2. Theorem A keeps \(G_\perp(\delta)\) explicit and does not infer it from an
   adjacency gap.
3. The weak-only identical-module class is retained as a negative control and
   as a possible narrow exact-invariant theorem, not as the broad reference.
4. Proposition B uses a separate nontrivial modular reference; the symmetric
   control benchmark cannot supply that novelty.
5. Large heterogeneous simulations remain blocked until the augmented Lin
   operator and its smallest singular value are implemented.
