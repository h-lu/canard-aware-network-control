# RFDE Lin-gap formulation

Status: **the \(\mathbb R^4\) reference-gap template and the separate
\(2N\)-state operator contract are fixed; the actual endpoint bundles and
Fredholm gate remain open.** This specification removes the earlier
set-subtraction ambiguity and fixes the index bookkeeping after phase fixing.
It does not yet prove a full-network maximal-canard root or a global pulse
threshold.

## 1. Fixed history and differentiability spaces

Let \(\delta=\sqrt\varepsilon\) and \(r=\Theta_{\max}\). After the fold
blow-up, write the selected two-module RFDE as

\[
 U'(s)=\bar{\mathcal F}_\delta(U_s;\nu,\mathcal R),
 \qquad U_s(\theta)=U(s+\theta),
 \qquad \theta\in[-r,0],
 \tag{1}
\]

with \(U=(X_1,Y_1,X_2,Y_2)\). Three different spaces have different jobs:

\[
 X^0=C([-r,0],\mathbb R^4),
 \qquad X^1=C^1([-r,0],\mathbb R^4),
 \tag{2}
\]

\[
 \bar{\mathcal M}_{\delta,\nu,\mathcal R}
 =\{\phi\in X^1:\phi'(0)=
 \bar{\mathcal F}_\delta(\phi;\nu,\mathcal R)\},
 \tag{3}
\]

and Sobolev orbit spaces \(W^{k,p}\), \(1<p<\infty\), for the boundary-value
map. The natural continuous RFDE semiflow lives on \(X^0\); classical
compatible histories live on the solution manifold (3).

Moving a point delay is not differentiable in the ordinary operator norm on
\(X^0\). Version 1 therefore makes a concrete choice:

- point-delay locations form a finite-dimensional parameter vector;
- orbit pieces are controlled in a strong Sobolev space;
- first derivatives use translation differentiability in \(W^{1,p}\);
- a quadratic residual is claimed only after a \(W^{2,p}\), or equivalent,
  \(C^2\) result is proved;
- measure perturbations on an infinite-dimensional space vary weights on a
  fixed support.

Equations (1)--(22) are written on the exact block-synchronous two-module
reference subsystem. They define the reference gap, but by themselves do not
define a full-network transfer problem. For an \(N\)-node structural
perturbation that breaks block synchrony, the same construction must instead
use

\[
 U_N=(X_1,Y_1,\ldots,X_N,Y_N)\in\mathbb R^{2N},
 \qquad
 X_N^j=C^j([-r,0],\mathbb R^{2N}),
\]

with a complete \(2N\)-state history jump. At the exact reference, that
operator must decompose into collective, module-difference, and within-module
history blocks. A Fredholm result only for the \(\mathbb R^4\) subsystem would
prove a reduced theorem, not Theorem A for structurally perturbed networks.

The proof reference now includes fixed dual-state synchronization
\(D(P-I)v+E(P-I)w\), with \(D,E>0\). At the singular fold its exact
current-state Jacobian has one collective length-two zero Jordan chain and
\(N-1\) transverse blocks with eigenvalues \(-D,-E\). This removes the
voltage-only model's \(N-1\) recovery centers, but it is only the algebraic
input to the full RFDE construction. The weak long-delay spectrum, endpoint
bundles, and transverse history-block inverse still have to be proved.
After quotienting out the canonical RFDE history directions, a reduced
two-dimensional transverse skeleton with finite defect dimensions
\(d_-,d_+\) has the diagnostic count \(d_-+d_+-2\). Point constraints at
both ends fail this diagnostic. This is not an RFDE index theorem: the proof
must construct a history-space dichotomy/Fredholm trace pair of index zero
and only then recover \(d_-+d_+=2\) in a justified finite-defect reduction,
or work on the two-dimensional center manifold and prove a complete-history
fiber lift.

Bounded-Lipschitz or Wasserstein control of freely moving Dirac masses is an
extension. Such a metric gives useful Lipschitz closeness, but by itself does
not justify the Banach-space \(C^2\) expansion required by Theorem A.

## 2. Selected local canard pieces

Let \(r_c,\ell_c\) be the critical module modes, normalized by
\(\ell_c^\top r_c=1\), and define the critical current-state coordinate

\[
 \xi_c(\phi)=\ell_c^\top\pi_X\phi(0).
 \tag{4}
\]

Choose \(L>0\) and the three history-space sections

\[
 \Sigma_{\rm in}=\{\xi_c=L\},\qquad
 \Sigma=\{\xi_c=0\},\qquad
 \Sigma_{\rm out}=\{\xi_c=-L\}.
 \tag{5}
\]

The selected entry and exit sets are full-history slices

\[
 D^a_{\rm in}=S^a_\delta\cap\Sigma_{\rm in},
 \qquad
 D^r_{\rm out}=S^r_\delta\cap\Sigma_{\rm out},
 \tag{6}
\]

of fixed attracting and repelling slow manifolds. This selection is part of
the threshold definition and records the exponentially small nonuniqueness of
Fenichel extensions rather than hiding it.

The matching section in (5) is the single phase condition. It is transverse
because the leading calibration canard has \(X'_0=-1/2\). No second integral
phase condition is added.

An RFDE semiflow is not invertible on all of \(X^0\). The repelling piece is
therefore not obtained by a backward RFDE initial-value solve. The proof must
first construct a finite-dimensional backward-extendible center or
center-unstable solution manifold, construct the repelling slow manifold
there, and lift its complete histories into the RFDE BVP.

## 3. Two-piece boundary-value operator

Let

\[
 z=(u^-,u^+,\alpha_-,\alpha_+,T_-,T_+)
 \tag{7}
\]

collect the two orbit pieces, entry/exit coordinates, and flight times. The
intervals are rescaled to fixed domains in the analysis. Define

\[
 \bar{\mathfrak F}_\delta(z,\nu,\mathcal R)=
 \begin{pmatrix}
 \dot u^--\bar{\mathcal F}_\delta((u^-)_s;\nu,\mathcal R)\\
 \dot u^+-\bar{\mathcal F}_\delta((u^+)_s;\nu,\mathcal R)\\
 B_-((u^-)_{-T_-},\alpha_-;\nu,\mathcal R)\\
 B_+((u^+)_{T_+},\alpha_+;\nu,\mathcal R)\\
 \xi_c((u^-)_0)\\
 J(u^-,u^+)
 \end{pmatrix},
 \tag{8}
\]

where the last component is the complete-history jump

\[
 J(u^-,u^+)=(u^-)_0-(u^+)_0.
 \tag{9}
\]

Matching only the current states \(u^-(0)\) and \(u^+(0)\) would not splice
two RFDE solutions. Equation (9) matches the entire history on \([-r,0]\).

## 4. Correct Fredholm index and augmentation

At a reference local canard
\((z_{c,\delta},\nu_{c,\delta},0)\), set

\[
 \bar L_\delta=D_z\bar{\mathfrak F}_\delta
 (z_{c,\delta},\nu_{c,\delta},0).
 \tag{10}
\]

After the phase condition in (8), the required one-gap hypothesis is

\[
 \ker \bar L_\delta=\{0\},\qquad
 \dim\operatorname{coker}\bar L_\delta=1,
 \qquad
 \operatorname{ind}\bar L_\delta=-1.
 \tag{11}
\]

This replaces the inconsistent statement “index zero after phase fixing with
a one-dimensional cokernel.” Choose

\[
 \bar\psi_\delta\in\mathscr Y^*,\qquad
 \operatorname{Range}\bar L_\delta=\ker\bar\psi_\delta,
 \qquad \|\bar\psi_\delta\|=1,
 \tag{12}
\]

and a Lin direction \(\bar e_\delta\in\mathscr Y\) with

\[
 \bar\psi_\delta(\bar e_\delta)=1.
 \tag{13}
\]

Choose \(\bar e_\delta\) to have only a history-jump component. The augmented
operator

\[
 \widehat{\bar L}_\delta(\zeta,\gamma)
 =\bar L_\delta\zeta-\gamma\bar e_\delta
 \tag{14}
\]

has index zero and is required to be invertible. Equivalently,

\[
 \bar L_\delta:\mathscr X\longrightarrow
 \operatorname{Range}\bar L_\delta
 \tag{15}
\]

is an isomorphism. Its inverse norm is denoted by the range/transverse
constant

\[
 \bar G_\perp(\delta)=
 \left\|
 (\bar L_\delta:\mathscr X\to\operatorname{Range}\bar L_\delta)^{-1}
 \right\|.
 \tag{16}
\]

Here “transverse” means transverse to the one-dimensional Lin cokernel. In the
full \(2N\)-state problem it must control both the collective range equation
and every network-transverse history block; it is not a bound on the voltage
scaffold alone.

The cokernel covector belongs to the dual of the codomain; writing
\(D_z\mathfrak F|_{\psi^\perp}\) as a restriction of the domain is therefore
incorrect.

## 5. Strict scalar Lin gap

If (14) is invertible and the nonlinear BVP is sufficiently smooth, the
implicit-function theorem gives unique local functions
\((z(\nu,\mathcal R),\bar d_\delta(\nu,\mathcal R))\) satisfying

\[
 \bar{\mathfrak F}_\delta(z(\nu,\mathcal R),\nu,\mathcal R)
 =\bar d_\delta(\nu,\mathcal R)\bar e_\delta.
 \tag{17}
\]

The strict Lin gap is

\[
 \boxed{
 \bar d_\delta(\nu,\mathcal R)
 =\bar\psi_\delta\bar{\mathfrak F}_\delta
 (z(\nu,\mathcal R),\nu,\mathcal R).
 }
 \tag{18}
\]

All dynamic, entry, exit, and phase residuals have already been solved. Since
\(\bar e_\delta\) lies only in the jump component, augmented-IFT uniqueness
gives

\[
 \bar d_\delta=0
 \quad\Longleftrightarrow\quad
 (u^-)_0=(u^+)_0.
 \tag{19}
\]

If the endpoint maps directly parameterize the selected slow-manifold slices
without extra fiber coordinates, (19) is also equivalent to their local
intersection. If invariant-fiber coordinates are present, that geometric
interpretation requires the additional zero-fiber implication specified in
`full-network-lin-operator.md`; a zero complete-history jump alone gives only
a matched fiber connection.

The adjoint \(\bar\psi_\delta\) is not the static network left mode \(\ell_c\).
For a discrete-delay variational equation it contains an advanced dynamic
adjoint and entry, exit, phase, and jump multipliers. Its structural first
variation has the schematic form

\[
 D_{\mathcal R}\bar d_\delta[\mathcal R]
 =\int p_\delta(s)^\top
 D_{\mathcal R}\bar{\mathcal F}_\delta(q_{\delta,s})[\mathcal R],ds
 +\text{boundary terms}.
 \tag{20}
\]

Thus a topology-weighted moment must be derived from the dynamic adjoint; it
cannot be asserted from \(\ell_c^\top B r_c\) alone.

## 6. Root response and coordinate invariance

Use the blown-up parameter \(a=1+\delta^2\nu\) in the local theorem and set

\[
 \bar d_\delta(\nu_{c,\delta},0)=0,
 \qquad
 \bar m_\delta^{(\nu)}=
 |\partial_\nu \bar d_\delta(\nu_{c,\delta},0)|>0.
 \tag{21}
\]

Then

\[
 \nu_c'(0)[\mathcal R]
 =-
 \frac{D_{\mathcal R}\bar d_\delta
 (\nu_{c,\delta},0)[\mathcal R]}
 {\partial_\nu \bar d_\delta(\nu_{c,\delta},0)}.
 \tag{22}
\]

Physical-parameter derivatives obey
\(\partial_a=\delta^{-2}\partial_\nu\); the two transversality constants must
not be mixed.

Changing admissible BVP coordinates, the jump complement, or the normalization
of \(\bar\psi_\delta\) multiplies a local gap by a nonvanishing factor. Therefore
the zero set, simple-root property, and ratio (22) are invariant. The numerical
values of \(\bar d_\delta\), \(\bar m_\delta\), and \(\bar G_\perp\) still depend on norms and
normalization. Changing the selected entry/exit slow manifolds is a change of
the threshold, not a coordinate change.

An experimental observable detects the same geometric root only if its
derivative does not annihilate the Lin jump direction. Observable-dependent
zeros are called output-event thresholds.

## 7. What has and has not been completed

Completed for the \(\mathbb R^4\) reference template:

- fixed history, solution-manifold, and strong BVP spaces;
- full-history matching rather than current-state matching;
- one phase condition and the correct post-phase Fredholm index;
- the algebraic form of an index-zero augmented Lin operator;
- a candidate scalar gap whose zero is equivalent to a complete selected-history match only if the stated Fredholm and endpoint zero-fiber hypotheses hold;
- normalization-invariant first root response.

Still open for the frozen reference and its full \(2N\)-state extension:

- [ ] construct the center/solution manifold and selected endpoint maps;
- [ ] construct dual-scaffold history-space dichotomy/fiber endpoint pairs and prove they are Fredholm of index zero in every transverse block, or prove a two-dimensional center-manifold construction with complete-history lift;
- [ ] prove the required \(C^2\) dependence for the finite delay parameters;
- [ ] prove (11), closed range, and invertibility of (14);
- [ ] realize the specified \(\mathfrak F_{\delta,N}\) with constructed endpoint maps, prove its collective/module-difference/within-module history decomposition, and bound \(G_\perp(\delta)\) from that full Lin BVP;
- [ ] derive the dynamic adjoint and boundary terms in (20);
- [ ] prove a uniform lower bound in (21) on the declared parameter wedge;
- [ ] connect the local matched segment to a global pulse threshold.

The detailed full-network domain/codomain and trace-index contract are in
[the dual-scaffold operator specification](full-network-lin-operator.md).
That note fixes what must be proved; it does not discharge the open items
above.

The classical foundation is supplied by RFDE phase-space and invariant-
manifold theory, exponential-dichotomy/Fredholm results, and Lin reductions
for functional differential equations. Those works justify this architecture
but do not verify the singular canard estimates needed here.
