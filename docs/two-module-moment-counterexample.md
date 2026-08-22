# Two-module delay moment: closure lemma and range-forcing counterexample

Status: **finite-dimensional identities proved exactly; the RFDE threshold
expansion and uniform remainder remain targets.** This note separates the
scalar moment that is visible to the critical projection from a transverse
delay functional that the projection can miss.

## 1. Exact layerwise closure criterion

Let \(r,\ell\in\mathbb R^2\) satisfy \(\ell^\top r=1\), and set

\[
 P=r\ell^\top,
 \qquad P_\perp=I-P.
 \tag{1}
\]

For an operator-valued delay measure \(\mathbb B(d\theta)\),

\[
 \boxed{
 P_\perp\mathbb B(d\theta)r=0
 \quad\Longleftrightarrow\quad
 \mathbb B(d\theta)r=r\rho_c(d\theta),
 }
 \tag{2}
\]

where

\[
 \rho_c(d\theta)=\ell^\top\mathbb B(d\theta)r.
 \tag{3}
\]

If

\[
 \mathbb B(d\theta)=\sum_k C_k\delta_{\theta_k}(d\theta)
 \tag{4}
\]

has distinct delay atoms, (2) is equivalent to

\[
 C_kr=\beta_kr
 \quad\text{for every delay layer }k.
 \tag{5}
\]

Thus closure is a measure identity, not merely an eigenvector condition for
the total matrix \(B=\sum_kC_k\).

## 2. A concrete nondegenerate FHN fold

Use the fast two-module core

\[
\begin{aligned}
 F_1&=v_1-\frac{v_1^3}{3}-w_1+\frac12(v_2-v_1),\\
 F_2&=v_2-\frac{v_2^3}{3}-w_2+2(v_1-v_2),
\end{aligned}
\tag{6}
\]

and slow equations

\[
 \dot w_1=\varepsilon(v_1-\sigma-\mu),
 \qquad
 \dot w_2=\varepsilon(v_2-2\mu),
 \qquad
 \sigma=\sqrt{3/2}.
 \tag{7}
\]

At \(\mu=0\),

\[
 v_*=(\sigma,0)^\top,
 \qquad w_*=(0,2\sigma)^\top.
 \tag{8}
\]

The fast Jacobian is

\[
 A_0=
 \begin{pmatrix}-1&1/2\\2&-1\end{pmatrix}
 =-2P_\perp,
 \tag{9}
\]

with

\[
 r=(1,2)^\top,
 \qquad
 \ell=(1/2,1/4)^\top.
 \tag{10}
\]

The fold is nondegenerate because

\[
 \ell^\top D_v^2F(v_*,w_*)[r,r]
 =-\sigma\ne0.
 \tag{11}
\]

Along \(v=v_*+rX\), the slow field is exactly \(r(X-\mu)\), so \(\mu\)
is a scalar unfolding of the critical direction.

## 3. Source-history feedback architecture

For this exact counterexample, the weak feedback is

\[
 \varepsilon K\left[
 Bv(t)-\int\mathbb B_\eta(d\theta)
 v(t-\theta/\sqrt\varepsilon)
 \right].
 \tag{12}
\]

It compares each weighted source with its delayed history. This is distinct
from receiver-self diffusion \(v_a(t)-v_b(t-\tau)\); the distinction is
explicit and is revisited in Section 6. Constant histories see zero feedback
whenever \(\int\mathbb B_\eta=B\).

Take two distinct delays \(\theta_0\ne\theta_1\) and

\[
 C_0=
 \begin{pmatrix}1/6&1/12\\1/6&1/4\end{pmatrix},
 \qquad
 C_1=
 \begin{pmatrix}1/3&1/6\\1/2&5/12\end{pmatrix},
 \tag{13}
\]

\[
 T=\begin{pmatrix}1&0\\-2&0\end{pmatrix},
 \qquad
 C_0^\eta=C_0+\eta T,
 \qquad
 C_1^\eta=C_1-\eta T,
 \tag{14}
\]

\[
 \mathbb B_\eta(d\theta)
 =C_0^\eta\delta_{\theta_0}(d\theta)
 +C_1^\eta\delta_{\theta_1}(d\theta).
 \tag{15}
\]

For \(|\eta|<1/20\), both layer matrices are positive. Their total is the
same matrix for every \(\eta\):

\[
 C_0^\eta+C_1^\eta
 =B=
 \begin{pmatrix}1/2&1/4\\2/3&2/3\end{pmatrix},
 \qquad Br=r.
 \tag{16}
\]

## 4. Same total topology and projected moment, different range forcing

At \(\eta=0\), each delay layer preserves the critical mode:

\[
 C_0r=\frac13r,
 \qquad
 C_1r=\frac23r.
 \tag{17}
\]

Hence the critical delay measure and first moment are

\[
 \rho_c=\frac13\delta_{\theta_0}
 +\frac23\delta_{\theta_1},
 \qquad
 M_1^{(2)}=\frac{\theta_0}{3}+\frac{2\theta_1}{3}.
 \tag{18}
\]

Let \(q=Tr=(1,-2)^\top\); then \(\ell^\top q=0\). For every \(\eta\),

\[
 C_0^\eta r=\frac13r+\eta q,
 \qquad
 C_1^\eta r=\frac23r-\eta q.
 \tag{19}
\]

The critical projection is therefore unchanged:

\[
 \ell^\top\mathbb B_\eta(d\theta)r
 =\frac13\delta_{\theta_0}
 +\frac23\delta_{\theta_1},
 \tag{20}
\]

but the range forcing is not:

\[
 P_\perp\mathbb B_\eta(d\theta)r
 =\eta q(\delta_{\theta_0}-\delta_{\theta_1}).
 \tag{21}
\]

Equivalently,

\[
 \int\theta\mathbb B_\eta(d\theta)r
 =M_1^{(2)}r
 +\eta(\theta_0-\theta_1)q.
 \tag{22}
\]

Thus two systems can have the same total topology \(B\), the same projected
delay measure, and the same \(M_1^{(2)}\), while presenting different forcing
to the transverse RFDE range equation.

The leading fast transverse response is nonzero:

\[
 A_\perp^{-1}q=-\frac12q,
 \tag{23}
\]

and the FHN nonlinearity sends it back into critical solvability:

\[
 \ell^\top D_v^2F
 [r,A_\perp^{-1}q]
 =\frac\sigma2\ne0.
 \tag{24}
\]

Thus there is a nonzero local channel by which transverse forcing can return
to critical solvability. This does not by itself exclude cancellation in the
complete RFDE dynamic-adjoint integral or its boundary terms. It does prove
that such cancellation cannot be inferred from the projected moment and must
be established, if present, by the frozen Lin calculation.

## 5. Corrected Proposition B target

Subject to the actual Lyapunov--Schmidt scaling, a candidate bookkeeping form
is

\[
 \boxed{
 \mu_c
 =\mu_{c,0}+c_0\varepsilon
 +K\varepsilon^{3/2}
 \left(
 C_\parallel M_1^{(2)}
 +\mathcal J_{\perp,\delta}[\mathbb B]
 \right)
 +O(\varepsilon^2).
 }
 \tag{25}
\]

Here \(\mathcal J_{\perp,\delta}\) is the explicit composition

\[
 \text{delay translation}
 \longrightarrow
 \text{transverse RFDE inverse}
 \longrightarrow
 \text{dynamic critical-adjoint solvability}.
 \tag{26}
\]

The factor \(\varepsilon^{3/2}\) represents the intended same-order regime and
requires \(\mathcal J_{\perp,\delta}=O(1)\). If the transverse inverse makes
this functional grow as \(\delta\to0\), the asymptotic ordering must be changed.
For the source-history architecture (12), condition (2) kills the leading
delayed-source transverse forcing provided the current, instantaneous,
nonlinear, and endpoint/Lin operators preserve the same mode splitting.
Outside that complete closure class, setting
\(\mathcal J_{\perp,\delta}\) to zero is an assumption to prove, not a moment
closure.

## 6. Perron no-go for nonnegative receiver-self diffusion

The source-history architecture in (12) is not silently substituted for the
standard receiver-self form. In that standard form, let

\[
 D=\operatorname{diag}(B\mathbf1),
 \qquad
 \text{feedback}=Dv(t)-\sum_kC_kv(t-\theta_k),
 \qquad B=\sum_kC_k,
 \tag{27}
\]

with \(B\ge0\) irreducible and a positive critical mode \(r>0\). Suppose the
current term and every delay layer preserve the critical line:

\[
 Dr\in\operatorname{span}(r),
 \qquad
 C_kr\in\operatorname{span}(r).
 \tag{28}
\]

Since \(D\) is diagonal and \(r>0\), \(Dr=cr\) forces every row sum of
\(B\) to equal \(c\), so \(B\mathbf1=c\mathbf1\). The layer assumptions give
\(Br=\beta r\) for some \(\beta\). Because \(B\geq0\) is irreducible, both
positive eigenvectors belong to its Perron eigenvalue. Hence \(\beta=c\), and
Perron--Frobenius uniqueness implies

\[
 r\parallel\mathbf1.
 \tag{29}
\]

Finally, \(C_k\mathbf1=\beta_k\mathbf1\) says every distinct-delay layer has
the same receiving-row mass. This is precisely common-row-measure closure.

Therefore a genuinely modular positive-mode result for nonnegative
receiver-self diffusion must do at least one of the following:

- retain \(\mathcal J_{\perp,\delta}\);
- prove from the complete dynamic adjoint that the transverse term cancels or
  enters only at higher order;
- permit signed excitatory/inhibitory weights;
- change the feedback architecture, as in (12).

Topology and layer closure alone therefore cannot justify a general law that
only replaces \(\Theta\) by the scalar \(M_1^{(2)}\).

## 7. Proof status

The following are exact and executable in
`src/canard_control/two_module_moment.py`:

- the FHN equilibrium, critical modes, and fold nondegeneracy;
- positivity on the declared \(\eta\) interval;
- fixed total gain and fixed projected delay measure;
- the transverse first-moment forcing;
- the nonzero nonlinear return coefficient.

Equation (25) is still a theorem target. Its dynamic RFDE adjoint,
\(\mathcal J_{\perp,\delta}\), its singular-limit scaling, and uniform
\(O(\varepsilon^2)\) remainder remain to be
derived in the augmented Lin formulation.
