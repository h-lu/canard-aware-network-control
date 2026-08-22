# K1 and tail compatibility of the fixed-scaled-delay chart

Status: **Gate D is not yet closed by the present references or by the
fixed-tube graph theorem.** There is a precise obstruction to applying the
usual \(K_1\) center-manifold theorem to the special-flow reduction on a
fixed neighborhood. That obstruction is not a no-go theorem: the
exponential weight in the Krupa--Szmolyan first integral can suppress the
bad backtrack derivative on a logarithmically receding section. This note
proves the individual-backtrack obstruction and a conditional suppression
lemma, and records the part of the history lift that is complete. The
fixed-tube mixed-jet prerequisite has since been closed in
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md). The remaining
curve-wise selected-trace theorem and the resulting trace-to-gap implication
are stated more sharply in
[long-delay-selected-trace-proof.md](long-delay-selected-trace-proof.md).

## 1. The two compactifications use incompatible delay times

In the canonical \(K_2\) variables used in
[reduced_canard_root.py](../src/canard_control/reduced_canard_root.py),

\[
 x_2=-\alpha X,\qquad y_2=\alpha Y,
\]

the singular reduced field and its distinguished connection are

\[
 q_0(x_2,y_2)=(-y_2+x_2^2,x_2),\qquad
 \gamma_0(s)=\left(\frac{s}{2},\frac{s^2}{4}-\frac12\right).
\tag{1}
\]

The \(K_1\leftrightarrow K_2\) change in Krupa--Szmolyan is

\[
 x_1=x_2y_2^{-1/2},\qquad
 r_1=r_2y_2^{1/2},\qquad
 \epsilon_1=y_2^{-1}.
\tag{2}
\]

Put \(\rho=\sqrt{\epsilon_1}=y_2^{-1/2}\). Along the attracting
tail of (1), \(s\to-\infty\),

\[
 x_1\longrightarrow-1,\qquad
 \rho=\frac{2}{|s|}\bigl(1+O(s^{-2})\bigr).
\tag{3}
\]

The two desingularized times satisfy

\[
 dt_2=\rho\,dt_1.
\tag{4}
\]

Consequently, a fixed \(K_2\) delay \(\theta>0\) is a \(K_1\) past
interval

\[
 T_1(\rho)=\frac{\theta}{\rho}+O(1)
 \qquad(\rho\downarrow0).
\tag{5}
\]

Equivalently, in physical fast time,

\[
 r_1\tau=r_1\frac{\theta}{r_2}=\frac{\theta}{\rho}.
\]

Thus a delay which is fixed on the blown-up RFDE history interval is not a
bounded-time operation in \(K_1\).

## 2. Individual K1 backtracks have no uniform C1 bound

Let \(P_\theta=\phi_0^{-\theta}\) be the backward-time map of (1). The
special-flow graph writes a delayed state as \(P_\theta(u)\), with the
perturbed flow replacing \(\phi_0\) for positive \(r_2\).

**Proposition 1 (backtrack derivative obstruction).** On every fixed-width
\(K_1\) neighborhood of the attracting point \(p_a=(-1,0)\), the maps
\(P_\theta\), written in \(K_1\) coordinates, have no uniform \(C^1\)
bound as \(\rho\downarrow0\). More precisely, their operator norm satisfies

\[
 \|DP_\theta\|
 \geq\exp\left(\frac{\theta}{\rho}+O(1)\right).
\tag{6}
\]

Multiplication by a prefactor having any finite-order zero at \(\rho=0\)
does not restore a bound for a component that does not annihilate the
expanding singular direction. Thus a standard full-neighborhood \(C^k\)
argument cannot be justified from the polynomial weak factor alone. A
model-specific projection could in principle cancel that direction and must
be checked separately.

*Proof.* In \((x_1,\rho)\), the singular field (1) is

\[
 \dot x_1=-1+x_1^2-\frac12\rho^2x_1^2,\qquad
 \dot\rho=-\frac12\rho^3x_1.
\tag{7}
\]

The fast eigenvalue at \(p_a\) is \(-2\), which indicates the expanding
backward direction but does not by itself give an invariant fast-fiber
formula for the variable stopping time. A coordinate-free lower bound follows
directly in \(K_2\). Since
\(\operatorname{div}q_0=2x_2\), Liouville's formula gives

\[
 \det DP_\theta(\gamma_0(s))
 =\exp\left(\int_0^{-\theta}(s+t)\,dt\right)
 =\exp\left(-s\theta+\frac{\theta^2}{2}\right).
\tag{8}
\]

Along the attracting tail, (3) and (8) give
\(|\det DP_\theta|=\exp(2\theta/\rho+O(1))\). In two dimensions,
\(\|DP_\theta\|^2\geq|\det DP_\theta|\), proving (6). Finally,
\(\rho^m e^{c/\rho}\to\infty\) for every finite \(m\) and \(c>0\).
\(\square\)

For the two-atom model, the longer atom has nonzero critical weight \(2/3\),
and the transverse redistribution also contains that atom with a nonzero
algebraic coefficient. This makes structural annihilation unlikely, but a
cone or tangent/normal estimate is still required before assigning the exact
expanding component or exponent to the final delayed combination.

The restriction of \(P_\theta\) to the one-dimensional center branch does
have an ordinary expansion in \(\rho\). Proposition 1 concerns the
fixed-width neighborhood required by a standard center-manifold and
invariant-foliation theorem. It leaves open a curve-wise construction that
never backtracks an off-center point.

## 3. The H weight makes a logarithmic rescue viable

Proposition 1 does not imply that the endpoint coefficient is
uncontrollable. In \(K_1\), the canonical first integral is

\[
 H_1(x_1,\epsilon_1)
 =e^{-2/\epsilon_1}
 \left(\frac14+\frac{1-x_1^2}{2\epsilon_1}\right).
\tag{9}
\]

At a physical \(K_1\) radius \(r_1\),
\(\epsilon_1=\delta^2/r_1^2\), so its weight is
\(\exp(-2r_1^2/\delta^2)\). This dominates every factor
\(e^{Cr_1/\delta}\).

**Lemma 2 (logarithmic-section suppression).** Let

\[
 S_\delta=\sqrt{2p\log(1/\delta)},\qquad p>0,
\tag{10}
\]

and take the \(K_2\) endpoints through
\(\gamma_0(\pm S_\delta)\), so their \(y_2\)-coordinate is fixed by that
section. Suppose their \(K_1\) traces stay in a fixed strip
\(|x_1|\le C_0\), and the finitely many mixed parameter derivatives used
in the gap satisfy

\[
 |\mathscr D z^{a/r}_\delta|
 \le C(1+S_\delta)^m e^{CS_\delta}.
\tag{11}
\]

Then every endpoint term obtained by applying \(H\), with the same finite
number of derivatives, is bounded by

\[
 C'(1+S_\delta)^{m'}
 e^{-S_\delta^2/2+C'S_\delta}
 =O(\delta^{p-\kappa})
\tag{12}
\]

for every fixed \(\kappa>0\). The omitted Gaussian tail obeys the same
bound. Thus \(p\) can be chosen so that both contributions are below any
prescribed algebraic order in \(\delta\).

*Proof.* Along (1),

\[
 y_2(\pm S_\delta)=\frac{S_\delta^2}{4}-\frac12,
\]

so (9) contains the factor

\[
 e^{-2y_2}=e^{1-S_\delta^2/2}.
\]

Every fixed derivative of \(H_1\) is this factor times a rational
expression bounded on the endpoint sections by a polynomial in
\(S_\delta\). Faà di Bruno's formula and (11) give the first bound in
(12). For every \(\kappa>0\),

\[
 (1+S_\delta)^{m'}e^{C'S_\delta}\le\delta^{-\kappa}
\]

for all sufficiently small \(\delta\), proving (12). Finally,

\[
 \int_S^\infty s^2e^{-s^2/2}\,ds
 \le C(S+S^{-1})e^{-S^2/2},\qquad S\ge1,
\]

which proves the tail assertion. \(\square\)

If differentiation of the moving section introduces a fixed factor
\(\delta^{-a}\), choose \(p\) larger by \(a\). Therefore failure of a
uniform full-neighborhood \(C^1\) norm is harmless provided that the
selected one-sided traces satisfy the single-exponential tame bound (11).
That bound is not proved in the current documents.

## 4. What the cited theorems do and do not supply

[Krupa--Touboul (2016), Lemmas 1--2](https://doi.org/10.1007/s10884-015-9478-2)
show, for a regular RFDE, that choices of a Fenichel slow manifold and a
local center manifold can be made to overlap. Their phase space is
\(C([-h,0],\mathbb R^n)\) with fixed maximal delay \(h\), and their
argument uses a fixed spectral gap and cutoffs on that fixed space.

Here, in physical fast time,

\[
 h=\frac{\theta_1}{\delta}\longrightarrow\infty.
\tag{13}
\]

Their lemmas do not state estimates uniform as \(h\to\infty\), nor mixed
\(\delta\)- and \(\eta\)-derivative bounds for the overlap. Passing to
\(s=\delta t\) fixes the delay interval but produces the singular
transverse generator \(A/\delta\). The special-flow graph handles that
generator on a fixed \(K_2\) tube, but its full-neighborhood backtrack has
the loss in Proposition 1. The overlap lemmas therefore do not prove (11).

[Krupa--Szmolyan (2001), Proposition 3.4](https://doi.org/10.1137/S0036141099360919)
assumes a \(C^k\) vector field on a fixed \(K_1\) box, which is not
available here. Their Proposition 3.5 proves

\[
 D_c(r_2,\lambda_2)
 =d_{r_2}r_2+d_{\lambda_2}\lambda_2
 +O\bigl((|r_2|+|\lambda_2|)^2\bigr),
\tag{14}
\]

including the \(K_1\) endpoint term at first Melnikov order. In the present
normalization,

\[
 r_2=\delta,\qquad \lambda_2=-\alpha\delta\nu,
\]

while the first \(\eta\)-dependent vector-field term is
\(r_2^2\eta Q_{2,\eta}\). The desired coefficient lies inside the
unspecified quadratic remainder in (14). A parameter-differentiated,
second-order tail estimate is still required.

## 5. Why a fixed cutoff cannot determine the coefficient

**Proposition 3 (minimal cutoff counterexample).** Fix a finite uncut
segment \(|s|\le L\), enlarged by all delay backtracks used by the computed
jet. There are two smooth completions which agree, with all derivatives, on
that segment but have different \(r_2^2\eta\) Melnikov coefficients.

*Proof.* Return temporarily to the audited \((X,Y)\) reduced coordinates,
in which the adjoint and the transverse-return jet were computed. Put

\[
 c=\frac{K(\theta_0-\theta_1)}{4\alpha}\ne0,\qquad
 \psi(s)=e^{-s^2/2}(s,1)^T.
\]

The audited local jet on the singular connection is

\[
 Q_{2,\eta}(\gamma_0(s))=-cs\,e_x.
\tag{15}
\]

Choose a nonnegative smooth bump \(b\not\equiv0\) supported outside the
enlarged uncut segment and extend it smoothly to a tubular neighborhood.
Two completions which differ by \(-csb(s)e_x\) on the connection agree on
every point controlled by the fixed-tube graph theorem. Their whole-line
coefficients differ by

\[
 -c\int_{-\infty}^{\infty}
 b(s)s^2e^{-s^2/2}\,ds\ne0.
\tag{16}
\]

\(\square\)

For the physical completion, the missing contribution must be selected by
the physical attracting and repelling slow histories. At a fixed symmetric
section, the omitted term

\[
 -c\int_{|s|>L}s^2e^{-s^2/2}\,ds
\tag{17}
\]

is nonzero. Proposition 3 rules out a fixed tube, not the logarithmic
construction: with \(L=S_\delta\), Lemma 2 makes (17) smaller than the
desired remainder, provided (11) holds.

## 6. The complete-history lift is exact, conditionally on the curves

**Lemma 4 (injective history lift).** Let \(S^a,S^r\subset U\) be two
selected reduced curves on which the special-flow embedding
\(\iota_{\delta,\eta}:U\to
C([-\theta_1,0],\mathbb R^4)\) is defined. Then

\[
 \iota_{\delta,\eta}(S^a)\cap\iota_{\delta,\eta}(S^r)
 =\iota_{\delta,\eta}(S^a\cap S^r).
\tag{18}
\]

*Proof.* If \(\iota(u_a)=\iota(u_r)\), evaluate at the present time and
project to the \(u\)-coordinates. This composition is the identity, so
\(u_a=u_r\). The reverse inclusion is immediate. \(\square\)

Thus a reduced intersection is equivalent to equality of the complete
embedded histories once the physical selected curves have been constructed.

## 7. Exact remaining estimates

A logarithmic-section proof of Gate D now has three specific obligations.

1. Construct one-sided physical slow curves
   \(S^a_{\delta,\eta,\nu}\) and \(S^r_{\delta,\eta,\nu}\) on the
   special-flow graph and prove (11) through two \(\eta\)-derivatives and
   the required \(\delta,\nu\) derivatives. Full-neighborhood \(K_1\)
   regularity is not required.

2. Extend the graph-transform bounds to
   \(|s|\le S_\delta+O(1)\). A sufficient one-extra-order estimate is

   \[
   \max_{0\le j\le2}
   \|\partial_\eta^jR_Q^{(3)}\|
   \le C\delta^4(1+S_\delta)^m e^{CS_\delta}.
   \tag{19}
   \]

   It is \(O(\delta^{4-\kappa})\) for every \(\kappa>0\), so the unused
   graph order yields the required \(O(\delta^3)\) gap error. The proof of
   the fixed-tube theorem suggests (19): the polynomial data have polynomial
   norms on the growing tube, a fixed-delay flow costs \(e^{CS_\delta}\),
   and \(\delta e^{CS_\delta}\to0\). Those constants have not yet been
   tracked.

3. Multiply the geometric \(H\)-gap by the fixed nonzero normalization used
   in the symbolic audit, and call the resulting unscaled matching gap
   \(D\). Prove

   \[
   \begin{aligned}
   \partial_\nu D
     &=\delta M_\nu+O(\delta^2),\\
   \partial_\eta D
     &=\delta^2 M_\eta+O(\delta^3),\\
   \partial_{\eta\eta}D&=O(\delta^2),
   \end{aligned}
   \tag{20}
   \]

   uniformly near the leading root. In the orientation used by the current
   symbolic audit,

   \[
   M_\nu=\sqrt{2\pi},\qquad
   M_\eta=-\frac{K(\theta_0-\theta_1)}{4\alpha}\sqrt{2\pi}.
   \tag{21}
   \]

Equations (11), (19), and (20), followed by the implicit-function theorem
and Lemma 4, would give

\[
 \nu_c(\delta,\eta)-\nu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta\eta
 +O(\delta^2|\eta|+\delta\eta^2),
\]

and hence the claimed physical \(\mu=\delta^2\nu\) law.

The conditional endpoint-suppression estimate is proved in Lemma 2 assuming
(11). What remains is the single-exponential selected-trace bound (11) and the
growing-tube graph bound (19). The normalized gap estimates (20) now follow
from these inputs by Theorem 2 of
[long-delay-selected-trace-proof.md](long-delay-selected-trace-proof.md);
they do not follow unconditionally
from the present fixed-tube theorem, Krupa--Touboul Lemmas 1--2, or
Krupa--Szmolyan Propositions 3.4--3.5.

### Stop point

These selected-trace and growing-graph inputs cannot honestly be promoted to
proved statements from the current material.

- Fixed-\(\delta\) smoothness of the Krupa--Touboul overlap gives no bound
  on how its mixed parameter derivatives depend on
  \(h=\theta_1/\delta\). A generic invocation of a center-manifold theorem
  does not imply the single-exponential estimate (11).
- The constants in the present special-flow theorem are allowed to depend
  on a fixed cutoff. The proof has not constructed anisotropic cutoffs on
  the \(S_\delta\)-tube or shown that their mixed-jet constants grow only as
  \(\operatorname{poly}(S_\delta)e^{CS_\delta}\). The observation that
  \(\delta e^{CS_\delta}\to0\) is a proof strategy, not a proof of (19).
- Without (11) and (19), differentiation of the selected endpoint maps and
  the \(O(\delta^3)\) remainder in (20) are uncontrolled. Proposition 3.5
  of Krupa--Szmolyan leaves precisely this \(r_2^2\eta\) term inside its
  quadratic remainder.

Accordingly, the rigorous output of this note is Proposition 1, Lemma 2,
Proposition 3, and the conditional history-lift Lemma 4. The geometric root
and its coefficient remain conditional on the selected-trace/growing-graph
input, not on the subsequent Gaussian differentiation itself.

## 8. Claim consequence

The permitted current statement is:

> The finite-regularity fixed-tube invariant-history graph is proved, the local
> \(r_2^2\eta\) graph jet is remainder-controlled and symbolically checked,
> and a reduced intersection
> would lift exactly to a complete-history
> intersection. Individual backtrack maps are nonuniform, so the standard
> full-neighborhood \(K_1\) theorem is not yet applicable; the first-integral
> weight nevertheless makes a logarithmic-section proof viable. Its tame
> selected-trace and growing-tube estimates remain open.

Until the selected-trace/growing-graph hypothesis is proved, the Gaussian value
\(1/(4\alpha)\) remains a conditional candidate for the selected physical
RFDE root, and Gate D must remain marked **open**.
