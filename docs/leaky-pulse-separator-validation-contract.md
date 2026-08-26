# A quantitative validation contract for the physical pulse separator

Status: **conditional theorem interface plus a source-bound binary64 target,
not a separator proof.**  This note fixes the exact phase-space object, the
third-return gap, the error decomposition, and a narrow pulse bracket that a
directed RFDE calculation must validate.  All displayed observations from
the target computation remain non-directed until the inequalities in
Sections 3--5 are enclosed.

## 1. Exact separator gap

Work in the proved solution-determining reduced history space

\[
 Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R.
\]

Let \(\gamma_i\) be the phase-fixed inner periodic orbit and let \(\Sigma\)
be the section

\[
 v(0)=v_i(0),\qquad \dot v_i(0)>0.
\]

Once the corrected Floquet calculation proves a simple positive unstable
multiplier and excludes every other nontranslation multiplier outside the
unit disk, normalize the unstable left Riesz covector \(\ell_u\), write
\(Y_\Sigma=E^u\oplus E^s\), and represent the local stable manifold as

\[
 W^s_{\rm loc}(\gamma_i)\cap\Sigma
   =\{u=h(z):z\in E^s\},
 \qquad h(0)=Dh(0)=0.                       \tag{1.1}
\]

For the physical pulse history \(K(J)\), let \(B_3(J)\) be its third
positive return to \(\Sigma\).  The exact gap to be certified is

\[
 \mathcal H_3(J)
 =\ell_u\{B_3(J)-\gamma_i(0)\}
  -h\!\left(P_s\{B_3(J)-\gamma_i(0)\}\right).          \tag{1.2}
\]

Thus \(\mathcal H_3(J)=0\) is a stable-manifold intersection, not merely a
zero of a finite monodromy eigenvector.  Because the desired unstable
multiplier is positive, a validated local cone estimate will also preserve
the sign of (1.2) between successive returns.

## 2. The selected numerical target

The earlier three-mesh diagnostic located the common second/third-return
root near

\[
 J_*^{\rm num}=0.3011353370869.
\]

The source-bound target now selects

\[
 I_J=[0.30113,0.30114]                                  \tag{2.1}
\]

on the 180-step finite section and samples nine equally spaced amplitudes.
At the two endpoints, its third-return linear coordinates are approximately

\[
 \widehat g_3(0.30113)=7.44\times10^{-5},\qquad
 \widehat g_3(0.30114)=-6.50\times10^{-5}.              \tag{2.2}
\]

Across the sample ladder the centered derivative stays between roughly
\(-14.0\) and \(-13.9\).  The largest sampled reduced-state sup distance at
the two endpoints is about \(1.05\times10^{-4}\).  These are feasibility
observations only: the mesh sup is not the continuous history norm, and the
finite left eigenvector is not yet the RFDE Riesz covector.

The proposed directed calculation should target

\[
 E_H\le3\times10^{-5},\qquad
 E_{H'}\le5,
 \qquad R_Y\ge2\times10^{-4}.                           \tag{2.3}
\]

Here \(E_H\) and \(E_{H'}\) are total errors relative to the numerical
coordinate and derivative, while \(R_Y\) is a **continuous reduced-history
radius** for the stable graph.  Satisfying (2.3) would leave strict endpoint
sign and derivative margins.  The current target artifact records (2.3) as
requested bounds, never as proved bounds.

## 3. Required directed error decomposition

Let \(\widehat\ell\), \(\widehat B_3\), and \(\widehat\gamma_i\) be the
stored numerical objects.  Suppose a directed calculation gives

\[
 \|\ell_u-\widehat\ell\|\le E_\ell,
 \quad
 \|B_3-\widehat B_3\|_Y\le E_B,
 \quad
 \|\gamma_i-\widehat\gamma_i\|_Y\le E_\gamma.          \tag{3.1}
\]

Put \(E_x=E_B+E_\gamma\),
\(\widehat x=\widehat B_3-\widehat\gamma_i\), and assume the validated
stable graph satisfies

\[
 |h(z)|\le C_h\|z\|^2,
 \qquad \|Dh(z)\|\le L_h                              \tag{3.2}
\]

on the required radius.  Then a sufficient endpoint error is

\[
 E_H=
 E_\ell(\|\widehat x\|_Y+E_x)
 +\|\widehat\ell\|E_x
 +C_h\|P_s\|^2(\|\widehat x\|_Y+E_x)^2.               \tag{3.3}
\]

No term in (3.3) may be replaced by binary64 mesh convergence.  In
particular, the orbit-reference error and the interpolation error between
history nodes must be enclosed in the declared \(Y\)-norm.

For the derivative, let \(x'=\partial_J(B_3-\gamma_i)\) and enclose
\(\|x'-\widehat x'\|_Y\le E_{x'}\).  A sufficient derivative error is

\[
 E_{H'}=
 E_\ell(\|\widehat x'\|_Y+E_{x'})
 +\|\widehat\ell\|E_{x'}
 +L_h\|P_s\|(\|\widehat x'\|_Y+E_{x'}).                \tag{3.4}
\]

The section time is part of this derivative.  If
\(e(\phi)=\phi_v(0)-v_i(0)\), the event correction is

\[
 t_3'(J)=
 -\frac{De\,D_J\Phi_{t_3(J)}K(J)}
         {De\,f(B_3(J))},                              \tag{3.5}
\]

and the denominator must be bounded away from zero on the entire pulse
box.  Differentiating a fixed-time flow while omitting (3.5) does not prove
transversality on the Poincare section.

## 4. Conditional crossing lemma

> **Lemma 4.1 (directed third-return crossing).**  Assume the inner Floquet
> dichotomy and the stable graph (1.1) have been validated on a ball
> containing \(B_3(I_J)\).  If directed enclosures prove
> \[
> \begin{aligned}
>  &\widehat g_3(0.30113)-E_H(0.30113)>0,\\
>  &\widehat g_3(0.30114)+E_H(0.30114)<0,\\
>  &\sup_{J\in I_J}\widehat g_3'(J)+E_{H'}(J)<0,
> \end{aligned}                                        \tag{4.1}
> \]
> then there is a unique \(J_c\in I_J\) with
> \(B_3(J_c)\in W^s_{\rm loc}(\gamma_i)\).  Moreover the intersection is
> transverse and its orientation is fixed by the sign in (4.1).

The proof is the intermediate value theorem plus strict monotonicity of the
exact gap (1.2).  Membership in the stable manifold gives convergence to
the inner cycle in the full RFDE history space through the already proved
reduced-history lift.

Lemma 4.1 proves a unique **local pulse separator intersection**.  It does
not identify the two asymptotic destinations.

## 5. From the crossing to biological onset

Three additional enclosures are required before \(J_c\) is a biological
onset threshold:

1. a positive unstable-cone expansion that carries the two signs of
   \(\mathcal H_3\) to disjoint local exit faces;
2. a method-of-steps enclosure carrying the negative face into the proved
   quiet Razumikhin basin;
3. a nonlinear attracting tube carrying the positive face to the outer
   periodic orbit.

Only their conjunction yields

\[
 J<J_c\Rightarrow E_q,
 \qquad J=J_c\Rightarrow\gamma_i,
 \qquad J>J_c\Rightarrow\gamma_o,                       \tag{5.1}
\]

up to the chosen orientation.  The proved \(J=0.30\) quiet capture is the
strict quiet-side anchor; the corresponding outer-side attachment remains
open.

## 6. Reproducibility and claim boundary

The target is generated by
`experiments/leaky_pulse_separator_validation_target.py` and binds the
periodic-orbit artifact and the earlier separator candidate by hash.  Its
claim ledger deliberately leaves the continuous history tube, directed
endpoint signs, Riesz covector, stable graph, separator, onset, and routing
flags false.

This contract is the model-specific input to the general Lyapunov--Perron
route in `docs/leaky-pulse-onset-proof-route.md`.  It should be replaced by a
directed certificate, not cited as if the requested error budget (2.3) had
already been achieved.
