# A same-model recovery-clamped separator for the dual-scaffold FHN network

Status: **proved for an ideal controlled decision protocol on the fixed
rank-one two-module topology.**  The result concerns a constant complete-history
reset, an exact collective-recovery clamp, and first hits of the voltage faces
\(x=\pm1\).  It is not an unforced or maximal-canard onset theorem, and the two
first-hit faces are not identified with biological pulse and quiet basins.

The executable arithmetic is in
[`fhn_same_model_separator.py`](../src/canard_control/fhn_same_model_separator.py),
the driver is
[`fhn_same_model_separator.py`](../experiments/fhn_same_model_separator.py),
and the current result record is
[`fhn_same_model_separator.json`](../experiments/results/fhn_same_model_separator.json).
Its SHA-256 digest at the time of this note is

```text
9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86
```

The periodic response certificate uses the completely synchronous restriction
of the same plant.  The recovery clamp below is switched on only during the
decision stage; it is absent from the autonomous RFDE whose periodic response
was validated.

## 1. Plant, delay layers, and the controlled leaf

Let \(C_1,C_2\) be nonempty modules of sizes \(n_1,n_2\), and write

\[
 \bar z_a=\frac1{n_a}\sum_{i\in C_a}z_i,
 \qquad
 \pi^Tz=\frac12(\bar z_1+\bar z_2).
\tag{1.1}
\]

Thus \(\pi^T\mathbf1=1\).  Define the same-module and cross-module delay
layers by

\[
 (B_0z)_i=\frac12\bar z_a,
 \qquad
 (B_1z)_i=\frac12\bar z_b,
 \qquad i\in C_a,\quad b\ne a.
\tag{1.2}
\]

Their sum is the rank-one projection

\[
 P=B_0+B_1=\mathbf1\pi^T,
 \qquad P^2=P.
\tag{1.3}
\]

For componentwise \(H(z)=(z-1)^3\), the baseline plant is

\[
\begin{aligned}
 \dot v={}&v-\frac13v^3-w+D(P-I)v\\
 &+\varepsilon\kappa_1
   \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
   \{B_0H(v(t-\tau_0))+B_1H(v(t-\tau_1))-H(v)\},\\
 \dot w={}&\varepsilon(v-a\mathbf1)+E(P-I)w.
\end{aligned}
\tag{1.4}
\]

Here and below powers of \(v\) are componentwise.  We fix

\[
 \varepsilon=\frac15,
 \quad a=\frac35,
 \quad \tau_0=4\sqrt5,
 \quad \tau_1=5\sqrt5,
 \quad D=3,
 \quad E=2,
\tag{1.5}
\]

and use the validated gain box

\[
 U=[0.199999999999,0.200000000001]
   \times[0.249999999999,0.250000000001].
\tag{1.6}
\]

The values \(D=3\) and \(E=2\) are fixed here for the full-network decision
estimate.  They do not change the synchronous periodic branch because both
instantaneous scaffolds vanish on complete synchrony.

During the decision stage, apply the common recovery input

\[
 u_c(v)=-\varepsilon(\pi^Tv-a),
 \qquad
 \dot w=\varepsilon(v-a\mathbf1)+E(P-I)w+\mathbf1u_c(v).
\tag{1.7}
\]

Since \(\pi^T(P-I)=0\), (1.7) gives

\[
 \frac{d}{dt}\pi^Tw=0.
\tag{1.8}
\]

The controlled RFDE is therefore considered on the closed history leaf

\[
 \mathcal X_{\rm cl}
 =\{\phi\in C([-\tau_*,0],\mathbb R^{2N}):
       \pi^T\phi_w(\theta)=0\text{ for every }\theta\},
 \qquad \tau_*=5\sqrt5.
\tag{1.9}
\]

This restriction is essential.  If the collective recovery coordinate were
retained while only its derivative were set to zero, it would be a neutral
coordinate and the hyperbolic codimension-one conclusion below would be
false in that enlarged phase space.  Equivalently, one may regard (1.7) as an
ideal algebraic clamp that removes the collective recovery coordinate.

The common input has zero transverse projection:

\[
 (I-P)\mathbf1u_c=0.
\tag{1.10}
\]

Consequently the clamp fixes the collective mean without changing the
module-difference or within-module recovery equations.

## 2. Synchronous decision equation and reset histories

The synchronous leaf in \(\mathcal X_{\rm cl}\) has
\(v=x\mathbf1\) and \(w=0\).  Equations (1.2) and (1.7) reduce the decision
dynamics exactly to

\[
\begin{aligned}
 \dot x={}&x-\frac{x^3}{3}
 +\varepsilon\kappa_1
 \left\{\frac{x(t-\tau_0)+x(t-\tau_1)}2-x\right\}\\
 &+\varepsilon\kappa_3
 \left\{
 \frac{(x(t-\tau_0)-1)^3+(x(t-\tau_1)-1)^3}{2}
 -(x-1)^3\right\}.
\end{aligned}
\tag{2.1}
\]

For \(-1\le r\le1\), define the complete-history reset

\[
 \Phi_r(\theta)=(r\mathbf1,0),
 \qquad -\tau_*\le\theta\le0.
\tag{2.2}
\]

At the release instant, both delayed-minus-current actuators vanish on
\(\Phi_r\); the two instantaneous scaffolds vanish as well.  For \(r=0\),
the entire future remains constant, so \(\Phi_0\) is the exact controlled
equilibrium for every \((\kappa_1,\kappa_3)\in U\).

The reset in (2.2) prescribes a whole delay window.  No assertion is made here
that a finite-duration laboratory pulse realizes this history exactly.

## 3. Characteristic roots and the reset projection

Put

\[
 k=\kappa_1+3\kappa_3,
 \qquad d=\varepsilon k,
 \qquad \alpha=1-d.
\tag{3.1}
\]

The collective characteristic function at \(\Phi_0\) is

\[
 \Delta(z)=z-\alpha-\frac d2
       \{e^{-z\tau_0}+e^{-z\tau_1}\}.
\tag{3.2}
\]

The directed gain-box bounds give

\[
\begin{aligned}
 d&\in[
 0.1899999999991999999999999999999999999999999999993395464,
 0.1900000000008000000000000000000000000000000000009136178],\\
 \alpha&\in[
 0.8099999999991999999999999999999999999999999999980600405,
 0.8100000000008000000000000000000000000000000000011736244],\\
 \alpha-d&\ge
 0.6199999999983999999999999999999999999999999999974885366.
\end{aligned}
\tag{3.3}
\]

> **Theorem 3.1 (one controlled unstable root).**  For every gain pair in
> \(U\), \(\Delta\) has exactly one zero in the open right half-plane,
> counted with algebraic multiplicity, and has no zero on the imaginary axis.
> The right-half-plane zero \(\lambda_u\) is real, positive, and simple.

**Proof.** For \(s\in[0,1]\), consider

\[
 \Delta_s(z)=z-\alpha-\frac{sd}{2}
       \{e^{-z\tau_0}+e^{-z\tau_1}\}.
\tag{3.4}
\]

On \(\operatorname{Re}z=0\),

\[
 \left|\frac{sd}{2}
 \{e^{-z\tau_0}+e^{-z\tau_1}\}\right|
 \le d<\alpha\le|z-\alpha|.
\tag{3.5}
\]

On a sufficiently large right half-circle, \(z-\alpha\) also dominates the
bounded delayed term, uniformly in \(s\).  Rouché's theorem, equivalently the
argument principle along this homotopy, therefore preserves the number of
right-half-plane zeros.  At \(s=0\), there is exactly one, namely
\(z=\alpha\).  Inequality (3.5) also excludes imaginary roots for every
\(s\).  Finally, \(\Delta(0)=-1\) and \(\Delta(x)\to+\infty\) as
\(x\to+\infty\), so the unique right-half-plane root is real and positive.
Its total algebraic multiplicity is one. \(\square\)

The root equation also gives \(0<\lambda_u<\alpha+d=1\).  Normalize the
unstable eigenfunction by \(e_u(0)=1\).  For the linearized solution with
constant history \(r\), direct Laplace transformation gives

\[
 \widehat x_r(z)=\frac r z+\frac{r}{z\Delta(z)}.
\tag{3.6}
\]

Hence its unstable spectral coefficient is

\[
 c_u(r)=\frac{r}{\lambda_u\Delta'(\lambda_u)}.
\tag{3.7}
\]

Because

\[
 \lambda_u\Delta'(\lambda_u)
 =\lambda_u+\frac d2\sum_{j=0}^1
   (\lambda_u\tau_j)e^{-\lambda_u\tau_j}
 \le1+d,
\tag{3.8}
\]

the reset tangent has the uniform projection bound

\[
 c_u'(0)\ge\frac1{1+d}
 \ge
 0.8403361344532165807499474174247059177025716262714088742.
\tag{3.9}
\]

Thus the constant-history reset curve is transverse to the stable spectral
space at \(\Phi_0\).

## 4. The two first-hit channels

For \(0<r<1\), let \(T_+(r)\) be the first time the solution of (2.1) with
history \(\Phi_r\) reaches \(x=1\).  For \(-1<r<0\), define \(T_-(r)\)
analogously using the face \(x=-1\).  Set

\[
 c_+=\frac23-\varepsilon(\kappa_1+3\kappa_3),
 \qquad
 c_-=\frac23-\varepsilon(\kappa_1+7\kappa_3).
\tag{4.1}
\]

Uniformly on \(U\), the directed certificate gives

\[
 c_+\ge
 0.4766666666658666666666666666666666666666666666649547831,
\tag{4.2}
\]

and

\[
 c_-\ge
 0.2766666666650666666666666666666666666666666666645611784.
\tag{4.3}
\]

> **Theorem 4.1 (exact reset-family first-hit threshold).**  For every gain
> pair in \(U\),
> \[
> \begin{array}{ll}
> 0<r<1:&0<T_+(r)\le c_+^{-1}\log(1/r),\\[1mm]
> -1<r<0:&0<T_-(r)\le c_-^{-1}\log(1/|r|).
> \end{array}
> \tag{4.4}
> \]
> Before its first hit, the positive solution is strictly increasing and
> remains in \((0,1)\); the negative solution is strictly decreasing and
> remains in \((-1,0)\).  The operational first-hit threshold on the reset
> family is therefore exactly \(r_c=0\), uniformly on \(U\).

**Proof.** Suppose first that \(0<x\le1\) and that every delayed value
\(y\) lies in \([0,x]\).  Then

\[
 x-\frac{x^3}{3}\ge\frac23x,
 \qquad 0\le x-y\le x,
\tag{4.5}
\]

and

\[
 0\le(x-1)^3-(y-1)^3
 \le(x-1)^3+1=x(x^2-3x+3)\le3x.
\tag{4.6}
\]

Equation (2.1) therefore gives \(\dot x\ge c_+x>0\).  Starting from the
constant history, a maximal-interval argument preserves the assumed ordering:
monotonicity implies \(0\le x(t-\tau_j)\le x(t)\) until the first hit.
Gronwall's inequality then gives \(x(t)\ge re^{c_+t}\), proving the first
line of (4.4).

For the negative channel, write \(u=-x\).  If \(-1\le x\le y\le0\), then

\[
 0\le y-x\le u,
 \qquad
 0\le(y-1)^3-(x-1)^3
 \le(1+u)^3-1=u(u^2+3u+3)\le7u.
\tag{4.7}
\]

It follows that \(\dot u\ge c_-u>0\).  The same maximal-interval argument
and \(u(t)\ge|r|e^{c_-t}\) prove the second line. \(\square\)

The word *threshold* in Theorem 4.1 refers only to the declared detector:
which of \(x=+1\) and \(x=-1\) is reached first.  The theorem stops at that
face and proves no subsequent pulse, quiet passage, basin capture, or
no-return property.

## 5. Size-uniform transverse variational decay

Let

\[
 q=(\mathbf1_{C_1},-\mathbf1_{C_2})^T,
\tag{5.1}
\]

and let \(W_a\) be the zero-sum subspace supported on \(C_a\).  Directly from
(1.2),

\[
\begin{array}{c|cc}
 &B_0&B_1\\ \hline
 \mathbf1&\frac12\mathbf1&\frac12\mathbf1\\
 q&\frac12q&-\frac12q\\
 W_1\oplus W_2&0&0.
\end{array}
\tag{5.2}
\]

Thus the collective, module-difference, and within-module spaces form an
exact invariant decomposition for the variational RFDE.  The common clamp
input has no transverse component by (1.10).

Along a synchronous decision trajectory in \([-1,1]\), put

\[
 C_*=\kappa_1+12\kappa_3.
\tag{5.3}
\]

Indeed, both the current and delayed cubic derivatives obey
\(3(x-1)^2\le12\) on this interval.  For a module-difference perturbation
\((p,q_r)q\), the exact variational equation is

\[
\begin{aligned}
 \dot p={}&[1-x(t)^2-D-\varepsilon c(t)]p-q_r\\
 &+\frac\varepsilon2
 \{c_0(t)p(t-\tau_0)-c_1(t)p(t-\tau_1)\},\\
 \dot q_r={}&\varepsilon p-Eq_r,
\end{aligned}
\tag{5.4}
\]

where \(0<c(t),c_j(t)\le C_*\).  Within-module modes satisfy (5.4) with
the delayed line removed.

For \(Z=|p|+\rho|q_r|\), \(\rho=1\), define

\[
 \alpha_\perp
 =\min\{D-1-\varepsilon(C_*+\rho),E-\rho^{-1}\},
 \qquad
 \beta_\perp=\varepsilon C_*.
\tag{5.5}
\]

The upper right Dini derivative satisfies

\[
 D^+Z(t)\le-\alpha_\perp Z(t)
 +\beta_\perp\sup_{t-\tau_*\le s\le t}Z(s).
\tag{5.6}
\]

The directed bounds are

\[
\begin{aligned}
 C_*&\le
 3.200000000013000000000000000000000000000000000011818582,\\
 \alpha_\perp&\ge
 0.9999999999999999999999999999999999999999999999993157722,\\
 \beta_\perp&\le
 0.6400000000026000000000000000000000000000000000029110986,\\
 \alpha_\perp-\beta_\perp&\ge
 0.3599999999973999999999999999999999999999999999974310153.
\end{aligned}
\tag{5.7}
\]

> **Theorem 5.1 (decision-stage transverse variational stability).**  For
> arbitrary positive module sizes \(n_1,n_2\), every module-difference and
> within-module variational solution along either synchronous first-hit
> channel decays exponentially until that channel reaches its detector face.
> The estimate is uniform in \(n_1,n_2\).  A certified decay-rate lower bound
> is \(\lambda_0=0.03\).

**Proof.** Inequality (5.6) and the strict margin in (5.7) give Halanay's
inequality.  The candidate rate is accepted because directed arithmetic gives

\[
 \alpha_\perp-\lambda_0
 -\beta_\perp e^{\lambda_0\tau_*}
 \ge
 0.07495108269966745042958921253309012629192168572188775416>0.
\tag{5.8}
\]

The identities (5.2) make the scalar estimates independent of their
multiplicities.  Module averaging has norm one and the associated projections
have bounds independent of \(n_1,n_2\), so the same is true after returning to
the nodewise history norm. \(\square\)

Theorem 5.1 is a linear variational statement.  It does not provide a
quantified tube of nonsynchronous histories whose nonlinear solutions remain
near a synchronous channel or hit the same face.

## 6. The controlled complete-history stable manifold

> **Theorem 6.1 (local codimension-one controlled separator).**  Fix a gain
> pair in \(U\).  In the controlled history leaf \(\mathcal X_{\rm cl}\), the
> equilibrium \(\Phi_0\) has a one-dimensional unstable spectral subspace and
> no center spectrum.  It therefore possesses a local \(C^1\) stable manifold
> \(W^s_{\rm loc}(\Phi_0)\) of codimension one in
> \(\mathcal X_{\rm cl}\).  The reset curve \(r\mapsto\Phi_r\) meets this
> manifold transversely at \(r=0\), and this is its only intersection in a
> sufficiently small reset interval.

**Proof.** Theorem 3.1 gives one simple unstable collective root and excludes
collective center roots.  At \(x=0\), Theorem 5.1 places the entire transverse
evolution strictly in the stable half-plane.  These subspaces exhaust the
linearization on the clamped leaf by (5.2).  The polynomial RFDE vector field
is smooth, so the RFDE stable-manifold theorem supplies the asserted local
manifold.  The projection bound (3.9) proves transversality of the reset curve;
the local uniqueness of its intersection follows from the implicit-function
theorem. \(\square\)

This is a complete-history codimension-one separator in the **controlled
clamped phase space**.  It is not a stable manifold of the unforced plant.  No
uniform radius for this manifold, no nonlinear noisy-history capture tube, and
no physical clamp-error tolerance are asserted.

## 7. Consequence for the ideal three-output protocol

Let

\[
 P_{\rm per}(b)=
 \bigl(T(b)^{-1},(V_{\max}(b)-V_{\min}(b))^2\bigr)
\tag{7.1}
\]

be the validated synchronous periodic response with the decision controller
off.  Theorem 4.1 gives the exact operational threshold \(r_c(b)=0\).  Hence
the staged ideal-protocol response is

\[
 \mathcal Q_{\rm op}(b,r)=(P_{\rm per}(b),-r),
 \qquad
 D\mathcal Q_{\rm op}=\operatorname{diag}(DP_{\rm per},-1).
\tag{7.2}
\]

Combining (7.2) with the
[direct periodic target-ball theorem](paper-iv-direct-response-target-ball.md)
gives a closed three-output ball. The independent executable composition is
[the three-output certificate](../src/canard_control/fhn_same_model_three_output.py),
with [driver](../experiments/fhn_same_model_three_output.py) and
[tracked result](../experiments/results/fhn_same_model_three_output.json).
The result digest is

~~~text
afc03431d61d86c6bda8b56a73bdeea76b357e9a31a4a843d9f55cebbf666532
~~~

For the fixed matrix

\[
 M_0=\operatorname{diag}(B_0,-1),
\tag{7.3}
\]

the singular lower bound is still \(s_0\), while the full derivative defect
is exactly the two-output defect \(r_B\). Thus the three-dimensional
Euclidean input ball of radius \(10^{-12}\) about \((b_c,0)\) covers a
closed output ball of radius at least

\[
 1.62187273782174089504757331762715967009378618047942197
 \times10^{-14}
\tag{7.4}
\]

about \((P_{\rm per}(b_c),0)\). Every target in that ball has a unique
preimage in the certified input ball. This theorem concerns frequency,
squared voltage range, and the ideal operational first-hit margin. It does
not turn (7.4) into an unsquared-amplitude or biological pulse-safety ball.

## 8. Claim ledger

| Statement | Status |
|---|---|
| Same dual-scaffold plant and microscopic gain box as the synchronous periodic response | **Proved; \(D=3,E=2\) are fixed here and vanish on synchrony** |
| Exact common-input clamp on \(\pi^Tw=0\) | **Proved by (1.7)--(1.10)** |
| Constant complete-history reset and exact zero equilibrium | **Proved** |
| One simple collective right-half-plane root and no imaginary root | **Proved by Theorem 3.1** |
| Nonzero constant-reset unstable projection | **Proved by (3.6)--(3.9)** |
| Positive/negative \(\pm1\) first-hit classification | **Proved by Theorem 4.1** |
| Local complete-history stable manifold | **Proved only in the controlled clamped leaf** |
| Arbitrary \(n_1,n_2\) transverse decay | **Proved for the linear variational RFDE on the fixed rank-one two-module topology** |
| Ideal three-output frequency--squared-range--operational-margin ball | **Proved and source-bound by the staged certificate (7.4)** |
| Nonlinear or noisy nonsynchronous history capture | **Not proved** |
| Finite-duration pulse realization, clamp error, or hardware containment | **Not proved** |
| Pulse/quiet basin capture or no return after the \(\pm1\) faces | **Not proved** |
| Unforced onset or maximal-canard onset | **Not asserted** |
| Attraction of the baseline periodic orbit | **Not proved** |
| Full-network transverse variational stability along the periodic orbit | **Proved downstream for this fixed rank-one family; it does not imply attraction** |
| General network topology | **Not proved; only the rank-one two-module family with arbitrary module sizes** |
| Closure of issue 15 | **No** |
