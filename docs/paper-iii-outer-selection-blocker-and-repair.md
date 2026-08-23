# Paper III Gate P3-A: the outer-selection obstruction and a repair

Status: **the nonuniqueness and mixed-jet obstruction in Sections 2--3 are
proved exactly.  The scalar anchored-transfer estimate in Section 5 is also
proved exactly.  The curve-restricted formulation in Section 4 is exact for
the physical two-module RFDE.  The nonlinear model-specific dichotomy and
gluing theorem stated as Gate P3-A$^*$ in Section 6 is a feasible repair,
not a completed theorem.  Consequently this note does not close the
physical maximal-canard gate.**

The executable certificate is
`src/canard_control/outer_selection_coherence.py`; its tests are in
`tests/test_outer_selection_coherence.py`.  This note does not modify the
frozen JNS manuscript.

## 1. What the proposed gate must select

Let \(T=\varepsilon t\), \(\varepsilon=\delta^2\).  In the physical modal
coordinates of `outer-modal-algebra.md`, the two-module RFDE has the exact
slow-time form

\[
\begin{aligned}
 \varepsilon \xi_T
   &=\mathcal F_c(\xi,\zeta,\rho,\kappa)
      +\varepsilon\mathcal H_c[x_T;\eta],\\
 \varepsilon \zeta_T
   &=\mathcal F_\perp(\xi,\zeta,\rho,\kappa)
      +\varepsilon\mathcal H_\perp[x_T;\eta],\\
 \rho_T&=\xi-\mu,\\
 \varepsilon\kappa_T&=\varepsilon\zeta-D_w\kappa.
\end{aligned}
\tag{1.1}
\]

The slow-time delays are

\[
 h_k=\delta\theta_k.
\tag{1.2}
\]

A physical outer selection is therefore not just a current-state curve.  It
must give a parameterized curve of compatible histories, with enough
regularity that present evaluation, delayed evaluation, the matching hit,
and their parameter derivatives are all controlled.  After scaling the
slow history interval back to the fixed interval
\([-\theta_1,0]\), write

\[
 \widehat x_T(\vartheta)=x(T+\delta\vartheta),
 \qquad -\theta_1\leq\vartheta\leq0.
\tag{1.3}
\]

The required object is a \(C^1_\nu C^2_\eta\) map into a strong history
space on (1.3), not a separately smooth choice for every fixed
\(\delta\).

The current wording of Gate P3-A proposes two selection principles:

1. forward Lyapunov--Perron decay on the attracting side; and
2. bounded complete backward extension on the repelling side.

The first phrase defines a unique object only after the reference orbit,
one-sided projector, domain, and boundary datum of the Lyapunov--Perron map
have been fixed.  The second phrase does not eliminate the forward-unstable
normal mode at all.  The latter failure already occurs in a scalar ODE and
is therefore not a subtlety created by the delay.

## 2. An exact RFDE-subclass counterexample

Every ODE is a retarded equation whose vector field ignores its history.
Consider, on \(T\leq0\),

\[
 \varepsilon x_T=x.
\tag{2.1}
\]

For every scalar function \(C_\delta(\nu,\eta)\),

\[
 x_{\delta,\nu,\eta}(T)
 =C_\delta(\nu,\eta)e^{T/\varepsilon}
\tag{2.2}
\]

is a complete backward solution satisfying

\[
 \sup_{T\leq0}|x_{\delta,\nu,\eta}(T)|
 \leq |C_\delta(\nu,\eta)|,
 \qquad
 \lim_{T\to-\infty}x_{\delta,\nu,\eta}(T)=0.
\tag{2.3}
\]

Thus bounded complete backward extension leaves the coefficient \(C_\delta\)
arbitrary.  It removes a forward-stable mode, which would grow backward, but
does not remove the forward-unstable mode in (2.1).

This freedom persists even if all choices are exponentially close as
unparameterized curves.  Fix \(0<a<b\) and put

\[
\begin{aligned}
 C_\delta(\nu,\eta)
 =e^{-a/\varepsilon}\big[&
 (1+\nu)\sin(\eta e^{b/\varepsilon})\\
 &+1-\cos(\eta e^{b/\varepsilon})\big].
\end{aligned}
\tag{2.4}
\]

On a fixed bounded parameter box, \(C_\delta=O(e^{-a/\varepsilon})\),
and it is smooth in \((\nu,\eta)\) for every fixed positive \(\delta\).
At \(\eta=0\), however,

\[
\begin{aligned}
 \partial_\eta C_\delta
   &=(1+\nu)e^{(b-a)/\varepsilon},\\
 \partial_{\eta\eta}C_\delta
   &=e^{(2b-a)/\varepsilon},\\
 \partial_{\nu\eta}C_\delta
   &=e^{(b-a)/\varepsilon}.
\end{aligned}
\tag{2.5}
\]

At \(T=0\), the fixed-interval representation of the complete history is

\[
 \widehat x_0(\vartheta)
 =C_\delta(\nu,\eta)e^{\vartheta/\delta},
 \qquad -\theta_1\leq\vartheta\leq0.
\tag{2.6}
\]

Present evaluation sends (2.6) to \(C_\delta\).  Since present evaluation
is continuous in every strong history norm used for an RFDE solution
manifold, each of the norms of the jets in (2.5) is bounded from below by
the displayed current-state value.

> **Proposition 2.1 (backward completeness does not imply tame
> selection).**  Fix arbitrary finite constants \(p,M,m,c,C>0\), and let
>
> \[
>  S_\delta=\sqrt{2p\log(1/\delta)}.
> \]
>
> There is a family of complete backward histories satisfying (2.3), lying
> \(O(e^{-a/\delta^2})\) from the zero history in the \(C^0\) history norm,
> whose
> \(C^1_\nu C^2_\eta\) jets do not obey
>
> \[
>  C\delta^{-M}\langle S_\delta\rangle^m e^{cS_\delta}.
> \tag{2.7}
> \]

**Proof.**  Use (2.4).  For the first \(\eta\)-jet, the logarithm of the
ratio between (2.5) and (2.7), apart from a bounded \(\nu\)-factor, is

\[
 \frac{b-a}{\delta^2}
 -M\log(1/\delta)-m\log\langle S_\delta\rangle-cS_\delta-\log C.
\tag{2.8}
\]

It tends to \(+\infty\).  The second \(\eta\)-jet and the mixed jet give
the same conclusion.  Equation (2.6) transfers the lower bounds to the
strong history norm.  \(\square\)

The analogous attracting equation

\[
 \varepsilon x_T=-x
\tag{2.9}
\]

also shows that “converges forward to the slow curve” is not a selection
rule: every initial coefficient converges.  A genuine Lyapunov--Perron
definition repairs (2.9) only because it declares a projector and a
no-incoming boundary condition in addition to decay.

## 3. Why this is the minimal blocker for the two-module model

Along the singular critical curve of the physical model, the small voltage
eigenvalue is

\[
 \lambda_c(\xi)=-2\alpha\xi+O(\xi^2).
\tag{3.1}
\]

Hence the right branch \(\xi>0\) has only stable fast normal directions,
whereas the middle branch \(\xi<0\) has one forward-unstable voltage
direction.  The other voltage mode and the transverse recovery mode remain
stable.  Bounded backward extension removes the stable modes but leaves an
arbitrary coefficient in precisely the direction modeled by (2.1).

There is a second local difficulty.  At \(\mu=0\),

\[
 \rho_0(\xi)=-\alpha\xi^2+O(\xi^3),
 \qquad \rho_T=\xi.
\tag{3.2}
\]

Consequently

\[
 \frac{d\xi}{dT}
 =\frac{\xi}{\rho_0'(\xi)}
 =-\frac1{2\alpha}+O(\xi).
\tag{3.3}
\]

The repelling outer branch reaches the fold in finite backward slow time.
Thus “complete backward extension while remaining on a fixed normally
hyperbolic outer segment” cannot literally be the missing global boundary
condition.  Any complete extension must say how the curve continues through
or outside the fold neighborhood; that is exactly the selection information
which Gate P3-A currently omits.

Finally, exponentially close histories need not be equal histories.  The
local scalar gap is equivalent to a complete-history intersection only
because both canonical traces lie on the same injectively embedded exact
history graph.  If an independently chosen physical outer curve is merely
\(O(e^{-A/\varepsilon})\)-close to that graph, present evaluation and stable
projection give a shadow, not membership.  In an infinite-dimensional
history space, one scalar parameter cannot generically remove every
off-graph component.  Exact common-graph overlap is therefore an additional
compatibility condition, not a consequence of Fenichel closeness.

It follows that the original Gate P3-A has no well-defined theorem object:
the hypotheses do not specify which member of the exponentially close outer
family is being differentiated, and they do not ensure that the two selected
curves live in one finite-dimensional history graph.  Proposition 2.1 shows
that the requested mixed-jet estimate cannot be deduced from the stated
properties.

## 4. Exact curve-restricted formulation

The failure above does not require an ambient backward RFDE.  The correct
way to formulate a repaired selection is along a finite-dimensional base
curve.

Let \(r\) parameterize a physical outer branch and let

\[
 \mathcal K_{\delta,\lambda}:I\longrightarrow\mathbb R^4,
 \qquad \lambda=(\nu,\eta),
\tag{4.1}
\]

be a current-state parameterization with
\(\pi_\rho\mathcal K(r)=r\).  Its base speed is forced by (1.1):

\[
 q_{\delta,\lambda}(r)
 =\pi_\xi\mathcal K_{\delta,\lambda}(r)-\mu.
\tag{4.2}
\]

Denote the two-sided flow of this scalar ODE by
\(\Phi_q^T\).  The curve-restricted history is

\[
 \mathfrak I_{\delta,\lambda}(r)(\vartheta)
 =\mathcal K_{\delta,\lambda}
   \bigl(\Phi_q^{\delta\vartheta}(r)\bigr),
 \qquad -\theta_1\leq\vartheta\leq0.
\tag{4.3}
\]

The delayed atoms in (1.1) are exactly

\[
 \mathfrak I_{\delta,\lambda}(r)(-\theta_k)
 =\mathcal K_{\delta,\lambda}
   \bigl(\Phi_q^{-\delta\theta_k}(r)\bigr).
\tag{4.4}
\]

If \(\mathcal V_{\delta,\lambda}\) denotes the slow-time RFDE vector field in
(1.1), the exact parameterization equation is

\[
 D\mathcal K_{\delta,\lambda}(r)q_{\delta,\lambda}(r)
 =\mathcal V_{\delta,\lambda}
   \bigl(\mathfrak I_{\delta,\lambda}(r)\bigr).
\tag{4.5}
\]

Equations (4.2)--(4.5) use only the invertible scalar base flow.  They do
not invert the ambient retarded semiflow.

> **Lemma 4.1 (exact curve-restricted lift).**  Suppose
> \(\mathcal K_{\delta,\lambda}\) and \(q_{\delta,\lambda}\) solve
> (4.2)--(4.5), the scalar base flow exists for all retained backtracks,
> and their flow hull remains in the uncut physical tube.  Then (4.3) is an
> exact history solution of the unprepared RFDE.  If
> \(\pi_\rho\mathcal K(r)=r\), the history parameterization is injective.

**Proof.**  Let \(r(T)=\Phi_q^T(r_0)\) and
\(x(T)=\mathcal K(r(T))\).  The chain rule and (4.5) give

\[
 x_T=D\mathcal K(r(T))q(r(T))
     =\mathcal V_{\delta,\lambda}(\widehat x_T).
\]

Equation (4.4) identifies every delayed value in this equality with the
corresponding value of the same curve.  Thus \(x\) solves the physical RFDE
on the retained flow hull.  No ambient history is propagated backward.
Finally, present evaluation followed by \(\pi_\rho\) recovers \(r\), which
proves injectivity.  \(\square\)

In normal coordinates \(n\) along the singular branch, differentiating
(4.5) gives a nonautonomous equation of the form

\[
 \varepsilon n_T=A(T)n
 +\varepsilon\mathcal N_\delta
   \bigl(T,n(T),n(T-h_0),n(T-h_1);\lambda\bigr).
\tag{4.6}
\]

Let \(U(T,S)\) be the principal operator of its local normal part and let
\(P_s(T),P_u(T)\) be a dichotomy.  On a finite branch interval
\([T_-,T_+]\), a genuine curve-wise Lyapunov--Perron selection must declare
the boundary coordinates \(\beta_s,\beta_u\) and solve

\[
\begin{aligned}
 n(T)={}&U(T,T_-)P_s(T_-)\beta_s
 +\int_{T_-}^{T}U(T,S)P_s(S)\mathcal N_\delta(S)\,dS\\
 &+U(T,T_+)P_u(T_+)\beta_u
 -\int_T^{T_+}U(T,S)P_u(S)\mathcal N_\delta(S)\,dS.
\end{aligned}
\tag{4.7}
\]

For the attracting branch \(P_u=0\).  On the middle branch, the
one-dimensional \(P_u\) term is indispensable.  Bounded backward extension
does not determine \(\beta_u\); (2.1) is equation (4.7) with
\(\mathcal N=0\) and arbitrary \(\beta_u\).

The exact object needed for mixed jets is therefore the fixed point of
(4.7), with parameter-coherent boundary maps

\[
 (\delta,\nu,\eta)\longmapsto(\beta_s,\beta_u)
\tag{4.8}
\]

specified before differentiation.  The finite-dimensional base backtracks
in (4.4), not an ambient backward RFDE solve, are used at every Picard step.

## 5. Exact anchored transfer in the scalar normal model

The missing boundary data are not an arbitrary technical burden.  Once
they are tame, their influence at the fold overlap is flat on the algebraic
canard scale.

> **Proposition 5.1 (anchored boundary data are superalgebraically
> forgotten).**  Let \(\varepsilon=\delta^2\), fix \(A>0\), and suppose a
> finite collection of mixed parameter derivatives of an outer boundary
> datum \(b_\delta(\lambda)\) is bounded by \(C\delta^{-M}\).  For either the
> attracting propagation
>
> \[
>  \varepsilon x_T=-x,\qquad x(0)=b_\delta,\qquad 0\leq T\leq A,
> \]
>
> or the backward propagation from the repelling boundary
>
> \[
>  \varepsilon x_T=x,\qquad x(0)=b_\delta,\qquad -A\leq T\leq0,
> \]
>
> the corresponding matching history of slow length
> \(h_\delta=\delta\theta_1\) satisfies
>
> \[
>  \|\mathscr D x_{\rm match}\|_{\rm hist}
>  \leq C\delta^{-M}
>  \exp\left(-\frac{A}{\delta^2}
>             +\frac{\theta_1}{\delta}\right).
> \tag{5.1}
> \]
>
> Hence it is \(O(\delta^N)\) for every prescribed finite \(N\).

**Proof.**  The present values are \(b_\delta e^{-A/\varepsilon}\).
On the attracting segment the oldest retained history point can be larger
than the present value by at most
\(e^{h_\delta/\varepsilon}=e^{\theta_1/\delta}\).  On the repelling segment
the present point is the largest point in the backward history, so the same
bound remains valid.  Parameter differentiation acts only on \(b_\delta\)
in this constant-coefficient model.  This proves (5.1).  Finally,

\[
 -\frac{A}{\delta^2}+\frac{\theta_1}{\delta}
 +(M+N)\log(1/\delta)\longrightarrow-\infty,
\]

which proves the last assertion.  \(\square\)

The executable test compares the logarithm in (5.1) with arbitrary fixed
algebraic targets, avoiding numerical underflow.  Proposition 5.1 is not a
proof of (4.7) for the nonlinear model.  It identifies the correct scale:
a fixed positive outer normal action dominates both a slow-delay history
loss \(e^{C/\delta}\) and the inner logarithmic loss \(e^{cS_\delta}\).

## 6. A well-posed replacement: Gate P3-A$^*$

There are two honest ways to repair the theorem.  The first preserves a
maximal-canard statement; the second is more directly biological.

### 6.1 Compatible common-graph selection

Fix two physical outer sections, independent of \(\delta\), on compact
normally hyperbolic pieces of the attracting and middle branches.  Fix the
phase and the stable/unstable boundary projectors in (4.7).  Define the
outer boundary maps by one common compatibility rule: the resulting
curve-restricted solutions must continue the same exact local history graph
on a fixed overlap.  This defines a member of the nonunique Fenichel family
rather than pretending that every member is identical.

The repaired analytic gate is the following.

> **Gate P3-A$^*$ (compatible physical outer continuation; open).**
> Fix compact boxes
> \[
>  |\nu-\nu_0|\leq\bar\nu,\qquad
>  |\eta|\leq\bar\eta<1/20,
> \]
> fixed physical outer sections, and a logarithmic exponent
> \(p_{\log}\) chosen only after all tame exponents below.  There must
> exist
> \[
>  \delta_0,A_*,C,C_0,M_0,M,m,c>0,
> \]
> independent of \(0<\delta\leq\delta_0\), \(\nu\), and \(\eta\), for
> which the uncut physical vector field admits solutions of
> (4.2)--(4.7) on the attracting and middle outer segments with the
> declared common-graph boundary normalization.  For every
> \(0\leq i\leq1\), \(0\leq j\leq2\), including the rectangular mixed
> derivatives, prove:
>
> 1. existence and uniqueness within the normalized curve class;
> 2. \(C^1_\nu C^2_\eta\) strong-history jets of (4.3);
> 3. fixed positive normal actions \(A_a,A_r\), with
>    \(A_*\leq\min(A_a,A_r)\), and the boundary-to-match sensitivity
>    estimate
>
>    \[
>     \left\|
>       \partial_\nu^i\partial_\eta^j
>       \bigl(\phi^{a/r}_{\beta_1,\rm match}
>             -\phi^{a/r}_{\beta_2,\rm match}\bigr)
>     \right\|_{\rm hist}
>     \leq C\delta^{-M_0}
>       e^{-A_*/\delta^2+C_0/\delta}
>       \|\beta_1-\beta_2\|_{C^1_\nu C^2_\eta};
>    \tag{6.1}
>    \]
> 4. exact equality with the same local complete-history graph on the
>    compatibility overlap for the normalized compatible choice, not just
>    current-state closeness;
> 5. arrival at
>
>    \[
>     S_\delta=\sqrt{2p_{\log}\log(1/\delta)},\qquad
>     r_\delta=\frac12\delta S_\delta
>       \bigl(1+O(S_\delta^{-2})\bigr)
>    \]
>
>    with the already proved
>    \(\delta^{-M}\langle S_\delta\rangle^m e^{cS_\delta}\) trace
>    bounds; and
> 6. containment of every base backtrack (4.4) in the enlarged uncut
>    logarithmic history tube.

All constants in this statement are fixed before \(p_{\log}\) is chosen.

The singular geometry already verifies the sign pattern needed for the
dichotomy.  On fixed outer pieces the voltage normal eigenvalues are
bounded away from zero and \(D_w>0\) supplies the third stable rate.  The
weak delayed field is an \(O(1)\) term in (4.6), whereas the leading normal
generator is \(A/\varepsilon\).  Near the logarithmic overlap,

\[
 |\lambda_c|\asymp\delta S_\delta,
 \qquad
 \frac{|\lambda_c|}{\varepsilon}
 \asymp\frac{S_\delta}{\delta}.
\tag{6.2}
\]

A slow delay of length \(\delta\theta_k\) therefore costs at most a fixed
subalgebraic factor \(e^{C S_\delta}\) there.  Along the singular inner
curve a backtrack changes the inner phase by only the fixed amount
\(\theta_k\); enlarging the graph target from \(S_\delta\) to
\(S_\delta+\theta_1+B\) is sufficient.  These observations identify the
right norms but do not replace the nonlinear dichotomy proof.

The proof should be split at a fixed small physical radius \(r_0>0\):

1. on the fixed outer pieces, prove (4.7) and its triangular mixed jets by
   roughness of the finite-dimensional normal dichotomy under the weak
   curve-wise delay operator;
2. use the positive action between the outer sections and \(r_0\) to obtain
   (6.1), including differentiated boundary terms;
3. on \(r_\delta\leq r\leq r_0\), invoke the existing growing special-flow
   history graph and one-sided phase-normal Green estimates; and
4. use uniqueness in the normalized curve class to obtain exact
   complete-history overlap.

This route never invokes an ambient backward RFDE.  It also states honestly
what remains selection-dependent: a different compatible normalization can
change the exact finite-\(\delta\) root by a flat amount, although (6.1)
makes every fixed algebraic coefficient, including the
\(\delta^3\eta\) response, invariant.

### 6.2 A biological history-reset protocol

The causal alternative is now constructed in
`paper-iii-causal-reset-separator.md`.  Its final hold lasts at
least one maximal physical delay, clamps the voltage, presets the collective
recovery coordinate, and lets the physical recovery equation generate the
released history.  The resulting fixed-interval history is explicit,
parameter smooth, and independent of pre-hold delayed voltage memory.  The
same calculation proves that a voltage hold alone cannot erase an unknown
collective recovery error; that error survives exactly, whereas transverse
recovery error decays like \(e^{-D_wT_R}\).

For a reset path through the two singular fast channels, opposite
positive-\(\varepsilon\) endpoint outcomes and a nonempty compact
transition set are proved.  What remains open is the signed exchange Gate
R-S: show that the transition set is one simply crossed complete-history
separator and that its sign selects the two blocks arbitrarily close to the
root.  Thus the causal construction removes the nonunique outer-manifold
choice, but it does not yet identify a unique reset threshold with the
preparation-indexed canard root.

## 7. Consequence for the current Paper III claim

The original Gate P3-A cannot be marked proved.  The exact failure is not
the lack of a sufficiently clever norm:

- bounded complete backward extension leaves the repelling unstable
  coefficient free;
- fixed-\(\delta\) smoothness and exponential closeness do not imply uniform
  mixed parameter jets; and
- exponential closeness to the local history graph does not imply exact
  history membership or a scalar-codimension intersection.

The intrinsic-canard repair is to replace “choose the physical outer
selections” by the fully specified compatible Lyapunov--Perron boundary
normalization in Gate P3-A$^*$.  The causal reset repair is now exact through
existence of a transition set, but its unique-boundary conclusion remains
conditional on Gate R-S.  Until P3-A$^*$ or the corresponding reset
exchange/root comparison is proved, the preparation-indexed local root must
remain distinct from a physical outer maximal-canard or pulse root.
