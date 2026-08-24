# An explicit nonzero-eta Floquet box for the quadratic period lock

Status: **proved at the exact reference gain pair, for
\(|\eta|\le3\times10^{-6}\), and promoted to every finite balanced
Dobrushin topology with \(\tau(Q)\le1/4\).**  The distinguished synchronous
orbit is exactly unchanged because the carrier delay is its exact period.
A new 32,046-leaf perturbation certificate proves that its synchronous
translation multiplier remains algebraically simple and that every other
synchronous multiplier remains inside the unit disk.  The quadratic carrier
has zero pure-transverse derivative, so the previously proved Dobrushin
transverse rate is unchanged.  Hence each fixed finite admitted network has
a local basin of orbital attraction throughout this eta interval.

This is an explicit stability interval for one common periodic orbit on one
fixed physical-parameter RFDE family, whose vector field varies with eta.
It is not a joint gain--eta box, a network-uniform nonlinear basin, or a
fixed-\(\varepsilon\) canard-root response theorem.

The executable directed certificate is
[quadratic_period_lock_eta_floquet_box.py](../src/canard_control/quadratic_period_lock_eta_floquet_box.py),
the full-leaf generator is
[quadratic_period_lock_eta_floquet_box.py](../experiments/quadratic_period_lock_eta_floquet_box.py),
and the refusal tests are
[test_quadratic_period_lock_eta_floquet_box.py](../tests/test_quadratic_period_lock_eta_floquet_box.py).

## 1. Exact orbit and exact transverse identity

Consider the quadratic period-locked dual-scaffold RFDE of
[the carrier theorem](quadratic-period-locked-selected-root.md), at

\[
 \varepsilon=\frac15,\qquad a=\frac35,\qquad
 (\kappa_1,\kappa_3)=\left(\frac15,\frac14\right),\qquad
 \tau_*=T_*.
\tag{1.1}
\]

Its added voltage field is

\[
 \varepsilon\eta\Pi\left[
 (v(t)-\mathbf1)^{\circ2}
 -(v(t-T_*)-\mathbf1)^{\circ2}\right].
\tag{1.2}
\]

If \((V_*,W_*)\) is the distinguished synchronous \(T_*\)-periodic
orbit, the bracket in (1.2) vanishes pointwise.  Thus the same orbit and
the same physical period solve the RFDE for every real \(\eta\), not just
to first order.

Let \(E=\ker\pi^T\).  Along any synchronous base history, the derivative of
the carrier on a pure transverse history \(x\in E\) is

\[
 2\Pi\left[
 (V_*(t)-1)x(t)-(V_*(t-T_*)-1)x(t-T_*)
 \right]=0.
\tag{1.3}
\]

Consequently the full transverse variational RFDE is exactly independent
of \(\eta\).  In particular, for every finite nonnegative balanced topology
with \(\tau(Q)\le1/4\), the oscillation-norm Halanay estimate from
[the Dobrushin attraction theorem](paper-iv-dobrushin-periodic-attraction.md)
retains its certified exponential rate \(0.007\).

## 2. The synchronous eta column

Normalize the periodic orbit to unit period and use the logarithmic Floquet
parameter \(s\), so one physical-period shift contributes \(e^{-s}\).
On the voltage component the exact added synchronous pencil is

\[
 \boxed{
 \Delta_\eta\mathcal L_s
 =-2\varepsilon T_*\eta\,
 M_{V_*-1}(1-e^{-s}),}
 \qquad
 \Delta_\eta\mathcal L_s=0
 \quad\hbox{on recovery}.
\tag{2.1}
\]

Here \(M_{V_*-1}\) denotes Wiener convolution by \(V_*-1\).  In particular,
\(\Delta_\eta\mathcal L_0=0\), so the translation vector
\(p=(V_*',W_*')\) stays in the kernel for every eta.

There is a separate moving-period column at \(s=0\), and its normalization
must not be confused with the state-pencil coefficient in (2.1).  Here
\(\theta=t/T_*\) and \(p(\theta)=X_*'(\theta)\) is the normalized tangent;
the physical tangent satisfies
\(p(t/T_*)=T_*\dot x_*(t)\).  For the normalized residual
\(F=DX-Tf\), the carrier's delayed Jacobian is
\(-2\varepsilon\eta M_{V_*-1}\).  In the standard period column

\[
 b=f+\frac{\tau_*}{T}BSp,
\tag{2.2}
\]

the reference identity \(\tau_*/T_*=1\) therefore gives

\[
 \Delta_\eta b=-2\varepsilon\eta M_{V_*-1}p,
 \qquad
 \|\partial_\eta b\|
 \le2\varepsilon\|V_*-1\|_{\mathcal W}\|p\|_{\mathcal W}.
\tag{2.3}
\]

There is no factor \(T_*\) in (2.3).  This is consistent with the exact
identity \(E'_0p=T_*b\): the factor \(T_*\) belongs to \(E'_0\), not to the
normalized period column.

## 3. Four-block leafwise perturbation bound

The previous right-half theorem stores a contraction \(q_C<1\) for each of
32,046 terminal rectangles, but it stores neither a uniform resolvent norm
nor the entries of the finite preconditioner nor a norm for the new eta
channel.  Its minimum slack therefore cannot be used directly, and a newly
formed binary inverse cannot silently be paired with the old \(q_C\).  The
present certificate freezes only the parent partition.  At every leaf
\(C\), it reruns the parent's complete directed four-block validator to
obtain a fresh strict base contraction \(\widehat q_C<1\), together with its
actual finite center inverse \(R_C\) and tail diagonal inverse
\(D_{Q,C}^{-1}\).  The eta perturbation is added to
\(\widehat q_C\), never to an unmatched stored contraction.

Let \(P\) be the retained Fourier projection and \(Q=I-P\).  Directed
Wiener bounds give

\[
 C_*:=2\varepsilon T_*\|V_*-1\|_{\mathcal W}
 \le 19.366302309727024.
\tag{3.1}
\]

On a leaf with \(s\in C\), the complex split norm obeys

\[
 \|1-e^{-s}\|_{\mathrm{split}}
 \le F_C:=\min\left\{1+\sqrt2,
 \sqrt2(\sigma_C^++|\varphi|_C^+)\right\}.
\tag{3.2}
\]

The same convolution estimate applies separately to all four maps

\[
 P\Delta_\eta\mathcal L_sP,\quad
 P\Delta_\eta\mathcal L_sQ,\quad
 Q\Delta_\eta\mathcal L_sP,\quad
 Q\Delta_\eta\mathcal L_sQ.
\tag{3.3}
\]

Indeed, Fourier projection is contractive and multiplication in the Wiener
algebra is submultiplicative.  Therefore both input-column sums of the
preconditioned two-by-two block operator are bounded by the same number:

\[
 \left\|A_C\Delta_\eta\mathcal L_s\right\|_1
 \le |\eta|C_*F_C
 \left(\|R_C\|_1+\|D_{Q,C}^{-1}\|_1\right).
\tag{3.4}
\]

Thus a directed admissible radius for leaf \(C\) is

\[
 \eta_C=
 \frac{1-\widehat q_C}{
 C_*F_C(\|R_C\|_1+\|D_{Q,C}^{-1}\|_1)}.
\tag{3.5}
\]

The full replay gives

\[
 \min_C\eta_C
 \ge 3.31818779196334183438251596448305770862425688971545298
 \times10^{-6}.
\tag{3.6}
\]

The tight leaf is `main_upper` and is also the parent cover's tight leaf.  It
has

\[
 \widehat q_C\le
 0.9949969734691212177432801648052352667472012755814612224,
\tag{3.7}
\]

\(\|R_C\|_1\le2048.123996012442\ldots\), and
\(\|D_{Q,C}^{-1}\|_1\le0.00244869612601\ldots\).  The theorem therefore
uses the outwardly separated value

\[
 \boxed{|\eta|\le3\times10^{-6}}.
\tag{3.8}
\]

This calculation is not an inference from the parent slack.  It is a full
base-contraction replay followed by a new leafwise evaluator for the eta
residual, bound to the parent result hash, leaf count, and leaf digest.

## 4. Translation, tail, and outer half-plane

At \(s=0\), (2.1) leaves the state column of the bordered operator
unchanged.  Only (2.3) changes its period column.  If \(D_0\) is the parent
bordered inverse, then

\[
 \|D_0\|\le
 23.3856903454031773370305076754640443238837022658085131.
\tag{4.1}
\]

The directed Neumann product

\[
 |\eta|\,\|D_0\|\,
 2\varepsilon\|V_*-1\|_{\mathcal W}\|p\|_{\mathcal W}
\tag{4.2}
\]

is strictly below one on (3.8), so the perturbed bordered operator remains
invertible.  Together with the eta-dependent local bounds

\[
 c_{1,\eta}\le c_1+|\eta|C_*,\qquad
 c_{2,\eta}\le c_2+\frac{|\eta|C_*\|p\|}{2},
\tag{4.3}
\]

the parent punctured-neighborhood argument remains strict on its full
radius \(0.0011037180178957863\ldots\).  Hence \(s=0\) is still the only
nearby characteristic value and is algebraically simple.

For the Fourier tail and the outer half-plane, the complex Wiener norm gives
\(|1-e^{-s}|\le2\) when \(\Re s\ge0\).  Adding this eta perturbation to the
parent bounds gives, at \(|\eta|=3\times10^{-6}\), contractions below
\(0.273\) in the tail and below \(0.862\) for \(\Re s\ge128\).  Both are far
from the controlling leafwise constraint.

## 5. Active-horizon Floquet bridge

For nonzero eta the delay \(T_*\) is active.  Thus the shorter-horizon
compactness argument from the eta-zero parent cannot simply be inherited.
The following lemma supplies the missing bridge on
\(C([-T_*,0],\mathbb R^2)\).

> **Lemma 5.1 (power compactness and translation Jordan bridge).**  Let
> \(M_\eta=U_\eta(T_*,0)\) be the one-period monodromy of the synchronous
> variational RFDE on its active horizon \(T_*\).  Then:
>
> 1. \(M_\eta^2=U_\eta(2T_*,0)\) is compact;
> 2. every nonzero multiplier \(\mu\) is represented, at the spectral-set
>    level, by a characteristic value \(s\), \(e^s=\mu\), of the periodic
>    pencil (2.1); every unit-multiplier eigenhistory and every putative
>    rank-two generalized history has the regularity needed for the explicit
>    translation-chain calculation below;
> 3. invertibility of the eta-dependent phase-bordered operator together
>    with \(E'_{0,\eta}p=T_*b_\eta\) excludes a generalized vector above the
>    translation eigenvector.  Hence the unit multiplier is algebraically
>    simple.

**Proof.**  A bounded set of initial histories gives uniformly bounded
solutions on \([0,2T_*]\) by the linear RFDE Gronwall estimate.  On
\([T_*,2T_*]\), the equation then gives a common derivative bound.  The
segments at time \(2T_*\) are uniformly bounded and equicontinuous, so
Arzelà--Ascoli makes \(U_\eta(2T_*,0)\) compact.  Periodicity of the
coefficients gives \(U_\eta(2T_*,0)=M_\eta^2\).  Thus \(M_\eta\) is
power-compact and its nonzero spectral points have finite algebraic
multiplicity.

Let \(G_1\) be the finite-dimensional generalized eigenspace at the unit
multiplier.  The restriction of \(M_\eta\) to \(G_1\) is invertible.  Hence
for every integer \(m\), each \(\phi\in G_1\) can be written
\(\phi=M_\eta^{2m}\psi\) with \(\psi\in G_1\).  Retarded smoothing of
\(U_\eta(2mT_*,0)\) therefore bootstraps precisely the translation
eigenhistory and any putative rank-two generalized history into the strong
periodic domain used below.  No general multiplicity-preserving bridge for
arbitrary nontranslation multipliers is claimed or needed.

If \(M_\eta\phi=\mu\phi\), \(\mu\ne0\), uniqueness and periodicity imply
that its physical-time solution satisfies
\(x(t+T_*)=\mu x(t)\).  Choosing a logarithm \(e^s=\mu\), the normalized
function \(y(\theta)=e^{-s\theta}x(T_*\theta)\) is one-periodic and satisfies
\(\mathcal L_{s,\eta}y=0\).  The converse follows by reversing this
construction.

For the translation mode define the physical-time solution

\[
 \widehat p(t):=p(t/T_*)=T_*\dot x_*(t).
\tag{5.1}
\]

Take \(\phi_0\) to be the history of \(\widehat p\).  If

\[
 (M_\eta-I)\phi_1=\phi_0,
\tag{5.2}
\]

where \(\phi_0\) is the translation history, the corresponding solutions
obey

\[
 x_1(t+T_*)-x_1(t)=\widehat p(t).
\tag{5.3}
\]

Indeed, both sides of the difference solve the same periodic variational
RFDE and have the same initial segment.  In normalized time,

\[
 q(\theta):=x_1(T_*\theta)-\theta p(\theta)
\tag{5.4}
\]

is one-periodic.  Direct substitution gives the first analytic root-chain
equation

\[
 \mathcal L_{0,\eta}q+E'_{0,\eta}p=0.
\tag{5.5}
\]

This also proves the converse chain correspondence needed at \(\mu=1\).
The exact moving-period identity is

\[
 E'_{0,\eta}p=T_*b_\eta.
\tag{5.6}
\]

After replacing \(q\) by \(z=q-\ell(q)p/\ell(p)\), equation (5.5) and
\(\ell(z)=0\) say

\[
 \mathcal B_\eta(z,-T_*)
 =\bigl(\mathcal L_{0,\eta}z+b_\eta T_*,\ell(z)\bigr)=0.
\tag{5.7}
\]

The directed Neumann bound (4.2) proves that \(\mathcal B_\eta\) is
invertible, whereas (5.7) has nonzero scalar component \(-T_*\), a
contradiction.  Bordered invertibility also makes
\(\ker\mathcal L_{0,\eta}=\operatorname{span}\{p\}\), excluding extra
geometric eigenvectors.  Since a power-compact operator with algebraic
multiplicity greater than one and one-dimensional eigenspace must possess a
rank-two Jordan chain, the unit multiplier is algebraically simple.
\(\square\)

The proof deliberately uses the active horizon and \(M_\eta^2\).  It does
not use the eta-zero nilpotent extension of a shorter history space.

## 6. Floquet and full-network theorem

> **Theorem 6.1 (explicit eta Floquet stability box).**  Fix (1.1), the
> physical delay \(\tau_*=T_*\), and \(|\eta|\le3\times10^{-6}\).  The
> distinguished synchronous periodic orbit is exactly the reference orbit.
> Its synchronous monodromy has one algebraically simple unit multiplier,
> and every other synchronous multiplier lies strictly inside the unit
> disk.

**Proof.**  Exact period locking gives the orbit and translation vector.
Lemma 5.1 and the local remainder bounds prove algebraic simplicity and
exclude the punctured translation neighborhood.  The
32,046 leaf inequalities (3.4)--(3.8) exclude the remaining compact
right-half keyhole.  The tail and outer estimates close the infinite
Fourier complement and \(\Re s\ge128\).  These regions exhaust the closed
logarithmic right half-plane modulo the translation value. \(\square\)

> **Corollary 6.2 (nonzero-eta Dobrushin periodic attraction).**  Let
> \(Q\ge0\) be any finite row-stochastic matrix with a strictly positive
> stationary row \(\pi^T\), assume \(\tau(Q)\le1/4\), and let
> \(B_0,B_1\ge0\) satisfy
> \(B_j\mathbf1=\mathbf1/2\) and
> \(\pi^TB_j=\pi^T/2\).  Under Theorem 6.1, the full-network monodromy has
> one algebraically simple unit multiplier and all other multipliers lie
> strictly inside the unit disk.  For each fixed finite admitted topology,
> an open history neighborhood converges to a phase translate of the
> synchronous orbit.

**Proof.**  The collective/transverse splitting is exact.  Theorem 6.1
settles the collective block, while (1.3) and the existing Dobrushin theorem
settle the entire transverse block with rate \(0.007\), independently of
eta.  For each fixed finite network the drift is a smooth polynomial RFDE,
and the monodromy is eventually compact on the active enlarged history
space.  [Hale--Verduyn Lunel, Chapter 10, Section 10.3, Theorem 3.3,
pp. 321--324](https://doi.org/10.1007/978-1-4612-4342-7) therefore gives
local nonlinear orbital attraction with asymptotic phase. \(\square\)

The linear transverse rate is uniform, but the open nonlinear neighborhood
in Corollary 6.2 may depend on \(N,Q,B_0,B_1\) and eta.

## 7. Exact scope

| Statement | Status |
|---|---|
| Exact reference orbit for every real eta | **Proved** |
| Algebraically simple translation multiplier for \(|\eta|\le3\times10^{-6}\) | **Proved** |
| No other synchronous multiplier on or outside the unit circle | **Proved on the eta box at the exact gain pair** |
| Arbitrary finite balanced topology with \(\tau(Q)\le1/4\) | **Proved** |
| Full-network local orbital attraction | **Proved for each fixed admitted network** |
| Joint microscopic gain--eta box | **Not proved** |
| Network-uniform nonlinear basin | **Not proved** |
| Fixed-\(\varepsilon=1/5\) nonzero selected-root derivative \(\partial_\eta a_c\) | **Not proved by this Floquet theorem** |
| Biological onset, pulse capture, safety, or global attraction | **Not implied** |
