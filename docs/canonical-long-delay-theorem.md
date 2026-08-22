# Canonical long-delay local history-connection theorem

Status: **proved for every fixed admissible preparation datum
\(\mathcal P\), 2026-08-22.** The proof is split between the exact model,
growing-graph, one-sided Green, and normalized-gap notes and is assembled
below. An independent falsification audit found no remaining P0/P1 gap after
the weighted-space and preparation-quantifier repairs. The theorem concerns
a canonical local history selection. It does not identify an unspecified
outer Fenichel family with that selection.

## 1. The object whose root is taken

Fix

\[
 K\ne0,\qquad D_w>0,\qquad
 0<\theta_0<\theta_1,
 \qquad \alpha=\frac{\sqrt6}{4},
\tag{1}
\]

and the final two-module RFDE (M). The layer parameter is restricted to a
closed interval inside its exact positivity range

\[
 -\frac16<\eta<\frac1{12}.
\tag{2}
\]

Let \(\delta=\sqrt\varepsilon\), \(\mu=\delta^2\nu\), and choose one
sufficiently large, fixed \(p\). Put

\[
 S_\delta=\sqrt{2p\log(1/\delta)}.
\tag{3}
\]

Also fix one admissible preparation datum \(\mathcal P\): the graph cutoff
profiles, planar joining cutoff, degree-three normal extension operator,
phase buffer, and the two \(\mathscr H=0\) tail levels. Every unadorned gap
and root below is relative to this declared \(\mathcal P\); equivalently it
may be written \(D_{\mathcal P}\), \(\nu_{c,\mathcal P}\), and
\(\mu_{c,\mathcal P}\). The estimates are uniform over preparation data
with the common finite derivative bounds in the two construction theorems,
but no preparation-independent exact finite-\(\delta\) root is asserted.

For every target \(\delta\), the growing-graph construction uses a cutoff
frozen at that target and a dummy amplitude
\(\rho_{\mathrm{amp}}\in[-\delta,\delta]\). On the retained shrinking tube
it gives an exact local invariant-history graph of the uncut RFDE and a
reduced field

\[
 Q_{\delta,\nu,\eta}
 =q_0+\delta q_1+\delta^2q_2+\delta^3R_3,
\tag{4}
\]

with the declared \(C_\nu^1C_\eta^2\) rectangular mixed jets and the
pointwise Gaussian-compatible remainder. Outside the retained tube, extend
the planar field by the canonical preparation: it equals \(q_0\) on the
two tails. The preparation is only a selection device; no prepared point
outside the retained tube is called a solution of the physical RFDE.

On the left and right prepared tails impose the exact level condition
\(\mathscr H=0\), and impose the common phase \(X=0\) at the matching
section. The one-sided Green construction gives unique traces

\[
 z^a_{\delta,\nu,\eta},\qquad
 z^r_{\delta,\nu,\eta}.
\tag{5}
\]

Their retained central pieces lie on the exact uncut history graph. Define

\[
 D(\delta,\nu,\eta)
 =\frac{2}{\alpha e}
 \left[
  \mathscr H(z^a_{\delta,\nu,\eta}(0))
  -\mathscr H(z^r_{\delta,\nu,\eta}(0))
 \right].
\tag{6}
\]

At \(X=0\), the derivative of \(\mathscr H\) in the transverse
\(Y\)-direction is nonzero near the singular matching point. Hence, in the
small neighborhood fixed by the trace theorem,

\[
 D=0
 \quad\Longleftrightarrow\quad
 z^a(0)=z^r(0).
\tag{7}
\]

Thus the root is not merely a zero of an arbitrary observable. By planar
uniqueness and injectivity of the history embedding, it is equality of the
two complete retained RFDE histories.

## 2. Main theorem

**Theorem A (canonical local history-connection root).** For every fixed
admissible preparation datum \(\mathcal P\), there are
\(\delta_0,\eta_0,c_0>0\) such that, for

\[
 0<\delta<\delta_0,
 \qquad |\eta|<\eta_0,
\]

the normalized gap \(D/\delta\) has a unique root
\(\nu_c(\delta,\eta)\) in

\[
 \left|\nu+\frac{11}{24\alpha}\right|<c_0.
\tag{8}
\]

The corresponding retained histories meet exactly and form one local RFDE
orbit through the fold chart. Moreover,

\[
\boxed{
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}
   \delta^3\eta
 +O(\delta^4|\eta|+\delta^3\eta^2).}
\tag{9}
\]

The remainder is uniform on the fixed data box. Since
\(4\alpha=\sqrt6\), the leading coefficient is
\(K(\theta_0-\theta_1)/\sqrt6\).

### Proof assembly

The exact layer algebra gives, for every \(\eta\),

\[
 \ell^T\mathbb B_\eta(d\theta)r
 =\frac13\delta_{\theta_0}(d\theta)
  +\frac23\delta_{\theta_1}(d\theta),
\tag{10}
\]

while its transverse history forcing changes by
\(\eta q(\delta_{\theta_0}-\delta_{\theta_1})\). Thus the compared
systems have the same complete projected delay measure, not just the same
first moment.

The growing-graph Taylor theorem makes the fixed-tube symbolic jets actual
on \(|s|\le S_\delta\), including

\[
 \partial_\nu q_1=(0,1)^T,
 \qquad
 \partial_\eta q_1=0,
 \qquad
 \partial_\eta q_{2,X}(\gamma_0(s),\nu,0)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
\tag{11}
\]

The phase-normal Green theorem constructs the two traces, eliminates the
normally growing mode by opposite one-sided projections, and supplies the
mixed trace estimates. Gaussian differentiation of (6) then yields

\[
\begin{aligned}
 \frac{D}{\delta}
  &=\sqrt{2\pi}
    \left(\nu+\frac{11}{24\alpha}\right)+O(\delta),\\
 \partial_\nu D
  &=\delta\sqrt{2\pi}+O(\delta^2),\\
 \partial_\eta D
  &=-\frac{K(\theta_0-\theta_1)}{4\alpha}
    \sqrt{2\pi}\,\delta^2
    +O(\delta^3+\delta^2|\eta|),\\
 \partial_{\eta\eta}D&=O(\delta^2).
\end{aligned}
\tag{12}
\]

The first two lines give existence, uniqueness, and the simple-root bound by
the implicit-function theorem. Along the root,

\[
 \partial_\eta\nu_c
 =-\frac{\partial_\eta D}{\partial_\nu D}
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta
  +O(\delta^2+\delta|\eta|).
\tag{13}
\]

Integrating (13) from \(0\) to \(\eta\) and multiplying by
\(\delta^2\) proves (9). Finally, (7), planar uniqueness, and injectivity
of the uncut history embedding prove equality of complete retained
histories. No backward inversion of the ambient RFDE semiflow is used.

## 3. Robustness to a tame outer selection

The canonical preparation is not claimed to be an arbitrarily chosen outer
Fenichel manifold. A separate comparison statement is available.

**Conditional Corollary B (physical outer selection).** Suppose a physical
attracting/repelling outer history family is selected by a fixed,
parameter-coherent rule, enters the retained graph, and its boundary
residual and rectangular \(C_\nu^1C_\eta^2\) jets are bounded by

\[
 C\langle S_\delta\rangle^m e^{cS_\delta}
\tag{14}
\]

with constants fixed before \(p\) is chosen. Then its matching gap differs
from the canonical gap by

\[
 O\left(e^{-S_\delta^2/2+cS_\delta}
          \langle S_\delta\rangle^{m'}\right)
 =O(\delta^{p-o(1)}),
\tag{15}
\]

with the same parameter derivatives. Choosing \(p\) sufficiently large
makes the physical root difference smaller than the remainder in (9), so
the physical outer root has the same leading coefficient.

The hypothesis (14) is not yet proved for an arbitrary RFDE Fenichel
selection. Without a parameter-coherent selection rule, it is false as a
logical inference: exponentially close outer manifolds can be chosen with
arbitrarily oscillatory parameter dependence. Corollary B must therefore
remain conditional until an outer Lyapunov--Perron construction verifies
(14).

## 4. Verification record and remaining physical gate

The proof audit checked all of the following in the final files.

1. The growing graph is exact on the retained shrinking tube, uses a cutoff
   frozen at the target \(\delta\), and proves the full expansion (4) with
   state derivatives through order three and rectangular
   \(C_\nu^1C_\eta^2\) jets.
2. Its uncut flow hull includes every fixed-delay segment needed for
   \(q_1,q_2\), every history in the embedding, and the central portions of
   both traces. Artificial prepared tails are excluded from the RFDE claim.
3. The Green proof controls the tangent phase and normal one-sided
   projection uniformly before \(p\) is chosen, proves the moving-section
   jets, and bootstraps the canonical traces into the shrinking actual graph.
4. The baseline first line of (12), the central equivalence (7), and all
   mixed derivatives used to differentiate (6) are written explicitly.
5. An independent skeptical audit finds no hidden
   \(e^{S_\delta^2/2}\), derivative-dependent exponent, moving-cutoff
   derivative, or ambient-backward-RFDE step.

All five checks pass for the preparation-indexed canonical object, so (9) is
a proved local RFDE history-connection theorem. It must still not be
advertised as the physical maximal-canard theorem. The physical outer
maximal-canard wording belongs only to Corollary B after its additional
hypothesis is verified.
