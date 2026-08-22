# Shared recovery: a formal transverse moment calculation

## 1. Status and purpose

This note repairs the extra slow center in the two-module source-history
example and computes the first coefficient by which its hidden transverse
delay moment can return to the scalar canard solvability condition.

Three levels of assertion must remain separate.

1. **Exact algebra.** The shared-recovery singular matrix has one critical
   voltage--recovery Jordan chain and one stable transverse voltage mode. The
   coordinate change and quadratic FHN terms are exact. Once the displayed
   truncated inner and finite-section problems are fixed, their range response
   and adjoint identities are also exact symbolic identities.
2. **Formal local conclusion.** For the stated blow-up and a frozen symmetric
   Lin section, the interior contribution is

   \[
   \mathcal J_{\perp,0}
   =\frac{\eta(\theta _0-\theta _1)}4.
   \tag{1}
   \]

   For fixed inner delays, it is \(O(1)\) as
   \(\delta=\sqrt\varepsilon\to0\), rather than being suppressed by an
   additional power of \(\delta\).
3. **Not proved here.** Equation (1) is not an RFDE threshold theorem. A
   theorem still needs the RFDE solution manifold, advanced dynamic adjoint,
   entry/exit bundles, history-jump terms, a one-dimensional cokernel, and a
   uniform remainder. Those terms could change, or in a special geometry
   cancel, the interior coefficient.

The executable identities are in
`src/canard_control/shared_recovery_moment.py`.

## 2. Why the original recovery architecture is insufficient

Let

\[
A_0=\begin{pmatrix}-1&1/2\\2&-1\end{pmatrix}=-2P_\perp,
\quad
r=\binom{1}{2},
\quad
\ell=\binom{1/2}{1/4},
\tag{2}
\]

so that \(A_0r=0\), \(\ell^\top A_0=0\), and
\(\ell^\top r=1\). With two independent recovery variables, the singular
linearization is

\[
J_{\mathrm{two}}=
\begin{pmatrix}A_0&-I_2\\0&0\end{pmatrix},
\qquad
\det(\lambda I-J_{\mathrm{two}})=\lambda^3(\lambda+2),
\tag{3}
\]

and \(\dim\ker J_{\mathrm{two}}=2\). Thus there is an additional slow
recovery direction. A scalar gap and scalar dynamic adjoint are not intrinsic
unless one first prescribes a compatible fiber or makes that direction
hyperbolic.

There are two clean repairs.

- Use one shared recovery variable. This is the minimal analytic model used
  below.
- Retain two recovery variables but add a fixed, non-actuated transverse
  scaffold \(-D_wP_\perp w\), \(D_w>0\). The singular characteristic
  polynomial becomes

  \[
  \lambda^2(\lambda+2)(\lambda+D_w),
  \tag{4}
  \]

  and the kernel is one-dimensional. This is the appropriate repair for a
  two-recovery biological reference or for a collective-network corollary.

The scaffold should be part of the reference dynamics, not one of the three
control actuators. It vanishes on the collective subspace and supplies a
fixed gap in the transverse recovery block of the singular current-state
matrix. This does not by itself establish an RFDE spectral gap.

## 3. Shared-recovery eta family

Put \(\sigma=\sqrt{3/2}\), \(v_*=(\sigma,0)^\top\), and
\(\delta=\sqrt\varepsilon\). In fast time consider

\[
\begin{aligned}
\dot v_1={}&v_1-\frac{v_1^3}{3}-W
+\frac12(v_2-v_1)+\varepsilon K\,\mathcal H_{\eta,1}[v_t],\\
\dot v_2={}&v_2-\frac{v_2^3}{3}-2W
+2(v_1-v_2)-2\sigma+\varepsilon K\,\mathcal H_{\eta,2}[v_t],\\
\dot W={}&\varepsilon\{\ell^\top(v-v_*)-\mu\}.
\end{aligned}
\tag{5}
\]

The constant input in the second equation only locates the fold at
\((v_*,W)=(v_*,0)\). The source-history feedback is

\[
\mathcal H_\eta[v_t]
=Bv(t)-C_0^\eta v(t-\theta_0/\delta)
-C_1^\eta v(t-\theta_1/\delta),
\tag{6}
\]

with the matrices from the two-module moment example,

\[
C_0^\eta=C_0+\eta T,
\qquad
C_1^\eta=C_1-\eta T,
\qquad
B=C_0+C_1,
\tag{7}
\]

\[
T=\begin{pmatrix}1&0\\-2&0\end{pmatrix},
\qquad
Tr=q=\binom{1}{-2},
\qquad
\ell^\top q=0.
\tag{8}
\]

Consequently the eta deformation leaves the total matrix and the projected
delay measure unchanged, but its delayed-source part forces the transverse
mode by

\[
-\varepsilon K\eta q
\{\xi(t-\theta_0/\delta)-\xi(t-\theta_1/\delta)\}
\tag{9}
\]

on a critical-mode history \(v-v_*=r\xi\).

The singular matrix for \((v,W)\) is

\[
J_{\mathrm{shared}}=
\begin{pmatrix}A_0&-r\\0&0\end{pmatrix},
\qquad
\det(\lambda I-J_{\mathrm{shared}})
=\lambda^2(\lambda+2),
\qquad
\dim\ker J_{\mathrm{shared}}=1.
\tag{10}
\]

This is the necessary current-state center structure for a planar
fold/canard reduction. It does not by itself construct that reduction or
prove that the full RFDE Lin operator has a scalar cokernel.

## 4. Canonical critical and transverse coordinates

Let

\[
q=\binom{1}{-2},
\qquad
m=\binom{1/2}{-1/4},
\qquad
\alpha=\frac\sigma2,
\tag{11}
\]

and write

\[
v-v_*=r\xi+q\zeta,
\qquad
x=\alpha\xi,
\qquad
z=\alpha\zeta,
\qquad
y=-\alpha W,
\qquad
a=\alpha\mu.
\tag{12}
\]

The dual identities are

\[
\ell^\top r=m^\top q=1,
\qquad
\ell^\top q=m^\top r=0.
\tag{13}
\]

Direct expansion of the local FHN field through quadratic order gives

\[
\dot x=y-(x+z)^2+O_3(x,z),
\qquad
\dot z=-2z-(x+z)^2+O_3(x,z),
\tag{14}
\]

and

\[
\dot y=\varepsilon(a-x).
\tag{15}
\]

Only the eta-dependent part of the delay feedback is needed below. Because
of (13), it has no direct critical projection and contributes

\[
-\varepsilon K\eta
\{x(t-\theta_0/\delta)-x(t-\theta_1/\delta)\}
\tag{16}
\]

to the transverse equation. Eta-independent feedback and cubic terms affect
the baseline canard coefficients but not the isolated linear-in-eta channel
calculated here.

For the scaffold alternative, the transverse voltage--recovery block is

\[
\begin{pmatrix}-2&-1\\0&-D_w\end{pmatrix}.
\tag{17}
\]

Its inverse maps a pure voltage forcing \((1,0)^\top\) to
\((-1/2,0)^\top\). Hence the leading local eta coefficient below is
unchanged by the scaffold. The scaffold removes the displayed
finite-dimensional center obstruction; well-posedness of the RFDE reduction
remains a separate theorem obligation.

## 5. Blow-up and transverse range inverse

Use

\[
x=\delta X,
\quad y=\delta^2Y,
\quad z=\delta^2Z,
\quad a=\delta^2\nu,
\quad s=\delta t.
\tag{18}
\]

The leading singular canard is

\[
X_0(s)=-\frac{s}{2}.
\tag{19}
\]

The stable transverse equation has an eta-independent leading solution
\(Z_0\). Differentiating only the eta channel, its first correction satisfies

\[
\delta Z_\eta'(s)+2Z_\eta(s)
=-\delta K\eta
\{X_0(s-\theta_0)-X_0(s-\theta_1)\}.
\tag{20}
\]

The affine history makes the delay translation exact:

\[
X_0(s-\theta_0)-X_0(s-\theta_1)
=\frac{\theta_0-\theta_1}{2}.
\tag{21}
\]

The unique bounded whole-line response of the frozen inner equation is
therefore

\[
Z_\eta^{\mathrm{bd}}
=-\delta\frac{K\eta(\theta_0-\theta_1)}4.
\tag{22}
\]

If instead \(Z_\eta(-L)=0\) is imposed, the exact finite-section response is

\[
Z_\eta^{\mathrm{in}}(s)
=Z_\eta^{\mathrm{bd}}
\left(1-e^{-2(s+L)/\delta}\right).
\tag{23}
\]

Thus the difference is a stable entry layer. Formula (22) identifies the
coefficient

\[
Z_{1,\eta}
=-\frac{K\eta(\theta_0-\theta_1)}4
\tag{24}
\]

when \(Z=Z_0+\delta Z_1+\cdots\). Since the critical quadratic term in
(14) contains \(-2\delta XZ\) after blow-up, (24) returns at the next inner
order as

\[
f_\eta(s)=-2X_0(s)Z_{1,\eta}
=-\frac{K\eta(\theta_0-\theta_1)}4s.
\tag{25}
\]

This order bookkeeping matters: the eta response is \(O(\delta)\) in
\(Z\), but its coefficient contributes to \(\nu_1\) and hence to the
physical canard parameter at order \(K\delta^3=K\varepsilon^{3/2}\).

## 6. Formal dynamic adjoint and whole-line pairing

At the order containing (25), the critical correction \(u=(U,V)^\top\)
obeys the formal operator equation

\[
L_0u=\binom{f_\eta}{\nu_{1,\eta}},
\qquad
L_0(U,V)=\binom{U'-sU-V}{V'+U}.
\tag{26}
\]

The tangent mode and a decaying adjoint mode are

\[
\phi(s)=\binom{-1}{s},
\qquad
\psi(s)=e^{-s^2/2}\binom{s}{1}.
\tag{27}
\]

They satisfy \(L_0\phi=0\) and \(L_0^*\psi=0\) exactly. The interior
pairings are

\[
N_\eta
=\int_{\mathbb R}\psi_1f_\eta\,ds
=-\frac{K\eta(\theta_0-\theta_1)}4\sqrt{2\pi},
\tag{28}
\]

\[
D_\nu
=\int_{\mathbb R}\psi_2\,ds
=\sqrt{2\pi}.
\tag{29}
\]

With the sign convention in (26), solvability is
\(N_\eta+\nu_{1,\eta}D_\nu=0\), so

\[
\nu_{1,\eta}
=\frac{K\eta(\theta_0-\theta_1)}4,
\qquad
\mathcal J_{\perp,0}
:=\frac{\nu_{1,\eta}}K
=\frac{\eta(\theta_0-\theta_1)}4.
\tag{30}
\]

Because \(a=\alpha\mu=\delta^2\nu\), the corresponding formal coefficient
in the original unfolding coordinate is

\[
[\mu_c]_{K\eta\delta^3}
=\frac{K\eta\delta^3(\theta_0-\theta_1)}{4\alpha},
\tag{31}
\]

where the bracket records only this monomial in the formal expansion. It is
subject to all RFDE qualifications in Section 8.

## 7. A finite-section normalization and its boundary term

On \([-L,L]\), impose the tangent-compatible endpoint lines

\[
V(-L)-LU(-L)=0,
\qquad
V(L)+LU(L)=0,
\tag{32}
\]

and the phase condition \(U(0)=0\). The multipliers paired with the left
endpoint, right endpoint, and phase residuals are

\[
e^{-L^2/2},
\qquad
-e^{-L^2/2},
\qquad
0,
\tag{33}
\]

respectively. These values annihilate the endpoint traces of the adjoint
exactly.

Set

\[
I_0(L)=\int_{-L}^Le^{-s^2/2}\,ds,
\qquad
I_2(L)=\int_{-L}^Ls^2e^{-s^2/2}\,ds
=I_0(L)-2Le^{-L^2/2}.
\tag{34}
\]

For the frozen endpoint lines and the bounded candidate response (22), the
interior result is

\[
\nu_{1,\eta}^{\mathrm{int}}(L)
=\frac{K\eta(\theta_0-\theta_1)}4
\frac{I_2(L)}{I_0(L)},
\tag{35}
\]

which converges to (30) as \(L\to\infty\).

Using the zero-incoming response (23) instead subtracts

\[
\frac{K\eta(\theta_0-\theta_1)}{4I_0(L)}
\int_{-L}^L s^2e^{-s^2/2}e^{-2(s+L)/\delta}\,ds
\tag{36}
\]

from (35). For fixed \(L\), the integral is bounded by
\(L^2\delta/2\), so this entry-layer choice changes the finite-section
coefficient by \(O(\delta)\), but not its nonzero \(O(1)\) limit.

More generally, let \(\beta_-\) and \(\beta_+\) denote the direct
linear-in-eta residuals of the two endpoint equations at this order. Their
adjoint pairing is

\[
e^{-L^2/2}(\beta_- -\beta_+),
\tag{37}
\]

and the formal root becomes

\[
\nu_{1,\eta}(L)
=\frac{K\eta(\theta_0-\theta_1)}4
\frac{I_2(L)}{I_0(L)}
-\frac{e^{-L^2/2}(\beta_- -\beta_+)}{I_0(L)}.
\tag{38}
\]

The fixed algebraic section has \(\beta_-=\beta_+=0\). True RFDE
entry/exit bundles and history jumps need not have zero derivatives, which is
why (38), rather than (35) alone, is the correct theorem-design template.

## 8. What an RFDE theorem must still prove

To promote the calculation to Proposition B, one must construct an augmented
RFDE Lin operator for the repaired model and prove all of the following.

- The relevant slow manifolds and history segments lie in a specified RFDE
  phase/solution manifold.
- After phase fixing, the linearized Lin problem has a one-dimensional
  cokernel and a uniformly bounded range inverse in the chosen weighted
  spaces.
- The advanced dynamic adjoint, including its jumps at discrete-delay atoms,
  converges to the local adjoint (27) in the singular limit.
- The derivatives of the entry/exit bundles and complete-history jump yield
  the boundary contribution in (38), with no unaccounted leading term.
- The eta-dependent coefficient is uniform for the declared ranges of
  \(K,\eta,\theta_j\), and the remainder is of the order claimed in the
  threshold expansion.

Until those points are established, the mathematically justified conclusion
is narrower but nontrivial: the projected first moment does not determine the
formal inner threshold coefficient, the hidden transverse channel is
generically nonzero in this repaired example, and its local contribution is
not \(\delta\)-degenerate.
