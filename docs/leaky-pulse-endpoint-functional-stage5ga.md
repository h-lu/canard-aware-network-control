# Stage 5G-a: source-bound endpoint functional coordinates

Status: **PROVED endpoint theorem / no stable graph or crossing theorem.**

Stage 5G-a evaluates the two exact endpoints of the Stage-5C selected
late-window Route-C event branch in the same complete-history space, Grushin
normalization, and physical phase used by Stages 3, 4D, 4E, 5E, and 5F.  It
proves opposite signs of the fixed functional coordinate.  It does not
replace the missing quantitative stable graph and does not identify the
selected event with an ordinal third crossing or biological onset.

## 1. Registered objects and quantifiers

The history and section spaces are

\[
Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R,
\qquad
\|(\phi,w)\|_Y=\max\{\|\phi\|_\infty,|w|\},
\]

\[
\Sigma=\{y\in Y:y_v(0)=0\}.
\]

Stage 5E fixes

\[
q=q_{\rm phys}=\widetilde q/\gamma,
\qquad
f=f_{\rm phys}=\gamma\ell/\ell(\widetilde q),
\qquad f(q)=1,
\qquad P_s=I-qf.
\]

On the affine Route-C section there is a global bounded linear splitting

\[
\mathcal C:\Sigma\longrightarrow\ker f\times\mathbb R,
\qquad
\mathcal C(\kappa)=(P_s\kappa,f(\kappa)),
\qquad
\mathcal C^{-1}(z,u)=z+qu.
\]

Indeed, \(f(P_s\kappa)=0\), while \(f(q)=1\) gives both inverse identities.
Thus there is no additional ambient-coordinate containment gate on
\(\Sigma\).  A future local stable graph only requires the stable coordinate
\(P_s\kappa\) to lie in its domain; the scalar coordinate
\(f(\kappa)\) need not be bounded by the graph height.

Let \(K(J)\) be the unique selected Route-C event history from Stage 5C and
let \(X_*\) be the exact inner periodic-orbit history at the same section
phase.  Then

\[
\kappa(J)=K(J)-X_*\in\Sigma.
\]

The parameterization is

\[
J=\frac{2409}{8000}+\frac{3}{40000}\xi,
\qquad \xi\in[-1,1],
\]

with

\[
J_-=\frac{6021}{20000},\qquad J_+=\frac{753}{2500}.
\]

The Taylor--Bernstein evaluator requires positively oriented parameter
shards.  Stage 5G-a therefore encloses every parameter in the one-sided
intervals

\[
[-1,-1+2^{-30}],\qquad[1-2^{-30},1].
\]

Each interval contains its exact endpoint.  On each endpoint shard the
certificate encloses every
\(\theta\in[-5\sqrt5,0]\) using 512 directed history cells, not a finite
history sample.

Stage 5C proves one transverse event in a common late window for every
parameter.  Stage 5D proves that the corresponding map \(K:I_J\to Y\) is
continuously differentiable.  Together these facts exclude switching to a
different event inside the selected window.  They do not count earlier
crossings.

## 2. Centered same-row calculation

For \(\sigma\in\{-,+\}\), Stage 5G-a freezes the exact decimal centers

\[
c_-=0.021366541445,
\qquad
c_+=-0.016474080047
\]

and forms

\[
r_\sigma=\kappa(J_\sigma)-c_\sigma q
\]

before applying a norm or absolute value.  The centers are merely convenient
exact rational choices.  No binary64 midpoint is used as proof data.

Let \(\ell_g\) be the same finite-plus-Neumann-tail atom--density guide used
by Stage 4E.  The certificate retains the current recovery atom, the direct
and omitted dictionaries for both delays, the delay seams, the inner-orbit
uncertainty, and all 512 history cells.  The current voltage atom vanishes
only because the following are exact section identities:

\[
K_v(J,0)=X_{*,v}(0)=V_{\rm true}(0),
\qquad q_v(0)=0.
\]

The Stage-4E measure difference gives

\[
|\ell(r_\sigma)|
\le |\ell_g(r_\sigma)|
 +\|\ell-\ell_g\|\,\|r_\sigma\|_Y.
\]

The denominator is the Stage-5E lower bound for the modulus of this same
row applied to the same eigencolumn.  Since \(|\gamma|=1\) and the exact
physical functional is real on real histories,

\[
f(\kappa(J_\sigma))
\in[c_\sigma-\rho_\sigma,c_\sigma+\rho_\sigma].
\]

The public JSON ledger is composable: the measure error, numerator, radius,
functional interval, and projection norm are recomputed outward from the
serialized residual action and norm.

## 3. Direct norm of the physical eigencolumn

For the projection identity

\[
P_s\kappa(J_\sigma)
=r_\sigma+q\bigl(c_\sigma-f(\kappa(J_\sigma))\bigr),
\]

Stage 5G-a evaluates \(q_{\rm phys}\) directly on the same 512 continuous
history cells and at the current recovery coordinate.  This gives a much
sharper source-bound norm than the general Stage-5F Wiener majorant.  The
certificate records both numbers and verifies

\[
\|q_{\rm phys}\|_{Y,\mathrm{direct}}
\le \|q_{\rm phys}\|_{Y,\mathrm{Stage\ 5F}}.
\]

The endpoint projection estimate is then

\[
\|P_s\kappa(J_\sigma)\|_Y
\le \|r_\sigma\|_Y
 +\|q\|_{Y,\mathrm{direct}}\rho_\sigma.
\]

The direct norm cannot be replaced by a smaller asserted number: the entire
proof-bearing numeric core is frozen independently of the certificate
digest, and a fresh replay reconstructs the 512-segment bound.

## 4. The endpoint theorem

The registered result gives strict intervals of the form

\[
f(\kappa(J_-))\subset(0,\infty),
\qquad
f(\kappa(J_+))\subset(-\infty,0).
\]

It also proves that the exact target

\[
\eta_{\rm target}=10^{-3}
\]

is admissible in the following conditional sense: if a future quantitative
stable graph in this identical chart proves

\[
|\psi(P_s\kappa(J_-))|\le\eta_{\rm target},
\qquad
|\psi(P_s\kappa(J_+))|\le\eta_{\rm target},
\]

then

\[
H(J_-)>0>H(J_+),
\qquad
H(J)=f(\kappa(J))-\psi(P_s\kappa(J)).
\]

This is only an arithmetic implication.  Stage 5G-a supplies neither
\(\psi\) nor its endpoint heights, so it does not claim stable-gap signs.

## 5. Exact boundary of the result

Stage 5G-a proves:

- a single continuously differentiable selected-event branch on the pulse
  interval, with no switching inside its registered window;
- source-bound complete-history enclosures at both exact endpoints;
- the direct complete-history norm of the registered physical eigencolumn;
- opposite signs of \(f_{\rm phys}(\kappa(J_-))\) and
  \(f_{\rm phys}(\kappa(J_+))\);
- endpoint bounds on \(\|P_s\kappa(J_\pm)\|_Y\);
- the global affine section splitting
  \(\kappa\leftrightarrow(P_s\kappa,f(\kappa))\);
- admissibility of the conditional graph-height target \(10^{-3}\).

The following remain **OPEN**:

- a quantitative inner stable graph in this registered chart;
- containment of the full stable-coordinate curve
  \(P_s\kappa(I_J)\) in the graph domain;
- actual stable-gap endpoint signs and a selected-event stable-sheet
  crossing;
- identification of the selected event as the ordinal third crossing;
- biological onset, two-sided routing, capture, and any
  frequency--amplitude--safety or asynchronous-network radius.

Endpoint signs and the conditional Stage-5F derivative interval will be
sufficient for existence and uniqueness once the graph, graph height, and
full-interval containment premises are proved.  Interval Newton is optional
and is not claimed here.
