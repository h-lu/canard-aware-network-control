# A direct target ball from the periodic FHN response box

Status: **the two-output frequency--squared-range target ball is proved.** The
argument uses the validated enclosure of the entire derivative family about
one fixed matrix. It does not require a second-sensitivity or Hessian bound.
The calibrated three-output extension is conditional on a quantified
complete-history calibration chart; no physical pulse-onset claim is made in
this note.

The executable certificate is
[`fhn_response_target_ball.py`](../src/canard_control/fhn_response_target_ball.py),
the driver is
[`fhn_response_target_ball.py`](../experiments/fhn_response_target_ball.py),
and the tracked result is
[`fhn_response_target_ball.json`](../experiments/results/fhn_response_target_ball.json).
Its SHA-256 digest is

```text
dc17c3f845c3e317570c71af3acff670fb6955e2920ad2cea256507c1353dc05
```

## 1. A fixed-derivative-box inverse theorem

Let \(U_+\subset\mathbb R^d\) be open, let \(P:U_+\to\mathbb R^d\) be
\(C^1\), and suppose that

\[
 \overline B_R(b_c)\subset U_+ .
\tag{1.1}
\]

Fix a matrix \(B_0\in\mathbb R^{d\times d}\).

> **Theorem 1.1 (direct derivative-box target ball).** Assume
>
> \[
>  \sigma_{\min}(B_0)\ge s_0>0,
>  \qquad
>  \sup_{b\in\overline B_R(b_c)}
>       \|DP(b)-B_0\|_2\le r_B<s_0.
> \tag{1.2}
> \]
>
> Put
>
> \[
>  \beta=s_0-r_B,
>  \qquad q=\frac{r_B}{s_0},
>  \qquad \rho=\beta R.
> \tag{1.3}
> \]
>
> Then \(q<1\), \(P\) is injective on
> \(\overline B_R(b_c)\), and
>
> \[
>  \|P(b)-P(\widetilde b)\|_2
>  \ge \beta\|b-\widetilde b\|_2
>  \qquad
>  (b,\widetilde b\in\overline B_R(b_c)).
> \tag{1.4}
> \]
>
> Moreover,
>
> \[
>  \overline B_\rho(P(b_c))
>     \subset P\bigl(\overline B_R(b_c)\bigr),
>  \qquad
>  B_\rho(P(b_c))\subset P\bigl(B_R(b_c)\bigr).
> \tag{1.5}
> \]
>
> Every target in either target ball has a unique preimage in the
> corresponding input ball.

**Proof.** Write

\[
 N(b)=P(b)-P(b_c)-B_0(b-b_c).
\tag{1.6}
\]

The line segment between two points of the closed input ball remains in that
ball. The fundamental theorem of calculus and (1.2) give

\[
 \|N(b)-N(\widetilde b)\|_2
 \le r_B\|b-\widetilde b\|_2.
\tag{1.7}
\]

Subtracting (1.7) from the lower singular-value estimate for \(B_0\) proves
(1.4). For a target displacement \(z\), consider

\[
 \mathcal T_z(b)
 =b_c+B_0^{-1}\{z-N(b)\}.
\tag{1.8}
\]

Its Lipschitz constant is at most \(r_B/s_0=q<1\). If
\(\|z\|_2\le\rho\), then, for \(b\in\overline B_R(b_c)\),

\[
 \|\mathcal T_z(b)-b_c\|_2
 \le\frac{\|z\|_2+r_BR}{s_0}\le R.
\tag{1.9}
\]

Thus \(\mathcal T_z\) is a contraction of the closed input ball into itself.
Its unique fixed point satisfies \(P(b)=P(b_c)+z\), proving the closed-ball
inclusion. If \(\|z\|_2<\rho\), the last inequality is strict, so the fixed
point lies in the open input ball. Equation (1.4) gives uniqueness in the
whole closed ball. \(\square\)

Hypothesis (1.2) is not merely the pointwise statement
\(\inf_b\sigma_{\min}(DP(b))>0\). It is the coherent enclosure of every
derivative about the **same** invertible matrix \(B_0\). That fixed center is
what makes (1.7) quantitative without estimating \(D^2P\). The abstract
argument is a quantitative inverse theorem; the new content used below is
the directed RFDE derivative-family enclosure to which it applies.

## 2. Directed FHN instantiation

For the synchronous two-delay FHN branch, take

\[
 P(\kappa_1,\kappa_3)
 =\left(T^{-1},(V_{\max}-V_{\min})^2\right),
 \qquad b_c=(0.2,0.25).
\tag{2.1}
\]

The parameter-box theorem proves a \(C^1\) branch on an open neighborhood of
the certified box and proves that its maximum and minimum are unique and
nondegenerate. Consequently \(P\) is \(C^1\). Its tracked derivative
enclosure is centered at the stored binary64 matrix, interpreted as an exact
dyadic matrix,

\[
 B_0=
 \begin{pmatrix}
  0.03669982799550202&0.13633946068777764\\
 -3.645615771771411&-6.136337974459385
\end{pmatrix}.
\tag{2.2}
\]

The displayed decimals are the shortest decimal renderings of four exact
binary64 numbers, not exact decimal input data. Their unambiguous hexadecimal
representations are

~~~text
[[ 0x1.2ca51e204de06p-5,  0x1.173924a6775cep-3],
 [-0x1.d2a389a0c51f1p+1, -0x1.88b9c2e960616p+2]]
~~~

The certificate converts those four IEEE values to exact dyadic intervals
before taking determinants or norms.

Directed determinant/Frobenius arithmetic and the four entrywise response
intervals give

\[
 \begin{aligned}
 s_0&\ge
 0.0380780707316509809056500398064619174206299619483928191,\\
 r_B&\le
 0.0218593433534335719551743066301903207196921001434632885,\\
 \beta=s_0-r_B&\ge
 0.0162187273782174089504757331762715967009378618048867663,\\
 q=\frac{r_B}{s_0}&\le
 0.574066462229238030186824143693907387195163195333072207<1.
 \end{aligned}
\tag{2.3}
\]

The Frobenius bound for \(DP-B_0\) is also a spectral-norm bound. The closed
Euclidean input ball of radius

\[
 R=10^{-12}
\tag{2.4}
\]

about \(b_c\) lies in the declared rectangular gain box. Theorem 1.1
therefore proves the following statement.

> **Corollary 2.1 (validated FHN frequency--squared-range target ball).** The
> image of \(\overline B_{10^{-12}}(b_c)\) under (2.1) contains the closed
> Euclidean ball about the exact output \(P(b_c)\) of radius
>
> \[
>  \boxed{\rho_P\ge
>  1.62187273782174089504757331762715967009378618047942197
>  \times10^{-14}.}
> \tag{2.5}
> \]
>
> Every target in this closed output ball has a unique gain pair in the
> closed input ball. Targets satisfying the strict radius inequality have
> their unique gain pair in the open input ball.

The center \(P(b_c)\) is the exact mathematical output of the validated
orbit, not the unvalidated binary collocation value. A numerical enclosure of
the center is unnecessary for this relative target-ball statement and is not
silently substituted for it.

## 3. Calibrated safety coordinate

Suppose a complete-history calibration theorem supplies a fixed normalized
gap coordinate \(s\) on the full product

\[
 (-R_s,R_s)\times\overline B_R(b_c),
 \qquad R_s>0,
\tag{3.1}
\]

and define

\[
 \mathcal Q_{\mathrm{cal}}(b,s)=(P(b),-s).
\tag{3.2}
\]

> **Corollary 3.1 (conditional calibrated three-output ball).** Under (3.1),
> the image of the product domain contains the open Euclidean output ball
> about \(\mathcal Q_{\mathrm{cal}}(b_c,0)\) of radius
>
> \[
>  \rho_{\mathrm{cal}}=\min\{\rho_P,R_s\}.
> \tag{3.3}
> \]
>
> Every target in this ball has a unique preimage in the product domain.

Indeed, Corollary 2.1 determines \(b\) from the first two target components,
and the exact identity \(s=-z_3\) determines the third. No derivative of the
calibration map enters after \(s\) has been adopted as the protocol
coordinate.

Corollary 3.1 is not by itself a model-level biological control theorem. The
generic raw-preset calibration still lacks a numerical \(R_s\), laboratory
actuator containment, and an identification with unforced biological onset.
A downstream
[same-model clamped separator](paper-iv-same-model-clamped-separator.md)
now supplies a different, exact operational coordinate \(s=r\) for the fixed
rank-one \(D=3,E=2\) instance. Its source-bound
[three-output composition](../src/canard_control/fhn_same_model_three_output.py)
proves the staged frequency--squared-range--operational-margin ball without
promoting it to an unforced or biological-basin theorem.

## 4. Claim boundary and remaining work

| Statement | Status |
|---|---|
| Uniform derivative enclosure about one fixed \(B_0\) | **Proved by the parameter-box certificate** |
| Two-output FHN target ball (2.5) | **Proved** |
| Second sensitivity or a Lipschitz constant for \(DP\) | **Not proved; not needed for (2.5)** |
| Calibrated three-output target-ball formula (3.3) | **Proved conditionally on a common quantified calibration chart** |
| Numerical calibration half-width and raw hardware containment | **Open** |
| Same-model periodic-response/separator and staged operational target ball | **Proved downstream for the fixed rank-one \(D=3,E=2\) instance** |
| Equality with unforced pulse onset or a maximal-canard root | **Not asserted** |
| Full-network transverse stability along the periodic orbit | **Proved downstream for the fixed rank-one family; not supplied by this theorem alone** |
| Attraction | **Open; transverse stability does not determine the synchronous stability index** |

Second sensitivities remain useful for enlarging the certified input region,
controlling raw-coordinate derivatives, and obtaining conventional
\(C^{1,1}\) robustness estimates. They are no longer a logical prerequisite
for a nonzero periodic frequency--squared-range target radius on the current
box. Transfer from \(R_h\) to the unsquared voltage range requires a separate
positive range enclosure and coordinate-change estimate; that amplitude
target ball is not claimed here.
