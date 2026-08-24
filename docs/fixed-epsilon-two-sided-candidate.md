# A fixed-\(\varepsilon\) two-sided full-history-matched candidate

Status: **an actual binary64 two-branch numerical solve, not a selected-root
certificate.**  The split RFDE residual contains a left flight, a right
flight, a phase condition, and equality of every represented history node at
the seam.  Sparse Newton closes this square residual, and a full discrete
left adjoint agrees with both a direct parameter tangent and centered finite
differences.  The finest central computation gives

\[
 a_N=1.0425120444679274,
 \qquad
 \rho_N=-0.3463310348461952.
\tag{0.1}
\]

These are **finite-section candidates**.  The calculation still prescribes
an artificial entry history and replaces the backward-extendible repelling
trace bundle by one scalar exit observable.  Consequently (0.1) is neither a
selected root nor an enclosure of \(\rho_*\).

The implementation is
[fixed_epsilon_two_sided_candidate.py](../src/canard_control/fixed_epsilon_two_sided_candidate.py),
the deterministic generator is
[fixed_epsilon_two_sided_candidate.py](../experiments/fixed_epsilon_two_sided_candidate.py),
and the hostile tests are
[test_fixed_epsilon_two_sided_candidate.py](../tests/test_fixed_epsilon_two_sided_candidate.py).
The package is source-bound to the exact-contract blueprint and its frozen
result and note.  Its JSON result stores all 1338 binary64 components of the
finest primal trace and all 1338 components of the normalized discrete
adjoint, together with separate byte-level hashes.

## 1. Plant, horizons, and the two branches

The chart is the exact fold-time RFDE from the blueprint, with

\[
 \delta=\frac1{\sqrt5},\qquad \varepsilon=\frac15,
 \qquad a=1+\delta^2\nu,
\]

\[
\begin{aligned}
X'={}&Y-X^2
+\delta\left[-\frac{X^3}{3}
+\frac15\left(\frac{X_4+X_5}{2}-X\right)\right]\\
&+\delta^2\eta(X^2-X_\Theta^2)
+\frac{\delta^3}{4}
\left(\frac{X_4^3+X_5^3}{2}-X^3\right),\\
Y'={}&-X+\delta\nu .
\end{aligned}
\tag{1.1}
\]

The physical history input is the periodic-orbit period diagnostic

\[
 T_{\mathrm{diag}}=16.54038779818094,
\]

and its scaled midpoint is

\[
 \Theta_{\mathrm{diag}}=\delta T_{\mathrm{diag}}
 =7.397086298188131>5>4.
\tag{1.2}
\]

This decimal is not an exact plant delay.  The parent periodic-orbit
certificate encloses the true period, whereas the present binary64 candidate
uses only its midpoint and does not propagate period uncertainty.

Fix \(L_-=L_+=L\).  On a uniform mesh of step \(h_N=1/N\), represent

\[
 H_N=\frac{\lceil N\Theta_{\mathrm{diag}}\rceil}{N}
 \ge \Theta_{\mathrm{diag}}.
\tag{1.3}
\]

The left array covers \([-L-H_N,0]\), and the right array covers
\([-H_N,L]\).  Delays 4 and 5 are exact mesh shifts; the period delay is
linearly interpolated.  At \(N=8,16,32\), the represented horizons are
\(7.5,7.4375,7.40625\), respectively.

## 2. The square split-history residual

Let \(z^-_j,z^+_j\in\mathbb R^2\) be the left and right nodal states.  The
finite entry template is

\[
\begin{aligned}
 X_{\rm ent}(t;q,\nu)&=-\frac{t+q}{2},\\
 Y_{\rm ent}(t;q,\nu,\eta)&=\frac{(t+q)^2-2}{4}
 +\delta\nu(t+L)+c(q,\eta),
 \qquad -L-H_N\le t\le-L.
\end{aligned}
\tag{2.1}
\]

Put \(x_j=(L+j-q)/2\) for \(j=0,4,5\) and
\(x_\Theta=(L+\Theta_{\rm diag}-q)/2\).  The constant shift is

\[
\begin{aligned}
c(q,\eta)={}&-\delta\left[-\frac{x_0^3}{3}
+\frac15\left(\frac{x_4+x_5}{2}-x_0\right)\right]\\
&-\delta^2\eta(x_0^2-x_\Theta^2)
-\frac{\delta^3}{4}\left(\frac{x_4^3+x_5^3}{2}-x_0^3\right).
\end{aligned}
\tag{2.2}
\]

It is smooth in \((q,\nu,\eta)\).  Since the fast field is affine in \(Y\),
(2.2) enforces the RFDE solution-manifold compatibility equation at
\(t=-L\): the template derivative and vector field both have fast component
\(-1/2\).  Its slow compatibility equation is already exact because
\(c(q,\eta)\) is constant in history time.  The maximum stored compatibility
defect is \(2.23\times10^{-16}\).  This compatible history has **not** been
shown to lie in the selected attracting bundle.

On each flight interval use the implicit trapezoidal collocation residual

\[
 R_j=\frac{z_{j+1}-z_j}{h_N}
 -\frac12\{F(z_j)+F(z_{j+1})\}.
\tag{2.3}
\]

The complete discrete system is

\[
\mathcal F_N(z^-,z^+,q,\nu;\eta)=
\begin{pmatrix}
 z^-|_{[-L-H_N,-L]}-z_{\rm ent}(q,\nu,\eta)\\
 R^-_{\rm flow}\\
 X^-(0)\\
 z^+|_{[-H_N,0]}-z^-|_{[-H_N,0]}\\
 R^+_{\rm flow}\\
 G(z^+(L))
\end{pmatrix}=0,
\tag{2.4}
\]

where

\[
 G(X,Y)=\frac{X^2}{2}-\frac{Y}{2}-\frac14.
\tag{2.5}
\]

The fourth row of (2.4) is a full represented-history jump, not current-state
matching.  For example, at \(L=3,N=32\), (2.4) has 1338 unknowns and 1338
residuals and matches 238 two-state history nodes, hence 476 scalar history
components.  The extra phase variable \(q\) closes the phase equation, while
\(\nu\) closes the exit equation.

A method-of-steps DOP853 solve supplies a seed; sparse Newton then solves
(2.4).  Continuation to \(\eta=\pm2\times10^{-4}\), section variation, and
mesh refinement are all recomputed from the same residual rather than by
post-processing a scalar shooting gap.

## 3. Discrete adjoint and the physical response factor

Separate \(\nu\) from the remaining unknowns \(u=(z^-,z^+,q)\).  Then

\[
 J_N=\partial_u\mathcal F_N\in\mathbb R^{M_N\times(M_N-1)},
 \qquad c_\nu=\partial_\nu\mathcal F_N,
 \qquad K_N=[J_N,c_\nu].
\tag{3.1}
\]

The computed full-residual covector is

\[
 K_N^T\psi_N=e_{M_N},
\tag{3.2}
\]

so, to roundoff,

\[
 J_N^T\psi_N=0,
 \qquad \psi_N^Tc_\nu=1.
\tag{3.3}
\]

This transpose includes the entry, phase, complete-jump, exit, and both flow
blocks.  In the flow block, its delayed transpose contributions are the
discrete counterpart of the advanced differential expression

\[
 -p'(s)=A_0(s)^Tp(s)
 +\sum_{\tau\in\{4,5\}}
 \mathbf 1_{\{s+\tau\in I\}}A_\tau(s+\tau)^Tp(s+\tau).
\tag{3.4}
\]

Equation (3.2) does not validate a continuous advanced adjoint or its tail.
It is only a complete **discrete** adjoint candidate.

With \(c_\eta=\partial_\eta\mathcal F_N\), define

\[
 m_{\nu,N}=\psi_N^Tc_\nu,
 \qquad m_{\eta,N}=\psi_N^Tc_\eta.
\]

Because \(a=1+\delta^2\nu\), the physical response candidate is

\[
 \rho_N
 =-\delta^2\frac{m_{\eta,N}}{m_{\nu,N}}.
\tag{3.5}
\]

The factor \(\delta^2=1/5\) is essential.  The same value is obtained by
solving

\[
 K_N(u_\eta,\nu_\eta)=-c_\eta
\tag{3.6}
\]

and taking \(\delta^2\nu_\eta\).

## 4. Numerical diagnostics

For the central section \(L=3\):

| \(N\) | dimension | \(q_N\) | \(\nu_N\) | \(a_N\) | \(\rho_N\) |
|---:|---:|---:|---:|---:|---:|
| 8 | 342 | -0.062065610 | 0.211965309 | 1.042393062 | -0.346382729 |
| 16 | 674 | -0.061676471 | 0.212441319 | 1.042488264 | -0.346341371 |
| 32 | 1338 | -0.061579262 | 0.212560222 | 1.042512044 | -0.346331035 |

The coarse-to-medium divided by medium-to-fine differences are 4.009 for
\(\nu_N\) and 4.001 for \(\rho_N\), consistent with the expected
second-order accuracy of (2.3).  This is an empirical convergence diagnostic,
not an error bound.

Across all five stored solves:

- the maximum nonlinear residual is \(1.60\times10^{-14}\);
- the maximum nodewise complete-history jump is \(4.41\times10^{-24}\);
- the maximum \(\|J_N^T\psi_N\|_\infty\) is
  \(1.27\times10^{-15}\);
- adjoint and direct-tangent responses differ by at most
  \(2.23\times10^{-16}\);
- adjoint and centered finite differences differ by at most
  \(4.49\times10^{-10}\).

The section study at \(N=16\) is less reassuring:

| \(L\) | \(\nu_N\) | \(a_N\) | \(\rho_N\) |
|---:|---:|---:|---:|
| 2.5 | 0.268177985 | 1.053635597 | -0.350420392 |
| 3.0 | 0.212441319 | 1.042488264 | -0.346341371 |
| 3.5 | 0.165892292 | 1.033178458 | -0.352413883 |

The section spreads are 0.10229 in \(\nu_N\) and 0.00607 in \(\rho_N\).
Thus the apparent response is less section-sensitive than the candidate root,
but the observed section dependence still dominates the observed mesh
dependence.  Neither spread is an error bound for an unknown selected root.

## 5. Exact remaining obstruction

For the proposed Chebyshev/Lobatto ledger with \(p=6\), 16 history cells,
and 8 flight cells, one branch has 290 raw coefficients and the two-state
history has 194 raw coefficients.  The earlier shorthand treated 193
attracting coordinates as a compatible history chart.  That interpretation
is false: the two endpoint compatibility equations have exact rank two, so
the discrete endpoint-compatible level has dimension 192.  A rank-193
fixed-parameter immersion into that level cannot exist.

There are two equivalent count-consistent formulations.  In the ambient
formulation retain \(\xi_-\in\mathbb R^{193}\), but impose two explicit
compatibility rows on its image; the admissible zero fibre then has effective
dimension 191.  Replace each raw 194-row entry, exit, and seam equality by a
192-row projected equality and add six compatibility rows.  The arithmetic
is

\[
 \dim X_N=2(290)+193+1=774,
 \qquad
 \dim Y_N=2(96)+3(192)+6+1=775.
\tag{5.1}
\]

In endpoint-compatible intrinsic coordinates for the same raw multicell
ledger, the corresponding arithmetic is \(769\times768\).  The invariant
object is the Fredholm index, not either matrix size.  Moreover, the
194-coefficient space is only value-continuous: global \(C^1\) regularity
adds 30 internal derivative-continuity conditions, leaving dimensions 164
before and 162 after endpoint compatibility.  A \(W^{2,p}\) realization has
to make the analogous strong seams explicit.  Thus (5.1) is a repaired raw
arithmetic ledger, not an assembled strong-history collocation operator.

The required exit object remains a one-dimensional compatible,
backward-extendible history chart.  The scalar equation \(G=0\) has the
opposite geometry: on the 194-dimensional raw history space it leaves a
193-dimensional fibre.  Exact compatible histories with the same current
state and \(G=0\) but different delayed values produce different future
derivatives.  Hence it cannot substitute for the repelling chart.

If the repaired endpoint maps are constructed, one must still prove full
column rank and a one-dimensional cokernel, freeze a jump-slot complement,
and validate the resulting bordered inverse.  The ambient direct root system
is 775-dimensional; the gap-root formulation
\((\mathfrak F-de,d)=0\) in \((z,d,\nu)\) is 776-dimensional.  Coefficient
tails and the interval uncertainty of \(T_*\) must also be included.

The exact compatibility obstruction and repaired count are proved in
[the attracting-endpoint audit](fixed-epsilon-selected-attracting-endpoint-chart.md)
and [the Fredholm-structure audit](fixed-epsilon-selected-fredholm-structure.md).
The failure of the scalar exit and the minimum invariant-chart problem are
proved in
[the repelling-endpoint audit](fixed_epsilon_selected_repelling_endpoint.md).
The present entry template still supplies 194 artificial conditions, while
\(G=0\) supplies only one exit condition.  Its accurately solved square
residual therefore remains the wrong endpoint problem.  The actual Fredholm
endpoint operator remains unconstructed.

## 6. Claim ledger

| Claim | Status |
|---|---|
| Actual left/right finite-dimensional candidate | **Computed** |
| Phase condition and full nodewise history jump | **Solved** |
| Discrete full-residual adjoint candidate | **Computed** |
| Mesh and section diagnostics | **Computed** |
| Rank-two endpoint compatibility and raw-compatible dimension correction | **Proved exactly** |
| Repaired ambient \(775\)-by-\(774\) arithmetic ledger | **Proved; operator not assembled** |
| Selected attracting trace chart | **Open** |
| Backward-extendible repelling trace chart | **Open** |
| Global strong-history multicell realization | **Open** |
| Correct one-cokernel Fredholm BVP | **Open** |
| Continuous advanced adjoint and tails | **Open** |
| Interval inverse / radii polynomial | **Open** |
| Fixed-\(\varepsilon\) selected root | **Open** |
| Enclosure \(0\notin\rho_*\) | **Open** |
| Physical onset, capture, or basin statement | **Open** |
