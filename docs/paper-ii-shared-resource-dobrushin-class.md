# A genuinely arbitrary-\(N\) shared-resource network class

Status: **exact graph-family skeleton and blow-up identities proved below;
root response open.**  This class is not a replication of the two-module
example.  Its instantaneous topology may be any finite Markov network with
a uniform Dobrushin mixing gap.  A single shared recovery/resource variable
leaves exactly one slow direction, so the singular fold has one critical
fast mode without an artificial transverse recovery scaffold.

The class supplies a natural nonempty family for the dimension-uniform
history-graph theorem.  It also exposes a useful cancellation: homogeneous
node nonlinearities do not automatically return a projection-invisible
transverse perturbation to the scalar canard coordinate.  A nonzero topology
coefficient still requires the full Schur--Melnikov mechanism.

The exact finite-dimensional and fold-chart identities are reproduced in
[shared_resource_markov.py](../src/canard_control/shared_resource_markov.py)
and [its regression tests](../tests/test_shared_resource_markov.py).

## 1. Uniformly mixing graph topology

Let \(P_N\) be an \(N\times N\) row-stochastic matrix with a strictly
positive stationary distribution \(\pi_N\):

\[
 P_N\mathbf 1=\mathbf 1,\qquad
 \pi_N^\top P_N=\pi_N^\top,\qquad
 \pi_N^\top\mathbf 1=1.
 \tag{1.1}
\]

Its Dobrushin coefficient is

\[
 \tau(P_N)
 =\frac12\max_{i,k}\sum_j|(P_N)_{ij}-(P_N)_{kj}|.
 \tag{1.2}
\]

Fix \(\gamma>0\) and assume

\[
 \tau(P_N)\le1-\gamma
 \tag{1.3}
\]

for every graph in the family.  This permits directed, weighted, unequal,
and nonnormal networks; it is stronger than a bare eigenvalue gap because
it controls the semigroup in a dimension-independent node norm.

For \(x\in\mathbb R^N\), put

\[
 \operatorname{osc}(x)=\max_i x_i-\min_i x_i,\qquad
 \|x\|_{\pi,\mathrm{osc}}
 =|\pi_N^\top x|+\operatorname{osc}(x).
 \tag{1.4}
\]

This is a norm.  Define

\[
 P_c=\mathbf1\pi_N^\top,\qquad P_\perp=I-P_c.
 \tag{1.5}
\]

Then

\[
 \|P_c\|_{\pi,\mathrm{osc}}\le1,\qquad
 \|P_\perp\|_{\pi,\mathrm{osc}}\le1,
 \tag{1.6}
\]

and on \(E_N=\ker\pi_N^\top\) the norm is just
\(\operatorname{osc}(x)\).

### Proposition 1.1 (dimension-uniform transverse semigroup)

For \(D>0\), let \(A_N=D(P_N-I)|_{E_N}\).  Then

\[
 \|e^{A_Nt}\|_{E_N\to E_N}
 \le e^{-D\gamma t},\qquad t\ge0,
 \tag{1.7}
\]

uniformly in \(N\).

#### Proof

Dobrushin's inequality gives
\(\operatorname{osc}(P_N^kx)\le\tau(P_N)^k\operatorname{osc}(x)\).
Using the Poisson expansion,

\[
 e^{D(P_N-I)t}
 =e^{-Dt}\sum_{k=0}^\infty\frac{(Dt)^k}{k!}P_N^k,
\]

and (1.3) gives

\[
 \operatorname{osc}(e^{D(P_N-I)t}x)
 \le e^{-Dt}e^{Dt(1-\gamma)}\operatorname{osc}(x).
\]

Stationarity preserves \(E_N\), proving (1.7). \(\square\)

## 2. Shared-resource FitzHugh--Nagumo network

Let \(v\in\mathbb R^N\), \(w\in\mathbb R\), and define componentwise powers.
For \(\varepsilon=\delta^2\), consider

\[
\begin{aligned}
 \dot v(t)
 &=v(t)-\frac13v(t)^{\circ3}-w(t)\mathbf1
   +D(P_N-I)v(t)\\
 &\quad+\varepsilon K\left[
 C_Nv(t)-\int_{[0,\Theta_*]}
       \mathbb B_N(d\theta)\,
       v\!\left(t-\frac{\theta}{\delta}\right)\right],\\
 \dot w(t)&=\varepsilon\bigl(\pi_N^\top v(t)-a\bigr),
\end{aligned}
\tag{2.1}
\]

where

\[
 C_N=\int_{[0,\Theta_*]}\mathbb B_N(d\theta).
 \tag{2.2}
\]

The balanced form (2.2) makes the delayed feedback vanish on every constant
history.  Assume the operator-valued measures and their declared structural
derivatives have uniformly bounded total variation in the norm (1.4).

At

\[
 v_*=\mathbf1,\qquad w_*=\frac23,\qquad a_*=1,
 \tag{2.3}
\]

the equilibrium residual vanishes.  The fast voltage Jacobian is
\(D(P_N-I)\).  Its kernel is \(\operatorname{span}\{\mathbf1\}\), while
(1.7) controls the complement.  Moreover,

\[
 \pi_N^\top D_v^2F(v_*,w_*)[\mathbf1,\mathbf1]=-2\ne0,
 \tag{2.4}
\]

and

\[
 D_a(\pi_N^\top v-a)=-1.
 \tag{2.5}
\]

Thus (2.3) is a simple collective fold with one slow unfolding direction.

### Uniform nonlinear bounds

The norm (1.4) controls coordinates:

\[
 \|x\|_\infty\le\|x\|_{\pi,\mathrm{osc}}.
 \tag{2.6}
\]

Also

\[
 \|y\|_{\pi,\mathrm{osc}}\le3\|y\|_\infty.
 \tag{2.7}
\]

Consequently pointwise multiplication is a uniformly bounded multilinear
map, with

\[
 \|x_1\circ\cdots\circ x_k\|_{\pi,\mathrm{osc}}
 \le3\prod_{j=1}^k\|x_j\|_{\pi,\mathrm{osc}}.
 \tag{2.8}
\]

On a declared coordinate box
\(\sup_i|v_i|\le V_*\), the cubic voltage field therefore has
dimension-independent Fréchet bounds through every requested order:
\[
 \|D^2F(v)\|\le6V_*,\qquad
 \|D^3F\|\le6,\qquad D^kF=0\quad(k\ge4).
 \tag{2.9}
\]

This avoids the coordinate-spike failure of normalized weighted
\(\ell^2\) balls.

## 3. Exact fold chart

Set

\[
 v=\mathbf1+\delta\mathbf1X+\delta^2z,\qquad
 w=\frac23-\delta^2Y,\qquad
 a=1+\delta^2\nu,\qquad
 \pi_N^\top z=0,\qquad s=\delta t.
 \tag{3.1}
\]

For a chart history \(\phi\), write

\[
 \mathcal L_N[\phi]
 =C_N\phi(0)-\int\mathbb B_N(d\theta)\phi(-\theta).
 \tag{3.2}
\]

Direct substitution in (2.1) gives the exact fixed-history-interval RFDE

\[
\begin{aligned}
 X'={}&Y-X^2\\
 &+\delta\left[-\frac13X^3
 +K\pi_N^\top\mathcal L_N[\mathbf1X+\delta z]\right]\\
 &-\delta^2\pi_N^\top z^{\circ2}
 -\delta^3X\pi_N^\top z^{\circ2}
 -\frac{\delta^4}{3}\pi_N^\top z^{\circ3},\\
 Y'={}&-X+\delta\nu,\\
 \delta z'={}&A_Nz
 +\delta P_\perp\left[-2Xz
 +K\mathcal L_N[\mathbf1X+\delta z]\right]\\
 &-\delta^2P_\perp(z^{\circ2}+X^2z)
 -\delta^3P_\perp(Xz^{\circ2})
 -\frac{\delta^4}{3}P_\perp z^{\circ3}.
\end{aligned}
\tag{3.3}
\]

There is no singular stable shift: the algebraic equation at \(\delta=0\)
is \(A_Nz=0\), hence \(z=0\) on \(E_N\).  Equations (1.7), (2.9), the
fixed-support operator-TV bound, and a componentwise bounded preparation
put (3.3) directly into the dimension-uniform special-flow history-graph
theorem.

### Corollary 3.1 (history graph, conditional only on preparation data)

For every family satisfying (1.1)--(1.3) and the uniform fixed-support
operator-TV bounds, any preparation satisfying the explicit logarithmic
tame conditions of the abstract graph theorem yields an invariant
complete-history graph for (3.3), with constants independent of \(N\).
The retained histories solve the unprepared RFDE wherever their full delay
backtracks remain in the uncut hull.

This corollary is a model-fitting statement, not a canard-root theorem.
Construction of the canonical or physical matching traces and their gap is
still required.

## 4. Projected measures and the return mechanism

The complete critical projected delay measure is

\[
 \rho_{c,N}(d\theta)
 =\pi_N^\top\mathbb B_N(d\theta)\mathbf1.
 \tag{4.1}
\]

A structural perturbation \(\Delta\mathbb B_N\) is projection-neutral when

\[
 \pi_N^\top\Delta\mathbb B_N(d\theta)\mathbf1=0
 \quad\text{as a measure identity}.
 \tag{4.2}
\]

It may nevertheless generate the transverse forcing

\[
 P_\perp\int\Delta\mathbb B_N(d\theta)\mathbf1
 \,[X(s)-X(s-\theta)].
 \tag{4.3}
\]

For the homogeneous cubic in (2.1), the immediate quadratic return cancels:

\[
 \pi_N^\top\bigl(\mathbf1\circ z\bigr)=\pi_N^\top z=0.
 \tag{4.4}
\]

Therefore projection neutrality alone does not imply either a nonzero or a
zero canard-root response.  A linear response can re-enter through delayed
stable-to-critical mixing, preparation/endpoint terms, or heterogeneous
curvature.  If, in addition to (4.2), every layer is block closed,

\[
 \pi_N^\top\mathbb B_N(d\theta)P_\perp=0,
 \tag{4.5}
\]

and the selected-history gap has no explicit transverse or endpoint
dependence, the strict direct-sum calculation makes the first transverse
coefficient zero.  This is a negative control, not a universal selection
law.

## 5. Why this class matters

1. The graph topology is not restricted to two modules or an equitable
   quotient.  Any finite directed Markov network satisfying the uniform
   Dobrushin condition is allowed.
2. The shared recovery/resource variable gives a biologically interpretable
   one-gap candidate without adding a fixed transverse recovery scaffold.
3. The same theorem permits matrix-valued heterogeneous delays in a
   dimension-independent operator-TV ball.
4. The cancellation (4.4) prevents a false genericity claim: a transverse
   topology perturbation becomes a canard-threshold perturbation only after
   the complete Schur--Melnikov return has been evaluated.
5. Networks with independent node recoveries are not covered by this
   one-slow-variable class.  Their cokernel dimension must be handled by the
   vector-gap theorem.

## 6. Remaining proof obligations

- construct one explicit preparation with the tame bounds used in
  Corollary 3.1; equation (3.3) is already reproduced symbolically from
  the physical model;
- define canonical or physical selected histories and the complete-history
  gap;
- prove its simple-root derivative uniformly in \(N\);
- evaluate the full direct/transverse/history/endpoint topology functional
  and provide a nonzero witness, or state the resulting cancellation
  theorem;
- connect the physical root to a pulse/quiet global itinerary before using
  it as a biological safety coordinate.

## 7. Reproduction

Run the following command from the repository root:

    PYTHONPATH=build/testdeps:src python3 -m pytest -q \
      tests/test_shared_resource_markov.py

The tests check the exact Dobrushin coefficient and transverse semigroup
bound for a nonuniform stationary distribution, the physical-to-chart
polynomial division and all three zero residuals in (3.3), a
projection-neutral transverse forcing direction, and invalid Markov data as
a negative control.
