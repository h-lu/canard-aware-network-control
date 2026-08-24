# Bounded additive finite-time preparation of a constant FHN history

Status: **proved on a declared bounded initial-data cylinder for the fixed rank-one
two-module \(D=3,E=2\) FHN network.** Exact causal cancellation of the known
baseline vector field, together with a componentwise square-root reaching
law, brings every current node state to \((r,0)\) in finite time. Continuing
the same bounded additive feedback for one maximum-delay window then creates
the constant complete history \(\Phi_r\) without a state overwrite or an
impulse.

This is an exact-model mathematical actuator theorem, not a hardware theorem.
It requires every current node state and both delayed voltage layers. It does
not prove robustness to model error, noisy measurements, actuator bandwidth,
slew rate, energy limits, or saturation beyond the stated authority bounds.

The executable theorem is
[fhn_bounded_additive_preparation.py](../src/canard_control/fhn_bounded_additive_preparation.py),
the driver is
[fhn_bounded_additive_preparation.py](../experiments/fhn_bounded_additive_preparation.py),
and the directed record is
[fhn_bounded_additive_preparation.json](../experiments/results/fhn_bounded_additive_preparation.json).
Its SHA-256 digest is

~~~text
8681f800c42420207a94f505b3c8831c7409f3619cf640cbd24de580cd87f548
~~~

The source records are the same-model separator

~~~text
9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86
~~~

and the analytic ideal-hold note

~~~text
1f68aed9409bf4e04799903993b77b1d939b7f39e588f887cb54aec7f9aa459e
~~~

The latter proves why a maximum-delay hold creates \(\Phi_r\), but postulates
an ideal overwrite. The present theorem replaces that overwrite on a bounded
initial-data cylinder by an additive input with an explicit
node-count-independent amplitude bound.

## 1. Baseline network and delay norms

Let \(C_1,C_2\) be nonempty modules of arbitrary finite sizes \(n_1,n_2\).
Set

\[
 \pi_i=\frac{1}{2n_a}\quad(i\in C_a),\qquad
 P=\mathbf 1\pi^T.
\tag{1.1}
\]

The nonnegative delay layers \(B_0,B_1\) average, respectively, over the
same and opposite source modules with total row mass \(1/2\). Hence

\[
 B_0+B_1=P,\qquad
 \|P\|_\infty=1,\qquad
 \|B_0\|_\infty=\|B_1\|_\infty=\frac12.
\tag{1.2}
\]

For a row belonging to \(C_a\), the absolute row sum of \(P-I\) is
\(2-1/n_a\). Therefore

\[
 \|P-I\|_\infty
   =2-\frac{1}{\max\{n_1,n_2\}}<2.
\tag{1.3}
\]

The strict inequality depends on the module sizes, while the upper bound
\(2\) does not. All authority estimates below use the latter.

With \(h(s)=(s-1)^3\), define the baseline right-hand sides

\[
\begin{aligned}
 F_v(v_t,w)={}&v-\frac{v^{\circ3}}3-w+3(P-I)v\\
 &+\varepsilon\kappa_1
   \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
   \{B_0h(v(t-\tau_0))+B_1h(v(t-\tau_1))-h(v)\},
\end{aligned}
\tag{1.4}
\]

and

\[
 F_w(v,w)=\varepsilon(v-a\mathbf1)+2(P-I)w.
\tag{1.5}
\]

Here

\[
 \varepsilon=\frac15,\qquad a=\frac35,\qquad
 \tau_0=4\sqrt5,\qquad \tau_1=\tau_*=5\sqrt5,
\tag{1.6}
\]

and the gains lie in the microscopic box bound to the separator artifact.

## 2. Bounded initial-data cylinder and additive controller

Let the initial voltage history and current recovery state satisfy

\[
 \|\phi_v\|_\infty\le V_0,\qquad
 \|w(0)\|_\infty\le W_0,
\tag{2.1}
\]

and choose \(|r|\le R\le1\). These inequalities define the bounded data
cylinder used below. They do **not** make a compact subset of the
infinite-dimensional RFDE phase space: closed sup-norm balls in a history
space are not compact without additional regularity, and the old recovery
history is deliberately unrestricted. No phase-space compactness is used in
the proof. No bound on that old recovery history is needed because neither
(1.4) nor (1.5) contains delayed recovery. Define

\[
 \sigma_{1/2}(z)=\operatorname{sgn}(z)\sqrt{|z|}
\tag{2.2}
\]

componentwise. For \(K_v,K_w>0\), apply during preparation

\[
\begin{aligned}
 u^v(t)&=-F_v(v_t,w)
         -K_v\sigma_{1/2}(v-r\mathbf1),\\
 u^w(t)&=-F_w(v,w)-K_w\sigma_{1/2}(w).
\end{aligned}
\tag{2.3}
\]

This is an additive input: the state is not reassigned at \(t=0\). It is
causal because at time \(t\) it uses only \(v(t)\), \(w(t)\),
\(v(t-\tau_0)\), and \(v(t-\tau_1)\), together with the known matrices and
parameters. It requires all current node states and both delayed voltage
layers, but neither future values nor a recovery-history measurement.

Exact algebraic cancellation in (2.3) gives, with
\(e=v-r\mathbf1\),

\[
 \dot e_i=-K_v\sigma_{1/2}(e_i),\qquad
 \dot w_i=-K_w\sigma_{1/2}(w_i).
\tag{2.4}
\]

Thus preparation destroys neither causality nor the initial history; it
cancels its instantaneous effect on the known vector field.

## 3. Forward uniqueness and exact settling

The map \(\sigma_{1/2}\) is continuous and increasing, although it is not
locally Lipschitz at zero. Consequently, for
\(f_K(x)=-K\sigma_{1/2}(x)\),

\[
 (x-y)\{f_K(x)-f_K(y)\}\le0.
\tag{3.1}
\]

If \(x_1,x_2\) are two Carathéodory solutions with the same initial value,
then

\[
 \frac{d}{dt}|x_1-x_2|^2
 =2(x_1-x_2)\{f_K(x_1)-f_K(x_2)\}\le0
\tag{3.2}
\]

almost everywhere. Hence the solution is forward unique. This monotonicity
argument is essential: invoking local Lipschitz continuity at zero would be
false. Backward uniqueness from the settled state is not asserted.

The forward solution is explicit:

\[
 x(t)=\operatorname{sgn}(x_0)
 \left(\max\left\{\sqrt{|x_0|}-\frac K2t,0\right\}\right)^2.
\tag{3.3}
\]

It reaches zero by \(2\sqrt{|x_0|}/K\) and remains there. Since

\[
 \|e(0)\|_\infty\le V_0+R,
\tag{3.4}
\]

all nodes reach \((r,0)\) no later than

\[
 \overline T_{\mathrm{set}}
 =\max\left\{
 \frac{2\sqrt{V_0+R}}{K_v},
 \frac{2\sqrt{W_0}}{K_w}
 \right\}.
\tag{3.5}
\]

There is no need for ideal event detection. Keep the same controller active
until the predetermined release time

\[
 T_{\mathrm{rel}}
 =\overline T_{\mathrm{set}}+\tau_*.
\tag{3.6}
\]

Equation (3.3) shows that \(v=r\mathbf1,w=0\) throughout
\([\overline T_{\mathrm{set}},T_{\mathrm{rel}}]\). Therefore, for every
\(-\tau_*\le\theta\le0\),

\[
 (v,w)(T_{\mathrm{rel}}+\theta)=(r\mathbf1,0),
\tag{3.7}
\]

so the release history is exactly \(\Phi_r\). Switching the preparation
input off at \(T_{\mathrm{rel}}\) may create a bounded input jump, but the
state remains continuous and no impulse is used.

## 4. Node-count-independent authority

Put \(V=\max\{V_0,R\}\). The explicit solution (3.3) implies

\[
 \|v(t)\|_\infty\le V,\qquad
 \|w(t)\|_\infty\le W_0
\tag{4.1}
\]

throughout settling and hold. Every delayed voltage is either part of the
initial history or part of this controlled trajectory, so it satisfies the
same bound. Moreover,

\[
 |h(s)|=|s-1|^3\le(V+1)^3\qquad(|s|\le V).
\tag{4.2}
\]

Using (1.2)--(1.3), the additive voltage authority satisfies

\[
\begin{aligned}
 \|u^v(t)\|_\infty\le{}&
 V+\frac{V^3}{3}+W_0+2DV\\
 &+2\varepsilon\kappa_1^+V
 +2\varepsilon\kappa_3^+(V+1)^3
 +K_v\sqrt{V_0+R},
\end{aligned}
\tag{4.3}
\]

where \(D=3\) and \(\kappa_j^+\) are the directed gain-box upper endpoints.
Similarly,

\[
 \|u^w(t)\|_\infty
 \le\varepsilon(V+a)+2EW_0+K_w\sqrt{W_0},
\qquad E=2.
\tag{4.4}
\]

These are per-node sup-norm bounds independent of \(n_1,n_2\). They grow
with the declared cylinder radii; no uniform authority is claimed over
unbounded initial data.

## 5. Directed numerical instance

For

\[
 V_0=W_0=2,\qquad R=\frac34,\qquad K_v=K_w=1,
\tag{5.1}
\]

160-bit MPFR directed arithmetic gives:

| quantity | directed upper bound | declared safe ceiling |
|---|---:|---:|
| voltage authority | \(23.1849790618559665912241330351\) | \(23.19\) |
| recovery authority | \(9.9342135623730950488016887243\) | \(9.94\) |
| state settling time | \(3.3166247903553998491149327367\) | — |
| maximum-delay hold | \(11.1803398874989484820458683437\) | — |
| complete-history preparation | \(14.4969646778543483311608010804\) | \(14.50\) |

The voltage authority decomposes into directed upper contributions from the
intrinsic, recovery, scaffold, linear-delay, cubic-delay, and reaching terms.
The tracked record stores each contribution separately so that changing a
gain endpoint or an operator norm cannot silently preserve the total.

## 6. Optional nodewise recovery continuation

After preparation, two distinct recovery-control routes are available.

The separator artifact uses the collective clamp

\[
 u^w_{\mathrm{coll}}
 =-\varepsilon(\pi^Tv-a)\mathbf1,
\tag{6.1}
\]

which fixes the collective recovery coordinate and retains its certified
fixed-topology transverse dynamics.

Alternatively, retain only the exact nodewise recovery cancellation

\[
 u^w_{\mathrm{node}}
 =-\{\varepsilon(v-a\mathbf1)+E(P-I)w\}.
\tag{6.2}
\]

Do not continue the voltage cancellation. Then the decision-stage equations
are

\[
 \dot v=F_v(v_t,w),\qquad \dot w=0.
\tag{6.3}
\]

Starting from the prepared state \(w=0\), every recovery coordinate remains
zero exactly. Conditional on a declared decision tube

\[
 \|v(t)\|_\infty\le H,
\tag{6.4}
\]

the required nodewise recovery authority is

\[
 \|u^w_{\mathrm{node}}(t)\|_\infty
 \le\varepsilon(H+a).
\tag{6.5}
\]

For \(H=1.5\), the directed upper bound is
\(0.4200000000000000000000000000000000000000000000011\).
This optional route supplies an exact bounded nodewise zero-recovery clamp
for the fixed model. It is stated separately from the collective clamp and
does not prove a general-topology sign-cone theorem. It still requires exact
state and model information.

## 7. Scope and refusal rules

The executable theorem refuses a mismatched separator artifact, a changed
causal-hold note, a different model or scaffold, a reset outside
\([-1,1]\), a negative or nonfinite declared bound, or a nonpositive reaching
gain.
The result proves:

- bounded additive finite-time state preparation on the declared bounded
  initial-data cylinder;
- exact production of \(\Phi_r\) after a scheduled maximum-delay hold;
- causal use of current full state and the two delayed voltage layers;
- forward Carathéodory uniqueness despite the non-Lipschitz square root;
- node-count-independent input-amplitude bounds; and
- the optional conditional nodewise recovery continuation (6.2).

It does not prove RFDE phase-space compactness, bounded bandwidth, slew rate,
energy, model mismatch, measurement noise, hardware implementation, a uniform
controller over unbounded initial sets, general network topology, unforced or
maximal-canard onset, periodic attraction, or closure of issue 15.

Reproduce the record with

~~~bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_bounded_additive_preparation.py
~~~

and run the hostile tests with

~~~bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_bounded_additive_preparation.py
~~~
