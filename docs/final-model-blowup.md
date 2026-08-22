# Exact blow-up of the final two-module model

Status: **exact symbolic model reduction, followed by one explicitly formal
inner pairing.** This note fixes the coordinates and powers of
\(\delta=\sqrt\varepsilon\) used in the base theorem. It does not assert the
existence of a singular RFDE invariant manifold or a maximal canard.

The executable certificate is
`src/canard_control/final_model_blowup.py`; its independent regression tests
are in `tests/test_final_model_blowup.py`.

## 1. Modal coordinates and physical equation

For the model (M), put

\[
 u=v-v_*,\qquad p=w-w_*,
\]

and use

\[
 r=\binom{1}{2},\quad q=\binom{1}{-2},\qquad
 \ell=\binom{1/2}{1/4},\quad m=\binom{1/2}{-1/4}.
\]

Thus

\[
 u=r\xi+q\zeta,\qquad p=r\rho+q\kappa,
\]

with

\[
 \ell^Tr=m^Tq=1,\qquad \ell^Tq=m^Tr=0.
\]

Set

\[
 \sigma=\sqrt{\frac32},\qquad
 \alpha=\frac{\sigma}{2}=\frac{\sqrt6}{4}.
\]

The two delay layers in modal coordinates are exactly

\[
 \begin{aligned}
 [C_0^\eta]_{(r,q)}&=
 \begin{pmatrix}
 1/3&-1/12\\ \eta&1/12+\eta
 \end{pmatrix},\\
 [C_1^\eta]_{(r,q)}&=
 \begin{pmatrix}
 2/3&-1/12\\ -\eta&1/12-\eta
 \end{pmatrix},\\
 [B]_{(r,q)}&=
 \begin{pmatrix}1&-1/6\\0&1/6\end{pmatrix}.
 \end{aligned}
\tag{1}
\]

In particular, the \(\eta\)-deformation has modal matrix

\[
 [T]_{(r,q)}=\begin{pmatrix}0&0\\1&1\end{pmatrix}.
\tag{2}
\]

It has no direct critical projection and acts on the transverse component
through the delayed first voltage coordinate \(\xi+\zeta\).

At \(\varepsilon=0\), the current-state Jacobian of (M) is

\[
 J_0=
 \begin{pmatrix}
 A_0&-I\\0&-D_wP_\perp
 \end{pmatrix},
 \qquad
 \det(\lambda I-J_0)
 =\lambda^2(\lambda+2)(\lambda+D_w).
\tag{3}
\]

Its kernel is one-dimensional and its generalized center is the collective
Jordan chain of length two. Equation (3) is a finite-dimensional identity;
it is not a spectral-gap theorem for the full delay generator.

## 2. The required anisotropic blow-up

The raw coordinates used here agree with
\(X=\delta^{-1}\ell^T(v-v_*)\). The complete scaling is

\[
\boxed{
\begin{aligned}
 v(t)&=v_*+\delta rX(s)+\delta^2qZ(s),\\
 w(t)&=w_*-\delta^2rY(s)+\delta^4qW(s),\\
 \mu&=\delta^2\nu,\qquad s=\delta t.
\end{aligned}}
\tag{4}
\]

The transverse recovery is \(O(\delta^4)\), not \(O(\delta^2)\). If all
recovery components were instead scaled isotropically by \(\delta^2\), the
fixed physical coupling would appear with coefficient \(-D_w/\delta\) in
the \(s\)-equation. Formula (4) resolves its nontrivial invariant-graph scale.

Since the physical delays are \(\tau_k=\theta_k/\delta\),

\[
 \delta(t-\tau_k)=s-\theta_k.
\]

The rescaled history interval is therefore the fixed interval
\([-\theta_1,0]\).

For a history \(\phi\), write

\[
 \phi_k=\phi(s-\theta_k),\qquad
 \Delta\phi=\phi_0-\phi_1,
\]

and define

\[
\begin{aligned}
 \mathcal D_c\phi
 &=\phi-\frac13\phi_0-\frac23\phi_1,\\
 \mathcal D_{cz}\phi
 &=-\frac16\phi+\frac1{12}\phi_0+\frac1{12}\phi_1,\\
 \mathcal D_z\phi&=-\mathcal D_{cz}\phi.
\end{aligned}
\tag{5}
\]

## 3. Exact fixed-scaled-delay chart

Direct substitution of (4) into the physical model (M), followed by the
\(\ell\)- and \(m\)-projections, gives the exact polynomial RFDE

\[
\begin{aligned}
X'={}&Y-\alpha X^2\\
&+\delta\left[
K\mathcal D_cX-2\alpha XZ-\frac{20}{9}\alpha^2X^3
\right]\\
&+\delta^2\left[
K\mathcal D_{cz}Z-\alpha Z^2+4\alpha^2X^2Z
\right]\\
&-\delta^3\frac{20}{3}\alpha^2XZ^2
+\delta^4\frac43\alpha^2Z^3,\\[1mm]
Y'={}&-X+\delta\nu,\\[1mm]
\delta Z'={}&-2Z-\alpha X^2\\
&+\delta\left[
-2\alpha XZ+\frac43\alpha^2X^3-K\eta\Delta X
\right]\\
&+\delta^2\left[
-W-\alpha Z^2-\frac{20}{3}\alpha^2X^2Z
+K(\mathcal D_zZ-\eta\Delta Z)
\right]\\
&+\delta^3 4\alpha^2XZ^2
-\delta^4\frac{20}{9}\alpha^2Z^3,\\[1mm]
\delta W'={}&Z-D_wW.
\end{aligned}
\tag{6}
\]

This statement is exact. The symbolic certificate constructs the physical
FitzHugh--Nagumo field, the two perturbed delay matrices, and the recovery
scaffold first. It then substitutes (4) and verifies both projected and
full-vector reconstruction residuals:

\[
R_X=R_Z=R_Y=R_W=0,\qquad
R_{\mathrm{fast}}=R_{\mathrm{slow}}=0.
\tag{7}
\]

Thus (7) is not obtained by comparing two separately hard-coded copies of
(6).

## 4. Exact singular algebraic graph

Setting \(\delta=0\) in the last two equations of (6) gives

\[
 -2Z-\alpha X^2=0,\qquad Z-D_wW=0.
\]

Their unique solution is

\[
 \boxed{
 Z_0=-\frac{\alpha}{2}X^2,\qquad
 W_0=-\frac{\alpha}{2D_w}X^2.}
\tag{8}
\]

After imposing (8), the leading critical system is

\[
 X'=Y-\alpha X^2,\qquad Y'=-X.
\tag{9}
\]

Equations (8)--(9) are exact singular-limit algebra. They do not prove that
an invariant history graph persists for positive \(\delta\).

## 5. Formal lowest-order transverse return

The leading whole-line canard of (9) is

\[
 X_0(s)=-\frac{s}{2\alpha},\qquad
 Y_0(s)=\frac{s^2-2}{4\alpha}.
\tag{10}
\]

If \(Z=Z_0+\delta Z_1+\cdots\), differentiation of the
\(O(\delta)\) transverse equation with respect to \(\eta\) at zero gives

\[
 \partial_\eta Z_1
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}.
\tag{11}
\]

Its return through \(-2\alpha\delta XZ\) is

\[
 f_{\perp,\eta}(s)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
\tag{12}
\]

For the formal whole-line operator

\[
 L_0(U,V)=\binom{U'-sU-V}{V'+U},
\]

the decaying adjoint solution is

\[
 \psi(s)=e^{-s^2/2}\binom{s}{1}.
\]

The Gaussian solvability pairing yields

\[
 \partial_\eta\nu_1(0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}.
\]

Since \(\mu=\delta^2\nu\), the resulting formal prediction is

\[
 \boxed{
 \partial_\eta\mu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta^3
 +O(\delta^4)
 =\frac{K(\theta_0-\theta_1)}{\sqrt6}\delta^3
 +O(\delta^4).}
\tag{13}
\]

Thus the audited sign is the sign of
\(K(\theta_0-\theta_1)\). In particular, for
\(K>0\) and \(\theta_0<\theta_1\), the displayed leading derivative is
negative. The coefficient is independent of \(D_w\): the recovery variable
\(W\) first enters the transverse voltage equation at order \(\delta^2\),
after (11) has already been determined.

Within this note, (13) is only formal. The subsequent construction in
[special-flow-graph-theorem.md](special-flow-graph-theorem.md) and the
parameterized splitting in
[reduced-canard-root.md](reduced-canard-root.md) make it rigorous on a fixed
compact tube. Its identification with the selected physical long-delay root
still requires the estimates in
[k1-tail-compatibility.md](k1-tail-compatibility.md).

## 6. Obligations not proved by this blow-up note

No code or identity in this note alone proves any of the following:

1. that the full delay generator has exactly two relevant roots and a
   uniformly bounded complementary inverse;
2. that the singular equations (6) possess a two-dimensional invariant
   history graph, with the parameter regularity required by (13);
3. that the attracting and repelling histories intersect at a simple root;
4. that the reduced intersection lifts to equality of complete RFDE
   histories;
5. that the endpoint and history-jump terms leave the whole-line coefficient
   in (13) unchanged;
6. that the claimed uniform remainder holds.

The fixed physical recovery coupling becomes singular after the time change,
so a standard parameter-smooth RFDE center-manifold theorem cannot be cited
without additional work. The special-flow graph theorem now supplies the
uniform compact-tube graph and its finite jets. What remains for the
long-delay model is not this local graph, but its controlled use on growing
logarithmic tubes and the selected attracting/repelling trace estimates.
