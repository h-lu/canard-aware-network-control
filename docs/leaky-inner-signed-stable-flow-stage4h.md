# Stage 4H: signed stable flow on the inner Route-C return

## Outcome

Stage 4H removes a structural ambiguity in the missing stable-power ingress.
On one inner period the Volterra expansion is **exactly finite**, and the
stable row must be formed as a signed continuous-history measure before any
total variation is taken.  The source-bound calculation implements this
order and finds a phase-fixed one-step stable-map norm near
\(4\times10^{-3}\),
far below the declared strong rate

\[
 \rho_s=\frac{1+e^{-0.01}}2=0.9950249168\ldots .
\]

This is strong numerical evidence, not yet the directed inequality
\(\|L P_s\|<\rho_s\).  The current artifact therefore does not prove
\(K_s=1\), a stable graph, a split return tube, a separator crossing, or
pulse onset.

The executable source is
[leaky_inner_signed_stable_flow_stage4h.py](../src/canard_control/leaky_inner_signed_stable_flow_stage4h.py),
the generator is
[leaky_inner_signed_stable_flow_stage4h.py](../experiments/leaky_inner_signed_stable_flow_stage4h.py),
and the registered result is
[leaky_inner_signed_stable_flow_stage4h.json](../experiments/results/leaky_inner_signed_stable_flow_stage4h.json).

## 1. Exact four-word reduction

Let \(F(t,s)\) be the fundamental matrix of the current two-dimensional ODE
and let \(B_j(t)=b_j(t)e_1e_1^T\).  The center period and delays satisfy

\[
 2\tau_0<T<\tau_0+\tau_1,
 \qquad T<3\tau_0.
\]

Every mixed word and every word of length at least three is therefore
time-inactive on \(0\le t\le T\).  The current-state resolvent contains
exactly

\[
 \varnothing,\quad (0),\quad (1),\quad (0,0),
\]

and the initial-voltage history density contains
\((0),(1),(0,0)\).
This is a support theorem, not a numerical truncation.

Writing \(F(t)=F(t,0)\),

\[
 a_j(r)=F(r)^{-1}e_1b_j(r),
 \qquad
 C_j(t)=\int_{\tau_j}^{t}
 a_j(r)e_1^TF(r-\tau_j)\,dr,
\]

the atom is

\[
 R(t,0)=F(t)\{I+C_0(t)+C_1(t)+C_{00}(t)\}.
\]

For an initial history point \(\theta\), the one-delay density is
\(F(t)a_j(\theta+\tau_j)\) on its active triangle.  The only two-delay term is

\[
 F(t)\{C_0(t)-C_0(\theta+2\tau_0)\}a_0(\theta+\tau_0).
\]

These formulas replace an uncontrolled finite-node history discretization
by atom-plus-density rows on the declared Banach space.

## 2. Stable deflation and event projection

On the Route-C section \(\Sigma=\{\phi_v(0)=0\}\), the current-voltage atom
does not act.  Hence the norm of a row is the modulus of its current-recovery
atom plus the total variation of its voltage-history density.

Let \(q\) be the Stage-3 section eigenhistory and \(f\) the Stage-4D
atom-plus-density covector.  Stage 4H forms

\[
 S_i(t)=R_i(t)-q_i(t)\frac{f}{f(q)}
\]

as one signed measure and only then evaluates its total variation.  Separate
bounds for \(R_i(t)\) and the rank-one term are recorded solely to exhibit
the cancellation loss; they are not used as a proposed certificate.

For \(T-\tau_1\le t\le T\), the phase-fixed voltage-history row is

\[
 S_v(t)-\frac{\dot v(t)}{\dot v(T)}S_v(T),
\]

and the recovery row is

\[
 S_w(T)-\frac{\dot w(T)}{\dot v(T)}S_v(T).
\]

Thus both the unstable deflation and the Route-C event correction occur
before total variation.

## 3. What the diagnostic establishes

The artifact reports nested output-time grids, direct versus
quadrature evaluations of \(f(q)\), and reconstruction of the Stage-3
unstable flow from the exact four words.  It also reports the unstable
history separately: the phase-fixed expansion agrees with the expected
multiplier \(e^{s_u}\) to the displayed binary accuracy.

The intermediate full-history flow is not expected to have norm below one:
at early times it still contains the non-isometric stable projection on the
unadvanced part of the history.  This quantity is useful for a return-tube
majorant, whereas the much smaller phase-fixed one-step row is the relevant
candidate for proving \(K_s=1\) by submultiplicativity.

The same diagnostic also tests the linear part of the Stage-4B split tube.
Stage 4E divides its (q,q) output by \(\|q^\Sigma\|_Y^2\), so the unstable
coordinate used there corresponds to the unit-(Y) vector
\(q^\Sigma/\|q^\Sigma\|_Y\).  With (R_s=10^{-3}) and
\(R_u=7\times10^{-4}\), Stage 4H therefore records

\[
 M_sR_s+
 \frac{\max_{0\le t\le T}\|U(t)q^\Sigma\|_Y}
      {\|q^\Sigma\|_Y}R_u .
\]

Its sampled value is below the section radius (10^{-2}), leaving a
separate margin for nonlinear and directed errors.  Because both flow
factors are sampled, this is a budget diagnostic, not a validated return
tube.

All computed values remain diagnostics because DOP853 and Gauss--Legendre
quadrature are not outward rounded and a finite output-time grid does not
enclose a continuous supremum.

## 4. Smallest remaining rigorous gate

The missing object is now specific: a common outward piecewise-polynomial
enclosure of the two-variable signed density \(S(t,\theta)\) on its three
support triangles.  It must include

1. residual bounds for \(F,C_0,C_1,C_{00}\);
2. the validated orbit and Stage-3 \(q\) errors;
3. the Stage-4D adjoint-row, density-basis, and normalization errors;
4. outward absolute integrals on every triangle; and
5. the continuous output-phase supremum.

Only after their combined error is smaller than the recorded margin to
\((1+e^{-0.01})/2\) may one assert \(\|LP_s\|<\rho_s\) and hence
\(K_s=1\).
The present diagnostic shows a large margin and no structural obstruction,
but deliberately leaves every such proof flag false.

## 5. Replay

Generate the source-bound artifact with

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_signed_stable_flow_stage4h.py
```

The fast static audit is

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_signed_stable_flow_stage4h.py --check
```
