# Flagship research design: transverse delay organization and a canard root

Status: **proof-first design, 2026-08-22.** This document controls the
submission scope until the main theorem is proved. The broader finite-
network transfer and frequency--amplitude--safety program remains in the
repository, but it enters the paper only through the promotion gates below.

## 1. The paper in one sentence

Two delayed FitzHugh--Nagumo systems can have the same total delayed gain and
the same delay measure seen by the critical projection, yet have different
local canard thresholds because delay forcing enters a stable transverse
mode and returns through the nonlinearity.

The paper must prove this statement for one fixed two-module RFDE. It must not
replace the missing proof by assuming a full Fredholm theory and then applying
the implicit-function theorem.

## 2. Nearest result and the new mathematical object

[Zhang et al. (2026)](https://doi.org/10.1137/24M1696548) compute high-order
canard data for one weakly delayed van der Pol oscillator. In their
normalization, \(J=\varepsilon K\),
\(\tau=\Theta/\sqrt\varepsilon\), and \(a\) is the scalar van der Pol
unfolding parameter. Their coefficient is the required calibration:

\[
 a_c=1-\frac18\varepsilon
 +\frac{K\Theta}{8}\varepsilon^{3/2}+\cdots .
\tag{1}
\]

Equation (1), the weak-feedback scaling, and the nonlinear time-transformation
calculation are prior work, not contributions of this paper. The new object is
the derivative of a geometric RFDE canard root in a direction that is
invisible to the critical projected delay measure.

No theorem is imported from the scalar van der Pol equation into the vector
FitzHugh--Nagumo RFDE. The parameter-regular invariant-history reduction, the
transverse return, and the history-level canard intersection and remainder are
new proof obligations.

The intended distinction is therefore about the result, not merely the
method:

- the published scalar problem computes a threshold inside one delayed
  oscillator;
- the present problem proves that a transverse delay organization changes the
  threshold even when the scalar delayed data are held fixed.

## 3. Base RFDE and fixed-data contract

The submission core uses exactly two voltage--recovery modules and two fixed
scaled delay atoms

\[
 0<\theta_0<\theta_1\leq\theta_{\max},
 \qquad \tau_k=\theta_k/\delta,
 \qquad \delta=\sqrt\varepsilon.
\tag{2}
\]

Let \(v=(v_1,v_2)^\top\), \(w=(w_1,w_2)^\top\), and
\(\sigma=\sqrt{3/2}\). In physical fast time, the target RFDE to be
algebraically re-audited in Phase I is

\[
\boxed{
\begin{aligned}
 \dot v(t)={}&F(v(t),w(t))
 +\varepsilon K\left[
 Bv(t)-C_0^\eta v(t-\tau_0)-C_1^\eta v(t-\tau_1)
 \right],\\
 \dot w(t)={}&\varepsilon
 \begin{pmatrix}v_1(t)-\sigma-\mu\\ v_2(t)-2\mu\end{pmatrix}
 -D_wP_\perp(w(t)-w_*),
\end{aligned}}
\tag{M}
\]

where

\[
 F(v,w)=
 \begin{pmatrix}
 v_1-v_1^3/3-w_1+(v_2-v_1)/2\\
 v_2-v_2^3/3-w_2+2(v_1-v_2)
 \end{pmatrix},
 \qquad
 v_*=\begin{pmatrix}\sigma\\0\end{pmatrix},
 \quad
 w_*=\begin{pmatrix}0\\2\sigma\end{pmatrix}.
\]

The positive two-layer family from
[two-module-moment-counterexample.md](two-module-moment-counterexample.md) is

\[
\begin{gathered}
 C_0=\begin{pmatrix}1/6&1/12\\1/6&1/4\end{pmatrix},
 \qquad
 C_1=\begin{pmatrix}1/3&1/6\\1/2&5/12\end{pmatrix},\\
 T=\begin{pmatrix}1&0\\-2&0\end{pmatrix},
 \qquad
 C_0^\eta=C_0+\eta T,
 \qquad
 C_1^\eta=C_1-\eta T,
 \qquad
 B=C_0+C_1.
\end{gathered}
\tag{3}
\]

Thus the delayed term has the source-history form

\[
 \mathcal H_\eta[v_t]
 =Bv(t)-C_0^\eta v(t-\theta_0/\delta)
       -C_1^\eta v(t-\theta_1/\delta).
\tag{4}
\]

Equivalently, its operator-valued delay measure is

\[
 \mathbb B_\eta(d\theta)
 =C_0^\eta\delta_{\theta_0}(d\theta)
 +C_1^\eta\delta_{\theta_1}(d\theta).
\tag{4a}
\]

The final theorem model retains two recovery variables and adds the fixed,
non-actuated recovery coupling

\[
 -D_wP_\perp(w-w_*),
 \qquad D_w>0,
\tag{5}
\]

where

\[
 r=\begin{pmatrix}1\\2\end{pmatrix},
 \qquad
 \ell=\begin{pmatrix}1/2\\1/4\end{pmatrix},
 \qquad
 P_\perp=I-r\ell^\top.
\]

This fixed \(O(1)\) physical-time coupling vanishes on the critical recovery
line and removes the extra transverse recovery center. It changes
off-critical recovery dynamics and must be named as part of the model, not
hidden as a control input. Fix once and for all

\[
 K\neq0,\qquad D_w>0,\qquad
 0<\theta_0<\theta_1,\qquad L>0,
 \qquad 0<\bar\eta<1/20.
\]

For \(|\eta|\leq\bar\eta\), both delayed layer matrices are positive. Every
estimate constant in the base theorem may depend on these fixed data and on
the frozen section conventions, but not on \(\delta\) or \(\eta\).

The proof is formulated after the fold blow-up and time scaling
\(s=\delta t\), so the history interval is the fixed interval
\([ -\theta_1,0]\). With
\(X=\delta^{-1}\ell^\top(v-v_*)\), fix local entry and exit sections
\(X=\pm L\), a matching section \(X=0\), and a phase condition placing the
match at \(s=0\). The intended object is an injective history embedding

\[
 \iota_{\delta,\eta}:U\subset\mathbb R^2
 \longrightarrow C([ -\theta_1,0],\mathbb R^4)
\]

whose image contains the selected attracting and repelling local slow
histories. Their reduced scalar matching gap on \(X=0\) is denoted
\(d(\mu,\delta,\eta)\); a selected matching parameter is a zero of \(d\).
Gate D must prove that this reduced zero is equivalent to equality of the
embedded complete histories before it is called an RFDE maximal canard. The
exact orientation, fibers, and gap normalization must be stated before the
target theorem is promoted to a result.

The following are fixed for version 1:

- \(N=2\), with two fixed modules rather than arbitrary module sizes;
- two fixed delay atoms rather than moving delay measures;
- the fixed \(K,D_w,\theta_0,\theta_1,L\) and positivity radius above;
- one local right-fold canard and fixed entry/exit sections;
- the geometric threshold is a local slow-history intersection, not a global
  spike detector.

General \(N\), freely moving delay support, arbitrary node heterogeneity, and
global pulse events are not part of the base theorem.

## 4. Exact invariants and the candidate coefficient

The family (3) is designed so that

\[
 C_0^\eta+C_1^\eta=B
\tag{6}
\]

and the critical projected delay measure

\[
 \ell^\top\mathbb B_\eta(d\theta)r
 =\frac13\delta_{\theta_0}(d\theta)
  +\frac23\delta_{\theta_1}(d\theta)
\tag{7}
\]

are independent of \(\eta\), while

\[
 P_\perp\mathbb B_\eta(d\theta)r
 =\eta q\left[
   \delta_{\theta_0}(d\theta)-\delta_{\theta_1}(d\theta)
  \right],
 \qquad q=Tr=\begin{pmatrix}1\\-2\end{pmatrix},
\tag{8}
\]

is not. These are exact finite-dimensional identities.

At \(\varepsilon=0\), \(\mu=0\), and \((v,w)=(v_*,w_*)\), the current-state
Jacobian has

\[
 \det(zI-J_0)=z^2(z+2)(z+D_w),
\tag{8a}
\]

so its generalized center is exactly the collective length-two Jordan chain.
This identity does not prove the RFDE spectral gap required in Gate A.

Let

\[
 \alpha=\frac12\sqrt{\frac32}.
\tag{9}
\]

The current inner calculation predicts

\[
 \partial_\eta\mu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta^3
 +O(\delta^4).
\tag{10}
\]

Equation (10) is a target, not an established RFDE result. It may change when
the actual invariant-history embedding and endpoint terms are computed. A
different nonzero coefficient is an acceptable theorem; an exact
cancellation changes the project into a first-nonzero-order or cancellation
theorem.

## 5. Minimum theorem target for the base paper

The theorem should have the following form.

> **Main theorem -- transverse delay contribution.** There exist
> \(\delta_0,\eta_*,C>0\), with \(\eta_*\leq\bar\eta\), such that, for
> \(0<\delta\leq\delta_0\) and \(|\eta|\leq\eta_*\), the two-module RFDE
> (M) has a unique selected local matching root
> \(\mu_c(\delta,\eta)\). The corresponding reduced attracting and repelling
> histories have the same image under \(\iota_{\delta,\eta}\), so this root is
> the unique selected local RFDE maximal-canard parameter. Moreover, for the
> coefficient \(c_\perp\) obtained
> from the actual RFDE reduction,
> \[
> \left|
> \mu_c(\delta,\eta)-\mu_c(\delta,0)
> -c_\perp K\eta(\theta_0-\theta_1)\delta^3
> \right|
> \leq C\left(\delta^4|\eta|+\delta^3\eta^2\right).
> \tag{11}
> \]
> The total gain (6) and projected delay measure (7) are independent of
> \(\eta\), whereas \(c_\perp\neq0\).

The formal candidate value is \(c_\perp=1/(4\alpha)\), but the paper may state
it only after the full reduction proves it. The coefficient may depend on the
fixed model data and parameter normalization. If the root is called
geometric, its value must be shown independent of admissible section and gap
conventions. Every uniformity statement in (11) must be fixed in the theorem
rather than supplied by a numerical experiment.

## 6. Shortest proof route

```mermaid
flowchart TD
    A["Exact layer identities and current-state singular spectrum"] --> B["RFDE spectral subspace and complementary gap"]
    B --> C["Two-dimensional invariant history manifold"]
    C --> D["Embedding iota and stable foliation"]
    D --> E["Reduced fold jet including the transverse delay channel"]
    E --> F["Simple planar canard matching root with a uniform remainder"]
    F --> G["Lifted RFDE slow-history intersection"]
    G --> H["Main theorem and coefficient c_perp"]
    H --> I["Optional general-N transfer"]
    H --> J["Optional three-coordinate control"]
```

Each supporting result has one mathematical job.

| Result | Object that must be constructed or estimated | Obstruction removed | Current status |
|---|---|---|---|
| Lemma 1 | Identities (6)--(8), fold nondegeneracy, and the repaired singular characteristic polynomial | Excludes a disguised scalar-moment change and removes the extra recovery center | Exact algebra exists; it must be rerun for the single final equation |
| Proposition 2 | A two-dimensional invariant history manifold \(\mathcal M_{\delta,\eta}=\iota_{\delta,\eta}(U)\), parameterized uniformly in \((\delta,\eta)\) | Infinite-dimensional history and backward-extension problem | Open; first proof gate |
| Proposition 3 | Stable foliation and a transverse inverse estimate on the chosen weighted spaces | Converts the current-state spectral gap into an actual RFDE range solve | Open |
| Proposition 4 | The reduced vector-field jet through the order producing \(\eta\delta^3\) | Upgrades the formal response and includes all embedding/endpoint contributions | Formal interior calculation only |
| Proposition 5 | A simple attracting/repelling slow-curve intersection and the remainder in (11) | Converts a jet into an actual geometric canard root | Open |
| Lift lemma | Equivalence between the reduced intersection and intersection of embedded complete histories | Prevents a matched-fiber event from being mislabeled as an RFDE maximal canard | Open |

The first paper should construct the matching gap in coordinates on
\(\mathcal M_{\delta,\eta}\) and use the injective history embedding to prove
the corresponding complete-history intersection. It should not begin by
postulating an arbitrary \(2N\)-state Fredholm trace pair.

The broader contracts in `scope-and-theorems.md` and
`full-network-lin-operator.md` are therefore promotion specifications, not
assumptions available to the base proof.

## 7. Stop/go gates

### Gate A -- relevant spectrum

Prove that the repaired RFDE has exactly the required two-dimensional
relevant spectral subspace and a uniform complementary gap in the declared
scaled history setting.

- **Pass:** construct Proposition 2.
- **Fail:** use the shared-recovery three-state model only if the coefficient
  mechanism survives and the biological/modeling restriction is stated.

### Gate B -- parameter-regular invariant history manifold

Obtain enough \((\delta,\eta)\)-regularity to compute the jet and control its
remainder.

- **Pass:** compute the true coefficient.
- **Fail:** a fixed-\(\delta\) implicit-function result is not a flagship
  asymptotic theorem; stop and redesign.

### Gate C -- coefficient

Calculate every interior, embedding, endpoint, and history-jump contribution.

- **Nonzero:** prove (11) with the calculated coefficient.
- **Cancellation:** determine the first nonzero order or prove a structural
  cancellation theorem.
- **Uncontrolled:** do not identify the formal inner coefficient with the
  RFDE threshold derivative.

### Gate D -- geometric canard

Prove the simple root, uniform remainder, and history-lift equivalence.

- **Pass:** the main theorem is complete.
- **Fail:** use “reduced connection root,” not “RFDE maximal-canard
  threshold,” and do not submit it as the stated theorem.

### Gate E -- promotion to general networks

Only after Gate D passes, attempt the full finite-\(N\) direct-sum Lin theorem.
It enters this paper only if it supplies a model-specific \(N\)-uniform inverse
bound and a computable structural functional without introducing a second
unproved geometry.

### Gate F -- control corollary

The frequency--amplitude--safety result enters this paper only if the periodic
branch, extrema regularity, and a positive singular-value lower bound follow
from one short additional section. A plotted determinant is insufficient. If
the result requires an independent phase--amplitude theory, omit it from the
title, abstract, and main claims.

## 8. Claim hierarchy

| Level | Permitted claim | Evidence required |
|---|---|---|
| Exact | Fixed total gain, fixed projected delay measure, algebraic mode forcing, and generalized-center dimension of the \(\varepsilon=0\) current-state Jacobian | Symbolic or hand proof for the final model |
| Formal | Candidate coefficient \(1/(4\alpha)\) | Truncated inner calculation, explicitly labelled formal |
| Theorem | Actual coefficient, local RFDE canard root, and remainder (11) | Center-manifold construction, history lift, simple root, and uniform estimates |
| Numerical | Convergence of normalized threshold differences | Two independent refinements and uncertainty below the observed discrepancy |
| Excluded | Global spiking threshold, arbitrary finite network, or independent three-coordinate assignment | Not inferred from the local theorem |

## 9. Paper architecture

1. **Introduction and main theorem.** Present the two delay organizations,
   state (11), and explain the boundary with Zhang et al. (2026).
2. **The fixed two-module RFDE.** Give the equation, exact invariants, fold
   geometry, and repaired singular spectrum.
3. **Nonlocal invariant manifold.** Construct
   \(\mathcal M_{\delta,\eta}\), its embedding, stable foliation, and parameter
   dependence.
4. **The reduced fold jet.** Calculate the transverse range response and its
   nonlinear return to the critical equation.
5. **The canard intersection.** Prove the simple root, remainder, history
   lift, and main theorem.
6. **Numerical check.** Test only the normalized limit
   \[
   \frac{\mu_c(\delta,\eta)-\mu_c(\delta,0)}
        {K\eta(\theta_0-\theta_1)\delta^3}
   \longrightarrow c_\perp.
   \tag{12}
   \]
7. **Discussion.** State the precise promotion conditions for general
   networks and control.

Move mechanical matrix calculations, repeated jet coefficients, solver
configuration, and secondary convergence tables to appendices. Keep the
invariant-history construction, transverse return mechanism, and canard root
argument in the main text.

## 10. Figure plan

Use at most two essential figures in the base paper.

1. **Mechanism schematic:** delay-layer redistribution \(\to\) stable
   transverse response \(\to\) nonlinear return \(\to\) canard-root shift.
   It must be labelled as a schematic, not a phase portrait proof.
2. **Computed asymptotic test:** the normalized quantity in (12), with
   refinement uncertainty, against \(\delta\).

If Gate E passes, add one full/reduced structural-root displacement figure.
If Gate F passes, replace rather than supplement a figure with the certified
control singular-value region.

## 11. Work plan

### Phase I -- close the model and spectrum

- write one final RFDE combining the positive two-layer family and the fixed
  recovery coupling;
- rerun every exact equilibrium, projection, positivity, and spectrum check;
- prove or falsify Gate A before adding simulations.

### Phase II -- construct the invariant geometry

- select the RFDE theorem used for the invariant history manifold and translate
  every hypothesis into the scaled model;
- construct the stable foliation and complete-history embedding;
- freeze entry/exit sections only after that geometry exists.

### Phase III -- compute and prove the threshold law

- derive the true reduced jet and adjoint/solvability coefficient;
- prove the simple canard root and (11);
- verify the history lift.

### Phase IV -- validate and decide promotion

- implement the normalized test (12) with two refinements;
- audit every claim as exact, formal, proved, or numerical;
- attempt Gates E and F only after the main theorem is complete.

## 12. Submission rule

The abstract leads with (11) and the fixed-projected-delay-measure/changing-
transverse-organization mechanism. The
paper does not lead with a generic implicit-function formula, a scalar
\(K\Theta/8\) coefficient, or the number of model components. General network
transfer and three-coordinate control appear as main claims only after their
promotion gates have been passed.

Execution is tracked in
[the base-theorem issue](https://github.com/h-lu/canard-aware-network-control/issues/10)
and
[the flagship epic](https://github.com/h-lu/canard-aware-network-control/issues/9).
