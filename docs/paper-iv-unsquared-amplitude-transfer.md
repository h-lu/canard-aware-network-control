# A source-bound unsquared-amplitude target ball for the periodic FHN branch

Status: **the uniform positive voltage-amplitude enclosure and the
two-output frequency--unsquared-amplitude target ball are proved by an
independent directed replay.** The binary64 Fourier record is exact input
data for a finite polynomial, not an exact RFDE orbit. A conditional third
coordinate follows in any common quantified calibration chart. No numerical
calibration width or physical pulse-onset identification is claimed here.

The proof implementation is
[fhn_unsquared_amplitude_transfer.py](../src/canard_control/fhn_unsquared_amplitude_transfer.py),
the source-bound driver is
[fhn_unsquared_amplitude_transfer.py](../experiments/fhn_unsquared_amplitude_transfer.py),
and the generated record is
[fhn_unsquared_amplitude_transfer.json](../experiments/results/fhn_unsquared_amplitude_transfer.json).
The refusal and composition tests are in
[test_fhn_unsquared_amplitude_transfer.py](../tests/test_fhn_unsquared_amplitude_transfer.py).

## 1. The missing coordinate step

The established response theorem concerns

\[
 P(b)=(F(b),R_h(b)),
 \qquad R_h(b)=A(b)^2,
 \qquad
 A(b)=\max_\theta V_b(\theta)-\min_\theta V_b(\theta).
\tag{1.1}
\]

It proves that a closed gain ball about \(b_c=(0.2,0.25)\) covers a
nonzero Euclidean ball about the **exact** output \(P(b_c)\). That theorem
cannot simply be relabeled as an \((F,A)\) theorem. The map
\(R_h\mapsto\sqrt{R_h}\) is singular at zero, and a forward Lipschitz bound
for the square-root image would be an outer estimate, not an inner ball
known to be covered by the response map.

Two additional ingredients are needed:

1. a uniform exact-orbit enclosure
   \(0<A_-\le A(b)\le A_+<\infty\) on the whole gain box; and
2. an inverse-coordinate calculation that maps every target in a proposed
   \((F,A)\) ball into the already covered \((F,R_h)\) ball.

Both ingredients are supplied below.

## 2. Source, space, and correction-ball contract

Let

\[
 U=[0.199999999999,0.200000000001]
 \times[0.249999999999,0.250000000001].
\tag{2.1}
\]

The \(129\)-node binary64 candidate record determines one finite
real-conjugate Fourier polynomial
\(\bar x=(\bar v,\bar w,\bar T)\). Each stored binary64 number is treated
as its exact dyadic rational value when inserted into an MPFR interval.
This makes \(\bar x\) exact *polynomial data*. It does not make \(\bar x\)
an RFDE solution.

The fresh parameter-box replay proves, for every \(b\in U\), a unique
phase-fixed exact periodic solution \(x_b\) satisfying

\[
 \|x_b-\bar x\|_\square\le \rho_x,
 \qquad \rho_x=5\times10^{-9},
\tag{2.2}
\]

where

\[
 \|(v,w,T)\|_\square
 =\sum_k\bigl(
 |\Re v_k|+|\Im v_k|+|\Re w_k|+|\Im w_k|
 \bigr)+|T|
\tag{2.3}
\]

is the real-conjugate component-Wiener product norm. Hence

\[
 \sup_\theta |V_b(\theta)-\bar V(\theta)|\le \rho_x.
\tag{2.4}
\]

This is coefficient-space algebra. It neither differentiates a point delay
as a bounded operator on \(C^0\) nor uses point-delay operator-norm
continuity on \(C^0\).

The replay also repeats the \(4096\)-cell directed derivative exclusion and
the RFDE curvature calculation. Every \(V_b\) therefore has one maximum and
one minimum, whose phases lie in the common outward dyadic enclosures

\[
\begin{aligned}
 I_+={}&[
 0.0971789956092834472656249999999999999999999999999144715,\\
 &\hspace{14mm}
 0.0971790552139282226562500000000000000000000000000855285],\\
 I_-={}&[
 0.798113957047462463378906249999999999999999999999315772,\\
 &\hspace{14mm}
 0.798114016652107238769531250000000000000000000000684228].
\end{aligned}
\tag{2.5}
\]

The floating extrema used to locate search neighborhoods are not theorem
values. Every accepted endpoint sign, curvature bound, and Fourier
evaluation on (2.5) is directed.

### Source binding

The new driver does more than read values from the floating candidate:

- it pins the exact candidate-file SHA-256;
- it reconstructs the binary64 arrays and reruns D1, D3, and D4;
- after JSON normalization, it requires the reconstructed parameter
  validation to agree field by field with the tracked parameter-box record;
- it derives a fresh \((F,R_h)\) target radius from that reconstructed
  validation and requires exact agreement with the tracked target record;
  and
- it records hashes of every transitive proof source used in the replay.

Thus the new certificate proves its squared-range target ball from the same
candidate polynomial and correction ball used for the amplitude enclosure.
It does not infer branch identity merely from two old summary files.
Equality with the tracked parameter and target records is an additional
consistency check. Matching a few sampled extrema would not satisfy these
checks.

## 3. Uniform exact-orbit amplitude enclosure

For a phase interval \(I\), let
\(\operatorname{Eval}(\bar v,I)\) denote MPFR-directed evaluation of the
finite real-conjugate Fourier polynomial. Equations (2.2)--(2.5) imply

\[
\begin{aligned}
 V_{\max}(b)&\in
 \operatorname{Eval}(\bar v,I_+)+[-\rho_x,\rho_x],\\
 V_{\min}(b)&\in
 \operatorname{Eval}(\bar v,I_-)+[-\rho_x,\rho_x]
\end{aligned}
\tag{3.1}
\]

for every \(b\in U\). The directed replay returns

\[
\begin{aligned}
 V_{\max}(b)&\in[
 1.93406327151920518409809759858497216615671825444576443,\\
 &\hspace{34mm}
 1.93406459386103160099698801611228051168771028922940805],\\
 V_{\min}(b)&\in[
 -1.01331410191142478456039139637915704642138299865115011,\\
 &\hspace{34mm}
 -1.01331295150622793179457944748716070850262680731264519].
\end{aligned}
\tag{3.2}
\]

Subtracting the intervals proves the following statement.

> **Theorem 3.1 (uniform unsquared voltage amplitude).** Every exact
> phase-fixed periodic orbit on \(U\) has one voltage maximum and one
> voltage minimum, and
> \[
> \boxed{
> 2.94737622302543311589267704607213287465934506175704116
> \le A(b)\le
> 2.94737869577245638555737941249143755810909328788192661.}
> \tag{3.3}
> \]
> In particular, \(A(b)>0\) uniformly on the entire gain box.

The proof does not require the candidate phases to equal the exact extrema.
The exact extrema may move anywhere inside (2.5); interval Fourier
evaluation plus the Wiener correction covers that movement.

A coarser proof would also be possible without isolating extrema: evaluate
the candidate at two fixed dyadic phases for a lower oscillation bound, use
twice the nonconstant Fourier coefficient \(\ell^1\) norm for an upper
bound, and subtract or add \(2\rho_x\). The present route is sharper and is
already tied to D3, which is needed for the response derivative.

## 4. General square-to-amplitude inner-ball lemma

The coordinate geometry is independent of the FHN calculation.

> **Lemma 4.1 (inner ball under \(R=A^2\)).** Let \(D\) be a parameter
> domain and suppose
> \[
> P(D)\supseteq\overline B_\rho(F_c,A_c^2),
> \qquad P(b)=(F(b),A(b)^2),
> \tag{4.1}
> \]
> with a unique preimage in \(D\) for every point of the displayed ball.
> Suppose
> \[
> 0<A_-\le A_c\le A_+.
> \tag{4.2}
> \]
> If \(r>0\) satisfies
> \[
> r\le\rho,\qquad
> r\le A_-/2,\qquad
> (2A_++r)r\le\rho,
> \tag{4.3}
> \]
> then, for \(Q(b)=(F(b),A(b))\),
> \[
> Q(D)\supseteq\overline B_r(F_c,A_c),
> \tag{4.4}
> \]
> and every point of this ball has a unique preimage in \(D\).

**Proof.** Write a target displacement in \((F,A)\) coordinates as
\((x,y)\), where \(x^2+y^2\le r^2\). The corresponding displacement in
\((F,R)\) is

\[
 (x,\,2A_cy+y^2).
\tag{4.5}
\]

Put \(L=2A_++r\). Since \(|y|\le r\),

\[
 |2A_cy+y^2|\le L|y|.
\tag{4.6}
\]

Therefore

\[
\begin{aligned}
 \|(x,2A_cy+y^2)\|_2
 &\le \max\{1,L\}\,\|(x,y)\|_2\\
 &\le \max\{r,Lr\}\le\rho.
\end{aligned}
\tag{4.7}
\]

The two separate conditions \(r\le\rho\) and \(Lr\le\rho\) in (4.3)
are essential when \(L\) is not known a priori to exceed one. Equation
(4.1) now supplies a unique \(b\in D\). Moreover,

\[
 A_c+y\ge A_- - r\ge A_-/2>0.
\tag{4.8}
\]

Because exact amplitude is nonnegative,
\(A(b)^2=(A_c+y)^2\) implies \(A(b)=A_c+y\). Thus \(Q(b)\) is the target,
and uniqueness follows from uniqueness in (4.1). Non-strict inequalities
prove the closed-ball statement, including its boundary. If the target
satisfies \(\|(x,y)\|_2<r\), then (4.7) is strict and the corresponding
squared-range target lies in the open ball. \(\square\)

A convenient admissible value is

\[
 r_*=\min\left\{
 \rho,\frac{A_-}{2},
 \sqrt{A_+^2+\rho}-A_+
 \right\},
\tag{4.9}
\]

where the last term is evaluated without cancellation as

\[
 \sqrt{A_+^2+\rho}-A_+
 =\frac{\rho}{\sqrt{A_+^2+\rho}+A_+}.
\tag{4.10}
\]

Equations (4.5)--(4.7), rather than a forward square-root Lipschitz
estimate, are what prove an inner target ball.

## 5. Validated FHN frequency--amplitude ball

The directed derivative-box theorem gives

\[
 \rho_P\ge
 1.62187273782174089504757331762715967009378618047942197
 \times10^{-14}
\tag{5.1}
\]

for the \((F,R_h)\) target ball. Substituting (3.3) and (5.1) into
(4.9)--(4.10) gives the public lower radius

\[
 \rho_A=
 2.75138166016477172021072951467987182906462947064987861
 \times10^{-15}.
\tag{5.2}
\]

All displayed endpoints are exact public decimals. The implementation
parses \(A_-\) downward, \(A_+\) upward, and \(\rho_P\) downward. It
computes (4.10) with directed intervals, reduces the lower endpoint by a
relative \(2^{-100}\) serialization margin, serializes it downward, reparses
the public value, and checks the inequalities in (4.3) using the reparsed
upper endpoint. The final composition check is

\[
 (2A_++\rho_A)\rho_A
 \le
 1.62187273782174089504757331762588023809767484061035673
 \times10^{-14}
 <\rho_P.
\tag{5.3}
\]

The frequency-coordinate check \(\rho_A<\rho_P\) and the positivity check
\(\rho_A<A_-/2\) are also made with directed reparsed endpoints.

> **Corollary 5.1 (frequency--unsquared-amplitude target ball).** Let
> \(D=\overline B_{10^{-12}}(b_c)\). The image of \(D\) under
> \[
> Q(b)=(F(b),A(b))
> \tag{5.4}
> \]
> contains the closed Euclidean ball of radius \(\rho_A\) in (5.2) about
> the exact output \(Q(b_c)\). Every target in the closed ball has a unique
> gain pair in \(D\). Every target satisfying the strict radius inequality
> has its unique gain pair in the open input ball.

The center \(Q(b_c)\) is the output of the exact validated RFDE orbit. Its
amplitude is enclosed by (3.3), but it is not replaced by the binary64
candidate amplitude.

The radius in (5.2) is microscopic because the validated gain half-width is
only \(10^{-12}\). The result closes the coordinate-transfer gap; it is not
evidence of a laboratory-scale control range.

## 6. Conditional calibrated safety coordinate

Assume separately that one common model supplies a fixed normalized safety
coordinate \(s\) on

\[
 D\times(-R_s,R_s),\qquad R_s>0,
\tag{6.1}
\]

and that in this calibrated chart the output is exactly

\[
 \mathcal Q_{\mathrm{cal}}(b,s)=(F(b),A(b),-s).
\tag{6.2}
\]

> **Corollary 6.1 (conditional three-output ball).** Under (6.1)--(6.2),
> the image contains the open Euclidean ball about
> \(\mathcal Q_{\mathrm{cal}}(b_c,0)\) of radius
> \[
> \rho_{A,s}=\min\{\rho_A,R_s\}.
> \tag{6.3}
> \]
> Every target in this ball has a unique preimage in the product domain.

Corollary 5.1 determines \(b\), and the identity \(s=-z_3\) determines the
third input. This is conditional because the amplitude certificate does not
supply \(R_s\), a raw-preset inverse, or hardware containment. It also does
not identify the calibrated gap with an unforced biological first-hit onset
or a maximal-canard root.

## 7. Proof dependency graph

\[
\begin{array}{c}
 \text{exact binary64 Fourier polynomial and source hash}\\
 \downarrow\\
 \text{uniform D1 Wiener correction ball on }U\\
 \downarrow\\
 \text{D3 derivative exclusion and common extrema brackets}\\
 \downarrow\\
 \text{directed Fourier evaluation plus correction radius}\\
 \downarrow\\
 0<A_-\le A(b)\le A_+\\
 \text{D4 derivative box}\longrightarrow
 \text{proved }(F,R_h)\text{ target ball}\\
 \searrow\hspace{22mm}\swarrow\\
 \text{Lemma 4.1}\longrightarrow
 \text{proved }(F,A)\text{ target ball}\\
 \downarrow\quad\text{if a quantified calibration chart exists}\\
 \text{conditional }(F,A,-s)\text{ target ball}.
\end{array}
\tag{7.1}
\]

No Floquet-attraction statement and no physical-onset statement is used in
the square-to-amplitude coordinate transfer.

## 8. Claim ledger

| Claim | Status |
|---|---|
| Binary64 values are exact dyadic data for one finite Fourier polynomial | **Proved by exact float-to-MPFR enclosure** |
| The binary64 polynomial is itself an exact RFDE orbit | **False; explicitly not claimed** |
| The exact orbit lies in the \(5\times10^{-9}\) Wiener correction ball for all \(b\in U\) | **Proved by fresh D1 replay** |
| One voltage maximum and one minimum on the whole gain box | **Proved by fresh D3 replay** |
| Uniform positive unsquared-amplitude enclosure (3.3) | **Proved** |
| Fresh \((F,R_h)\) target ball and amplitude enclosure use the same branch | **Proved in one replay; equality with tracked records is also checked** |
| Nonzero \((F,A)\) target ball (5.2) | **Proved** |
| Numerical three-output radius | **Open until a numerical \(R_s\) in a common calibration chart is supplied** |
| Formula \(\min\{\rho_A,R_s\}\) in an exact calibrated chart | **Proved conditionally** |
| Raw actuator containment, biological pulse onset, or maximal-canard identification | **Open / not asserted** |
| Macroscopic robustness of the target ball | **Not supplied; the present radius is microscopic** |

The mathematical advance is narrow but genuine: the observable is now the
physical unsquared voltage excursion rather than its algebraic square, and
the response image contains a rigorously certified nonzero inner ball. The
remaining obstacle is no longer the square-root coordinate; it is the
independent biological calibration/onset theorem and the size of its
admissible chart.
