# Stage 4S-A: qualitative near-two-period event tube

## Result

This certificate proves the smallest common-full-ball event theorem supported
by the current artifacts.  It does not validate the preferred Stage-4N ball.
There exists an unspecified \(\lambda_*\in(0,1]\) such that every history in

\[
 B_{\lambda_*}=\{\|x_s\|_Y\le 0.0097\lambda_*,\quad
 |x_u|\le 0.00025\lambda_*\},
\]

including every continuous stable history satisfying the norm bound, has one
unique positive-oriented exact phase-zero voltage event in the same fixed
physical-time window.  The event time and complete-history hit are \(C^2\) on
an open neighborhood of this closed ball in the reduced history space, through
the exact full-history lift/projection bridge below.  Both the injected initial
history and the hit lie in one fixed local patch of the exact phase-zero
section.

No numerical lower bound for \(\lambda_*\) is obtained.  In particular,
\(\lambda_*=1\), a self-map of the same scaled anisotropic ball, and an
effective nonlinear-flow remainder are not proved.

## Exact-center arithmetic

The true period enclosure is

\[
18.1862099491259209928507043514802987643728364255154943129826431
\le P\le
18.1862099491299209928507043513998453548898588869845056870173569.
\]

With \(h=10^{-3}\), the common center window is

\[
I=[36.3714198982518419857014087029605975287456728510309886259652862,
36.3734198982598419857014087027996907097797177739690113740347138].
\]

The maximum phase offset from \(2P\) is at most
\(0.0010000000079999999999999998390931810340449229380227480694276\).
Multiplication by the validated physical orbit-history speed gives a history
displacement at most
\(0.000406372544273331895877834683363911344159153488734618242548\)
(rounded upward),
strictly inside the declared section-ball radius
\(0.00999999999999999999999999999999999999999999999998246666\).
Therefore the
validated ball speed applies throughout the center window:

\[
\partial_t g_Y(\Psi_tY_*)\ge
0.206753913748020768886579840564112686146218775927720324.
\]

Both center endpoint gaps are at least
\(0.000206753913748020768886579840564112686146218775927720324\).
The strict smoothing margin is

\[
T_- - 2\tau_{\max}\ge
14.0107401232539450216096720156478351743394892549157313832472982>0.
\]

## Full-history to reduced-history \(C^2\) bridge

Stage 4R is a theorem on

\[
X=C([-r,0],\mathbb R^2),
\]

whereas the Stage-4N coordinates belong to

\[
Y=C([-r,0],\mathbb R)\times\mathbb R.
\]

These spaces are not identified.  The exact reduced-history certificate
supplies the bounded projection

\[
\pi(\phi_v,\phi_w)=(\phi_v,\phi_w(0))
\]

and the compatible affine lift \(\mathcal I(q,\omega)=(q,\mathcal R(q,\omega))\),
where

\[
\mathcal R(q,\omega)(\theta)=e^{-\varepsilon\theta}
\left[\omega-\varepsilon\int_\theta^0e^{\varepsilon s}(q(s)-a)\,ds\right].
\]

The lift is affine \(C^\infty\), its derivative is a continuous linear split
right inverse of \(\pi\), and \(\pi\mathcal I=I_Y\).  The exact semiflow
factorization is

\[
\Psi_t=\pi\Phi_t\mathcal I\quad(t\ge0),\qquad
\Phi_t=\mathcal I\Psi_t\pi\quad(t\ge r).
\]

The full periodic center is compatible, so
\(X_*^X=\mathcal I(Y_*)\); this follows by applying the recovery ODE identity
on every length-\(r\) segment of the periodic solution.

Apply Stage 4R only to the full semiflow \(\Phi\) on \(X\), using the initial
parameterization \(\mathcal I:W\subset Y\to X\) and
\(g_X=g_Y\circ\pi\).  Since its full segment map is jointly \(C^2\) for
\(t>2r\), composition gives the reduced-space corollary

\[
(t,y)\longmapsto\Psi_t(y)=\pi\Phi_t(\mathcal I y)
\quad\text{jointly }C^2\quad(t>2r).
\]

Moreover,

\[
g_X(\Phi_t\mathcal I y)=g_Y(\Psi_t y).
\]

Thus the endpoint signs, speed, selected time, and implicit-function
denominator are the same in both formulations, and

\[
R_Y(y)=\Psi_{T(y)}y=\pi\Phi_{T(y)}\mathcal I y
\]

is \(C^2\).  Because \(T_->2r>r\), the corresponding full hit is compatible:
\(\Phi_{T(y)}\mathcal I y=\mathcal I R_Y(y)\).

## Why a nonzero full ball exists, with the quantifiers in order

The exact center orbit exists on the compact interval \(I\), its endpoint
signs are strict, and its event speed has a strict lower bound.  The maximal
semiflow domain is open and the RFDE solution and physical vector field depend
continuously on the complete continuous initial history, uniformly over a
compact time interval.  Hence first obtain an open ambient neighborhood
\(W\subset Y\) of \(Y_*\) preserving half of both endpoint margins and half of
the speed margin.  The bridge above gives \(C^2\) maps
\(T:W\to\mathbb R\) and \(R_Y:W\to Y\).

Now define the reduced local section patch

\[
\Sigma_{\rm loc}=\{y:g_Y(y)=0,\ 
\|y-Y_*\|_Y<R_{\rm sec}\},
\]

and the initial section injection

\[
j(x_s,x_u)=Y_*+x_s+\widehat qx_u.
\]

The initial chart domain is imposed first:

\[
D_{\rm in}=j^{-1}(W\cap\Sigma_{\rm loc}).
\]

Then impose terminal containment using the already constructed selected hit:

\[
D=D_{\rm in}\cap(R_Y\circ j)^{-1}(\Sigma_{\rm loc}).
\]

Both sets are open in \(E_s\times\mathbb R\), and \(0\in D\) because the
center return is exact.  Consequently

\[
j(D)\subset\Sigma_{\rm loc},\qquad
R_Y(j(D))\subset\Sigma_{\rm loc}.
\]

For the fixed Route-C splitting,
\(\|x_s+\widehat qx_u\|_Y\le\lambda(0.0097+0.00025)\).  Only after the final
domain \(D\) has been formed do we choose \(\lambda_*>0\) with
\(B_{\lambda_*}\subset D\).

Finally define

\[
\chi(y)=\bigl(P_s(y-Y_*),\widehat f(y-Y_*)\bigr),\qquad
D_{\rm out}=\chi(\Sigma_{\rm loc}).
\]

Then \(D_{\rm out}\) is open in \(E_s\times\mathbb R\), and
\(\chi:\Sigma_{\rm loc}\to D_{\rm out}\) is an affine section chart with
inverse given by the restriction of \(j\).  Hence

\[
P_{\rm sel}=\chi\circ R_Y\circ j:D\to D_{\rm out}
\]

is the induced \(C^2\) selected section return.  No claim
\(P_{\rm sel}(D)\subset D\), or self-map of \(B_{\lambda_*}\), is made.

This argument is qualitative: compactness gives no effective modulus of
continuous dependence and hence no numerical \(\lambda_*\).

## Claim boundaries

- **Proved numerically:** the center window, center endpoint signs, center
  positive speed, the \(C^2\) smoothing margin, and the exact center return.
- **Proved qualitatively:** a nonzero scaled ball of arbitrary continuous
  histories with one common selected-event window, the exact full-\(X\) to
  reduced-\(Y\) \(C^2\) bridge, and both initial and terminal section-patch
  containment.
- **Conditional:** Stage-4P graph arithmetic.  Its reference rows still need
  a preferred-domain map and six certified projected Hessian blocks.
- **Corrected nonclosing feasibility row:** Stage 4N now uses
  \(B=\sup|v_*-1|\) and
  \(H_r=2(1+B+r)+12\varepsilon\kappa_3(B+r)\).  The corrected generic
  Gronwall row still fails, more strongly; it is not a lower bound on the true
  nonlinear flow deviation and is not promoted here.
- **Registered but not numerically promoted:** the Stage-4M unit-\(Y\)
  splitting.  Only its qualitative coordinate interface is used because
  \(\lambda_*\) is existential; its continuous-history normalization adapter
  remains open.
- **Diagnostic:** every Stage-4Q finite-grid row; none is used here.
- **Open:** a numerical \(\lambda_*\), the unscaled preferred ball, event
  ordinal or first return, \(Q=P^2\), Hessian blocks, stable graph, pulse-sheet
  crossing, biological onset/control, routing, capture, safety, and a general
  network canard theorem.

The selected event is unique only in this fixed near-\(2P\) window.  That is
not a proof that it is the first return, the second positive-oriented crossing,
or the biological pulse onset.  All times and delays above are physical; no
period normalization or finite-history grid is used.

## Reproduction

```bash
PYTHONPATH=src /usr/bin/python3 experiments/leaky_inner_stage4s_event_tube.py
PYTHONPATH=src /usr/bin/python3 -m pytest -q tests/test_leaky_inner_stage4s_event_tube.py
```
