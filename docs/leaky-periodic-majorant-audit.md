# Independent audit of the leaky periodic majorants

Status: **the formula adaptation is proved, and the registered inner branch
passes the resulting directed radii theorem.**  This note audits only the
passage from the already established non-leaky Fourier/Wiener construction to
the recovery equation

\[
 w'=\varepsilon(v-a-w).
\tag{0.1}
\]

It does not transfer any Floquet spectrum from the old model.  In particular,
algebraic simplicity of the neutral multiplier, exclusion of other unit-circle
multipliers, and the unstable multiplier count remain open.

The proof formulas are implemented in
[leaky_periodic_majorant_audit.py](../src/canard_control/leaky_periodic_majorant_audit.py).
The branch calculation is in
[leaky_periodic_validation.py](../src/canard_control/leaky_periodic_validation.py),
and the source-locked polynomial is
[autonomous_leaky_recovery_inner_branch_artifact.json](../experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json).

## 1. Operator and norm

Let \(\mathcal A_{\mathbb R}\) be the real-conjugate Fourier Wiener algebra
with component complex norm

\[
 \|c\|_{\mathcal A}
 =\sum_{k\in\mathbb Z}(|\Re c_k|+|\Im c_k|).
\tag{1.1}
\]

For \(x=(v,w,T)\), use

\[
 \|x\|_\square=\|v\|_{\mathcal A}+\|w\|_{\mathcal A}+|T|.
\tag{1.2}
\]

The normalized phase-bordered coefficient map has recovery component

\[
 \mathcal F_w(v,w,T)
 =Dw-T\varepsilon(v-a-w).
\tag{1.3}
\]

The phase row used by the infinite calculation is the affine functional with
normal \(D\bar x\) and center \(\bar x\).  It need not equal the continuation
phase row that produced the floating-point candidate; the candidate satisfies
the new affine phase equation exactly, and this is the phase row enclosed by
the coefficient validator.

Write \(\mathcal F^0\) for the old map with recovery equation
\(Dw-T\varepsilon(v-a)\).  Their exact difference is

\[
 L(v,w,T):=\mathcal F-\mathcal F^0=(0,\varepsilon T w,0).
\tag{1.4}
\]

It follows without a remainder that

\[
 DL(v,w,T)[u]
 =(0,\varepsilon(Tu_w+w u_T),0)
\tag{1.5}
\]

and

\[
 \{DL(x+h)-DL(x)\}[u]
 =(0,\varepsilon(h_Tu_w+h_wu_T),0).
\tag{1.6}
\]

Equations (1.4)--(1.6) are the entire model-dependent adaptation at the
operator level.

## 2. Finite matrix and point defect

Suppose that \(\bar v\) and \(\bar w\) have Fourier support in
\(|k|\le m\), and take a cutoff \(M\ge3m\).  Let \(P\) project onto
\(|k|\le M\) together with the period and phase coordinates, and put
\(Q=I-P\).  On the tail use

\[
 (A_Qy)_k=(2\pi ik)^{-1}y_k.
\tag{2.1}
\]

Equation (1.4) adds \(\varepsilon\bar T\bar w\) to the recovery residual.
Equation (1.5) adds

\[
 D_w\mathcal F_w-D_w\mathcal F_w^0
   =\varepsilon\bar T I,
 \qquad
 \partial_T\mathcal F_w-\partial_T\mathcal F_w^0
   =\varepsilon\bar w.
\tag{2.2}
\]

These are precisely the two additions made by the finite coefficient-column
routine.  No other state, phase, or period entry changes.

Because multiplication by the scalars \(\varepsilon\bar T\) and
\(\varepsilon\), and multiplication of the scalar period input by the finite
polynomial \(\bar w\), do not change a Fourier index,

\[
 QDL(\bar x)P=0,
 \qquad
 PDL(\bar x)Q=0.
\tag{2.3}
\]

Thus the old finite-to-tail and tail-to-finite support searches transfer
unchanged.  The finite-to-finite matrix is recomputed with (2.2); it is not
borrowed from the old orbit.

For a recovery-tail input, the fast equation contributes the coefficient
\(1\), while (1.5) contributes \(\varepsilon\) in the recovery row.  Therefore
the recovery column of the lower-order tail operator is bounded by

\[
 1+\varepsilon.
\tag{2.4}
\]

After (2.1), its contribution is at most

\[
 \frac{\bar T(1+\varepsilon)}{2\pi(M+1)}.
\tag{2.5}
\]

This is the changed branch in the implemented tail-to-tail maximum.  The
voltage-tail column is unchanged, since the derivative of (1.4) with respect
to \(v\) is zero and the term \(-T\varepsilon v\) already belonged to the old
recovery equation.

## 3. Correction-ball derivative bound

Let

\[
 A=A_P\oplus A_Q,
 \qquad
 a_*:=\max\left\{\|A_P\|_1,
                  \frac1{2\pi(M+1)}\right\}.
\tag{3.1}
\]

For \(\|h\|_\square\le\rho\), the two nonzero input columns in (1.6) have
norms

\[
 \varepsilon|h_T|,
 \qquad
 \varepsilon\|h_w\|_{\mathcal A}.
\tag{3.2}
\]

The induced \(\ell^1\) operator norm is the maximum column sum, not the sum of
the two columns.  Consequently,

\[
 \|A\{DL(x+h)-DL(x)\}\|
 \le a_*\varepsilon\rho.
\tag{3.3}
\]

Hence, if the old derivative-variation bound is

\[
 \|A(D\mathcal F^0(\bar x+h)-D\mathcal F^0(\bar x))\|
 \le Z_1^0\rho+Z_2^0\rho^2+Z_3^0\rho^3,
\tag{3.4}
\]

then the leaky coefficients are valid with

\[
 Z_1=Z_1^0+a_*\varepsilon,
 \qquad Z_2=Z_2^0,
 \qquad Z_3=Z_3^0.
\tag{3.5}
\]

The implementation previously wrote \(\|A_P\|_1\varepsilon\).  The inner
artifact already had \(\|A_P\|_1\gg\|A_Q\|\), so its numerical bound was
unchanged.  The audited source now computes the maximum in (3.1) explicitly,
removing that hidden genericity assumption.

All other nonlinear terms are in the unchanged fast equation or in the old
part \(Dw-T\varepsilon(v-a)\).  The Wiener convolution bounds, exact delay
rotations, finite-output moving-delay estimate, tail cancellation of the
Fourier mode factor, real-conjugate coordinate weights, and directed
binary64 product bounds therefore transfer with the same hypotheses.  No
parameter-box or Floquet result transfers: those operators depend on different
parameters and on the orbit itself.

## 4. Radii theorem for the registered inner polynomial

For the 129-node inner polynomial, \(m=64\), \(M=192\), and
\(r=10^{-5}\).  At 160-bit directed precision the stored calculation gives

\[
\begin{aligned}
 Y&\le1.898922976421907\times10^{-13},\\
 Z_0&\le0.03154258666980007,\\
 Z_1&\le6002.004206791699,\\
 Z_2&\le2002.044979488625,\\
 Z_3&\le139.8649892414301.
\end{aligned}
\tag{4.1}
\]

Thus

\[
 q(r)=Z_0+Z_1r+Z_2r^2+Z_3r^3
 \le0.09156282894235487<1
\tag{4.2}
\]

and

\[
 r-\{Y+q(r)r\}
 \ge9.084371520684153\times10^{-6}>0.
\tag{4.3}
\]

> **Theorem 4.1 (inner leaky periodic orbit).**  For the exact decimal
> parameters \(\varepsilon=0.2\), \(a=0.25\), \(\Theta_0=4\),
> \(\Theta_1=5\), \(\kappa_1=0.004\), and \(\kappa_3=0.005\), the leaky
> two-delay RFDE has a unique phase-fixed periodic solution in the component
> Wiener ball of radius \(10^{-5}\) about the source-locked inner Fourier
> polynomial.  At that solution the phase-bordered coefficient derivative is
> bijective.  Its inverse, measured from the residual norm to the base
> component-Wiener norm, has norm at most
> \(120.3101842920348\).

The proof is the same contraction argument as for the baseline finite/tail
theorem after substituting (2.2), (2.4), and (3.5).  The tail fixed-point
identity first restores one Fourier derivative, so the fixed point is in the
domain of the RFDE coefficient operator.  Injectivity of the finite stored
preconditioner follows from its directed inverse defect; the analytic tail
preconditioner is coefficientwise injective.  Therefore a fixed point of the
preconditioned Newton map is a zero of the phase-bordered RFDE map.  The
uniform contraction bound also gives the asserted bordered derivative
inverse.

## 5. Exact claim boundary

The audit proves the leaky formula adaptation and, together with the tracked
directed artifact, the inner phase-fixed periodic orbit and its bordered
inverse.  It does **not** prove that the inner orbit has one unstable
multiplier.  The following remain separate gates:

1. Fredholm-to-history-monodromy algebraic-multiplicity transfer;
2. exclusion of nontranslation multipliers from the unit circle; and
3. a directed Riesz or winding count of unstable multipliers.

The outer polynomial has no registered full replay artifact and its present
Fourier resolution does not close an analogous radii inequality.  No outer
orbit or attracting-index claim is made here.
