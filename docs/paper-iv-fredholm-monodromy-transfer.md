# Phase borders, RFDE monodromy, and the unit Floquet multiplier

Status: **the Fredholm-to-monodromy transfer and the center unit-multiplier
claim are proved.**  Applied to the center orbit validated in
[paper-iv-infinite-periodic-validation.md](paper-iv-infinite-periodic-validation.md),
the result proves that the multiplier $1$ of the synchronous two-delay FHN
monodromy is algebraically simple.  A directed estimate also excludes all
unit multipliers with Bloch phase

\[
  0<|\varphi|\leq
  7.705280328597522\times10^{-4}.
\]

**Full unit-circle exclusion is still open.**  The unresolved positive
phases are

\[
 7.705280328597522\times10^{-4}<\varphi\leq\pi.
\]

For a closed-cover validation it is sufficient, and technically preferable,
to retain the already excluded endpoint and certify the compact Bloch arc

\[
 [7.705280328597522\times10^{-4},\pi],
\tag{0.1}
\]

because real conjugation covers the negative arc.  No parameter-box,
extremum, or response claim is made here.  The isolated implementation and
tests are
[rfde_floquet_transfer.py](../src/canard_control/rfde_floquet_transfer.py)
and
[test_rfde_floquet_transfer.py](../tests/test_rfde_floquet_transfer.py).
The executable center transfer is bound to the exact binary candidate and
the radius/inverse fields of the tracked e4dbe67 result by a SHA-256 evidence
fingerprint; it refuses a different candidate or altered theorem bounds.
The frozen JNS manuscript is not modified or used as evidence.

The standard history-space facts used below are the solution-process and
periodic-system results in Chapters 6, 10, and 13 of
[Hale--Verduyn Lunel (1993)](https://doi.org/10.1007/978-1-4612-4342-7),
and Chapters XIV--XVI of
[Diekmann--van Gils--Verduyn Lunel--Walther (1995)](https://doi.org/10.1007/978-1-4612-4206-2).
In particular, a retarded solution operator is eventually compact and its
nonzero multipliers are isolated eigenvalues of finite algebraic
multiplicity.  The generalized-Floquet-function construction is also
displayed explicitly in Section 4.5 and equation (1.123) of
[Hupkes (2008)](https://math.leidenuniv.nl/scripties/PhdHupkes.pdf).
The transfer proof here is included in full because the moving-delay period
column is the decisive model-specific seam.

## 1. The periodic variational problem

Consider the autonomous discrete-delay RFDE

\[
 \dot x(t)=f(x(t),x(t-\tau _1),\ldots,x(t-\tau _q)),
 \qquad \tau_j>0,
\tag{1.1}
\]

and a nonconstant $T$-periodic classical solution $x_*$.  Put

\[
 X(\theta)=x_*(T\theta),\qquad
 \alpha_j=\frac{\tau_j}{T}.
\tag{1.2}
\]

Along the orbit let $A_0(\theta)$ and $A_j(\theta)$ be the derivatives of
$f$ in its current and $j$-th delayed arguments.  On one-periodic
functions define

\[
 \mathcal Ly
 =y'-TA_0y-T\sum_{j=1}^q A_j\mathcal S_{\alpha_j}y,
 \qquad
 (\mathcal S_\alpha y)(\theta)=y(\theta-\alpha).
\tag{1.3}
\]

Differentiating the normalized orbit equation with respect to the *real
period*, while the physical delays stay fixed, gives the column

\[
 D_T\Phi(X,T)=-b,
 \qquad
 b=f+\sum_{j=1}^q
       \alpha_jA_j\mathcal S_{\alpha_j}X'.
\tag{1.4}
\]

The delayed term in (1.4) is compulsory.  Replacing $b$ by $f$ proves
the ODE statement, not the RFDE statement.

Let $E_1\hookrightarrow E_0$ be real periodic function spaces on which
$\mathcal L:E_1\to E_0$ is defined, and let
$\ell:E_1\to\mathbb R$ be a bounded phase functional.  The bordered
derivative is

\[
 \mathcal B(y,\sigma)
 =\bigl(\mathcal Ly-b\sigma,\ell(y)\bigr).
\tag{1.5}
\]

For the BVP realization one may take
$E_1=H^1_{\rm per}$ and $E_0=L^2_{\rm per}$.  The derivative is Fredholm
of index zero: $d/d\theta$ has index zero and the current and delayed
lower-order terms are relatively compact through the compact embedding
$H^1(\mathbb T)\hookrightarrow L^2(\mathbb T)$.  Adding one domain scalar
and one range scalar preserves the index.  If
$\mathcal W^m_{\mathbb R}$ denotes the state-coordinate projection of the
prior validation's space $\mathcal X^m_{\mathbb R}$, the validated
real-conjugate Wiener realization is

\[
 \mathcal B:
 \underbrace{\mathcal W^1_{\mathbb R}\times\mathbb R_T}
             _{\mathcal X^1_{\mathbb R}}
 \longrightarrow
 \underbrace{\mathcal W^0_{\mathbb R}\times\mathbb R_{\rm phase}}
             _{\mathcal Y^0_{\mathbb R}}.
\tag{1.6}
\]

Here, exactly as in the prior validation, $\mathcal X^1_{\mathbb R}$
already contains the single **real** period coordinate, while
$\mathcal Y^0_{\mathbb R}$ contains the state residual and one real phase
scalar.  Thus (1.6) neither counts $T$ twice nor complexifies it.

Section 3 below supplies the regularity bridge between these realizations.

## 2. Exact Fredholm-to-monodromy theorem

Let $r=\max_j\tau_j$, let

\[
 \mathscr C=C([-r,0],\mathbb R^d),
\]

and let $M=U(T,0):\mathscr C\to\mathscr C$ be the monodromy operator of
the physical-time variational RFDE.  The tangent history is

\[
 p_0(s)=\dot x_*(s),\qquad -r\leq s\leq0.
\tag{2.1}
\]

> **Theorem 2.1 (phase border and the unit RFDE multiplier).**
> Assume the following.
>
> 1. The RFDE is retarded, its variational coefficients along $x_*$ are
>    continuous and $T$-periodic, and $M$ is power compact.  The last
>    property is automatic for (1.1), because $U(t,s)$ is compact after
>    the maximal delay.
> 2. $X'\in E_1$, and every periodic variational solution and every
>    periodicization of a rank-two generalized solution at multiplier $1$
>    belongs to $E_1$.
> 3. The column in (1.5) is exactly (1.4).
>
> Then the following statements are equivalent:
>
> \[
> \begin{split}
> &\mathcal B\text{ is injective};\\
> &\ker\mathcal L=\operatorname{span}\{X'\},\quad
>   \ell(X')\ne0,\quad b\notin\operatorname{Ran}\mathcal L;\\
> &\ker(M-I)=\operatorname{span}\{p_0\},\quad
>   p_0\notin\operatorname{Ran}(M-I),\quad \ell(X')\ne0;\\
> &1\text{ is an algebraically simple eigenvalue of }M
>   \text{ and }\ell(X')\ne0.
> \end{split}
> \tag{2.2}
> \]
>
> If, in addition, the BVP realization of $\mathcal B$ is Fredholm of
> index zero, injectivity and bijectivity of that realization are
> equivalent.  Thus a validated inverse of the correctly bordered
> derivative proves algebraic simplicity of $1$; no separate adjoint
> pairing computation is needed.

**Proof.**  Autonomy gives $\mathcal LX'=0$.  If $\mathcal B$ is
injective, then $\ell(X')\ne0$, since otherwise
$\mathcal B(X',0)=0$.  Given $y\in\ker\mathcal L$, subtract the unique
multiple of $X'$ that makes $\ell(y)=0$; injectivity then gives
$y\in\operatorname{span}\{X'\}$.  If $b=\mathcal Ly$, the same phase
adjustment would put a nonzero pair $(y-cX',1)$ in
$\ker\mathcal B$.  Hence $b\notin\operatorname{Ran}\mathcal L$.
The converse follows by reversing these three arguments.  This proves the
first equivalence in (2.2).

Taking the history segment of a periodic variational solution identifies
$\ker\mathcal L$ with $\ker(M-I)$.  The nontrivial point is the range
condition.  Direct calculation from (1.3)--(1.4) gives

\[
 \boxed{\mathcal L(\theta X')=Tb.}
\tag{2.3}
\]

Suppose $(M-I)\psi=p_0$, and let $u(t;\psi)$ be the associated
variational solution.  Periodicity of the coefficients and uniqueness give

\[
 u(t+T)=u(t)+\dot x_*(t).
\tag{2.4}
\]

Consequently

\[
 z(\theta)=u(T\theta)-\frac{\theta}{T}X'(\theta)
\tag{2.5}
\]

is one-periodic and satisfies $\mathcal Lz=-b$.  Conversely, if a periodic
$z$ satisfies $\mathcal Lz=-b$, then
$u(T\theta)=z(\theta)+\theta X'(\theta)/T$ is a homogeneous variational
solution satisfying (2.4).  Therefore

\[
 b\in\operatorname{Ran}\mathcal L
 \quad\Longleftrightarrow\quad
 p_0\in\operatorname{Ran}(M-I).
\tag{2.6}
\]

For the power-compact operator $M$, every nonzero spectral value has
finite algebraic multiplicity.  Geometric multiplicity one together with
the absence of a rank-two Jordan vector is equivalent to algebraic
multiplicity one.  This real-space conclusion is also the complex
algebraic-multiplicity statement.  Indeed, the complex kernel is the
complexification of the real kernel; and if the real vector $p_0$ had a
complex preimage under $M-I$, the real part of that preimage would be a
real preimage.  Thus a complex Jordan chain cannot evade the real range
obstruction.  This proves (2.2).  Finally a Fredholm operator of index zero
is bijective exactly when it is injective.  \(\square\)

The theorem separates several statements that are often conflated:

- $\ker\mathcal L=\operatorname{span}\{X'\}$ proves only geometric
  simplicity;
- $b\notin\operatorname{Ran}\mathcal L$ excludes the Jordan vector and
  upgrades geometric to algebraic simplicity;
- an arbitrary border column does not test that Jordan vector;
- algebraic simplicity of $1$ does not exclude multipliers
  $e^{i\varphi}\ne1$ elsewhere on the unit circle.

## 3. Why the validated Fourier inverse sees the history spectrum

The center proof constructs a solution in the component Wiener algebra and
then bootstraps once to its first-derivative domain.  For the polynomial FHN
field this bootstrap iterates.  If $X\in\mathcal W^m$, every current and
shifted polynomial in $X$ also lies in $\mathcal W^m$, and the orbit
equation puts $X$ in $\mathcal W^{m+1}$.  Hence the validated orbit and
all variational coefficients are $C^\infty$.

Every eigenhistory at a nonzero multiplier $\lambda$ lies in the range of
a sufficiently smoothing solution operator: if $M\psi=\lambda\psi$, then
$\psi=\lambda^{-n}M^n\psi$.  Its variational solution therefore first
becomes $C^1$ and then bootstraps to $C^\infty$.  In particular, for
$\lambda=e^{i\varphi}$ the periodic Bloch factor obtained from that
solution lies in the complexification of $\mathcal W^1_{\mathbb R}$, so
the kernel test in Section 5 sees every possible nonzero unit multiplier,
not merely smooth trial functions.  At $\lambda=1$ the same statement
places every periodic variational solution in $\mathcal W^1_{\mathbb R}$.
The argument also applies to the generalized periodicization (2.5), whose
inhomogeneity $b$ is smooth.  A $C^3$ periodic function already has
absolutely summable Fourier coefficients with one Fourier derivative.
Thus all state functions used in Theorem 2.1 lie in
$\mathcal W^1_{\mathbb R}$ and, after adjoining the real period scalar,
in the validated domain $\mathcal X^1_{\mathbb R}$.

This is the required bridge.  Bijectivity on a finite Fourier truncation
alone would not supply it, and injectivity on a small coefficient space
would not control history-space eigenvectors without the bootstrap.

## 4. Application to the center two-delay FHN orbit

At

\[
 (\varepsilon,a,\Theta_0,\Theta_1,\kappa_1,\kappa_3)
 =(0.2,0.6,4,5,0.2,0.25),
\tag{4.1}
\]

the earlier infinite proof supplies a radius-$10^{-7}$ classical orbit
and a phase-bordered inverse bound

\[
 \|\mathcal B^{-1}\|\leq23.45219633406240.
\tag{4.2}
\]

The norm in (4.2) maps the state-Wiener-plus-phase residual norm into the
*base* state-Wiener-plus-period norm; it is not an
\(\mathcal X^1\)-graph-norm estimate.  That is sufficient below because
\(\mathcal L_s-\mathcal L\) is a bounded lower-order map from the base
space to the residual space.

The coefficient of candidate mode $k=1$, minus the whole correction
radius, gives

\[
 |v_1|\geq0.6753571589344110>0,
\tag{4.3}
\]

so the exact orbit is nonconstant.  Directed delay and period bounds give

\[
 T\geq16.54038769818094
 >11.18033988749895\geq\max_j\tau_j.
\tag{4.4}
\]

Thus the one-period monodromy itself is compact.  The period column used in
the validated matrix is exactly $-b$ from (1.4), including both
$\tau_j/T$ contributions.  Theorem 2.1 therefore proves:

> **Corollary 4.1 (center unit multiplier).**  The synchronous two-delay FHN
> monodromy at (4.1) has multiplier $1$ with algebraic multiplicity one.

This changes the center claim from open to proved.  It does not yet prove
full Floquet hyperbolicity.

## 5. A directed punctured neighborhood of 1

For $s=i\varphi$, a multiplier $e^{i\varphi}$ is equivalent to a
one-periodic solution of the Bloch equation

\[
 \mathcal L_s y=0,
\tag{5.1}
\]

where

\[
 \mathcal L_s y
 =y'+sy-TA_0y
  -T\sum_j e^{-s\alpha_j}A_j\mathcal S_{\alpha_j}y.
\tag{5.2}
\]

It is enough to take $-\pi<\varphi\leq\pi$.  Complexify the validated real
*linear* domain and range with the split norm

\[
 \|u+iv\|_\oplus=\|u\|_\square+\|v\|_\square.
\tag{5.3}
\]

For a complex scalar use the matching notation
$|c|_\oplus=|\Re c|+|\Im c|$.  In particular, because $s=i\varphi$,
$|cs|_\oplus=|c|_\oplus|s|$.  This complexifies the period-column
direction $\sigma$ only as part of a linear operator; the validated base
period $T$, the delay fractions $\tau_j/T$, and the nonlinear orbit remain
real.

The real inverse extends to this complexification with the same norm.  Put
$C_s=\mathcal L_s-\mathcal L$.  The exact cancellations are

\[
 \begin{aligned}
 C_sy
  &=sy-T\sum_j(e^{-s\alpha_j}-1)A_j\mathcal S_{\alpha_j}y,\\
 C_sX'-sTb
  &=-T\sum_j(e^{-s\alpha_j}-1+s\alpha_j)
          A_j\mathcal S_{\alpha_j}X'.
 \end{aligned}
\tag{5.4}
\]

Taylor's integral formula and
$|e^{-it}|_\oplus=|\cos t|+|\sin t|\leq\sqrt2$ give

\[
 |e^{-it}-1|_\oplus\leq\sqrt2|t|,
 \qquad
 |e^{-it}-1+it|_\oplus\leq\frac{|t|^2}{\sqrt2}.
\]

For the FHN delayed term specifically,
$A_j\mathcal S_{\alpha_j}y
=\mathcal S_{\alpha_j}(H_v(v_*)y)$.  Coefficient multiplication is
submultiplicative and this *single* real-Wiener shift costs at most
$\sqrt2$; it is not estimated as a coefficient shift followed by a second
state shift.  Combining it with the preceding scalar-rotation bounds gives

\[
 \|C_s y\|\leq c_1|s|\,\|y\|,
\qquad
 \|C_sX'-sTb\|\leq c_2|s|^2,
\tag{5.5}
\]

with the directed bounds

\[
 c_1\leq27.66929154675788,
 \qquad
 c_2\leq337.6796828012269.
\tag{5.6}
\]

For the FHN delayed field
$H(v)=\varepsilon\kappa_1v/2+
\varepsilon\kappa_3(v-1)^3/2$, these constants are obtained from

\[
 \begin{aligned}
 B_*&\geq\|H_v(v_*)\|_\square,\\
 c_1&=1+2(\tau_0+\tau_1)B_*,\\
 c_2&=TB_*(\alpha_0^2+\alpha_1^2)\|X'\|_\square.
 \end{aligned}
 \tag{5.7}
\]

The factors of two in $c_1$ and the absence of a factor $1/2$ in
$c_2$ account for both the real-Wiener shift norm and the split-norm
complex rotation.  They are not Euclidean-norm estimates copied into the
validated component norm.

For completeness, write a hypothetical kernel vector as
$y=cX'+z$, where $\ell(z)=0$.  Equations (2.3)--(5.5) give

\[
 \mathcal B(z,-csT)
 =\bigl(-C_sz-c(C_sX'-sTb),0\bigr).
\tag{5.8}
\]

If $D=\|\mathcal B^{-1}\|$, then

\[
 \|z\|_\oplus+|c|_\oplus T|s|
 \leq D\{c_1|s|\|z\|_\oplus+c_2|c|_\oplus|s|^2\}.
\tag{5.9}
\]

Hence $\ker\mathcal L_s=\{0\}$ whenever

\[
 Dc_1|s|<1,
 \qquad
 Dc_2|s|<T.
\tag{5.10}
\]

The implementation takes half of both directed thresholds, leaving strict
margins.  It proves

\[
 \boxed{
 0<|\varphi|\leq7.705280328597522\times10^{-4}
 \Longrightarrow
 e^{i\varphi}\notin\sigma(M).}
\tag{5.11}
\]

The constants in (5.6) use the exact correction ball, not just the stored
polynomial.  In particular, the orbit-tangent majorant is

\[
 \|X'\|_\square\leq41.11902213912061,
\tag{5.12}
\]

and the delayed variational coefficient has Wiener norm at most
$0.6626038756701235$.

## 6. The exact remaining directed gate

For each closed interval $I\subset[\delta,\pi]$, where $\delta$ is the
lower bound in (5.11), construct one preconditioner

\[
 \mathcal A_I=A_{P,I}\oplus A_{Q,I}
\tag{6.1}
\]

for the complex Bloch operator (5.2).  Its four directed block bounds must
hold simultaneously for every $\varphi\in I$ and every orbit in the
validated correction ball:

\[
\begin{array}{c|cc}
 &P\text{ output}&Q\text{ output}\\ \hline
P\text{ input}&Z_{PP,I}&Z_{QP,I}\\
Q\text{ input}&Z_{PQ,I}&Z_{QQ,I}.
\end{array}
\tag{6.2}
\]

The cell closes if

\[
 \max\{Z_{PP,I}+Z_{QP,I},
       Z_{PQ,I}+Z_{QQ,I}\}<1.
\tag{6.3}
\]

The source checks three hostile bookkeeping conditions: the cells must
form a connected cover of the whole arc (0.1), every declared block upper
bound must be nonnegative, and (6.3) must be strict in every cell.  The
arithmetic that produces a cell must separately prove that its numbers are
outward bounds for the exact-orbit ball over the whole phase interval; the
contract checker cannot infer that provenance from decimal strings and
therefore **always leaves `outer_arc_exclusion_validated=false`**, even when
the bare-number bookkeeping contract passes.  Midpoint
invertibility, a sampled singular-value plot, or cells evaluated only at
the stored polynomial do not supply validated cells.

No such directed outer-arc cells are supplied in this stage.  Therefore the
correct current ledger is:

| Claim | Status |
|---|---|
| Center RFDE orbit | **Proved** by the prior infinite radii theorem |
| Center phase-bordered Fourier derivative | **Proved bijective** by the prior theorem |
| Fourier/BVP derivative to monodromy transfer | **Proved** by Theorem 2.1 and Section 3 |
| Multiplier $1$ geometrically simple | **Proved** |
| Multiplier $1$ algebraically simple | **Proved** |
| Other multipliers on the local arc (5.11) | **Directed exclusion proved** |
| Other multipliers with $\delta<|\varphi|\leq\pi$ | **Open: compact finite/tail cell gate (0.1), (6.2)--(6.3)** |
| Full unit-circle exclusion / Floquet hyperbolicity | **Open** |
| Parameter-box continuation, extrema, response block | **Proved on the later microscopic-box certificate; \(\beta_U\ge0.0162187\)** |
| Issue 15 | **Open** |

Run the isolated checks with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_rfde_floquet_transfer.py
```

## 7. Hostile self-audit

1. **Wrong period column.**  If the delayed pieces of (1.4) are omitted,
   (2.3) fails and bordered invertibility does not exclude a Jordan chain.
   The implementation requires this seam explicitly.
2. **Geometric versus algebraic simplicity.**  Kernel dimension one alone
   is not enough.  The range obstruction (2.6) is the additional argument.
3. **Fourier versus history space.**  A small-space inverse is not silently
   identified with a history-space theorem; Section 3 proves that every
   relevant eigenfunction and periodicized generalized eigenfunction lies
   in the validated domain.
4. **Real versus complex perturbations.**  The claim at $1$ can be proved
   over the real space.  The punctured-arc estimate explicitly complexifies
   the inverse using the split norm.
5. **Compactness.**  The application checks $T>\max_j\tau_j$, so the
   one-period monodromy is compact; it does not merely assume a
   finite-dimensional spectrum.
6. **Local versus global exclusion.**  Algebraic simplicity gives only an
   unspecified spectral neighborhood.  Equation (5.11) is the directed
   quantitative neighborhood.  Neither statement is relabeled as the
   missing outer-arc proof.
7. **Center versus box.**  Every proved numerical statement here is at the
   single center parameter.  None is promoted to the issue-15 parameter
   box.
