# Proof-first outline for the finite-network and biological-control paper

Status: **active successor architecture, not a completed manuscript.**  The
existing two-module JNS manuscript remains a self-contained paper about a
canonical local complete-history connection.  This outline governs the
larger finite-network and biological-control paper.  A theorem is promoted
here only after its model-specific hypotheses have been verified in the
source-bound records.

## Working title

**Canard-Root Transfer and Physical Pulse-Threshold Control in Finite
Retarded Networks**

The title deliberately names two distinct codimension-one objects.  A
complete-history canard root is a parameter root of a Lin gap; a physical
pulse threshold is an intersection of a stimulus-history curve with a stable
manifold.  The paper may compare them, but it must not identify them without
a separate zero-set theorem.

## JNS positioning

The [Journal of Nonlinear Science scope](https://link.springer.com/journal/332/aims-and-scope)
asks that a paper both contribute to a technical area and illuminate
phenomena beyond a narrow specialty.  The
flagship manuscript should therefore be organized around the dynamical
mechanism, not around the inventory of interval certificates.  Its broad
question is how a codimension-one history-space boundary survives network
embedding and becomes a physically actuated pulse threshold.  The two
reusable mathematical steps are the dimension-independent transverse Green
inverse and the conversion of a stable-manifold crossing into a
frequency--amplitude--safety coordinate.

The center inner spectral count and the two-output response theorem are
substantial ingredients, but they do not by themselves supply that broader
conclusion.  Without Theorem C, the appropriate paper is a rigorous RFDE
spectral/response paper with a narrower title.  A JNS-facing title and
abstract may advertise biological pulse-threshold control only after the
stable-manifold crossing and both basin attachments are proved.  Local outer
capture may be proved directly by contraction of the exact phase-fixed
history return; a global outer Floquet zero count is not a prerequisite
unless the manuscript separately advertises that spectral conclusion.  The
introduction should remain readable beyond RFDE specialists, while the
Fourier-tail trees, hashes and hostile mutations belong in appendices or the
reproducibility supplement.

## Main question and result

The paper asks when collective slow--fast dynamics survive embedding into a
finite delayed network without acquiring uncontrolled transverse roots, and
whether the resulting physical pulse boundary can be used together with
frequency and amplitude as independent local control coordinates.

The common mechanism is a collective/quotient upper-triangular decomposition
for row-mass Dobrushin networks; common delay-layer left balance is not
required.  A dimension-independent transverse decay estimate is upgraded to
a complete-line Green inverse.  This gives two consequences:

1. a scalar simple complete-history canard root transfers to the canonical
   synchronized network Lin problem with the same index, root, slope and
   orientation;
2. scalar equilibrium, periodic-orbit and physical-pulse dynamics lift
   synchronously, while all network-transverse variational directions decay
   at an explicit rate.

The root-transfer conclusion has two mathematically distinct levels.  First,
canonical synchrony gives an exact upper-triangular Lin operator and a
bounded codomain conjugation to the scalar/transverse direct sum.  The
corrected full cokernel leaves collective parameter gaps unchanged whenever
the scalar complete-history problem exists.  Second, a
dimension-uniform structural theorem continues a selected simple root under
small network residuals, with an explicit admissible radius, a unique-root
interval, and a quadratic response remainder.  Its graph-first implication
is a proved conditional synthesis: joint gap regularity, a uniform simple
slope, and model-fitting bounds remain hypotheses to be checked in each
class.  The shared-resource heterogeneous-curvature class supplies a
nonempty, synchrony-quotient-free Dobrushin instance for a fixed-support
structural direction.  It does not supply an arbitrary neighborhood of
topology changes.

The collective/transverse mechanism is also the foundation for the
leaky-recovery pulse-onset theorem.  In that scalar leaky model, the center
inner Floquet count and the directed two-output periodic response are now
proved, while the scalar complete-history canard root remains open.  The full
biological result still depends on a parameter-coherent inner splitting and
quantitative stable graph, a directed pulse-family crossing, a local outer
return contraction, two-sided routing, and the safety gates listed below.  A
global outer zero-index theorem would strengthen the spectral picture but is
not logically required by this route.

## Headline theorem package

### Theorem A: complete-line transverse inverse

For every finite network satisfying

\[
 Q\ge0,\quad Q\mathbf1=\mathbf1,\quad
 \pi\ge0,\quad\pi^T\mathbf1=1,\quad\pi^TQ=\pi^T,\quad
 \tau(Q)\le\frac12,
 \qquad
 B_j\ge0,\quad B_j\mathbf1=\frac12\mathbf1,
\]

and for every complete synchronous leaky trajectory in the validated voltage
strip, the transverse history evolution satisfies

\[
 \|U_{\perp,N}(t,s)\|_{1/10}\le e^{-(t-s)/10},
 \qquad
 \|G_{\perp,N}\|\le10.                                  \tag{A}
\]

The constants do not depend on network size or on the admitted topology.
This theorem is proved.  It does not assert a dimension-uniform equivalence
with Euclidean norms or a topology-uniform nonlinear basin radius.

The same constants now give a genuinely nonlinear companion statement.  For
every real network solution whose retained node voltages remain in
\(|v_i-1|\le5/2\),

\[
 M(t)\le e^{-(t-t_0)/10}
 \sup_{t_0-r\le s\le t_0}M(s),
 \qquad M=\max\{\operatorname{osc}v,3\operatorname{osc}w\}. \tag{A2}
\]

This stripwise synchronization theorem is uniform in \(N\) and topology and
is proved without linearization.  Strip residence is a hypothesis: (A2)
does not yet provide a topology-uniform invariant neighborhood.

The collective component is also controlled structurally.  Set
\[
 \delta_j=\frac12\|\pi^TB_j-\tfrac12\pi^T\|_1,\qquad
 \delta_B=\delta_0+\delta_1.
\]
With \(\bar v=\pi^Tv\), \(\bar w=\pi^Tw\), its equation is the scalar leaky
RFDE plus a voltage forcing \(R_{\rm coll}\), and exact arithmetic gives
\[
\begin{aligned}
 |R_{\rm coll}(t)|\le{}&
 \frac{391}{20000}\{\delta_0M(t-\tau_0)+\delta_1M(t-\tau_1)\}\\
 &+\frac{1403}{400}M(t)^2
 +\frac3{800}\{M(t-\tau_0)^2+M(t-\tau_1)^2\}\\
 \le{}&\frac{391}{20000}\delta_B\mathcal H_M(t)
       +\frac{703}{200}\mathcal H_M(t)^2 ,
\end{aligned}
\]
where \(\mathcal H_M(t)=\sup_{t-r\le s\le t}M(s)\).  Forward integration
retains the full delayed-history residence:
\[
\begin{aligned}
 \int_{t_0}^{\infty}|R_{\rm coll}(t)|\,dt
 \le{}&\frac{391}{20000}
 \{\delta_0(10+4\sqrt5)+\delta_1(10+5\sqrt5)\}M_0\\
 &+\left(\frac{703}{40}+\frac{27\sqrt5}{800}\right)M_0^2\\
 \le{}&\frac{391(2+\sqrt5)}{4000}\delta_BM_0
       +\frac{56483}{3200}M_0^2.                     \tag{A3}
\end{aligned}
\]
The delayed values cannot be replaced by the current \(M(t)\).  At
\(\delta_B=0\), (A3) recovers the balanced purely quadratic bound with exact
coefficient \(703/40+27\sqrt5/800\).  All estimates are conditional on the
same strip residence as (A2) and uniform in finite \(N\) and admitted
topology; in particular, no positive lower bound on stationary weights is
used.  They are not a scalar shadowing tube or basin theorem.

For the balanced subclass \(\delta_B=0\), a source-bound composition lemma
gives the exact promotion interface.  It proves a first-strip-exit bootstrap,
a full-history-ball routing budget, and a monotone-gap threshold perturbation
theorem, all conditional on a separately validated scalar forced-routing
tube and a product-basin lift margin.  No concrete asynchronous radius is
inserted because those scalar and lift constants remain unavailable; the
precise formulas appear in (E3)--(E5).  The released nonbalanced theorem
supplies the forcing bound (A3), not a routing or safety radius.

### Theorem B: general finite-network root transfer

The theorem has an exact canonical layer and a structural-persistence layer.

**B0: exact canonical transfer.**  Assume a scalar phase-fixed Lin problem
has Fredholm index \(-1\), a normalized one-dimensional cokernel, a
complete-history gap \(d(\nu)\), and a simple root

\[
 d(\nu_c)=0,\qquad d'(\nu_c)\ne0.                       \tag{B1}
\]

For the canonical synchronized network realization, all endpoint, phase and
gap conditions act on the collective block and the transverse trace requires
bounded completeness.  Then

\[
 \mathcal L_N=
 \begin{pmatrix}\mathcal L_\parallel&C_N\\
                 0&\mathcal L_{\perp,N}\end{pmatrix},
 \qquad
 T_N\mathcal L_N=\mathcal L_\parallel\oplus
                         \mathcal L_{\perp,N},          \tag{B2}
\]

where
\[
 T_N(y_\parallel,y_\perp)
 =(y_\parallel-C_NG_{\perp,N}y_\perp,y_\perp),\qquad
 \|C_NG_{\perp,N}\|\le\frac{391}{2000}\delta_B.
\]
If \(\psi\) is the normalized scalar cokernel, the full functional is
\[
 \Psi_N(y_\parallel,y_\perp)
 =\psi(y_\parallel-C_NG_{\perp,N}y_\perp).
\]
It agrees with \(\psi\) on collective parameters, so
\(d_N(\nu)=d(\nu)\) and every admitted finite network has the same Fredholm
data and simple root.  The transverse hypothesis is proved by Theorem A.
The scalar leaky phase-fixed hypotheses (B1) and the declared collective
preparation remain hypotheses; no unconditional canard or onset follows.

**B1: uniform structural transfer.**  For a normalized selected gap
\(\widetilde d_N(\nu,\mathcal R)\), suppose the graph/trace or augmented-Lin
package, the model-fitting estimate, joint \(C^2\) gap regularity, and the
uniform bounds

\[
 |\partial_\nu\widetilde d_N(\nu_{0,N},0)|\ge m_*,\qquad
 \|D_{\mathcal R}\widetilde d_N(\nu_{0,N},\mathcal R)\|\le B_*,\qquad
 \|D^2\widetilde d_N\|\le M_*
 \tag{B3}
\]

hold on one common cylinder.  With range-solve radius \(\eta_*\), fitting
constant \(C_{\rm fit}\), and the common cylinder radii denoted by
\(r_\nu,r_{\mathcal R}\), set

\[
 \rho_* = \min\!\left\{
 r_{\mathcal R},\frac{m_*r_\nu}{2B_*},
 \frac{m_*}{2M_*(1+2B_*/m_*)},
 \frac{\eta_*}{C_{\rm fit}}
 \right\}.                                               \tag{B4}
\]

For every \(r=\|\mathcal R_N\|_{\rm net,N}\le\rho_*\), there is exactly
one selected root in

\[
 |\nu-\nu_{0,N}|\le \frac{2B_*}{m_*}r,
\]

and, writing \(a_N=\partial_\nu\widetilde d_N(\nu_{0,N},0)\) and
\(\ell_N=D_{\mathcal R}\widetilde d_N(\nu_{0,N},0)\),

\[
 \left|\nu_{c,N}(\mathcal R_N)-\nu_{0,N}
       +\frac{\ell_N[\mathcal R_N]}{a_N}\right|
 \le \frac{M_*}{2m_*}\left(1+\frac{2B_*}{m_*}\right)^2r^2. \tag{B5}
\]

All constants are independent of the admitted finite network size.  This is
a local selected-root theorem, not a global canard theorem; a geometric
canard additionally needs the zero-fiber implication, and physical pulse
onset additionally needs Theorem C.

**B2: proved nontrivial network instance.**  In the shared-resource,
heterogeneous-curvature model, finite directed row-stochastic matrices with a
common Dobrushin gap admit a fixed-support, full-row-neutral delayed
perturbation for which

\[
 \mu_{c,N}(\delta,\zeta)-\mu_{c,N}(\delta,0)
 =\mathscr C_N\delta^3\zeta
 +O(\delta^4|\zeta|+\delta^3\zeta^2),                    \tag{B6}
\]

with a uniform remainder and

\[
 \mathscr C_N=-\frac{K}{2\alpha^2}
 \pi_N^T\operatorname{diag}(c_N)A_N^{-1}P_{\perp,N}
 \dot M_{1,N}\mathbf1.
\]

Under its declared nondegeneracy, \(\inf_N|\mathscr C_N|>0\).  This is a
genuine general-topology instance because the family need not have a
nontrivial synchrony quotient.  Its proved scope is nevertheless fixed
delay support, a canonical prepared-tail selection, a common Dobrushin gap,
and the stated structural direction.  Differentiability under arbitrary
changes of the base topology, moving delay atoms, and closing-gap graph
families remains open.

### Theorem C: physical-pulse onset in the leaky RFDE

On a nonempty parameter box \(\Xi\), let the quiet equilibrium be attracting,
let the outer periodic orbit possess a quantitative local attraction tube,
and let the inner periodic orbit have precisely one nontranslation unstable
multiplier.  The outer tube may come from a direct phase-fixed return
contraction; no global multiplier count is built into the statement.  In the
exact reduced history space, construct the inner local stable manifold and
its signed defining function \(H(\xi,J)\) along the one-unit physical-pulse
curve.  Prove

\[
 H(\xi,J_-)>0>H(\xi,J_+),\qquad
 |\partial_JH(\xi,J)|\ge m_J>0.                         \tag{C1}
\]

After attaching the two local exit faces to an explicit quiet basin and an
outer periodic attraction tube, there is a unique \(C^1\) threshold
\(J_c(\xi)\) with

\[
\begin{cases}
 J<J_c(\xi)&\Longrightarrow E_q,\\
 J=J_c(\xi)&\Longrightarrow \Gamma_i,\\
 J>J_c(\xi)&\Longrightarrow \Gamma_o.
\end{cases}                                             \tag{C2}
\]

The exact reduced-history factorization, pulse embedding, large quiet basin,
and \(J=0.30\) quiet capture are proved.  Binary64 third-return diagnostics
locate a nondegenerate candidate near \(0.301135337086902\); they do not prove
a stable-sheet crossing.  The adaptive directed target is the wider interval
\([0.30105,0.30120]\), whose diagnostic endpoint gap has substantially more
room than the narrow bracket.  A directed family audit now proves that the
naive zero-centered enclosure cannot exploit that room.  The full-width tube
closes only \(730\) of \(1152\) method-of-steps cells.  One member of an exact
30,000-shard partition closes all cells with weighted state radius below
\(9.678\times10^{-3}\), but conversion to the reduced-history norm gives
\(1.0739434\times10^{-2}>10^{-2}\), and the other 29,999 shards have not been
replayed.  More decisively, its first and second zero-centered parameter
majorants reach \(3.844\times10^6\) and \(2.546\times10^{13}\); their
zero-width limits remain \(3.817\times10^6\) and \(2.510\times10^{13}\).
This is a rigorous rejection of full-history symmetric sharding as the
crossing proof, not a rejection of the pulse family.  The replacement is a
cellwise parameter Taylor model through order four, with only the fifth-order
remainder enclosed symmetrically, an implicit return-time jet, pullback of
the complete history to a common event graph, and a scalar stable-gap sign
and monotonicity argument; interval Newton may optionally sharpen the root
after existence and uniqueness are proved.  Stage 5B now closes the fixed-common-time part of
that replacement rigorously.  A \(192\)-bit Taylor--Bernstein enclosure
propagates the scaled coefficients
\(b_k=h^k\partial_J^kz/k!\), \(0\le k\le4\), jointly over all \(1152\)
time cells and the full interval \(J\in[0.30105,0.30120]\).  With time
degree \(16\), the maximum joint coefficient error is
\(8.57254\times10^{-19}\); the exact cubic degree-five through
degree-twelve tail forcing is at most \(2.05948\times10^{-9}\); and the
full-width fifth-order remainder tube closes with
\(\|R_5\|_P\le1.72064\times10^{-8}\).  An independent full recomputation
reproduces the frozen certificate.  Thus correlation is no longer merely a
binary64 explanation of the wrapping failure: the fixed-time wide parameter
family is proved.  Stage 5C then source-binds the corrected exact inner-orbit
section level and proves, over the same full interval, exactly one positive
Route-C event in the common bracket
\([555\sqrt5/24,1+546\sqrt5/24]\).  Its speed is at least
\(0.2133519018\), its fourth-order event-time graph has uniform remainder
\(10^{-4}\), and its common-event reduced-history tube has radius at most
\(0.008199932\).  Independent replay reproduces the certificate and a
hostile test rejects the obsolete Fourier candidate level.  No ordinal
``third crossing,'' stable coordinate sign, selected crossing, onset, or
routing is promoted, and no optional Newton enclosure is supplied.  Stage 5D
separately differentiates the exact
first-variation equation on all \(1152\) cells rather than differentiating
the Stage-5B remainder estimate.  It proves
\(T_J\in[336.624302835,456.574093812]\), retains the event-translation term,
and encloses the continuous complete-history derivative by
\(\|D_JK\|_Y\le142.200203\).  Stage 5E fixes the physical real right gauge
and proves on the full pulse interval that
\[
 f_{\rm phys}(D_JK)\in[-258.746521015805,-245.253478984195].
\]
Stage 5F then uses the identical continuous-history max norm \(Y\), Route-C
section \(\Sigma\), physically oriented Grushin pair, and centered coordinate
\(\kappa=K-X_*\).  It proves
\(\|P_sD_J\kappa\|_Y\le14.727579\) and the conditional implication
\[
 \sup\|D\psi\|\le16
 \quad\Longrightarrow\quad
 H'(J)\in[-494.387771,-9.612229]\subset(-\infty,0),
\]
provided the quantitative centered graph exists in that registered chart
and the chart/domain contain \(\kappa(I_J)\) and \(P_s\kappa(I_J)\).
These are the frozen Stage-5F parent bounds, retained for audit history but
sharpened by Stages 5G-a and 5G-b.  Stage 5G-a proves, in the same centered
chart and complete-history row,
\[
 f_{\rm phys}(\kappa(J_-))\in[0.019677187,0.023055896],\qquad
 f_{\rm phys}(\kappa(J_+))\in[-0.018164491,-0.014783669],
\]
together with endpoint stable-coordinate norms at most \(0.008935972\) and
\(0.008927665\).  The direct physical-column norm and the exact projection
identity in Stage 5G-b then prove
\[
 \|P_sD_J\kappa\|_Y\le5.979324,
 \qquad
 P_s\kappa(I_J)\subset
 \overline B_Y(0,47/5000)\cap\ker f_{\rm phys}.
\]
Thus no separate ambient-chart containment estimate is needed: a future
stable graph need only have a stable domain containing this certified ball.
If that graph also has \(\sup\|D\psi\|\le16\), the sharpened conditional
implication is
\[
 H'(J)\in[-354.415700,-149.584300]\subset(-\infty,0).
\]
The endpoint functional signs, the full-interval stable-coordinate cone, and
this conditional arithmetic are proved.  The quantitative graph, its domain,
derivative and endpoint-height bounds, graph-adjusted stable-gap signs,
selected crossing, the event's ordinal, physical onset, routing, capture, and
network safety remain open.  Interval Newton is only an optional later
sharpening of a root already proved by graph-adjusted stable-gap endpoint
signs and strict monotonicity.
At the center
parameter, a complete closed-right-half-plane count now gives exactly two
characteristic values with algebraic multiplicity: the simple translation
value \(s=0\) and exactly one simple positive nontranslation value; the
complementary keyhole count is zero.  Thus the center inner orbit has exactly
one unstable multiplier.  Classical RFDE periodic-orbit theory and the exact
reduced-history factorization now give a qualitative \(C^1\), codimension-one
local stable manifold in the full history space and a corresponding reduced
stable sheet.  Two completed source-bound left-strip covers now prove the
stronger quantitative center bound
\(\rho_s\le e^{-0.01}=0.9900498337\ldots<1\) for every remaining stable
multiplier.  The subsequent Route-C projection audit proves a strict
stable/unstable separation but also gives \(\|P_s\|\ge2\).  With the old
scalar remainder constant \(C_N=10\), the selected Lyapunov--Perron row has
left side at least \(4606.52>2500\); the earlier all-constants-one feasibility
row is therefore rejected, not retained as evidence.  The replacement works
directly in split coordinates.  It has identified all six independent
stable/unstable-output, \(ss/su/uu\)-input return-Hessian blocks and registered
an exact positive \(2\times2\) Perron/self-map evaluator.  A numerical theorem
still requires a direct stable power constant, a validated split return ball,
and upper bounds for those six blocks.
A source-bound three-mesh long-double pilot preserves this block structure.
Its refinement envelope gives a \(2\times2\) Perron value below \(0.04913\),
positive self-map slack in both components, and graph height about
\(8.25\times10^{-6}\).  The smallest single-block inflation threshold is
about \(1.751\) for the stable-output/\(uu\)-input block; the numerically
largest unstable-output/\(uu\)-input block may be inflated by more than a
factor of forty before the pilot gate fails.  This is a proof-design and
prioritization result, not RFDE evidence: the finite tensors are not
outward-rounded and have no continuous-history discretization enclosure.
Stage 4C closes the qualitative correlated-deflation mechanism.  For the
simple nonneutral unstable multiplier, every nonzero left eigenfunctional
has \(f(q)\ne0\); its RFDE action is a current-state atom plus delayed-history
density, it annihilates the neutral tangent, and the Route-C section
projection preserves its action.  Stage 4D now closes the
infinite-dimensional bridge left there.  It proves the bilinear Fourier
reversal \(\widehat r_n=E_{-,-n}\) with no conjugation, an adjoint-tail
contraction below \(0.104434\), full tail Wiener norm below \(0.011506\),
and the border normalization
\[
 3.05331\times10^{-4}<|f(q)|<5.46928\times10^{-4}.
\]
It reconstructs the continuous Route-C history measure and validates a
nonzero recovery-history action.  Stage 4E then propagates the physical-time
second variation on 1042 delay-aligned cells, applies the same continuous
atom-plus-density row to the directly deflated history, and proves
\[
 \|Y_{qq}-q^\Sigma f(Y_{qq})/f(q^\Sigma)\|_Y
 \le0.04754988548,\qquad
 C^{uu}_{s,\mathrm{base}}\le7.905649079<12.
\]
The total correlated action error is at most \(1.50030\times10^{-6}\);
the certificate explicitly includes guide/model/recovery residuals, all
cell seams, the approximate-adjoint identity defect, the history-density
product variation, and normalization.  This is a rigorous base-orbit block,
not a uniform radius-\(0.0017\) split-ball bound.  The other five blocks,
stable power, split-return tube and six-block quantitative graph remain
open.  Stage 4G computes the exact sufficient inflation threshold
\[
 L_{uu}<2408.4417186722
\]
but rigorously rejects a positive scalar \(P\)-logarithmic-norm route: it
first leaves the radius-\(0.01\) local section ball at cell \(581\), with
voltage radius \(0.010059402\), and reaches a period-end voltage bound above
\(2.15\).  This is a no-go theorem for that majorant, not for uniform
inflation.  Since
\(2\tau_0<T<\tau_0+\tau_1<3\tau_0\), the replacement signed ingress has only
the four words \(\varnothing,(\tau_0),(\tau_1),(\tau_0,\tau_0)\) and must
form \(U(t)P_s\) before total variation.
An independent Stage-2 replay does validate an explicit phase-zero voltage
history section: the orbit crosses with speed at least
\(0.2469269660\ldots\), the speed remains at least
\(0.2067539137\ldots\) on its radius-\(0.01\) section ball, and the old
binary64 voltage level has a unique nearby true-orbit crossing.  This is an
orbit-section admissibility theorem only; it is not a crossing of the
physical pulse curve with the stable sheet.
The history-space routing contract now adds two rigorous anchors.  On the
outer-orbit history tube of radius \(0.01\), the vector-field remainder and
second derivative satisfy
\[
 \|R_F(\eta)\|\le3.50816330348\,\|\eta\|_X^2,
 \qquad \|D^2F\|\le7.02973994029.
\]
The strict \(J=0.30\) quiet capture and continuous dependence also give a
nonexplicit open quiet pulse interval around \(0.30\).  At the other end, a
2064-cell directed method-of-steps calculation for the exact quiet history
and physical pulse \(J=0.32\) isolates the third positive declared-section
event in
\[
 [94.9619021653635192071,\,94.9619021653635201635].
\]
A 241-cell continuous-history Bernstein comparison, including the validated
outer orbit and period correction, proves reduced and complete ambient
history distance at most
\(2.637078616900037\times10^{-5}\) from the exact phase-zero outer-orbit
history.  This lies strictly inside the ambient radius-\(10^{-4}\) ball with
margin \(7.362921383099962\times10^{-5}\).  It is not a same-section or basin
statement: a Poincar\'e theorem must separately validate a nonlinear phase
chart with \(Q_{\rm phase}d_X<r_{\rm section}\), followed by a return
self-map and derivative contraction.  The same routing contract
proves the sufficient outer contraction inequality
\(K_o\rho_o^m+C_mr_o<1\), the exact signed factorization
\(\delta_+=a(\delta,z)\delta\), and the two complete-history attachment
budgets, while leaving all their missing numerical inputs null.
The result has not been continued over
\(\Xi\), and it supplies no explicit graph radius, particular pulse-section
crossing, or onset theorem.  The outer zero-unstable count, both parameter-box
index statements, quantitative stable graph, directed crossing, outer tube, and
two-sided routing remain open.  A directed full bordered Grushin inverse now
closes on the local disk, but its scalar Rouch\'e comparison does not: the
Neumann bottom-row back-substitution accounts for more than \(99.5\%\) of the
deficit.  An exact rational staircase removes the circular ownership seam but
still has a nonempty complement frontier at the 5000-cell calibration budget.
For the biological-capture
theorem the next proof object is therefore the phase-fixed complete-history
return operator itself.  Binary64 finite sections give
\(\rho\approx0.02195\), \(\|P\|_\infty\approx0.127\), and
\(\|P^2\|_\infty\approx0.00278\).  A subsequent source-bound Stage-2 audit
now performs the phase subtraction cell by cell with 160-bit outward
arithmetic on the exact stored 360-step binary matrix.  On physical output
rows it proves the discrete signed-measure shadow bounds
\[
 Q_{v,h}\le0.126907894814399,
 \qquad Q_{w,h}\le0.002760007256130,
\]
whereas estimating the fixed-time and phase terms separately would give a
triangle bound above \(5.169\).  The signed cancellation factor exceeds
\(40.73\), leaving discrete linear margin at least \(0.873092105185601\).
This is rigorous for the stored finite shadow, not yet for arbitrary
continuous histories.  The continuous RFDE operator has a current-value
Dirac atom, an absolutely continuous history density, and a recovery scalar
column; the section kills the Dirac atom exactly.  Interval
Taylor--Volterra propagation of the signed density and the exact-orbit and
period transfer errors \(E_v,E_w\) remain open.  The continuous linear gate
is
\[
 \max\{Q_{v,h}+E_v,Q_{w,h}+E_w\}<1.
\]
The first continuous-kernel shard is now proved: for
\(\theta\in[-10^{-3},0]\), both delay-injection branches have directed
resolvent, interval-Picard endpoint, and absolutely continuous density boxes
over their first \(10^{-3}\) elapsed-time cell, including the
\(10^{-8}\) exact-orbit and period uncertainty.  This is a composable
Volterra base cell, not a global transfer bound.  Stage 3B then crosses the
first nonzero delayed-forcing boundary for both branches and proves that a
direct positive global tiling would require roughly \(1.05\times10^6\)
coarse tasks; its local masses cannot be used as \(E_v,E_w\).

Stage 3C supplies the replacement representation.  Exact support and
\(3\tau_0-T>0.2283989174\) make every delay word of length at least three
zero.  The complete global kernel is therefore the signed sum of \(14\)
history-word and \(7\) recovery-scalar integrals, all of ordered dimension
at most two, for a representation compression factor greater than
\(49\,914\).  Stage 3D reduces all ordered two-simplex terms exactly to the
eight one-dimensional primitives \(F,G,H_0,H_1,L_{00},L_{01},L_{10},L_{11}\).
Stage 3E then proves a global degree-24, 1024-cell relative-residual
certificate on the exact orbit/period ball:
\[
 \eta\le0.005026008,\quad
 \|\widehat F^{-1}F-I\|_\infty\le0.005038659,\quad
 \|G\widehat F-I\|_\infty\le0.005064176.
\]
Separate absolute propagation gives unusable \(H,L\) errors \(190.1\) and
\(7.17\times10^6\), so those are explicitly not used as transfer errors.
Stage 3F now places every word, both injections and phase subtraction in one
advanced row before total variation.  It proves the exact combined-row
identity, instantaneous Green and boundary bounds \(14977.452934\) and
\(66623.270373\), the positive delayed allowances under the declared full
targets, full coefficient variation at most \(1.633190\times10^{-6}\), and
the phase-ratio transfer errors.  Its delayed Green/tensor residual remains
open.  Hence \(E_v,E_w\) are still null even though the independent phase
transfer \(E_{\rm phase}\le0.737275\) is proved.  After \(E_v,E_w\) close, a
continuous phase-chart bound, nonlinear second-variation bound, return
self-map radius, and the pulse-to-section attachment are still required for
an attracting tube.

### Theorem D: frequency--amplitude--safety controllability

Let \(F(\xi)\) be the autonomous outer-orbit frequency, \(A(\xi)\) its
unsquared peak-to-peak voltage amplitude, and

\[
 S(\xi,J)=J-J_c(\xi),\qquad
 \mathcal Q(a,\kappa_3,J)=(F,A,S).                     \tag{D1}
\]

Then

\[
 D\mathcal Q=
 \begin{pmatrix}
  D_\xi(F,A)&0\\
  -D_\xi J_c&1
 \end{pmatrix},
 \qquad
 \det D\mathcal Q=\det D_\xi(F,A).                    \tag{D2}
\]

The directed D4 certificate has status **ACCEPT** on the common orbit/extrema box.  Its
branchwise determinant enclosures have opposite fixed signs,

\[
 \det D_\xi(F,A)_{\rm in}
 \in[-0.229823,-0.228398],
 \qquad
 \det D_\xi(F,A)_{\rm out}
 \in[0.533847,1.694625].                               \tag{D3}
\]

For the outer branch used in \(\mathcal Q\), the parameter inverse is
Lipschitz with certified constant
\(22.044336699647400986\ldots<22.044336699647401\), and the directed
branch-centered \((F,A)\) target-ball radius is at least
\(4.5363124943378087\times10^{-12}\).  The smaller certified lower bound
\(4.0971263701603406\times10^{-13}\) is only the common minimum for tuning
the two distinct branch-centered responses at one shared radius; it is not
the flagship outer radius and the two balls are not concentric.

These D4 conclusions do not define \(J_c\).  The three-output
\((F,A,S)\) inverse and its quantitative target ball remain conditional on
Theorem C and bounds for \(D_\xi J_c\); no separator, physical onset, safety
threshold, outer capture, or pulse-routing conclusion follows from (D3).

### Corollary E: finite-network pulse control

For exactly synchronous stimuli and histories, Theorems C--D lift without
changing \(J_c,F,A\), because the synchronous restriction is the scalar
leaky RFDE.  Theorem A excludes additional transverse linear instability.
More precisely, the monodromy operator along the synchronized inner orbit
has the exact collective/quotient upper-triangular form

\[
 M_{i,N}=
 \begin{pmatrix}M_{i,\parallel}&*\\0&M_{i,\perp,N}\end{pmatrix},
 \qquad r(M_{i,\perp,N})<e^{-T_i/10}<1.                \tag{E1}
\]

The spectrum is the union of the diagonal-block spectra.  Conditional on
Theorem C, its only nontranslation unstable multiplier is therefore the
scalar one.  For every fixed admitted finite topology the
network inner orbit has a \(C^1\), codimension-one local stable manifold.
Local uniqueness and invariance imply that its intersection with the exact
synchrony subspace is the embedded scalar stable manifold.  Consequently
the synchronous pulse curve crosses at exactly the same \(J_c\) and with the
same orientation.

This statement also has a genuinely asynchronous, but initially
topology-by-topology, consequence.  If

\[
 (\eta,J)\longmapsto K_N(\eta,J)
\]

is any declared \(C^1\) local chart of perturbed network pulse histories,
with \(K_N(0,J)\) synchronous, the same nonzero \(J\)-derivative and the
Banach-space implicit-function theorem give a unique local threshold sheet

\[
 J=J_{c,N}(\eta),\qquad J_{c,N}(0)=J_c.                \tag{E2}
\]

Thus a scalar physical threshold, once proved, is not destroyed by adding
finitely many admitted transverse network directions.  Equation (E2) is
conditional on Theorem C and is not yet assigned a topology-uniform radius
or derivative bound.

For asynchronous histories, the proved nonlinear estimate (A2) contracts
node diameter whenever the trajectory remains in the voltage strip, and
(A3) makes the resulting collective forcing integrable.  It is quadratic in
the balanced subclass and contains the resolved linear imbalance otherwise.
A source-bound scalar routing tube could therefore turn the local sheet
(E2) into a network-uniform asynchronous capture theorem, but the released
composition certificate currently treats \(\delta_B=0\).  The
strip-invariant routing tube and the radius of any threshold neighborhood
are not proved.

The quantitative composition theorem is now source-bound.  Suppose a scalar
forced routing tube accepts every mean-history/forcing pair satisfying

\[
 L_0\delta_{\rm mean}
 +\int_{t_0}^{\infty}|r(t)|\,dt<\eta_{\rm route}
\]

and keeps its mean voltage at distance at least \(d_{\rm strip}>0\) from the
boundary \(|v-1|=5/2\).  A full-network basin conclusion additionally needs
a product-lift theorem with margin \(d_{\rm lift}>0\); a scalar basin alone
does not supply it.  Put

\[
 R_0=\max\{\delta_{\rm mean},M_0\}.
\]

Then the first-exit bootstrap and product lift close for every admitted
finite network in the balanced subclass under the strict budget

\[
 R_0<\min\{d_{\rm strip},d_{\rm lift}\},
 \qquad
 L_0R_0+\frac{56483}{3200}R_0^2<\eta_{\rm route}.      \tag{E3}
\]

For exact mean entrance this reduces to

\[
 M_0^2<\min\left\{d_{\rm strip}^2,d_{\rm lift}^2,
                    \frac{3200\eta_{\rm route}}{56483}\right\}. \tag{E4}
\]

If the oriented scalar gap has \(-H'(J)\ge m_J>0\) on a half-width \(r_J\)
and the
network perturbation satisfies

\[
 \|\widetilde H-H\|_\infty\le\epsilon_H(R_0)<m_Jr_J,
 \qquad
 \|\widetilde H'-H'\|_\infty<m_J,
\]

then it has exactly one perturbed root in
\([J_c-r_J,J_c+r_J]\), with no assertion about roots outside, and

\[
 |J_{c,N}-J_c|\le\frac{\epsilon_H(R_0)}{m_J};
 \qquad J\in[J_c-r_J,J_c+r_J],\quad
 |J-J_c|>\frac{\epsilon_H(R_0)}{m_J}
 \quad\Longrightarrow\quad\hbox{same signed side}.     \tag{E5}
\]

Here \(\epsilon_H=L_{H0}R_0+L_{H1}(56483/3200)R_0^2\), with an analogous
formula for the derivative error.  Equations (E3)--(E5) are proved
implications, not numerical leaky-model conclusions: every scalar route,
lift, slope and response constant in them is still open.

## Shortest dependency chain

~~~text
validated scalar orbits on a common box
       |                         |
inner center count [proved]  directed D(F,A) [proved]
       |                         |
parameter-coherent split         |
       |                         |
six-block stable graph           |
       |                         |
directed pulse-family crossing   |
       |                         |
unique J_c and D J_c ------------+
       |                         |
two local exit faces       outer signed-kernel return contraction
       |                         |
quiet/outer capture --------------+
                 |
       quantitative (F,A,S) inverse
                 |
      synchronous finite-network lift

row-mass Dobrushin identities
                 |
complete-line transverse inverse
       /                         \
scalar Lin gap/root          transverse pulse stability
       |                         |
general network root transfer ---+
~~~

The two branches meet in the network theorem, not by asserting that the
scalar Lin root and the pulse threshold are the same scalar quantity.

## Paper organization

1. **Introduction.**  State the two codimension-one objects, the shared
   transverse obstruction, and the two headline consequences.  Position the
   result against delayed canards, RFDE phase--amplitude reduction, pulse
   thresholds, and network synchronization.
2. **Row-mass retarded networks.**  Define the scalar leaky RFDE, the finite
   network class, the collective/quotient upper-triangular decomposition,
   its balanced direct-sum special case, and the declared history norms.
3. **Complete-line transverse dynamics.**  Prove Theorem A by the weighted
   Dobrushin--Halanay estimate and forward pullback.  Keep all topology and
   norm quantifiers visible.
4. **Canard-root transfer.**  State the scalar Lin problem, prove Theorem B,
   and give the proved shared-resource nontrivial root instance.  Put the
   broad structural-perturbation theorem and quadratic remainder after the
   exact synchronized transfer.
5. **Validated scalar invariant objects.**  Introduce the quiet equilibrium,
   inner and outer periodic branches, common parameter box, extrema, and
   Floquet count.  Move Fourier/tail bookkeeping to an appendix, retaining
   the Riesz/Schur mechanism in the main text.
6. **The physical pulse separator.**  Use the reduced history space,
   Lyapunov--Perron stable graph, pulse entrance map, crossing derivative,
   two exit faces, and basin attachment to prove Theorem C.
7. **Frequency, amplitude, and safety.**  Derive the bordered response rows,
   prove (D2), give the quantitative inverse and safety inequalities, and
   state Corollary E.
8. **Numerical validation and reproducibility.**  Report only claim-bearing
   interval constants in the main text.  Put schemas, hashes, arithmetic
   environments, cell partitions, and hostile mutation tests in the
   supplement.
9. **Discussion.**  Separate exact synchrony from asynchronous robustness,
   fixed Dobrushin gaps from sparse/closing-gap families, and pulse safety
   from any unproved equality with a maximal-canard parameter root.

## Main text versus appendices

The main text retains the complete-line pullback argument, the exact
upper-triangular Lin conjugation and full cokernel, the Lyapunov--Perron
construction, the pulse-routing geometry, and the block-triangular control
inverse.  Appendices contain:

- Fourier/Wiener finite-tail estimates and logarithmic right-half covers;
- parameter-box sensitivity residuals and interval determinant arithmetic;
- method-of-steps Bernstein propagation for basin attachment;
- source manifests, reproduction commands, and validation ledgers.

The old fixed-amplitude target-chart construction is not inserted into this
paper unless it is needed to prove the scalar leaky Lin root.  Its separate
collar and trace problems should not interrupt the pulse-onset argument.

## Release gate

The manuscript is not submission-ready until all of the following are true:

1. the proved center inner one-unstable splitting is continued to a parameter
   neighborhood adequate for Theorem C, with uniform projection and graph
   constants; a global outer zero-unstable count is required only if stated as
   a theorem, while local outer attraction may instead be supplied by the
   direct return contraction;
2. the local stable graph, directed pulse-family crossing, both exit routes,
   nonlinear phase chart, and outer attracting tube are certified;
3. the proved outer D4 enclosure and its nonzero two-output target radius are
   composed with the physical-threshold theorem without replacing the outer
   radius by the smaller simultaneous-branch minimum;
4. \(D_\xi J_c\) and the physical safety inequalities are bounded;
5. the general-network theorem states exactly which conclusions are uniform
   in \(N\) and which hold only for each fixed topology;
   in particular, the fixed-topology threshold sheet (E2) is not presented
   as a topology-uniform asynchronous basin until a strip-invariant
   collective routing tube has been certified; the integrable quadratic
   defect estimate (A3) alone does not supply that tube;
6. every theorem clause is linked to a proof or a source-bound numerical
   certificate, the full focused test suite passes, and the rendered PDF is
   reviewed page by page.

The scalar leaky canard root and a theorem comparing it with \(J_c\) would
strengthen the paper, but they are not silently assumed in Theorems C--D.  If
the final title or abstract claims a same-model canard-to-onset identity,
that comparison becomes an additional mandatory release gate.
