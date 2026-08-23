# Paper III U-OUT\({}^+\): the fixed-chart obstruction and a sufficient jet gate

Status: **Propositions 1.1, 1.2, and 2.1 and Theorem 3.1 below are
proved. They show that the existing fixed-\(p\) logarithmic right-fold
construction cannot, by its present endpoint estimate alone, prove the
action-supercritical residual U-OUT-RES, and that the value hypotheses
B1--B4 do not imply the uniform parameter jets U-OUT-J. These are
logical no-go results, not a proof that the physical residual is nonzero.
The physical terminal BVP, common-history leaf, two-sided sensitivity, and
an exact or action-supercritical \(C^1\) residual remain open.**

The logarithmic comparisons and the exact oscillatory-jet counterexample
are implemented in src/canard_control/u_out_action_scale.py and tested in
tests/test_u_out_action_scale.py. This note does not change the frozen JNS
manuscript.

## 1. A fixed logarithmic fold chart cannot pay a fixed outer action

The canonical local theorem fixes one number \(p>0\), independently of
\(\delta\), and uses

\[
 S_\delta=\sqrt{2p\log(1/\delta)}.
 \tag{1.1}
\]

After any fixed polynomial and finite-backtrack losses, its endpoint
suppression has the form

\[
 E_\delta
 =C_E\delta^{p-M_E}e^{c_ES_\delta}.
 \tag{1.2}
\]

By contrast, the terminal matching theorem requires a residual no larger
than

\[
 R_\delta
 =C_R\delta^{-M_R}
   \exp\!\left[-\frac{A+\chi}{\delta^2}
                    +\frac{L_R}{\delta}\right],
 \qquad A>0,\quad\chi>0.
 \tag{1.3}
\]

> **Proposition 1.1 (fixed-\(p\) action obstruction; PROVED).**
> For every fixed finite choice of
> \(p,M_E,M_R,c_E,L_R\geq0\), \(C_E,C_R>0\), and
> \(A+\chi>0\),
> \[
>  \frac{E_\delta}{R_\delta}\longrightarrow+\infty
>  \qquad(\delta\downarrow0).
>  \tag{1.4}
> \]
> Consequently, a proof supplying only
> \(|m_\delta(0)|\leq E_\delta\) cannot imply the U-OUT-RES
> bound \(|m_\delta(0)|\leq R_\delta\). This failure already occurs
> in the scalar ODE subclass of RFDEs.

**Proof.** Write \(\ell_\delta=\log(1/\delta)\). Directly,

\[
 \log\frac{E_\delta}{R_\delta}
 =\frac{A+\chi}{\delta^2}-\frac{L_R}{\delta}
  -(p-M_E+M_R)\ell_\delta
  +c_E\sqrt{2p\ell_\delta}+\log\frac{C_E}{C_R}.
 \tag{1.5}
\]

The first term dominates every other displayed term, proving (1.4).
For logical sharpness, consider

\[
 \delta^2 n_s=a(s)n,\qquad
 \int_0^L a(s)\,ds=A,\qquad n(0)=E_\delta.
 \tag{1.6}
\]

This is an RFDE whose functional ignores the past. It saturates the local
upper bound, whereas its required terminal coordinate is

\[
 n(L)=E_\delta e^{A/\delta^2}\longrightarrow\infty.
\]

Thus no implication from the scale (1.2) to bounded terminal matching is
valid without an additional cancellation or a stronger estimate.
\(\square\)

This proposition does **not** assert that the physical mismatch saturates
(1.2). It leaves two possible closures: an exact identity
\(m_\delta(0)=0\), or a new global argument proving a bound genuinely
smaller than (1.3). What it rules out is obtaining that conclusion merely
by increasing the one fixed exponent \(p\) in the existing local theorem.

> **Proposition 1.2 (required chart radius; PROVED).**
> Ignore only fixed polynomial, \(e^{L/\delta}\), and prefactor losses. If
> a Gaussian endpoint factor \(e^{-S_\delta^2/2}\) is to be no larger than
> \(e^{-(A+\chi)/\delta^2}\), then
> \[
>  S_\delta\geq\frac{\sqrt{2(A+\chi)}}{\delta}.
>  \tag{1.7}
> \]
> With the logarithmic form (1.1), this requires
> \[
>  p=p_\delta\geq
>  \frac{A+\chi}{\delta^2\log(1/\delta)}.
>  \tag{1.8}
> \]
> With all fixed losses restored, (1.8) remains valid with a
> \(1+o(1)\) factor. Hence \(p_\delta\to\infty\), while the physical fold
> radius satisfies
> \[
>  \delta S_\delta\geq\sqrt{2(A+\chi)}+o(1),
>  \tag{1.9}
> \]
> rather than tending to zero.

**Proof.** Taking logarithms of the two Gaussian factors gives (1.7), and
substitution of (1.1) gives (1.8). In the full comparison, all omitted
terms are \(O(\delta^{-1})+O(\log(1/\delta))\), whereas the action is
\((A+\chi)\delta^{-2}\); solving the resulting quadratic in
\(S_\delta\) proves the \(1+o(1)\) statement and (1.9). \(\square\)

Equation (1.9) is the geometric content of the obstruction. Paying the
whole outer action by Gaussian suppression would extend the chart to a
fixed physical distance from the fold. That is a global outer BVP, not
the shrinking \(K_2\) theorem already proved.

For the declared reset \(\rho_R=-1/2\), the audited singular action is

\[
 A_R=0.5607898753226717\ldots .
 \tag{1.10}
\]

The decimal is only a reproducible diagnostic; Propositions 1.1--1.2 use
only \(A_R>0\), which was proved from the exact singular geometry.

## 2. A value residual does not control U-OUT-J

Theorem 6.1 in the terminal-matching note uses the value residual
\(|m(0,u)|\leq r_\delta\) and a derivative floor
\(|\partial_\beta m|\geq d_\delta\). Those hypotheses select a small
root for each fixed \(\delta\), but they contain no uniform information
about its parameter derivative.

> **Proposition 2.1 (oscillatory terminal-root counterexample; PROVED).**
> Let \(A>\chi>0\), \(\varepsilon=\delta^2\), and set
> \[
>  d_\delta=e^{-A/\varepsilon},\qquad
>  r_\delta=e^{-(A+\chi)/\varepsilon},\qquad
>  \omega_\delta=e^{2\chi/\varepsilon}.
>  \tag{2.1}
> \]
> On \([-1,1]\times[-1,1]\), define
> \[
>  m_\delta(\beta,u)
>  =d_\delta\beta+r_\delta\sin(\omega_\delta u).
>  \tag{2.2}
> \]
> Then \(\partial_\beta m_\delta=d_\delta>0\),
> \(|m_\delta(0,u)|\leq r_\delta\), and for all small \(\delta\)
> the unique root satisfies
> \[
>  |\beta_\delta^*(u)|\leq e^{-\chi/\varepsilon}\to0.
>  \tag{2.3}
> \]
> Nevertheless,
> \[
>  |\partial_u\beta_\delta^*(0)|
>  =e^{\chi/\varepsilon}\longrightarrow\infty.
>  \tag{2.4}
> \]
> Thus B3--B4, even at the exact action-supercritical scales, do not imply
> U-OUT-J. In fact, the example may be embedded in an exact
> terminal-normalized ODE family satisfying the analogues of B1--B4.

**Proof.** The root is exactly

\[
 \beta_\delta^*(u)
 =-\frac{r_\delta}{d_\delta}
   \sin(\omega_\delta u).
\]

Equations (2.3)--(2.4) follow by substitution. Moreover, (2.2) is not an
artificial Banach-space pathology. Fix a delay length \(\tau>0\), extend
\(a(s)>0\) smoothly to the incoming buffer
\([ -\delta^2\tau,L]\), and take the autonomous ODE subclass

\[
 \dot s=\delta^2,\qquad \dot n=a(s)n,\qquad
 a(s)>0,\qquad \int_0^L a(s)\,ds=A.
\]

The terminal-normalized family

\[
 n_\beta(s)=\beta
 \exp\!\left[-\delta^{-2}\int_s^L a(r)\,dr\right]
\]

is exact, remains in \(|n|\leq1\) for \(|\beta|\leq1\), and has incoming
current value \(d_\delta\beta\). Its complete incoming history is

\[
 \mathcal G_\delta(\beta)(\vartheta)
 =\left(\delta^2\vartheta,
   \beta\exp\!\left[-\delta^{-2}
       \int_{\delta^2\vartheta}^{L}a(r)\,dr\right]\right),
 \qquad -\tau\le\vartheta\le0.
\tag{2.5}
\]

Set
\(\beta_{\rm can}(u)=-(r_\delta/d_\delta)
\sin(\omega_\delta u)\) and
\(\phi^{\rm can}_{\delta,u}=\mathcal G_\delta(\beta_{\rm can}(u))\).
On the affine history leaf
\(\phi^{\rm can}_{\delta,u}
 +\operatorname{span}\{\partial_\beta\mathcal G_\delta\}\), use the bounded
chart given by present normal evaluation. Then

\[
 \Xi_{\delta,u}\!\left(
   \mathcal G_\delta(\beta)-\phi^{\rm can}_{\delta,u}
 \right)
 =d_\delta(\beta-\beta_{\rm can}(u))
 =m_\delta(\beta,u).
\tag{2.6}
\]

Thus \(m=0\) is equivalent to equality of the **complete** histories, not
only of their present states, and the analogues of B1--B4 hold. Because
\(A>\chi\), the canonical incoming-history derivative has size at most
\(r_\delta\omega_\delta=e^{-(A-\chi)/\varepsilon}\), whereas the terminal
coordinate derivative in (2.4) diverges. All data are \(C^1\) for every
fixed positive \(\delta\), but no uniform selected-root jet follows.
\(\square\)

The example identifies the missing quantifier. Fixed-\(\delta\)
differentiability is not a uniform \(C^1_u\) estimate.

## 3. The exact scalar ratio and one robust sufficient condition

The exact condition needed for U-OUT-J can be stated without a full RFDE
trichotomy: the root ratios below, multiplied by the known terminal-family
mixed-jet losses, must have the orders required by (3.5). A fixed positive
action margin is one robust sufficient way to guarantee this, but is not
necessary.

> **Theorem 3.1 (terminal root with a uniform parameter jet; PROVED).**
> Let \(U\subset\mathbb R^q\) be open and
> \(m_\delta\in C^1([-R,R]\times U,\mathbb R)\). Suppose
> \(\partial_\beta m_\delta\) has one sign and
> \[
>  |\partial_\beta m_\delta|\geq d_\delta>0,\qquad
>  |m_\delta(0,u)|\leq r_\delta<d_\delta R.
>  \tag{3.1}
> \]
> Then for every \(u\in U\) there is a unique
> \(\beta_\delta^*(u)\in(-R,R)\) satisfying
> \(m_\delta(\beta_\delta^*(u),u)=0\). If in addition
> \[
>  \|D_um_\delta(\beta_\delta^*(u),u)\|
>  \leq s_\delta,
>  \tag{3.2}
> \]
> then
> \[
>  \sup_{u\in U}|\beta_\delta^*(u)|
>  \leq\frac{r_\delta}{d_\delta},\qquad
>  \sup_{u\in U}\|D_u\beta_\delta^*(u)\|
>  \leq\frac{s_\delta}{d_\delta}.
>  \tag{3.3}
> \]
> In particular, fix \(R,U,A,\chi_r,\chi_s,c_d,C_r,C_s,L_d,L_r,L_s\)
> and the exponents \(M_d,M_r,M_s\), independently of \(\delta\). If
> \[
> \begin{aligned}
>  d_\delta&\geq
>   c_d\delta^{M_d}e^{-A/\delta^2-L_d/\delta},\\
>  r_\delta&\leq
>   C_r\delta^{-M_r}
>   e^{-(A+\chi_r)/\delta^2+L_r/\delta},\\
>  s_\delta&\leq
>   C_s\delta^{-M_s}
>   e^{-(A+\chi_s)/\delta^2+L_s/\delta},
> \end{aligned}
> \tag{3.4}
> \]
> with \(\chi_r,\chi_s>0\), then there exists \(\delta_0>0\) such that for
> every \(0<\delta\le\delta_0\) the root is defined as above and both
> quantities in (3.3) tend to zero faster than every algebraic power of
> \(\delta\).

**Proof.** The endpoint sign argument in Lemma 4.1 of the terminal-matching
note gives existence and uniqueness and the first inequality in (3.3).
Differentiating \(m_\delta(\beta_\delta^*(u),u)=0\) gives

\[
 D_u\beta_\delta^*
 =-\frac{D_um_\delta(\beta_\delta^*,u)}
         {\partial_\beta m_\delta(\beta_\delta^*,u)},
\]

which proves the second. Dividing the last two lines of (3.4) by the
first leaves a positive \(\delta^{-2}\) action margin; it dominates all
fixed polynomial and \(\exp(L/\delta)\) losses. \(\square\)

For the physical tracker, (3.2)--(3.4) must be combined with uniform
\(C^1_u\) bounds on the terminal family and its \(\beta\)-derivative.
If those family bounds have only fixed polynomial and
\(e^{L/\delta}\) losses, (3.4) makes the correction terms
\(D_\beta\mathcal K\,\beta_\delta^*\) and
\(D_\beta\mathcal K\,D_u\beta_\delta^*\) superalgebraically small.
The ordinary compact normally hyperbolic tracker estimate would then yield

\[
 \|z^m_{\delta,u}-z^m_{0,u}\|_{C^1_uC^0_t}=O(\delta),
 \qquad
 \|\dot\rho\|_{C^1_uC^0_t}=O(\delta^2).
 \tag{3.5}
\]

That last physical implication is **CONDITIONAL** on the terminal-family
bounds and the ordinary compact outer estimate; Theorem 3.1 proves only
the scalar jet step and shows the precise additional residual that must be
estimated.

It is useful to name this convenient sufficient hypothesis:

> **B5 (sufficient action-supercritical parameter residual; OPEN for the physical
> RFDE).** The differentiated physical mismatch at the selected terminal
> root obeys the third line of (3.4), uniformly over the fixed control box,
> and the terminal family has only fixed polynomial/\(e^{L/\delta}\)
> mixed-jet losses.

B4 and B5 are not duplicates. B4 bounds the value \(m_\delta(0,u)\) and
therefore the size of the terminal correction. B5 bounds
\(D_um_\delta(\beta_\delta^*(u),u)\) and therefore its parameter jet.
B5 is automatic if the reference match is an exact identity jointly in
\(u\): then both the value residual and its parameter derivative vanish.
It is not automatic from pointwise exact matching at one parameter. Nor is
B5 necessary: if the known terminal-family mixed-jet loss is
\(\mathcal L_\delta\), the exact requirement is that
\(\mathcal L_\delta s_\delta/d_\delta\) (and the corresponding value ratio)
obey the orders demanded by (3.5). For example, a merely
\(e^{-(L+1)/\delta}\) ratio already defeats an \(e^{L/\delta}\) family loss
without a positive \(\delta^{-2}\) action margin.

## 4. Consequence for the physical U-OUT\({}^+\) program

The method-of-steps identity remains useful but does not remove this
obstruction. Because \(\rho_T=\xi-\mu<0\) and the slow delays are
\(h_k=\delta\theta_k\), every delayed query lies upstream in \(\rho\).
Thus an exact incoming history generates a causal curve-restricted solution
until reset or tube exit. This proves the continuation alternative, but a
forward-unstable normal error is still multiplied by
\(e^{A_R/\delta^2}\). Causality proves existence; it does not prove
containment.

The strongest justified closure statement is therefore the following.

> **Revised U-OUT\({}^+\) completion (CONDITIONAL).** B1
> (physical terminal family), B2 (exact complete-history leaf), B3
> (two-sided action sensitivity), B4 (an exact or action-supercritical
> value residual), and either B5 or any quantitative ratio estimate strong
> enough after the known terminal-family losses, together with uniform
> terminal-family jets, imply the exact reset-reaching tracker
> and the finite-segment bounds (3.5). The selected future-extension and
> direct relative-growth graph theorems may then be applied without a full
> RFDE stable foliation.

For the current physical two-module model, the status is:

| Assertion | Status | Reason |
|---|---|---|
| Exact causal method-of-steps continuation until reset or exit | **PROVED** | Forward RFDE well-posedness and monotone \(\rho\) |
| Fixed-\(p\) local endpoint bound implies U-OUT-RES | **FALSE as an implication** | Proposition 1.1 and scalar RFDE-subclass saturation |
| Increasing one fixed \(p\) reaches the action scale | **FALSE** | Proposition 1.2; the required \(p_\delta\) diverges |
| B1--B4 imply uniform U-OUT-J | **FALSE as an implication** | Proposition 2.1 |
| Scalar root and uniform root jet under the ratio bound; B5 is sufficient | **PROVED** | Theorem 3.1 |
| Physical U-OUT-BVP / U-OUT-LEAF / U-OUT-SENS | **OPEN** | No exact fold-to-reset terminal family or differentiated Green identity has been constructed |
| Physical U-OUT-RES / parameter-jet ratio | **OPEN** | Requires exact global selection coherence or quantitative value and derivative residuals strong enough after terminal-family losses |
| Physical U-OUT\({}^+\) | **OPEN** | Depends on the preceding physical statements |

There are only two mathematically honest routes past the fixed-chart
obstruction. One may prove that the physical terminal normalization and
the canonical retained trace agree **exactly**, including their parameter
jets; or one may define and analyze a separate global fold-to-reset root by
a terminal-normalized BVP. The second root may differ from the existing
preparation-indexed local root by a beyond-all-orders amount, even though
both have the same algebraic canard coefficient. Equality of those exact
finite-\(\delta\) roots is an additional theorem, not a consequence of
their common asymptotic expansion.
