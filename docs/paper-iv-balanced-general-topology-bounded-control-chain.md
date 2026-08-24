# A bounded staged control chain on balanced delayed FHN networks

Status: **proved for every finite network in the balanced two-half-delay-layer
class below, on a declared bounded initial-data cylinder and an exact-model
decision tube.** The result combines finite-time complete-history preparation,
positive or negative controlled voltage-threshold onset, a finite controlled
voltage excursion, and two nonzero local target balls for synchronous-branch
frequency, unsquared amplitude, and operational safety.

The periodic outputs are synchronous-branch outputs. They are independent of
the topology inside the declared class because the synchronized restriction is
exactly the tracked scalar RFDE. They are not asynchronous or
arbitrary-history frequency-amplitude outputs, and no attraction of the full
network to that branch is proved.

The executable proof record is
[fhn_balanced_control_chain.py](../src/canard_control/fhn_balanced_control_chain.py),
the generator is
[fhn_balanced_control_chain.py](../experiments/fhn_balanced_control_chain.py),
and the source-bound result is
[fhn_balanced_control_chain.json](../experiments/results/fhn_balanced_control_chain.json).
Its SHA-256 digest is

~~~text
090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9
~~~

The three parent records are pinned to

~~~text
bounded preparation: 8681f800c42420207a94f505b3c8831c7409f3619cf640cbd24de580cd87f548
balanced sign cone:   1dd606d7f4aec1ea857f1c53d4e60106fc2737089b67e989aa7b192fe3ca43fb
amplitude safety:     b9d00edd48c4ae5e61291dfd08fa13d6bb6775acf7f2683b69d3d2838130da36
~~~

The first parent proves bounded preparation only for the tracked rank-one
two-module instance, and the second parent treats its nodewise recovery clamp
as an ideal state constraint. This note does not alter those parent claims.
Sections 3 and 4 supply the missing general-topology authority and bounded
clamp arguments. Similarly, the amplitude-safety parent itself is a
fixed-topology result; Section 6 transfers only its synchronous scalar branch.

## 1. Balanced two-delay network class

Let \(N\ge 1\), let \(\mathbf 1\in\mathbb R^N\), and let
\(P,B_0,B_1\in\mathbb R^{N\times N}\). Assume

\[
 P\ge 0,\qquad P\mathbf 1=\mathbf 1,
\tag{1.1}
\]

and choose a strictly positive row vector \(\pi^T\) such that

\[
 \pi^T\mathbf 1=1,\qquad \pi^TP=\pi^T.
\tag{1.2}
\]

The two delay layers satisfy

\[
 B_\ell\ge 0,\qquad
 B_\ell\mathbf 1=\frac12\mathbf 1,\qquad
 \pi^TB_\ell=\frac12\pi^T,\qquad \ell=0,1.
\tag{1.3}
\]

No irreducibility, primitivity, Dobrushin contraction, symmetry, normality,
rank-one representation, or commutation relation is assumed. Reducible
networks are included whenever a strictly positive stationary weight has been
chosen.

Put

\[
 f(s)=s-\frac{s^3}{3},\qquad h(s)=(s-1)^3,
\tag{1.4}
\]

and fix

\[
 \varepsilon=\frac15,\quad a=\frac35,\quad D=3,\quad E=2,\quad
 \tau_0=4\sqrt5,\quad \tau_1=\tau_*=5\sqrt5.
\tag{1.5}
\]

For gains in the tracked microscopic box, the controlled network is

\[
\begin{aligned}
 \dot v&=F_v(v_t,w)+u^v,\\
 \dot w&=F_w(v,w)+u^w,
\end{aligned}
\tag{1.6}
\]

where all nonlinearities act componentwise and

\[
\begin{aligned}
 F_v(v_t,w)={}&f(v)-w+D(P-I)v\\
 &+\varepsilon\kappa_1
 \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
 \{B_0h(v(t-\tau_0))+B_1h(v(t-\tau_1))-h(v)\},
\end{aligned}
\tag{1.7}
\]

while

\[
 F_w(v,w)=\varepsilon(v-a\mathbf 1)+E(P-I)w.
\tag{1.8}
\]

This is one cross-model class: preparation, decision, and synchronous
periodic stages use the same \(P,B_0,B_1\), parameters, and baseline vector
fields.

## 2. Finite-time preparation on a bounded initial-data cylinder

Let the relevant initial data satisfy

\[
 \|\phi_v\|_\infty\le V_0,\qquad
 \|w(0)\|_\infty\le W_0,\qquad |r|\le R.
\tag{2.1}
\]

This is the declared **bounded initial-data cylinder**. It is not compact in
the RFDE phase-space topology. In fact, closed sup-norm history balls need not
be compact, and the old recovery history is unrestricted because neither
(1.7) nor (1.8) contains delayed recovery. No RFDE phase-space compactness is
used or claimed.

Define componentwise

\[
 \sigma_{1/2}(z)=\operatorname{sgn}(z)\sqrt{|z|}.
\tag{2.2}
\]

During preparation apply the causal additive feedback

\[
\begin{aligned}
 u^v&=-F_v(v_t,w)-K_v\sigma_{1/2}(v-r\mathbf 1),\\
 u^w&=-F_w(v,w)-K_w\sigma_{1/2}(w),
\end{aligned}
\tag{2.3}
\]

with \(K_v,K_w>0\). It uses the current node states and the two delayed
voltage layers. It uses neither future values nor a state overwrite. Exact
cancellation gives, for \(e=v-r\mathbf 1\),

\[
 \dot e_i=-K_v\sigma_{1/2}(e_i),\qquad
 \dot w_i=-K_w\sigma_{1/2}(w_i).
\tag{2.4}
\]

The scalar field in (2.4) is continuous and one-sided Lipschitz, although it
is not locally Lipschitz at zero. Its forward-unique solution is

\[
 z(t)=\operatorname{sgn}(z_0)
 \left(\max\left\{\sqrt{|z_0|}-\frac K2t,0\right\}\right)^2.
\tag{2.5}
\]

Consequently every current node reaches \((r,0)\) by

\[
 T_{\mathrm{set}}\le
 \max\left\{
 \frac{2\sqrt{V_0+R}}{K_v},
 \frac{2\sqrt{W_0}}{K_w}
 \right\}.
\tag{2.6}
\]

Keep (2.3) active until the predetermined release time

\[
 T_{\mathrm{rel}}=\overline T_{\mathrm{set}}+\tau_*.
\tag{2.7}
\]

Then the complete RFDE history is exactly

\[
 \Phi_r(\theta)=(r\mathbf 1,0),\qquad -\tau_*\le\theta\le 0.
\tag{2.8}
\]

Switching (2.3) off may produce a bounded input jump, but the state remains
continuous; no impulse is used.

## 3. Authority uniform in node count and topology

The nonnegative row-mass assumptions imply

\[
 \|P\|_\infty=1,\qquad
 \|B_0\|_\infty=\|B_1\|_\infty=\frac12.
\tag{3.1}
\]

The triangle inequality therefore gives

\[
 \|P-I\|_\infty\le 2,\qquad
 \|B_0\|_\infty+\|B_1\|_\infty=1.
\tag{3.2}
\]

The bound \(2\) is sharp in this class: a directed cycle permutation matrix
with no diagonal entries has \(\|P-I\|_\infty=2\). Thus (3.2) does not hide a
rank-one or large-network limit.

Let \(V=\max\{V_0,R\}\). Formula (2.5) yields

\[
 \|v(t)\|_\infty\le V,\qquad
 \|w(t)\|_\infty\le W_0
\tag{3.3}
\]

during settling and hold. Every delayed voltage is either in the declared
initial voltage-history ball or on the controlled trajectory. Hence the same
bound applies, and \(|h(s)|\le(V+1)^3\). Equations (3.1)--(3.3) give

\[
\begin{aligned}
 \|u^v\|_\infty\le{}&
 V+\frac{V^3}{3}+W_0+2DV
 +2\varepsilon\kappa_1^+V\\
 &+2\varepsilon\kappa_3^+(V+1)^3
 +K_v\sqrt{V_0+R},
\end{aligned}
\tag{3.4}
\]

and

\[
 \|u^w\|_\infty\le
 \varepsilon(V+a)+2EW_0+K_w\sqrt{W_0}.
\tag{3.5}
\]

These are per-node sup-norm bounds, uniform in \(N\) and in every topology
satisfying (1.1)--(1.3). They depend on the declared cylinder radii; there is
no uniform authority over unbounded initial data.

For

\[
 V_0=W_0=2,\qquad R=\frac34,\qquad K_v=K_w=1,
\tag{3.6}
\]

the directed parent endpoints and the universal norm calculation give:

| quantity | directed upper bound |
|---|---:|
| preparation voltage authority | \(23.1849790618559665912241330351\) |
| preparation recovery authority | \(9.9342135623730950488016887243\) |
| state settling time | \(3.3166247903553998491149327367\) |
| maximum-delay hold | \(11.1803398874989484820458683437\) |
| complete-history preparation | \(14.4969646778543483311608010804\) |

The fixed-topology preparation constants therefore transfer without a
topology-dependent loss.

## 4. Bounded recovery cancellation after release

At \(T_{\mathrm{rel}}\), close the voltage preparation feedback:

\[
 u^v=0.
\tag{4.1}
\]

Retain only the additive nodewise recovery cancellation

\[
 u^w=-\{\varepsilon(v-a\mathbf 1)+E(P-I)w\}=-F_w(v,w).
\tag{4.2}
\]

Since preparation gives \(w(T_{\mathrm{rel}})=0\), equation (4.2) yields

\[
 w(t)\equiv 0
\tag{4.3}
\]

throughout the decision stage. On a declared voltage tube
\(\|v(t)\|_\infty\le H\), the actual input along (4.3) satisfies

\[
 \|u^w(t)\|_\infty
 =\varepsilon\|v(t)-a\mathbf 1\|_\infty
 \le\varepsilon(H+a).
\tag{4.4}
\]

For \(H=3/2\), this is at most

\[
 \boxed{
 \|u^w\|_\infty\le
 0.42000000000000000000000000000000000000000000000108108.}
\tag{4.5}
\]

Thus the ideal nodewise zero-recovery constraint used by the balanced
sign-cone theorem is realized by a bounded mathematical additive actuator on
the detector/excursion tube. This is an exact-model cancellation statement.
It is not a hardware, bandwidth, slew-rate, saturation-under-error, or
measurement-noise robustness theorem.

## 5. Controlled threshold onset and finite excursion

Under (4.1)--(4.3), the voltage equation is

\[
 \dot v=f(v)+D(P-I)v+
 \varepsilon\left\{
 \sum_{\ell=0}^1B_\ell G(v(t-\tau_\ell))-G(v)
 \right\},
\tag{5.1}
\]

where

\[
 G(s)=\kappa_1s+\kappa_3(s-1)^3.
\tag{5.2}
\]

This is exactly the model of the pinned balanced sign-cone theorem. Its
positive and negative complete-history orthants are invariant, and the
balanced mean \(x=\pi^Tv\) obeys topology-independent one-sided growth
estimates. The result needs only (1.1)--(1.3), not contraction or
irreducibility.

The two translated target-ball charts have reset projections

\[
 I_+=[0.499999999999,0.500000000001]
\tag{5.3}
\]

and

\[
 I_-=[-0.500000000001,-0.499999999999].
\tag{5.4}
\]

Both are contained in \([-3/4,3/4]\), so preparation applies. The release
history is \(\Phi_r\), and hence lies in the appropriate history orthant. Its
mean magnitude is at least \(0.499999999999\), exceeding the sign-cone
certificate's lower bound \(0.06\) by \(0.439999999999\).

It follows that the positive chart has a nodewise \(+1\) first hit and later
a nodewise \(+3/2\) hit. The negative chart has a nodewise \(-1\) first hit
and later a nodewise \(-6/5\) hit. The detector and excursion nodes need not
be the same. Measured from release, conservative directed deadlines are:

| chart | detector | detector deadline | excursion | excursion deadline |
|---|---:|---:|---:|---:|
| positive | \(+1\) | \(5.902260244961032\) | \(+3/2\) | \(53.64793041518532\) |
| negative | \(-1\) | \(10.16895439798666\) | \(-6/5\) | \(38.40682402081322\) |

Adding the complete-history preparation time gives deadlines from the start
of control:

\[
\begin{array}{c|cc}
 &\text{detector}&\text{excursion}\\ \hline
 +&20.39922492281538&68.14489509303967\\
 -&24.66591907584100&52.90378869866757.
\end{array}
\tag{5.5}
\]

These are controlled voltage-threshold and controlled excursion statements.
They do not identify a biological basin, an action potential, a no-return
surface, or autonomous excitability.

## 6. Synchronous scalar restriction

For arbitrary scalars \(s,q,s_0,s_1\), substitute

\[
 v=s\mathbf 1,\qquad w=q\mathbf 1,\qquad
 v(t-\tau_\ell)=s_\ell\mathbf 1.
\tag{6.1}
\]

Equations (1.1) and (1.3) give

\[
 (P-I)\mathbf 1=0,\qquad
 B_\ell\mathbf 1=\frac12\mathbf 1.
\tag{6.2}
\]

Therefore every component of (1.7)--(1.8) is the same scalar equation:

\[
\begin{aligned}
 \dot s={}&s-\frac{s^3}{3}-q\\
 &+\varepsilon\kappa_1
 \left\{\frac{s_0+s_1}{2}-s\right\}\\
 &+\varepsilon\kappa_3
 \left\{\frac{(s_0-1)^3+(s_1-1)^3}{2}-(s-1)^3\right\},\\
 \dot q={}&\varepsilon(s-a).
\end{aligned}
\tag{6.3}
\]

Thus the synchronized subspace is invariant for every topology in the class,
and its restriction is exactly the tracked two-delay scalar RFDE. The
synchronous periodic branch and its scalar frequency and voltage amplitude
are consequently the same for all such topologies. This algebra proves
existence and topology independence of the branch outputs; it proves neither
transverse stability nor attraction to the branch.

## 7. Frequency-amplitude-operational-safety target balls

Write

\[
 Q_A(\kappa_1,\kappa_3,r)
 =\bigl(F_{\mathrm{sync}},A_{\mathrm{sync}},-r\bigr).
\tag{7.1}
\]

Here \(F_{\mathrm{sync}}\) and \(A_{\mathrm{sync}}\) are computed on the
periodic branch of (6.3), while \(S_{\mathrm{op}}=-r\) is the exact staged
reset coordinate. It is an operational safety output, not an autonomous or
biological safety margin.

For each center

\[
 b_+=\left(0.2,0.25,\frac12\right),\qquad
 b_-=\left(0.2,0.25,-\frac12\right),
\tag{7.2}
\]

the closed Euclidean input ball of radius

\[
 R_{\mathrm{in}}=10^{-12}
\tag{7.3}
\]

has an image under (7.1) containing the closed Euclidean output ball of
radius

\[
 \boxed{
 \rho_{F,A,S}=
 2.75138166016477172021072951467987182906462947064987861
 \times10^{-15}.}
\tag{7.4}
\]

Every target in either output ball has a unique preimage in the corresponding
translated input ball. This uniqueness is in the three scalar inputs
\((\kappa_1,\kappa_3,r)\). No uniqueness of a full-network asynchronous state,
history, or periodic orbit is asserted.

## 8. Main staged theorem

> **Theorem 8.1 (balanced-network bounded staged control chain).**
> Let \(N\ge1\) and let \(P,\pi,B_0,B_1\) satisfy (1.1)--(1.3). Let the
> relevant initial data lie in the bounded initial-data cylinder
> \(\|\phi_v\|_\infty\le2\), \(\|w(0)\|_\infty\le2\). Choose either center
> \(b_+\) or \(b_-\), and choose any target in the corresponding closed
> \((F_{\mathrm{sync}},A_{\mathrm{sync}},S_{\mathrm{op}})\) output ball of
> radius (7.4). Then:
>
> 1. that target has a unique preimage
>    \((\kappa_1,\kappa_3,r)\) in the closed input ball of radius \(10^{-12}\);
> 2. the exact-model additive feedback (2.3), with \(K_v=K_w=1\), creates
>    the exact complete history \(\Phi_r\) no later than the preparation time
>    in Section 3, with the topology-independent authority bounds there;
> 3. after release, \(u^v=0\) and the bounded additive recovery control (4.2)
>    preserve \(w=0\); the positive chart reaches \(+1\) and \(+3/2\), while
>    the negative chart reaches \(-1\) and \(-6/5\), by the deadlines in
>    (5.5);
> 4. the same network possesses the invariant synchronous periodic branch
>    whose \(F_{\mathrm{sync}},A_{\mathrm{sync}}\), together with \(-r\),
>    equal the chosen target.

**Proof.** The parent amplitude-safety result supplies the unique preimage and
keeps its reset projection inside one of (5.3)--(5.4). Equations (3.1)--(3.5)
extend the exact finite-time preparation proof to every topology in the
declared class without changing its public authority or time endpoints.
Equation (2.8) supplies the sign-definite complete history required by the
balanced sign-cone theorem. Equations (4.2)--(4.5) replace that theorem's
ideal recovery constraint by a bounded exact-model additive input on the
whole decision tube. The sign-cone theorem then gives the detector and
excursion hits. Finally, (6.2)--(6.3) identify the synchronized restriction
with the scalar RFDE used by the amplitude-safety parent, so its target-ball
conclusion transfers to the synchronous branch of every declared topology.
\(\square\)

Theorem 8.1 is deliberately staged. It does not prove that the trajectory
which makes the finite excursion subsequently converges to the synchronous
periodic branch. Such a conclusion would require a basin and attraction
theorem that is not presently available.

## 9. Exact claim boundary

The result proves:

- arbitrary finite \(N\) within the balanced two-half-delay-layer class;
- exact-model bounded additive preparation on the declared bounded
  initial-data cylinder, without overwrite or impulse;
- exact complete-history creation in finite time;
- bounded additive nodewise recovery cancellation on the declared decision
  tube;
- nonsynchronous balanced-network controlled onset and finite excursion;
- topology-independent synchronous-branch
  \(F_{\mathrm{sync}},A_{\mathrm{sync}}\);
- two nonzero three-dimensional target balls for
  \((F_{\mathrm{sync}},A_{\mathrm{sync}},S_{\mathrm{op}})\), with unique
  scalar-input preimages.

It does **not** prove:

- compactness of the RFDE phase-space initial set;
- uniform authority over unbounded initial data;
- asynchronous frequency or amplitude outputs;
- transverse or full-network periodic attraction;
- an unforced onset or a maximal-canard onset;
- a biological basin, an action potential, or a no-return theorem;
- general-topology canard-root equivalence;
- robustness to model uncertainty or measurement noise;
- bandwidth, slew-rate, energy, or hardware realizability.

The executable validator treats every item in the second list as false and
rejects a result record that promotes any of them.
