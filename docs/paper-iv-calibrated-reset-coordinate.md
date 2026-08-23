# A calibrated complete-history reset coordinate

Status: **the local calibration theorem, exact block-diagonal response and
quantitative product-neighborhood inverse below are proved.** They apply to
the controlled collective-clamp separator, not to the open unforced canard or
biological first-hit threshold. A model-level FHN control theorem still
requires a validated laboratory implementation of the calibration map,
second-sensitivity bounds for a target radius, and, if attraction is claimed,
a stability index placing every nontrivial multiplier inside the unit disk.
The microscopic parameter-box periodic response gate is proved in
[paper-iv-periodic-parameter-box.md](paper-iv-periodic-parameter-box.md), and
the full synchronous unit-circle exclusion is proved in
[paper-iv-full-floquet-parameter-box.md](paper-iv-full-floquet-parameter-box.md).

The point of the construction is simple. A raw reset preset generally has a
threshold \(a_c(b)\) that drifts with the two baseline controls \(b\).
Instead of treating that drift as a third response row, use the
complete-history gap itself as the local reset coordinate. This is an exact
change of protocol coordinates; it is not an approximation and it does not
alter the baseline periodic experiment.

## 1. Complete-history calibration

Let \(b\in U\subset\mathbb R^2\) be the controls used in the baseline
periodic experiment. For the separate controlled pulse-decision experiment,
let

\[
 \Gamma(a,b)=G_b(\mathcal R(a,b))
\tag{1.1}
\]

be the jointly \(C^1\) complete-history separator gap of
[paper-iv-reset-only-block-control.md](paper-iv-reset-only-block-control.md).
Here \(a\) is a raw reset preset,
\(G_b=0\) is the controlled complete-history separator, and
\(\mathcal R(a,b)\) is the released-and-clamped history. Assume the two
signs of \(G_b\) label the declared local pulse and quiet channels, and

\[
 \Gamma(a_0,b_0)=0,
 \qquad \partial_a\Gamma(a_0,b_0)\ne0.
\tag{1.2}
\]

> **Theorem 1.1 (exact calibrated reset coordinate).** There are
> neighborhoods \(J_s\ni0\), \(U_0\ni b_0\), \(J_a\ni a_0\), and a unique
> jointly \(C^1\) map
>
> \[
>  \mathcal A:J_s\times U_0\longrightarrow J_a
> \tag{1.3}
> \]
>
> such that
>
> \[
>  \Gamma(\mathcal A(s,b),b)=s.
> \tag{1.4}
> \]
>
> At \(s=0\), \(\mathcal A(0,b)=a_c(b)\), where \(a_c(b)\) is the unique
> local raw-preset threshold, and
>
> \[
>  \partial_s\mathcal A=\frac1{\partial_a\Gamma},
>  \qquad
>  D_b\mathcal A=-\frac{D_b\Gamma}{\partial_a\Gamma},
> \tag{1.5}
> \]
>
> evaluated at \((\mathcal A(s,b),b)\). Therefore the pulled-back reset
> history
>
> \[
>  \mathcal R_{\rm cal}(s,b)
>  :=\mathcal R(\mathcal A(s,b),b)
> \tag{1.6}
> \]
>
> lies on the separator exactly when \(s=0\), and the signs of \(s\) are
> the two controlled channel sides.

**Proof.** Apply the inverse-function theorem to
\(\Psi(a,b)=(\Gamma(a,b),b)\). Its derivative is block triangular with
determinant \(\partial_a\Gamma(a_0,b_0)\ne0\). The local inverse has the
form \((s,b)\mapsto(\mathcal A(s,b),b)\), which proves (1.3)--(1.4).
Differentiating (1.4) proves (1.5). Equation (1.6) and the definition of
\(\Gamma\) give the last assertion. \(\square\)

The theorem does not say that a fixed raw preset is independent of \(b\).
It says that a parameter-dependent calibration of that preset gives an
exact signed coordinate. If the laboratory protocol cannot implement
\(\mathcal A(s,b)\), the general block-triangular theorem with threshold
gradient \(D_ba_c\) remains the relevant result.

The complete-history function \(G_b\) need not itself be an online
observable.  The command map may instead be tabulated from a validated model
or from boundary-calibration experiments.  Until one such realization and
its error bound are supplied, \(s\) is a rigorous protocol coordinate, not a
directly measured biological quantity.

Nor does a change of units create free actuator authority. If

\[
 |\partial_a\Gamma|\ge g>0,
 \qquad \|D_b\Gamma\|\le C_\Gamma,
\tag{1.7}
\]

then (1.5) gives the raw-command costs

\[
 |\partial_s\mathcal A|\le g^{-1},
 \qquad \|D_b\mathcal A\|\le C_\Gamma/g.
\tag{1.8}
\]

Thus the normalization of \(G\), the half-width of \(J_s\), and the
Jacobian of the command map \((b,s)\mapsto(b,\mathcal A(s,b))\) must be
fixed and bounded before (2.4) is interpreted as a physical conditioning
statement. A small \(g\) is not cured by renaming the input.

> **Corollary 1.2 (collective-clamp specialization).** Fix a sufficiently
> small positive \(\delta\) and a compact control set satisfying Theorem 5.1
> of
> [paper-iii-collective-clamp-separator.md](paper-iii-collective-clamp-separator.md).
> With \(\Gamma=g_\delta\), the hypotheses of Theorem 1.1 hold after
> shrinking the common reset interval. Hence the declared two-module
> collective-clamp protocol has a jointly \(C^1\) calibrated channel
> coordinate \(s\), and \(s=0\) is exactly its unique local
> complete-history pulse/quiet separator.

**Proof.** That theorem supplies a jointly \(C^1\) scalar
\(g_\delta(a,b)\), a unique zero \(a=0\), channel labels on its two signs,
and \(\partial_ag_\delta(0,b)\ne0\), uniformly on the compact control set
for the fixed \(\delta\). Compactness and continuity give a common
neighborhood on which the derivative remains nonzero. Apply Theorem 1.1.
\(\square\)

## 2. Exact three-output response

Let

\[
 P(b)=(F(b),A(b))
\tag{2.1}
\]

be frequency and squared observable range on a phase-fixed periodic branch.
The reset protocol is inactive during this baseline experiment. Orient the
calibrated safety margin as \(S_{\rm cal}=-s\) and define

\[
 \mathcal Q_{\rm cal}(b,s)=\bigl(P(b),-s\bigr).
\tag{2.2}
\]

> **Theorem 2.1 (block-diagonal calibrated controllability).** If \(P\)
> is \(C^1\) and
>
> \[
>  B=D_bP,
>  \qquad \sigma_{\min}(B)\ge\beta>0,
> \tag{2.3}
> \]
>
> then
>
> \[
>  D\mathcal Q_{\rm cal}
>   =\begin{pmatrix}B&0\\0&-1\end{pmatrix},
>  \qquad
>  \sigma_{\min}(D\mathcal Q_{\rm cal})
>   =\min\{\sigma_{\min}(B),1\}
>   \ge\min\{\beta,1\}>0.
> \tag{2.4}
> \]

**Proof.** The first two outputs do not depend on the reset-only coordinate
\(s\), while (1.4) makes the signed controlled gap exactly \(s\). Thus
(2.4) follows by differentiation and the singular values of a block-diagonal
matrix are the union of the singular values of its blocks. \(\square\)

This removes the canard-conditioning row cancellation from the response
written in calibrated protocol coordinates. It does not refute that
cancellation for three raw baseline actuators and does not bound raw
hardware effort: the calibrated reset is a separate experiment, and its
command map has the costs (1.8).

## 3. A quantitative product-neighborhood inverse

The calibration chart has a finite usable half-width. The following result
keeps that width separate from the periodic-response inverse radius.

> **Theorem 3.1 (covered target ball).** Suppose \(P\) is \(C^1\) on the
> closed \(b\)-ball of radius \(R_b\) about \(b_0\), this ball is contained
> in \(U_0\), and the calibration chart (1.3) is defined on the full product
>
> \[
>  (-R_s,R_s)\times \overline B_{R_b}(b_0)
>  \subset J_s\times U_0.
> \tag{3.0}
> \]
>
> Assume
>
> \[
>  \sigma_{\min}(D_bP(b_0))\ge\beta>0,
>  \qquad
>  \|D_bP(b)-D_bP(\widetilde b)\|_2
>       \le L\|b-\widetilde b\|_2,
> \tag{3.1}
> \]
>
> Put
>
> \[
>  r_b=\begin{cases}
>    R_b/2,&L=0,\\
>    \min\{R_b/2,\beta/(2L)\},&L>0,
>  \end{cases}
>  \qquad
>  \rho_b=\beta r_b-\frac L2r_b^2,
> \tag{3.2}
> \]
>
> and
>
> \[
>  \rho_{\rm cal}=\min\{\rho_b,R_s/2\}.
> \tag{3.3}
> \]
>
> Then the image of
>
> \[
>  \{\|b-b_0\|_2<r_b,\ |s|<R_s/2\}
> \tag{3.4}
> \]
>
> under \(\mathcal Q_{\rm cal}\) contains the Euclidean output ball of
> radius \(\rho_{\rm cal}\) about
> \(\mathcal Q_{\rm cal}(b_0,0)\). Every target in that ball has a unique
> preimage in (3.4).

**Proof.** The quantitative inverse theorem applied to \(P\) gives a
unique \(b\) for every two-output displacement of norm less than
\(\rho_b\). Set \(s\) equal to minus the requested safety displacement.
For a three-output target of norm less than (3.3), both requirements hold,
and (2.2) gives the unique preimage. \(\square\)

Here \(R_s\) is measured in the declared, fixed normalization of the
complete-history gap. The theorem certifies a target ball in calibrated
command coordinates. A raw-preset target radius additionally requires
bounds such as (1.7)--(1.8) and containment of
\(\mathcal A((-R_s,R_s),U_0)\) in the hardware range.

The executable formulas are in
[calibrated_reset_control.py](../src/canard_control/calibrated_reset_control.py),
with regression tests in
[test_calibrated_reset_control.py](../tests/test_calibrated_reset_control.py).
The block lower-bound helper propagates a supplied rigorous bound exactly;
the SVD and radius evaluators use ordinary binary64 arithmetic and are
diagnostics, not directed interval certificates.

## 4. Claim boundary

| Statement | Status |
|---|---|
| Local raw-preset to signed-gap calibration | **Proved** under the jointly \(C^1\) separator/reset hypotheses |
| Exact block-diagonal three-output response | **Proved** |
| Quantitative product-neighborhood target ball | **Proved conditionally on supplied \(L,R_b,R_s\); not yet instantiated for FHN** |
| Bounded raw-preset implementation of the calibrated command | **Conditional on fixed gap normalization, (1.7), and hardware-range containment** |
| Calibrated coordinate for the declared clamped two-module protocol | **Proved implication of the fixed-\(\delta\) separator theorem** |
| Parameter-box periodic FHN response lower bound | **Proved on the declared microscopic box; \(\beta_U\ge0.0162187\)** |
| Synchronous orbital Floquet hyperbolicity | **Proved uniformly on the microscopic gain box** |
| Floquet attraction and response-derivative Lipschitz bound | **Open; issue 15 remains open** |
| Unforced pulse threshold or maximal-canard identification | **Not asserted** |
