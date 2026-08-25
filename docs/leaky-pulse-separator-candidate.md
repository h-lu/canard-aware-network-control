# A finite-section candidate for the physical pulse separator

Status: **source-bound numerical candidate, not a separator theorem.**  The
calculation identifies a sharply converged pulse amplitude at which a sample
of the solution-determining reduced state approaches the inner periodic
branch over three successive returns.  It supplies a concrete target
for a validated Floquet/stable-manifold connection calculation.  Neither the
finite eigenvector nor the resulting shooting zero is presently enclosed by
directed arithmetic.

## 1. A history-space finite-section shooting coordinate

Let $K(J)\in C([-5\sqrt5,0],\mathbb R^2)$ be the exact terminal-history
curve produced by the one-unit voltage pulse.  Its construction and positive
stimulus orientation are proved separately in
`docs/leaky-pulse-terminal-history.md`.  After release, let

\[
 \Phi_tK(J)
\]

denote the autonomous RFDE history.  The phase of the registered inner
periodic polynomial is fixed by the section

\[
 v=v_{\rm in}(0),\qquad \dot v_{\rm in}(0)>0.
\]

The continuous reduced state consisting of the voltage history and current
recovery value determines future solutions because recovery enters without
delay.  For a monodromy step count $n$, the map $H_n$ samples that voltage
history on the uniform mesh extending just beyond the longest delay and
appends the current recovery coordinate.  This finite vector determines only
the declared cubic-interpolation discretization; its Euclidean norm is not a
norm of the full two-component RFDE history.  If $M_n$ is the resulting RK4
finite monodromy matrix and $\ell_n$ is its normalized leading left
eigenvector, oriented by a positive recovery component, define at the $k$-th
positive return

\[
 g_{n,k}(J)=
 \ell_n^{\mathsf T}
 \left{
 H_n(\Phi_{t_{n,k}(J)}K(J))-H_n\gamma_{\rm in}(0)
 \right}.
\tag{1.1}
\]

The experiment solves $g_{n,k}(J)=0$ for

\[
 n\in\{120,180,240\},\qquad k\in\{1,2,3\}.
\]

The physical integration is split on both grids

\[
 m\sqrt5,\qquad 1+m\sqrt5,
\]

as well as at the final time.  These grids contain the propagation times of
the possible regularity losses at pulse onset and release, and every segment
is shorter than the shortest delay.  Thus delayed evaluations use completed
segments and no DOP853 step crosses a declared propagated-regularity
breakpoint.  A separate ladder decreases the relative and absolute tolerances
by two orders of magnitude and decreases the maximum step from $0.04$ to
$0.01$.

## 2. What the convergence means

The roots concentrate near

\[
 J_{\rm sep}^{\rm num}\simeq 0.30113533709.
\tag{2.1}
\]

The stored roots and multiplier-scaled derivatives are

| $n$ | $J_{n,1}$ | $J_{n,2}$ | $J_{n,3}$ | scaled derivatives, $k=1,2,3$ |
|---:|---:|---:|---:|---:|
| 120 | 0.301135337048820 | 0.301135337086903 | 0.301135337086903 | -3.4490018, -3.4490111, -3.4490026 |
| 180 | 0.301135337052195 | 0.301135337086904 | 0.301135337086900 | -3.4489715, -3.4489880, -3.4489859 |
| 240 | 0.301135337051298 | 0.301135337086900 | 0.301135337086901 | -3.4489558, -3.4489725, -3.4489721 |

At each fixed $n$, the second and third return roots agree much more closely
than the first and second.  At the third root the reduced sampled state is
close to the stored inner reference, while the multiplier-scaled derivatives

\[
 \lambda_n^{-(k-1)}\,\partial_J g_{n,k}(J_{n,k})
\tag{2.2}
\]

remain bounded away from zero and agree across returns and meshes.  This is
the numerical signature expected when a one-parameter pulse curve crosses a
codimension-one stable manifold transversely: the unstable coordinate grows
by approximately $\lambda_n$ at each return, whereas (2.2) removes that
growth.

Equation (2.1) corrects an earlier exploratory value by about
$2.4\times10^{-9}$.  The change comes from treating $t=1$ as an explicit
left/right forcing breakpoint.  The refinement ladder shows that the
corrected binary64 value is insensitive to the subsequently tightened ODE
tolerances.  This remains convergence evidence, not a rigorous error bar.

## 3. Strict claim boundary

The calculation does establish the following reproducible observations:

- after omitting in each matrix the eigenvalue closest to $1$, the three
  finite spectra each have one observed multiplier outside the unit disk;
- their leading real multiplier is near $2.01045$;
- the relative defect obtained by applying the finite monodromy matrix to
  the sampled translation tangent decreases from $3.35\times10^{-6}$ to
  $2.05\times10^{-7}$ across the mesh ladder;
- all nine finite shooting coordinates have roots in
  $[0.301,0.3012]$;
- the third-return roots agree across the three meshes, and their scaled
  stimulus derivatives have magnitude greater than $3$;
- the result persists under the same-method, tighter-tolerance integration
  refinement ladder.

It does **not** establish any of the following:

- that a finite-section multiplier is an RFDE Floquet multiplier;
- convergence of the finite-section spectrum as the mesh is refined;
- simplicity of the neutral multiplier or exclusion of other unit-circle
  spectrum;
- a validated unstable Riesz projector or left Floquet covector;
- existence of the local stable manifold in the chart used by (1.1);
- an intersection of $K(J)$ with that stable manifold;
- a directed enclosure of any displayed shooting root or its derivative;
- routing of the two sides, endpoint basin inclusions, or a unique physical
  onset threshold.

The next rigorous bridge is therefore precise: enclose the relevant Floquet
spectral projection, construct a validated phase-fixed local stable-manifold
chart, and solve one connecting boundary-value problem near (2.1).  Only
after the two sides are routed to certified invariant sets can this value be
called a biological onset threshold.  Here $F$ denotes the frequency of the
outer periodic orbit, not a repeated-stimulus frequency.  The paper's
$(F,A,J-J_c)$ control statement therefore requires validated outer-orbit
frequency and extrema sensitivities, pulse-threshold sensitivities, and
safety inequalities on one common $(a,\kappa_3)$ parameter box.  A multi-pulse
return map would be needed only for a different problem in which the control
variable is the repetition frequency of the stimulus.

The executable candidate and its hostile proof-status ledger are generated
by `experiments/leaky_pulse_separator_candidate.py`.
