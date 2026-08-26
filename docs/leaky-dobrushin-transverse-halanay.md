# Uniform transverse decay for finite leaky-recovery networks

Status: **proved at the center parameters for every finite topology in the
declared balanced Dobrushin class.**  The quiet equilibrium and both
validated scalar periodic orbits have no unstable or neutral transverse
network direction.  This is a linear transverse theorem.  The collective
Floquet indices, a network-uniform nonlinear basin radius, and physical-pulse
onset remain open.

## 1. Network and synchronous restriction

Let all scalar nonlinearities act componentwise and consider

\[
\begin{aligned}
 \dot v={}&f(v)-w+3(Q-I)v
 +\varepsilon\kappa _1
 \{B_0v(t-\tau _0)+B_1v(t-\tau _1)-v\}\\
 &+\varepsilon\kappa _3
 \{B_0H(v(t-\tau _0))+B_1H(v(t-\tau _1))-H(v)\},\\
 \dot w={}&\varepsilon(v-a\mathbf1-w)+2(Q-I)w,
\end{aligned}
\tag{1.1}
\]

where

\[
 f(s)=s-s^3/3,\qquad H(s)=(s-1)^3.
\]

For every finite network assume

\[
 Q\mathbf1=\mathbf1,\quad \pi^TQ=\pi^T,\quad
 \tau(Q)\le\frac12,
\tag{1.2}
\]

Here

\[
 \tau(Q)=\frac12\max_{i,k}\sum_\ell|Q_{i\ell}-Q_{k\ell}|
\]

is the Dobrushin contraction coefficient.  For \(j=0,1\), also assume

\[
 B_j\ge0,\quad B_j\mathbf1=\frac12\mathbf1,
 \quad \pi^TB_j=\frac12\pi^T.
\tag{1.3}
\]

Here \(\pi\) is strictly positive.  The synchronous subspace is invariant,
and its restriction is exactly the scalar leaky RFDE at

\[
 \varepsilon=\frac15,\quad a=\frac14,\quad
 \kappa _1=\frac1{250},\quad \kappa _3=\frac1{200},
 \quad(\tau _0,\tau _1)=(4\sqrt5,5\sqrt5).
\tag{1.4}
\]

Normalize \(\pi^T\mathbf1=1\).  The balance identities give the invariant
splitting

\[
 \mathbb C^N=\operatorname{span}\{\mathbf1\}\oplus\ker\pi^T
\tag{1.5}
\]

for every current and delayed block of the variational equation.  Thus the
collective block is the scalar variational RFDE and the complementary block
is genuinely transverse.  No simultaneous diagonalization of \(Q,B_0,B_1\)
is assumed.

## 2. Directed voltage strip

The source-bound inner and outer radii theorems provide exact scalar
periodic orbits in the phase-fixed component Wiener balls of radius
\(\rho=10^{-5}\).  In particular, the voltage correction is pointwise at
most \(\rho\).  The separately source-validated Floquet-transfer artifact
provides a bound \(L_i\) on the exact normalized-phase tangent of each
orbit.  If \(s_k=k/1024\), directed Fourier evaluation and the nearest
sample on the phase circle give

\[
 \sup_s|V_i(s)-1|
 \le \max_k|\bar V_i(s_k)-1|+\rho+\frac{L_i}{2048}.
\tag{2.1}
\]

All three terms in (2.1) are outward-rounded.  They prove

\[
 |V_i(t)-1|<\frac52,
 \qquad i\in\{u,p\}.
\tag{2.2}
\]

The executable artifact records the two strict margins separately; the
smaller, on the outer branch, is still greater than \(0.0101\).  Thus the
1024 values are not being treated as a sampled extremum.

## 3. Weighted oscillation estimate

For \(z\in\mathbb C^N\), set

\[
 \operatorname{diam}z=\max_{i,k}|z_i-z_k|.
\tag{3.1}
\]

This equals \(\operatorname{osc}z\) for real vectors and is a norm on
\(\ker\pi^T\).  The usual Dobrushin argument remains valid over
\(\mathbb C\): the difference of two stochastic rows is the common mass
\(\tau\) times the difference of two convex combinations, whose distance
is bounded by the diameter.  Hence

\[
 \operatorname{diam}(Qz)\le\tau(Q)\operatorname{diam}z,
 \qquad
 \operatorname{diam}(B_jz)\le\frac12\operatorname{diam}z.
\tag{3.2}
\]

Let \((x,y)\) be a possibly complex transverse variational solution along
the quiet equilibrium or either periodic orbit, and put

\[
 M(t)=\max\{\operatorname{diam}x(t),
                 3\operatorname{diam}y(t)\}.
\tag{3.3}
\]

The voltage current coefficient in the exact variational equation is

\[
 g(t)=1-V(t)^2-\varepsilon\kappa_1
      -3\varepsilon\kappa_3(V(t)-1)^2
 \le 1-\varepsilon\kappa_1=0.9992.
\tag{3.4}
\]

Using (2.2) and the half-mass bound in (3.2), the sum of both delayed
voltage contributions is bounded by

\[
 \beta\le\varepsilon\{\kappa _1+3\kappa _3(5/2)^2\}
 =0.01955.
\tag{3.5}
\]

At a time when the voltage term realizes the maximum in (3.3), its local
decay is at least

\[
 \alpha_v=3(1-\tau(Q))-g(t)-\frac13
 \ge0.167466\ldots .
\tag{3.6}
\]

At a recovery maximum, the leak contributes the additional local decay
\(+\varepsilon\), whereas the weighted forcing from \(x\) is
\(3\varepsilon\).  Therefore

\[
 \alpha_w=2(1-\tau(Q))+\varepsilon-3\varepsilon
 \ge0.6.
\tag{3.7}
\]

Thus, with \(r=5\sqrt5\),

\[
 D^+M(t)\le-\alpha M(t)
 +\beta\sup_{t-r\le s\le t}M(s),
 \qquad \alpha=\min\{\alpha_v,\alpha_w\}.
\tag{3.8}
\]

Directed arithmetic proves both \(\alpha-\beta>0\) and

\[
 \alpha-\frac1{10}-\beta e^{r/10}>0.
\tag{3.9}
\]

For \(\lambda=1/10\), apply the first-crossing argument to
\(e^{\lambda t}M(t)\).  If

\[
 \|\phi\|_0=\sup_{-r\le\theta\le0}M(\phi(\theta)),\qquad
 \|\phi\|_\lambda=
 \sup_{-r\le\theta\le0}e^{\lambda\theta}M(\phi(\theta)),
\tag{3.10}
\]

then (3.9) yields both the familiar estimate

\[
 M(t)\le e^{-t/10}
 \sup_{-r\le s\le0}M(s).
\tag{3.11}
\]

and the sharper weighted statement

\[
 e^{t/10}M(t)\le\|\phi\|_{1/10}.
\tag{3.12}
\]

## 4. Consequences and exact boundary

> **Theorem 4.1.**  For every finite network satisfying (1.2)--(1.3), all
> transverse variational solutions along the quiet equilibrium, the inner
> scalar periodic orbit, and the outer scalar periodic orbit satisfy
> (3.11)--(3.12).  If \(U_i(T_i)\) is the transverse one-period history
> operator, then
> \[
>  \|U_i(T_i)\|_0\le e^{-(T_i-r)/10},\qquad
>  \|U_i(T_i)\|_{1/10}\le e^{-T_i/10}.
> \tag{4.1}
> \]
> Consequently every noncollective periodic multiplier \(\mu\) satisfies
> \(|\mu|<e^{-T_i/10}<1\).  The full-network quiet equilibrium is locally
> exponentially stable for every fixed admitted topology.

Equation (4.1) separates two quantities that must not be conflated.  The
loss of one retained-history length occurs in the **unweighted operator
norm**, giving \(e^{-(T_i-r)/10}\).  The equivalent exponentially weighted
history norm has operator bound \(e^{-T_i/10}\), and spectral values do not
depend on which equivalent norm is used.  Hence the multiplier disk has the
stronger radius \(e^{-T_i/10}\).  The executable record stores both bounds.
The strict residual in (3.9) allows a slightly larger decay exponent, which
makes the displayed multiplier inequality strict.

For the last conclusion, (1.5) splits the full linearized equilibrium
semigroup into the already proved exponentially stable scalar collective
block and the transverse block controlled above.  On the fixed
finite-dimensional node space, diameter is equivalent to the ordinary norm
on \(\ker\pi^T\).  The full linearization is therefore exponentially stable,
and the standard linearized-stability theorem for retarded equations gives
local nonlinear exponential stability.  This argument is for each fixed
admitted topology; it supplies no topology-independent nonlinear radius.

For the cycles, the theorem says only that all undecided Floquet indices are
collective.  Until the scalar outer index zero and scalar inner index one are
proved, it does not promote network orbital attraction or the network
separator index.  It also proves no network-uniform nonlinear basin radius,
global synchronization, physical onset threshold, or pulse capture.

Reproduce the source-bound record with

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_dobrushin_transverse_halanay.py
```
