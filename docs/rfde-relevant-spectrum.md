# Relevant characteristic roots of the scaled-delay chart

Status: **proved characteristic-root count, uniform in the declared
parameter box.** The proof also bounds the finite characteristic matrix on
fixed contours. A phase-space Riesz-projector bound and a uniform
complementary Green operator require additional RFDE resolvent estimates and
are not inferred from the root count.

## 1. Linearized characteristic matrix

Linearizing the exact chart at the origin gives

\[
\begin{aligned}
X'&=Y+\delta K\mathcal D_cX
 +\delta^2K\mathcal D_{cz}Z,\\
Y'&=-X,\\
\delta Z'&=-2Z-\delta K\eta\Delta X
 +\delta^2[-W+K(\mathcal D_zZ-\eta\Delta Z)],\\
\delta W'&=Z-D_wW.
\end{aligned}
\tag{1}
\]

For \(e_j(\lambda)=e^{-\lambda\theta_j}\), define

\[
\begin{aligned}
a(\lambda)&=1-\frac13e_0-\frac23e_1,\\
b(\lambda)&=-\frac16+\frac1{12}(e_0+e_1),\\
h(\lambda)&=e_0-e_1,\\
g(\lambda)&=-b-\eta h.
\end{aligned}
\tag{2}
\]

After multiplying the last two characteristic rows by \(\delta\), which
does not change roots for \(\delta>0\), the matrix is

\[
\mathcal M_{\delta,\eta}(\lambda)=
\begin{pmatrix}
\lambda-\delta Ka&-1&-\delta^2Kb&0\\
1&\lambda&0&0\\
\delta K\eta h&0&
2+\delta\lambda-\delta^2Kg&\delta^2\\
0&0&-1&D_w+\delta\lambda
\end{pmatrix}.
\tag{3}
\]

## 2. Uniform root-count proposition

**Proposition 1.** Fix

\[
 K\in\mathbb R\setminus\{0\},\quad D_w>0,\quad
 0<\theta_0<\theta_1,\quad |\eta|\leq\bar\eta.
\]

There are \(\delta_0>0\) and \(\gamma=1/4\) such that, for every
\(0<\delta\leq\delta_0\):

1. the half-plane \(\Re\lambda\geq-\gamma\) contains exactly two
   characteristic roots, counted with algebraic multiplicity;
2. one root lies in \(B_{1/8}(i)\), the other in \(B_{1/8}(-i)\), and both
   are simple;
3. every other characteristic root satisfies
   \(\Re\lambda<-\gamma\).

All statements are uniform for \(|\eta|\leq\bar\eta\).

### Proof

Put

\[
 E_\gamma=e^{\gamma\theta_1},\qquad
 A_\gamma=1+E_\gamma,\qquad
 B_\gamma=\frac{1+E_\gamma}{6},
\]

\[
 H_\gamma=2E_\gamma,\qquad
 G_\gamma=B_\gamma+\bar\eta H_\gamma.
\tag{4}
\]

On \(\Re\lambda\geq-\gamma\),

\[
 |a|\leq A_\gamma,\quad |b|\leq B_\gamma,
 \quad |h|\leq H_\gamma,\quad |g|\leq G_\gamma.
\tag{5}
\]

Split (3) into critical and stable \(2\times2\) blocks. The stable block is

\[
 S=\begin{pmatrix}
 2+\delta\lambda-\delta^2Kg&\delta^2\\
 -1&D_w+\delta\lambda
 \end{pmatrix}.
\tag{6}
\]

Set \(A_0=2+\delta\lambda\) and \(D_0=D_w+\delta\lambda\). If

\[
 \delta\gamma\leq\min\{1,D_w/2\},
\]

then \(|A_0|\geq1\) and \(|D_0|\geq D_w/2\) throughout the half-plane.
Since

\[
 \det S=A_0D_0+\delta^2(1-KgD_0),
\]

we have

\[
 \frac{|\det S-A_0D_0|}{|A_0D_0|}
 \leq\delta^2\left(\frac2{D_w}+|K|G_\gamma\right).
\tag{7}
\]

Choose \(\delta_0\) so that the right-hand side is at most \(1/2\). Then

\[
 |\det S|\geq\frac12|A_0D_0|>0,
 \qquad
 \left|\frac{D_0}{\det S}\right|\leq2.
\tag{8}
\]

These estimates hold for arbitrarily large imaginary part; in particular,
they do not discard high-frequency delay roots.

The Schur complement gives

\[
 \det\mathcal M=(\det S)q_{\delta,\eta}(\lambda),
\]

where

\[
 q_{\delta,\eta}(\lambda)=
 \lambda^2+1-\delta K\lambda a
 +\delta^3K^2\eta\lambda bh\frac{D_0}{\det S}.
\tag{9}
\]

Consequently,

\[
 |q_{\delta,\eta}(\lambda)-(\lambda^2+1)|
 \leq p_\delta|\lambda|,
\tag{10}
\]

with

\[
 p_\delta=\delta |K|A_\gamma
 +2\delta^3K^2\bar\eta B_\gamma H_\gamma.
\tag{11}
\]

On the vertical line \(\lambda=-\gamma+iy\), the elementary estimate

\[
 |\lambda^2+1|=|\lambda-i|\,|\lambda+i|
 \geq\frac\gamma{\sqrt2}(1+|\lambda|)
\tag{12}
\]

holds for \(\gamma=1/4\). Choose \(\delta_0\) smaller so that

\[
 p_{\delta_0}<\frac\gamma{2\sqrt2}.
\tag{13}
\]

On \(|\lambda|=2\), we have \(|\lambda^2+1|\geq3\). Requiring also
\(p_{\delta_0}<3/4\) gives the strict Rouché inequality on the boundary of

\[
 \Omega=\{\Re\lambda>-\gamma,\ |\lambda|<2\}.
\]

Thus \(q_{\delta,\eta}\) and \(\lambda^2+1\) have the same number of roots
in \(\Omega\), namely two. For \(|\lambda|\geq2\),

\[
 |\lambda^2+1|\geq|\lambda|^2-1
 >p_\delta|\lambda|,
\]

so there are no additional roots in the remainder of the half-plane.

Finally set \(\rho=1/8\). On \(|\lambda-i|=\rho\),

\[
 |\lambda^2+1|\geq\rho(2-\rho),\qquad
 |q_{\delta,\eta}-(\lambda^2+1)|
 \leq(1+\rho)p_\delta.
\]

Requiring

\[
 (1+\rho)p_{\delta_0}<\frac12\rho(2-\rho)
\tag{14}
\]

shows that the disk contains one root counted with multiplicity. The same
argument applies at \(-i\). Each root therefore has algebraic multiplicity
one. This proves the proposition. \(\square\)

An explicit admissible choice is any \(\delta_0\leq1\) satisfying (7),
(13), (14), and
\(\delta_0\gamma\leq\min\{1,D_w/2\}\).

## 3. First root expansion

Substitution into (9), followed by the simple-root expansion, gives

\[
 \lambda_\pm=\pm i+
 \frac{\delta K}{2}\left(
 1-\frac13e^{\mp i\theta_0}
 -\frac23e^{\mp i\theta_1}
 \right)+O(\delta^2),
\tag{15}
\]

uniformly in \(\eta\). The layer-redistribution parameter first enters this
frozen characteristic equation at order \(\delta^3\).

## 4. Characteristic residues and the remaining phase-space issue

On the two fixed circles
\(\Gamma_\pm=\{|\lambda\mp i|=1/8\}\), (8), (9), and (14) give a uniform
bound for \(\mathcal M^{-1}\). Restoring the two rows divided by \(\delta\)
multiplies on the right by
\(\operatorname{diag}(1,1,\delta,\delta)\), whose norm is at most one. Thus
the finite characteristic-matrix residues on these contours are uniformly
bounded.

This is an input to, but not yet a proof of, a phase-space Riesz-projector
bound. That conclusion requires writing the RFDE generator resolvent formula
and separately controlling its history-to-current-state integral and delayed
evaluation terms on \(C([ -\theta_1,0],\mathbb R^4)\).

Even after that projector step, one would not yet have a uniform semigroup
dichotomy. Eventual
compactness at each fixed \(\delta\) does not by itself control the constants
as \(\delta\to0\). In particular, Proposition 1 does not prove a uniform
right inverse for the nonautonomous variational operator along the canard.
That stronger object would require either a uniform generator-resolvent
bound on a complete vertical line, a method-of-steps contraction estimate,
or a direct Lyapunov--Perron construction.

The special-flow graph theorem in
[special-flow-graph-theorem.md](special-flow-graph-theorem.md) uses the last
option and therefore does not assume this missing implication.
