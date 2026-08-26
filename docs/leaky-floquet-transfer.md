# Neutral Floquet transfer for the leaky periodic branches

Status: **proved for both validated leaky branches.**  The history-space
monodromy of each branch has the autonomous multiplier (1) with algebraic
multiplicity one.  Directed estimates also exclude every nontrivial unit
multiplier on an explicit punctured arc about (1).  Full unit-circle
exclusion and both unstable-multiplier counts remain open.

The executable theorem carrier is
[leaky_floquet_transfer.py](../src/canard_control/leaky_floquet_transfer.py),
the generator is
[leaky_floquet_transfer.py](../experiments/leaky_floquet_transfer.py), and
the source-bound record is
[leaky_floquet_transfer.json](../experiments/results/leaky_floquet_transfer.json).
The argument consumes, but does not rewrite, the separately validated inner
and outer periodic-orbit artifacts.

## 1. Result

Fix

\[
 \varepsilon=\frac15,\qquad a=\frac14,\qquad
 \kappa _1=\frac1{250},\qquad \kappa _3=\frac1{200},
 \qquad (\tau _0,\tau _1)=(4\sqrt5,5\sqrt5),
\tag{1.1}
\]

and consider

\[
\begin{aligned}
 \dot v={}&v-\frac{v^3}{3}-w
 +\varepsilon\kappa _1
 \left(\frac{v(t-\tau _0)+v(t-\tau _1)}2-v\right)\\
 &+\varepsilon\kappa _3
 \left(\frac{(v(t-\tau _0)-1)^3+(v(t-\tau _1)-1)^3}{2}
 -(v-1)^3\right),\\
 \dot w={}&\varepsilon(v-a-w).
\end{aligned}
\tag{1.2}
\]

The source-bound radii arguments already give two distinct nonconstant
periodic solutions: the inner branch (Gamma_u) and the outer branch
(Gamma_p).  Let (M_u) and (M_p) denote their history-space
monodromy operators.

> **Theorem 1.1 (neutral multipliers of the leaky branches).**  The
> multiplier (1) is an algebraically simple eigenvalue of both (M_u)
> and (M_p).  Moreover, there are explicit directed numbers
> (delta_u>0) and (delta_p>0) such that
> \[
>  0<|\varphi|\leq\delta_i
>  \quad\Longrightarrow\quad
>  e^{i\varphi}\notin\sigma(M_i),
>  \qquad i\in\{u,p\}.
> \tag{1.3}
> \]
> The validated lower bounds are approximately
> \[
>  \delta_u>3.9588\times10^{-3},\qquad
>  \delta_p>2.8635\times10^{-3}.
> \tag{1.4}
> \]

The theorem proves neither
(sigma(M_i)\cap\{|\lambda|=1\}=\{1\}) nor the number of multipliers
with modulus greater than one.  Thus it does not yet prove that
(Gamma_p) attracts or that (Gamma_u) has precisely one unstable
multiplier.

## 2. The exact period column

Write (X(\theta)=x(T\theta)) and
(alpha_j=\tau_j/T).  Along either exact orbit, the normalized periodic
variational operator is

\[
 \mathcal Ly=y'-TA_0y-T\sum_{j=0}^1A_j\mathcal S_{\alpha_j}y.
\tag{2.1}
\]

The physical delays stay fixed when (T) varies.  Consequently the period
column of the normalized orbit equation is (-b), where

\[
 b=f+\sum_{j=0}^1\frac{\tau_j}{T}
       A_j\mathcal S_{\alpha_j}X'.
\tag{2.2}
\]

In particular, the recovery component is

\[
 (D_T\Phi)_w=-\varepsilon(v-a-w),
\tag{2.3}
\]

not the non-leaky expression (-\varepsilon(v-a)).  Direct
differentiation gives the decisive Jordan identity

\[
 \mathcal L(\theta X')=Tb.
\tag{2.4}
\]

Both source orbit validators contain (2.2)--(2.3), including every
moving-delay contribution, and their source manifests are checked before
the transfer is admitted.

## 3. From the bordered inverse to algebraic simplicity

Let (E_1\hookrightarrow E_0) be the periodic Wiener derivative domain
and base space used by the radii proof, and let (ell) be its phase
functional.  The validated bordered derivative is

\[
 \mathcal B(y,\sigma)
   =(\mathcal Ly-b\sigma,\ell(y)).
\tag{3.1}
\]

The derivative (d/d\theta:E_1\to E_0) is Fredholm of index zero.
The current and delayed terms are lower-order relatively compact
perturbations, and adjoining one domain and one range scalar preserves the
index.  The radii theorem proves that (mathcal B) is bijective.

Autonomy gives (mathcal LX'=0).  Injectivity of (3.1) first yields

\[
 \ker\mathcal L=\operatorname{span}\{X'\},
 \qquad \ell(X')\ne0.
\tag{3.2}
\]

It also yields (b\notin\operatorname{Ran}\mathcal L): otherwise a
phase-adjusted preimage of (b) would give a nonzero vector in
(ker\mathcal B).  This range obstruction is the step that goes beyond
geometric simplicity.

Let (p_0) be the tangent history.  A rank-two Jordan vector for the
history monodromy would produce a variational solution satisfying

\[
 u(t+T)=u(t)+\dot x(t).
\tag{3.3}
\]

Then
(z(\theta)=u(T\theta)-\theta X'(\theta)/T) is periodic and, by (2.4),
satisfies (mathcal Lz=-b), contradicting the range obstruction.  The
converse construction shows that this is an equivalence, not merely a
necessary condition.

The remaining function-space seam is also closed.  The polynomial RFDE
and its fixed translations bootstrap the validated Wiener orbit and its
variational coefficients to smoothness.  Since
(T_i>\max\{\tau_0,\tau_1\}) on both correction balls, each one-period
monodromy is compact.  Every nonzero eigenhistory, and every periodicized
rank-two generalized history at (1), lies in the range of a smoothing
iterate and then in the validated Fourier domain.  Thus the Fourier
kernel and range obstruction see all history-space Jordan chains.

## 4. Directed local Bloch exclusion

For (s=i\varphi), periodicization of a unit-modulus Floquet solution gives

\[
 \mathcal L_s y
 =y'+sy-TA_0y
 -T\sum_j e^{-s\alpha_j}A_j\mathcal S_{\alpha_j}y=0.
\tag{4.1}
\]

Complexify the real validated inverse with the split real/imaginary norm.
If (D_i) bounds (|\mathcal B_i^{-1}|), the exact cancellations from
(2.4) yield

\[
 \|C_sy\|\le c_{1,i}|s|\|y\|,
 \qquad
 \|C_sX_i'-sT_ib_i\|\le c_{2,i}|s|^2,
\tag{4.2}
\]

where (C_s=\mathcal L_s-\mathcal L).  Hence a kernel is impossible if

\[
 D_ic_{1,i}|s|<1,
 \qquad D_ic_{2,i}|s|<T_i.
\tag{4.3}
\]

The coefficient of a delayed voltage variation is

\[
 H_v(v)=\frac{\varepsilon\kappa_1}{2}
       +\frac{3\varepsilon\kappa_3}{2}(v-1)^2.
\tag{4.4}
\]

Using the full correction ball, the implementation bounds

\[
 c_{1,i}=1+2(\tau_0+\tau_1)\|H_v(v_i)\|,
\tag{4.5}
\]

and the corresponding second-order coefficient in (4.2).  The recovery
leak does not create a new Bloch phase term, but it changes the state-field
Lipschitz estimate used to bound (|X_i'|): the recovery input column is

\[
 1+\varepsilon,
\tag{4.6}
\]

not (1).  This change is included explicitly.  The certified radius is
one half of the smaller directed threshold in (4.3), so both inequalities
are strict.

## 5. Evidence and remaining gate

The transfer record binds the complete inner and outer result files, the
new theorem source, its generator, this note, and the generic RFDE transfer
theorem by SHA-256.  Its hostile validator rejects a different orbit
fingerprint, a missing bordered inverse, either omitted period-column term,
a correction ball crossing a nonpositive period, failure of
(T>\max\tau_j), or accidental promotion of any global Floquet flag.

Reproduce with

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_floquet_transfer.py

PYTHONPATH=src:.venv/lib/python3.14/site-packages /usr/bin/python3 -m pytest -q \
  tests/test_leaky_floquet_transfer.py
```

The next rigorous gate is a source-bound full-complex Bloch cover of
([\delta_i,\pi]) for each branch.  Even after that exclusion, a separate
deflated Riesz trace or determinant winding on an exterior annulus is
needed to prove the unstable counts (0) and (1).  Pointwise resolvent
invertibility alone does not determine either integer.
