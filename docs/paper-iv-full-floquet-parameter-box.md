# Uniform Floquet exclusion on the periodic FHN parameter box

Status: **proved.**  This note closes the compact Bloch-arc gate left open
by
[paper-iv-fredholm-monodromy-transfer.md](paper-iv-fredholm-monodromy-transfer.md)
and
[paper-iv-periodic-parameter-box.md](paper-iv-periodic-parameter-box.md).
The proof is uniform on the nonempty gain box

\[
 U=\{(\kappa _1,\kappa _3):
 |\kappa _1-0.2|\leq10^{-12},\quad
 |\kappa _3-0.25|\leq10^{-12}\}.
\tag{0.1}
\]

It proves orbital hyperbolicity of the *synchronous* periodic RFDE branch:
the autonomous multiplier $1$ is algebraically simple and there is no other
multiplier on the unit circle.  It does **not** prove that all nontrivial
multipliers lie inside the unit disk, nor does it prove attraction or
transverse stability of the full network.

The executable proof is
[fhn_bloch_outer_validation.py](../src/canard_control/fhn_bloch_outer_validation.py),
the driver is
[fhn_bloch_outer_validation.py](../experiments/fhn_bloch_outer_validation.py),
and the tracked record is
[fhn_bloch_outer_validation.json](../experiments/results/fhn_bloch_outer_validation.json).
Its SHA-256 digest is

```text
c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31
```

The source parameter-box record has digest

```text
ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0
```

and the exact binary candidate fingerprint is

```text
2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169
```

## 1. The theorem

Fix

\[
 (\varepsilon,a,\Theta_0,\Theta_1)=(0.2,0.6,4,5),
 \qquad \tau_j=\Theta_j/\sqrt\varepsilon.
\tag{1.0}
\]

Let $b=(\kappa _1,\kappa _3)\in U$.  The D1 theorem supplies a real
$C^1$ branch $b\mapsto(X_b,T_b)$ of phase-fixed periodic solutions of the
synchronous two-delay FHN equation.  Write $\mathcal M_b$ for the
one-period RFDE monodromy along this orbit.

> **Theorem 1.1 (uniform synchronous orbital hyperbolicity).**  For every
> $b\in U$, the monodromy $\mathcal M_b$ has the multiplier $1$ with
> algebraic multiplicity one and
> \[
>   \sigma(\mathcal M_b)\cap\{|\lambda|=1\}=\{1\}.
> \tag{1.1}
> \]
> The assertion is uniform over the whole closed box (0.1).

The directed period and delay bounds satisfy

\[
 \begin{aligned}
 T_-&:=16.5403877931809337427421269239857792854309082030864525
       \leq T_b\\
 &\leq
 T_+:=16.5403878031809337427421269239857792854309082031635475,\\
 T_-&>
 11.1803398874989484820458683436563811772030917980853282
 \geq\max_j\tau_j.
 \end{aligned}
\tag{1.2}
\]

Thus the one-period monodromy is compact.  Its nonzero spectrum consists of
isolated eigenvalues of finite algebraic multiplicity, so (1.1) is the
usual RFDE notion of orbital hyperbolicity.  No stability index or count of
multipliers outside the unit disk is asserted.

The Fourier boundary-value problem and the history-space spectrum are
equivalent here, uniformly in $b$.  Indeed, the validated D1 Wiener ball is
uniform on $U$; polynomial multiplication and translation preserve every
Wiener derivative domain, so the orbit equation bootstraps the whole branch
and its variational coefficients to $C^\infty$.  If
$\mathcal M_b\psi=\lambda\psi$ with $\lambda\ne0$, then
$\psi=\lambda^{-n}\mathcal M_b^n\psi$.  The strict inequality in (1.2)
makes the iterated solution operator smoothing, after which the
variational equation bootstraps the corresponding Floquet solution to
$C^\infty$.  Its Bloch periodicization therefore belongs to the complex
Wiener derivative domain used below (already $C^3$ suffices).  Conversely,
every kernel element in that domain defines a classical quasiperiodic
variational solution and hence a history eigenvector.  The same bootstrap
applies at $\lambda=1$ to periodic solutions and to the generalized
periodicization used to test a rank-two Jordan chain.  Thus no unit-circle
history multiplier is lost by the Fourier realization.

## 2. The exact Bloch operator

Put $\lambda=e^{i\varphi}$, with $-\pi\leq\varphi\leq\pi$, and periodicize a
Floquet function by

\[
 u(T\theta)=e^{i\varphi\theta}y(\theta).
\tag{2.1}
\]

For $\omega_k=2\pi k+\varphi$, define

\[
 \begin{aligned}
 g&=1-v^2-\varepsilon\kappa _1
       -3\varepsilon\kappa _3(v-1)^2,\\
 H&=\frac{\varepsilon\kappa _1}{2}
       +\frac{3\varepsilon\kappa _3}{2}(v-1)^2.
 \end{aligned}
\tag{2.2}
\]

The Fourier coefficients of the unbordered Bloch operator are

\[
 \begin{aligned}
 (\mathcal L_\varphi y)_{v,k}
 &=i\omega_k y_{v,k}-T(g*y_v)_k+Ty_{w,k}\\
 &\quad
   -T\sum_{j=0}^1
    e^{-i\omega_k\tau_j/T}(H*y_v)_k,\\
 (\mathcal L_\varphi y)_{w,k}
 &=i\omega_k y_{w,k}-T\varepsilon y_{v,k}.
 \end{aligned}
\tag{2.3}
\]

The output-mode rotation in (2.3) follows from the exact identity

\[
 H(S_\alpha v)S_\alpha y=S_\alpha(H(v)y).
\tag{2.4}
\]

Separately varying a shifted coefficient and a shifted input would lose
the cancellation in (2.4) and would not give the moving-period estimate
used below.

The proof validates the unbordered operator (2.3) directly.  A bordered
Bloch matrix is not a substitute: a bordered matrix can be invertible while
its unbordered upper-left block has a kernel.

## 3. The unit multiplier and a uniform local arc

The parameter-box D1 certificate gives the uniform bordered inverse bound

\[
 D_U\leq23.3856903454031773371.
\tag{3.1}
\]

Its period column is the derivative with respect to the physical period
while the physical delays remain fixed.  In particular it includes both
$\tau_j/T$ terms in

\[
 \mathcal L(\theta X')=T
 \left(f+\sum_j\frac{\tau_j}{T}A_jS_jX'\right).
\tag{3.2}
\]

The bordered derivative is Fredholm of index zero on every fiber, the
nonconstant-mode lower bound stays positive on the common D1 ball, and the
regularity bridge above applies to periodic and generalized periodic
solutions.  The Fredholm-to-monodromy argument in the preceding note
therefore applies to every $b\in U$: bordered injectivity gives
$\ker\mathcal L_0=\operatorname{span}\{X_b'\}$, while the exact column
(3.2) excludes the rank-two Jordan vector.  Hence $1$ is algebraically
simple throughout $U$.

For a quantitative punctured neighborhood, let $r=5\times10^{-9}$ be the
common orbit/period correction radius, let $H_U$ bound the exact coefficient
in (2.2), and let $P_U$ bound $\|X_b'\|$.  The directed values are

\[
 H_U\leq0.456441843211688910,
 \qquad P_U\leq41.118999229531193.
\tag{3.3}
\]

With $T_-$ and $T_+$ from (1.2), set

\[
 \begin{aligned}
 c_{1,U}&=1+2(\tau_0+\tau_1)H_U,\\
 c_{2,U}&=T_+H_U
 \left[\left(\frac{\tau_0}{T_-}\right)^2
      +\left(\frac{\tau_1}{T_-}\right)^2\right]P_U.
 \end{aligned}
\tag{3.4}
\]

Define the certified decimal endpoint

\[
 \delta_0=
 0.00110371801789578632406620967700529547972127567300209121.
\tag{3.5}
\]

The complexified bordered-kernel estimate excludes every nontrivial kernel
for $0<|\varphi|\leq\delta_0$, uniformly on $U$.

Here the bordered inverse acts on the abstract complexification of the real
Wiener space.  The outer-arc proof below instead uses arbitrary complex
Fourier coefficients with a split real/imaginary norm.  The two norms are
not identified; the two spectral exclusions are joined only after they have
been proved on their respective phase sets.

## 4. Full-complex finite/tail cells

For $\varphi\ne0$, the Bloch operator does not preserve
$y_{-k}=\overline{y_k}$.  The outer proof therefore uses

\[
 \|y\|_{\mathrm{sp}}
 =\sum_k\bigl(
 |\Re y_{v,k}|+|\Im y_{v,k}|
 +|\Re y_{w,k}|+|\Im y_{w,k}|
 \bigr).
\tag{4.1}
\]

At cutoff $M=64$, the finite block contains

\[
 2(2M+1)=258
\tag{4.2}
\]

complex coordinates, or 516 real coordinates after realification.  No
real-conjugate layout is used.

Let $I=[c-\eta,c+\eta]$ be one positive phase cell; the final cell is
allowed to end at the directed endpoint $\bar\pi>\pi$ in (5.3).  At its
center use the block preconditioner

\[
 A_I=\operatorname{diag}(A_P,D_c^{-1}|_Q),
 \qquad (D_cy)_k=i(2\pi k+c)y_k,
\tag{4.3}
\]

where $A_P$ is the stored binary64 inverse candidate for
$P\mathcal L_cP$.  The directed lower bound for the tail gap is

\[
 d_I=2\pi(M+1)-c.
\tag{4.4}
\]

The term $\eta/d_I$ is retained because the tail inverse in (4.3) is fixed
at $c$ rather than allowed to vary with $\varphi$.

Write $K_I=I-A_I\mathcal L_\varphi$ and, for $R,S\in\{P,Q\}$, let
$Z_{RS,I}$ bound $\|RK_IS\|$, where the first subscript denotes the output
block.  Thus the two input-column bounds are

\[
 q_I=\max\{Z_{PP,I}+Z_{QP,I},
            Z_{PQ,I}+Z_{QQ,I}\}.
\tag{4.5}
\]

The cell is accepted only when $q_I<1$.

### 4.1 Exact-orbit coefficient bounds

Let $V_0=\|\bar v\|$, $C_0=\|\bar v-1\|$, and let $G_0,H_0$ be the
candidate norms of (2.2).  If $h_1=h_3=10^{-12}$, then

\[
 \begin{aligned}
 \Delta G
 &=(2V_0+r)r+\varepsilon h_1\\
 &\quad+3\varepsilon
 \{\kappa_{3,+}(2C_0+r)r+h_3C_0^2\},\\
 \Delta H
 &=\frac{\varepsilon}{2}
 \{h_1+3[\kappa_{3,+}(2C_0+r)r+h_3C_0^2]\}.
 \end{aligned}
\tag{4.6}
\]

The directed record gives

\[
 \Delta G\leq3.566725961732635\times10^{-8},
 \qquad
 \Delta H\leq2.198012944935347\times10^{-9}.
\tag{4.7}
\]

Let $\bar T_\pm$ be the candidate period-enclosure endpoints, whereas
$T_-=\bar T_--r$ and $T_+=\bar T_++r$ are the correction-ball endpoints.
Put
$G_+=G_0+\Delta G$, $H_+=H_0+\Delta H$, and

\[
 \Gamma_g=rG_++\bar T_+\Delta G.
\tag{4.8}
\]

For finite output modes, with $\varphi_+=c+\eta$, define

\[
 \Gamma^P_{H,j}
 =\sqrt2\left[
 rH_++\bar T_+\Delta H
 +H_0\tau_j(2\pi M+\varphi_+)\frac r{T_-}
 \right].
\tag{4.9}
\]

Then

\[
 \Gamma_{\mathrm{conv},P}=\Gamma_g+\sum_j\Gamma^P_{H,j},
 \qquad
 \Gamma_{PP}=\max\{\Gamma_{\mathrm{conv},P}+\varepsilon r,r\}.
\tag{4.10}
\]

For a tail output, put $\rho_I=1+\eta/d_I$ and

\[
 \Gamma^Q_{H,j}
 =\frac{\sqrt2}{d_I}(rH_++\bar T_+\Delta H)
  +\sqrt2H_0\tau_j\frac r{T_-}\rho_I,
\tag{4.11}
\]

so that

\[
 \Gamma_{QP}=\frac{\Gamma_g}{d_I}+\sum_j\Gamma^Q_{H,j}.
\tag{4.12}
\]

These estimates cover the complete D1 correction ball.  They do not assume
that the exact orbit has finite Fourier support.

### 4.2 Phase Taylor bounds and the four blocks

At the candidate center define

\[
 \begin{aligned}
 a&=\|A_P\|, &
 \epsilon_0&=\|I-A_PP\mathcal L_cP\|,\\
 \mu&=\|A_P(P\mathcal L_cP)'\|, &
 \nu&\geq\frac12\|A_P(P\mathcal L_cP)''\|,\\
 p_0&=\|A_PP\mathcal L_cQ\|, &
 p_1&=\|A_P(P\mathcal L_cQ)'\|,\\
 q_0&=\|D_c^{-1}Q\mathcal L_cP\|, &
 q_1&=\|D_c^{-1}(Q\mathcal L_cP)'\|.
 \end{aligned}
\tag{4.13}
\]

The products in (4.13) are evaluated directly.  Replacing $\mu$ by the
much larger product $a\|\mathcal L_c'\|$ would destroy the useful cell
width near the unit multiplier.

The complete cell bounds are

\[
 \begin{aligned}
 Z_{PP,I}
 &=\epsilon_0+\eta\mu+\eta^2\nu+a\Gamma_{PP},\\
 Z_{PQ,I}
 &=p_0+\eta p_1+\eta^2p_2+a\Gamma_{\mathrm{conv},P},\\
 Z_{QP,I}
 &=q_0+\eta q_1+\eta^2q_2+\Gamma_{QP},\\
 Z_{QQ,I}
 &=\frac{\eta}{d_I}
 +\frac{T_+}{d_I}
 \max\{G_++2\sqrt2H_++\varepsilon,1\}.
 \end{aligned}
\tag{4.14}
\]

More explicitly, the common second-order remainder is bounded by

\[
 R_2=\frac{\bar T_+\sqrt2 H_0}{2}
 \left[
   \left(\frac{\tau_0}{\bar T_-}\right)^2+
   \left(\frac{\tau_1}{\bar T_-}\right)^2
 \right],
 \qquad p_2=\nu=aR_2,
 \qquad q_2=\frac{R_2}{d_I}.
\tag{4.15}
\]

Thus the Taylor factor $1/2$, the split-complex factor $\sqrt2$, and the
period/delay scaling are explicit.  Both $P\leftarrow Q$ and
$Q\leftarrow P$ are retained.  The unknown orbit correction may place
Fourier mass at arbitrary tail modes;
neither cross block can be set to zero from the finite support of the
candidate.

If (4.5) holds, then $A_I\mathcal L_\varphi$ is invertible by a Neumann
series.  In particular $\mathcal L_\varphi$ is injective, which is the
property needed to exclude a Floquet eigenfunction.

## 5. Directed arithmetic and the complete cover

Every theorem endpoint is evaluated with 160-bit MPFR directed rounding.
NumPy supplies only stored binary64 inverses and products.  They are treated
as exact arrays of binary numbers; Higham's $\gamma_n$ bound, a gradual-
underflow correction, and the interval distance from the exact coefficient
boxes bound the true products.  Complex matrices are realified as

\[
 \mathfrak R(A)=
 \begin{pmatrix}\Re A&-\Im A\\ \Im A&\Re A\end{pmatrix},
\tag{5.1}
\]

whose ordinary real $\ell^1$ norm is exactly (4.1).

The tracked record binds the proof module, driver, seven-file local source
dependency manifest, source parameter-box result, binary orbit fingerprint,
and loaded OpenBLAS library by SHA-256.  Its two column sums, $q_I$, and
$1-q_I$ are exact decimal recombinations of the four displayed block
bounds, so an external exact-rational checker can replay every strict
inequality without relying on hidden decimal-rounding slack.

Starting from the exact decimal endpoint $\delta_0$ in (3.5), the proof
uses 319 connected cells with nominal relative half-width

\[
 \frac{\eta}{c}=\frac1{80}.
\tag{5.2}
\]

The last cell is clipped outward to

\[
 3.14159265358979323846264338327950288419716939937909994,
\tag{5.3}
\]

which encloses the exact irrational endpoint $\pi$.  Adjacent cell
endpoints are equal as exact decimal rationals.

All 319 cells pass.  The global directed values are

\[
 \max_Iq_I
 \leq0.702632589520429562469789734051424685161919418833034141,
\tag{5.4}
\]

and

\[
 \min_I(1-q_I)
 \geq0.297367410479570437530210265948575314838080581166965859.
\tag{5.5}
\]

The maximum occurs in cell 318 (one-based indexing),

\[
 I_{318}=
 [3.05366349826788494697,\,3.13097143493289469247],
\tag{5.6}
\]

where

\[
 \begin{aligned}
 Z_{PP}+Z_{QP}&\leq0.70263258952042956247,\\
 Z_{PQ}+Z_{QQ}&\leq0.47170275417027465512.
 \end{aligned}
\tag{5.7}
\]

The positive cells prove exclusion on $[\delta_0,\pi]$.  Since the exact
branch is real,

\[
 (Cy)_k=\overline{y_{-k}},
 \qquad C\mathcal L_\varphi=\mathcal L_{-\varphi}C,
\tag{5.8}
\]

so the negative arc follows by conjugation with mode reversal.  Combining
(3.5), the positive cover, (5.8), and algebraic simplicity at $1$ proves
Theorem 1.1.

## 6. Reproduction, refusal, and remaining gates

From the repository root run

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_bloch_outer_validation.py
```

and test with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_bloch_outer_validation.py
```

The computation refuses a mismatched parameter-box digest, a different
candidate fingerprint, an invalid branch or bordered inverse, or a
nonpositive tail gap.  It refuses to set the theorem flag for a phase-cover
gap, an endpoint below directed $\pi$, a structurally mismatched cell, or
any cell with $q_I\geq1$.  The executable driver does not accept external
decimal block declarations: it manufactures every cell from the bound
formulas and then checks its hashes, dimensions, phase declaration,
structural identities, exact decimal block sums, and strict contraction
before assembly.

This result closes the Floquet gate in the periodic-control program.  It
does not supply

1. a stability index proving attraction;
2. the separate transverse-network Halanay hypothesis;
3. a directed second-sensitivity bound for the response derivative; or
4. the physical reset/separator constants and the final safe target radius.

Consequently issue 15 remains open even though its synchronous Floquet
subgate is now proved.
