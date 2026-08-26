# Exact continuous outer kernel: Stage-3 initial shard

Status: **two rigorous, composable AC-density injection shards; not a
full-period kernel or return contraction.** Stage 2 directed the signed
phase cancellation for the stored finite matrix but left the continuous
transfer errors \(E_v,E_w\) empty. This artifact begins the missing proof on
the exact RFDE itself. It validates the first \(10^{-3}\) physical-time cell
of both delayed-history injections, including the \(10^{-8}\) exact
orbit/period ball, and exports endpoint interval boxes suitable for the next
method-of-steps cell.

The executable source is
[the Stage-3 shard](../src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py),
the generator is
[the experiment](../experiments/leaky_outer_continuous_kernel_stage3_shard.py),
and the tracked output is
[the result](../experiments/results/leaky_outer_continuous_kernel_stage3_shard.json).

## 1. The shard

Fix the input-history cell

\[
 -10^{-3}\leq\theta\leq0.
\]

For delay \(\tau_j\), its AC-density injection occurs at
\(s=\theta+\tau_j\) with vector \(B_j(s)e_v\). Put \(u=t-s\). On
\(0\leq u\leq10^{-3}\),

\[
 u<10^{-3}<\tau_0,
\]

so causality gives \(R(t-\tau_k,s)=0\) for both delays. The principal
resolvent therefore obeys the ordinary interval equation

\[
 \frac{dR}{du}=A(s+u)R,\qquad R(0)=I.
\]

There is no omitted delayed term on this initial cell.

The exact period lies in the stored binary64 period plus/minus \(10^{-8}\).
The exact voltage is evaluated from the directed DFT of the stored Fourier
polynomial over the entire phase cell, then enlarged by \(10^{-8}\) in the
component Wiener norm. Thus

\[
 a(t)=1-V_o(t)^2-\varepsilon
 \{\kappa_1+3\kappa_3(V_o(t)-1)^2\}
\]

is enclosed for every exact orbit, period, injection label, and time in the
cell. Likewise, the injection coefficient

\[
 b_j(s)=\frac{\varepsilon}{2}
 \{\kappa_1+3\kappa_3(V_o(\theta)-1)^2\}
\]

is enclosed on the full \(\theta\)-cell.

## 2. A rigorous interval-Picard step

Let \(\mathcal A\) enclose \(A(s+u)\) on a cell of width \(h\), let
\(\mathcal F\) enclose already validated delayed forcing, and suppose the
incoming endpoint matrix lies in \(\mathcal X_0\). Write

\[
 L=\|\mathcal A\|_\infty,\quad
 X_0=\|\mathcal X_0\|_\infty,\quad
 F=\|\mathcal F\|_\infty.
\]

Every solution path satisfies

\[
 \|X(u)\|_\infty\leq(X_0+hF)e^{Lh}=:X_*.
\]

Hence

\[
 \|X(u)-X(0)\|_\infty
 \leq h(LX_*+F)=:\Delta.
\]

Enlarge every entry of \(\mathcal X_0\) by \(\Delta\) to obtain the invariant
path box \(\mathcal X_*\). Outward interval integration then gives

\[
 X(h)\in
 \mathcal X_0+h\{\mathcal A\mathcal X_*+\mathcal F\}.
\]

All norms, exponentials, products, sums, and endpoint conversions in the
artifact use 160-bit outward MPFR rounding. This is deliberately a low-order
but rigorous interval-Taylor/Picard shard. Its public evaluator also accepts
nonzero delayed forcing boxes, so validated endpoints can be composed once a
later shard crosses a delay boundary.

For each \(j=0,1\), the endpoint density box is finally

\[
 K_j(s+10^{-3},\theta)
 \in\mathcal R_j B_j(s)e_v.
\]

The result records the time and phase cells, exact voltage and coefficient
boxes, invariant path box, endpoint resolvent, density vector, no-delay
margin, and all validation gates separately.

## 3. What remains

This artifact covers one \(\theta\)-cell and only the first \(10^{-3}\) of
elapsed propagation. It has not yet:

- tiled \([-5\sqrt5,0]\) in \(\theta\);
- propagated every injection through all method-of-steps depths to
  \([T-5\sqrt5,T]\);
- made the signed return-time subtraction at the continuous-density level;
- integrated cellwise total variation; or
- produced \(E_v,E_w,E_{\rm phase}\).

Therefore the Stage-2 gate

\[
 \max\{Q_{v,h}+E_v,Q_{w,h}+E_w\}<1
\]

is not re-evaluated. No arbitrary-\(C^0\) contraction, outer attracting tube,
pulse capture, or onset statement follows from two local injection shards.
The mathematical advance is narrower: exact continuous AC-density propagation
has now started with a replayable interval cell and a source-bound composition
interface, rather than remaining only a proposed numerical route.
