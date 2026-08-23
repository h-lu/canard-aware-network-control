# A synchrony-quotient-free selected canard root from heterogeneous fold curvature

Status: **the preparation-indexed canonical local history root and its
dimension-uniform topology coefficient are proved below.**  The theorem
applies to arbitrary finite directed Markov networks with a common Dobrushin
gap; it does not assume an equitable partition or a two-module synchrony
quotient.  A
normalized family with no nontrivial synchrony quotient has the same nonzero
coefficient for every \(N\ge2\).

The finite-\(\delta\) root is indexed by the declared canonical preparation.
The theorem does not identify that root with an unspecified outer RFDE
Fenichel selection.  This distinction is essential: without a
parameter-coherent outer selection, endpoint derivatives can be changed
without changing the local invariant graph.

The exact matrix identities are implemented in
[heterogeneous_curvature_root.py](../src/canard_control/heterogeneous_curvature_root.py)
and checked in
[test_heterogeneous_curvature_root.py](../tests/test_heterogeneous_curvature_root.py).
Those checks reproduce the algebra; the history graph and the selected
traces are analytic objects in Theorem 4.1.

## 1. Network class

For each \(N\ge2\), let \(P_N\) be a nonnegative row-stochastic matrix and let
\(\pi_N\) be its strictly positive stationary probability column:

\[
 P_N\mathbf1=\mathbf1,
 \qquad \pi_N^\top P_N=\pi_N^\top,
 \qquad \pi_N^\top\mathbf1=1.
 \tag{1.1}
\]

Assume that the Dobrushin coefficients satisfy

\[
 \tau(P_N)\le1-\gamma
 \tag{1.2}
\]

for one \(\gamma>0\), independently of \(N\).  Put

\[
 P_{c,N}=\mathbf1\pi_N^\top,
 \qquad P_{\perp,N}=I-P_{c,N},
 \qquad E_N=\ker\pi_N^\top,
 \tag{1.3}
\]

and use

\[
 \|x\|_{N}=|\pi_N^\top x|+\operatorname{osc}(x),
 \qquad
 \operatorname{osc}(x)=\max_i x_i-\min_i x_i.
 \tag{1.4}
\]

For a fixed \(D>0\), the transverse generator

\[
 A_N=D(P_N-I)|_{E_N}
 \tag{1.5}
\]

satisfies

\[
 \|e^{A_Nt}\|_{E_N\to E_N}\le e^{-D\gamma t},
 \qquad
 \|A_N^{-1}\|_{E_N\to E_N}\le(D\gamma)^{-1}.
 \tag{1.6}
\]

The first estimate follows from the Poisson expansion and Dobrushin
contraction; the second follows by integrating the semigroup.  Neither
constant depends on \(N\).

Let \(c_N=(c_{1,N},\ldots,c_{N,N})^\top\) be the local fold-curvature
vector.  We impose the common normalization

\[
 0<c_-\le c_{i,N}\le c_+,
 \qquad \pi_N^\top c_N=\alpha>0,
 \tag{1.7}
\]

where \(c_-,c_+,\alpha\) are independent of \(N\).  Let \(\beta>0\) be a
fixed cubic coefficient.  At finitely many fixed chart delays
\(0\le\theta_0<\cdots<\theta_m\le\Theta_*\), take

\[
 B_{k,N}(\zeta)=B_{k,N}+\zeta R_{k,N},
 \qquad
 C_N(\zeta)=\sum_{k=0}^mB_{k,N}(\zeta).
 \tag{1.8}
\]

The base-layer sums and structural directions have uniformly bounded
operator total variation in (1.4), made quantitative in (3.1a).  The
support is fixed.  Most
importantly, the structural direction obeys the atomwise full-row identity

\[
 \boxed{\pi_N^\top R_{k,N}=0\quad(0\le k\le m).}
 \tag{1.9}
\]

This is stronger than
\(\pi_N^\top R_{k,N}\mathbf1=0\).  It removes the structural direction
from the critical delay equation for every vector history, including the
stable shift and all flow-history corrections.  At the same time,
\(R_{k,N}\mathbf1\) may be nonzero and may force \(E_N\).

For \(\varepsilon=\delta^2\), consider the shared-resource RFDE

\[
\begin{aligned}
 \dot v(t)={}&\frac23\mathbf1-w(t)\mathbf1
 -c_N\circ(v(t)-\mathbf1)^{\circ2}
 -\frac\beta3(v(t)-\mathbf1)^{\circ3}
 +D(P_N-I)v(t)\\
 &+\varepsilon K\left[
 C_N(\zeta)v(t)-\sum_{k=0}^mB_{k,N}(\zeta)
 v\left(t-\frac{\theta_k}{\delta}\right)
 \right],\\
 \dot w(t)={}&\varepsilon(\pi_N^\top v(t)-a).
\end{aligned}
\tag{1.10}
\]

Here \(K\ne0\), and powers and products are componentwise.  The balanced
current term makes the delay feedback vanish on a constant history.  The
fold is

\[
 (v,w,a)=(\mathbf1,2/3,1).
 \tag{1.11}
\]

Equation (1.10) is locally well posed on the continuous-history phase space
for every finite \(N\).  Positivity of the delay layers is not used in the
analysis, but it holds in the explicit family of Section 6 on a uniform
parameter interval.

## 2. The exact fold chart and the necessary stable translation

Set

\[
 s=\delta t,
 \qquad a=1+\delta^2\nu,
 \qquad w=\frac23-\delta^2Y.
 \tag{2.1}
\]

Write \(\mathcal A_N=D(P_N-I)\) on the ambient node space and define

\[
 g_N=A_N^{-1}P_{\perp,N}c_N\in E_N,
 \qquad z_{0,N}(X)=g_NX^2.
 \tag{2.2}
\]

The voltage chart is

\[
 v=\mathbf1+\delta\mathbf1X
       +\delta^2\bigl(z_{0,N}(X)+h\bigr),
 \qquad h\in E_N.
 \tag{2.3}
\]

The shift \(z_{0,N}\) is forced by the heterogeneous curvature.  Indeed,

\[
 \mathcal A_Nz_{0,N}(X)-P_{\perp,N}c_NX^2=0.
 \tag{2.4}
\]

Thus \(h=0\), rather than \(z=0\), is the singular stable graph.  The
uniform inverse estimate in (1.6) and (1.7) give uniform bounds for \(g_N\)
and all derivatives of \(z_{0,N}\) on the logarithmic fold tube.

For a complete chart history \(\phi\), define

\[
 \mathcal L_{N,\zeta}[\phi](s)
 =C_N(\zeta)\phi(s)
  -\sum_{k=0}^mB_{k,N}(\zeta)\phi(s-\theta_k).
 \tag{2.5}
\]

Put \(Z=z_{0,N}(X)+h\), and let \(\mathcal Q_N\) denote the right-hand side
of the following \(X\)-equation.  Direct substitution into (1.10), with no
Taylor remainder, gives

\[
\begin{aligned}
 X'=\mathcal Q_N={}&Y-\alpha X^2\\
 &+\delta\left[
 -2X\pi_N^\top(c_N\circ Z)-\frac\beta3X^3
 +K\pi_N^\top\mathcal L_{N,\zeta}[\mathbf1X]
 \right]\\
 &+\delta^2\left[
 -\pi_N^\top(c_N\circ Z^{\circ2})
 +K\pi_N^\top\mathcal L_{N,\zeta}[Z]
 \right]\\
 &-\delta^3\beta X\pi_N^\top Z^{\circ2}
 -\frac{\delta^4\beta}{3}\pi_N^\top Z^{\circ3},\\
 Y'={}&-X+\delta\nu,\\
 \delta h'={}&A_Nh\\
 &+\delta\left\{
 P_{\perp,N}\left[-2c_N\circ XZ
       +K\mathcal L_{N,\zeta}[\mathbf1X]\right]
       -2g_NX\mathcal Q_N
 \right\}\\
 &+\delta^2P_{\perp,N}\left[
 -c_N\circ Z^{\circ2}-\beta X^2Z
 +K\mathcal L_{N,\zeta}[Z]
 \right]\\
 &-\delta^3\beta X P_{\perp,N}Z^{\circ2}
 -\frac{\delta^4\beta}{3}P_{\perp,N}Z^{\circ3}.
\end{aligned}
\tag{2.6}
\]

The term \(-2g_NX\mathcal Q_N\) is the derivative of the translation
\(z_{0,N}(X)\); omitting it gives the wrong stable graph.  Formula (2.6)
also shows that the fixed chart delays have no hidden \(N\)-dependent
rescaling.

At \(\delta=0\), the reduced field is the same for every \(N\):

\[
 q_0(X,Y)=(Y-\alpha X^2,-X)^\top.
 \tag{2.7}
\]

Its singular canard and normalized decaying adjoint are

\[
 \gamma_0(s)=\left(-\frac{s}{2\alpha},
              \frac{s^2-2}{4\alpha}\right),
 \qquad
 \psi(s)=e^{-s^2/2}(s,1)^\top.
 \tag{2.8}
\]

## 3. Uniform history graph and the topology-return jet

The norm (1.4) controls every coordinate and componentwise multiplication:

\[
 \|x_1\circ\cdots\circ x_j\|_N
 \le3\prod_{\ell=1}^j\|x_\ell\|_N.
 \tag{3.1}
\]

The following lemma records the complete model fit rather than appealing to
finite-dimensional norm equivalence.

### Lemma 3.1 (dimension-uniform model fitting)

Fix the number of atoms, their locations, the constants in
(1.2), (1.7), and a bound

\[
 \sup_N\sum_{k=0}^m
 \left(\|B_{k,N}\|_{\mathcal L(\mathbb R^N,\|\cdot\|_N)}
       +\|R_{k,N}\|_{\mathcal L(\mathbb R^N,\|\cdot\|_N)}\right)
 \le B_*.
 \tag{3.1a}
\]

For every sufficiently small target \(\delta>0\), freeze
\(S=S_\delta\) as in (4.1).  System (2.6) then admits prepared transformed
data in the dimension-uniform special-flow theorem with the following
properties.

1. The reduced-stable state and delay-output spaces are
   \[
    \mathcal X_N=\mathbb R^2\times E_N,\qquad
    \|(u,h)\|_{\mathcal X_N}=\max\{|u|,\|h\|_N\},
   \]
   \[
    \mathcal Y_N=\mathcal X_N^{m+2},\qquad
    \|(y_{-1},y_0,\ldots,y_m)\|_{\mathcal Y_N}
    =\max_{-1\le k\le m}\|y_k\|_{\mathcal X_N}.
    \tag{3.1b}
   \]
   If \(J_k:\mathcal X_N\to\mathcal Y_N\) inserts a vector in the
   \(k\)-th slot, the fixed operator-valued measure
   \[
    \mathbf M_N(d\vartheta)
    =J_{-1}\delta_0(d\vartheta)
      +\sum_{k=0}^mJ_k\delta_{-\theta_k}(d\vartheta)
    \tag{3.1c}
   \]
   realizes the complete evaluation tuple
   \[
    \mathscr E_N\phi
    =\bigl(\phi(0),\phi(-\theta_0),\ldots,\phi(-\theta_m)\bigr),
    \qquad
    \|\mathbf M_N\|_{\mathrm{TV}}\le m+2.
    \tag{3.1d}
   \]
2. The stable generator has the semigroup bound (1.6).  The critical and
   transverse projectors and the collective injection obey
   \[
    \|P_{c,N}\|\le1,\qquad
    \|P_{\perp,N}\|\le1,\qquad
    \|x\|_\infty\le\|x\|_N,\qquad
    \|\mathbf1 X\|_N=|X|.
    \tag{3.1e}
   \]
3. There is one polynomial \(P_{12}\), independent of \(N\), such that the
   prepared transformed nonlinearities \(F_{N,S},G_{N,S}\) satisfy
   \[
   \sup_{\substack{N,\ |\rho|\le\delta\\
                   (\nu,\zeta)\text{ in the fixed parameter box}}}
   \max_{\substack{a+b+i+j\le12\\b\le3,\ i\le1,\ j\le2}}
   \left(
   \|D_z^a\partial_\rho^b\partial_\nu^i\partial_\zeta^jF_{N,S}\|_\infty
   +\|D_z^a\partial_\rho^b\partial_\nu^i\partial_\zeta^jG_{N,S}\|_\infty
   \right)
   \le P_{12}(S).
   \tag{3.1f}
   \]
4. At \(\rho=\delta\), the preparation equals (2.6) on an open
   neighborhood of the continuous depth-two \(q_0\)-flow hull of the
   retained tube, enlarged by the fixed buffer and by one common stable
   ball \(\|h\|_N\le h_*\).  This contains every retained delay backtrack
   and every \(o(1)\) base-flow shift used in the first two stable
   convolution jets.  The far convolution tail remains part of the
   preparation and is controlled by semigroup decay; it is not called an
   uncut physical orbit segment.

All constants in these statements are independent of \(N\).

#### Proof

For \(P_{c,N}x=\mathbf1\pi_N^\top x\),
\(\|P_{c,N}x\|_N=|\pi_N^\top x|\).  Also
\(\pi_N^\top P_{\perp,N}x=0\) and subtraction of a constant does not change
oscillation, so
\(\|P_{\perp,N}x\|_N=\operatorname{osc}(x)\).  This proves the first two
bounds in (3.1e).  Since \(\pi_N^\top x\) is a convex combination of the
coordinates,
\[
 |x_i|\le|\pi_N^\top x|+\operatorname{osc}(x),
\]
which proves the remaining coordinate bounds.  Dobrushin contraction gives
(1.6), including the uniform inverse bound.

The injections \(J_k\) have norm one.  Summing the variations of the fixed
atoms proves (3.1d), even when a delayed atom coincides with the current
atom.  The measure \(\mathbf M_N\) is independent of
\((\rho,\nu,\zeta)\); hence all of its parameter derivatives vanish and the
balanced-anchor condition of the abstract theorem is automatic.  The
matrices \(B_{k,N}+\zeta R_{k,N}\) occur in \(F_{N,S},G_{N,S}\), where
(3.1a) bounds both the current sum and all delayed sums.  This placement
also makes the fixed-support \(C_\nu^1C_\zeta^2\) assertion literal rather
than a differentiability claim about moving point masses.

For componentwise products, coordinate control followed by
\(\|y\|_N\le3\|y\|_\infty\) proves (3.1); multiplication by \(c_N\) costs
at most the common factor \(c_+\).  Thus every Nemytskii derivative of the
quadratic and cubic local terms has a dimension-independent multilinear
norm.  The translation satisfies
\[
 \|g_N\|_N
 \le(D\gamma)^{-1}\|P_{\perp,N}c_N\|_N,
\]
so \(z_{0,N}(X)=g_NX^2\) and its derivatives have the same uniform
property.

Replace every displayed \(\delta\) in the transformed nonlinear terms by
the dummy amplitude \(\rho\), after substituting the explicit expression
for \(\mathcal Q_N\) in the stable equation.  The resulting expressions are
finite polynomials in \(\rho,\nu,\zeta\), the current state, and the
evaluation tuple (3.1d).  Prepare \(q_0\) by the common compact planar
cutoff in the \((\chi,d)\) fold coordinates, and use that same cutoff to
prepare every polynomial \((X,Y)\)-coefficient in every current and history
slot of \(F_{N,S},G_{N,S}\).
Prepare each current and history \(h_i\)-slot by one fixed scalar
\(C^\infty\) saturation, equal to the identity on \([-h_*,h_*]\), and
apply \(P_{\perp,N}\) to every prepared stable output.  The Nemytskii
estimate above bounds every derivative of these componentwise saturations
without a factor depending on \(N\).

On the support of the planar cutoff, \(X,Y,z_{0,N}(X)\) and their requested
derivatives are bounded by a polynomial in \(S\).  Repeated product and
chain rules, using the preceding uniform operator bounds, therefore give
(3.1f).  Choose the planar cutoff to equal one on the continuous
depth-two hull plus the fixed buffer and the finite stable-convolution
shifts used by the coefficient jets, and choose the scalar saturations to
equal the identity on the common stable ball.  Semigroup decay controls the
remaining convolution tail without identifying it as physical.  This
proves item 4.  Local well-posedness of the unprepared finite-\(N\) RFDE
follows from the bounded linear evaluations and the locally Lipschitz
polynomial vector field.
\(\square\)

Consequently the dimension-uniform special-flow graph theorem applies to
(2.6).  For a cutoff frozen at the target \(\delta\), it gives on the
retained logarithmic tube an exact invariant complete-history graph and a
reduced field

\[
 Q_{N,\delta,\nu,\zeta}
 =q_0+\delta q_{1,N}+\delta^2q_{2,N}
  +\delta^3R_{3,N},
 \tag{3.2}
\]

with uniform \(C_\nu^1C_\zeta^2\) jets and the Gaussian-compatible
pointwise remainder needed by the one-sided trace theorem.  The graph
history is an injective exact embedding wherever the full backtrack lies
in the uncut hull.

We now calculate the only first structural return.  Let

\[
 \dot M_{1,N}=\sum_{k=0}^m\theta_kR_{k,N},
 \qquad
 h_{*,N}=\frac{K}{2\alpha}
 A_N^{-1}P_{\perp,N}\dot M_{1,N}\mathbf1,
 \tag{3.3}
\]

and set

\[
 r_N=\pi_N^\top\operatorname{diag}(c_N)h_{*,N}.
 \tag{3.4}
\]

### Lemma 3.2 (heterogeneous Hessian return)

Along \(\gamma_0\), the first stable structural jet is constant and the
first two reduced structural jets are

\[
 D_\zeta h_{1,N}(\gamma_0(s))=h_{*,N},
 \qquad D_\zeta q_{1,N}=0,
 \tag{3.5}
\]

\[
 \boxed{
 D_\zeta q_{2,N}(\gamma_0(s),\nu,0)
 =\left(\frac{r_N}{\alpha}s,0\right)^\top.}
 \tag{3.6}
\]

#### Proof

On the singular canard,

\[
 X_0(s)-X_0(s-\theta_k)=-\frac{\theta_k}{2\alpha}.
 \tag{3.7}
\]

The order-\(\delta\) stable graph equation obtained from (2.6) is
\(A_Nh_{1,N}+G_{1,N}=0\).  Differentiating it in \(\zeta\), using
(1.9) and (3.7), gives

\[
 D_\zeta G_{1,N}
 =-\frac{K}{2\alpha}P_{\perp,N}
     \dot M_{1,N}\mathbf1,
\]

which proves the first identity in (3.5).

Identity (1.9) annihilates the structural critical delay term for every
history.  It therefore kills not only the direct collective history in
\(q_1\), but also the structural operator applied to \(z_{0,N}\) and to the
first flow-history correction in \(q_2\).  The translation \(z_{0,N}\) is
independent of \(\zeta\).  The only remaining derivative in the critical
equation is the mixed local Hessian term

\[
 -2X\pi_N^\top\operatorname{diag}(c_N)h_{*,N}=-2Xr_N.
\]

Substitution of \(X_0(s)=-s/(2\alpha)\) proves (3.6).  This argument keeps
the complete flow history; it does not replace it by an endpoint or a first
moment before (1.9) is applied. \(\square\)

The Melnikov pairing is now explicit:

\[
 M_{\zeta,N}
 =\int_{\mathbb R}\psi(s)^\top
 D_\zeta q_{2,N}(\gamma_0(s))\,ds
 =\sqrt{2\pi}\frac{r_N}{\alpha}.
 \tag{3.8}
\]

It is nonzero exactly when \(r_N\ne0\).  If \(c_N=\alpha\mathbf1\), then
\(r_N=\alpha\pi_N^\top h_{*,N}=0\), recovering the homogeneous-curvature
cancellation.  Thus heterogeneity, rather than projection neutrality by
itself, is the return mechanism.

## 4. Canonical selected-history root

Fix \(p>4\) sufficiently large and

\[
 S_\delta=\sqrt{2p\log(1/\delta)}.
 \tag{4.1}
\]

Also fix a **uniformly admissible preparation rule**
\(\mathcal P=(\mathcal P_N)_{N\ge2}\): common frozen graph-cutoff profiles,
a common planar joining cutoff, a degree-three normal-extension rule, a
common phase buffer, common invariant-tail levels, and componentwise stable
cutoffs with one set of derivative bounds.  Its \(N\)-th member inserts the
\(N\)-node physical field on the continuous depth-two uncut hull.  It is
independent of \(\nu,\zeta\).  All bounds below are uniform over preparation
rules with these common finite derivative bounds.  This formulation does
not identify different-dimensional phase spaces; it specifies the same
construction and the same constants on each of them.

Let \(z^a_{N,\mathcal P_N}\) and \(z^r_{N,\mathcal P_N}\) be the attracting and
repelling one-sided traces selected by the prepared invariant tails and the
phase \(X(0)=0\).  On their retained central pieces they lie on the exact
uncut RFDE history graph.  With

\[
 H_\alpha(X,Y)=\frac12e^{-2\alpha Y}
 \left(\alpha Y-\alpha^2X^2+\frac12\right),
 \tag{4.2}
\]

define the normalized central gap

\[
 D_{N,\mathcal P_N}(\delta,\nu,\zeta)
 =\frac{2}{\alpha e}
 \left[H_\alpha(z^a_{N,\mathcal P_N}(0))
             -H_\alpha(z^r_{N,\mathcal P_N}(0))\right].
 \tag{4.3}
\]

The normalization makes the leading gap equal to the \(\psi\)-pairing.
Near the singular crossing, \(D_{N,\mathcal P_N}=0\) is equivalent to equality
of the two planar current states.  Planar uniqueness and injectivity of the
history embedding then make it equality of the two retained complete RFDE
histories.

Define

\[
 \kappa_N=\frac\beta3
 +2\pi_N^\top\operatorname{diag}(c_N)g_N,
 \qquad
 \nu_{0,N}=-\frac{3\kappa_N}{8\alpha^3}.
 \tag{4.4}
\]

### Theorem 4.1 (dimension-uniform synchrony-quotient-free root response)

Consider any family satisfying (1.1)--(1.9), with the common bounds stated
there, and assume

\[
 \inf_N|r_N|>0.
 \tag{4.5}
\]

Choose a compact interval \(I_\nu\) whose interior contains all
\(\nu_{0,N}\) with one positive distance to its boundary; such an interval
exists by (1.6)--(1.7).  For every uniformly admissible preparation rule
\(\mathcal P=(\mathcal P_N)\), there are
\(\delta_0,\zeta_0,c_0,C>0\), independent of \(N\), such that for every

\[
 N\ge2,
 \qquad 0<\delta<\delta_0,
 \qquad |\zeta|<\zeta_0,
 \tag{4.6}
\]

the normalized gap \(D_{N,\mathcal P_N}/\delta\) has exactly one root

\[
 \nu_{c,N,\mathcal P_N}(\delta,\zeta)
 \quad\text{in}\quad
 |\nu-\nu_{0,N}|<c_0.
 \tag{4.7}
\]

The two retained complete histories agree at that root.  For
\(\mu=\delta^2\nu\),

\[
\boxed{
\begin{aligned}
 &\mu_{c,N,\mathcal P_N}(\delta,\zeta)
   -\mu_{c,N,\mathcal P_N}(\delta,0)\\
 &\qquad=\mathscr C_N\,\delta^3\zeta
 +O\left(\delta^4|\zeta|+\delta^3\zeta^2\right),\\
 &\mathscr C_N
 =-\frac{r_N}{\alpha}
 =-\frac{K}{2\alpha^2}
 \pi_N^\top\operatorname{diag}(c_N)
 A_N^{-1}P_{\perp,N}\dot M_{1,N}\mathbf1.
\end{aligned}}
\tag{4.8}
\]

The remainder constant is independent of \(N\) and of the preparation rule
in the declared bounded class.  The exact root may depend on
\(\mathcal P_N\); the coefficient in (4.8) does not.  In particular, (4.5)
makes the leading response uniformly nonzero, while (1.6)--(1.9) make every
constant in the graph, trace, endpoint, and implicit-root estimates uniform.

#### Proof

The leading reduced coefficient obtained from (2.6) is

\[
 q_{1,N,X}
 =-\kappa_NX^3
 +K\pi_N^\top\mathcal L_{N,0}[\mathbf1X],
 \qquad q_{1,N,Y}=\nu.
 \tag{4.9}
\]

On \(\gamma_0\), the balanced delay term is constant in \(s\), so its
pairing with \(s e^{-s^2/2}\) is zero.  Since

\[
 -\kappa_NX_0(s)^3
 =\frac{\kappa_N}{8\alpha^3}s^3,
 \qquad
 \psi(s)^\top\partial_\nu q_{1,N}
 =e^{-s^2/2},
 \tag{4.9a}
\]

the local cubic and unfolding contributions have signs
\[
 \int_{\mathbb R}\psi^\top q_{1,N}\,ds
 =\sqrt{2\pi}
 \left(\nu+\frac{3\kappa_N}{8\alpha^3}\right).
 \tag{4.9b}
\]

Here we used

\[
 \int_{\mathbb R}e^{-s^2/2}\,ds=\sqrt{2\pi},
 \qquad
 \int_{\mathbb R}s^4e^{-s^2/2}\,ds=3\sqrt{2\pi},
\]

so the leading zero is
\(\nu_{0,N}=-3\kappa_N/(8\alpha^3)\), with the sign displayed in
(4.4).  The one-sided Green trace calculation therefore gives, uniformly
in \(N\),

\[
 \frac{D_{N,\mathcal P_N}}\delta
 =\sqrt{2\pi}(\nu-\nu_{0,N})+O(\delta),
 \qquad
 \partial_\nu D_{N,\mathcal P_N}
 =\delta\sqrt{2\pi}+O(\delta^2).
 \tag{4.10}
\]

Lemma 3.2 and the same complete one-sided Green calculation give

\[
\begin{aligned}
 \partial_\zeta D_{N,\mathcal P_N}
 &=\delta^2\sqrt{2\pi}\frac{r_N}{\alpha}
   +O(\delta^3+\delta^2|\zeta|),\\
 \partial_{\zeta\zeta}D_{N,\mathcal P_N}&=O(\delta^2).
\end{aligned}
\tag{4.11}
\]

These are not formal whole-line integrals.  The attracting and repelling
Green operators contain the opposite one-sided normal projections; their
prepared endpoint values supply the two missing Gaussian tails.  The
moving-hit, phase, current-history evaluation, and endpoint derivatives are
therefore already present in (4.10)--(4.11).  Two admissible preparations
with common bounds change these equations only by

\[
 O\left(e^{-S_\delta^2/2+cS_\delta}
             \langle S_\delta\rangle^m\right)
 =O(\delta^{p-o(1)}),
 \tag{4.12}
\]

with the same \(C_\nu^1C_\zeta^2\) derivatives.  Choosing \(p\) before
\(\delta_0\) makes (4.12) smaller than the remainder in (4.11).

The first relation in (4.10), its simple \(\nu\)-slope, and the uniform
implicit-function theorem prove (4.7).  Along the root,

\[
 \partial_\zeta\nu_{c,N,\mathcal P_N}
 =-\delta\frac{r_N}{\alpha}
  +O(\delta^2+\delta|\zeta|).
 \tag{4.13}
\]

Integrating from \(0\) to \(\zeta\) and multiplying by \(\delta^2\) proves
(4.8).  Equality of retained complete histories follows from the gap
equivalence and the exact history embedding described above. \(\square\)

The nondegeneracy hypothesis (4.5) is used only to assert a uniformly
nonzero topology response.  Existence and simplicity of the \(\nu\)-root
follow from (4.10) without it.

## 5. Why endpoint and preparation terms do not invalidate (4.8)

There are three different claims, and only the first two are proved here.

1. **Exact canonical root.**  For each fixed \(\mathcal P_N\), (4.7) is an
   actual zero of a gap between two selected complete histories, not a
   formal series.
2. **Preparation-stable algebraic coefficient.**  Equation (4.12) shows that
   every preparation in the bounded admissible class has the coefficient
   (4.8), even though its exact finite-\(\delta\) root can differ by a
   term that is smaller than the displayed algebraic remainder after the
   fixed \(p\) has been chosen sufficiently large.
3. **Physical outer maximal canard.**  This would require a separately
   chosen attracting/repelling RFDE outer family to enter the same graph
   with parameter-coherent boundary residuals and
   \(C_\nu^1C_\zeta^2\) jets.  That Lyapunov--Perron comparison is not proved
   here.  No physical outer root is claimed.

This separation is why no endpoint term has been silently set to zero.  It
is either included in the canonical one-sided trace problem or retained as
the explicit missing hypothesis in item 3.

## 6. A normalized nonzero family for every \(N\)

The abstract coefficient in (4.8) could vanish.  The following exact family
shows that the nonzero case is nonempty, dimension-uniform, and does not
come from a hidden two-module lift.

Let \(\pi_N=N^{-1}\mathbf1\), \(P_N=P_{c,N}\), and define the centered grid

\[
 s_{i,N}=
 \frac{\sqrt3\,(2i-N-1)}{\sqrt{(N-1)(N+1)}},
 \qquad 1\le i\le N.
 \tag{6.1}
\]

Then

\[
 \pi_N^\top s_N=0,
 \qquad \pi_N^\top s_N^{\circ2}=1,
 \qquad \|s_N\|_\infty<\sqrt3,
 \tag{6.2}
\]

and all entries of \(s_N\) are distinct.  Fix

\[
 0<\sigma<1/\sqrt3,
 \qquad c_N=\mathbf1+\sigma s_N.
 \tag{6.3}
\]

Thus every curvature is positive and \(\alpha=1\).  For two delays
\(0\le\theta_0<\theta_1\), take

\[
 B_{0,N}=B_{1,N}=bP_{c,N},
 \qquad
 R_{0,N}=s_N\pi_N^\top,
 \qquad
 R_{1,N}=-s_N\pi_N^\top,
 \tag{6.4}
\]

with \(b>0\).  Both base-plus-structural layers are entrywise positive for

\[
 |\zeta|<\frac{b}{\|s_N\|_\infty},
 \tag{6.5}
\]

and the right side is bounded below by \(b/\sqrt3\).  Moreover,

\[
 \pi_N^\top R_{0,N}=\pi_N^\top R_{1,N}=0,
 \qquad
 \dot M_{1,N}\mathbf1=(\theta_0-\theta_1)s_N.
 \tag{6.6}
\]

Since \(A_N=-D I\) on \(E_N\), direct calculation gives

\[
 \nu_{0,N}=-\frac\beta8+\frac{3\sigma^2}{4D},
 \qquad
 \boxed{\mathscr C_N
 =\frac{K\sigma(\theta_0-\theta_1)}{2D}\ne0,}
 \tag{6.7}
\]

independently of \(N\).  Hence

\[
 \mu_{c,N,\mathcal P_N}(\delta,\zeta)
 -\mu_{c,N,\mathcal P_N}(\delta,0)
 =\frac{K\sigma(\theta_0-\theta_1)}{2D}
  \delta^3\zeta
 +O(\delta^4|\zeta|+\delta^3\zeta^2)
 \tag{6.8}
\]

with one remainder constant for all \(N\).

All uniform hypotheses can be read off explicitly.  Here
\(\tau(P_N)=0\), the transverse semigroup is \(e^{-Dt}I\), and
\(\|c_N\|_N\) is bounded using
\(\|s_N\|_\infty<\sqrt3\).  Moreover,

\[
 \|s_N\pi_N^\top x\|_N
 \le2\sqrt3\,\|x\|_N,
 \tag{6.9}
\]

so the layer total variations are bounded independently of \(N\).  The
nondegeneracy scalar is

\[
 r_N=-\frac{K\sigma(\theta_0-\theta_1)}{2D},
 \tag{6.10}
\]

also independent of \(N\).  Thus (4.5) holds whenever
\(K\sigma(\theta_0-\theta_1)\ne0\).  The sign and scale are transparent:
for \(D,\sigma>0\) and \(\theta_0<\theta_1\), the root coefficient in
(6.7) has sign opposite to \(K\), is linear in the delay separation and
curvature contrast, and decays like \(D^{-1}\).

This family has no nontrivial synchrony partition.  If two distinct nodes
\(i\ne j\) were placed in the same synchrony cell, equality of their voltage
coordinates would have to be preserved.  Test this condition on a constant
history with \(v_i=v_j\ne1\).  The balanced delay term vanishes, the two
rows of \(P_{c,N}\) give the same instantaneous coupling at nodes \(i,j\),
and the common resource and cubic terms also agree.  Their local quadratic
terms nevertheless differ because \(c_{i,N}\ne c_{j,N}\).  The corresponding
polydiagonal is therefore not invariant.  Only the singleton partition
survives.  In particular, (6.8) cannot be explained as an exact lift of a
two-module canard root.

## 7. Scope

Theorem 4.1 proves a local, preparation-indexed, complete-history canard
connection for a uniformly Dobrushin, shared-resource Markov-network class
and a nonzero topology response that remains uniform as \(N\) varies.  It
does not prove:

- a preparation-independent finite-\(\delta\) threshold;
- identification with an arbitrary physical outer slow-manifold selection;
- a global spike/reset separator or a biological pulse-control theorem;
- state-dependent, moving, neutral, or unbounded delay operators; or
- a uniform conclusion when the Dobrushin gap closes or the operator-TV
  bounds grow with \(N\).

The mathematical addition over the homogeneous shared-resource calculation
is precise: the stable response is still constant, but heterogeneous fold
curvature makes the mixed critical Hessian covector nonzero.  This is the
first arbitrary-\(N\), synchrony-quotient-free selected-history root in the current
Paper II program.

## 8. Reproduction

Run

    PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
      tests/test_heterogeneous_curvature_root.py

The exact tests verify a nonuniform three-node example, the all-\(N\)
coefficient (6.7), positivity of the perturbed delay layers, and rejection
of directions that preserve only the collective vector rather than the
full critical row.
