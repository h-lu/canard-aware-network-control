# Stage 4J pilot: common projected residual for the inner stable flow

Status: **source-bound diagnostic / OPEN directed certificate.**

## Outcome

The Stage-4J pilot removes the scalar-forward obstruction exposed by Stage
4I.  It builds the general-start four-word resolvent and, on the complete
history space, forms the same doubly projected object

\[
 \widehat{\mathcal S}(t,s)
   =P_s(t)\widehat{\mathcal U}(t,s)P_s(s)
\]

for both the intermediate-flow norm and the residual.  The current atoms,
propagated voltage-history density, recovery coordinate, and the unadvanced
translation/identity block are retained until both rank-one subtractions
have been made.  Absolute values are taken only afterwards.

The source-bound numbers strongly support a directed upgrade.  On the
declared finite grids they give

| quantity | binary pilot value |
|---|---:|
| \(\widehat K\) | \(17.2564383872\) |
| differential-residual integral supremum | \(1.86133613881\times10^{-6}\) |
| projected initial defect | \(3.09278429273\times10^{-10}\) |
| history-transport boundary defect | \(3.89021461703\times10^{-11}\) |
| activation-jump proxy | \(4.03734665887\times10^{-12}\) |
| accumulated ordinary-seam proxy | \(6.42193199303\times10^{-13}\) |
| combined \(\Delta\) | \(1.86168899892\times10^{-6}\) |
| \(K_{\mathrm{int}}=\widehat K/(1-\Delta)\) | \(17.2564705133\) |
| preprojection \(\Delta_T\) | \(1.86168899892\times10^{-6}\) |
| \(C_{\Pi,T}\) | \(2.01358056802\) |
| event-row error proxy | \(1.40768175195\times10^{-6}\) |
| terminal \(M_s\) proxy | \(0.00420051810664\) |

The maximum sampled \(\widehat K\) occurs at \(s=t\approx7.95647\) and is
caused by the unadvanced translation/identity block.  This is important:
closing only the active density triangles would miss the actual intermediate
norm.

None of these finite-grid values is an upper bound.  Accordingly all
directed \(\widehat K,\Delta,K_{\mathrm{int}},\Delta_T,\varepsilon_{\Pi,T}\),
terminal \(M_s\), stable-power, split-tube, graph, separator, and onset fields
remain null or false.

The executable source is
[leaky_inner_projected_stable_flow_stage4j_pilot.py](../src/canard_control/leaky_inner_projected_stable_flow_stage4j_pilot.py),
the generator is
[leaky_inner_projected_stable_flow_stage4j_pilot.py](../experiments/leaky_inner_projected_stable_flow_stage4j_pilot.py),
and the registered result is
[leaky_inner_projected_stable_flow_stage4j_pilot.json](../experiments/results/leaky_inner_projected_stable_flow_stage4j_pilot.json).

## Same-object construction

Let \(A=\widehat{\mathcal U}(t,s)\), let
\(d_s=f_s(q_s)\), and first retain the correlated quantities

\[
 b=Aq_s,\qquad g=f_tA,\qquad
 h=g-\frac{g(q_s)}{d_s}f_s=f_tAP_s(s).
\]

Every output row is then assembled as

\[
 rAP_s(s)-\frac{q_t^{(r)}}{f_t(q_t)}h,
 \qquad
 rAP_s(s)=r-\frac{r(q_s)}{d_s}f_s.                  \tag{1}
\]

Formula (1) is used without expanding the two signed cancellations.  The
residual replaces \(A\) by the complete raw differential residual and uses
the identical construction.  Thus the pilot no longer mixes
\(\widehat U P_s\) in the norm with \(P_tE\) in the residual.  At formula
level the output row annihilates \(q_s\), and the complete output lies in
\(\ker f_t\).  A proof must still enclose the transported rows,
normalizations, and their uncertainties outward before those analytic
constraints are promoted.

For output times \(u<s\), the raw row is the translated point evaluation of
the input history.  It is singular with respect to the atom--density row.
Consequently its norm is computed as one plus the total variation of the
common signed continuous part; it is not replaced by a finite-node history
matrix.

## Residual ledger

The sampled \(\Delta\) is the explicit sum of five sources:

1. \(\|P_s-P_s\widehat U(s,s)P_s\|\);
2. the time integral of the common doubly projected differential residual;
3. the history-transport boundary mismatch between the translated identity
   and the newly propagated voltage row;
4. delay-activation seams;
5. every Stage-4I cubic-guide cell seam.

The reported activation-right differential residual,
\(4.43437959639\times10^{-7}\), is kept separate from the activation jump so
it cannot be mistaken for a seam size.  The largest Stage-4I primitive seam
is \(1.38777878078\times10^{-17}\).  The pilot conversion of those primitive
seams to a projected complete-history budget is deliberately conservative,
but it is not directed; the proof source must re-form each seam in the same
signed row.

The endpoint event correction is applied only at \(T\).  No moving
\(\Pi_t\) is inserted, so there is no hidden \(\dot\Pi_t\) residual.

## Exact remaining gate

The pilot's 49-node trapezoidal history rule is useful for source-bound
profiling but is explicitly inadmissible as proof evidence.  Its worst
disagreement with the high-order Fourier/word oracle for \(f_s(q_s)\) is
about \(5.92\times10^{-8}\), whereas the high-order phase-covariance drift
is about \(8.53\times10^{-13}\).  A zero-measure activation endpoint also
receives a spurious positive trapezoid weight unless the identity boundary
is handled separately.  The source does handle that boundary separately,
but the episode identifies exactly why finite-node quadrature cannot be
promoted.

The smallest remaining directed gate is therefore a 192-bit or higher
piecewise Taylor--Bernstein enclosure over every active \((s,t,\theta)\)
support cell.  It must:

- enclose the common signed rows in (1), including the unadvanced block;
- integrate the final absolute density outward on exact support pieces;
- validate continuous \((s,t)\) suprema, rather than a mesh spread;
- carry the Stage-4D row, normalization, orbit, and coefficient errors in
  the same expression;
- prove the stable residual constraints and include all four residual
  sources in the directed \(\Delta\) ledger;
- bound the terminal event row separately and verify the strict rate gate.

The numerical margin is not the obstruction: even a coarse directed
\(\widehat K<20\) and \(\Delta<10^{-3}\) would give a useful a posteriori
constant.  The open issue is constructing the correlated continuous
enclosure without reverting to the unstable primitive-by-primitive forward
majorant rejected by Stage 4I.

## Replay

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 \
  experiments/leaky_inner_projected_stable_flow_stage4j_pilot.py
```

The static source and parent audit is

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 \
  experiments/leaky_inner_projected_stable_flow_stage4j_pilot.py --check
```
