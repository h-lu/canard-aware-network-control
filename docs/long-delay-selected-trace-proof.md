# Long-delay selected traces and the normalized canard gap

Status: **an abstract trace-to-gap implication is proved below, but its
selected-trace and growing mixed-graph inputs are not proved for the
long-delay RFDE.** In particular, this note does
not close Gate D and does not promote the conditional coefficient
\(1/(4\alpha)\) to an RFDE maximal-canard theorem. It identifies a smaller
missing statement than full-neighborhood \(K_1\) regularity: a curve-wise,
Gaussian-weighted estimate for the two selected outer-to-inner trace maps.

The distinction is essential. The first-integral weight suppresses an
endpoint after suitable bounds on its parameter derivatives have been
established; it does not itself establish those derivative bounds.

## 1. Coordinates, sections, and constants

Fix the data

\[
 K\ne0,\qquad D_w>0,\qquad
 0<\theta _0<\theta _1,\qquad
 |\eta|\leq\eta_*,
\]

and fix the attracting and repelling outer slow-history selections. Every
constant below may depend on these data, the selections, a compact
\(\nu\)-interval about

\[
 \nu _0=-\frac{11}{24\alpha},
 \qquad \alpha=\frac{\sqrt6}{4},
\]

and the declared uncut physical neighborhood, but not on
\(\delta,\nu,\eta\).

In the \(K_2\) variables of the final model, put

\[
 z=(X,Y),\qquad
 q_0(X,Y)=(Y-\alpha X^2,-X),
\]

and write the distinguished singular connection as

\[
 \gamma_0(s)=
 \left(-\frac{s}{2\alpha},\frac{s^2-2}{4\alpha}\right).
\tag{1}
\]

For a number \(p>4\), to be fixed after the tame algebraic loss in Lemma T
is known, let

\[
 S_\delta=\sqrt{2p\log(1/\delta)}.
\tag{2}
\]

The auxiliary transition sections are

\[
 \Sigma^a_\delta:
 Y=\frac{S_\delta^2-2}{4\alpha},\ X<0,
 \qquad
 \Sigma^r_\delta:
 Y=\frac{S_\delta^2-2}{4\alpha},\ X>0.
\tag{3}
\]

They recede in \(K_2\), but their physical fold radius tends to zero:

\[
 r_{1,\delta}
 =\delta\sqrt{\frac{S_\delta^2}{4}-\frac12}
 =\frac{\delta S_\delta}{2}
   \left(1+O(S_\delta^{-2})\right).
\tag{4}
\]

Thus (3) are matching sections, not replacements for the fixed outer
selections.

Use the Krupa--Szmolyan coordinates

\[
 x=-\alpha X,\qquad y=\alpha Y,
\]

and define

\[
 H(x,y)=\frac12e^{-2y}\left(y-x^2+\frac12\right),
 \qquad
 \mathscr H(X,Y)=H(-\alpha X,\alpha Y).
\tag{5}
\]

Along (1),

\[
 \nabla\mathscr H(\gamma_0(s))
 =\frac{\alpha e}{2}
   e^{-s^2/2}(s,1)^T.
\tag{6}
\]

Let \(z^a_{\delta,\nu,\eta}\) and
\(z^r_{\delta,\nu,\eta}\) denote the reduced images of the fixed selected
attracting and repelling histories. Parameterize each by its actual reduced
flow time and translate that time so that it meets the matching section
\(X=0\) at time zero. Thus

\[
 z^a(0),z^r(0)\in\{X=0\}.
\]

Let \(t_a=t_a(\delta,\nu,\eta)<0\) and
\(t_r=t_r(\delta,\nu,\eta)>0\) be their respective hitting times of
\(\Sigma^a_\delta\) and \(\Sigma^r_\delta\). They are not set equal to
\(-S_\delta\) and \(S_\delta\). Define

\[
 D(\delta,\nu,\eta)
 =\frac{2}{\alpha e}
 \left[
  \mathscr H(z^a_{\delta,\nu,\eta}(0))
  -\mathscr H(z^r_{\delta,\nu,\eta}(0))
 \right].
\tag{7}
\]

This is the unscaled gap. The normalized gap used for the implicit-function
argument is \(D/\delta\).

## 2. The exact selected-trace estimate that is needed

For \(c,m\geq0\), set

\[
 \|f\|_{G;c,m,I}
 =\int_I e^{-s^2/2+c|s|}
          \langle s\rangle^m |f(s)|\,ds,
 \qquad \langle s\rangle=(1+s^2)^{1/2}.
\tag{8}
\]

This is an integral norm, not an unweighted supremum on the growing tube.
The Gaussian is decisive: for fixed \(c,m\),

\[
 \sup_{S\geq1}
 \int_{-S}^{S}e^{-s^2/2+c|s|}\langle s\rangle^m\,ds<\infty.
\tag{9}
\]

The following is the missing model-specific statement.

> **Selected-trace lemma T (open for the final long-delay RFDE).** There are
> \(c,m,C,M>0\) such that the fixed outer selections reach (3), belong to the
> uncut invariant-history graph together with every delayed backtrack used
> there, cross their section transversely exactly once, and depend \(C^1\) on
> \(\nu\) and \(C^2\) on \(\eta\). After the
> matching-section phase is fixed, their hitting times satisfy
> \[
>  t_a=-S_\delta+O(1),\qquad t_r=S_\delta+O(1),
> \tag{T0}
> \]
> and their two one-sided reduced traces satisfy
> \[
> \begin{aligned}
>  \sum_{\sigma=a,r}
>  \|z^\sigma-\gamma_0\|_{G;c,m,I_\sigma}
>    &\leq C\delta,\\
>  \sum_{\sigma=a,r}
>  \|\partial_\nu z^\sigma\|_{G;c,m,I_\sigma}
>    &\leq C\delta,\\
>  \sum_{\sigma=a,r}
>  \left(
>   \|\partial_\eta z^\sigma\|_{G;c,m,I_\sigma}
>   +\|\partial_{\eta\eta}z^\sigma\|_{G;c,m,I_\sigma}
>   +\||\partial_\eta z^\sigma|^2\|_{G;c,m,I_\sigma}
>  \right)&\leq C\delta^2,
> \end{aligned}
> \tag{T1}
> \]
> where \(I_a=[t_a,0]\) and \(I_r=[0,t_r]\). At the outer ends, through
> the same derivatives and with total derivatives of the endpoint maps,
> \[
>  |x_1|+|\mathscr D x_1|+|\mathscr D^2x_1|
>  +|\mathscr D t_{a/r}|+|\mathscr D^2t_{a/r}|
>  \leq C\delta^{-M}\langle S_\delta\rangle^m e^{cS_\delta},
> \tag{T2}
> \]
> for the derivatives \(\mathscr D\) used in (T1).

The powers of \(\delta\) in (T1) are forced by the final chart: \(\nu\)
first occurs in \(\delta q_1\), whereas \(\eta\) first occurs in
\(\delta^2q_2\). The factor \(e^{c|s|}\) allows the genuine derivative loss
of a fixed \(K_2\) backtrack near the \(K_1\) boundary. A polynomial-only
trace norm is not justified. The fixed algebraic loss \(\delta^{-M}\) in
(T2) is harmless after \(p\) is chosen, but its exponent must be proved and
must not depend on the derivative order being estimated.

## 3. Endpoint suppression

The next lemma is a consequence of (T2); it does not prove (T2).

**Lemma 1 (selected endpoint suppression).** Suppose (T2) holds. For every
fixed finite list of the indicated parameter derivatives and every
\(N>0\), increasing the fixed number \(p\) in (2), if necessary, gives

\[
 \left|
  \mathscr D\mathscr H(z^a(t_a))
 \right|
 +
 \left|
  \mathscr D\mathscr H(z^r(t_r))
 \right|
 =O(\delta^N).
\tag{10}
\]

**Proof.** At either endpoint, the section definition, rather than the
flow-time parameterization, gives

\[
 y=\frac{S_\delta^2}{4}-\frac12,
 \qquad e^{-2y}=e^{1-S_\delta^2/2}.
\]

Every fixed derivative of (5) is this Gaussian factor times a polynomial in
\(x,y\). Expressing \(x=x_1\sqrt y\), applying the chain rule, and using
(T2) gives

\[
 |\mathscr D\mathscr H|
 \leq C\delta^{-M'}\langle S_\delta\rangle^{m'}
       e^{-S_\delta^2/2+c'S_\delta}.
\]

For each \(\kappa>0\), the last expression is
\(O(\delta^{p-M'-\kappa})\). Choose \(p>N+M'\) and then
\(0<\kappa<p-M'-N\). \(\square\)

Boundedness of \(x_1\) without its parameter derivatives is not enough for
(10). The derivative bounds in (T2) are a real hypothesis, not harmless
bookkeeping.

## 4. A proved trace-to-gap theorem

Assume that on the selected logarithmic tube the actual reduced field has
the remainder-controlled expansion

\[
 Q_{\delta,\nu,\eta}
 =q_0+\delta q_1(\cdot,\nu)
       +\delta^2q_2(\cdot,\nu,\eta)
       +\delta^3R_3(\cdot,\delta,\nu,\eta),
\tag{11}
\]

with two \(\eta\)-derivatives and one \(\nu\)-derivative. Suppose the
coefficients and these derivatives have polynomial-exponential pointwise
bounds compatible with (8). For the final model, the exact formal
coefficients which the mixed-jet graph lemma must promote to (11) are

\[
 \partial_\nu q_1=(0,1)^T,
 \qquad
 \partial_\eta q_1=0,
\tag{12}
\]

and, on (1),

\[
 \partial_\eta q_2(\gamma_0(s),\nu,0)
 =-c_\perp^*s(1,0)^T,
 \qquad
 c_\perp^*=\frac{K(\theta_0-\theta_1)}{4\alpha}.
\tag{13}
\]

**Theorem 2 (selected traces imply the normalized gap estimates).** If
(11)--(13), Lemma T, and the uncut-history membership in Lemma T hold, then,
uniformly for \(\nu\) near \(\nu_0\) and \(|\eta|\leq\eta_*\),

\[
\boxed{
\begin{aligned}
 \partial_\nu D
  &=\delta\sqrt{2\pi}+O(\delta^2),\\
 \partial_\eta D
  &=-\frac{K(\theta_0-\theta_1)}{4\alpha}
    \sqrt{2\pi}\,\delta^2
    +O(\delta^3+\delta^2|\eta|),\\
 \partial_{\eta\eta}D&=O(\delta^2).
\end{aligned}}
\tag{14}
\]

In particular, the last estimate is not an additional Melnikov
calculation; it follows from the \(C^2_\eta\) trace and graph bounds once
their \(\delta\)-orders are retained.

**Proof.** Along either selected trace, (5) and (11) give

\[
 \frac{d}{ds}\mathscr H(z)
 =\delta A_1(z,\nu)
  +\delta^2A_2(z,\nu,\eta)
  +\delta^3A_3(z,\delta,\nu,\eta),
\tag{15}
\]

where \(A_j=\nabla\mathscr H\cdot q_j\) for \(j=1,2\) and
\(A_3=\nabla\mathscr H\cdot R_3\). Splitting at \(s=0\) yields the exact
identity

\[
\begin{aligned}
 \frac{\alpha e}{2}D
 ={}&\mathscr H(z^a(t_a))
     -\mathscr H(z^r(t_r))\\
 &+\int_{t_a}^{0}\frac{d}{ds}\mathscr H(z^a(s))\,ds
  +\int_{0}^{t_r}\frac{d}{ds}\mathscr H(z^r(s))\,ds.
\end{aligned}
\tag{16}
\]

Lemma 1 makes the differentiated endpoint terms smaller than every order
needed below. Differentiating the moving limits in (16) produces the same
Gaussian endpoint factor multiplied by the hitting-time jets in (T2), and
is therefore suppressed by the same lemma. On the two finite integrals,
differentiate under the integral.
The derivatives of \(\mathscr H\) along the tube are a Gaussian times a
polynomial. Hence (9), (T1), and the coefficient bounds give a common
integrable majorant, uniformly in \(\delta\).

For the \(\nu\)-derivative, the only order-\(\delta\) term is

\[
 \delta\nabla\mathscr H(\gamma_0(s))^T(0,1)
 =\frac{\alpha e}{2}\delta e^{-s^2/2}.
\]

Replacing a selected trace by \(\gamma_0\) costs \(O(\delta^2)\) by the
first two estimates in (T1). By (T0), the remainder of the Gaussian integral
outside \([t_a,t_r]\) is
\(O(\delta^{p-\kappa})\) for every fixed \(\kappa>0\).
After the normalization in (16), this proves the first line of (14).

Because \(q_1\) is independent of \(\eta\), differentiating its contribution
in (15) produces

\[
 \delta D_zA_1(z,\nu)\,\partial_\eta z=O(\delta^3)
\]

after integration, by (T1). The only order-\(\delta^2\) term is therefore

\[
 \delta^2\nabla\mathscr H(\gamma_0(s))^T
 \partial_\eta q_2(\gamma_0(s),\nu,0).
\]

Using (6) and (13), its normalized whole-line value is

\[
 -c_\perp^*\delta^2
  \int_{\mathbb R}s^2e^{-s^2/2}\,ds
 =-c_\perp^*\sqrt{2\pi}\,\delta^2.
\]

The replacement of a trace by \(\gamma_0\), the \(R_3\) term, and the
\(\eta\)-variation of \(\partial_\eta q_2\) give respectively
\(O(\delta^3)\), \(O(\delta^3)\), and \(O(\delta^2|\eta|)\). This proves the
second line of (14).

Differentiate (15) twice with respect to \(\eta\). The
\(\delta A_1\) contribution is

\[
 \delta\left[
  D_zA_1\,\partial_{\eta\eta}z
  +D_z^2A_1[\partial_\eta z,\partial_\eta z]
 \right],
\]

which is \(O(\delta^3)\) after integration by (T1). The
\(\delta^2A_2\) contribution contains
\(\delta^2\partial_{\eta\eta}A_2\), which is \(O(\delta^2)\), while every
term containing a trace derivative is of higher order. The twice
differentiated \(\delta^3A_3\) term is \(O(\delta^3)\). Lemma 1 controls the
endpoint terms, proving the third line of (14). \(\square\)

The proof uses the pointwise-in-\(s\) exponential allowance through the
Gaussian norm (8). Replacing it by the crude growing-tube supremum
\(e^{cS_\delta}\) inside the integrals would create false subalgebraic losses.

## 5. Root consequence, conditional on the selected traces and growing graph

The leading gap at \(\delta=0\) is

\[
 \frac{D}{\delta}
 =\sqrt{2\pi}
  \left(\nu+\frac{11}{24\alpha}\right)+O(\delta).
\tag{17}
\]

Consequently, Theorem 2 and the implicit-function theorem would give

\[
 \nu_c(\delta,\eta)-\nu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}
   \delta\eta
  +O(\delta^2|\eta|+\delta\eta^2),
\tag{18}
\]

and, since \(\mu=\delta^2\nu\),

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}
   \delta^3\eta
  +O(\delta^4|\eta|+\delta^3\eta^2).
\tag{19}
\]

Equations (18)--(19) remain conditional because Lemma T is open.

## 6. Why the current theorems do not prove Lemma T

The obstruction is not the Gaussian calculation. In the \(K_1\) coordinate
\(\rho=\sqrt{\epsilon_1}\), a fixed \(K_2\) delay is a past time
\(\theta/\rho+O(1)\). Along the attracting singular branch, there are
constants \(c_0,C_0>0\) such that the backward flow satisfies

\[
 \|D\Phi_{q_0}^{-\theta}\|
 \geq C_0\exp\left(\frac{c_0\theta}{\rho}\right)
\tag{20}
\]

At (3), \(\rho=2S_\delta^{-1}(1+O(S_\delta^{-2}))\), so (20) already forces a
single-exponential loss \(e^{cS_\delta}\); the exact exponent is not needed.
On a fixed \(K_1\) neighborhood,
however, \(\rho\downarrow0\) independently of \(\delta\), and no uniform
\(C^1\) bound exists. Thus Krupa--Szmolyan Proposition 3.4, which assumes a
smooth vector field on a fixed \(K_1\) box, does not apply to the long-delay
special-flow reduction.

The proved compact-tube history graph also does not imply Lemma T. Its
cutoff and contraction constants may depend on a fixed tube, while
\(S_\delta\to\infty\). The characteristic-root count at the fold does not
fill this gap: it does not supply a phase-space projector or a nonautonomous
Green operator along either outer slow branch.

There is also a simple logical counterexample to a frequently used shortcut.
Suppose only that a selected endpoint stays in a fixed \(K_1\) strip and is
smooth in \(\eta\) for every fixed \(\delta\). The bounded family

\[
 x_{1,\delta}(\eta)
 =x_{1,0}+a\sin(\eta e^{1/\delta^2})
\tag{21}
\]

has those properties, but
\(\partial_\eta x_{1,\delta}(0)=ae^{1/\delta^2}\). The Gaussian at the
logarithmic section is only algebraic in \(\delta\) and cannot suppress this
derivative. Thus fixed-\(\delta\) smoothness plus a bounded strip cannot be
used in place of (T2). Formula (21) is not asserted to arise from the final
RFDE; it disproves the claimed implication from the presently available
hypotheses.

## 7. The minimum remaining theorem

To close the long-delay route, one must prove Lemma T by a curve-wise
construction. The precise operator input can be stated as follows. On the
fixed scaled history space

\[
 \mathcal C=C([-\theta_1,0],\mathbb R^4),
 \qquad
 \|\phi\|_{\mathcal C}
 =\sup_{-\theta_1\leq\vartheta\leq0}|\phi(\vartheta)|,
\tag{22}
\]

let \(\mathcal L^{a/r}_\delta\) be the nonautonomous variational RFDE along
the fixed attracting or repelling outer selection, stopped when it reaches
(3). Remove the tangent direction by the phase \(X(0)=0\). The required
one-sided Green theorem is the existence of solution operators

\[
 \mathcal G^a_\delta:(f,b_a)\longmapsto\xi^a,
 \qquad
 \mathcal G^r_\delta:(f,b_r)\longmapsto\xi^r,
\tag{23}
\]

for the attracting forward boundary condition and the repelling
backward-extendible boundary condition, respectively, such that their
parameter-differentiated solutions satisfy (T1)--(T2). In particular, a
characteristic-root count is insufficient: (23) must include the
history-to-current-state evaluation, the one-sided boundary projections,
and the phase projection, with constants independent of \(\delta\) except
for the one fixed algebraic loss \(\delta^{-M}\).

The cutoff requirement is finite and explicit at coefficient level. Let

\[
 \Theta^{[d]}=
 \left\{\theta_{j_1}+\cdots+\theta_{j_k}:
 0\leq k\leq d,\ j_i\in\{0,1\}\right\}.
\tag{24}
\]

The formal coefficient \(q_1\) uses atom depth one. Differentiating one
delayed flow evaluation to obtain \(q_2\) uses atom depth at most two.
Therefore the cutoff must equal the physical vector field on the union of
the selected logarithmic tube and its \(q_0\)-flow backtracks by every
\(\vartheta\in\Theta^{[2]}\), with a fixed-width buffer. This condition
establishes cutoff independence of (12)--(13); it does not control the
actual graph remainder.

For the latter, truncate the stable Lyapunov--Perron integral at

\[
 R_\delta=L\log(1/\delta).
\tag{25}
\]

If \(\|e^{Ar}\|\leq M_Ae^{-\beta r}\), then

\[
 \delta\int_{R_\delta}^{\infty}\|e^{Ar}\|\,dr
 \leq\frac{M_A}{\beta}\delta^{1+\beta L}.
\tag{26}
\]

The polynomial factors in \(r\) created by the finite parameter derivatives
only add powers of \(\log(1/\delta)\) to (26) and do not change its selectable
algebraic order.

The retained convolution backtracks the reduced flow by only
\(\delta R_\delta=O(\delta\log(1/\delta))\). On this buffered growing tube
one must prove, pointwise in the phase coordinate,

\[
 \max_{0\leq j\leq2}
 \left|
  \partial_\eta^j
  \left(Q-q_0-\delta q_1-\delta^2q_2\right)
  (\gamma_0(s)+\zeta)
 \right|
 \leq C\delta^3\langle s\rangle^m e^{c|s|},
\tag{27}
\]

with the spatial and \(\nu\)-derivative bounds used in Theorem 2. Taking
\(L>2/\beta\) makes (26) smaller than \(\delta^3\). The pointwise weight in
(27), rather than the crude growing-tube supremum \(e^{cS_\delta}\), is what
preserves the exact \(O(\delta^3)\) gap error after Gaussian integration.

A sufficient proof package for (23) and (27) is:

1. a nonautonomous exponential dichotomy for the full scaled RFDE
   variational equation along each normally hyperbolic outer branch, on
   (22), with an anisotropic chart norm and constants tracked down to
   \(r_1=r_{1,\delta}\);
2. \(C^1_\nu C^2_\eta\) Lyapunov--Perron trace maps for the attracting
   forward selection and the repelling backward-extendible selection, with
   the phase-point loss bounded by a fixed power of \(\delta^{-1}\) times
   \(\operatorname{poly}(|s|)e^{c|s|}\), not by
   \(e^{c/\delta^2}\);
3. overlap of those trace maps with the growing-tube special-flow graph and
   proof that every retained delayed backtrack stays in the buffered uncut
   region described after (24);
4. the finite-depth coefficient calculation (24), stable-tail estimate
   (26), and mixed graph remainder (27).

No result currently proved in this repository supplies item 1 or 2. No cited
fixed-delay center-manifold or standard \(K_1\) theorem has the required
uniformity as the physical delay \(\theta_1/\delta\) diverges. Therefore the
smallest honest stop point is Lemma T, not the Gaussian pairing and not the
second \(\eta\)-derivative calculation.

## 8. Claim boundary

The defensible conclusion is:

- the logarithmic sections and Gaussian trace norm needed by the long-delay
  argument are explicit;
- under the single selected-trace lemma T and the growing mixed graph jet,
  all three normalized gap derivative estimates, including
  \(\partial_{\eta\eta}D=O(\delta^2)\), follow by Theorem 2;
- fixed-neighborhood \(K_1\) regularity fails, and fixed-\(\delta\)
  smoothness of an outer selection does not imply Lemma T;
- Lemma T is not proved for the final RFDE, so (18)--(19) remain conditional.

Numerical convergence of a prescribed-history finite-section root can test
the sign and scale in (13), but it does not establish Lemma T or any estimate
in (14).
