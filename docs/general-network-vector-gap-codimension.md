# Vector complete-history gaps and canard codimension

Status: **abstract Lyapunov--Schmidt theorem proved below; network
identification open.**  This note gives the correct replacement for a scalar
canard root when a delayed fast--slow network has more than one matching
obstruction.  It does not determine the obstruction dimension of a proposed
node model, construct its selected histories, or prove that a zero of the
abstract gap is a physical pulse threshold.

The result is deliberately independent of a particular coordinate
projection.  The gap takes values in the cokernel of the complete-history
matching operator.  Consequently its dimension is invariant under changing
the nondegenerate Lin coordinates.

## 1. Fredholm matching data

Let \(X,Y\) be real Banach spaces, let \(U=\mathbb R^m\) be an actuator or
unfolding space, and let \(\mathfrak R\) be a Banach space of admissible
network perturbations.  Consider

\[
 \mathcal F:X\times U\times\mathfrak R\longrightarrow Y,
 \qquad \mathcal F(0,0,0)=0,
 \tag{1.1}
\]

of class \(C^2\) on a neighborhood of the origin.  In an RFDE Lin problem,
\(X\) contains the two orbit pieces, phase variables, and every freely
matched endpoint fiber; \(Y\) contains the differential residuals, phase
condition, and the full-history endpoint jump.  The endpoint spaces must be
chosen before the following index is computed.

Put

\[
 L=D_x\mathcal F(0,0,0).
\]

Assume:

1. \(L\) is injective and Fredholm of index \(-q\), with \(q\ge1\);
2. there is a bounded surjection
   \(\Psi:Y\to\mathbb R^q\) satisfying
   \(\ker\Psi=\operatorname{Ran}L\);
3. there is a bounded injection
   \(E:\mathbb R^q\to Y\) with \(\Psi E=I_q\);
4. \(L:X\to\ker\Psi\) has bounded inverse \(G\).

The phase condition has already removed the time-translation kernel.  Thus
the index is \(-q\), not zero.  Adding \(q\) Lin jump variables, or \(q\)
independent unfolding parameters with a nonsingular response, produces an
index-zero augmented problem.

Define

\[
 P=I_Y-E\Psi.
 \tag{1.2}
\]

Then \(P^2=P\), \(\operatorname{Ran}P=\operatorname{Ran}L\), and
\(PE=0\).  No Hilbert-space orthogonality is required.

## 2. Intrinsic vector gap

### Theorem 2.1 (complete-history Lyapunov--Schmidt gap)

Under the hypotheses of Section 1, there are neighborhoods
\(\mathcal U\subset U\times\mathfrak R\) and \(\mathcal V\subset X\), and a
unique \(C^2\) map

\[
 x_*:\mathcal U\longrightarrow\mathcal V,
 \qquad x_*(0,0)=0,
 \tag{2.1}
\]

such that

\[
 P\mathcal F(x_*(u,\mathcal R),u,\mathcal R)=0.
 \tag{2.2}
\]

The vector Lin gap

\[
 d(u,\mathcal R)
 =\Psi\mathcal F(x_*(u,\mathcal R),u,\mathcal R)
 \in\mathbb R^q
 \tag{2.3}
\]

is \(C^2\), and

\[
 \mathcal F(x,u,\mathcal R)=0
 \quad\Longleftrightarrow\quad
 x=x_*(u,\mathcal R),\quad d(u,\mathcal R)=0
 \tag{2.4}
\]

on these neighborhoods.  At the reference point,

\[
 \begin{aligned}
 D_px_*[h]&=-G P D_p\mathcal F[h],\\
 D_pd[h]&=\Psi D_p\mathcal F[h],
 \end{aligned}
 \qquad p=(u,\mathcal R).
 \tag{2.5}
\]

#### Proof

The derivative with respect to \(x\) of the left-hand side of (2.2) is
\(PL=L:X\to\operatorname{Ran}L\), a bounded isomorphism.  The Banach-space
implicit-function theorem gives (2.1)--(2.2) and uniqueness.  Since

\[
 \mathcal F=P\mathcal F+E\Psi\mathcal F,
\]

(2.4) follows from (2.2), the injectivity of \(E\), and uniqueness of the
range solve.  Differentiating (2.2) gives the first identity in (2.5).
Differentiating (2.3) and using \(\Psi L=0\) gives the second. \(\square\)

The formula \(D_pd=\Psi D_p\mathcal F\) is a reference-point identity.  Away
from the reference point, variations of the selected histories, endpoint
maps, and cokernel coordinates enter the full chain rule.  They must not be
discarded when computing a topology coefficient.

### Coordinate invariance

If \(\widetilde\Psi=J\Psi\) for \(J\in GL(q)\), choose the compatible
cokernel complement \(\widetilde E=EJ^{-1}\).  Then
\(\widetilde E\widetilde\Psi=E\Psi\), so the range projection \(P\), the
range solution \(x_*\), and the gap satisfy
\(\widetilde d=Jd\).  With an arbitrary new complement, this literal
identity need not hold, but the zero set and its codimension are still
intrinsic because both Lyapunov--Schmidt systems are locally equivalent to
\(\mathcal F=0\).
A scalar projection of \(d\) is equivalent to full matching only when
\(q=1\) and that projection is nonzero on the cokernel.

## 3. Canard locus and actuator count

Let

\[
 A=D_ud(0,0):\mathbb R^m\longrightarrow\mathbb R^q,
 \qquad
 B=D_{\mathcal R}d(0,0):\mathfrak R\longrightarrow\mathbb R^q.
 \tag{3.1}
\]

### Theorem 3.1 (codimension and structural response)

Suppose \(A\) is surjective.  Choose a complement
\(\mathbb R^m=K\oplus U_1\), where \(K=\ker A\), such that
\(A_1=A|_{U_1}:U_1\to\mathbb R^q\) is an isomorphism.  Then the local
complete-history canard set is a \(C^2\) graph

\[
 u=k+\varphi(k,\mathcal R),
 \qquad k\in K,
 \tag{3.2}
\]

with \(\varphi(0,0)=0\), and

\[
 D_{\mathcal R}\varphi(0,0)[\mathcal R]
 =-A_1^{-1}B[\mathcal R].
 \tag{3.3}
\]

Thus the canard locus has codimension \(q\) in actuator space.  If \(m=q\),
the root is locally unique and

\[
 u_c(\mathcal R)-u_c(0)
 =-A^{-1}B[\mathcal R]+O(\|\mathcal R\|^2).
 \tag{3.4}
\]

#### Proof

Apply the finite-dimensional implicit-function theorem to
\((s,k,\mathcal R)\mapsto d(k+s,\mathcal R)\), with \(s\in U_1\).  Its
\(s\)-derivative is \(A_1\).  Differentiation gives (3.3); Taylor's theorem
gives (3.4). \(\square\)

### Corollary 3.2 (robust actuator-count obstruction)

Local robust correction of every small cokernel mismatch requires
\(D_ud\) to be surjective and therefore requires \(m\ge q\).  If \(m<q\),
no \(C^1\) actuator law can provide a local right inverse for all mismatch
directions.

This is a differential robustness obstruction, not a claim that a particular
underactuated system has no isolated canard.  A derivative of deficient rank
at one point does not by itself preclude nonlinear solvability.

## 4. Quantitative square case

For a usable network theorem, the inverse radius must be explicit.  Suppose
\(m=q\), \(A\) is invertible, and on
\(\|u\|\le r_u,\|\mathcal R\|\le r_R\),

\[
 \|D_ud-A\|\le\frac1{2\|A^{-1}\|},
 \qquad
 \|D_{\mathcal R}d\|\le M_R,
 \qquad
 \|D^2d\|\le M_2.
 \tag{4.1}
\]

If

\[
 2\|A^{-1}\|M_Rr_R\le r_u
 \tag{4.2}
\]

define the frozen-derivative Newton map

\[
 T_{\mathcal R}(u)=u-A^{-1}d(u,\mathcal R).
 \tag{4.2a}
\]

Assume, in addition to (4.2), that \(T_{\mathcal R}\) maps the displayed
\(u\)-ball into itself.  The first bound in (4.1) makes it a contraction
there, with Lipschitz constant at most \(1/2\).  Hence
\(d(u,\mathcal R)=0\) has one root there and

\[
 \begin{aligned}
 \|u_c(\mathcal R)\|
 &\le2\|A^{-1}\|M_R\|\mathcal R\|,\\
 \|u_c(\mathcal R)+A^{-1}B[\mathcal R]\|
 &\le
 \frac{M_2}{2}\|A^{-1}\|
 \bigl(1+2\|A^{-1}\|M_R\bigr)^2
 \|\mathcal R\|^2.
 \end{aligned}
 \tag{4.3}
\]

The second line displays the powers of the simple-root inverse explicitly;
they cannot be compressed to one factor \(\|A^{-1}\|\).

## 5. Consequences for delayed fast--slow networks

1. A network with one critical fold mode does not automatically have a
   scalar canard threshold.  The complete-history endpoint problem must
   have \(q=1\) after phase and every free endpoint fiber has been counted.
2. If independent recovery directions remain center-like in the singular
   limit, \(q\) must be computed from the full selected-history problem.  It
   may grow with network size.  Projecting the jump onto one observable then
   defines only an output event, not a maximal canard.
3. A shared slow resource, or a proved uniformly contracting transverse
   recovery bundle, is a natural one-gap class.  Standard nodewise recovery
   networks require the vector-gap analysis unless their extra slow
   directions are eliminated by a justified reduction; the actual value of
   \(q\), including the possibility \(q=1\), must be computed from the
   selected-history problem.
4. In the vector case, a topology response is a matrix-valued functional
   \(B:\mathfrak R\to\mathbb R^q\), and its direct, transverse-resolvent,
   trace, history, and endpoint pieces must all be retained.
5. A pulse detector is an additional global event map.  Even when \(d=0\)
   is a physical maximal canard, a pulse threshold requires a separate
   entry--exit--return theorem.

## 6. Paper II obligations

The abstract result above may be invoked only after the following data are
proved with constants uniform in \(N\):

- selected attracting and repelling complete-history slices and a phase
  condition;
- the Fredholm index and cokernel dimension \(q_N\);
- a bounded cokernel map \(\Psi_N\), complement \(E_N\), and range inverse
  \(G_N\);
- the zero-fiber implication making \(d_N=0\) equivalent to intersection of
  the selected slow histories;
- a topology/heterogeneity parameterization differentiable in the declared
  operator topology;
- a rank theorem for \(D_ud_N\), or an explicit statement that the canard
  set has higher codimension;
- at least one nontrivial graph family for which these conditions follow
  from graph and delay-measure hypotheses rather than being assumed.

Classical Lyapunov--Schmidt and Lin theory provide the reduction mechanism.
The proposed new content for Paper II is the singular canard application,
dimension-uniform network estimates, topology-resolved response functional,
and a verifiable nontrivial network class--not the abstract implicit-function
theorem by itself.
