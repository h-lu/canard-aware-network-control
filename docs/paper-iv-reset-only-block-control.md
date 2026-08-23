# Reset-only safety actuation and a quantitative three-output inverse

Status: **the operational-threshold implicit-function result, the exact
block-triangular response theorem, its smallest-singular-value bound, the
quantitative inverse radius, and the cubic Hopf witness are proved below.**
For the collective-recovery-clamped FitzHugh--Nagumo experiment, the
complete-history separator used here is supplied by
paper-iii-collective-clamp-separator.md for every sufficiently small fixed
positive singular parameter under its stated hypotheses. A validated
periodic branch, unique-extrema box, and interval enclosure of the
two-by-two frequency--amplitude response for the declared synchronous FHN
RFDE are now supplied on a microscopic gain box by
[paper-iv-periodic-parameter-box.md](paper-iv-periodic-parameter-box.md).
Thus the positive block criterion has its periodic \(2\times2\) input; a
model-level FHN three-output theorem still requires the reset constants and,
for a target radius, a response-derivative Lipschitz bound.

The constants below are evaluated by
src/canard_control/operational_control_repair.py and checked in
tests/test_operational_control_repair.py. This note does not change the
frozen JNS manuscript. The interval-box utility in that module is explicitly
a floating-point candidate diagnostic; it is not a directed interval
implementation.

## 1. Separate the two experiments

Let

\[
 b=(b_1,b_2)\in U\subset\mathbb R^2
 \tag{1.1}
\]

denote two controls that occur in the baseline RFDE. When a nondegenerate
periodic branch exists, let

\[
 P(b)=\bigl(F(b),A(b)\bigr),
 \qquad
 F=T^{-1},
 \qquad
 A=(\max h-\min h)^2.
 \tag{1.2}
\]

For the declared synchronous FHN specialization, the intended choice is
\(b=(\kappa_1,\kappa_3)\): the linear and cubic delayed-feedback gains
remain baseline controls, while the former common-delay-shift actuator is
replaced by \(a_{\rm op}\).

The periodic adjoints in paper-iv-periodic-rfde-adjoints.md give the two
rows of \(D_bP\). A plotted closed orbit alone does not prove the bordered
periodic-operator or extremum hypotheses used there.

The third control \(a_{\rm op}\) is used only in a separate pulse-decision
experiment. It selects a reset history, is absent from the baseline RFDE,
and is inactive while \(F\) and \(A\) are measured. Consequently

\[
 \partial_{a_{\rm op}}F
 =\partial_{a_{\rm op}}A=0
 \tag{1.3}
\]

exactly. This is a protocol identity, not a small-coupling approximation.
It fails if the reset actuator leaks into the baseline vector field.
The symbol \(a_{\rm op}\) is not the FHN recovery-nullcline unfolding often
also denoted by \(a\); it is a reset preset or stimulus amplitude.

## 2. From a complete-history separator to a controlled operational threshold

Fix a positive delay scale. Let \(\mathcal X\) be the RFDE history space for
the collective-recovery-clamped decision experiment. The
implicit-function argument requires parameter regularity, not merely a
separate defining function for each fixed \(b\). Assume there are common
neighborhoods \(\mathcal V\subset\mathcal X\), \(U_0\subset\mathbb R^2\)
and a jointly \(C^1\) map

\[
 G:\mathcal V\times U_0\longrightarrow\mathbb R,
 \qquad
 G_b(\phi):=G(\phi,b),
 \tag{2.1}
\]

such that \(G_b=0\) is the local separator and its signs label the quiet
and pulse exit channels. Also assume the complete reset map

\[
 \mathcal R:J\times U_0\longrightarrow\mathcal V
 \tag{2.2}
\]

is jointly \(C^1\). It is the history produced by the voltage hold,
recovery preset, and subsequent collective clamp. Define

\[
 \Gamma(a_{\rm op},b)
 =G_b\bigl(\mathcal R(a_{\rm op},b)\bigr).
 \tag{2.3}
\]

The parameter derivatives in (2.3) include changes of both the reset
history and the complete-history stable manifold. Replacing \(\Gamma\) by a
current-voltage projection would discard delayed-history terms.

> **Proposition 2.1 (operational channel threshold).** Under the joint
> \(C^1\) assumptions on \(G\) and \(\mathcal R\) above, \(\Gamma\) is
> jointly \(C^1\). Suppose
> \(\Gamma(a_0,b_0)=0\) and
>
> \[
>  \partial_{a_{\rm op}}\Gamma(a_0,b_0)\ne0.
>  \tag{2.4}
> \]
>
> Then there are neighborhoods of \(b_0\) and \(a_0\) and a unique \(C^1\)
> function \(a_c(b)\) such that
>
> \[
>  \Gamma(a_c(b),b)=0,
>  \qquad
>  D_ba_c
>  =-\frac{D_b\Gamma}{\partial_{a_{\rm op}}\Gamma}
>       \bigg|_{(a_c(b),b)}.
>  \tag{2.5}
> \]
>
> If, on this neighborhood,
>
> \[
>  \|D_b\Gamma\|\le C_\Gamma,
>  \qquad
>  |\partial_{a_{\rm op}}\Gamma|\ge g>0,
>  \tag{2.6}
> \]
>
> then
>
> \[
>  \|D_ba_c\|\le\gamma:=C_\Gamma/g.
>  \tag{2.7}
> \]

**Proof.** Apply the parameter-dependent implicit-function theorem to
(2.3). Formula (2.5) is its derivative formula, and taking norms gives
(2.7). \(\square\)

Orient the laboratory calibration so that increasing \(a_{\rm op}\) moves
toward the pulse channel. The signed operational safety margin is

\[
 S(b,a_{\rm op})=a_c(b)-a_{\rm op},
 \qquad
 DS=(D_ba_c,-1).
 \tag{2.8}
\]

For the centered reset curve in the clamped-separator theorem, \(a_c=0\) in
its intrinsic coordinate. Proposition 2.1 transfers that result to a fixed
laboratory amplitude whose center can depend on \(b\).

This is a controlled operational channel threshold: an actual
RFDE stable manifold in complete-history space separates trajectories that
reach declared pulse and quiet channel blocks. It is a threshold for the
**controlled collective-clamp protocol**. It is neither the unforced pulse
threshold nor an identified maximal-canard root.

## 3. Exact block triangularity and a singular-value bound

Define

\[
 \mathcal Q(b,a_{\rm op})
 =\bigl(F(b),A(b),a_c(b)-a_{\rm op}\bigr).
 \tag{3.1}
\]

At a point where these functions are \(C^1\), put

\[
 B=D_bP\in\mathbb R^{2\times2},
 \qquad
 c=D_ba_c\in\mathbb R^2.
 \tag{3.2}
\]

Equations (1.3) and (2.8) give

\[
 M:=D\mathcal Q
 =
 \begin{pmatrix}
  B&0\\
  c^T&-1
 \end{pmatrix}.
 \tag{3.3}
\]

The third column is therefore independent of any near-parallelism between
amplitude and canard-root responses in the old three-baseline-actuator
design. The remaining rank question is two-dimensional: can \(b_1,b_2\)
independently change \(F\) and \(A\)?

> **Theorem 3.1 (quantitative block-triangular controllability).** Suppose
>
> \[
>  \sigma_{\min}(B)\ge\beta>0,
>  \qquad
>  \|c\|\le\gamma.
>  \tag{3.4}
> \]
>
> Set
>
> \[
> \begin{aligned}
>  q(\beta,\gamma)
>   &=1+\frac{1+\gamma^2}{\beta^2},\\
>  \Lambda_+(\beta,\gamma)
>   &=\frac12\left[
>      q(\beta,\gamma)
>      +\sqrt{q(\beta,\gamma)^2-\frac4{\beta^2}}
>     \right],\\
>  m(\beta,\gamma)
>   &=\Lambda_+(\beta,\gamma)^{-1/2}.
> \end{aligned}
> \tag{3.5}
> \]
>
> Then
>
> \[
>  \boxed{\sigma_{\min}(M)\ge m(\beta,\gamma)>0,}
>  \qquad
>  \|M^{-1}\|_2\le\sqrt{\Lambda_+(\beta,\gamma)}.
>  \tag{3.6}
> \]

**Proof.** The inverse is

\[
 M^{-1}
 =
 \begin{pmatrix}
  B^{-1}&0\\
  c^TB^{-1}&-1
 \end{pmatrix}.
 \tag{3.7}
\]

For \(y\in\mathbb R^2\) and \(s\in\mathbb R\),

\[
 \begin{aligned}
 \|M^{-1}(y,s)\|^2
 &\le \beta^{-2}\|y\|^2
   +(\gamma\beta^{-1}\|y\|+|s|)^2\\
 &=
 \begin{pmatrix}\|y\|&|s|\end{pmatrix}
 H_{\beta,\gamma}
 \begin{pmatrix}\|y\|\\|s|\end{pmatrix},
 \end{aligned}
 \tag{3.8}
\]

where

\[
 H_{\beta,\gamma}
 =
 \begin{pmatrix}
  \beta^{-2}(1+\gamma^2)&\gamma/\beta\\
  \gamma/\beta&1
 \end{pmatrix}.
 \tag{3.9}
\]

Its trace is \(q(\beta,\gamma)\), its determinant is \(\beta^{-2}\), and
its largest eigenvalue is \(\Lambda_+\). Thus
\(\|M^{-1}\|_2^2\le\Lambda_+\). Since
\(\sigma_{\min}(M)=\|M^{-1}\|_2^{-1}\), (3.6) follows. \(\square\)

For stable floating-point evaluation, do not form \(\beta^{-2}\) or
\(\gamma^2\) directly. The same constant satisfies

\[
 \sqrt{\Lambda_+}
 =
 \frac1\beta
 \left\|
  \begin{pmatrix}1&0\\ \gamma&\beta\end{pmatrix}
 \right\|_2.
 \tag{3.10}
\]

Scaling the displayed matrix by
\(\max\{1,\beta,\gamma\}\) keeps all entries bounded by one. If the
positive lower bound lies below the binary64 range, the executable helper
returns zero for that lower bound and \(+\infty\) for the inverse-squared
bound rather than raising an overflow or division exception.

This is stronger than \(\det M=-\det B\ne0\): it quantifies how a steep
threshold \(a_c(b)\) degrades the usable inverse. Under (2.6), insert
\(\gamma=C_\Gamma/g\) in (3.5).

For one fixed positive singular parameter, local \(C^1\) dependence makes
\(\gamma\) finite after shrinking the control neighborhood. A lower bound
uniform as the singular parameter tends to zero additionally requires
uniform \(\beta\), \(G\), and \(g\); the fixed-parameter separator theorem
alone does not supply those constants.

If actuator leakage produces \(\widetilde M=M+E\) with a proved bound
\(\|E\|_2\le\eta<m\), Weyl's inequality gives

\[
 \sigma_{\min}(\widetilde M)\ge m-\eta>0.
 \tag{3.11}
\]

## 4. A quantitative inverse radius

A pointwise singular value does not give the size of a usable control
neighborhood. The next estimate supplies one.

> **Theorem 4.1 (covered target ball).** Let
> \(x_0=(b_0,a_{{\rm op},0})\). Suppose \(\mathcal Q\) is \(C^1\) on
> \(\overline B_R(x_0)\), with
>
> \[
>  \sigma_{\min}(D\mathcal Q(x_0))\ge m_0>0,
>  \qquad
>  \|D\mathcal Q(x)-D\mathcal Q(y)\|_2
>   \le L\|x-y\|_2.
>  \tag{4.1}
> \]
>
> If \(L>0\), then for every
>
> \[
>  0<r\le R,
>  \qquad
>  Lr<m_0,
>  \tag{4.2}
> \]
>
> the image \(\mathcal Q(B_r(x_0))\) contains the target ball centered at
> \(\mathcal Q(x_0)\) of radius
>
> \[
>  \rho(r)=m_0r-\frac L2r^2.
>  \tag{4.3}
> \]
>
> Every target in that ball has a unique preimage in \(B_r(x_0)\). One
> conservative closed choice is
>
> \[
>  r_*=\min\{R/2,m_0/(2L)\},
>  \qquad
>  \rho_*=m_0r_*-\frac L2r_*^2,
>  \tag{4.4}
> \]
>
> whose contraction factor is at most \(1/2\). If \(L=0\), take
> \(r_*=R/2\) and \(\rho_*=m_0R/2\).

**Proof.** Write \(A_0=D\mathcal Q(x_0)\) and

\[
 N(x)=\mathcal Q(x)-\mathcal Q(x_0)-A_0(x-x_0).
 \tag{4.5}
\]

On \(B_r(x_0)\), (4.1) implies

\[
 \|N(x)\|\le\frac L2\|x-x_0\|^2,
 \qquad
 \|N(x)-N(y)\|\le Lr\|x-y\|.
 \tag{4.6}
\]

For a target displacement \(z\), use

\[
 \mathcal T_z(x)
 =x_0+A_0^{-1}\{z-N(x)\}.
 \tag{4.7}
\]

Since \(\|A_0^{-1}\|\le m_0^{-1}\), (4.2) and (4.6) make
\(\mathcal T_z\) a contraction. If \(\|z\|<\rho(r)\), it maps the closed
input ball into itself. Banach's theorem gives existence and uniqueness.
The choices in (4.4) give the stated constants. \(\square\)

Thus a validated \(\beta\), separator ratio \(C_\Gamma/g\), and derivative
Lipschitz bound \(L\) produce a nonzero three-output target ball, rather
than merely a nonzero determinant.

## 5. An exactly verifiable Hopf frequency--amplitude pair

The block theorem reduces the positive design to a two-by-two question.
The following exact family proves that this condition is mathematically
consistent and supplies a normal-form comparison matrix.

Let \(z\in\mathbb C\), \(b\in\mathbb R^2\), and consider

\[
 \dot z=\{\lambda(b)+i\omega(b)\}z
       -(1+ic)|z|^2z,
 \tag{5.1}
\]

where \(c\in\mathbb R\) and

\[
 \lambda(b)=\lambda_0+\ell^T(b-b_0),
 \qquad
 \omega(b)=\omega_0+w^T(b-b_0).
 \tag{5.2}
\]

On a box where

\[
 \lambda(b)>0,
 \qquad
 \Omega(b):=\omega(b)-c\lambda(b)>0,
 \tag{5.3}
\]

there is a hyperbolic attracting periodic orbit, modulo phase,

\[
 z_b(t)=\sqrt{\lambda(b)}e^{i\Omega(b)t}.
 \tag{5.4}
\]

For \(h(z)=\operatorname{Re}z\), its maximum and minimum are unique modulo
one period and nondegenerate. Directly,

\[
 F=\frac{\Omega}{2\pi},
 \qquad
 A=(2\sqrt\lambda)^2=4\lambda.
 \tag{5.5}
\]

> **Theorem 5.1 (exact Hopf response).** The response of (5.5) is
>
> \[
>  B_H=
>  \begin{pmatrix}
>   (w-c\ell)^T/(2\pi)\\
>   4\ell^T
>  \end{pmatrix}.
>  \tag{5.6}
> \]
>
> It is nonsingular exactly when
>
> \[
>  \det\begin{pmatrix}\ell^T\\w^T\end{pmatrix}\ne0.
>  \tag{5.7}
> \]
>
> More quantitatively, put
>
> \[
> \begin{aligned}
>  d_H&=|\det B_H|
>      =\frac2\pi
>       \left|\det\begin{pmatrix}\ell^T\\w^T\end{pmatrix}\right|,\\
>  q_H&=\|B_H\|_F^2
>      =\frac{\|w-c\ell\|^2}{4\pi^2}+16\|\ell\|^2.
> \end{aligned}
> \tag{5.8}
> \]
>
> Then
>
> \[
>  \boxed{
>  \beta_H
>  =\left\{\frac{q_H-\sqrt{q_H^2-4d_H^2}}2\right\}^{1/2}>0,}
>  \tag{5.9}
> \]
>
> and \(\beta_H\ge d_H/\sqrt{q_H}\).

**Proof.** In polar variables,

\[
 \dot r=(\lambda-r^2)r,
 \qquad
 \dot\theta=\omega-cr^2.
 \tag{5.10}
\]

Equations (5.3)--(5.5) and the extremum statements follow. Differentiating
(5.5) gives (5.6), whose determinant gives (5.7)--(5.8). The squared
singular values are the roots of \(s^2-q_Hs+d_H^2=0\), proving (5.9).
Finally \(d_H=\sigma_{\min}(B_H)\sigma_{\max}(B_H)\) and
\(\sigma_{\max}(B_H)\le\|B_H\|_F\). \(\square\)

For \(\ell=(1,0)\) and \(w=(0,1)\), \(\det B_H=-2/\pi\) for every shear
\(c\). Thus nonlinear frequency shear cannot destroy the independent
growth-rate and angular-frequency directions.

This exact cubic normal form is a witness, not a proof for the declared FHN
RFDE. If a validated reduction or direct adjoint computation proves

\[
 \|B_{\rm FHN}-B_H\|_2\le\eta<\beta_H,
 \tag{5.11}
\]

then Weyl's inequality gives

\[
 \sigma_{\min}(B_{\rm FHN})\ge\beta_H-\eta>0.
 \tag{5.12}
\]

No such \(\eta\) is asserted here.

## 6. The interval test required for synchronous FHN

Validated continuation must enclose the periodic orbit, bordered inverse,
unique extrema, and both response rows, obtained from adjoints or equivalent
sensitivity columns. Suppose it gives

\[
 B_{\rm FHN}\in\bar B+[-R_B,R_B],
 \qquad
 R_B\ge0\quad\hbox{entrywise}.
 \tag{6.1}
\]

Every error matrix \(E\) in (6.1) obeys

\[
 \|E\|_2\le\|E\|_F\le\|R_B\|_F.
 \tag{6.2}
\]

For a computer-assisted proof, let \(\underline s_B\) be a
directed-rounding lower bound for \(\sigma_{\min}(\bar B)\), and let
\(\overline r_B\) be a directed-rounding upper bound for
\(\|R_B\|_F\). The checkable condition is

\[
 \boxed{
 \beta_{\rm box}
 :=\underline s_B-\overline r_B>0.}
 \tag{6.3}
\]

Weyl's inequality then proves, for every response in the interval,

\[
 \sigma_{\min}(B_{\rm FHN})\ge\beta_{\rm box}.
 \tag{6.4}
\]

If (2.6) is also enclosed, Theorem 3.1 gives

\[
 \sigma_{\min}(D\mathcal Q)
 \ge m(\beta_{\rm box},C_\Gamma/g).
 \tag{6.5}
\]

Condition (6.3) is in singular-value form because a nonzero midpoint
determinant controls no other matrix in the interval box. The helper
floating_interval_candidate_diagnostic evaluates the analogous expression
with ordinary NumPy floats only. Its positive output is a candidate for
directed verification, not an interval certificate: it does not outward
round the box endpoints, the midpoint singular value, or the Frobenius
norm.  That former gate is now closed by the independent MPFR-directed
finite/tail proof in
[paper-iv-periodic-parameter-box.md](paper-iv-periodic-parameter-box.md),
which gives \(\beta_U\ge0.0162187\) on its declared microscopic gain box.

A rigorous declared-FHN implementation has now supplied the first four
items below, with the qualification in item 4, and still needs the last two:

1. a periodic-orbit residual and inverse bound for the bordered RFDE BVP;
2. exactly one maximum and minimum, with interval curvature bounded away
   from zero;
3. a directed squared-range sensitivity/response enclosure, including all
   moving-delay and moving-period terms;
4. exclusion of every nontrivial unit-circle multiplier; if attraction of
   the baseline orbit is part of the claim, a separate stable-index or
   multiplier-count argument;
5. a lower reset-transversality bound \(g\) and upper separator derivative
   bound \(G\); and
6. a derivative Lipschitz bound \(L\) to claim a nonzero target radius.

Floating-point continuation can propose these enclosures, but cannot
replace them.

## 7. Result ledger

| Claim | Status | Scope |
|---|---|---|
| Reset-only actuator leaves baseline \(F,A\) unchanged | Proved exactly | Protocol identity (1.3), provided there is no actuator leakage |
| Local laboratory threshold \(a_c(b)\) | Proved from a jointly \(C^1\) parameterized complete-history separator/reset pair and transverse reset | Proposition 2.1 |
| Collective-clamp channel separator | Proved elsewhere under stated RFDE hypotheses | Small positive fixed singular parameter; controlled protocol |
| Unforced physical pulse separator | Open | Needs the saddle--slow-history exchange theorem |
| Equality of \(a_c\) with a maximal-canard root | Not asserted | Needs a reset-to-canard factorization |
| Block-triangular \(3\times3\) response | Proved exactly | Theorem 3.1 |
| Positive full smallest-singular-value bound | Proved from \(\beta>0\) and finite \(\gamma\) | Formula (3.5) |
| Nonzero local target radius | Proved when \(L\) is supplied | Theorem 4.1 |
| Hopf frequency--amplitude nondegeneracy | Proved for the exact cubic family | Theorem 5.1 |
| Declared synchronous FHN periodic branch, unique extrema, and orbital Floquet hyperbolicity | Proved on the microscopic gain box | Directed D1/D3 certificate plus the 319-cell full-complex Bloch theorem; attraction is not inferred |
| Declared FHN two-by-two response certificate | Proved on the microscopic gain box | Directed \(\beta_U\ge0.0162187\) |
| Declared FHN positive \(3\times3\) control theorem | Conditional | The periodic block is supplied; still needs the clamped reset constants in (2.6) and, for a radius, (4.1) |

The old design could lose a singular direction when amplitude and safety
both followed the same thin canard coordinate. The repaired protocol puts
safety on an independent experimental coordinate whose derivative is
exactly \(-1\). This removes that structural obstruction.  The ordinary
two-output periodic response is now certified on a microscopic box, but
the reset transversality, response-Lipschitz/target-radius, hardware, and
Floquet-attraction gates are not thereby supplied.  Nor is the controlled
separator renamed as an unforced canard threshold.
