# Stage 4L contract: direct terminal stable-row certificate

Status: **THEOREM DESIGN / OPEN numerical certificate.**  This route is a
strictly smaller alternative to validating the complete two-parameter
intermediate stable flow in Stage 4J.  It is sufficient for the discrete
stable-power input of the Lyapunov--Perron return-map theorem, but it does
not validate the nonlinear return tube or exclude an earlier section hit.

## 1. The discrete lemma

Let

\[
 \Sigma_0=T_{X_*}\Sigma=\{h\in Y:h_v(0)=0\}
\]

be the linear tangent section.  Let
\(P^{\rm sel}\) denote the selected near-one-period phase-fixed section
map at the inner periodic orbit and put
\[
 A=DP^{\rm sel}(0)
   =\Pi_T\mathcal U(T,0)|_{\Sigma_0}.
\]
The word *selected* is mandatory until a nonlinear tube excludes an earlier
section hit.  This linear stage does not prove that \(P^{\rm sel}\) is the
first positive return.

Let \(q^\Sigma\) be the physical section eigencolumn, let \(f_0\) be the raw
Stage-4D functional, and register
\[
 \gamma=f_0(q^\Sigma)\ne0,\qquad q=q^\Sigma,\qquad
 f=f_0/\gamma .
\]
Suppose the exact physical right/left pair obeys

\[
 Aq=\mu_uq,\qquad fA=\mu_uf,\qquad f(q)=1,
 \qquad P_s=I-qf,\qquad E_s=\ker f\subset\Sigma_0.  \tag{1.1}
\]

Then

\[
 AP_s=P_sA=P_sAP_s,\qquad
 AP_s(\Sigma_0)\subset E_s,\qquad
 A_s=A|_{E_s}.                                      \tag{1.2}
\]

If one directed complete-history calculation proves

\[
 \|AP_s\|_{\mathcal L(\Sigma_0,Y)}
 \le \rho_{\rm term}
 \le \rho_s^{\rm LP}<1,                             \tag{1.3}
\]

then, by invariance and submultiplicativity,

\[
 \|A_s^n\|_{E_s\to Y}\le\rho_{\rm term}^{n}
 \qquad(n\ge0).                                     \tag{1.4}
\]

Here \(E_s\) carries the same inherited \(Y\) norm as the graph theorem.
Thus the matrix Lyapunov--Perron budget may use

\[
 K_s=1,\qquad \rho_s=\rho_s^{\rm LP}.               \tag{1.5}
\]

It may instead use \(\rho_s=\rho_{\rm term}\) after rerunning the exact
majorant with that rate.  Proving only \(\rho_{\rm term}<1\), without the
comparison in (1.3), does not justify retaining a smaller previously
registered Lyapunov--Perron rate.  No bound for
\(\mathcal U(t,s)P_s(s)\) at intermediate physical times is needed for
(1.4).  Such an intermediate-flow bound may still be needed by a separate
return-tube or no-earlier-hit proof, and (1.3) must not be promoted to
either of those conclusions.

## 2. Why the terminal calculation is lower dimensional

On the validated inner branch, the return period is longer than the maximal
delay, while the four-word support also requires

\[
 T>\tau_{\max},\qquad T>2\tau_0,\qquad
 T<\tau_0+\tau_1,\qquad T<3\tau_0.                 \tag{2.1}
\]

Consequently every time in the returned history
\(T+\theta\), \(-\tau_{\max}\le\theta\le0\), is positive, so the terminal
return has no unadvanced translation/identity block.  Its exact
method-of-steps representation contains only

\[
 \varnothing,\qquad(\tau_0),\qquad(\tau_1),
 \qquad(\tau_0,\tau_0).                              \tag{2.2}
\]

A Stage-4L certificate must verify (2.1) with directed true-period and delay
intervals, not merely copy the center-period comparisons in Stage 4H.  In
particular, if \(T\in[T_-,T_+]\), it must check

\[
 T_->\tau_{\max,+},\quad T_->2\tau_{0,+},\quad
 T_+<\tau_{0,-}+\tau_{1,-},\quad T_+<3\tau_{0,-}.   \tag{2.3}
\]

The output-phase cover must contain the true interval
\([T_--\tau_{\max,+},T_+]\).  The Stage-4I center grid must either be
extended to \(T_+\) or accompanied by a directed terminal-time shift
remainder.

Stage 4J needs a continuous \((s,t,\theta)\) enclosure because its
a-posteriori residual lemma controls all intermediate stable propagators.
For (1.3), the section start is fixed and only the returned-history phase
and the input-history variable remain.  The required continuous object is
therefore a terminal two-variable atom--density kernel.

This dimension reduction is legitimate only because the target is the
discrete operator norm (1.3).  It cannot be used to infer that the physical
trajectory stays in a prescribed tube between the two section events.

## 3. Common signed terminal row

Let \(\ell_0(y)=y_v(0)\), let
\(a_T=\ell_0(\dot X_T)=\dot v(T)>0\), and define the exact physical event
correction by

\[
 \Pi_Ty=y-\dot X_T\,\frac{\ell_0(y)}{a_T}.           \tag{3.1}
\]

The tangent, event speed, and raw returned row must be enclosed in one
correlated expression.  There is no moving \(\Pi_t\).
Let
\(R_\theta\) be either the voltage-history evaluation row at returned phase
\(\theta\) or the current-recovery output row.  The object whose norm is
certified is

\[
 \mathfrak m_\theta
   =R_\theta\Pi_T\mathcal U(T,0)P_s.                 \tag{3.2}
\]

Both rank-one operations in (3.2) must be formed before any absolute value:

\[
 \mathcal U(T,0)P_s
 =\mathcal U(T,0)
  -\mathcal U(T,0)q\,f,
\]

and \(\Pi_T\) subtracts the terminal tangent row with the same directed
event-speed denominator.  The Stage-3 physical column, the Stage-4D
atom--density functional, the Stage-4E normalization/correlation ledger,
and the physical terminal event row must remain in one expression.  Bounds
for the raw row and the two rank-one rows cannot be subtracted after their
norms have been taken.

The equality \(AP_s=P_sAP_s\) and the range inclusion in (1.2) must be
proved analytically from the exact eigen-relations.  A small numerical
value of \(f(AP_sh)\) is not a substitute.  Once this invariance is
source-bound, no additional numerical left projection is needed in (3.2).

On the Route-C tangent section, the input current-voltage atom annihilates
every admissible perturbation.  More precisely, for any row \(m\),

\[
 \|m|_{\Sigma_0}\|
   =\inf_{c\in\mathbb R}\|m-c\ell_0\|_{Y^*}.         \tag{3.3}
\]

Thus its current-voltage \(\delta_0\) atom may be removed exactly.  After
that quotient operation, write

\[
 \mathfrak m_\theta(h)
   =a_w(\theta)h_w(0)
    +\int_{-\tau_{\max}}^0h_v(\eta)\,
       d\nu_\theta(\eta).                            \tag{3.4}
\]

The induced row norm is bounded by

\[
 |a_w(\theta)|+\|\nu_\theta\|_{\rm TV}.             \tag{3.5}
\]

The output norm is the maximum of (3.5) over the complete returned voltage
history and the recovery output.  Therefore a source-bound certificate of

\[
 \max\left\{
  \sup_{\theta\in[-\tau_{\max},0]}
   \bigl(|a_w(\theta)|+\|\nu_\theta\|_{\rm TV}\bigr),
  |a_w^{\rm rec}|+\|\nu^{\rm rec}\|_{\rm TV}
 \right\}
 \le\rho_{\rm term}                                 \tag{3.6}
\]

proves (1.3).  A finite-node matrix norm, Gaussian quadrature, or a sampled
maximum in \(\theta\) does not prove (3.6).

## 4. Directed implementation route

Partition the returned phase at every delay-activation boundary and use
the 1042-cell delay-aligned physical grid already registered by Stage 4I.
On each exact output/input support rectangle:

1. insert the four exact words (2.2) symbolically;
2. substitute the Stage-4I Taylor--Bernstein enclosures for
   \(F,G,C_0,C_1,C_{00}\), including their coefficient tails and cell
   seams;
3. insert the Stage-3/4D/4E column, atom--density row, orbit and
   normalization uncertainties;
4. apply the input stable deflation and terminal event correction in the
   common row (3.2);
5. only then bound atoms and integrate the absolute density outward;
6. take the continuous output-phase supremum by Bernstein subdivision.

The Stage-4I primitive tubes are fixed-start raw method-of-steps
certificates and do not assume \(K_s\), \(\rho_{\rm term}\), or terminal
contraction.  Consequently their direct algebraic image in (3.2) gives a
noncircular route around the full Stage-4J \((s,t)\) residual problem.
No error term may use the unknown \(\rho_{\rm term}\), \(K_s\), or
\(\|AP_s\|\) in its own propagation.

The Stage-4I coarse induced-measure error is already a directed consequence
of its primitive tubes, but it is not by itself the center enclosure in
(3.6).  The common Taylor--Bernstein row must supply that center, and all
rank-one and event uncertainties must be added before the final comparison
with \(\rho_{\rm term}\).

The source-bound diagnostics give

\[
 \|P_sAP_s\|\approx0.00414,
 \qquad
 \text{coarse primitive induced-measure error}<0.00147. \tag{4.1}
\]

These are feasibility numbers only.  In particular, the sampled center
\(0.00414\) and the coarse primitive error \(0.00147\) may not simply be
added and promoted: the common continuous center row is still missing.
They leave almost two orders of
magnitude of slack even for a conservative target
\(\rho_{\rm term}=0.1\), and far more for the currently registered
\(0.9950249169\) rate.  The remaining issue is directed continuous
enclosure, not numerical contraction.

## 5. Acceptance gates

A Stage-4L result may set the phase-fixed stable-map and \(K_s=1\) flags to
true only if it contains all of the following:

- exact byte hashes and normal validation of Stages 3, 4D, 4E, 4H and 4I;
- the exact definitions of \(\Sigma_0,P^{\rm sel},A,\Pi_T,q,f,P_s,E_s\),
  the nonzero normalization \(\gamma\), and the analytic eigen/intertwining
  identities in (1.1)--(1.2);
- directed true-period inequalities (2.3), proof that the returned history
  lies after physical time zero, and proof of the exact four-word support
  (2.2);
- every returned-history phase and every input-history support cell;
- coverage through \(T_+\), including terminal-time shift error if the
  Stage-4I center grid is reused;
- the common double rank-one row (3.2), formed before norms;
- the current-recovery atom and continuous voltage-history density in the
  same \(Y\) max norm used by the graph theorem;
- exact quotient removal of the section-null current-voltage atom by (3.3);
- all Fourier tails, orbit/root/period errors, primitive residuals,
  activation seams, cell seams, normalization errors and event-time errors;
- outward absolute-density integration and a continuous output-phase
  supremum;
- a strict directed inequality
  \(\rho_{\rm term}\le\rho_s^{\rm LP}<1\), or a fresh majorant replay using
  \(\rho_{\rm term}\);
- exact schema, canonical digest, runtime equality, atomic generation, a
  fresh independent replay and hostile mutations.

Hostile tests must reject omission of any word or support rectangle,
separate norming of the rank-one pieces, a finite-node history row, sampled
phase maxima, current-voltage atoms treated as active on \(\Sigma_0\), a
changed \((q,f)\) normalization, omission of the terminal event correction,
use of the affine section in place of \(\Sigma_0\), promotion to a first
return, omission of output invariance, center-\(T\)-only coverage,
self-referential error propagation, or promotion of (1.3) to a nonlinear
return tube.

Even after these gates close, the following remain false: the six uniform
nonlinear Hessian blocks, split-ball containment, quantitative stable graph,
pulse/stable-sheet crossing, biological onset, two-sided routing and network
safety.  Stage 4L supplies only the discrete linear ingress \(K_s=1\).
