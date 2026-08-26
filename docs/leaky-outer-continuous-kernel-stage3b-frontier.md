# Exact continuous outer kernel: Stage-3B first-delay frontier

Status: **a rigorous two-dimensional tile crosses the first nonzero
delayed-resolvent boundary for both injection branches; the full continuous
return kernel and \(C^0\) contraction remain open.**

The executable source is
[the Stage-3B frontier](../src/canard_control/leaky_outer_continuous_kernel_stage3b_frontier.py),
the generator is
[the experiment](../experiments/leaky_outer_continuous_kernel_stage3b_frontier.py),
and the tracked output is
[the result](../experiments/results/leaky_outer_continuous_kernel_stage3b_frontier.json).
The artifact is bound to the corrected Stage-3 result and the exact stored
outer orbit, uses the unshifted physical coefficient convention, retains the
\(10^{-8}\) orbit/period ball, and performs every proof arithmetic operation
with 160-bit outward MPFR rounding.

## 1. The two-dimensional method-of-steps tile

Fix

\[
 \Theta=[-10^{-3},0],\qquad
 s_j=\theta+\tau_j,\qquad
 u=t-s_j,\qquad j=0,1.
\]

For \(0\leq u<\tau_0\), the resolvent satisfies

\[
 \partial_uR_j(u,\theta)=A(s_j+u)R_j(u,\theta),\qquad R_j(0,\theta)=I.
\]

The source divides the elapsed coordinate into cells of width at most
\(0.5\). On every rectangle \(\Theta\times U_k\), it evaluates the exact
Fourier voltage over the whole phase cell, adds the exact-orbit radius, and
forms an interval enclosure of \(A\). For

\[
 A=\begin{pmatrix}a&-1\\ \varepsilon&-\varepsilon\end{pmatrix},
\]

the infinity logarithmic norm is bounded by

\[
 \mu_\infty(A)\leq \max\{a^++1,0\}.
\]

Consequently

\[
 \|R_j(\tau_0^-,\theta)\|_\infty
 \leq
 G_j^-:=
 \exp\!\left(\sum_k h_k\mu_{\infty,k}^+\right).
\]

The recorded values are \(G_0^-<1.45665\times10^7\) and
\(G_1^-<2.43188\times10^7\). These are rigorous but intentionally coarse;
they are not candidates for the Stage-2 shadow-transfer errors.

The directed algebraic enclosure of \(\tau_0=4\sqrt5\) has a tiny nonzero
width. Across its uncertainty strip, the artifact also bounds the predecessor
resolvent \(R_j(u-\tau_0,\theta)\), rather than silently replacing it by the
identity. Its bridge is

\[
 G_j^+\leq
 \left(G_j^-+\Delta\tau_0\,b_0^+G_{\rm pred}\right)
 \exp(\mu_{\rm strip}^+\Delta\tau_0).
\]

This closes the strip for every exact delay in the directed interval.

## 2. The first genuinely delayed forcing

On

\[
 U_*=[\tau_0^+,\tau_0^++10^{-3}],
\]

the equation contains the nonzero term

\[
 F_j(u,\theta)
 =
 B_0(s_j+u)R_j(u-\tau_0,\theta).
\]

The predecessor elapsed interval is contained in
\([0,10^{-3}+\Delta\tau_0]\), where delayed feedback is still identically
zero. Stage-3's public directed Picard evaluator therefore encloses this
predecessor from \(I\), multiplies it by the delayed coefficient matrix, and
then performs a second Picard step with \(F_j\neq0\). The lower witnesses

\[
 \|F_0\|_\infty>4.0231\times10^{-4},
 \qquad
 \|F_1\|_\infty>4.4227\times10^{-4}
\]

certify that this is not another no-delay shard.

For a fixed output-row diagonal crossing the rectangle, the local,
uncorrected, per-branch history-density tile mass is bounded by

\[
 |\Theta|\,
 \sup_{\Theta\times U_*}
 \|R_j(u,\theta)B_j(s_j)e_v\|_\infty.
\]

The source uses the invariant path box, not merely the endpoint box, in this
calculation. The resulting local upper bounds are about \(25.421\) and
\(42.421\). They are neither returned-row TV bounds nor phase-subtracted
masses. Their size is a useful negative diagnostic: the coarse bridge proves
existence and composition across the delay face, but cannot be inserted as
\(E_v\) or \(E_w\).

## 3. Tight frontier and executable refinement rule

In parallel, the same \(0.5\)-cells are composed with the tighter interval
Picard endpoint boxes. For the \(\tau_0\) injection branch, eight cells close
before the first threshold failure on approximately \([4,4.5]\); for the
\(\tau_1\) branch, seven close before failure on approximately \([3.5,4]\).
The result records the accumulated path-expansion radius, failure cell,
endpoint norm and width, coefficient norm, and a source-computed minimum
dyadic depth sufficient for

\[
 h\|\mathcal A\|_\infty\leq\frac1{32}.
\]

Both first-failure cells require depth five by this prescribed step-norm
criterion, giving nominal child widths at most \(0.015625\). This is a
refinement prescription, not a claim that every child has already passed the
relative path-expansion test.

Every continuation must also enforce a relative path-expansion condition,
split \(\theta\) until the voltage enclosure has width at most \(10^{-3}\),
place exact faces at \(\tau_0\) and \(\tau_1\), and reference only previously
validated predecessor digests. A failed tight box is not a rejected
solution: the coarse enclosure remains rigorous, but the box is forbidden
from contributing to a sharp transfer error.

## 4. Exact frontier and theorem status

The history interval requires 11,181 nominal \(\theta\)-bands of width
\(10^{-3}\); one band is treated here, leaving 11,180 bands and 22,360
unstarted branch-band chains. On the treated band, 18 and 13 nominal
\(0.5\)-elapsed cells remain for the two branches after the first crossing.
The certificate's exact nominal coarse two-dimensional queue contains
1,048,203 remaining cells before adding mandatory \(\tau_1\)-alignment faces
and adaptive children. That last caveat matters: adaptive refinement changes
the eventual leaf count, so the nominal count is not presented as a completed
cover.

No returned output-history row has yet received the complete signed density;
phase subtraction has not been performed at the continuous level; and
\(E_v,E_w,E_{\rm phase}\) remain empty. Therefore

\[
 \max\{Q_{v,h}+E_v,Q_{w,h}+E_w\}<1
\]

is not re-evaluated. The flags for arbitrary-\(C^0\) linear contraction,
nonlinear outer attraction, pulse capture, and physical onset all remain
false. The rigorous advance is exactly the first delayed Volterra term and
its composable frontier, not a global contraction theorem.
