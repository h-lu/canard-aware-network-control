# Inner stable manifold Stage 2: spectral ingress and executable norm gates

## 1. Strict result

Stage 1 proves qualitative existence of the center inner orbit's local
\(C^1\), codimension-one stable manifold and exposes a quantitative
Lyapunov--Perron contract. Two independently registered left-strip artifacts
now supply a baseline theorem and its source-bound extension:

\[
r(L_s)\le \bar\rho_s
=0.999000499833374991668055357167655974702355902361104908<1.
\]

\[
r(L_s)\le \bar\rho_s^{\rm strong}
=0.99004983374916805357390597718003655777207908125490723<1.
\]

Stage 2 source-binds this number and proves three limited quantitative facts.

- On the one-dimensional unstable eigenspace,
  \(\|L_u^{-n}\|\le\rho_u^n\), with intrinsic dichotomy constant
  \(K_u=1\) and
  \(\rho_u\le0.549712198641301272665939640424\).
- A nonconstant Fourier mode gives an existential affine history section
  with pointwise physical-time speed greater than
  \(0.0591798839620661\) at some orbit phase.
- More strongly, an RFDE vector-field replay identifies phase
  \(\theta_*=0\) and the voltage component. The resulting section is exactly
  anchored at the true orbit value \(V(0)\) and has pointwise physical-time
  speed at least \(0.246926966042201268\) on the validated orbit. Polynomial
  field bounds then give uniform speed at least \(0.206753913748020768\) on
  its declared radius-\(0.01\) max-norm section ball. This ball also proves a
  unique nearby true-orbit crossing of the old binary64 pulse level.

The declared reduced-history norm is
\(\|(\phi,w)\|_Y=\max(\|\phi\|_\infty,|w|)\). All these sections are affine,
so their defining functions have exact
\(C^2\) constant zero. These results are not yet a quantitative stable graph.
No stable or unstable Riesz-projection norm, numerical stable dichotomy
constant, full return-flow tube, return-map \(C^2\) bound, nonlinear
remainder, or continuous-history return ball has been validated. Separator,
onset, and routing flags therefore remain false.

## 2. A spectral radius is not a power bound at its boundary

The left-strip result bounds \(r(L_s)\), whereas the Stage-1 sequence
argument requires

\[
\|L_s^n\|\le K_s\rho_s^n \qquad(n\ge0).
\]

One must not insert \(\bar\rho_s\) as the power rate without controlling
Jordan growth or a resolvent on that boundary. For each spectral parent,
Stage 2 selects the strictly larger working rate

\[
\widehat\rho_s=\frac{1+\bar\rho_s}{2}
=0.999500249916687495834027678584
\]

and then optimizes the scalar kernel in the sequence weight. Under the
explicitly optimistic substitution \(p_s=p_u=K_s=K_u=1\),

\[
C_\beta(\beta)=\frac{1}{\beta-\widehat\rho_s}
+\frac{\rho_u}{1-\beta\rho_u},
\]

with derivative

\[
C_\beta'(\beta)=-\frac{1}{(\beta-\widehat\rho_s)^2}
+\frac{\rho_u^2}{(1-\beta\rho_u)^2}.
\]

Its stationary point is above \(1.407\) for both rows, so directed arithmetic
proves that this optimistic kernel is strictly decreasing throughout the
admissible interval \((\widehat\rho_s,1)\). Instead of using a second
midpoint mechanically, the executable row chooses

\[
\beta=1-\frac{1-\widehat\rho_s}{8}.
\]

The spectral-radius formula proves that some finite \(K_s\) exists at this
strict rate. It supplies no numerical upper bound for \(K_s\), so the stable
dichotomy gate remains open.

For the baseline \(\gamma=10^{-3}\) row, this gives

\[
\beta=0.9999375312395859369792534598229784984\ldots,
\qquad
C_\beta=2288.078042128990\ldots,
\]

and the sufficient scalar threshold for the Stage-1 seed radius
\(r=2\times10^{-4}\) is only

\[
C_N<1.0926200741272891581\ldots .
\]

The old \(C_N=10\) discriminant has the directed upper bound
\(-8.1523121685\ldots<0\). Even the fixed-working infimum as
\(\beta\uparrow1\) permits only \(C_N<1.2486134344\ldots\). This is the
honest-failure row.

The strengthened \(\gamma=10^{-2}\) parent instead gives

\[
\bar\rho_s^{\rm strong}
=0.99004983374916805357390597718003655777\ldots,
\]

with working rate

\[
\widehat\rho_s^{\rm strong}
=0.99502491687458402678695298859001827889\ldots .
\]

The same fixed near-unit rule gives

\[
\beta^{\rm strong}
=0.99937811460932300334836912357375228486\ldots,
\qquad
C_\beta=230.9360662340596715\ldots .
\]

Consequently the sufficient threshold is

\[
C_N<10.825506993204714023\ldots,
\]

and the old \(C_N=10\) scalar discriminant has the directed lower bound
\(0.0762557350637613\ldots>0\). The fixed-working infimum at
\(\beta\uparrow1\) has threshold supremum at least
\(12.3626223034759625\ldots\). Thus the strengthened gap plus this explicit
weight removes the *spectral-gap-only* obstruction. At the selected rates the
actual missing constants must satisfy the explicit budget

\[
K_s C_N\left(
229.716190473016\,K_sp_s
+1.219875761044\,K_up_u
\right)<2500.
\]

This is not RFDE evidence: the substitutions
\(p_s=p_u=K_s=K_u=1\) are optimistic placeholders, and the required
projection and stable-power constants remain unknown. The Stage-2 partial
adapter uses the strengthened working rate and explicit near-unit weight,
but still emits no graph constant.

## 3. The phase-bordered inverse and Route B

The periodic-orbit proof uses the affine phase condition

\[
\ell(y)=\langle D_{\rm phase}X_{\rm ref},y\rangle_{\rm mean}
\]

on whole-period Fourier profiles. Its bordered derivative satisfies

\[
\mathcal B(y,\sigma)=(\mathcal Ly-b\sigma,\ell(y)),
\qquad \|\mathcal B^{-1}\|\le120.310184292034788290719619642.
\]

The nonconstant-mode lower bound \(m\) implies

\[
\|X'\|_\infty\ge2\pi m>6m
=1.07625838629800229815\ldots .
\]

Since \(\mathcal B(X',0)=(0,\ell(X'))\), the inverse estimate yields

\[
|\ell(X')|\ge\frac{6m}{\|\mathcal B^{-1}\|}
\ge0.00894569643153024963\ldots .
\]

The range obstruction already proved in the Floquet transfer also makes
\(\mathcal B^{-1}(0,1)\) a normalized phase vector. Thus the BVP phase
condition has exact \(C^2=0\) and quantitative transversality in the
whole-period Wiener space.

This functional is not a functional on one RFDE history: it pairs against a
profile over an entire period, whereas a Poincare section lives in
\(C([-r,0])\times\mathbb R\). The BVP inverse is therefore not, by itself, a
history-section or Riesz-projection norm.

There is nevertheless an exact abstract pullback. Let

\[
\mathcal E_\gamma:C([-r,0],\mathbb R^2)
\longrightarrow C([0,T],\mathbb R^2)
\]

map an initial variational history at the chosen orbit phase to its
finite-time variational trajectory. This trajectory need not be periodic;
the mean-pairing formula defining \(\ell\) extends verbatim to continuous
profiles on \([0,T]\). Smooth RFDE theory makes \(\mathcal E_\gamma\) bounded
and linear. Hence

\[
\ell_H=\ell\circ\mathcal E_\gamma
\]

defines an affine history section, with \(C^2=0\), whose pointwise physical
orbit speed obeys

\[
|\ell_H(\dot p_0)|=\frac{|\ell(X')|}{T}
\ge0.000491894217520404522\ldots .
\]

The current artifacts do not register an operator representation or norm
for \(\mathcal E_\gamma\). Route B is therefore a valid abstract interface,
but not yet an executable quantitative return section.

## 4. Route C: explicit point evaluation at phase zero

An unweighted Wiener correction ball does not directly control the
derivative of an arbitrary corrected Fourier series. Here that missing
operation is unnecessary. The Floquet-transfer proof already derives a
source-bound tangent correction from the RFDE vector-field identity
\(X'=T F(X,X_{\tau_0},X_{\tau_1})\), including delay-shift changes.

At normalized phase \(\theta_*=0\), directed point evaluation gives

\[
V_{\rm cand}(0)\in
[0.905393843282120025506287674943450838327407828420743243,
 0.905393843282120025506287674943450838327407845269167748]
\]

and

\[
V'_{\rm cand}(0)\ge
4.49125235059806734348456083838335610804702518973850728.
\]

The replayed global normalized-tangent correction is at most

\[
5.8423478375391683980816381943863793110453102822201369\times10^{-4},
\]

so the true validated orbit satisfies

\[
V'(0)\ge
4.49066811581431342664475267456391747011592065870720491.
\]

Using the period upper bound

\[
T\le18.1862199491279209928507043514400720596313476562736539
\]

gives the physical-time speed

\[
\dot V(0)=\frac{V'(0)}{T}
\ge0.246926966042201268440571312807745794383056108957168589.
\]

Therefore

\[
h_C(\phi)=\phi_v(0)-V(0)
\]

is an explicit affine history section with functional norm one, a split
chart-projection bound two, and exact \(C^2=0\). It uses the same history
evaluation functional and positive orientation as the registered section
`v=v_inner(0), positive crossing`.

The old pulse code, however, fixes the binary64 candidate level

\[
V_{\rm pulse}=0.90539384328211869,
\]

whereas the exact value \(V(0)\) is only enclosed in the validated interval
displayed above. The old level lies inside that enclosure, but equality with
the true \(V(0)\) is not proved. Consequently the old pulse target must be
re-shot before it can be transferred to the exact Route-C section.

The old level is nevertheless an admissible local orbit section in its own
right. Its height error from \(V(0)\) is at most

\[
1.0000000001332268\times10^{-5}.
\]

The global physical history-speed upper bound is
\(0.406372541022351568\ldots\). Taking a symmetric time bracket of radius

\[
9.6733356288671430\times10^{-5}
\]

moves the orbit history by at most
\(3.9309779796647881\times10^{-5}\), well inside the radius-\(0.01\)
section ball. The uniform positive speed therefore brackets the old level on
both sides and proves one unique local true-orbit crossing, with speed at
least \(0.206753913748020768\ldots\).

This narrow result is orbit-section admissibility only. It is not
transversality of the pulse endpoint map \(K(J)\) to \(W^s\), does not
validate a first-return map, and does not prove a pulse separator or onset.

No additional first-order weighted Fourier-tail bound is required for the
pointwise speed because the RFDE identity supplies the tangent correction.
Moreover, the polynomial reduced RFDE closes the local section-speed seam.
On the max-norm ball of radius \(R=0.01\) centered at the exact phase-zero
history, the orbit sup bounds and correction radius give

\[
L_F\le4.0173052294180499554\ldots .
\]

Thus

\[
a_{\rm section}\ge
0.2469269660422012684\ldots
-4.0173052294180499554\ldots\times0.01
\ge0.2067539137480207688\ldots>0.
\]

This is a source-bound uniform speed on a declared *section ball*. It is not
a full return-flow tube: no current artifact proves that nearby histories
remain in a controlled orbit tube for one complete return or that their
return endpoints lie in this section ball. Route C therefore still does not
validate the first-return map or a pulse crossing.

## 5. Riesz projections and dichotomy constants

The phase-fixed return map has a qualitative splitting

\[
E^s\oplus E^u,\qquad \dim E^u=1.
\]

On the unstable eigenline the restriction is scalar multiplication, so
\(K_u=1\). Projection onto that line still requires a norm bound. A minimal
history-space certificate can use

\[
P_u=\frac{1}{2\pi i}\int_{\Gamma_u}
(zI-M_\Sigma)^{-1}\,dz,
\]

which gives

\[
\|P_u\|\le
\frac{\operatorname{length}(\Gamma_u)}{2\pi}
\sup_{z\in\Gamma_u}\|(zI-M_\Sigma)^{-1}\|.
\]

On the phase section \(P_s=I-P_u\), hence
\(\|P_s\|\le1+\|P_u\|\). A resolvent circle at the declared working rate
would also give

\[
K_s\le\widehat\rho_s
\sup_{|z|=\widehat\rho_s}\|(zI-L_s)^{-1}\|.
\]

The existing left-strip cells prove zero-freeness of a Fourier
characteristic pencil. Their Neumann constants are not resolvent bounds for
the history-section monodromy in the declared continuous norm. Likewise,
the local unstable Grushin border does not contain a validated RFDE adjoint
eigenhistory or Riesz covector. Neither object can be substituted for the
displayed projection or power bounds.

## 6. Executable return-map \(C^2\) interface

For an affine history section let \(H=\|Dh\|\), let \(Q\) bound the section
chart projection, and let \(a>0\) bound \(|DhF|\) from below on a return tube.
Let \(F_0,F_1\) bound \(\|F\|,\|DF\|\), and let \(U_1,U_2\) bound the first
two state derivatives of the RFDE flow over the full return-time window.
Implicit differentiation of the event equation gives

\[
\tau_1=\frac{HU_1}{a},
\]

\[
\tau_2=\frac{H}{a}
\left(U_2+2F_1U_1\tau_1+F_1F_0\tau_1^2\right),
\]

and the first-return bound

\[
M_2=Q\left(
U_2+2F_1U_1\tau_1+F_1F_0\tau_1^2+F_0\tau_2
\right).
\]

For \(P(x)=Lx+N(x)\), Taylor's theorem then permits

\[
C_N=M_2,\qquad
\|DN(x)\|\le C_N\|x\|,\qquad
\|N(x)\|\le\tfrac12C_N\|x\|^2.
\]

The Stage-2 evaluator implements these formulas. For the actual orbit it
uses the radius-\(0.01\) section ball and its uniform event speed, but returns
null because the full return-flow tube, return-time window,
\(F_0,F_1,U_1,U_2\) on that tube, and validated return ball are absent.
The \(10^{-5}\) periodic-BVP correction ball is a whole-profile zero-problem
ball; the periodic-BVP correction ball is not a return-map ball.

## 7. Section-route comparison

Route A retains the old binary64 voltage level and its third-return target.
Its unique local true-orbit intersection and local section-ball speed are now
validated. Its exact reference history, full return-flow tube, stable graph,
and directed pulse-history errors remain open.

Route C uses the exact true-orbit level \(V(0)\). Its pointwise orbit speed is
proved, as is a uniform speed on its local section ball. It still needs a
complete return-flow tube, endpoint containment in the section ball,
return-map \(C^2\), and stable-graph enclosures in the same norm. Because its
level is not proved to equal Route A's binary64 level, it also requires a
fresh pulse re-shoot.

Route B uses \(h_B=(\ell\circ\mathcal E_\gamma)(\phi-p_0)\). It aligns with
the validated BVP phase row and has exact \(C^2=0\), but requires a
source-bound realization and norm for \(\mathcal E_\gamma\), a tube-uniform
speed, and a fresh pulse re-shoot. The old voltage-section signs do not
transfer to Route B.

No route currently proves a pulse crossing.

## 8. Strict boundary

After Stage 2, both numerical stable radii, a strict strengthened working rate
and sequence weight, intrinsic \(K_u=1\), BVP phase pairing, abstract Route B,
and explicit Route-C section-ball speed are available. The Stage-1
Lyapunov--Perron evaluator still receives null stable/unstable projection
norms, null numerical \(K_s\), null full return-flow tube, null return
\(C^2\), null nonlinear remainder, and null return radius. Consequently it
emits no \(q\), no candidate graph radius, and no stable-separator theorem.
