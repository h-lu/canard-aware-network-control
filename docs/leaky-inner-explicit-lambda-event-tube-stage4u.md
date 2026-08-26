# Stage 4U: an explicit scaled near-two-period event tube

Status: **PROVED EXPLICIT SCALED REDUCED-\(Y\) BALL EVENT TUBE.**

Stage 4U proves a deliberately small quantitative version of the qualitative
near-two-period event theorem.  Let \(M=E_s\times\mathbb R\), where the
directly bound Stage-4M splitting has
\(E_s=\ker\widehat f\subset\Sigma_0\),
\(\widehat q\in\Sigma_0\), \(\|\widehat q\|_Y=1\), and
\(\widehat f(\widehat q)=1\).  In these fixed unit-\(Y\) Route-C coordinates,
every reduced-history coordinate in

\[
 B_{\lambda_0}=\{\|x_s\|_Y\le0.0097\lambda_0,
 |x_u|\le0.00025\lambda_0\},
 \qquad \boxed{\lambda_0=9\times10^{-31}},
\]

including every arbitrary continuous reduced-\(Y\) stable vector
\(x_s\in E_s\) satisfying the norm bound, has one unique positive-oriented
event in one fixed physical-time window near \(2P\).  This does not quantify
over arbitrary two-component histories in the full space \(X\).  The event
time and complete reduced-history hit are \(C^2\) first on an ambient open
set \(W_{\rm open}\subset Y\), and then on its section-coordinate restriction
\(D_{\rm open}=j^{-1}(W_{\rm open}\cap\Sigma_{\rm loc})\).  The hit lies in
the declared local phase-zero section patch.  This is not a self-map of the
same scaled ball and carries no event-ordinal claim.

The executable source is
[leaky_inner_explicit_lambda_event_tube_stage4u.py](../src/canard_control/leaky_inner_explicit_lambda_event_tube_stage4u.py),
the atomic generator is
[leaky_inner_explicit_lambda_event_tube_stage4u.py](../experiments/leaky_inner_explicit_lambda_event_tube_stage4u.py),
and the registered result is
[leaky_inner_explicit_lambda_event_tube_stage4u.json](../experiments/results/leaky_inner_explicit_lambda_event_tube_stage4u.json).

## 1. Corrected scalar comparison

Let \(B=\sup_t|v_*(t)-1|\), so the corrected Stage-4N parent gives

\[
 B\le0.5300579564872213584478710086646587288,
 \qquad A_0\le1.775740624398391663912912818272403.
\]

For a bootstrap radius \(\beta\), the exact fast-field Hessian rows give

\[
 H_\beta
 =2(1+B+\beta)+12\varepsilon\kappa_3(B+\beta),
 \qquad
 L_\beta=\max\{A_0+H_\beta\beta,2\varepsilon\}.
\]

The leading \(1\) is essential: \(B\) bounds \(|v_*-1|\), not \(|v_*|\).
Stage 4U chooses \(\beta\) to be half of the certified center endpoint gap.
It runs the comparison through

\[
 T_+=2P_++10^{-3}
 =36.3734198982598419857014087027996907097797177739690113740347138,
\]

not merely through one period.  The resulting outward values satisfy

\[
 L_\beta<1.777,
 \qquad
 G_\beta=e^{L_\beta T_+}<1.137586\times10^{28}.
\]

Although this gain is enormous, scaling the initial radius makes the
bootstrap strict.  The ambient open proof neighborhood uses
\(\lambda_{\rm open}=9.1\times10^{-31}\), strictly larger than
\(\lambda_0\), and satisfies

\[
 0.00995\lambda_{\rm open}G_\beta<\beta.
\]

Here

\[
 W_{\rm open}
 =\{y\in Y:\|y-Y_*\|_Y<0.00995\lambda_{\rm open}\}.
\]

The coordinate domain is introduced only after the ambient theorem:
\(D_{\rm open}=j^{-1}(W_{\rm open}\cap\Sigma_{\rm loc})\).  The triangle
inequality places the explicit coordinate diamond, and hence the closed
\(B_{\lambda_0}\), inside this domain.

The directed ceiling for this half-margin construction is approximately
\(9.13306649\times10^{-31}\), so the disclosed open scale remains strictly
inside it.

## 2. Complete-history Gronwall inequality

For the difference \(\eta\) from the exact periodic solution, define

\[
 M(t)=\max\left\{
 \|\eta_v\|_{[-\tau_{\max},0]},|\eta_w(0)|,
 \sup_{0\le s\le t}\max(|\eta_v(s)|,|\eta_w(s)|)
 \right\}.
\]

Before a delayed argument activates, \(\eta_v(s-\tau_j)\) is the exact
translate of the arbitrary initial history and is bounded by the first term
in \(M\).  After activation it is bounded by \(M(s)\).  The corrected row
therefore gives one continuous inequality

\[
 M(t)\le \rho_{\rm open}+\int_0^tL_\beta M(s)\,ds,
 \qquad 0\le t\le T_+.
\]

This single supremum argument covers both delay-activation faces, all later
method-of-steps seams, and the translated complete-history output; it does
not sample time or replace a continuous history by nodes.  A first-exit
argument and Gronwall give \(M(t)<\beta\) throughout the interval.  The
reduced polynomial vector field is bounded on this tube, so the maximal
solution cannot end before \(T_+\).

## 3. Endpoint signs and speed

With \(h=10^{-3}\), the fixed window is

\[
 I=[2P_--h,2P_++h].
\]

The Stage-2 orbit-history speed bounds the exact center's displacement over
this window, while the Stage-2 positive voltage-event speed supplies the two
center signs.  The choice of \(\beta\) ensures that the full open flow family
retains at least half of each center endpoint gap:

\[
 \sup_{y\in W_{\rm open}}g_Y(\Psi_{T_-}y)<0,
 \qquad
 \inf_{y\in W_{\rm open}}g_Y(\Psi_{T_+}y)>0.
\]

For every \((t,y)\in I\times W_{\rm open}\), the complete reduced history is
strictly inside the Stage-2 radius-\(0.01\) ball.  Hence

\[
 \partial_tg_Y(\Psi_t y)
 \ge a_{\rm orb}^- -L_F^+\|\Psi_t y-Y_*\|_Y>0.24.
\]

Continuity gives an event for each history and strict positive speed makes it
the unique event in this fixed window.  This proves no first-, second-, or
other ordinal label.

## 4. Moving complete history and the local patch

At the moving event time \(T(y)\), compare with the exact orbit at the same
physical time before translating back to phase zero:

\[
 \|\Psi_{T(y)}y-Y_*\|_Y
 \le
 \|\Psi_{T(y)}y-\Psi_{T(y)}Y_*\|_Y
 +\|\Psi_{T(y)}Y_*-Y_*\|_Y.
\]

The first term is controlled by the complete-history Gronwall tube and the
second by the exact center-window displacement.  Their sum is strictly below
\(0.01\).  Since the selected-event equation also gives \(g_Y=0\), every hit
lies in

\[
 \Sigma_{\rm loc}=\{y:g_Y(y)=0,\ \|y-Y_*\|_Y<0.01\}.
\]

This estimate covers all physical times in
\([T_--\tau_{\max},T_+]\), not only the current event value.

## 5. Full/reduced bridge and regularity

The exact reduced-history theorem provides the compatible affine lift
\(\iota:Y\to X\), projection \(\pi:X\to Y\), and semiflow intertwining
\(\pi\Phi_t=\Psi_t\pi\).  The model functional
\(F:X\to\mathbb R^2\) is a finite-evaluation polynomial and therefore
globally \(C^\infty\); the affine event functional
\(g_X=g_Y\circ\pi\) is also globally \(C^\infty\).  Thus the Stage-4R
functional and event domains can both be taken to be \(X\).  Stage 4U proves
the quantitative tube in \(Y\); it does not assert that the same radius
bounds the full \(X\)-history norm.  The lift nevertheless transfers the
common solution domain to the full RFDE.

The strict smoothing margin

\[
 T_- -2\tau_{\max}>14
\]

allows Stage 4R to be applied in the full history space with parameterization
\(\iota:W_{\rm open}\to X\), then projected back to \(Y\).  This first gives

\[
 \widetilde T:W_{\rm open}\to\mathbb R,
 \qquad
 \widetilde R_Y(y)=\Psi_{\widetilde T(y)}y:W_{\rm open}\to Y
\]

of class \(C^2\).  Now set

\[
 j(x_s,x_u)=Y_*+x_s+\widehat qx_u,
 \qquad
 D_{\rm open}=j^{-1}(W_{\rm open}\cap\Sigma_{\rm loc}).
\]

The explicit diamond
\(\{\|x_s\|_Y+|x_u|<0.00995(9.1\times10^{-31})\}\) lies in
\(D_{\rm open}\), and the closed \(B_{\lambda_0}\) lies strictly inside that
diamond.  Hence \(T=\widetilde T\circ j\) and
\(R_Y=\widetilde R_Y\circ j\) are \(C^2\) on \(D_{\rm open}\).

For \(\chi(y)=(P_s(y-Y_*),\widehat f(y-Y_*))\), define the open output
domain \(D_{\rm out}=\chi(\Sigma_{\rm loc})\subset M\).  Then

\[
 P_{\rm sel}=\chi\circ\widetilde R_Y\circ j:
 D_{\rm open}\longrightarrow D_{\rm out}
\]

is the induced selected local-section return.  No inclusion
\(D_{\rm out}\subset D_{\rm open}\), hence no same-domain self-map, is
asserted.

## 6. Boundary

Stage 4U does not prove \(\lambda=1\), a self-map of the scaled ball, a full
\(X\)-norm tube with the same radius, a scaled ball of arbitrary full-\(X\)
two-component histories, an event ordinal or no-earlier-return cover,
\(Q=P^2\), any projected Hessian block, a stable graph, pulse-sheet crossing,
biological onset/control, routing, capture, safety radius, or a
general-network canard theorem.  The pending numerical continuous-history
normalization adapter is not promoted; the theorem is stated in the fixed
abstractly unit-\(Y\) splitting directly registered by Stage 4M and inherited
by Stage 4N.

## 7. Replay

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 \
  experiments/leaky_inner_explicit_lambda_event_tube_stage4u.py
```
