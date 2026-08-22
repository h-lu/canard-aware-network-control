# Final model (M): exact algebra and a minimal spectral diagnostic

Status: **exact finite-dimensional audit plus an uncertified fixed-parameter
RFDE root diagnostic, 2026-08-22.** The identities in Sections 2--6 are
proved by direct algebra and reproduced in
`src/canard_control/final_two_module.py`. Section 7 is numerical evidence
only. Nothing in this note alone proves a full RFDE spectral gap, an
invariant history manifold, or a canard-threshold theorem. The later
special-flow, growing-tube, and phase-normal Green notes prove the
preparation-indexed canonical local history-connection theorem; no such
analytic conclusion is inferred from the algebra below.

## 1. Frozen equation and conventions

Let

\[
 \sigma=\sqrt{3/2},\qquad
 r=\binom{1}{2},\qquad
 \ell=\binom{1/2}{1/4},\qquad
 P=r\ell^\top,\qquad P_\perp=I-P.
\]

The final two-module model is

\[
\begin{aligned}
 \dot v(t)={}&F(v(t),w(t))
 +\varepsilon K\left[
 Bv(t)-C_0^\eta v(t-\theta_0/\delta)
       -C_1^\eta v(t-\theta_1/\delta)
 \right],\\
 \dot w(t)={}&\varepsilon
 \binom{v_1(t)-\sigma-\mu}{v_2(t)-2\mu}
 -D_wP_\perp(w(t)-w_*),
 \qquad \varepsilon=\delta^2,
\end{aligned}
\tag{M}
\]

where

\[
 F(v,w)=\binom{
 v_1-v_1^3/3-w_1+(v_2-v_1)/2
 }{
 v_2-v_2^3/3-w_2+2(v_1-v_2)
 },
\]

\[
 v_*=\binom{\sigma}{0},\qquad
 w_*=\binom{0}{2\sigma},\qquad
 0<\theta_0<\theta_1,\qquad D_w>0.
\]

The two delayed layers and their signed redistribution direction are

\[
 C_0=\begin{pmatrix}1/6&1/12\\1/6&1/4\end{pmatrix},\qquad
 C_1=\begin{pmatrix}1/3&1/6\\1/2&5/12\end{pmatrix},\qquad
 T=\begin{pmatrix}1&0\\-2&0\end{pmatrix},
\]

\[
 C_0^\eta=C_0+\eta T,\qquad
 C_1^\eta=C_1-\eta T,\qquad B=C_0+C_1.
\]

Here “positive layer” always means **entrywise positive**. The matrix \(T\)
is intentionally signed: it is a tangent direction in layer space, not
itself a biological coupling layer.

## 2. Equilibrium and the fold mode

At \(\mu=0\), direct substitution gives

\[
 F(v_*,w_*)=0,
 \qquad
 \binom{v_{*,1}-\sigma}{v_{*,2}}=0.
\]

Moreover,

\[
 B-C_0^\eta-C_1^\eta=0.
\]

Consequently the source-history feedback vanishes on every constant history,
and \((v_*,w_*)\) is an equilibrium for every admissible \(\eta\), \(K\), and
positive \(\varepsilon\). The recovery scaffold also vanishes there.

The fast voltage Jacobian is

\[
 A_0=D_vF(v_*,w_*)
 =\begin{pmatrix}-1&1/2\\2&-1\end{pmatrix}
 =-2P_\perp,
\]

and

\[
 \ell^\top r=1,\qquad A_0r=0,\qquad \ell^\top A_0=0.
\]

With

\[
 q=\binom{1}{-2},\qquad
 \ell_\perp=\binom{1/2}{-1/4},
\]

the two modal pairs are biorthogonal:

\[
 \ell^\top q=\ell_\perp^\top r=0,\qquad
 \ell_\perp^\top q=1,\qquad P_\perp q=q,\qquad A_0q=-2q.
\]

For the fold curvature,

\[
 \ell^\top D_v^2F(v_*,w_*)[r,r]
 =-\sigma\ne0.
\tag{1}
\]

The slow field also selects the same critical line exactly. If
\(v=v_*+rX\), then

\[
 \binom{v_1-\sigma-\mu}{v_2-2\mu}
 =r(X-\mu).
\tag{2}
\]

Equations (1)--(2) verify the elementary fold and unfolding algebra. They do
not establish the delayed invariant geometry near the fold.

## 3. Exact entrywise positivity range

The four entries that depend on \(\eta\) are

\[
 \frac16+\eta,\qquad
 \frac16-2\eta,\qquad
 \frac13-\eta,\qquad
 \frac12+2\eta.
\]

All remaining entries are fixed and strictly positive. Intersecting the four
strict inequalities gives the exact condition

\[
 \boxed{-\frac16<\eta<\frac1{12}.}
\tag{3}
\]

The paper's smaller choice \(|\eta|\le 1/20\) is therefore safe. On that
closed interval the smallest entry attained by either layer is exactly
\(1/15\). Thus any fixed \(0<\bar\eta<1/20\) leaves a strict margin.

## 4. Total gain and the complete projected delay measure

The total layer is independent of \(\eta\):

\[
 C_0^\eta+C_1^\eta
 =B
 =\begin{pmatrix}1/2&1/4\\2/3&2/3\end{pmatrix},
 \qquad Br=r.
\tag{4}
\]

More strongly, both projected atomic weights are fixed:

\[
 \ell^\top C_0^\eta r=\frac13,
 \qquad
 \ell^\top C_1^\eta r=\frac23.
\tag{5}
\]

Hence this is invariance of the **complete projected delay measure**, not
merely of its first moment:

\[
 \ell^\top\mathbb B_\eta(d\theta)r
 =\frac13\delta_{\theta_0}(d\theta)
  +\frac23\delta_{\theta_1}(d\theta).
\tag{6}
\]

Equivalently, for arbitrary test values \(h_0,h_1\),

\[
 \ell^\top(C_0^\eta r h_0+C_1^\eta r h_1)
 =\frac13h_0+\frac23h_1,
\]

whose \(\eta\)-derivative is identically zero.

## 5. What changes: the transverse history forcing

Since

\[
 Tr=q,
\]

the projected-out part of the delay measure is

\[
 P_\perp\mathbb B_\eta(d\theta)r
 =\eta q\,[\delta_{\theta_0}(d\theta)
             -\delta_{\theta_1}(d\theta)].
\tag{7}
\]

It is important to distinguish (7), which describes the delayed measure,
from the sign in the source-history feedback. For a scalar critical history
\(x\), define

\[
 \mathcal H_\eta[rx]
 =Brx(0)-C_0^\eta r x(-\theta_0)
           -C_1^\eta r x(-\theta_1).
\]

Then

\[
 \ell^\top\mathcal H_\eta[rx]
 =x(0)-\frac13x(-\theta_0)-\frac23x(-\theta_1),
\tag{8}
\]

while

\[
 P_\perp\mathcal H_\eta[rx]
 =\eta q\,[x(-\theta_1)-x(-\theta_0)].
\tag{9}
\]

Thus \(\eta\) changes a genuine transverse history channel while leaving all
of (4)--(6) fixed. Equations (7)--(9) are exact. The nonlinear
history-manifold and matching proof is supplied later for the
preparation-indexed canonical local root; an arbitrary physical outer
maximal-canard interpretation is not a consequence of this algebra.

## 6. The repaired current-state singular spectrum

At \(\varepsilon=0\) the weak delayed term switches off. The current-state
Jacobian in \((v,w)\) coordinates is

\[
 J_0=\begin{pmatrix}
 A_0&-I\\
 0&-D_wP_\perp
 \end{pmatrix}.
\tag{10}
\]

Exact factorization gives

\[
 \boxed{\det(zI-J_0)=z^2(z+2)(z+D_w).}
\tag{11}
\]

For every \(D_w>0\),

\[
 \dim\ker J_0=1,
 \qquad
 \dim\ker J_0^2=2,
 \qquad
 \dim\ker J_0^3=2.
\tag{12}
\]

An explicit length-two Jordan chain is

\[
 e_0=\binom{r}{0},
 \qquad
 e_1=\binom{0}{-r},
 \qquad
 J_0e_0=0,
 \qquad
 J_0e_1=e_0.
\tag{13}
\]

Also \((0,\ell)^\top\) spans the left kernel. The added recovery scaffold has
therefore removed the unwanted transverse recovery center from the
finite-dimensional singular Jacobian, leaving exactly one collective Jordan
chain at zero.

This current-state calculation by itself is not Gate A. In particular, (11)
contains no information about
the infinitely many characteristic roots created for positive \(\delta\) by
the delayed exponentials, nor does it provide an estimate uniform as
\(\delta\to0\).

## 7. Fixed-parameter RFDE characteristic-root diagnostic

For positive \(\delta\), linearization at \((v_*,w_*)\) has characteristic
matrix

\[
 \Delta(\lambda)=
 \begin{pmatrix}
 \lambda I-A_0-\delta^2KB
 +\delta^2K\displaystyle\sum_{k=0}^1
 C_k^\eta e^{-\lambda\theta_k/\delta}
 &I\\[2mm]
 -\delta^2I&\lambda I+D_wP_\perp
 \end{pmatrix}.
\tag{14}
\]

The code evaluates \(\det\Delta\) with multiprecision arithmetic and applies
a complex secant continuation to one supplied root seed. For

\[
 \delta=0.2,\quad K=1,\quad D_w=1,\quad
 \theta_0=0.5,\quad\theta_1=1,
\]

starting at \(0.01+0.21i\) gives:

| \(\eta\) | followed root \(\lambda\), rounded to 16 decimal digits |
|---:|---:|
| \(-0.02\) | \(0.008932506305572845+0.2149051653250718i\) |
| \(0\) | \(0.008932489549036367+0.2149057315003294i\) |
| \(0.02\) | \(0.008932472933953011+0.2149062975030451i\) |

The solver's unrounded internal roots have determinant residual below
\(10^{-30}\); evaluating the rounded display values need not preserve that
residual. The conjugate roots are present because (M) has real coefficients.
This table is useful only as a reproducible sign/convention check for (14) and as a
starting seed for a future certified spectral computation. The continuation:

- does not show that the displayed branch is rightmost;
- does not find or enclose all RFDE roots;
- does not prove root simplicity;
- does not prove a complementary spectral gap;
- does not give a bound uniform in \(\delta\) or \(\eta\).

Those conclusions require a separate analytic argument. That argument is now
given in [rfde-relevant-spectrum.md](rfde-relevant-spectrum.md); the table
above remains only an independent branch/sign diagnostic.

## 8. Reproduction and claim boundary

Run the exact and numerical audit with

```bash
PYTHONPATH=src python3 -m canard_control.final_two_module
PYTHONPATH=src python3 -m pytest -q tests/test_final_two_module.py
```

The tests establish reproducibility of the displayed algebra and one local
root branch. They do **not** establish any of the following:

1. a full-history RFDE spectral decomposition or uniform gap;
2. a parameter-regular invariant history embedding;
3. a stable foliation or bounded RFDE range inverse;
4. the coefficient of an RFDE canard matching gap;
5. existence, uniqueness, or asymptotics of a maximal-canard threshold.

Accordingly this note closes the exact-algebra part of Phase I. The separate
Rouché--Schur note closes the relevant-root count used by Gate A; neither
this fixed-parameter continuation nor the algebra alone does so.
