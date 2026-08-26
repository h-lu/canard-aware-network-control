# Stage 4V: orbit-aware logarithmic event tube

Status: **proved explicit scaled reduced-history event tube**.

## Result

In the fixed unit-\(Y\) Route-C coordinates, every history in

\[
 \|x_s\|_Y\le0.0097\lambda_0,
 \qquad |x_u|\le0.00025\lambda_0,
 \qquad \boxed{\lambda_0=1.2\times10^{-8}},
\]

including every arbitrary continuous stable history satisfying the norm
bound, has one unique positive-oriented event in the fixed physical window
near \(2P\).  The theorem holds on the strictly larger open scale
\(1.25\times10^{-8}\); the selected event time and complete reduced-history
hit are \(C^2\), and the hit remains in the declared local section patch.

This improves the scalar complete-history Gronwall scale
\(9\times10^{-31}\) by about 22 decimal orders.  It still does **not** prove
the preferred unscaled ball \(\lambda=1\), a same-ball self-map, an event
ordinal, Hessian blocks, a stable graph, pulse crossing, biological onset,
routing, capture, safety, or a general-network canard theorem.

## 1. The weighted-energy cancellation

Write \(x=\eta_v(t)\), \(y=\eta_w(t)\) for the difference from the exact
periodic orbit and set

\[
 z(t)^2=x(t)^2+\varepsilon^{-1}y(t)^2.
\]

With \(a(t)\) the current variational coefficient and \(b_j(t)\) the two
delayed coefficients, the difference equation gives the exact identity

\[
 \frac12\frac{d}{dt}z^2
 =a(t)x^2-y^2+\sum_{j=0}^1b_j(t)x(t)x(t-\tau_j)+x(t)N(t).
\]

The two instantaneous cross terms cancel: \(-xy+yx=0\).  Consequently the
instantaneous logarithmic rate is \(\max\{a(t),-\varepsilon\}\), not the
absolute row sum used by the scalar construction.

Let

\[
 Z(t)=\max\left\{
  \sup_{-\tau_{\max}\le\theta\le0}|\eta_v(\theta)|,
  \sup_{0\le s\le t}z(s)
 \right\}.
\]

Before a delay activates, its voltage is the exact translate of the initial
continuous history; afterwards it is a previous value of \(x\).  Both are
bounded by \(Z\).  At every time at which this envelope increases,

\[
 D^+Z(t)\le
 \left[r(t)+\frac12H_\beta Z(t)\right]Z(t),
 \quad
 r(t)=\max\{0,\max(a(t),-\varepsilon)+|b_0(t)|+|b_1(t)|\}.
\]

The polynomial fast-field Hessian gives

\[
 H_\beta=2(1+B+\beta)
 +12\varepsilon\kappa_3(B+\beta),
 \qquad B=\sup_t|v_*(t)-1|.
\]

## 2. Directed orbit integral

Stage 4V reuses the Stage-4I delay-aligned physical partition.  On each of
its 1042 cells, a 192-bit Taylor--Bernstein enclosure supplies an upper bound
for \(a\) and modulus bounds for \(b_0,b_1\).  Analytic Fourier tails and the
validated exact-orbit coefficient errors are added before the maximum and
the integration.  The result is

\[
 \int_0^{P_{\rm bin}}r(t)\,dt
 \le 6.353397548471471,
 \qquad
 \sup r(t)\le0.774979654297290.
\]

The true-period interval is handled by multiplying the one-binary-period
integral by \(P_+/P_{\rm bin}^-\).  Here \(P_{\rm bin}^-\) is the lower
endpoint obtained by inserting the exact binary64 period directly into MPFR;
it is not a rounded display decimal.  Two exact periods use twice this
rescaled integral, and the remaining event-window phase offset uses the
directed global rate maximum.  No sampled time maximum is promoted.

There is a second, distinct period correction in each delayed coefficient.
The delayed dictionaries use the binary centers \(P_{\rm bin},\tau_j^{\rm
bin}\), whereas the exact delayed phase uses \(P,\tau_j\).  Stage 4V inserts
the explicit argument bridge

\[
 \delta v_{\rm del}
 \le E_v+\|\dot Y_*\|_\infty
 \left(
  \tau_{\max}\frac{|P-P_{\rm bin}|}{P_-}
  +|\tau_j-\tau_j^{\rm bin}|
 \right),
\]

and propagates its additional phase part through the coefficient slope
\(3\varepsilon\kappa_3(V+1)\).  This contribution is added to the inherited
Stage-4I coefficient error.  The \(10^{-8}\) binary-algebra guard controls
rounded dictionary operations; it is not used as a proof of this phase
bridge.

## 3. Explicit scale

Choose \(\beta\) to be half the certified center endpoint gap.  Since
\(\varepsilon=1/5\), an initial reduced-\(Y\) radius \(\rho\) satisfies

\[
 Z(0)\le\sqrt{1+\varepsilon^{-1}}\,\rho=\sqrt6\,\rho.
\]

On a hypothetical first-exit interval \(Z\le\beta\), the preceding
inequality gives

\[
 Z(t)\le Z(0)\exp\left(
   \int_0^t r(s)\,ds+\frac12H_\beta\beta t
 \right).
\]

The directed construction ceiling is approximately
\(1.2770\times10^{-8}\).  The open scale \(1.25\times10^{-8}\) lies strictly
below it, so the bound is strictly below \(\beta\) through \(T_+\).  This
proves the common solution tube, endpoint signs, positive event speed, unique
selected event in the fixed window, and complete returned-history patch
containment.  The Stage-4R theorem is then applied directly on this explicit
open ball, using the exact full-/reduced-history bridge proved in Stage 4S-A
and the strict smoothing margin.  The argument does not assume that the
unspecified qualitative Stage-4S-A neighborhood already contains this ball.

## 4. What this says about the preferred ball

For \(\lambda=1\), the weighted initial energy radius is already about 236
times \(\beta\).  Thus the hypothesis \(Z\le\beta\) fails at \(t=0\), and
the sufficient comparison is inapplicable.  One may record the formal
exponential right-hand side obtained by ignoring this failure, but that
number is **not** a validated flow bound.  This is a no-go only for the
weighted-energy full-time half-gap construction, not a lower bound on the
true flow.

There is also a source-bound warning about the fixed \(\pm10^{-3}\) window:
the sampled current-state row norm \(0.0373895\), multiplied by
\(R_s=0.0097\), exceeds the center endpoint gap.  Because this parent field
is a sampled maximum and no directed lower witness for the relevant event
functional is available, Stage 4V does not claim that the fixed window
excludes the preferred ball.

The next sharp route should separate a broad global boundedness tube from a
terminal event-time tube, validate the signed fixed-time event functional and
its nonlinear second variation, and, if necessary, enlarge the center event
window.  Terminal phase-fixed contraction alone cannot control event-time
drift.

## Reproduction

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_logarithmic_event_tube_stage4v.py

OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 -m pytest -q \
  tests/test_leaky_inner_logarithmic_event_tube_stage4v.py
```
