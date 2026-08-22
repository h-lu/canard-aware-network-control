# The reduced canard root: a second-order parameterized splitting result

Status: **exact normalization and symbolic integrands, plus a conditional
second-order splitting template.** The compact-tube graph's finite-order
mixed regularity and the selected K1/tail estimates are not yet proved. Until
both are closed, the Gaussian coefficient and selected reduced root below are
conditional calculations rather than theorem outputs.

The executable algebraic audit is
[reduced_canard_root.py](../src/canard_control/reduced_canard_root.py).
It checks the normalization and every integral used below. It does not
replace the geometric K1 argument.

## 1. Which Krupa--Szmolyan result is relevant

The relevant primary source is Krupa and Szmolyan,
[Extending Geometric Singular Perturbation Theory to Nonhyperbolic
Points--Fold and Canard Points in Two
Dimensions](https://doi.org/10.1137/S0036141099360919), SIAM Journal on
Mathematical Analysis 33 (2001), 286--314.

The precise results are:

1. Theorem 3.1, which constructs the selected maximal-canard curve;
2. Proposition 3.4, which constructs the attracting and repelling center
   manifolds in chart K1; and
3. Proposition 3.5, which computes the first-order splitting in chart K2.

There is no relevant “Lemma 3.4” in that paper. Section 3.4 is the K1
analysis, and Proposition 3.5 is the splitting statement.

Their notation is

\[
 r_2=\sqrt{\epsilon},\qquad
 \lambda_2=\frac{\lambda}{r_2}.
\tag{1}
\]

Theorem 3.1 determines the physical canard parameter through order
\(\epsilon=r_2^2\), with remainder \(O(\epsilon^{3/2})=O(r_2^3)\).
The transverse-delay effect studied here is exactly an \(r_2^3\) term in
the physical parameter. It lies inside that published remainder. Thus
Theorem 3.1 cannot be cited as proving our coefficient; the parameterized
second-order extension in Section 4 is necessary.

## 2. Exact normalization of the reduced special flow

On the target finite-regularity special-flow graph, write

\[
 Q_{\delta,\nu,\eta}(u)
 =q_0(u)+\delta q_1(u,\nu)
  +\delta^2q_2(u,\nu,\eta)
  +\delta^3R_3(u,\delta,\nu,\eta),
\tag{2}
\]

where \(u=(X,Y)^T\) and

\[
 q_0(X,Y)=
 \binom{Y-\alpha X^2}{-X},
 \qquad
 \alpha=\frac{\sqrt6}{4}.
\tag{3}
\]

The finite-order graph target would give the expansion in (2), with two
uniform \(\eta\)-derivatives, on every declared compact inner flow tube. At
present this expansion is the formal invariance recursion whose uniform
remainder is conditional on the mixed-jet lemma. The singular canard is

\[
 \gamma_0(s)=
 \binom{-s/(2\alpha)}{(s^2-2)/(4\alpha)}.
\tag{4}
\]

Set

\[
 x=-\alpha X,\qquad y=\alpha Y.
\tag{5}
\]

Then (3) becomes exactly the Krupa--Szmolyan K2 system

\[
 x'=-y+x^2,\qquad y'=x,
\tag{6}
\]

and (4) becomes

\[
 \gamma_c(s)=
 \binom{s/2}{s^2/4-1/2}.
\tag{7}
\]

A first integral of (6) is

\[
 H(x,y)=\frac12e^{-2y}
 \left(y-x^2+\frac12\right).
\tag{8}
\]

Along (4), the variational operator and its decaying adjoint solution are

\[
\begin{aligned}
 L_0(U,V)
  &=\binom{U'-sU-V}{V'+U},\\
 \psi(s)
  &=e^{-s^2/2}\binom{s}{1},
\qquad L_0^*\psi=0.
\end{aligned}
\tag{9}
\]

Moreover,

\[
 \nabla_{X,Y}H(-\alpha X,\alpha Y)
 \big|_{\gamma_0(s)}
 =\frac{\alpha e}{2}\psi(s).
\tag{10}
\]

Thus the first-integral gap and the adjoint gap differ only by the fixed
positive factor \(\alpha e/2\).

The parameter normalization is not optional. Since

\[
 Y'=-X+\delta\nu,
\]

equation (5) gives

\[
 y'=x+\alpha\delta\nu=x-\lambda_2,
\qquad
 \boxed{\lambda_2=-\alpha\delta\nu}.
\tag{11}
\]

Consequently,

\[
 \boxed{\lambda_{\rm KS}=\delta\lambda_2
 =-\alpha\delta^2\nu=-\alpha\mu}.
\tag{12}
\]

## 3. A normalized geometric gap

Fix attracting and repelling Fenichel manifolds outside the fold
neighborhood. Their choices are part of the definition; changing them can
move the selected canard by an exponentially small amount. Continue their
selected slow curves through K1 and into K2, and let
\(D_H(\delta,\nu,\eta)\) be the difference of their \(H\)-values where they
cross the section \(X=0\).

Because \(H_Y\ne0\) at the singular crossing,

\[
 D_H=0
 \quad\Longleftrightarrow\quad
 \text{the two selected slow curves intersect}.
\tag{13}
\]

For \(\delta>0\), define the normalized gap

\[
 \mathcal G(\delta,\nu,\eta)
 =\frac{2}{\alpha e\,\delta}D_H(\delta,\nu,\eta).
\tag{14}
\]

The factor \(1/\delta\) is essential. The raw derivative
\(\partial_\nu D_H\) is \(O(\delta)\); the normalized derivative has a
nonzero limit.

## 4. Conditional second-order splitting template

**Conditional Proposition 1 (parameterized second-order KS splitting).** Let a
\(C^5\) planar slow--fast family satisfy the canard-point conditions
(3.2)--(3.4) of Krupa--Szmolyan uniformly for the auxiliary parameter
\(\eta\). Perform their weighted blow-up, put \(r_2=\delta\), and restrict
the unfolding wedge by \(\lambda_2=-\alpha\delta\nu\), with
\((\nu,\eta)\) in a compact set. Assume that:

1. its K2 vector field has the expansion (2), with
   \(R_3\) and its first two \(\eta\)-derivatives uniformly \(C^3\);
2. \(q_1\) is independent of \(\eta\);
3. the outer slow-manifold selections are independent of \(\eta\) at first
   order, the selected K1 attracting and repelling traces are \(C^4\) in
   \((\delta,\nu,\eta)\), and on their K2 overlap
   \(\partial_\eta z_{a/r}=O(\delta^2\langle s\rangle^m)\), with analogous
   bounds through two \(\eta\)-derivatives;
4. \(D_H/\delta\) extends with the \(C^2_\eta\) regularity used below, and the
   differentiated K1 endpoint terms equal the missing tails of (19) up to
   \(O(\delta^3+\delta^2|\eta|)\), uniformly near the leading root; and
5. the integrands and trace remainders have polynomial growth in \(s\), so
   their products with the Gaussian adjoint weight are integrable uniformly.

Then \(D_H=\delta\widehat D_H\), where \(\widehat D_H\) is \(C^2\) in
\(\eta\), and the normalized gap in (14) satisfies

\[
\begin{aligned}
 \mathcal G(0,\nu,\eta)
 &=\int_{\mathbb R}
   \psi(s)^Tq_1(\gamma_0(s),\nu)\,ds,\\
 \partial_\eta\mathcal G(\delta,\nu,\eta)
 &=\delta M_\eta(\nu)
   +O(\delta^2+\delta|\eta|),
\end{aligned}
\tag{15}
\]

uniformly near the leading root, where

\[
 M_\eta(\nu)=
 \int_{\mathbb R}
 \psi(s)^T
 \partial_\eta q_2(\gamma_0(s),\nu,0)\,ds.
\tag{16}
\]

### Proof

At \(\delta=0\), both selected traces coincide with \(\gamma_0\), for every
\((\nu,\eta)\). Hence \(D_H(0,\nu,\eta)=0\), and the parameterized
Hadamard lemma gives \(D_H=\delta\widehat D_H\).

Krupa--Szmolyan Proposition 3.5 splits the \(H\)-difference into the two
identities

\[
\begin{aligned}
 H(z_a(0))
 &=H(z_a(T_-))
   +\int_{T_-}^{0}\frac{d}{ds}H(z_a(s))\,ds,\\
 H(z_r(0))
 &=H(z_r(T_+))
   -\int_{0}^{T_+}\frac{d}{ds}H(z_r(s))\,ds.
\end{aligned}
\tag{17}
\]

Their K1 calculation of the endpoint values in (17) supplies the missing
tails \((-\infty,T_-)\) and \((T_+,\infty)\). This is why the result is a
whole-line integral even though the gap is measured on a finite section.
It is not a formal replacement of a finite-section boundary-value problem.

Along either selected trace,

\[
 \frac{d}{ds}H(z)
 =\delta\nabla H(z)^Tq_1(z,\nu)
  +\delta^2\nabla H(z)^Tq_2(z,\nu,\eta)
  +O_{C_\eta^2}(\delta^3).
\tag{18}
\]

Differentiate (18) with respect to \(\eta\). By assumptions 2--3, the
parameter variation of either selected trace begins at order \(\delta^2\).
Its substitution into the first term of (18) is
therefore \(O(\delta^3)\). The only order-\(\delta^2\) contribution is

\[
 \delta^2\nabla H(\gamma_0(s))^T
 \partial_\eta q_2(\gamma_0(s),\nu,0).
\tag{19}
\]

Assumption 4 supplies the differentiated endpoint errors and turns the two
endpoint terms into the missing tails of (19). Combining both halves, using
(10), and dividing by the normalization in (14) proves (15)--(16) at
\(\eta=0\). Establishing assumption 4 for the nonlocal long-delay flow is the
substantive unresolved K1 problem; it is not imported from the scalar proof.

Uniform \(C^2\) dependence on \(\eta\) gives

\[
 \partial_\eta q_2(\cdot,\nu,\eta)
 =\partial_\eta q_2(\cdot,\nu,0)+O(|\eta|),
\]

while one further \(\delta\)-jet gives the \(O(\delta^2)\) term after
normalization. This proves the stated uniform remainder. \(\square\)

This conditional template identifies exactly which one-order-higher estimates
would extend the published Proposition 3.5. Its new content is bookkeeping of
the uniform mixed derivative and K1 endpoint term; the model-specific
verification of those hypotheses remains open.

## 5. Exact symbolic evaluation of the formal final-model recursion

The formal invariance recursion gives, along (4),

\[
\begin{aligned}
 q_{1,X}(\gamma_0(s),\nu)
 &=\frac{
  11s^3-12K(\theta_0+2\theta_1)
 }{72\alpha},\\
 q_{1,Y}(\gamma_0(s),\nu)&=\nu.
\end{aligned}
\tag{20}
\]

Let

\[
 I_0=\int_{\mathbb R}e^{-s^2/2}\,ds=\sqrt{2\pi}.
\]

The constant delay term in (20) pairs with the odd function
\(s e^{-s^2/2}\) and therefore vanishes. Since

\[
 \int_{\mathbb R}s^4e^{-s^2/2}\,ds=3I_0,
\]

equation (15) gives

\[
 \mathcal G(0,\nu,\eta)
 =I_0\left(\nu+\frac{11}{24\alpha}\right).
\tag{21}
\]

The candidate leading root of the conditional splitting problem is

\[
 \boxed{\nu_0=-\frac{11}{24\alpha}},
\qquad
 \partial_\nu\mathcal G(0,\nu_0,\eta)=I_0>0.
\tag{22}
\]

The exact symbolic invariance jet derived in
[special-flow-graph-theorem.md](special-flow-graph-theorem.md) is

\[
 \partial_\eta q_{2,X}(\gamma_0(s),\nu,0)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}s,
\qquad
 \partial_\eta q_{2,Y}=0.
\tag{23}
\]

Therefore

\[
\begin{aligned}
 M_\eta
 &=-\frac{K(\theta_0-\theta_1)}{4\alpha}
   \int_{\mathbb R}s^2e^{-s^2/2}\,ds\\
 &=-\frac{K(\theta_0-\theta_1)}{4\alpha}I_0.
\end{aligned}
\tag{24}
\]

All quantities in (20)--(24) are exact symbolic identities of the formal
invariance recursion and Gaussian pairing. They become coefficients of the
actual graph and selected root only under the hypotheses of Corollary 2.

## 6. The simple root and the uniform \(\eta\)-remainder

**Corollary 2 (conditional selected maximal-canard root).** If the
finite-order mixed-jet upgrade for the history graph and the final reduced
special flow's K1/tail-admissibility lemma in Section 7 both hold,
then there are \(\delta_0,\eta_0>0\) and a unique \(C^2\) function
\(\nu_c(\delta,\eta)\), for the fixed selected slow manifolds, such that
their reduced curves intersect. Moreover,

\[
 \boxed{
 \nu_c(\delta,\eta)-\nu_c(\delta,0)
 =\frac{K\eta(\theta_0-\theta_1)}{4\alpha}\delta
  +O(\delta^2|\eta|+\delta\eta^2).}
\tag{25}
\]

**Proof.** Equations (21)--(22) and the implicit-function theorem give a
unique root near \(\nu_0\). From (15), (22), and (24),

\[
\begin{aligned}
 \partial_\nu\mathcal G
 &=I_0+O(\delta),\\
 \partial_\eta\mathcal G
 &=-\frac{K(\theta_0-\theta_1)}{4\alpha}
   I_0\delta
   +O(\delta^2+\delta|\eta|).
\end{aligned}
\]

Implicit differentiation gives

\[
 \partial_\eta\nu_c(\delta,\eta)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta
  +O(\delta^2+\delta|\eta|).
\tag{26}
\]

Integrating (26) from \(0\) to \(\eta\) proves (25), since

\[
 \int_0^{|\eta|}
  (\delta^2+\delta r)\,dr
 =\delta^2|\eta|+\frac12\delta\eta^2.
\]

\(\square\)

Since \(\mu=\delta^2\nu\), (25) is equivalent to

\[
 \boxed{
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{K\eta(\theta_0-\theta_1)}{4\alpha}\delta^3
+O(\delta^4|\eta|+\delta^3\eta^2).}
\tag{27}
\]

In the Krupa--Szmolyan physical parameter,

\[
 \lambda_{{\rm KS},c}(\delta,\eta)
 -\lambda_{{\rm KS},c}(\delta,0)
 =-\frac{K\eta(\theta_0-\theta_1)}4\delta^3
+O(\delta^4|\eta|+\delta^3\eta^2).
\tag{28}
\]

The raw gap remains simple but is not uniformly conditioned:

\[
 \partial_\nu D_H
 =\frac{\alpha e}{2}\delta
  \left(I_0+O(\delta)\right).
\tag{29}
\]

The normalized gap in (14) is the uniformly conditioned object.

### Section independence

Let \(\Sigma\) and \(\widetilde\Sigma\) be two transverse sections crossed
once by both selected curves. The local flow map from \(\Sigma\) to
\(\widetilde\Sigma\) is a diffeomorphism. Therefore the two gaps have the
same zero set, and near a zero they differ by multiplication by a nonzero
smooth factor. At a root, that factor multiplies both
\(\partial_\eta D\) and \(\partial_\nu D\), so the quotient
\(-\partial_\eta D/\partial_\nu D\) and formula (25) are unchanged.

A frozen finite-section pairing without the selected endpoint variations is
not section independent. For example,

\[
 \int_{-L}^Ls^2e^{-s^2/2}\,ds
 =\int_{-L}^Le^{-s^2/2}\,ds-2Le^{-L^2/2}.
\tag{30}
\]

The missing term in (30), together with the tails outside \([-L,L]\), is
supplied by the K1 endpoint calculation in Proposition 1.

### Complete-history lift

Once the selected reduced curves have been constructed on the special-flow
graph, their intersection automatically lifts to equality of RFDE
histories. Indeed, the proved embedding \(\iota_{\delta,p}\) is injective
and conjugates the reduced flow to the RFDE semiflow. If the two reduced
curves meet at \(u_c\), both RFDE traces equal
\(\iota_{\delta,p}(u_c)\). Planar ODE uniqueness then makes the common
reduced orbit the selected local maximal canard. No arbitrary current-state
matching is used.

## 7. The long-delay geometric lemma

**Lemma 3 (K1/tail admissibility for the final special flow; open).** For
the final two-module RFDE and fixed selected outer slow manifolds, the
two-dimensional special-flow graph must extend far enough through the
weighted blow-up that:

1. its reduced K2 field has (2) on the full canard tube needed for matching;
2. the selected attracting and repelling reduced traces enter K2 as
   \(C^4\) parameter families;
3. their \(H\)-gap satisfies, uniformly near \((\nu_0,0)\),

   \[
   \begin{aligned}
   \partial_\nu D_H
   &=\frac{\alpha e}{2}\delta
     \left(I_0+O(\delta)\right),\\
   \partial_\eta D_H
   &=\frac{\alpha e}{2}\delta^2
     \left(M_\eta+O(\delta+|\eta|)\right),\\
   \partial_{\eta\eta}D_H&=O(\delta^2).
   \end{aligned}
   \tag{31}
   \]

4. the orbit selected by \(D_H=0\) stays in the uncut physical flow tube,
   including every delayed backtrack used by the graph embedding.

The current special-flow graph theorem is uniform on a fixed compact inner
tube. It does not prove Lemma 3 because the K1 endpoints correspond to
\(|s|\to\infty\) in K2. A fixed-\(L\) calculation cannot replace (31).

### A viable logarithmic growing-tube proof route

Purely polynomially weighted contraction on a full K1 neighborhood is not
available: individual long-delay backtracks have exponentially growing
derivatives. The following curve-wise estimates on a logarithmically growing
K2 tube are instead sufficient and are concrete proof targets.

Let \(\langle s\rangle=(1+s^2)^{1/2}\). On a tubular coordinate
\(u=\gamma_0(s)+\zeta\), require, for \(|a|\le3\) and \(0\le b\le2\),

\[
 \left|
 \partial_u^a\partial_\eta^b
 R_3(\gamma_0(s)+\zeta,\delta,\nu,\eta)
 \right|
 \le C_{a,b}\langle s\rangle^{m_{a,b}}e^{C_{a,b}|s|},
\tag{32}
\]

and analogous tame bounds for \(q_1,q_2\), on
\(|s|\leq S_\delta+O(1)\). Fixed scaled-delay shifts preserve this class:

\[
 \langle s-\theta_j\rangle^m e^{C|s-\theta_j|}
 \le C_{m,\Theta,C}\langle s\rangle^m e^{C|s|},
\qquad 0\le\theta_j\le\Theta.
\tag{33}
\]

The stable graph convolution also preserves them, because

\[
 \int_0^\infty e^{-\beta r}
 \langle s-\delta r\rangle^m e^{C|s-\delta r|}\,dr
 \le C_{m,\beta,C}\langle s\rangle^m e^{C|s|}
\tag{34}
\]

uniformly for small \(\delta\) with \(C\delta<\beta\). The missing
growing-tube graph theorem must establish these estimates; the fixed-tube
contraction does not supply them automatically. The target trace estimates
are

\[
\begin{aligned}
 |z_\pm(s)-\gamma_0(s)|
 &\le C\delta\langle s\rangle^m e^{C|s|},\\
 |\partial_\eta z_\pm(s)|
 &\le C\delta^2\langle s\rangle^m e^{C|s|},\\
 |\partial_{\eta\eta} z_\pm(s)|
 &\le C\delta^2\langle s\rangle^m e^{C|s|},
\end{aligned}
\tag{35}
\]

after the single tangent phase is fixed.

The cokernel weight is Gaussian, so every polynomial--single-exponential
remainder is integrable:

\[
 \int_{\mathbb R}
 e^{-s^2/2+C|s|}\langle s\rangle^m\,ds<\infty.
\tag{36}
\]

Equations (32)--(36), once proved with the explicit right inverse of \(L_0\),
would give the growing-tube K2 part of (31). They are consistent with, but do
not replace, the selected-trace estimates in
[k1-tail-compatibility.md](k1-tail-compatibility.md).

For a cutoff implementation, take

\[
 L_\delta=\sqrt{2p\log(1/\delta)},\qquad p>2.
\tag{37}
\]

For every fixed integer \(m\),

\[
 \int_{|s|>L_\delta}
 \langle s\rangle^m e^{-s^2/2+C|s|}\,ds
 \le C_{m,p,C}\,\delta^{p-o(1)}
 =o(\delta^2).
\tag{38}
\]

Hence the omitted mixed Melnikov tail is \(o(\delta^4)\) in the raw gap,
well below the required \(O(\delta^3)\) error in
\(\partial_\eta D_H\). On \([-L_\delta,L_\delta]\), use the weighted graph
estimates rather than an unweighted supremum; otherwise powers of
\(\log(1/\delta)\) contaminate the claimed remainder.

It remains to match at \(\pm L_\delta\) to K1 center-manifold traces and
prove

\[
\begin{aligned}
 \partial_\eta H(z_a(-L_\delta))
 &=\frac{\alpha e}{2}\delta^2
   \int_{-\infty}^{-L_\delta}
   \psi^T\partial_\eta q_2(\gamma_0)\,ds
   +O(\delta^3+\delta^2|\eta|),\\
 \partial_\eta H(z_r(L_\delta))
 &=-\frac{\alpha e}{2}\delta^2
   \int_{L_\delta}^{\infty}
   \psi^T\partial_\eta q_2(\gamma_0)\,ds
   +O(\delta^3+\delta^2|\eta|).
\end{aligned}
\tag{39}
\]

The exponential \(e^{-2/\epsilon_1}\) in the K1 first integral is the
mechanism expected to prove (39), exactly as in the published proof of
Proposition 3.5. Equations (32)--(39) are a proof route, not a completed
verification for the current nonlocal special flow.

## 8. Integrity boundary

At present the defensible statements are:

- the parameter normalization (11)--(12) is exact;
- Conditional Proposition 1 is a valid implication under its explicit
  trace/endpoint hypotheses, not a verification of those hypotheses;
- the final model satisfies the exact K2 algebraic identities and has the
  symbolic coefficients (20)--(24);
- the implicit-function and \(C^2_\eta\) remainder argument giving
  (25)--(28) is complete once the mixed-jet regularity lemma and Lemma 3 hold;
- the mixed-jet regularity lemma and Lemma 3 are the unclosed analytic
  obligations.

Until both the mixed-jet regularity lemma and Lemma 3 are proved, equations
(25)--(28) must not be presented as an unconditional maximal-canard theorem
for the RFDE.
