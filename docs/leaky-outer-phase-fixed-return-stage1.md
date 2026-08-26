# Direct phase-fixed outer return: Stage 1

Status: **source-bound pilot and executable proof contract, not an attraction
theorem.**  The exact outer RFDE orbit and its translation identity are
inherited at nested orbit radius (10^{-8}).  Four binary64 finite sections
strongly indicate that the phase-fixed one-return map is a contraction, but
finite sampled histories do not bound the operator on arbitrary continuous
histories.

The executable source is
[the Stage-1 contract](../src/canard_control/leaky_outer_phase_fixed_return_stage1.py),
the generator is
[the experiment](../experiments/leaky_outer_phase_fixed_return_stage1.py),
and the tracked output is
[the result](../experiments/results/leaky_outer_phase_fixed_return_stage1.json).

## Pilot

Let (M_n) be the existing finite monodromy matrix.  The pilot uses the
stored Fourier-orbit tangent (q=dot X_o), not a numerically selected unit
eigenvector.  For the physical current-voltage row

\[
 \ell(h)=\frac{h_v(0)}{\dot V_o(0)},\qquad \ell(q)=1,
\]

it forms ((I-q\otimes\ell)M_n) and restricts its input and output to
(h_v(0)=0).  At (n=120,180,240,360), the spectral radius settles near
(0.0219505), the induced matrix infinity norm lies near
(0.126)--(0.127), and the two-return norm near (0.00278).  The algebraic
projection annihilates the stored tangent to binary64 roundoff.  These are
diagnostics only: the RK4 matrix samples and interpolates the input history.
The fixed-time and rank-one correction matrices separately have infinity norm
about (2.74)--(2.76), while their signed difference has norm below
(0.127).  This is why a rigorous kernel proof must subtract signed measures
before taking total variation; a triangle bound on the two pieces cannot
close.

## Continuous-history route

Use the reduced history space

\[
 Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R,
 \qquad \|(h_v,h_w(0))\|_Y=
 \max\{\|h_v\|_\infty,|h_w(0)|\}.
\]

For every time (t), represent the linear variational solution by signed
measures on the *uninterpolated* input history:

\[
\begin{aligned}
 u(t)&=\alpha_v(t)h_w(0)+\int h_v(\theta)\,d\mu_t(\theta),\\
 w(t)&=\alpha_w(t)h_w(0)+\int h_v(\theta)\,d\nu_t(\theta).
\end{aligned}
\]

The measure-valued method of steps obeys

\[
 \dot\mu_t=a(t)\mu_t-\nu_t
 +b_0(t)\mu_{t-\tau_0}+b_1(t)\mu_{t-\tau_1},
 \qquad
 \dot\nu_t=\varepsilon(\mu_t-\nu_t),
\]

and the same recurrence for the scalar coefficients.  Initially the voltage
history is represented by its Dirac evaluation atoms and recovery by the
independent scalar coefficient.  Thus the construction covers every member
of (C^0); it does not require a modulus of continuity or a nodal
interpolation estimate.

At return, perform the time correction as a **signed measure subtraction**:

\[
 \widetilde\mu_{\theta}
 =\mu_{T+\theta}
 -\frac{q_v(\theta)}{q_v(0)}\mu_T,
 \qquad -5\sqrt5\leq\theta\leq0,
\]

with the analogous scalar coefficient and recovery row.  Only after this
neutral-direction cancellation is total variation bounded.  Since inputs on
the section satisfy (h_v(0)=0), the Dirac mass at zero is removed exactly.
The two continuous-history row norms are therefore

\[
 Q_v=\sup_\theta\bigl(\operatorname{TV}\widetilde\mu_\theta
       +|\widetilde\alpha_v(\theta)|\bigr),qquad
 Q_w=\operatorname{TV}\widetilde\nu_T+|\widetilde\alpha_w(T)|.
\]

A directed interval-Taylor or Bernstein implementation must propagate the
atoms and signed densities, enclose the exact-orbit coefficient error, and
control the cellwise total variation and quadrature remainder.  Bounding
fixed-time and phase-correction norms separately is discouraged because it
throws away the decisive signed cancellation.

## The single closing inequality

On a section ball of radius (r_o=10^{-4}), a second-variational kernel
enclosure must prove

\[
 \|DP_o(z)-DP_o(0)\|\leq C_{DP}\|z\|.
\]

After validating the unique first positive return and its event speed on the
same tube, the entire local contraction gate is

\[
 \boxed{\max\{Q_v,Q_w\}+C_{DP}\,10^{-4}<1.}
\]

The registered adapter leaves (Q_v,Q_w,C_{DP}), and the validated tube
radius null.  Hence the continuous-history derivative contraction,
nonlinear attracting tube, outer capture, and physical pulse onset all remain
false.  The large finite-section margin makes this route promising; it does
not make it proved.

## Ambient pulse distance is a separate gate

A pulse enclosure normally supplies an ambient complete-history distance
(d_X) to the exact phase-zero outer orbit; it does **not** put the pulse
history on the exact phase section.  The normalized event row and rank-one
correction above must therefore also validate a nonlinear phase chart
(Pi_o) with Lipschitz norm (Q_{\rm phase}).  Only then may one infer the
section distance bound

\[
 \|\Pi_o(H_{\rm pulse})-X_o(0)\|_Y
 \leq Q_{\rm phase}d_X.
\]

Entry into the contraction ball is the independent strict inequality

\[
 \boxed{Q_{\rm phase}d_X<r_{\rm section}.}
\]

The artifact records this as a second executable evaluator, with both inputs
null.  In particular, a sampled voltage crossing or a distance to the stored
Fourier polynomial is not silently promoted to an exact section entry.
