# Stage 4A: source-bound split-return pilot

## Status

This artifact executes the physical-time first and second variational
equations along the source-bound inner Route-C orbit polynomial. It computes
three finite-section meshes, a finite-horizon stable-power candidate, and
the six projected \(D^2P\) block pilots. The calculation uses
\(\mathtt{numpy.longdouble}\), fixed-step RK4, and cubic delayed
interpolation.

None of these values is an outward-rounded continuous-history bound. The
strict ingress therefore keeps \(K_s\), the split return-ball radius, and
all six Hessian blocks null. No stable graph, separator, or pulse onset is
claimed.

The executable source is
[leaky_projected_return_hessian_stage4a_pilot.py](../src/canard_control/leaky_projected_return_hessian_stage4a_pilot.py),
the generator is
[leaky_projected_return_hessian_stage4a_pilot.py](../experiments/leaky_projected_return_hessian_stage4a_pilot.py),
and the result is
[leaky_projected_return_hessian_stage4a_pilot.json](../experiments/results/leaky_projected_return_hessian_stage4a_pilot.json).

## Computation

The initial section coordinates consist of nodal voltage perturbations with
the current voltage fixed to zero, together with the current recovery
perturbation. The method of steps propagates the full first-variation matrix
and symmetric second-variation tensor. At one period, the affine-event
formulas produce the Route-C section return map in physical time.

The dominant right and left finite-section eigenvectors define
\(P_u=q\ell\) and \(P_s=I-P_u\). The six diagnostic blocks are

\[
 P_sD^2P(P_s\cdot,P_s\cdot),\quad
 P_sD^2P(P_s\cdot,q),\quad
 P_sD^2P(q,q),
\]

\[
 \ell D^2P(P_s\cdot,P_s\cdot),\quad
 \ell D^2P(P_s\cdot,q),\quad
 \ell D^2P(q,q).
\]

Their reported finite-tensor values use absolute row sums. This is an
upper bound for the computed nodal tensor, but not for the RFDE operator.

## Three-mesh result

The unstable multiplier converges across the \(120,180,240\)-step meshes as

\[
 2.01045325235,\qquad 2.01045360305,\qquad 2.01045366782.
\]

The corresponding stable projection norms are
\(2.40070789,2.40090289,2.40113693\), consistent with the independent
Stage-3 binary diagnostic. The \(240\)-step projected one-return stable
restriction has nodal norm

\[
 0.00448110906613<\rho_s.
\]

Thus \(K_s=1\) is an all-power candidate for this finite-section projected
map: at \(n=0\), the restriction is the identity on \(E_s\), and the
one-step norm is below \(\rho_s\), so submultiplicativity handles
\(n\geq1\). This does not contradict the old-norm result
\(\lVert P_s\rVert\geq2\). The latter is the norm of the ambient projection,
whereas \(K_s\) measures powers on the already split stable coordinate.
Neither finite-section statement is a continuous-history proof.

At \(240\) steps, the six block pilots are

\[
\begin{array}{lll}
 C_s^{ss}=0.0209910,&
 C_s^{su}=0.0821704,&
 C_s^{uu}=7.26112,\\
 C_u^{ss}=0.295927,&
 C_u^{su}=0.282260,&
 C_u^{uu}=26.19337.
\end{array}
\]

The source-registered heuristic envelope takes the maximum of the last two
meshes, adds twice their absolute change, and adds \(10^{-15}\). It gives

\[
\begin{array}{lll}
 \widehat C_s^{ss}=0.0224687,&
 \widehat C_s^{su}=0.0887641,&
 \widehat C_s^{uu}=7.94682,\\
 \widehat C_u^{ss}=0.296931,&
 \widehat C_u^{su}=0.283096,&
 \widehat C_u^{uu}=26.1969.
\end{array}
\]

This envelope is a convergence heuristic, not directed discretization
error.

## Matrix-majorant pilot

Substituting the heuristic envelope, \(K_s=1\), and the candidate radii
\(R_s=10^{-3}\), \(R_u=7\times10^{-4}\) into the exact Stage-4 evaluator
gives

\[
 M_{\mathrm{pilot}}=
 \begin{pmatrix}
 0.0194348&1.2982491\\
 0.000603959&0.0227152
 \end{pmatrix}.
\]

Although the upper-right entry exceeds one, the reverse coupling is tiny.
The Perron upper bound is \(0.0491246\), and the canonical weighted row-sum
upper bound is \(0.579216\). This is exactly the anisotropy erased by a
single scalar \(C_N\).

The pilot self-map image and residual are

\[
 \mathcal T(R)\leq
 \binom{0.000664105}{0.00000825231},
 \qquad
 R-\mathcal T(R)\geq
 \binom{0.000335895}{0.000691748}.
\]

It also gives

\[
 \lVert h\rVert\leq8.24606\times10^{-6},
 \qquad
 \lVert Dh\rVert\leq6.30763\times10^{-4}.
\]

Thus contraction, self-map, and the \(1.7\times10^{-3}\) design ball all
close at pilot level. Every theorem flag nevertheless remains false.

## Isolated inflation sensitivity

For each block, the exact Stage-4 evaluator multiplies only that pilot
baseline, holds the other five fixed, and bisects between the last closing
and first failing multiplier. The approximate closing multipliers are

\[
\begin{array}{c|rrrrrr}
\text{block}&C_s^{ss}&C_s^{su}&C_s^{uu}
             &C_u^{ss}&C_u^{su}&C_u^{uu}\\ \hline
\text{factor}&131.16&24.53&1.7510&2037&1469&44.65 .
\end{array}
\]

A common multiplier on all six blocks closes only to about \(1.72375\).
These are nonrigorous tolerances around a nonrigorous baseline, not theorem
allowances. They do reveal the correct validation priority:
\(s\leftarrow uu\) is the tight block because the stable self-map slack is
consumed first. The largest absolute block, \(u\leftarrow uu\), can tolerate
a much coarser isolated enclosure.

## Proof boundary

The three missing rigorous constructions are:

1. an all-power continuous-history stable propagator bound
   \(\lVert A_s^n\rVert\leq K_s\rho_s^n\);
2. a split return tube that proves the first positive return, excludes
   earlier hits, and retains a uniform event-speed lower bound;
3. outward-rounded first and second method-of-steps variations, including
   the validated orbit correction ball, followed by projection before
   norms.

The \(1.7\times10^{-3}\) split radius remains a design candidate only.
