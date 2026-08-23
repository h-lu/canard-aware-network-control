# Directed validation of the center periodic RFDE orbit

Status: **proved at the single declared center parameter.** A directed
finite/tail radii argument validates a periodic orbit of the synchronous
two-delay FHN RFDE within \(10^{-7}\) of the 97-node Fourier candidate and
validates its phase-bordered RFDE derivative. This is not yet the parameter
box required by [issue 15](https://github.com/h-lu/canard-aware-network-control/issues/15).
No claim is made here about full Floquet hyperbolicity, extrema throughout a
box, or the frequency--amplitude response matrix.

The implementation and tracked result are
[fhn_periodic_infinite_validation.py](../src/canard_control/fhn_periodic_infinite_validation.py),
[fhn_periodic_infinite_validation.py](../experiments/fhn_periodic_infinite_validation.py),
and
[fhn_periodic_infinite_validation.json](../experiments/results/fhn_periodic_infinite_validation.json).
The arithmetic backend is the MPFR-directed package described in
[paper-iv-directed-periodic-validation.md](paper-iv-directed-periodic-validation.md).

## 1. Coefficient equation and norm

For \(x=(v,w,T)\), let \(\mathcal F(x)\) be the phase-bordered Fourier
coefficient equation of the normalized periodic RFDE. Its fast component is

\[
 2\pi ikv_k-T\left[
 v-\frac{v^3}{3}-w-\varepsilon\kappa _1v
 -\varepsilon\kappa _3(v-1)^3
 +\sum_{j=0}^1 S_j(T)H(v)\right]_k,
\tag{1.1}
\]

where

\[
 H(v)=\frac{\varepsilon\kappa _1}{2}v+
       \frac{\varepsilon\kappa _3}{2}(v-1)^3,
\qquad
 (S_j(T)a)_k=e^{-2\pi ik\tau_j/T}a_k.
\tag{1.2}
\]

The slow component is
\(2\pi ikw_k-T\varepsilon(v-a)_k\). The proof is carried out only on the
real-conjugate space

\[
 \mathcal X^0_{\mathbb R}=\{(v,w,T):v_{-k}=\overline{v_k},\qquad
 w_{-k}=\overline{w_k},\qquad T\in\mathbb R\}
\]

of the component Wiener algebra, with

\[
 \|x\|_\square=
 \sum_k\bigl(
 |\Re v_k|+|\Im v_k|+|\Re w_k|+|\Im w_k|
 \bigr)+|T|.
\tag{1.3}
\]

The Fourier derivative domain is

\[
 \mathcal X^1_{\mathbb R}=
 \left\{x\in\mathcal X^0_{\mathbb R}:
 \sum_k |k|\bigl(|\Re v_k|+|\Im v_k|
                  +|\Re w_k|+|\Im w_k|\bigr)<\infty\right\}.
\tag{1.4}
\]

The residual space \(\mathcal Y^0_{\mathbb R}\) has the same unweighted
state coefficient norm and one real phase scalar. Thus
\(D\mathcal F(x):\mathcal X^1_{\mathbb R}\to
\mathcal Y^0_{\mathbb R}\) is an unbounded phase-bordered operator when its
domain is viewed inside \(\mathcal X^0_{\mathbb R}\).

This norm is deliberately unweighted. Complex multiplication is
submultiplicative in the component norm, while a delay rotation has norm at
most \(\sqrt2\). No complex-period extension is used: such an extension
would not give a bounded delay shift on the unweighted Fourier tail.

## 2. De-aliased finite block and tail inverse

The candidate has half-bandwidth \(48\); its cubic residual therefore has
support through \(M=144\). We project onto \(|k|\le M\) without modular
convolution. For each state, use the independent real coordinates

\[
 q=(c_0,\Re c_1,\Im c_1,\ldots,\Re c_M,\Im c_M),
\tag{2.1}
\]

and let \(E\) insert \(c_{-k}=\overline{c_k}\), while \(R\) restricts a
conjugate sequence to (2.1). Thus \(RE=I\). Let \(W\) put weight one on
the zero modes, period and phase, and weight two on every positive-mode real
or imaginary coordinate. Then

\[
 \|EW^{-1}y\|_\square=\|y\|_1.
\tag{2.2}
\]

The certified finite matrix is

\[
 J_{PP}^{\mathbb R}=W R P D\mathcal F(\bar x)P E W^{-1}.
\tag{2.3}
\]

It has real dimension \(4M+3=579\). The former \(1158\)-dimensional
ambient complex realification is not used. Let \(A_P\) be the stored
binary64 inverse of the interval midpoint of (2.3), and set

\[
 (A_Qy)_k=(2\pi ik)^{-1}y_k,\qquad |k|>M.
\tag{2.4}
\]

The real vector field, real delays and real phase condition commute with
Fourier conjugation. Hence \(\mathcal F(\mathcal X^1_{\mathbb R})\) lies in
\(\mathcal Y^0_{\mathbb R}\), and its
derivative lies in the same real subspace. The finite preconditioner is
defined through the independent coordinates above, and \(A_Q\) also
preserves conjugacy. Consequently \(A\) and the Newton map are closed on
\(\mathcal X^0_{\mathbb R}\); the proof never varies \(T\) in a complex
direction.

The binary matrix is used only as an accelerator. IEEE round-to-nearest is
checked and the exact product of its stored entries is bounded by the same
Higham plus smallest-normal correction used in the finite-stage note.
Directed bounds give

\[
\begin{aligned}
 \|A_P\|_1&\le19.35094416123991,\\
 \|I-A_PJ_{PP}^{\mathbb R}\|_1
 &\le1.212320634690941\times10^{-9},\\
 \|A\mathcal F(\bar x)\|_\square
 &\le2.385974762791979\times10^{-8}.
\end{aligned}
\tag{2.5}
\]

All four block columns of \(I-A D\mathcal F(\bar x)\) are then bounded:

\[
\begin{array}{c|cc}
 &\text{finite output}&\text{tail output}\\ \hline
\text{finite input}
 &1.212320634690941\times10^{-9}
 &0.04291456063102587\\
\text{tail input}
 &0.04541143431800499
 &0.1269956172053809 .
\end{array}
\tag{2.6}
\]

The induced column bound is therefore

\[
 Z_0\le
 \max\{0.04291456184334650,\,
       0.1724070515233859\}
 =0.1724070515233859<1.
\tag{2.7}
\]

Unlike the earlier nodal inverse, (2.6) is a de-aliased coefficient-space
finite/tail estimate.

## 3. Moving delays on the correction ball

The map \(T\mapsto S_j(T)\) is not continuous in operator norm on an
unweighted Wiener space: its formal derivative contains \(k\). A naive
Wiener Lipschitz assertion would therefore invalidate the proof.

The preconditioned derivative is nevertheless bounded. On finite output
modes, \(|k|\le M\). On tail modes, the factor \(k\) is cancelled by
\((2\pi ik)^{-1}\) in (2.4). For \(|T-\bar T|\le r\),

\[
\begin{aligned}
 \|A(S_j(T)-S_j(\bar T))a\|_\square
 &\le C_{S,j}r\|a\|_\square,\\
 \|A S_j(T)Da\|_\square
 &\le C_D\|a\|_\square.
\end{aligned}
\tag{3.1}
\]

Writing every delayed cubic as \(S_j(T)(v-1)^3\) keeps the output mode,
rather than an internal convolution mode, in (3.1). Here are the complete
column majorants used by the computation. This also fixes the meaning of the
three constants below.

Put \(a_P=\|A_P\|_1\), \(\sigma=\sqrt2\),
\(\underline T=\bar T-r_{\max}\),
\(\overline T=\bar T+r_{\max}\), and let \(\bar T_-\) be the directed lower
endpoint of the stored period. Define

\[
 C_D=\sigma(2\pi M a_P+1),\qquad
 C_{S,j}=\frac{C_D\tau_j}{\underline T^2},\qquad
 C_S=\sum_jC_{S,j}.
\tag{3.2}
\]

All norms in what follows are component Wiener norms. At the candidate set

\[
\begin{gathered}
 V=\|\bar v\|,\quad C=\|\bar v-1\|,\quad
 H=\|H(\bar v)\|,\quad H_D=\|D H(\bar v)\|,\\
 B=\|H_v(\bar v)\|,\qquad L=\|G_v(\bar v)\|,
\end{gathered}
\tag{3.3}
\]

where \(G(v,w)=v-v^3/3-w-\varepsilon\kappa _1v
-\varepsilon\kappa _3(v-1)^3\). The state-column coefficient changes are

\[
\begin{aligned}
 \ell_1&=2(V+3\varepsilon\kappa _3C),
 &\ell_2&=1+3\varepsilon\kappa _3,\\
 b_1&=3\varepsilon\kappa _3C,
 &b_2&=3\varepsilon\kappa _3/2,\\
 B_0&=\max\{L+2\sigma B+\varepsilon,1\}.
\end{aligned}
\tag{3.4}
\]

Thus the state-input columns are bounded coefficientwise by

\[
\begin{aligned}
 S_1&=a_P\{B_0+\overline T(\ell_1+2\sigma b_1)\}
       +\overline T B C_S,\\
 S_2&=a_P\overline T(\ell_2+2\sigma b_2),
 &S_3&=0.
\end{aligned}
\tag{3.5}
\]

For the period column define

\[
\begin{array}{lll}
 g_1=2+\varepsilon\kappa _1+V^2
          +3\varepsilon\kappa _3C^2,
 &g_2=V+3\varepsilon\kappa _3C,
 &g_3=1/3+\varepsilon\kappa _3,\\
 h_1=\varepsilon\kappa _1/2
          +3\varepsilon\kappa _3C^2/2,
 &h_2=3\varepsilon\kappa _3C/2,
 &h_3=\varepsilon\kappa _3/2.
\end{array}
\tag{3.6}
\]

The directed period-column bounds used in the source are

\[
\begin{aligned}
 P_1={}&a_P(g_1+2\sigma h_1)+HC_S+a_P\varepsilon\\
 &+\sum_j\left{
 \frac{a_P\sigma H_D\tau_j}{\underline T\bar T_-}
 +\frac{C_Dh_1\tau_j}{\underline T}
 +\frac{C_{S,j}H_D\tau_j}{\underline T}
 \right},\\
 P_2={}&a_P(g_2+2\sigma h_2)
       +\sum_j\frac{C_Dh_2\tau_j}{\underline T},\\
 P_3={}&a_P(g_3+2\sigma h_3)
       +\sum_j\frac{C_Dh_3\tau_j}{\underline T}.
\end{aligned}
\tag{3.7}
\]

The three reported constants are exactly

\[
 Z_1=\max\{S_1,P_1\},\qquad
 Z_2=\max\{S_2,P_2\},\qquad
 Z_3=P_3.
\tag{3.8}
\]

The terms in (3.7) respectively bound ordinary field variation, the
coefficient \(\tau_j/T\), the change of the delayed field, and the remaining
shift variation in the period column
\(-[G+\sum_jS_jH]-\sum_j(\tau_j/T)S_jDH(v)\). This decomposition never
differentiates the shift as an unpreconditioned Wiener operator.

Wiener convolution now gives, for \(0\leq \rho\leq
r_{\max}=10^{-7}\),

\[
 \|A[D\mathcal F(\bar x+h)-D\mathcal F(\bar x)]\|
 \le Z_1\rho+Z_2\rho^2+Z_3\rho^3,
 \qquad \|h\|_\square\leq\rho,
\tag{3.9}
\]

where

\[
\begin{aligned}
 Z_1&\le24700.52217026439,\\
 Z_2&\le6695.089546241814,\\
 Z_3&\le761.9789765758768.
\end{aligned}
\tag{3.10}
\]

## 4. Infinite radii theorem

At \(r=10^{-7}\), (3.9) is at most
\(0.002470052283977335\). Thus

\[
 q(r):=Z_0+Z_1r+Z_2r^2+Z_3r^3
 \le0.1748771038073633<1
\tag{4.1}
\]

and

\[
\begin{aligned}
 Y+q(r)r
 &\le4.134745800865612\times10^{-8}<r,\\
 r-\{Y+q(r)r\}
 &\ge5.865254199134388\times10^{-8}>0.
\end{aligned}
\tag{4.2}
\]

> **Theorem 4.1 (center periodic RFDE orbit).** At
> \((\varepsilon,a,\Theta_0,\Theta_1,\kappa_1,\kappa_3)
> =(0.2,0.6,4,5,0.2,0.25)\), the synchronous two-delay FHN RFDE has a unique
> phase-fixed periodic solution in the component-Wiener ball of radius
> \(10^{-7}\) about the stored Fourier polynomial. For every point in the
> intersection of that ball with \(\mathcal X^1_{\mathbb R}\), its
> phase-bordered coefficient derivative
> \(\mathcal X^1_{\mathbb R}\to\mathcal Y^0_{\mathbb R}\) is bijective. At
> the validated solution, the inverse has operator norm at most
> \(23.45219633406240\) from \(\mathcal Y^0_{\mathbb R}\) into the base
> \(\mathcal X^0_{\mathbb R}\) norm.

**Proof.** The Newton map \(x\mapsto x-A\mathcal F(x)\) extends continuously
from the Fourier derivative domain to the ball in
\(\mathcal X^0_{\mathbb R}\): on the tail, (2.4) cancels the unbounded
derivative. Equations (4.1)--(4.2) make it a strict self-map and contraction
there. For its fixed point \(x\), the tail component of the fixed-point
identity is

\[
 x_Q=T(2\pi ik)^{-1}[f(x)]_Q.
\tag{4.3}
\]

Here \(f\) denotes the two state fields in (1.1) and the slow equation.
Since \(f(x)\) is in the unweighted Wiener algebra, (4.3) first places
\(x\) in \(\mathcal X^1_{\mathbb R}\). Now \(\mathcal F(x)\) is defined.
The finite defect in (2.5) makes \(A_PJ_{PP}^{\mathbb R}\) invertible and
hence makes \(A_P\) injective; \(A_Q\) is injective coefficientwise.
Therefore \(A\mathcal F(x)=0\) implies \(\mathcal F(x)=0\), and the Fourier
series is a classical periodic RFDE solution.

It remains to justify the unbounded derivative statement. For any point
\(z\) in the ball and in \(\mathcal X^1_{\mathbb R}\), let
\(B_z\) denote the bounded extension of \(A D\mathcal F(z)\) to
\(\mathcal X^0_{\mathbb R}\). The same defect bound gives
\(\|I-B_z\|<1\). Given \(g\in\mathcal Y^0_{\mathbb R}\), set
\(h=B_z^{-1}Ag\). The tail part of \(B_zh=Ag\) has the same form as
(4.3), with \(g\) plus bounded lower-order terms on the right. Hence
\(h\in\mathcal X^1_{\mathbb R}\). It follows that
\(A(D\mathcal F(z)h-g)=0\), so injectivity of \(A\) gives
\(D\mathcal F(z)h=g\). Injectivity follows from invertibility of \(B_z\).
Finally,
\(\|B_z^{-1}A\|_{\mathcal Y^0\to\mathcal X^0}
\leq\|A\|/(1-q(r))\), which gives the stated base-norm bound. \(\square\)

## 5. Boundary and reproduction

The bordered inverse is not relabeled as full Floquet hyperbolicity. A
separate Fredholm-to-monodromy transfer is retained before even calling the
unit multiplier algebraically simple, and multipliers elsewhere on the unit
circle remain unchecked. Unique extrema, parameter continuation, adjoints,
and the \(2\times2\) response box also remain open. Consequently issue 15 is
not closed.

Run from the repository root:

~~~bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_periodic_infinite_validation.py
~~~

The tracked JSON records every finite/tail and radii constant and keeps the
remaining theorem flags false.
