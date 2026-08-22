# Exact-chart canard-threshold diagnostic

Status: **diagnostic numerical evidence; not a theorem or a proof.**

The exact four-dimensional fixed-scaled-delay chart is integrated by a
literal method of steps with Radau on every step interval.  The
prescribed history on `[-S-theta_1,-S]` is the leading canard and
its singular transverse graph.  At `+S`, `nu` is tuned until the
KS Hamiltonian has zero energy (implemented with its equivalent
positive normalization).

The reported quotient is

\[
 \frac{\nu_c(+h)-\nu_c(-h)}{2\delta h},
\qquad h=0.04,
\]

and the formal target is

\[
 \frac{K(\theta_0-\theta_1)}{4\alpha}
 = -0.2041241452319315
\]

for `K=1`, `theta_0=0.5`, `theta_1=1`, and
`alpha=sqrt(6)/4`.

| delta | S | nu_c(0) | plus quotient | minus quotient | central | relative error | max root residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.12 | 2.5 | -0.49967922 | -0.196999494 | -0.196954628 | -0.196977061 | 3.501e-02 | 1.803e-11 |
| 0.08 | 2.75 | -0.574251723 | -0.201733676 | -0.201717113 | -0.201725395 | 1.175e-02 | 1.722e-12 |
| 0.05 | 3 | -0.639036036 | -0.202546786 | -0.202541915 | -0.20254435 | 7.739e-03 | 2.098e-13 |
| 0.01 | 4 | -0.736926816 | -0.202745433 | -0.202745394 | -0.202745413 | 6.754e-03 | 5.673e-12 |
| 0.005 | 4.5 | -0.744489434 | -0.203220087 | -0.20321922 | -0.203219653 | 4.431e-03 | 1.972e-08 |
| 0.0025 | 5 | -0.746839663 | -0.203616824 | -0.203617929 | -0.203617376 | 2.483e-03 | 7.955e-08 |

## What this checks

Along the displayed diagonal sequence, `delta` decreases while
the finite section `S` increases.  The central quotient moves
toward the formal coefficient, and the plus/minus quotients
agree closely relative to the asymptotic discrepancy.  This is a sensitive
sign, scale, and implementation check of the transverse-return
calculation.

## What this does not check

The leading-canard history is prescribed rather than obtained
from the parameter-dependent invariant history graph.  The exit
condition is the leading Hamiltonian zero level at a finite
section, not equality of complete attracting and repelling RFDE
histories.  Therefore the computed root depends on the chosen
history, section, and order in which `delta -> 0` and `S ->
infinity` are approached.  Large `S` also amplifies integration
and interpolation errors along the repelling segment.  Neither
the observed convergence nor the small scalar residual proves
history/section independence, a simple geometric root, or the
uniform theorem remainder.

The exact settings and full-precision values are in
`experiments/results/exact_chart_threshold_convergence.json`.

## Numerical refinements

At the smallest displayed `delta` and largest `S`, the
archived tolerance and maximum-step refinements give
a tolerance spread of `2.809e-09`
and a maximum-step spread of `3.163e-09`
in the normalized central quotient. These discretization
spreads are much smaller than the displayed asymptotic
discrepancy, but they do not address history or section bias.
