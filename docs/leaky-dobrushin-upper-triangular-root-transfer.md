# Dobrushin root transfer without delay-layer left balance

Status: **proved conditional root-transfer theorem and conditional nonlinear
collective-forcing theorem.**  The scalar leaky complete-history canard root,
an invariant asynchronous strip, physical pulse onset, and two-sided routing
remain open.

## 1. Enlarged directed network class

Let \(Q\ge0\), \(Q\mathbf1=\mathbf1\), and

\[
 \tau(Q)\le\frac12.
\]

Choose a stationary probability vector \(\pi\), so
\(\pi^TQ=\pi^T\) and \(\pi^T\mathbf1=1\).  Zero entries of \(\pi\) are
allowed; no lower bound on \(\pi_{\min}\) is used.  For the two delayed
layers assume only

\[
 B_j\ge0,\qquad B_j\mathbf1=\frac12\mathbf1,qquad j=0,1.       \tag{1.1}
\]

In contrast with the earlier direct-sum theorem, this result does **not**
assume \(\pi^TB_j=\frac12\pi^T\).  Thus the current Markov layer and the
two delayed layers need not possess a common stationary left vector.

The row-mass identity in (1.1) preserves the synchronized scalar RFDE;
nonnegativity supplies, for every complex node vector,

\[
 \operatorname{diam}(B_jz)\le\frac12\operatorname{diam}z.      \tag{1.2}
\]

Subtracting a constant vector does not change diameter.  Therefore the
projection \(P=I-\mathbf1\pi^T\) and (1.2) give the same transverse
Dobrushin--Halanay inequality as in the balanced theorem.  In particular,
on the declared voltage strip,

\[
 \|U_{\perp,N}(t,s)\|_{1/10}\le e^{-(t-s)/10},
 \qquad \|G_{\perp,N}\|\le10.                          \tag{1.3}
\]

The constants in (1.3) are independent of finite \(N\), of \(\pi_{\min}\),
and of the admitted matrices.

## 2. Upper triangular, not direct sum

Write a history as a stationary collective coordinate plus a representative
of the quotient by synchrony,

\[
 x=\mathbf1\bar x+z,qquad \bar x=\pi^Tx,qquad \pi^Tz=0.
\]

Since every current and delayed layer maps \(\mathbf1\) into
\(\operatorname{span}\{\mathbf1\}\), a collective input cannot create a
transverse output.  Lack of left balance can, however, feed a transverse
history into the collective equation.  Consequently the phase-fixed
complete-history Lin operator has the block form

\[
 \mathcal L_N=
 \begin{pmatrix}
  \mathcal L_{\parallel}&C_N\\
  0&\mathcal L_{\perp,N}
 \end{pmatrix}.                                      \tag{2.1}
\]

This distinction is essential: calling (2.1) a direct sum would give an
incorrect full cokernel.

Because \(\mathcal L_{\perp,N}\) is an isomorphism, with inverse
\(G_{\perp,N}\), the bounded codomain row operation

\[
 T_N(y_\parallel,y_\perp)
 =\bigl(y_\parallel-C_NG_{\perp,N}y_\perp,y_\perp\bigr)       \tag{2.2}
\]

satisfies

\[
 T_N\mathcal L_N
 =\mathcal L_\parallel\oplus\mathcal L_{\perp,N}.     \tag{2.3}
\]

Hence (2.1) and the scalar Lin operator have the same Fredholm index, kernel
dimension, and cokernel dimension.  If \(\psi\) spans the scalar cokernel,
the correct full functional is

\[
 \Psi_N(y_\parallel,y_\perp)
 =\psi\bigl(y_\parallel-C_NG_{\perp,N}y_\perp\bigr).  \tag{2.4}
\]

Normalize with the same collective complement
\(e_N=(e_\parallel,0)\), so that
\(\psi(e_\parallel)=\Psi_N(e_N)=1\).
For a collective parameter or inhomogeneity \((g_\parallel,0)\),

\[
 \Psi_N(g_\parallel,0)=\psi(g_\parallel).             \tag{2.5}
\]

Thus a scalar simple complete-history root transfers with exactly the same
location, slope, and orientation.  This is an exact triangular transfer;
it is not a perturbative small-imbalance statement.

## 3. Uniform size of the triangular correction

Define the delay-layer balance defect

\[
 \delta_B=\sum_{j=0}^1\delta_j,qquad
 \delta_j=\frac12
 \left\|\pi^TB_j-\frac12\pi^T\right\|_1.             \tag{3.1}
\]

Both signed rows in (3.1) have zero total mass.  The oscillation duality
bound

\[
 |b^Tz|\le\frac12\|b\|_1\operatorname{diam}z,
 \qquad b^T\mathbf1=0,                                \tag{3.2}
\]

shows \(0\le\delta_B\le1\).  Along the voltage strip, the delayed
linearization coefficient satisfies

\[
 \varepsilon\left(\kappa_1+\frac{75}{4}\kappa_3\right)
 =\frac{391}{20000}.                                  \tag{3.3}
\]

Equations (1.3), (3.2), and (3.3) give the dimension-uniform row-operation
bound

\[
 \|C_NG_{\perp,N}\|
 \le\frac{391}{2000}\delta_B
 \le\frac{391}{2000}.                                \tag{3.4}
\]

Thus the triangular equivalence itself remains uniformly conditioned even
at the largest admissible left-balance defect.  No delayed-history residence
factor appears in (3.4): the complete-line norm takes a supremum over all
times, so a fixed time translation has norm one.  The forward-time
\(L^1\) estimate below is a different calculation because it begins at a
declared initial time.

## 4. Nonlinear synchronization and collective forcing

The nonlinear node-diameter proof uses only row mass and nonnegativity.  Put

\[
 M_0=\sup_{t_0-r\le s\le t_0}M(s),
 \qquad
 \mathcal H_M(t)=\sup_{t-r\le s\le t}M(s).
\]

While the retained solution remains in the voltage strip,

\[
 M(t)\le M_0e^{-(t-t_0)/10}.                           \tag{4.1}
\]

Left imbalance changes the stationary collective equation.  Decomposing

\[
 \pi^TB_j=\frac12\pi^T+b_j^T
\]

separates an imbalance term from the balanced Taylor remainder.  By (3.2),
the delayed linear and cubic imbalance at layer \(j\) is bounded by
\((391/20000)\delta_jM(t-\tau_j)\).  The weighted first-order Taylor
terms in the remaining part still cancel.  Resolving the current and delayed
quadratic terms gives

\[
\begin{aligned}
 |R_{\rm coll}(t)|\le{}&
 \frac{391}{20000}\bigl[
   \delta_0M(t-\tau_0)+\delta_1M(t-\tau_1)\bigr]\\
 &+\frac{1403}{400}M(t)^2
 +\frac3{800}\bigl[M(t-\tau_0)^2+M(t-\tau_1)^2\bigr].
                                                               \tag{4.2}
\end{aligned}
\]

In particular,

\[
 |R_{\rm coll}(t)|
 \le \frac{391}{20000}\delta_B\mathcal H_M(t)
     +\frac{703}{200}\mathcal H_M(t)^2.               \tag{4.3}
\]

The delayed values in (4.2) cannot in general be replaced by the current
\(M(t)\).  For example, the current diameter can vanish at \(t_0\) while
the prescribed retained history has nonzero diameter.

For \(t\in[t_0,t_0+\tau_j]\), the term \(M(t-\tau_j)\) may remain as
large as \(M_0\); afterwards it decays with rate \(1/10\).  Thus

\[
\begin{aligned}
 \int_{t_0}^{\infty}|R_{\rm coll}(t)|\,dt
 \le{}&\frac{391}{20000}
 \bigl[\delta_0(10+4\sqrt5)+\delta_1(10+5\sqrt5)\bigr]M_0\\
 &+\left(\frac{703}{40}+\frac{27\sqrt5}{800}\right)M_0^2.
                                                               \tag{4.4}
\end{aligned}
\]

Equation (4.4) is the sharper bound when \(\delta_0\) and \(\delta_1\)
are known separately.  If only \(\delta_B=\delta_0+\delta_1\) is retained,
the worst case places all imbalance on the longer delay, and

\[
\begin{aligned}
 \int_{t_0}^{\infty}|R_{\rm coll}(t)|\,dt
 \le{}&\frac{391(2+\sqrt5)}{4000}\,\delta_BM_0
     +\frac{56483}{3200}M_0^2.                         \tag{4.5}
\end{aligned}
\]

The balanced theorem is recovered at \(\delta_B=0\).  For nonbalanced
delay layers the proved topology-uniform estimate contains a term linear in
the initial diameter.  Without an additional cancellation, one cannot infer
a purely quadratic enlarged-class estimate from this argument.

## 5. Exact nonbalanced witness

The executable certificate includes

\[
 Q=\begin{pmatrix}1&0\\1/2&1/2\end{pmatrix},\quad
 B_0=\begin{pmatrix}0&1/2\\1/2&0\end{pmatrix},\quad
 B_1=\begin{pmatrix}1/2&0\\1/2&0\end{pmatrix},\quad
 \pi^T=(1,0).
\]

Here \(\tau(Q)=1/2\), \(\pi^TB_0\ne\frac12\pi^T\), and
\((\delta_0,\delta_1,\delta_B)=(1/2,0,1/2)\).  Nevertheless
\(PB_0\mathbf1=0\), while
\(\pi^TB_0P=(-1/2,1/2)\ne0\).  Thus the lower-left block in (2.1) is
exactly zero and the upper-right block is genuinely nonzero.

## 6. Boundary of the theorem

The result removes the common-left-balance assumption from the two fixed,
nonnegative, half-row-mass delay layers.  It does not cover signed coupling,
moving delay atoms, graph families with closing Dobrushin gap, heterogeneous
node vector fields, or an invariant asynchronous strip.  Most importantly,
it transfers a scalar canard root **if that scalar root is proved**; the
scalar leaky root and its equality or relation to physical pulse onset have
not been proved here.

Replay with

```bash
PYTHONPATH=src /usr/bin/python3 \
  experiments/leaky_dobrushin_upper_triangular_transfer.py
```
