# Stage 4N feasibility: why a scalar Gronwall tube does not close

Status: **SOURCE-BOUND NONCLOSING PILOT.**

This artifact tests the first generic construction for the nonlinear
selected-return parent required by Stage 4M.  The domain is the complete
preferred-B anisotropic ball

\[
 \|x_s\|_Y\le 0.0097,
 \qquad |\widehat x_u|\le 0.00025,
 \qquad \|x_s\|_Y+|\widehat x_u|\le0.00995.
\]

The calculation proves that two disclosed scalar row-sum/Gronwall routes do
not certify a common flow tube.  It does not prove that the true nonlinear
flow is large.  It also records a quantitative target for the signed
second-variation calculation that must replace them.

The executable source is
[leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py](../src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py),
the atomic generator is
[leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py](../experiments/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py),
and the registered result is
[leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json](../experiments/results/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json).

## 1. The sharper generic test already explodes

Stage 4I supplies source-bound maxima for the exact-orbit current and delayed
variational coefficients, including separate model-error radii.  Before any
modulus is taken over a nonlinear trajectory, the physical fast-field Hessian
rows are

\[
 -(2+6\varepsilon\kappa_3)v+6\varepsilon\kappa_3,
 \qquad
 3\varepsilon\kappa_3(v_{\tau_0}-1),
 \qquad
 3\varepsilon\kappa_3(v_{\tau_1}-1).
\]

The registered amplitude is the centered quantity

\[
 B=\sup_t|v_*(t)-1|\le0.5300579565,
\]

not a bound for \(|v_*|\).  Hence \(|v|\le1+B+r\) in the current
Hessian slot, while every \((v-1)\) factor is bounded by \(B+r\).  On the
input-radius tube the scalar Hessian row is therefore bounded by

\[
 H_r=2(1+B+r)+12\varepsilon\kappa_3(B+r),
\]

and not by the formula obtained by treating \(B\) as \(\sup|v_*|\).
Adding \(H_rr\) to the Stage-4I coefficient row gives

\[
 L_{4I}\le1.806451259683.
\]

The base history belongs to the ball, so any common near-period event horizon
must extend at least through the exact period.  With

\[
 T_->18.1862099491259,
\]

the deliberately optimistic scalar comparison gives

\[
 e^{L_{4I}T_-}\approx1.8520823\times10^{14},
 \qquad
 e^{L_{4I}T_-}r\approx1.8428219\times10^{12}.
\]

The registered exact inner-orbit centered voltage-strip margin is only
(1.9699420435\).  Thus this construction misses its own containment test by
at least

\[
 9.3547\times10^{11},
\]

or about \(11.971\) decimal orders.  This is the first frozen numerical
obstruction.  The Stage-6A-style polynomial row sum is even worse: it misses
by more than (32.25) decimal orders.

These statements concern the disclosed *upper-bound construction*.  They are
not lower bounds on the true nonlinear deviation.

## 2. What Stage 4I and Stage 4L do and do not supply

Stage 4I supplies the four-word algebraic skeleton

\[
 \varnothing,\quad(0),\quad(1),\quad(0,0)
\]

and directed residual tubes for its primitives.  It does not supply the
continuous signed intermediate stable row after rank-one deflation.  Stage
4L proves the selected *terminal linear* stable row

\[
 \|AP_s\|\le0.009896427481610001,
\]

but a terminal row cannot replace a nonlinear base-flow tube, common event
window, or no-earlier-return cover.

The next certificate must enclose the mild remainder

\[
 \eta_t=\mathcal U(t,0)\eta_0+
 \int_0^t\mathcal U(t,s)\mathcal N_s(\eta_s)\,ds
\]

through one continuous signed ((t,s,\theta)) kernel.  Stable deflation or
unstable action, moving-event corrections, and translated-history terms must
be correlated before a norm is taken.  The cover must include every delay
activation, the exact translation of arbitrary initial histories, every
time/history seam, and every returned-history phase
(-\tau_{\max}\le\theta\le0\).

## 3. Quantitative target for the sharp kernel

The Stage-4L stable row and the exact unstable eigen-relation give the
conditional terminal linear image estimate

\[
 \|Ax\|_Y
 \le \rho_s R_s+\mu_u\widehat R_u
 <0.000598609.
\]

If a future event-aligned complete-history second-variation kernel satisfies

\[
 \|R(x)-X_*-Ax\|_Y
 \le \frac12 K_{\rm ret}
       (\|x_s\|_Y+|\widehat x_u|)^2,
\]

then the conditional radius-(0.00995) returned-history gate closes whenever

\[
 \boxed{K_{\rm ret}<188.9122238810.}
\]

This is a design target, not a proved kernel bound.  It also does not replace
the six much more structured projected Hessian caps required by Stage 4M.

## 4. Claim boundary

Every common-event quantity remains open: (T_\pm), both endpoint signs,
the uniform positive speed, the complete flow and returned-history radii,
the launch collar, the middle slab cover, and the no-earlier admissible-return
margin.

An admissible earlier return still means a positive-oriented hit lying in the
local complete-history Route-C patch.  Negative-oriented crossings may remain.
The full history interval ([T_- -\tau_{\max},T_+]\), rather than only an
endpoint or finite history nodes, remains mandatory.

No selected or first return, Hessian block, stable graph, pulse crossing,
onset, routing, capture, or safety statement is proved.

## 5. Replay

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 \
  experiments/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py
```
