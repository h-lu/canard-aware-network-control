# Outer continuous kernel: Stage-3C finite delay-word compression

Status: **the million-cell continuation has been replaced by an exact finite
Volterra-word architecture; the 21 directed path integrals and hence the
continuous-history contraction remain open.**

The executable source is
[the Stage-3C module](../src/canard_control/leaky_outer_delay_word_stage3c_compression.py),
the generator is
[the experiment](../experiments/leaky_outer_delay_word_stage3c_compression.py),
and the tracked output is
[the result](../experiments/results/leaky_outer_delay_word_stage3c_compression.json).
The artifact binds the frozen Stage-2 signed kernel, the corrected Stage-3B
frontier, the exact outer orbit, and the ambient pulse attachment. Directed
claims use 160-bit outward MPFR arithmetic. The singular-value and sign-front
calculations are explicitly binary64 diagnostics.

## 1. Why the two-dimensional queue is not intrinsic

Let \(\Phi(t,s)\) be the fundamental matrix of the instantaneous equation

\[
 \partial_t\Phi(t,s)=A(t)\Phi(t,s),\qquad \Phi(s,s)=I.
\]

The causal principal resolvent of the two-delay variational equation obeys
the exact Volterra identity

\[
 R(t,s)=\Phi(t,s)+\sum_{j=0}^1
 \int_{s+\tau_j}^{t}\Phi(t,r)B_j(r)R(r-\tau_j,s)\,dr.
\tag{1.1}
\]

Iterating (1.1) labels every contribution by a finite word in the alphabet
\(\{0,1\}\). A word \(j_1\cdots j_m\) consumes at least
\(\tau_{j_1}+\cdots+\tau_{j_m}\) units of elapsed time. This elementary
causality fact, rather than a fine rectangular mesh, determines the global
complexity.

The \(\tau_j\)-history injection exists only for
\(\theta\in[-\tau_j,0]\). Its injection time
\(s=\theta+\tau_j\) is therefore nonnegative for both branches. The largest
possible elapsed horizon is consequently

\[
 H=T<26.605.
\]

The complete possible word list is

\[
 \varnothing,0,1,00,01,10,11.
\]

The \(\tau_1\)-history injection and the initial-recovery scalar column have
the same list,

\[
 \varnothing,0,1,00,01,10,11.
\]

In particular, \(3\tau_0>T\) excludes every word of length at least three.
This inequality is recomputed on the exact period/orbit ball with outward
arithmetic. Thus the whole phase-fixed operator contains 14 history-density
word terms and seven scalar-column word terms, each involving at most a
two-dimensional ordered integral. Stage-3B's nominal queue of 1,048,203
rectangles is replaced by 21 finite analytic terms, a representation-count
reduction by more than
40,000. This count does not assert that one polynomial box per word will
suffice.

## 2. Signed phase subtraction is retained exactly

For a history injection \(s=\theta+\tau_j\), each word contribution is phase
corrected before any absolute value is taken. For a returned voltage row,

\[
 e_v^T\left\{R_{\omega}(T+\sigma,s)
 -\frac{q_v(\sigma)}{q_v(0)}R_{\omega}(T,s)\right\}
 B_j(s)e_v.
\tag{2.1}
\]

The two injection branches and all words are then summed as signed quantities.
Only the resulting density is integrated in total variation. This preserves
the Stage-2 cancellation; applying a triangle inequality word by word would
again produce a useless bound.

Every ordered integration simplex is mapped to a unit cube by a triangular
Duffy transformation. The exact Fourier coefficient field, the
\(10^{-8}\) orbit ball, the current fundamental matrix and the path integrand
can then be enclosed by directed Chebyshev-to-Bernstein coefficients. The
only activation faces are

\[
 \theta=-\tau_0,
 \qquad
 t-(\theta+\tau_j)=\sum_{k\in\omega}\tau_k.
\]

There is no mathematical reason to retain a uniform \(10^{-3}\) theta mesh.

## 3. Low-rank and sign diagnostics

The source independently rebuilds the 120-, 180-, 240- and 360-step finite
sections. After phase subtraction, the matrix containing the physical
history columns and the recovery scalar is almost rank one. At 360 steps,
the maximum row-\(\ell^1\) residual after the best rank-one subtraction is
below \(3.72\times10^{-5}\), less than \(2.93\times10^{-4}\) of the largest
corrected row norm. This is a guide to a low-rank Bernstein enclosure, not a
bound on the continuous operator.

At all four resolutions, every binary sign change lies in one of two fixed
windows:

\[
 [-9.2,-8.45],\qquad[-1.2,-0.85].
\]

The first contains the exact branch-support face \(-\tau_0\); cubic-history
interpolation can create several nearby alternating coefficients. Outside
the two windows, every output row has the same normalized sign template

\[
                    +,quad-,\quad+.
\]

A proof-quality implementation may therefore integrate the signed polynomial
on the three safe regions and pay an absolute Bernstein mass only in the two
windows. The certificate does **not** promote the binary pattern to a
continuous sign theorem. A directed sign enclosure, or a direct bound for
the window mass, remains necessary.

## 4. Exact remaining gate

The finite proof task is now:

1. enclose the 14 history word contributions and seven scalar word
   contributions on their Duffy cubes;
2. sum contributions and perform (2.1) before absolute integration;
3. prove the continuous sign template off the two windows, or bound all five
   regions directly;
4. return \(E_v,E_w,E_{\rm phase}\), or direct bounds
   \(Q_v,Q_w,Q_{\rm phase}\).

The frozen Stage-2 gate allows

\[
 E_v<0.8730921051,\qquad E_w<0.9972399927.
\]

Using the independently validated pulse history distance and the
\(10^{-4}\) section radius, the phase-chart gate allows a total norm below
approximately \(3.792\); after subtracting the Stage-2 phase shadow, more
than \(1.85\) remains for \(E_{\rm phase}\). These are strict available
budgets, not error estimates.

No directed word integral has yet been emitted. Accordingly
\(E_v,E_w,E_{\rm phase}\) remain null, and arbitrary-\(C^0\) linear
contraction, nonlinear outer attraction, pulse capture and physical onset
all remain false. The advance is that the final continuous-kernel obstruction
is now one finite, source-bound path-integral calculation rather than an
unbounded adaptive grid campaign.
