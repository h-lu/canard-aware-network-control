# High-resolution outer periodic orbit for the leaky RFDE

Status: **the 129-node outer polynomial was under-resolved.  A source-bound
resolution ladder identifies 257 nodes as the first practical proof-scale
representation, and the directed finite/tail radii inequality at cutoff 384
validates a nearby phase-fixed periodic RFDE orbit and its bordered
derivative.  No attracting Floquet index is claimed.**

The replay contract is
[`leaky_outer_high_resolution.py`](../src/canard_control/leaky_outer_high_resolution.py),
the generator is
[`autonomous_leaky_recovery_outer_high_resolution.py`](../experiments/autonomous_leaky_recovery_outer_high_resolution.py),
and the tracked body is
[`autonomous_leaky_recovery_outer_high_resolution.json`](../experiments/results/autonomous_leaky_recovery_outer_high_resolution.json).
The equation-level change from the nonleaky validator is proved separately
in [`leaky-periodic-majorant-audit.md`](leaky-periodic-majorant-audit.md).

## 1. Object and claim boundary

The autonomous synchronous equation is

\[
\begin{aligned}
 v'={}&v-\frac{v^3}{3}-w
 +\varepsilon\kappa _1\left(
 \frac{v(t-\tau _0)+v(t-\tau _1)}2-v(t)\right)\\
 &+\varepsilon\kappa _3\left(
 \frac{(v(t-\tau _0)-1)^3+(v(t-\tau _1)-1)^3}{2}
 -(v(t)-1)^3\right),\\
 w'={}&\varepsilon(v-a-w),
\end{aligned}
\]

at

\[
 \varepsilon=\frac15,
 \quad a=\frac14,
 \quad \kappa _1=\frac1{250},
 \quad \kappa _3=\frac1{200},
 \quad (\tau _0,\tau _1)=(4\sqrt5,5\sqrt5).
\]

The floating-point continuation uses the stored binary64 inputs.  The
directed theorem interprets their shortest declared decimal spellings
\(0.2,0.25,4,5,0.004,0.005\) as exact and constructs
\(\tau_j=\theta_j/\sqrt\varepsilon\) by directed interval arithmetic.  Thus
the final existence statement is for the exact parameters displayed above;
the binary64 polynomial is only the center of its correction ball.

The continuation label `outer_pulse` records how the numerical branch was
obtained.  The directed result proves existence of a periodic solution near
that polynomial.  It does **not** yet prove that this solution is attracting,
that it is the large-amplitude attractor seen in time integration, or that
its basin is one side of the physical pulse threshold.  Those conclusions
require the independent Floquet and routing certificates described below.

## 2. Resolution ladder

Each row is independently initialized from the attracting ODE cycle and
continued through the same eleven gain values from zero to one.  The
collocation residual is evaluated at the nodes; the off-grid residual is
evaluated on both \(8n\) and \(16n\) uniform phases.  The two oversampling
factors give the same displayed maxima.

| nodes \(n\) | mandatory cubic cutoff \(3(n-1)/2\) | period | nodal defect | off-grid defect | high-mode diagnostic | bordered \(\sigma_{\min}\) | nodal \(\kappa _2\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 129 | 192 | 26.604416802557541 | \(8.97\times10^{-14}\) | \(3.50870\times10^{-5}\) | \(1.55197\times10^{-6}\) | 0.0975087 | 4407.47 |
| 193 | 288 | 26.604416802558230 | \(1.23\times10^{-13}\) | \(9.84875\times10^{-9}\) | \(2.95073\times10^{-9}\) | 0.109880 | 5739.93 |
| 257 | 384 | 26.604416802557488 | \(1.52\times10^{-13}\) | \(8.12150\times10^{-12}\) | \(4.40300\times10^{-12}\) | 0.118171 | 7036.05 |
| 385 | 576 | 26.604416802556884 | \(3.26\times10^{-13}\) | \(7.26974\times10^{-13}\) | \(1.27888\times10^{-15}\) | 0.128700 | 9584.36 |

The “high-mode diagnostic” is the binary64 sum of Fourier coefficients in
the outer twenty percent of represented modes.  It is not a tail enclosure.
The nodal \(2\)-norm condition number grows with the differentiation matrix,
but the smallest bordered singular value does not collapse.  More
importantly, the off-grid defect drops by about seven orders of magnitude
from 129 to 257 nodes.  A tiny nodal residual at 129 nodes therefore did not
show that the RFDE vector field was resolved between nodes.

On a common 6160-point phase grid, the 257- and 385-node polynomials satisfy

\[
\begin{aligned}
 |T_{257}-T_{385}|&=6.04\times10^{-13},\\
 \|x_{257}-x_{385}\|_\infty&=1.283\times10^{-13},\\
 \|\partial_\theta x_{257}-\partial_\theta x_{385}\|_\infty
 &=9.20\times10^{-12}.
\end{aligned}
\]

Thus 385 nodes are useful as an independent resolution comparison, whereas
257 nodes are the natural directed target: they have already reached the
off-grid \(10^{-11}\) scale, and the required cutoff is 384 rather than 576.

## 3. Directed finite/tail calculation

For the exact 257-node binary64 polynomial, cutoff \(M=384\), 160-bit MPFR
endpoint arithmetic, and radius \(r=10^{-5}\), the directed calculation gives

\[
\begin{aligned}
 Y&<2.57087\times10^{-13},\\
 Z_{PP}&<3.00382\times10^{-8},\\
 Z_{\mathrm{full}}&<0.0812146,\\
 Z_1&<1.60856\times10^4,
 \quad Z_2<1.88002\times10^3,
 \quad Z_3<114.097,\\
 Z_1r+Z_2r^2+Z_3r^3&<0.160856,\\
 q(r)&<0.242071,\\
 r-\{Y+q(r)r\}&>7.57929\times10^{-6}.
\end{aligned}
\]

The finite bordered inverse defect is only about \(3.0\times10^{-8}\).  The
larger point-operator contribution comes from the tail input column:

\[
 Z_{Q\leftarrow P}+Z_{Q\leftarrow Q}<0.081215,
 \qquad
 Z_{Q\leftarrow Q}<0.055494.
\]

This separates the numerical issues cleanly.  The 129-node failure was an
orbit-resolution failure.  At 257 nodes, neither the finite inverse nor the
tail coupling blocks prevent the radii argument; the nonlinear variation is
the largest term at the chosen radius.  Raising the state resolution to 385
nodes is therefore unnecessary for the center-orbit existence proof under
the current norm.

The equation-level leaky-majorant audit proves the only new residual,
Jacobian, finite/tail, and derivative-variation terms relative to the
nonleaky Wiener argument.  Together with the source-locked directed
calculation above, the negative radii polynomial validates a phase-fixed
periodic RFDE solution within the declared coefficient ball and gives the
bordered inverse bound

\[
 \|(D\mathcal F_{\mathrm{bord}})^{-1}\|<92.565.
\]

This is an orbit and bordered-inverse result, not a Floquet-index result.

## 4. What remains for biological pulse control

The following gates remain logically separate:

1. transfer the bordered Fourier kernel statement to algebraic simplicity of
   the unit history-monodromy multiplier;
2. cover the remainder of the unit circle by directed resolvent bounds;
3. compute a directed Riesz or winding count proving zero nontranslation
   unstable multipliers for this branch;
4. validate parameter-dependent extrema and the frequency--amplitude map;
5. prove that the two sides of the physical pulse separator enter the quiet
   and outer attracting neighborhoods.

Until the first three gates close, “outer attracting cycle” remains a
numerical branch interpretation.  The present result removes the more basic
existence and phase-bordered invertibility obstruction.
