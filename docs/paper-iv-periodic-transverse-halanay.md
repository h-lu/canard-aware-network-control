# Size-uniform transverse decay along the periodic FHN branch

Status: **proved for the fixed rank-one two-module topology with arbitrary
positive module sizes.**  The result upgrades the existing synchronous
Floquet theorem to full-network orbital hyperbolicity after fixing the
instantaneous scaffolds to \(D=3\) and \(E=2\).  It does not determine the
synchronous stability index and therefore does not prove attraction.

The executable coefficient certificate and representative exact node-level
algebra audit are
[`fhn_periodic_transverse_halanay.py`](../src/canard_control/fhn_periodic_transverse_halanay.py),
the driver is
[`fhn_periodic_transverse_halanay.py`](../experiments/fhn_periodic_transverse_halanay.py),
and the tracked result is
[`fhn_periodic_transverse_halanay.json`](../experiments/results/fhn_periodic_transverse_halanay.json).
Its SHA-256 digest is

```text
ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb
```

## 1. Fixed network and exact modal splitting

Let \(C_1,C_2\) have arbitrary sizes \(n_1,n_2\ge1\), let \(R\) take the
two module averages, and let \(S\) replicate two module values to the nodes. On
module coordinates put

\[
 C_0=\frac12 I_2,
 \qquad
 C_1=\frac12
 \begin{pmatrix}0&1\\1&0\end{pmatrix},
 \qquad
 B_j=SC_jR .
\tag{1.1}
\]

Then

\[
 P=B_0+B_1=\mathbf1\pi^T,
 \qquad
 \pi_i=\frac1{2n_a}\quad(i\in C_a).
\tag{1.2}
\]

The completely synchronous vector \(r_c=(1,1)^T\) and the module-difference
vector \(r_d=(1,-1)^T\) satisfy

\[
 C_0r_c=C_1r_c=\frac12r_c,
 \qquad
 C_0r_d=\frac12r_d,
 \qquad
 C_1r_d=-\frac12r_d.
\tag{1.3}
\]

Both \(B_0\) and \(B_1\) annihilate every within-module zero-mean vector.
Consequently node space splits exactly into the collective mode, one module-
difference mode, and \(N-2\) within-module modes.  The split is independent
of \(n_1,n_2\); no continuum or large-network approximation is involved.
The universal size quantifier follows from the formulas
\(B_j=SC_jR\), \(RS=I_2\), and
\(W_1\oplus W_2\subset\ker R\), together with the explicit modal basis in
the node equations. The executable certificate checks representative sizes
as algebra-regression tests; finite enumeration is not presented as a proof
of the universal quantifier.

Fix

\[
 (\varepsilon,a,\Theta_0,\Theta_1,D,E)
 =\left(\frac15,\frac35,4,5,3,2\right)
\tag{1.4}
\]

and retain the microscopic gain box

\[
 |\kappa_1-0.2|\le10^{-12},
 \qquad
 |\kappa_3-0.25|\le10^{-12}.
\tag{1.5}
\]

The scaffolds \(D(P-I)\) and \(E(P-I)\) vanish on synchrony. Thus fixing
\(D=3,E=2\) does not change the already validated synchronous periodic
branch or its two-output response map.  It does specify a particular full
network containing that branch.

## 2. Transverse variational equation

Let \((V(t),W(t))\) be any orbit on the validated synchronous branch. Define

\[
 \begin{aligned}
 g(t)&=1-V(t)^2-\varepsilon\kappa_1
       -3\varepsilon\kappa_3(V(t)-1)^2,\\
 H(t)&=\frac{\varepsilon\kappa_1}{2}
       +\frac{3\varepsilon\kappa_3}{2}(V(t)-1)^2.
 \end{aligned}
\tag{2.1}
\]

On the module-difference mode, the transverse variables \((x,y)\) solve

\[
 \begin{aligned}
 \dot x(t)={}&[g(t)-D]x(t)-y(t)
 +H(t-\tau_0)x(t-\tau_0)
 -H(t-\tau_1)x(t-\tau_1),\\
 \dot y(t)={}&\varepsilon x(t)-Ey(t).
 \end{aligned}
\tag{2.2}
\]

Every within-module mode obeys the same current-state system with both
delayed terms absent. It is therefore enough to estimate (2.2) with the
absolute sum of its two delayed coefficients.

## 3. Global current bound and the source Wiener estimate

Put \(q=3\varepsilon\kappa_3>0\). Completing the square gives the exact
identity

\[
 V^2+q(V-1)^2
 =(1+q)\left(V-\frac{q}{1+q}\right)^2+\frac{q}{1+q}.
\tag{3.1}
\]

Hence, globally in \(V\in\mathbb R\),

\[
 g(t)\le
 g_*=1-\varepsilon\kappa_1-\frac{q}{1+q}.
\tag{3.2}
\]

Directed evaluation on (1.5) yields

\[
 g_*\le
 0.8295652173920941398865781421878852635779889294300063374.
\tag{3.3}
\]

The full-complex periodic Floquet certificate already bounds the Wiener norm
of \(H\) uniformly over the exact orbit correction ball and the entire gain
box.  Since the Wiener norm dominates the pointwise norm,

\[
 \sup_t|H(t)|\le
 0.4564418432116889097019118385025544264603768202010172483.
\tag{3.4}
\]

Therefore the total delayed gain in (2.2) satisfies

\[
 \beta_\perp\le
 0.9128836864233778194038236770051088529207536404027187244.
\tag{3.5}
\]

This use of the source record is important: a sampled maximum of \(H\) would
not prove (3.4), whereas the validated Wiener enclosure does.

## 4. Halanay inequality

For a transverse solution put

\[
 M(t)=\max\{|x(t)|,|y(t)|\},
 \qquad
 M_t=\sup_{t-\tau_*\le s\le t}M(s),
 \qquad
 \tau_*=\max\{\tau_0,\tau_1\}.
\tag{4.1}
\]

If the voltage component realizes the maximum, (2.2)--(3.5) imply

\[
 D^+M(t)
 \le-[D-g_*-1]M(t)+\beta_\perp M_t.
\tag{4.2}
\]

If the recovery component realizes it, then

\[
 D^+M(t)\le-[E-\varepsilon]M(t).
\tag{4.3}
\]

Thus in both cases

\[
 D^+M(t)\le-\alpha_\perp M(t)+\beta_\perp M_t,
\tag{4.4}
\]

where the publicly recomposed directed endpoints are

\[
 \begin{aligned}
 D-g_*-1&\ge
 1.170434782607905860113421857812114736422011070567256752,\\
 E-\varepsilon&\ge
 1.799999999999999999999999999999999999999999999998084162,\\
 \alpha_\perp&\ge
 1.170434782607905860113421857812114736422011070565888296.
 \end{aligned}
\tag{4.5}
\]

In particular,

\[
 \boxed{
 \alpha_\perp-\beta_\perp\ge
 0.2575510961845280407095981808070058835012574301614590022>0.}
\tag{4.6}
\]

The maximum physical delay obeys

\[
 \tau_*\le
 11.18033988749894848204586834365638117720309179809627588.
\tag{4.7}
\]

At the directed candidate rate \(\lambda_\perp=0.02\), the Halanay residual

\[
 \alpha_\perp-\lambda_\perp
 -\beta_\perp e^{\lambda_\perp\tau_*}
\tag{4.8}
\]

has lower bound

\[
 0.008801439478304289668730401137295866821421657268435637754>0.
\tag{4.9}
\]

Halanay's inequality therefore gives exponential decay with every rate no
larger than \(0.02\), uniformly in the gain box, module sizes, and transverse
mode.

## 5. Full-network orbital hyperbolicity

> **Theorem 5.1 (size-uniform transverse periodic decay).**  For every gain
> pair in (1.5), every \(n_1,n_2\ge1\), and the fixed rank-one network
> (1.1)--(1.4), all transverse solutions of the variational RFDE along the
> validated synchronous periodic orbit decay exponentially.  The rate
> \(0.02\) is valid uniformly.

**Proof.**  The exact decomposition (1.3) reduces the only delayed transverse
block to (2.2); within-module modes delete its delayed terms.  Equations
(3.1)--(4.9) place every block under the same Halanay inequality.  The
constants do not depend on \(n_1,n_2\). \(\square\)

> **Corollary 5.2 (full-network orbital hyperbolicity).**  On the same box and
> for the same arbitrary module sizes, the full-network periodic orbit has
> exactly one unit-circle multiplier: the algebraically simple autonomous
> multiplier \(1\).

The synchronous Floquet theorem proves that the collective block has only
that simple unit multiplier.  Theorem 5.1 puts every multiplier from every
transverse block strictly inside the unit disk.  Exact modal direct-sum
decomposition then proves the corollary.

Corollary 5.2 is not an attraction theorem.  The synchronous theorem excludes
unit-circle crossings but does not yet count how many collective multipliers
lie outside the unit disk.  Transverse decay cannot determine that missing
synchronous stability index.

## 6. Claim ledger

| Statement | Status |
|---|---|
| Synchronous periodic branch on the microscopic gain box | **Proved by the source parameter-box theorem** |
| Synchronous orbital hyperbolicity | **Proved by the source full-complex Bloch theorem** |
| Exact collective/difference/within modal splitting | **Proved for the fixed rank-one two-module topology** |
| Transverse variational exponential decay along the entire periodic orbit | **Proved uniformly for arbitrary \(n_1,n_2\ge1\)** |
| Full-network orbital hyperbolicity | **Proved for this fixed topology and \(D=3,E=2\)** |
| Synchronous or full-network attraction | **Open; a stability index is still required** |
| Nonlinear synchronization or a noisy-history basin | **Not proved** |
| Arbitrary/general network topology | **Not proved** |
| Physical pulse onset or pulse/quiet basin capture | **Not implied by this theorem** |

The result is genuinely size-uniform but not topology-uniform.  Replacing the
rank-one delay layers by a general directed graph requires a graph-dependent
or graph-uniform operator norm bound and cannot be inferred from (1.3).
