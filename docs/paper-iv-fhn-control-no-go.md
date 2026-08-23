# A two-scale no-go theorem for the declared FHN control coordinates

Status: **the finite-network mode decomposition, the transverse stability
theorem, the response-matrix inequalities, and their sharpness statement are
proved below.  Their application to the physical pulse margin is conditional
on the root jet and one-coordinate canard-layer hypotheses in Section 4.**
The canonical local root has the required formal leading direction, but the
physical reset boundary still requires Paper III's signed-exchange Gate R-S.
No periodic FHN branch, unique-extrema box, or physical separator is claimed
to have been numerically certified here.

The exact layer algebra, explicit small-gain constants, and high-precision
sharpness diagnostic are implemented in
`src/canard_control/fhn_control_no_go.py` and tested in
`tests/test_fhn_control_no_go.py`.  This note does not edit the frozen JNS
manuscript.

## 1. The negative alternative

For the synchronous two-delay FitzHugh--Nagumo model in
`two-module-reference.md`, retain the declared actuators and outputs

\[
 u=(\kappa _1,\kappa _3,s),
 \qquad
 \mathcal Q_\varepsilon(u)=(F_\varepsilon,R_{h,\varepsilon},S_\varepsilon),
 \tag{1.1}
\]

where \(R_h=(\max h_N-\min h_N)^2\) and \(S\) is the positive pulse-safety
margin.  The conclusion of this note is not that the \(3\times3\) response
matrix is singular for every fixed \(\varepsilon>0\).  It is sharper in the
singular limit and weaker pointwise:

1. in frozen physical units, the safety row alone makes every right inverse
   grow at least algebraically when its declared root jet holds;
2. in the sharp canard layer, cancellation between the amplitude and safety
   rows makes every right inverse grow at least as fast as the reciprocal
   layer width; this order is sharp over the stated hypotheses;
3. dividing safety by its natural leading scale \(\varepsilon^{3/2}\) removes
   the first obstruction but not the second; and
4. the fixed voltage and recovery scaffolds can nevertheless make every
   noncollective network mode exponentially stable.  The control
   ill-conditioning is therefore not a transverse synchronization
   instability.

Thus the appropriate Paper IV result for these coordinates is alternative
\(\mathrm{(B)}\), a conditioning no-go, rather than an unsupported positive box
certificate.

On complete synchrony, the frozen observable satisfies
\(h_N=(2/3)V+(1/3)V=V\).  Hence its squared range is exactly
\((\max V-\min V)^2\), for every pair of module sizes.  The no-go therefore
uses the declared experimental output rather than replacing it by a modal
amplitude.

## 2. Exact full-network transverse decomposition

Let \(B_0\) and \(B_1\) be the same-module and cross-module halves of the
rank-one averaging matrix in the reference model.  For a receiver in module
\(a\), \(B_0\) averages its own source module with total mass \(1/2\), while
\(B_1\) averages the other source module with total mass \(1/2\).  Put

\[
 \mathbf 1=(1,\ldots,1)^T,
 \qquad
 q=(\underbrace{1,\ldots,1}_{n_1},
       \underbrace{-1,\ldots,-1}_{n_2})^T.
 \tag{2.1}
\]

If \(W_a\) is the zero-sum subspace supported on module \(a\), direct
summation gives the measure-layer identities

\[
\begin{array}{c|cc}
 &B_0&B_1\\ \hline
 \mathbf 1&\frac12\mathbf1&\frac12\mathbf1\\[1mm]
 q&\frac12q&-\frac12q\\[1mm]
 W_1\oplus W_2&0&0.
\end{array}
\tag{2.2}
\]

Consequently

\[
 \mathbb R^N
 =\operatorname{span}\{\mathbf1\}
  \oplus\operatorname{span}\{q\}
  \oplus W_1\oplus W_2
 \tag{2.3}
\]

is an exact invariant decomposition of the variational RFDE along every
completely synchronous solution.  Its multiplicities are \(1,1,N-2\),
independently of how the two module sizes are split.

Let \((V(t),W(t))\) be any completely synchronous solution and define

\[
 c(t)=\kappa _1+3\kappa _3(V(t)-1)^2,
 \qquad
 c_j(t)=\kappa _1+3\kappa _3(V(t-\tau_j)-1)^2.
 \tag{2.4}
\]

The collective variational equation is the linearization of the scalar
two-delay RFDE and is not repeated here.  A module-difference perturbation
\((p,q_r)q\) satisfies

\[
\begin{aligned}
 \dot p={}&[1-V(t)^2-D-\varepsilon c(t)]p-q_r\\
 &+\frac\varepsilon2
   \{c_0(t)p(t-\tau_0)-c_1(t)p(t-\tau_1)\},\\
 \dot q_r={}&\varepsilon p-Eq_r.
\end{aligned}
\tag{2.5}
\]

Every within-module mode satisfies the delay-free equation

\[
 \dot p=[1-V(t)^2-D-\varepsilon c(t)]p-q_r,
 \qquad
 \dot q_r=\varepsilon p-Eq_r.
 \tag{2.6}
\]

Equations (2.5)--(2.6) follow by differentiating the physical node model and
then using (2.2); they are not a moment closure or a small-delay expansion.

## 3. A full-network transverse Floquet theorem

The long delays prevent one from inferring transverse stability merely from
the current-state Jacobian.  For the declared scaffold, however, a direct
small-gain estimate is available.

> **Theorem 3.1 (size-uniform transverse stability).**
> Suppose a completely synchronous solution satisfies
>
> \[
>  |V(t)-1|\le B_V
> \quad\hbox{for all }t,
> \tag{3.1}
> \]
>
> and put
>
> \[
>  C_*:=|\kappa _1|+3|\kappa _3|B_V^2,
>  \qquad \tau_*:=\max\{\tau_0,\tau_1\}.
> \tag{3.2}
> \]
>
> Choose \(\rho>1/E\), and define
>
> \[
> \begin{aligned}
>  \alpha_\perp&:=\min\left\{
>     D-1-\varepsilon(C_*+\rho),\ E-\rho^{-1}
>     \right\},\\
>  \beta_\perp&:=\varepsilon C_*.
> \end{aligned}
> \tag{3.3}
> \]
>
> If \(\alpha_\perp>\beta_\perp\), every module-difference and
> within-module variational solution decays exponentially, uniformly in
> \(n_1,n_2\).  More precisely, if \(\lambda_*>0\) is the unique root
>
> \[
>  \lambda_*=\alpha_\perp-\beta_\perp e^{\lambda_*\tau_*},
> \tag{3.4}
> \]
>
> then the transverse evolution family has an estimate
> \(\|U_\perp(t,s)\|\le C_he^{-\lambda_*(t-s)}\), where \(C_h\) depends on
> the equivalent history norm but not on the module sizes.  If the
> synchronous solution is \(T\)-periodic, the transverse monodromy satisfies
>
> \[
>  r(\mathcal M_\perp)\le e^{-\lambda_*T}<1.
> \tag{3.5}
> \]
>
> Hence full-network hyperbolicity reduces to hyperbolicity of the exact
> synchronous scalar RFDE; no additional transverse neutral multiplier is
> present under (3.3).

**Proof.**  For a solution of (2.5), set
\(Z(t)=|p(t)|+\rho|q_r(t)|\).  Since \(1-V^2\le1\) and
\(|c|,|c_j|\le C_*\), its upper right Dini derivative obeys

\[
\begin{aligned}
 D^+Z(t)
 \le{}&-[D-1-\varepsilon C_*-\rho\varepsilon]|p(t)|\\
 &-(\rho E-1)|q_r(t)|
 +\varepsilon C_*
   \sup_{t-\tau_*\le r\le t}|p(r)|\\
 \le{}&-\alpha_\perp Z(t)+\beta_\perp
   \sup_{t-\tau_*\le r\le t}Z(r).
\end{aligned}
\tag{3.6}
\]

The same inequality holds for (2.6), with a zero delayed term, and hence also
with the larger right side in (3.6).  Halanay's inequality and
\(\alpha_\perp>\beta_\perp\)
give (3.4) and exponential decay.  The decomposition (2.3) makes the
constants independent of its multiplicities.  More explicitly, use the
nodewise maximum norm: module averaging has norm one, subtraction of a
module average has norm at most two, and the collective/difference
projections therefore have bounds independent of \(n_1,n_2\).  Taking the
maximum of the scalar estimates over the within-module components preserves
(3.6).  Passing from the current-state estimate to the weighted sup-history
norm costs at most \(e^{\lambda_*\tau_*}\).  Thus \(C_h\) may be taken as
this factor times the uniform projection constant just described.  Applying
the evolution bound to powers of the period map and taking \(k\)-th roots in
the spectral-radius formula proves (3.5).  The final statement follows
because the collective and transverse history spaces form an exact invariant
direct sum.  \(\square\)

For the declared long-delay scaling
\(\tau_*=\Theta_*/\sqrt\varepsilon\), the certified rate is explicit:

\[
 \lambda_*
 =\alpha_\perp-\frac1{\tau_*}
   W\!\left(\beta_\perp\tau_*e^{\alpha_\perp\tau_*}\right),
 \tag{3.7}
\]

where \(W\) is the principal Lambert function.  If \(C_*>0\),
\(\alpha_\perp\) stays away from zero, and \(\varepsilon\) is small,
comparison in (3.4) gives

\[
 \frac1{\tau_*}\log\frac{\alpha_\perp}{2\beta_\perp}
 \le\lambda_*
 \le\frac1{\tau_*}\log\frac{\alpha_\perp}{\beta_\perp},
 \tag{3.8}
\]

once the lower comparison value is at most \(\alpha_\perp/2\).  Thus this
certificate has rate \(\Theta(\sqrt\varepsilon|\log\varepsilon|)\).
Equation (3.8) is a
rate for the sufficient estimate, not an assertion that an actual
transverse characteristic root has that asymptotic location.

## 4. The model-specific response hypotheses

The no-go theorem needs no computed frequency row.  It uses only two local
properties of the declared safety and amplitude coordinates.  They are
stated explicitly because the first is not yet transferred to the physical
reset separator and the second is a global canard-explosion assertion, not a
consequence of the local adjoint formulas.

**Root-jet hypothesis \(\mathrm{(H_S)}\).**  On a compact actuator box with
\(\kappa _1\ge\kappa_->0\), the chosen signed safety coordinate is \(C^1\) and

\[
 D_uS_\varepsilon
 =\varepsilon^{3/2}s_0(u)+e_{S,\varepsilon}(u),
 \qquad
 \|e_{S,\varepsilon}\|\le C_S\varepsilon^2,
 \tag{4.1}
\]

uniformly, where

\[
 s_0(u)=\frac18\bigl(M_1^{(2)}(u),0,\kappa _1\bigr),
 \qquad
 M_1^{(2)}=\frac{\Theta_0^0+\Theta_1^0}{2}+s.
 \tag{4.2}
\]

The sign in (4.2) is for \(S=a_{\rm op}-a_c\).  The zero cubic entry records
that the cubic actuator is centered at the fold; it does not set the full
\(\kappa _3\) derivative to zero.  The local calculation supplies (4.2), but
the physical interpretation of (4.1) still requires the Paper III reset
separator to cross simply and to be identified with the canard root.
Moreover, a pointwise \(O(\varepsilon^2)\) root expansion does not imply
(4.1): the hypothesis explicitly requires the differentiated remainder to
be uniform on the actuator box.

**One-coordinate layer hypothesis \(\mathrm{(H_A)}\).**  On a canard operating box,

\[
 R_{h,\varepsilon}(u)
 =\mathscr A_\varepsilon
   \!\left(\frac{S_\varepsilon(u)}{w_\varepsilon}\right)
  +\mathscr R_\varepsilon(u),
 \tag{4.3}
\]

where \(w_\varepsilon>0\), and throughout the box

\[
 |\mathscr A_\varepsilon'|\ge m_A>0,
 \qquad
 \|D_u\mathscr R_\varepsilon\|\le C_R.
 \tag{4.4}
\]

Here \(\mathscr R_\varepsilon\) contains every bounded shape effect,
including the effect of \(\kappa _3\) at fixed safety.  Hypothesis
\(\mathrm{(H_A)}\) is the precise statement that the observed squared range is in a
sharp one-coordinate canard layer.  A plot of a rapid amplitude jump does
not prove its uniform derivative bounds.

## 5. Two-scale conditioning obstruction

For a \(3\times3\) response matrix \(M\), write

\[
 \sigma_{\rm sur}(M)
 :=\inf_{|y|=1}|M^Ty|.
 \tag{5.1}
\]

This is its smallest singular value.  The notation also emphasizes that the
same proof works with more than three actuators.

> **Theorem 5.1 (declared FHN two-scale no-go).**
> Let a \(C^1\) periodic branch with unique nondegenerate extrema be given,
> so that \(F_\varepsilon\) and \(R_{h,\varepsilon}\) are defined.  Assume
> \(\mathrm{(H_S)}\).  Then there is a constant \(C_0\), uniform on the compact
> actuator box, such that
>
> \[
>  \sigma_{\rm sur}(D_u\mathcal Q_\varepsilon)
>  \le \|D_uS_\varepsilon\|
>  \le C_0\varepsilon^{3/2}.
> \tag{5.2}
> \]
>
> If \(\mathrm{(H_A)}\) also holds, then
>
> \[
> \boxed{
>  \sigma_{\rm sur}(D_u\mathcal Q_\varepsilon)
>  \le
>  \frac{C_Rw_\varepsilon}
>       {\sqrt{w_\varepsilon^2+m_A^2}}.}
> \tag{5.3}
> \]
>
> For the naturally scaled output
>
> \[
>  \widehat{\mathcal Q}_\varepsilon
>  =\left(F_\varepsilon,R_{h,\varepsilon},
>          \frac{S_\varepsilon}{\varepsilon^{3/2}}\right),
> \tag{5.4}
> \]
>
> the remaining obstruction is
>
> \[
> \boxed{
>  \sigma_{\rm sur}(D_u\widehat{\mathcal Q}_\varepsilon)
>  \le
>  \frac{C_Rw_\varepsilon}
>       {\sqrt{w_\varepsilon^2+m_A^2\varepsilon^3}}
>  \le\frac{C_R}{m_A}
>       \frac{w_\varepsilon}{\varepsilon^{3/2}}.}
> \tag{5.5}
> \]
>
> Hence no family of linear right inverses is uniformly bounded in physical
> coordinates.  Even after the natural scaling (5.4), if
> \(w_\varepsilon\le C_we^{-\Lambda/\varepsilon}\), every right inverse
> \(\mathcal R_\varepsilon\) satisfies
>
> \[
>  \|\mathcal R_\varepsilon\|
>  \ge\frac{m_A}{C_RC_w}
>       \varepsilon^{3/2}e^{\Lambda/\varepsilon}
> \tag{5.6}
> \]
>
> when \(C_R>0\).  If \(C_R=0\), the amplitude and safety rows are exactly
> dependent and the response rank is at most two.

**Proof.**  Taking \(y=(0,0,1)^T\) in (5.1) gives the first inequality in
(5.2); (4.1)--(4.2) and compactness give the second.  Differentiate (4.3):

\[
 D_uR_h=c_\varepsilon D_uS_\varepsilon+r_\varepsilon,
 \qquad
 c_\varepsilon=\frac{\mathscr A_\varepsilon'}{w_\varepsilon},
 \qquad
 \|r_\varepsilon\|\le C_R.
 \tag{5.7}
\]

If \(f,a,s\) denote the three response rows, take

\[
 y=\frac{(0,1,-c_\varepsilon)^T}
         {\sqrt{1+c_\varepsilon^2}}.
 \tag{5.8}
\]

Then \(y^TD_u\mathcal Q_\varepsilon
=r_\varepsilon/\sqrt{1+c_\varepsilon^2}\).  Equations (4.4) and (5.1)
give (5.3).  In (5.4), relation (5.7) becomes

\[
 a=(c_\varepsilon\varepsilon^{3/2})\widehat s+r_\varepsilon.
 \tag{5.9}
\]

The same cancelling vector proves (5.5).  The norm of every right inverse is
at least \(\sigma_{\rm sur}^{-1}\), which yields (5.6).  When \(C_R=0\),
(5.7) is an exact row dependence.  \(\square\)

The theorem is independent of the frequency row: its cancelling left vector
has zero frequency component.  It also identifies what would be required to
evade the result.  On the naturally scaled output, a shape response must grow
at least on the scale

\[
 \|D_u\mathscr R_\varepsilon\|
 \gtrsim\frac{\varepsilon^{3/2}}{w_\varepsilon}
 \tag{5.10}
\]

before a uniform lower bound is even possible.  A bounded \(\kappa _3\)
shape column cannot do this.  Thus centering \(\kappa _3\) to remove its
leading threshold translation is useful for pointwise rank, but it does not
by itself provide robust three-coordinate control in an exponentially thin
canard layer.

## 6. Sharpness and reproducible high-precision diagnostic

The powers of \(w_\varepsilon\) in (5.3) and (5.5) cannot be improved from
the stated hypotheses.  Since \(\kappa _1\ge\kappa_->0\), (4.2) gives
\(\|s_0\|\ge\kappa_-/8\).  Rotate actuator coordinates so that
\(s_0/\|s_0\|=e_3\), choose bounded shape and frequency rows \(r=e_1\) and
\(f=e_2\), and put

\[
 \kappa_\varepsilon=\varepsilon^{3/2}\|s_0\|,
 \qquad c_\varepsilon=\frac{m_A}{w_\varepsilon},
\tag{6.1}
\]

\[
 M_\varepsilon=
 \begin{pmatrix}
  0&1&0\\
  1&0&c_\varepsilon\kappa_\varepsilon\\
  0&0&\kappa_\varepsilon
 \end{pmatrix}.
 \tag{6.2}
\]

One singular value is \(1\).  The other squared singular values have product
\(\kappa_\varepsilon^2\) and sum

\[
 1+\kappa_\varepsilon^2(1+c_\varepsilon^2).
 \tag{6.3}
\]

When \(w_\varepsilon/\kappa_\varepsilon\to0\), rationalizing the smaller
root gives

\[
 \sigma_{\min}(M_\varepsilon)
 \sim\frac1{|c_\varepsilon|}
 =\frac{w_\varepsilon}{m_A}.
 \tag{6.4}
\]

After dividing the last row by \(\varepsilon^{3/2}\), the same calculation
gives

\[
 \sigma_{\min}(\widehat M_\varepsilon)
 \sim\frac1{|c_\varepsilon|\varepsilon^{3/2}}
 =\frac{w_\varepsilon}{m_A\varepsilon^{3/2}}.
 \tag{6.5}
\]

Thus both upper bounds are asymptotically attained by full-rank matrices.
This also demonstrates why a nonzero determinant does not answer the robust
control question.

The test suite evaluates (6.3) with 120-decimal arithmetic at an exponential
width and verifies that the ratios in (6.4)--(6.5) approach one.  It also
checks the exact identities (2.2) for unequal module sizes and evaluates the
Lambert-\(W\) rate (3.7).  These computations validate the algebra and the
sharpness example; they are deliberately not presented as an FHN orbit
computation.

For example, the tested synthetic family uses
\(\varepsilon=0.02\), \(w_\varepsilon=e^{-35}\), and
\(\|s_0\|=0.23\).  It gives

| rows | computed \(\sigma_{\min}\) | cancellation bound | ratio |
|---|---:|---:|---:|
| physical safety | \(6.3051167601469892\times10^{-16}\) | \(6.3051167601469892\times10^{-16}\) | \(1-5.0\times10^{-25}\) |
| safety divided by \(\varepsilon^{3/2}\) | \(2.2291954086364453\times10^{-13}\) | \(2.2291954086364453\times10^{-13}\) | \(1-5.0\times10^{-25}\) |

These numbers concern the exact matrix (6.2), not a discretized FHN orbit,
and are not an interval certificate for a periodic branch.

## 7. What is proved and what remains

| Statement | Status | Missing item, if any |
|---|---|---|
| Exact collective/difference/within decomposition | Proved | None |
| All noncollective modes stable under (3.3) | Proved | A bound \(B_V\) and parameter values are needed to instantiate it on a chosen branch |
| Polynomial and canard-layer response bounds | Proved under \(\mathrm{(H_S)}\) and \(\mathrm{(H_A)}\) | The inequalities themselves need no orbit discretization |
| Leading safety direction (4.2) for the physical pulse margin | Conditional | Paper III Gate R-S, simple crossing, and root identification |
| One-coordinate amplitude layer with exponential width | Conditional | A global canard-explosion theorem for the declared RFDE branch |
| Nonempty periodic branch and unique peak/trough box | Open | Validated periodic BVP and extrema enclosure |
| Positive \(3\times3\) inverse box inside the sharp layer | Ruled out under \(\mathrm{(H_S)}\)--\(\mathrm{(H_A)}\) in frozen or naturally scaled units | Only an exponentially growing shape response or a change of output/operating regime can evade the theorem |

The negative theorem therefore advances Paper IV without pretending that the
remaining Paper III separator or a periodic-orbit existence proof has already
been completed.  Once those two model hypotheses are closed, no new matrix
calculation is needed: Theorem 5.1 immediately transfers to the physical
frequency--amplitude--pulse map.
