# Exact arbitrary-\(N\) blow-up and special-flow model fit

Status: **proved model-fitting lemma for the lifted node class,
2026-08-23.** The identities below hold for every \(n_1,n_2\geq 1\), and
all estimates use the node maximum norm with constants independent of
\(N=n_1+n_2\). Together with the abstract result in
[dimension-uniform-special-flow-history-graph.md](dimension-uniform-special-flow-history-graph.md),
they give a dimension-uniform invariant complete-history graph on the
logarithmic fold tube for the prepared lifted class.

By themselves they do **not** give a complete-history gap inverse, a canard
root, an outer slow-manifold selection, or a biological pulse theorem.  The
compatible canonical root for this exact quotient is now supplied by the
separate
[selected-root lift theorem](paper-ii-selected-root-lift-and-symmetry-breaking.md),
which uses equivariance and the proved two-module trace rather than silently
assuming a new arbitrary-network Lin inverse. The exact algebra here is
reproduced in
[lifted_network_blowup.py](../src/canard_control/lifted_network_blowup.py);
the tests compare its block-constant restriction with the already audited
two-module chart.

## 1. The full stable fiber

Use the projectors and vectors from
[paper-ii-lifted-two-module-class.md](paper-ii-lifted-two-module-class.md)
and write

\[
 P_\perp=I-P_c=P_m+P_w,
 \qquad E_N=P_\perp\mathbb R^N,
 \tag{1.1}
\]

with the norm inherited from \(\ell^\infty_N\). The voltage linearization is

\[
 A_{v,N}=-2P_m-D_vP_w.
 \tag{1.2}
\]

The stable fiber required by the graph theorem is

\[
 \mathcal E_N=E_N\times E_N,\qquad
 \|(U,V)\|_{\mathcal E_N}
 =\max\{\|U\|_\infty,\|V\|_\infty\}.
 \tag{1.3}
\]

Thus every module-difference and within-module voltage and recovery
direction is retained. No invariant two-dimensional module restriction is
used in the graph construction. Let

\[
 D_*:=\operatorname{diag}(v_*),\qquad
 \alpha=\frac12\sqrt{\frac32}=\frac{\sqrt6}{4}.
 \tag{1.4}
\]

For the nodewise cubic field, Taylor expansion at the fold is the exact
identity

\[
 \mathcal F_N(v_*+\xi,w_*+\omega)
 =A_{v,N}\xi-\omega-D_*(\xi\odot\xi)-\frac13\xi^{\odot3}.
 \tag{1.5}
\]

Hadamard multiplication has multilinear norm one on \(\ell^\infty_N\).
This fact makes the nonlinear estimates below independent of \(N\).

## 2. Fixed-support delay operator

The equitable model has layers \(A_{k,N}^\eta\) and current gain
\(B_N=A_{0,N}^\eta+A_{1,N}^\eta\). Include balanced residual layers by

\[
 \widetilde A_{k,N}=A_{k,N}^\eta+E_{k,N},\qquad
 \widetilde B_N=\widetilde A_{0,N}+\widetilde A_{1,N},
 \tag{2.1}
\]

and define

\[
 \mathcal L_{N,\eta,\mathcal R}[\psi]
 =\widetilde B_N\psi(0)
  -\widetilde A_{0,N}\psi(-\theta_0)
  -\widetilde A_{1,N}\psi(-\theta_1),\qquad
 \mathcal R=(E_{0,N},E_{1,N}).
 \tag{2.2}
\]

The declared model is \(\mathcal R=0\). The non-equitable family in Section
6 of the class note has \(E_{0,N}+E_{1,N}=0\), so its current term remains
exactly \(B_N\). For a fixed operator-TV ball

\[
 \|\mathcal R\|_{\mathrm{TV},\infty}
 :=\|E_{0,N}\|_{\infty\to\infty}
   +\|E_{1,N}\|_{\infty\to\infty}\leq R_*,
 \tag{2.3}
\]

the norm of (2.2) is bounded uniformly in \(N\). The graph theorem receives
the two delayed chart states through

\[
 \mathscr E_N\phi
 =\bigl(\phi(-\theta_0),\phi(-\theta_1)\bigr).
 \tag{2.4}
\]

With the maximum-product norm, this is represented by

\[
 \mathbb E_N=J_0\delta_{-\theta_0}+J_1\delta_{-\theta_1},\qquad
 \|J_0\|=\|J_1\|=1,\qquad
 \|\mathbb E_N\|_{\mathrm{TV}}=2.
 \tag{2.5}
\]

The measure is independent of \(\delta,\nu,\eta,\mathcal R\), so all its
parameter derivatives vanish. Layer-parameter dependence stays in the
finite-dimensional nonlinear maps below; no moving Dirac mass is
differentiated in operator TV.

## 3. Exact anisotropic chart

Let \(\delta=\sqrt\varepsilon\), \(\mu=\delta^2\nu\), and \(s=\delta t\).
Use the full-fiber scaling

\[
 \begin{aligned}
 v(t)&=v_*+\delta r_NX(s)+\delta^2z(s),\\
 w(t)&=w_*-\delta^2r_NY(s)+\delta^4W(s),
 \end{aligned}
 \qquad z,W\in E_N.
 \tag{3.1}
\]

The translations \(t-\theta_k/\delta\) become \(s-\theta_k\). Define

\[
 \begin{aligned}
 \Psi_N(\delta;X,z)
 &:=-D_*\bigl(r_NX+\delta z\bigr)^{\odot2}
    -\frac{\delta}{3}\bigl(r_NX+\delta z\bigr)^{\odot3},\\
 \mathcal R_{v,N}
 &:=A_{v,N}z+r_NY-\delta^2W+\Psi_N(\delta;X,z)\\
 &\quad+\delta K\,\mathcal L_{N,\eta,\mathcal R}
   [r_NX+\delta z].
 \end{aligned}
 \tag{3.2}
\]

The last line uses the present and delayed values of the displayed history.
Direct substitution into the physical RFDE gives, without a remainder,

\[
 \begin{aligned}
 X'&=\ell_N^\top\mathcal R_{v,N},&
 Y'&=-X+\delta\nu,\\
 \delta z'&=P_\perp\mathcal R_{v,N},&
 \delta W'&=z-D_wW.
 \end{aligned}
 \tag{3.3}
\]

The scale \(\delta^4W\) is forced by the last equation: it balances the
order-\(\delta^4\) transverse slow forcing with \(-D_wW\). An
order-\(\delta^2\) transverse recovery variable would insert \(-W\) into
the leading voltage algebraic equation and would not restrict to the exact
two-module chart.

## 4. Exact stable shift and divisibility

The identities

\[
 P_\perp D_*r_N^{\odot2}=\alpha q_N,\qquad
 A_{v,N}q_N=-2q_N
 \tag{4.1}
\]

give the shifts

\[
 U=z+\frac\alpha2q_NX^2,\qquad
 V=W+\frac\alpha{2D_w}q_NX^2.
 \tag{4.2}
\]

Set \(u=(X,Y)\) and \(h=(U,V)\). On \(\mathcal E_N\), define

\[
 \boxed{\mathcal A_N\binom UV
 =\binom{A_{v,N}U}{U-D_wV}.}
 \tag{4.3}
\]

Let \(f_X=\ell_N^\top\mathcal R_{v,N}\), after replacing

\[
 z=U-\frac\alpha2q_NX^2,\qquad
 W=V-\frac\alpha{2D_w}q_NX^2
 \tag{4.4}
\]

at the present and delayed states. The special-flow nonlinearities are

\[
 \begin{aligned}
 F_{N,X}
 &=\frac{f_X-(Y-\alpha X^2)}\delta,
 &F_{N,Y}&=\nu,\\
 G_{N,U}
 &=\frac{P_\perp\mathcal R_{v,N}
       +\delta\alpha q_NXf_X-A_{v,N}U}{\delta},\\
 G_{N,V}
 &=\frac{z-D_wW+(\delta\alpha/D_w)q_NXf_X-(U-D_wV)}
         {\delta}
 =\frac\alpha{D_w}q_NXf_X.
 \end{aligned}
 \tag{4.5}
\]

### Lemma 4.1 — exact model fit

For every \(n_1,n_2\geq1\), the three numerators divided by \(\delta\) in
(4.5) vanish identically at \(\delta=0\). Their quotients extend as exact
polynomials to both signs of \(\delta\). Consequently the transformed node
RFDE is exactly

\[
 \boxed{
 \begin{aligned}
 u'&=q_0(u)+\delta F_N
  \bigl(u,h,\mathscr E_N(u,h)_s;
        \delta,\nu,\eta,\mathcal R\bigr),\\
 \delta h'&=\mathcal A_Nh+\delta G_N
  \bigl(u,h,\mathscr E_N(u,h)_s;
        \delta,\nu,\eta,\mathcal R\bigr),\\
 q_0(X,Y)&=(Y-\alpha X^2,-X)^\top.
 \end{aligned}}
 \tag{4.6}
\]

This is an equality of RFDEs on \([-\theta_1,0]\), not a formal truncation.

**Proof.** Equation (1.5) and balance of the layers give (3.2)–(3.3) after
division by the exact powers on the left-hand side. At \(\delta=0\),
(4.1) and (4.4) give

\[
 \ell_N^\top\mathcal R_{v,N}=Y-\alpha X^2,\qquad
 P_\perp\mathcal R_{v,N}=A_{v,N}U.
 \tag{4.7}
\]

The recovery shift cancels
\(z-D_wW-(U-D_wV)\) identically. Hence all three differences in (4.5) have
zero constant coefficient in \(\delta\). Every term in (3.2) is polynomial
in \(\delta\), so polynomial division proves exact divisibility and supplies
the extensions at zero. Differentiating (4.2) gives the two terms
proportional to \(Xf_X\), and (4.6) follows. \(\square\)

The executable proof performs polynomial division and checks separately
that every division remainder and both reconstruction residuals are zero.

## 5. Uniform stable semigroup

Put

\[
 \varrho=\min\{2,D_v,D_w\},\qquad
 C_P=\|P_m\|_\infty+\|P_w\|_\infty\leq\frac72.
 \tag{5.1}
\]

The first semigroup component is

\[
 e^{A_{v,N}t}U_0
 =(e^{-2t}P_m+e^{-D_vt}P_w)U_0,
 \tag{5.2}
\]

and the second follows by variation of constants. Therefore

\[
 \boxed{
 \|e^{\mathcal A_Nt}\|_{\mathcal E_N\to\mathcal E_N}
 \leq C_P(1+t)e^{-\varrho t}
 \leq M_\infty e^{-\varrho t/2},\quad
 M_\infty=\frac72\left(1+\frac{2}{e\varrho}\right).}
 \tag{5.3}
\]

This is the same dimension-free maximum-norm bound as for the singular
current-state block, although the shifted generator is lower triangular.
No full positive-\(\delta\) RFDE spectral dichotomy is used.

## 6. Uniform transformed jets

Fix compact intervals for \(\nu,\eta\), a bounded residual ball (2.3), and
fixed positive \(D_v,D_w\). On

\[
 |X|\leq L_X,\quad |Y|\leq L_Y,\quad
 \|U\|_\infty,\|V\|_\infty\leq L_h,
 \tag{6.1}
\]

with the same delayed-slot bounds and \(|\delta|\leq\delta_*\), all
Fréchet derivatives through order twelve of \(F_N,G_N\) are bounded by one
polynomial in

\[
 L_X,L_Y,L_h,\delta_*,|K|,R_*,
 D_v,D_w,D_w^{-1},
 \tag{6.2}
\]

independently of \(N\). The same holds after one \(\nu\) derivative and two
structural-parameter derivatives. The data are affine in \(\nu\) and in
each layer perturbation, so their second pure data derivatives in those
parameters vanish.

Indeed,

\[
 \|r_N\|_\infty=\|q_N\|_\infty=2,\quad
 \|\ell_N^\top\|=\frac34,\quad
 \|P_\perp\|\leq\frac52,\quad
 \|P_m\|+\|P_w\|\leq\frac72,
 \tag{6.3}
\]

Hadamard multilinear norms equal one, and layer norms are controlled by
operator TV. Formulas (3.2) and (4.5) have state degree at most seven after
the shift. Thus state derivatives above degree seven vanish, with no hidden
coordinate sum. In the fold coordinates

\[
 \chi=-2\alpha X,\qquad
 d=Y-\alpha X^2+\frac1{2\alpha},
 \tag{6.4}
\]

the critical correction becomes

\[
 \widetilde F_N
 =\binom{-2\alpha F_{N,X}}
 {F_{N,Y}-2\alpha XF_{N,X}}.
 \tag{6.5}
\]

This adds one polynomial factor in \(X\), preserving the uniform conclusion.

## 7. Dimension-uniform bounded preparation

Choose \(\tau\in C^\infty(\mathbb R)\) equal to the identity on \([-1,1]\)
and constant outside \([-2,2]\), and put

\[
 \tau_L(a)=L\tau(a/L),\qquad
 \mathcal T_{N,L}(x)_i=\tau_L(x_i),\qquad L\geq1.
 \tag{7.1}
\]

Every Fréchet derivative is a diagonal pointwise product. Thus

\[
 \sup_N\|D^j\mathcal T_{N,L}\|
 \leq C_j\max\{1,L^{1-j}\}.
 \tag{7.2}
\]

For a stable slot use

\[
 \mathcal S_{N,L}(h)=P_\perp\mathcal T_{N,L}(h).
 \tag{7.3}
\]

This maps into \(E_N\), has uniform derivatives, and equals \(h\) for
\(h\in E_N\) with \(\|h\|_\infty\leq L\).

Fix the nested tubes of Section 4 in the abstract graph note. For
\(S=S_\delta\), choose

\[
 L_\chi(S)=S+B_*,\qquad L_d=\max\{1,d_*\},\qquad L_h=2h_*,
 \tag{7.4}
\]

enlarging their identity regions to contain the buffered depth-two hull

\[
 \mathfrak H^{[2]}(\mathcal U_D)
 =\{\phi_0^{-t}u:u\in\mathcal U_D,\ 0\leq t\leq2\theta_1\}
 \tag{7.5}
\]

and \(\|h\|\leq h_*\) in every current and delayed slot. Compose the exact
polynomials (4.5)–(6.5) slotwise with these scalar and projected
componentwise saturations. Prepare the singular field with (4.6a)–(4.6b) of
the abstract note. The result is globally \(C_b^{12}\), agrees with the
physical chart on an open neighborhood of the whole hull, and obeys

\[
 \sup_N\max_{a+b+i+e\leq12}
 \left(
 \|D_z^a\partial_\delta^b\partial_\nu^iD_{\mathcal R}^eF_{N,S}\|
 +\|D_z^a\partial_\delta^b\partial_\nu^iD_{\mathcal R}^eG_{N,S}\|
 \right)
 \leq P_{12}(S)
 \tag{7.6}
\]

for the derivative ranges in (4.6c) of the abstract theorem. The prepared
RFDE is globally Lipschitz apart from its bounded linear stable generator,
so method-of-steps theory gives its global semiflow on the fixed history
space.

## 8. Consequence and remaining gates

### Corollary 8.1 — lifted-network invariant complete-history graph

For every fixed logarithmic exponent and preparation above, there are
\(\delta_0,C>0\), independent of \(n_1,n_2\), such that the prepared lifted
network has the invariant history graph and mixed
\(\delta^3,\nu^1,\mathcal R^2\) jets of Corollary 4.1 in the abstract graph
note. On every retained segment whose full delay backtrack lies in (7.5),
the embedded histories solve the unprepared node RFDE exactly. The first two
graph coefficients are independent of the outer cutoff.

**Proof.** Lemma 4.1 supplies the exact special-flow form. Equations (5.3),
(2.5), and (7.6) supply the stable-semigroup, operator-TV, and transformed
data hypotheses. The prepared problem is well posed, and (6.3) gives the
uniform coordinate bounds. The abstract corollary applies. \(\square\)

This closes the **blow-up/model-fitting and invariant-history part of Gate
A** for the declared lifted family, including uniformly bounded balanced
operator-TV residuals.  The companion selected-root theorem now closes the
compatible canonical connection and the nonzero combined non-equitable
tangent through the exact quotient.  This note alone does not close the
later gates:

1. no uniform complete-history Lin inverse or simple gap root is proved for
   a general residual or a network without the exact quotient;
2. the pure within-module family of Proposition 6.1 has zero first response;
   no nonzero quadratic or higher coefficient is proved;
3. no local prepared history is identified with a physical outer maximal
   canard;
4. no spike onset, pulse safety boundary, frequency, or amplitude control
   theorem follows.

## 9. Reproduction

~~~sh
PYTHONPATH=build/testdeps:src python3 -m pytest -q \
  tests/test_lifted_network_blowup.py
~~~

The tests certify exact scaling, zero polynomial-division remainders,
full-state reconstruction, stable projection, the fixed-atom TV norm, the
maximum-norm semigroup estimate, the known projection-invisible module
channel, and exact restriction to the audited two-module shifted chart.
