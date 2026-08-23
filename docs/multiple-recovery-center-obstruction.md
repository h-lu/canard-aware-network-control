# Independent recoveries create a multiple-center obstruction

## 1. Purpose and claim ledger

This note isolates one concrete question that must be settled before a
scalar Lin gap can be promoted to a general delayed FitzHugh--Nagumo (FHN)
network:

> What is the singular center structure when every node retains its own
> recovery variable?

For a finite voltage-coupled network, the answer is exact.  At the
synchronous fold, the current-state Jacobian has an \((N+1)\)-dimensional
generalized zero eigenspace: one length-two fold chain and \(N-1\)
additional recovery-center eigenvectors.  For positive small
\(\varepsilon\), those extra directions become \(N-1\) characteristic roots
of order \(\varepsilon\).  Weak voltage delays on the canard scale do not
remove that root cluster.

The status of each conclusion is as follows.

| Label | Statement | Status |
|---|---|---|
| C1 | The singular generalized-center dimension is exactly \(N+1\). | Proved in Theorem 2.1. |
| C2 | Its quotient by the fold Jordan plane has dimension \(N-1\). | Proved in Corollary 2.2. |
| C3 | Without delay, \(N-1\) transverse roots are \(O(\varepsilon)\). | Proved in Proposition 3.1. |
| C4 | For weak voltage delays and \(\tau_k=O(\varepsilon^{-1/2})\), the \(N-1\) slow roots persist. | Proved in Theorem 3.2. |
| C5 | A scalar detector cannot have a simple isolated zero in a center-coordinate target of dimension greater than one. | Proved in Lemma 4.1. |
| C6 | If every post-phase center coordinate is an independent endpoint matching condition, then at least \(N\) scalar parameters are necessary for a full-rank local matching map. | Conditional linear-algebra consequence, not an RFDE index theorem. |
| O1 | The selected full-history Lin operator has cokernel dimension \(N\). | **Open; not inferred here.** |
| O2 | A physical pulse family spans all center mismatch coordinates. | **Open; requires a trace/control-rank theorem.** |
| O3 | The relevant outer canard branches exist and meet the selected sections with the claimed dimensions. | **Open; requires RFDE outer geometry.** |

Thus the note proves a model obstruction, not a complete delayed canard
matching theorem.

## 2. Exact singular algebra

### 2.1 The finite delayed FHN network

Let \(v,w\in\mathbb R^N\), let \({\bf 1}=(1,\ldots,1)^\top\), and consider

\[
\begin{aligned}
 \dot v(t)
 &=v(t)-\frac13v(t)^{\odot 3}-w(t)-Lv(t) \\
 &\quad+\varepsilon\sum_{k=1}^{m}
 B_k\bigl(v(t-\tau_k)-v(t)\bigr),\\
 \dot w(t)&=\varepsilon\bigl(v(t)-a{\bf 1}\bigr).
\end{aligned}
\tag{2.1}
\]

Here \(L\) is a possibly directed voltage-coupling Laplacian.  Assume

\[
L{\bf 1}=0,
\qquad
\ker L=\operatorname{span}\{{\bf 1}\},
\qquad
\ker L^2=\ker L,
\qquad
\operatorname{Re}\mu>0
\quad\text{for every }\mu\in\sigma(L)\setminus\{0\}.
\tag{2.2}
\]

The kernel equality says that the zero eigenvalue is semisimple.  In the
usual connected network case it is algebraically simple.  No symmetry or
diagonalizability of the nonzero spectrum is needed below.  The final
spectral inequality makes the nonzero voltage modes strictly stable, so
the generalized zero eigenspace computed below is the complete singular
center space.

At \(a=1\), the synchronous fold equilibrium is

\[
v_*={\bf 1},
\qquad
w_*=\frac23{\bf 1}.
\tag{2.3}
\]

The local cubic has zero voltage derivative there.  At
\(\varepsilon=0\), all delay terms and the recovery equation vanish from
the linearization.  With \(A=-L\), the singular current-state Jacobian is

\[
J_0=
\begin{pmatrix}
A&-I\\
0&0
\end{pmatrix}.
\tag{2.4}
\]

This is the precise source of the multiple-center effect: the \(N\)
recovery variables are frozen independently at the singular limit.

### Theorem 2.1 (exact generalized-center dimension)

Under (2.2),

\[
\ker J_0
=\{(x,Ax):x\in\mathbb R^N\},
\qquad
\dim\ker J_0=N,
\tag{2.5}
\]

and

\[
\ker J_0^2
=\{(x,Ax-b{\bf 1}):x\in\mathbb R^N, b\in\mathbb R\},
\qquad
\dim\ker J_0^2=N+1.
\tag{2.6}
\]

Moreover,

\[
\ker J_0^k=\ker J_0^2,
\qquad k\ge 2.
\tag{2.7}
\]

Consequently, the generalized zero eigenspace of \(J_0\) has dimension
exactly \(N+1\).

#### Proof

For \((x,y)\in\mathbb R^N\times\mathbb R^N\),

\[
J_0(x,y)=(Ax-y,0).
\tag{2.8}
\]

Thus \(J_0(x,y)=0\) if and only if \(y=Ax\), proving (2.5).  A second
application gives

\[
J_0^2(x,y)=\bigl(A(Ax-y),0\bigr).
\tag{2.9}
\]

Because \(\ker A=\operatorname{span}\{{\bf 1}\}\), equation (2.9)
vanishes if and only if \(Ax-y=b{\bf 1}\), which is (2.6).  The map
\((x,b)\mapsto(x,Ax-b{\bf 1})\) is injective, so its image has dimension
\(N+1\).

For \(k\ge2\), membership in \(\ker J_0^k\) is equivalent to

\[
A^{k-1}(Ax-y)=0.
\tag{2.10}
\]

The semisimplicity assumption gives \(\ker A^{k-1}=\ker A\).  Hence
(2.10) is equivalent to (2.9), proving (2.7).  \(\square\)

### Corollary 2.2 (one fold chain plus \(N-1\) recovery centers)

Let \(\ell^\top L=0\) and normalize
\(\ell^\top{\bf 1}=1\).  Set

\[
E_\perp=\ker\ell^\top.
\tag{2.11}
\]

The vectors

\[
e_f=({\bf 1},0),
\qquad
g_f=(0,-{\bf 1})
\tag{2.12}
\]

form a length-two Jordan chain,

\[
J_0e_f=0,
\qquad
J_0g_f=e_f.
\tag{2.13}
\]

For every \(q\in E_\perp\),

\[
k_q=(q,Aq)
\tag{2.14}
\]

is a zero eigenvector.  The map

\[
\Xi:\mathbb R\times\mathbb R\times E_\perp
\longrightarrow\ker J_0^2,
\qquad
\Xi(\alpha,b,q)
=(\alpha{\bf 1}+q,Aq-b{\bf 1})
\tag{2.15}
\]

is an isomorphism.  Therefore

\[
\ker J_0^2
=\operatorname{span}\{e_f,g_f\}
\oplus\{k_q:q\in E_\perp\},
\tag{2.16}
\]

and

\[
\dim\left(\ker J_0^2\big/\operatorname{span}\{e_f,g_f\}\right)=N-1.
\tag{2.17}
\]

The quotient in (2.17) is the exact algebraic recovery-center obstruction.
It is not yet an RFDE Lin cokernel.

## 3. The extra center directions become slow roots

### Proposition 3.1 (no-delay characteristic factorization)

Delete the delayed term in (2.1) and let
\(\mu_1=0,\mu_2,\ldots,\mu_N\) denote the eigenvalues of \(L\), counted
with algebraic multiplicity.  At (2.3), the positive-\(\varepsilon\)
current-state Jacobian is

\[
J_\varepsilon=
\begin{pmatrix}
-L&-I\\
\varepsilon I&0
\end{pmatrix}.
\tag{3.1}
\]

Its characteristic determinant is

\[
\det(\lambda I_{2N}-J_\varepsilon)
=\det(\lambda^2I+\lambda L+\varepsilon I)
=\prod_{j=1}^{N}
\bigl(\lambda^2+\mu_j\lambda+\varepsilon\bigr).
\tag{3.2}
\]

The collective factor is

\[
\lambda^2+\varepsilon,
\tag{3.3}
\]

whereas every nonzero \(\mu_j\) produces one slow root and one fast root:

\[
\lambda_{j,s}
=-\frac{\varepsilon}{\mu_j}+O(\varepsilon^2),
\qquad
\lambda_{j,f}
=-\mu_j+O(\varepsilon).
\tag{3.4}
\]

In particular, there are exactly \(N-1\) slow transverse roots, counting
algebraic multiplicity.

#### Proof

The block determinant in (3.2) follows by eliminating the recovery block;
both sides are polynomials in \(\lambda\), so the identity initially
obtained for \(\lambda\ne0\) extends to \(\lambda=0\).  Triangularizing
\(L\) gives the product.  The expansions in (3.4) follow from the two
roots of each scalar quadratic.  \(\square\)

If \(\operatorname{Re}\mu_j>0\), then
\(\operatorname{Re}(-1/\mu_j)<0\), so the slow root is stable.  Its
contraction rate nevertheless tends to zero with \(\varepsilon\).

### Theorem 3.2 (weak delays preserve the slow-root cluster)

Assume that the finite family \(B_k\) is uniformly bounded and that, for
some fixed \(\Theta>0\),

\[
0\le\tau_k(\varepsilon)\le
\frac{\Theta}{\sqrt\varepsilon}.
\tag{3.5}
\]

The characteristic determinant of the full delayed linearization is

\[
D_\varepsilon(\lambda)
=\det\Delta_\varepsilon(\lambda),
\tag{3.6}
\]

where

\[
\Delta_\varepsilon(\lambda)
=\lambda^2I+\lambda L+\varepsilon I
-\varepsilon\lambda\sum_{k=1}^{m}
B_k\bigl(e^{-\lambda\tau_k}-1\bigr).
\tag{3.7}
\]

Let \(\Gamma\) be a finite union of pairwise disjoint contours enclosing
all roots of

\[
p_0(\zeta)=\det(I+\zeta L)
\tag{3.8}
\]

and no root on the contours.  Then, for all sufficiently small positive
\(\varepsilon\), the delayed characteristic determinant has exactly
\(N-1\) roots of the form

\[
\lambda=\varepsilon\zeta
\tag{3.9}
\]

with \(\zeta\) inside \(\Gamma\), counting algebraic multiplicity.  Their
limiting rescaled locations are

\[
\zeta=-\frac1{\mu_j},
\qquad j=2,\ldots,N.
\tag{3.10}
\]

#### Proof

The full \(2N\)-dimensional RFDE characteristic matrix is

\[
\mathcal C_\varepsilon(\lambda)=
\begin{pmatrix}
\lambda I+L-\varepsilon\displaystyle\sum_k
B_k(e^{-\lambda\tau_k}-1)&I\\
-\varepsilon I&\lambda I
\end{pmatrix}.
\tag{3.11}
\]

For \(\lambda\ne0\), a block determinant gives
\(\det\mathcal C_\varepsilon=\det\Delta_\varepsilon\).  Both sides are
entire, hence the identity holds everywhere.

Set \(\lambda=\varepsilon\zeta\).  Factoring \(\varepsilon\) from each
row of (3.7) gives

\[
\varepsilon^{-N}D_\varepsilon(\varepsilon\zeta)
=\det\left[
I+\zeta L+\varepsilon\zeta^2I
-\varepsilon\zeta\sum_k
B_k(e^{-\varepsilon\zeta\tau_k}-1)
\right].
\tag{3.12}
\]

On every compact \(\zeta\)-set, (3.5) implies

\[
e^{-\varepsilon\zeta\tau_k}-1=O(\sqrt\varepsilon)
\tag{3.13}
\]

uniformly.  Consequently, the matrix inside (3.12) converges uniformly to
\(I+\zeta L\), and its determinant converges uniformly to \(p_0\).  On
each component of \(\Gamma\), the difference is eventually smaller than
\(|p_0|\).  Rouché's theorem preserves the number of enclosed zeros.

Because the zero eigenvalue of \(L\) contributes the constant factor one,
\(p_0\) has degree \(N-1\), with roots (3.10) counted algebraically.  This
proves the claim.  \(\square\)

### Corollary 3.3 (no uniform two-dimensional normal contraction)

Use the canard-scale time \(s=\sqrt\varepsilon\,t\).  The roots in Theorem
3.2 have rescaled rates

\[
\frac{\lambda}{\sqrt\varepsilon}
=O(\sqrt\varepsilon)\longrightarrow0.
\tag{3.14}
\]

Therefore a reduction that places only the fold Jordan plane in the
critical block cannot possess a complementary exponential contraction
rate bounded away from zero uniformly as \(\varepsilon\to0\).  This rules
out a **uniformly normally hyperbolic two-dimensional graph argument** for
the standard independent-recovery model.  It does not rule out a
nonuniform reduction, a larger \((N+1)\)-center reduction, or a reduction
inside an exactly invariant synchronous subspace.

## 4. What the algebra does and does not force for matching

### 4.1 Conditional center-coordinate count

Let

\[
\mathcal Z_0=\ker J_0^2,
\qquad
\mathcal F=\operatorname{span}\{e_f,g_f\}.
\tag{4.1}
\]

Then

\[
\dim\mathcal Z_0=N+1,
\qquad
\dim(\mathcal Z_0/\mathcal F)=N-1.
\tag{4.2}
\]

If a concrete endpoint construction leaves all of these coordinates free,
and a phase condition removes one direction in \(\mathcal F\), then its
remaining center-coordinate target has the **candidate** dimension

\[
(N+1)-1=N.
\tag{4.3}
\]

Equation (4.3) is only a finite-dimensional coordinate count.  It does not
prove that the selected full-history Lin operator has cokernel dimension
\(N\).  The endpoint manifolds can constrain or identify coordinates, and
the RFDE phase/history problem can change the Fredholm bookkeeping.

### Lemma 4.1 (scalar simple-zero no-go)

Let \(q>1\), let \(U\subset\mathbb R^q\) be a neighborhood of the origin,
and let \(d:U\to\mathbb R\) be \(C^1\).  If

\[
d^{-1}(0)\cap U_0=\{0\}
\tag{4.4}
\]

for some neighborhood \(U_0\), then

\[
Dd(0)=0.
\tag{4.5}
\]

#### Proof

If \(Dd(0)\ne0\), the implicit-function theorem makes \(d^{-1}(0)\) near
the origin a \((q-1)\)-dimensional \(C^1\) submanifold.  It therefore
contains points other than the origin, contradicting (4.4).  \(\square\)

Thus one scalar can encode a multi-coordinate equality only degenerately;
for example, a squared norm has the right zero set but zero derivative at
the solution.  It cannot support the usual simple-root implicit-function
argument.

Applied conditionally to (4.3), this says that for \(N>1\) a scalar simple
gap cannot detect an arbitrary mismatch in every post-phase center
coordinate.  Applied only to the recovery-center quotient, the same
conclusion begins at \(N>2\).  Neither application identifies the actual
RFDE Lin target without the missing endpoint theorem.

### Proposition 4.2 (conditional parameter-rank lower bound)

Suppose a specified endpoint problem really produces a \(C^1\) matching
map

\[
G:\mathbb R^m\longrightarrow\mathbb R^q
\tag{4.6}
\]

and robust first-order local right-solvability is to follow from a
submersion or inverse-function argument.  Then

\[
\operatorname{rank}DG(0)=q,
\qquad
m\ge q.
\tag{4.7}
\]

Consequently:

- matching all \(N-1\) recovery-center quotient coordinates would require
  at least \(N-1\) independent scalar parameters;
- matching all \(N\) candidate post-phase center coordinates would require
  at least \(N\) independent scalar parameters.

These are necessary rank bounds under the stated free-coordinate
hypothesis.  They are not sufficient controllability results, and
"parameters" cannot be replaced by "physical actuators" until the pulse
parameterization and trace derivative are constructed.

## 5. Three mathematically distinct model branches

The obstruction clarifies three options that must not be conflated.

1. **Standard independent recoveries.**  Model (2.1) has generalized-center
   dimension \(N+1\) and \(N-1\) slow transverse roots.  A genuine network
   theorem must retain or otherwise resolve these coordinates.

2. **Exact synchronous restriction.**  If the initial histories, inputs,
   delays, and coupling preserve the synchronous subspace, restricting to
   it yields the usual two-dimensional FHN problem.  This is a valid
   invariant-subspace theorem, but it does not control nonsynchronous
   histories or arbitrary network perturbations.

3. **Recovery-scaffold model.**  Adding order-one damping to recovery
   differences can move the \(N-1\) recovery directions into a uniformly
   stable block.  That supports a two-dimensional critical graph, but it is
   a changed biological model, not a theorem about (2.1).  The dual-state
   scaffold is treated separately in
   `docs/full-network-lin-operator.md`.

The first branch is the honest route to a general network canard theory for
independent recovery variables.  The present note establishes why it
requires a multiple-center construction.

## 6. Remaining RFDE gate

To turn the algebraic candidate (4.3) into a theorem about a vector Lin gap,
one must still:

1. construct the \((N+1)\)-center RFDE solution manifold, or a justified
   equivalent blow-up chart, with estimates uniform in the singular
   parameter;
2. construct the selected attracting and repelling outer history manifolds
   and their endpoint trace maps;
3. impose a phase condition and define the full-history jump operator;
4. prove that its linearization is Fredholm and compute its kernel and
   cokernel dimensions;
5. show which of the algebraic recovery-center coordinates survive the
   outer selection;
6. prove a full-rank derivative for a specified physical pulse family.

Only after steps 1--5 may one assign a concrete RFDE vector-gap dimension
\(q_N\).  Only after step 6 may one claim biological pulse controllability.

## 7. Reproducible symbolic checks

The file

`src/canard_control/multiple_recovery_center.py`

constructs the fold chain and recovery-center basis for a rank-one
voltage scaffold, checks the exact nullities, decomposes generalized-center
coordinates, and supplies the no-delay characteristic factor.  The rank-one
case is a reproducible witness for the general proof; Theorem 2.1 itself is
not restricted to rank-one coupling.

Run

```bash
python -m pytest -q tests/test_multiple_recovery_center.py
```
