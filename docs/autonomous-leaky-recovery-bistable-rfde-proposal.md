# An autonomous leaky-recovery RFDE program for physical pulse onset

Status: **the quiet equilibrium, two distinct phase-fixed periodic RFDE
orbits and their bordered inverses, and the oriented pulse-to-history curve
are proved.  The Floquet indices, stable separator, physical-pulse onset
surface, and three-output inverse remain open.**  This note originated as a
replacement proposal for the reference slice whose synchronous rest state was
proved unstable.  Its older binary64 diagnostics are retained below with
their original claim boundary; the later directed promotions are linked
explicitly.

The executable probe is
[autonomous_leaky_recovery_bistable_probe.py](../experiments/autonomous_leaky_recovery_bistable_probe.py),
and its generated record is
[autonomous_leaky_recovery_bistable_probe.json](../experiments/results/autonomous_leaky_recovery_bistable_probe.json).
The exact equilibrium certificate and immutable claim ledger are in
[autonomous_leaky_recovery_bistable.py](../src/canard_control/autonomous_leaky_recovery_bistable.py),
with hostile mutation and byte-replay checks in
[test_autonomous_leaky_recovery_bistable.py](../tests/test_autonomous_leaky_recovery_bistable.py).

## 1. Decision and minimality

Keep the delayed FHN voltage equation and replace only the recovery law by a
leaky recovery channel:

\[
\begin{aligned}
 \dot v={}&v-\frac{v^3}{3}-w
 +\varepsilon\kappa _1
 \left\{\frac{v(t-\tau _0)+v(t-\tau _1)}2-v\right\}\\
 &+\varepsilon\kappa _3
 \left\{\frac{H(v(t-\tau _0))+H(v(t-\tau _1))}{2}-H(v)\right\},\\
 \dot w={}&\varepsilon(v-a-w),
 \qquad H(v)=(v-1)^3.
\end{aligned}
\tag{1.1}
\]

The candidate center is

\[
 \boxed{
 \varepsilon=\frac15,\quad a=\frac14,\quad
 \kappa _1=\frac1{250},\quad \kappa _3=\frac1{200},\quad
 (\tau _0,\tau _1)=(4\sqrt5,5\sqrt5).}
\tag{1.2}
\]

Relative to the failed reference slice, (1.1) makes three changes: it adds
the single term \(-\varepsilon w\) to recovery, moves \(a\) from \(3/5\) to
\(1/4\), and reduces the two delayed gains.  The delayed nonlinearities,
physical delays, voltage cubic, and two-output periodic architecture are
unchanged.  The gain reduction is not cosmetic: at the old gains the
leaky-recovery equilibrium remains stable, but direct integration sends the
tested large histories to rest and supplies no attracting pulse cycle.

The model is autonomous.  A finite stimulus used below acts only on a fixed
interval \(0\le t\le1\); after \(t=1\) the vector field is exactly (1.1).
Thus eventual rest or pulse capture is a basin statement for one autonomous
RFDE, not a detector latch, reset policy, or post-event parameter switch.

## 2. A proved quiet equilibrium

Constant histories annihilate both delayed-difference channels.  At \(b=1\)
in the recovery law, an equilibrium satisfies

\[
 w=v-a=v-\frac{v^3}{3},
 \qquad v^3=3a=\frac34.
\tag{2.1}
\]

Hence there is exactly one real equilibrium,

\[
 E_q=(\alpha,\alpha-\tfrac14),
 \qquad \alpha=(3/4)^{1/3}.
\tag{2.2}
\]

Put

\[
 C=\varepsilon\{\kappa _1+3\kappa _3(\alpha-1)^2\},
 \qquad A=1-\alpha^2-C,
\tag{2.3}
\]

and

\[
 E(\lambda)=\frac{e^{-\tau _0\lambda}+e^{-\tau _1\lambda}}2.
\tag{2.4}
\]

The characteristic determinant at \(E_q\) is

\[
 \Delta(\lambda)
 =\{\lambda-A-CE(\lambda)\}(\lambda+\varepsilon)+\varepsilon.
\tag{2.5}
\]

Remove the delayed term and write

\[
 p(\lambda)=(\lambda-A)(\lambda+\varepsilon)+\varepsilon.
\tag{2.6}
\]

For \(r=\omega^2\), direct expansion gives

\[
\begin{aligned}
 D(r)
 &:={}|p(i\omega)|^2-C^2|i\omega+\varepsilon|^2\\
 &=r^2+\beta r+\gamma,
\end{aligned}
\tag{2.7}
\]

where

\[
\begin{aligned}
 \beta&=(\varepsilon-A)^2-2\varepsilon(1-A)-C^2,\\
 \gamma&=\varepsilon^2\{(1-A)^2-C^2\}.
\end{aligned}
\tag{2.8}
\]

The rational enclosure

\[
 \frac{1817}{2000}<\alpha<\frac{4543}{5000}
\tag{2.9}
\]

follows by cubing both endpoints.  Exact rational interval arithmetic then
gives

\[
\begin{array}{rcl}
 0.00082506188&<&C<0.00082511675,\\
 0.17362092325&<&A<0.17380268812,\\
 0.02619731188&<&\varepsilon-A,\\
 -0.32986601237&<&\beta<-0.32978374978,\\
 0.02730405269&<&\gamma,\\
 0.00040462465&<&4\gamma-\beta^2.
\end{array}
\tag{2.10}
\]

Because \(\beta<0\), the last two inequalities imply

\[
 \min_{r\ge0}D(r)=\gamma-\frac{\beta^2}{4}>0.
\tag{2.11}
\]

> **Proposition 2.1 (delay-independent quiet-state stability).**  At
> (1.2), the unique equilibrium \(E_q\) is locally exponentially stable for
> every pair of positive delays \(\tau _0,\tau _1\).

**Proof.**  The coefficients of \(p\) are

\[
 \varepsilon-A>0,
 \qquad \varepsilon(1-A)>0,
\tag{2.12}
\]

so \(p\) is Hurwitz.  Equations (2.7)--(2.11) show on the imaginary axis
that

\[
 \left|\frac{C(\lambda+\varepsilon)}{p(\lambda)}\right|<1.
\tag{2.13}
\]

The rational function in (2.13) is stable and proper, so its supremum on
the closed right half-plane is attained on the imaginary boundary.  Also
\(|E(\lambda)|\le1\) there.  Consequently the homotopy

\[
 p(\lambda)-sC(\lambda+\varepsilon)E(\lambda),
 \qquad 0\le s\le1,
\tag{2.14}
\]

has no imaginary-axis zero.  On large right half-disks the quadratic term
dominates uniformly in \(s\); the argument principle therefore preserves
the zero count from \(p\) to \(\Delta\).  Thus \(\Delta\) has no zero in
\(\operatorname{Re}\lambda\ge0\).  The linearized-stability principle for
retarded equations gives local exponential stability. \(\square\)

All signs in this proposition are exact.  The proposition is not a claim
about the periodic or global dynamics.  Its strict margins also imply, by
continuity, a non-explicit open parameter neighborhood on which the quiet
equilibrium remains stable.

## 3. Periodic branches: numerical discovery and directed promotion

The zero-delay-gain ODE at the same \((a,\varepsilon)\) has two numerically
resolved periodic orbits surrounding \(E_q\).  Its outer orbit has period
\(25.6059596862\).  The inner orbit has period \(18.0438321484\); a scalar
Poincare section gives return derivative \(1.922834524\), consistent with an
unstable-cycle candidate.  Calling this orbit a basin separator would
require a history-space argument that the diagnostics below do not supply.

Fourier continuation from zero gain to (1.2), at 129 nodes, produces the
following RFDE candidates.

| candidate | period | voltage amplitude | oversampled defect | leading nontranslation multiplier |
|---|---:|---:|---:|---:|
| outer pulse | \(26.6044168026\) | \(3.2860250879\) | \(3.51\times10^{-5}\) | \(-0.02195063\) |
| inner saddle candidate | \(18.1862099491\) | \(0.7706442669\) | \(1.28\times10^{-13}\) | \(2.01045399\) |

The finite monodromy discretizations at 120, 180, and 240 time steps show:

- for the outer cycle, zero nontranslation multipliers outside the unit
  disk and a neutral-multiplier error decreasing to \(6.22\times10^{-6}\);
- for the inner cycle, exactly one nontranslation multiplier outside the
  unit disk and a neutral-multiplier error decreasing to
  \(1.47\times10^{-7}\).

These are coherent convergence diagnostics, not directed Floquet counts.
The original outer collocation tail is visibly less resolved than the inner
one; a radii-polynomial proof must enclose that tail rather than quote the
nodal residual.

That existence gate has subsequently been closed.  An independent audit of
the leaky recovery majorants, followed by source-bound MPFR endpoint
calculations, validates the 129-node inner polynomial at cutoff 192.  A fresh
129/193/257/385-node outer ladder resolves the old aliasing defect and
validates the 257-node outer polynomial at cutoff 384.  Both calculations
prove a nearby phase-fixed periodic RFDE orbit and its bordered inverse.  See
[the finite/tail contract](leaky-periodic-finite-tail-floquet-contract.md),
[the majorant audit](leaky-periodic-majorant-audit.md), and
[the outer high-resolution artifact](leaky-outer-high-resolution-artifact.md).
They do not prove either Floquet index or either basin interpretation.

### 3.1 The physical-pulse curve and its numerical separator target

Start from the equilibrium history and apply a rectangular current to the
voltage equation,

\[
 u_J(t)=
 \begin{cases}
 J,&0\le t\le1,\\
 0,&t>1.
 \end{cases}
\tag{3.1}
\]

After \(t=1\), the evolution is autonomous.  Binary64 method-of-steps
integration through \(t=800\) gives

\[
\begin{array}{c|c|c}
 J&\text{voltage amplitude on }[650,800]&\text{observed destination}\\ \hline
 0.30&5.64\times10^{-4}&E_q,\\
 0.32&3.28602&\Gamma_p.
\end{array}
\tag{3.2}
\]

Thus \([0.30,0.32]\) is a numerical onset bracket for a finite physical
stimulus.  It is not yet a proof of endpoint basin inclusion, a unique
threshold, or monotonicity in \(J\).

Because both delays exceed the pulse duration, delayed slots remain at the
quiet equilibrium throughout \(0\le t\le1\).  The pulse stage therefore
reduces exactly to a smooth parameter ODE.  Its stimulus variational equation
proves that the complete terminal-history map
\(J\mapsto K(J)\in C([-5\sqrt5,0],\mathbb R^2)\) is injective and positively
oriented on the newly written history segment.  A separate three-mesh,
three-return finite-section calculation finds
\(J_{\rm sep}^{\rm num}\simeq0.301135337086902\), with multiplier-scaled
derivative near \(-3.449\).  See
[the terminal-history theorem](leaky-pulse-terminal-history.md) and
[the separator candidate](leaky-pulse-separator-candidate.md).  The latter is
not a directed Floquet covector, stable-manifold intersection, routing proof,
or onset theorem.

For comparison, the constant-history family

\[
 \Phi_I(\theta)=(\alpha+I,\alpha-\tfrac14),
 \qquad -\tau _1\le\theta\le0,
\tag{3.3}
\]

has the same numerical bracket \(I\in[0.30,0.32]\).  This agreement is useful
for constructing an isolating block, but (3.3) is not substituted for the
finite pulse (3.1) in the theorem below.

## 4. The autonomous onset theorem to prove

Let \(\xi=(a,\kappa_3)\), keep \(\varepsilon,\kappa_1\) and the two delays
fixed, and denote
by \(K_{\xi}(J)\) the complete history at \(t=1\) created by (3.1) from the
quiet equilibrium history.  For every fixed \(J\), all forcing is zero after
that history is created.

The following hypotheses are the exact remaining validation contract.

1. **Two periodic BVPs.**  On a closed box \(U\) about
   \((1/4,1/200)\), there are \(C^1\) phase-fixed branches
   \(\Gamma_p(\xi)\) and \(\Gamma_u(\xi)\), with simple voltage extrema.
2. **Floquet indices.**  The pulse branch has a simple multiplier one and
   no other multiplier on or outside the unit circle.  The inner branch has
   a simple multiplier one, exactly one real multiplier outside the unit
   circle, and every remaining multiplier strictly inside it.
3. **History-space isolating and routing block.**  In the RFDE phase space
   \(X=C([-\tau _1,0],\mathbb R^2)\), a parameterized Conley block
   \(N_\xi\) isolates \(\Gamma_u(\xi)\).  A local pulse-history tube
   \(\mathcal T_\xi\subset N_\xi\) is cut into exactly two components by
   \(W^s_{\mathrm{loc}}(\Gamma_u(\xi))\).  Within the same history-space
   block, there is no other complete invariant set relevant to this local
   routing: every orbit on one designated side enters a certified local
   attracting neighborhood of \(E_q\), and every orbit on the other side
   enters one of \(\Gamma_p\).  The histories \(K_\xi(0.30)\) and
   \(K_\xi(0.32)\) are certified on the respective sides.  A validated
   finite-dimensional invariant-graph reduction is an acceptable route
   only if its block and routing statements are pulled back to \(X\).
4. **Physical-pulse transversality.**  On a neighborhood of
   \((\xi_0,J_c)\), the terminal-history map
   \((\xi,J)\mapsto K_\xi(J)\in X\) is \(C^1\).  There are a common
   history neighborhood \(\mathcal V\subset X\) and a jointly \(C^1\) map
   \[
    h:U\times\mathcal V\longrightarrow\mathbb R
   \]
   such that \(h_\xi(\phi):=h(\xi,\phi)\) is a defining function for
   \(W^s_{\mathrm{loc}}(\Gamma_u(\xi))\cap\mathcal V\), normalized so that
   \(h_\xi<0\) on the quiet component of hypothesis 3 and \(h_\xi>0\) on
   its pulse component.  For some \(J_c\in(0.30,0.32)\),
   \[
    h_{\xi_0}(K_{\xi_0}(J_c))=0,
    \qquad
    \partial_J\{h_{\xi_0}(K_{\xi_0}(J))\}_{J=J_c}>0.
   \tag{4.1}
   \]
5. **Periodic response.**  For frequency \(F=T_p^{-1}\) and unsquared
   voltage amplitude \(A_p=V_{\max}-V_{\min}\),
   \[
    \det D_{(a,\kappa_3)}(F,A_p)(\xi_0)\ne0.
   \tag{4.2}
   \]

> **Theorem 4.1 (candidate: autonomous onset and three-output control).**
> Under hypotheses 1--5, after shrinking \(U\) and choosing an interval
> \(I\) about the center crossing, there is a unique \(C^1\) threshold
> \(J_c(\xi)\in I\).  For all \((\xi,J)\in U\times I\) whose terminal
> history lies in the fixed local pulse-history tube of hypothesis 3,
> \[
> \begin{cases}
> J<J_c(\xi)&\Longrightarrow K_\xi(J)\in\mathcal B(E_q(\xi)),\\
> J>J_c(\xi)&\Longrightarrow K_\xi(J)\in\mathcal B(\Gamma_p(\xi)).
> \end{cases}
> \tag{4.3}
> \]
> Define the signed local stimulus margin
> \[
> S(\xi,J)=J-J_c(\xi).
> \tag{4.4}
> \]
> Then
> \[
> \mathcal Q(a,\kappa_3,J)
> =\bigl(F(a,\kappa_3),A_p(a,\kappa_3),S(a,\kappa_3,J)\bigr)
> \tag{4.5}
> \]
> is a local \(C^1\) diffeomorphism.  Hence frequency, voltage amplitude,
> and signed local stimulus margin from physical pulse onset are locally
> independently controllable.

The proof is short once the five hard validation blocks exist.  Hyperbolic
continuation gives the two cycles and the stable manifold of the inner one.
The history-space Conley block and its certified routing identify the two
local components of the pulse-history tube with the two physical basins.
Stable-manifold transversality and the implicit-function theorem give
\(J_c(\xi)\).  Finally,

\[
 D\mathcal Q=
 \begin{pmatrix}
 F_a&F_{\kappa_3}&0\\
 (A_p)_a&(A_p)_{\kappa_3}&0\\
 -(J_c)_a&-(J_c)_{\kappa_3}&1
 \end{pmatrix},
\qquad
 \det D\mathcal Q
 =\det D_{(a,\kappa_3)}(F,A_p).
\tag{4.6}
\]

No derivative of the onset surface is needed to prove invertibility.

The 129-node centered-difference candidate is

\[
 D_{(a,\kappa_3)}(F,A_p)\approx
 \begin{pmatrix}
 -0.36999533&-0.29363660\\
 -9.06427918&-10.20513397
 \end{pmatrix},
\tag{4.7}
\]

with determinant \(1.11424778\) and singular values approximately
\(13.6573\) and \(0.0815861\).  This has a useful numerical margin, but it is
not yet the directed inequality (4.2).

## 5. Finite-network lift

The corresponding balanced finite network is

\[
\begin{aligned}
 \dot v={}&f(v)-w+3(Q-I)v
 +\varepsilon\kappa_1
 \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
 \{B_0H(v(t-\tau_0))+B_1H(v(t-\tau_1))-H(v)\},\\
 \dot w={}&\varepsilon(v-a\mathbf1-w)+2(Q-I)w,
\end{aligned}
\tag{5.1}
\]

Here all scalar nonlinearities act componentwise and

\[
 f(s)=s-\frac{s^3}{3},\qquad H(s)=(s-1)^3.
\tag{5.2}
\]

Assume

\[
 Q\mathbf1=\mathbf1,\quad \pi^TQ=\pi^T,
 \quad B_j\mathbf1=\tfrac12\mathbf1,
 \quad \pi^TB_j=\tfrac12\pi^T,
\tag{5.3}
\]

with nonnegative matrices and Dobrushin gap

\[
 \tau(Q)\le1-\gamma,\qquad \gamma\ge\frac12.
\tag{5.4}
\]

The synchronous restriction of (5.1) is exactly the scalar model (1.1).
Consequently, if the scalar rest and two cycles are validated, they lift as
synchronous network objects; the physical pulse lifts when the same stimulus
is applied at every node.  There is also a candidate transverse estimate.  If
an enclosed synchronous orbit satisfies

\[
 |V(t)-1|\le\frac52,
\tag{5.5}
\]

then

\[
 \beta_d
 :=\varepsilon\sup_t\{\kappa_1+3\kappa_3(V(t)-1)^2\}
 \le0.01955,
\tag{5.6}
\]

and the instantaneous voltage coefficient is at most

\[
 a_v^+\le1-\varepsilon\kappa_1=0.9992.
\tag{5.7}
\]

For the weighted transverse oscillation norm

\[
 M(t)=\max\{\|x(t)\|_{\rm osc},3\|y(t)\|_{\rm osc}\},
\tag{5.8}
\]

the standard matrix-measure calculation gives

\[
 D^+M(t)\le-\alpha M(t)
 +\beta_d\sup_{t-\tau_1\le s\le t}M(s),
\tag{5.9}
\]

where

\[
\begin{aligned}
 \alpha_v&=3\gamma-a_v^+-\frac13\ge0.167466\ldots,\\
 \alpha_w&=2\gamma+\varepsilon-3\varepsilon\ge0.6,\\
 \alpha&=\min\{\alpha_v,\alpha_w\}>\beta_d.
\end{aligned}
\tag{5.10}
\]

Conditional on both a rigorous matrix-measure derivation of (5.9) and a
directed replacement of (5.5), Halanay gives dimension-independent
transverse exponential decay.  The resulting target indices for every fixed
admitted finite network are zero unstable directions at \(E_q\) and
\(\Gamma_p\), and one collective unstable direction at \(\Gamma_u\).

This does not yet prove a dimension-uniform basin-tube radius.  That requires
uniform nonlinear stable-manifold and isolating-block estimates, not only
the linear Halanay margin.

## 6. Canard compatibility of the leaky slice

The leak does not destroy the singular fold, but it changes the correct
unfolding center.  Put

\[
 \varepsilon=\delta^2,
 \quad v=1+\delta X,
 \quad w=\frac23-\delta^2Y,
 \quad a=\frac13+\delta^2\nu,
 \quad s=\delta t.
\tag{6.1}
\]

The recovery equation becomes exactly

\[
 Y'=-X+\delta(\nu-Y).
\tag{6.2}
\]

The singular canard and adjoint remain

\[
 \gamma_0(s)=\left(-\frac{s}{2},\frac{s^2-2}{4}\right),
 \qquad \psi(s)=e^{-s^2/2}(s,1)^T.
\tag{6.3}
\]

At first order, the slow forcing is now

\[
 q_{1,Y}=\nu-Y_0(s),
\tag{6.4}
\]

whereas the voltage forcing is the same as in the quadratic period-lock
calculation.  Its Gaussian pairing is therefore

\[
 \int_{\mathbb R}\psi^Tq_1\,ds
 =\sqrt{2\pi}\left(\nu+\frac18+\frac14\right)
 =\sqrt{2\pi}\left(\nu+\frac38\right).
\tag{6.5}
\]

Thus the formal leading canonical root is

\[
 \nu_0=-\frac38,
 \qquad
 a_c(\delta)=\frac13-\frac38\delta^2+O(\delta^3).
\tag{6.6}
\]

At \(\delta^2=1/5\), the leading prediction is

\[
 a_c\approx\frac{31}{120}=0.258333\ldots,
\tag{6.7}
\]

only \(1/120\) above the bistable center \(a=1/4\).  The outer periodic
collocation branch becomes poorly conditioned as \(a\) approaches this
value, which is consistent with a nearby hard-excitation boundary but is
not evidence that the canard root equals the basin boundary.

One may also restore the quadratic period-lock carrier

\[
 \varepsilon\eta\{(v(t)-1)^2-(v(t-\tau_*)-1)^2\},
\tag{6.8}
\]

choosing \(\tau_*\) equal to the center pulse period.  It then vanishes on
both constant histories and the distinguished pulse orbit.  Its fold
pairing remains nonzero; formally the selected root retains the response

\[
 a_c(\delta,\eta)-a_c(\delta,0)
 =-\frac{\Theta_*}{2}\delta^3\eta
 +O(\delta^4|\eta|+\delta^3\eta^2).
\tag{6.9}
\]

Equations (6.5)--(6.9) are formal/adapted asymptotics until the leaky
complete-history graph theorem is written out.  Even after that step, a
fixed-\(\varepsilon\) theorem must still identify the selected canard root
with the physical-pulse stable-manifold crossing.  That equality is the
remaining canard-to-onset bridge, not something supplied by bistability
alone.

## 7. Proof tasks and acceptance gates

The work should be split into the following GitHub issues.

1. **Leaky equilibrium certificate -- complete.**  Preserve the exact
   rational inequalities (2.9)--(2.11) and add hostile tests for every sign.
2. **[Two directed periodic BVPs](https://github.com/h-lu/canard-aware-network-control/issues/20) -- center points complete.**
   The source-bound 129-node inner and 257-node outer radii theorems validate
   distinct center orbits and bordered inverses.  Continue both on a common
   \((a,\kappa_3)\) box.  Acceptance for this remaining box gate requires two
   uniform radii inequalities, disjoint orbit tubes, and directed simple
   extrema.
3. **[Two Floquet index counts](https://github.com/h-lu/canard-aware-network-control/issues/20).**
   Prove zero nontranslation unstable
   multipliers for \(\Gamma_p\) and exactly one for \(\Gamma_u\), including
   simplicity of the neutral multiplier and analytic-to-monodromy
   multiplicity transfer.
4. **[Physical-pulse separator](https://github.com/h-lu/canard-aware-network-control/issues/21).**
   In
   \(C([-\tau _1,0],\mathbb R^2)\), construct the history-space Conley
   block and local pulse-history tube of hypothesis 3, enclose the
   terminal-history map \(K_\xi(J)\), exclude other complete invariant sets
   in that same block, prove endpoint routing for \(J=0.30,0.32\), and
   validate one transverse adjoint pairing at the crossing.  Acceptance is
   a unique local \(C^1\) \(J_c(\xi)\), not merely two long integrations.
5. **[Frequency--amplitude target ball](https://github.com/h-lu/canard-aware-network-control/issues/22).**
   Enclose the matrix in (4.7), prove
   its determinant stays away from zero, transfer squared range to
   unsquared amplitude, and give a nonzero three-dimensional image radius
   for (4.5).
6. **[Dobrushin lift](https://github.com/h-lu/canard-aware-network-control/issues/22).**
   Validate (5.5), formalize (5.9), and prove the two
   attractors and one separator index for every fixed finite topology with
   \(\gamma\ge1/2\).  Treat a dimension-uniform nonlinear basin radius as a
   separate stronger gate.
7. **[Leaky canard root and onset comparison](https://github.com/h-lu/canard-aware-network-control/issues/18).**
   First close the target graph in
   [#19](https://github.com/h-lu/canard-aware-network-control/issues/19)
   and the selected root in
   [#16](https://github.com/h-lu/canard-aware-network-control/issues/16),
   then adapt the complete-history
   graph/root proof to (6.2), validate the fixed-
   \(\varepsilon\) selected root, and compare its dynamic adjoint with the
   stable-manifold pulse-onset adjoint.  A nonzero correlation is not
   equality; acceptance requires an explicit theorem relating the two
   codimension-one objects.

## 8. Claim ledger

**Proved now:** the unique synchronous equilibrium and its delay-independent
local exponential stability at (1.2); distinct inner and outer phase-fixed
periodic RFDE orbits and their bordered inverses at the center; and the
smooth, injective, positively oriented physical pulse-to-history curve.

**Numerically supported:** the interpretation of the outer orbit as
attracting and the inner orbit as having one unstable multiplier, a
nondegenerate finite-section separator target near
\(J=0.301135337086902\), the routed physical-pulse bracket
\([0.30,0.32]\), and a nonsingular \((a,\kappa_3)\)-to-
\((F,A_p)\) response.

**Conditional theorem:** autonomous two-basin onset and the three-output
local diffeomorphism, assuming the five validation blocks of Section 4.

**Open:** the common orbit/extrema box, directed Floquet index proofs, a unique
basin separator, physical pulse-map transversality, a nonzero validated
output-ball radius, the full finite-network basin lift, the fixed-
\(\varepsilon\) leaky canard root, and its identification with physical
onset.
