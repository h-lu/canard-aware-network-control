# Local Grushin pole subtraction at the outer translation root

Status: **Stage-1 failure contract; the global outer Floquet index remains
open.**  The complete bordered Fourier operator is rigorously invertible on
the closed disk

\[
             |s|\le 2.8\times10^{-3},
\]

but the attempted scalar effective-Hamiltonian Rouché comparison does not
close.  Consequently this artifact proves complete Grushin invertibility,
not a full-disk zero count.  The separate parent theorem continues to
exclude nontranslation roots in the punctured right half-disk of radius

\[
  \delta_p>
  0.00286350526812752530789320022889729032408013088844984066.
\]

The executable theorem carrier is
[leaky_floquet_outer_grushin_stage1.py](../src/canard_control/leaky_floquet_outer_grushin_stage1.py),
the generator is
[leaky_floquet_outer_grushin_stage1.py](../experiments/leaky_floquet_outer_grushin_stage1.py),
and the source-bound result is
[leaky_floquet_outer_grushin_stage1.json](../experiments/results/leaky_floquet_outer_grushin_stage1.json).

## Complete bordered operator

For the physical logarithmic Floquet pencil \(\mathcal L_s\), fix the
cutoff-64 left and right singular vectors of the binary64 centre matrix and
scale them by 20 and 5.  They define finite-supported, fixed borders
\(R_-\) and \(R_+\), and hence

\[
 \mathcal G_s=
 \begin{pmatrix}
   \mathcal L_s&R_-\\ R_+&0
 \end{pmatrix}.
\]

The singular vectors are guides only.  Invertibility is proved afterwards
for the complete operator: the coefficient convolution retains every mode
through 256, the finite/tail and tail/finite matrices explicitly reach mode
320, the remaining infinite tail is bounded by its exact fast and leaky-slow
diagonals, and the exact orbit lies in the independently derived nested
Wiener ball of radius \(10^{-8}\).

The delayed operator is represented as an unshifted coefficient followed by
the Bloch-delay phase on the **output row**.  The equivalent shifted
coefficient/input-column representation is checked entrywise.  Both mixed
conventions are rejected by binary64 and directed hostile oracles.

Unlike a right-half-plane cover, the Rouché circle crosses
\(\operatorname{Re}s<0\).  Every delayed bound therefore contains the
factor

\[
 \sup e^{-\alpha\operatorname{Re}s}
 \le \exp(\alpha_{\max}R)>1.
\]

Using \(|e^{-\alpha s}|\le1\) on this full circle would be invalid.  The
stored certificate exposes the resulting amplitude and hostile tests reject
its removal.

## Effective Hamiltonian and the failed final inequality

Let the bottom-right entry of \(\mathcal G_s^{-1}\) be \(E_{-+}(s)\).
Complete Grushin invertibility makes

\[
       \mathcal L_s\text{ singular}\quad\Longleftrightarrow\quad
       E_{-+}(s)=0
\]

with analytic multiplicity.  Boundary cells compare \(E_{-+}\) with the
nonzero affine guide \(a_*s\).  The complete operator contraction closes at

\[
 q_G\le 0.4868749648346581<1,
\]

and the full-disk Bloch amplitude is bounded by
\(1.001177375063315\).  The last scalar comparison, however, gives

\[
 |a_*|R\ge 7.470726303334246\times10^{-7},\qquad
 \sup_{|s|=R}|E_{-+}(s)-a_*s|
 \le2.016439989282795\times10^{-5}.
\]

Thus its directed margin is
\(-1.941732726249452\times10^{-5}\), and Rouché cannot be invoked.  More
than \(99.5\%\) of the comparison bound is the bottom-row Neumann
back-substitution term
\(2.008249452582517\times10^{-5}\); the affine interpolation error, centre
inverse/first-derivative error, and local Taylor remainder are respectively
below \(9.67\times10^{-11}\), \(8.17\times10^{-8}\), and
\(1.79\times10^{-10}\).  Finer boundary arcs therefore do not address the
dominant obstruction.

Alternative period-column/phase-row and period-column/point-row borders
were audited as diagnostics.  They amplify the displayed slope but amplify
the rigorous inverse/back-substitution error more strongly.  No claim is
based on those alternatives: border rescaling alone is not mathematical
progress.

## Exact remaining inequality

The sole missing inequality for this particular full-disk construction is

\[
 \sup_{|s|=R}|E_{-+}(s)-a_*s|<|a_*|R.
\]

It should next be attacked with exact autonomy built into the border—an
exact translation column and a normalized phase/adjoint row—and an integral
bound for \(E_{-+}(s)/s\), so that an \(s\)-independent orbit error is not
paid at every boundary point.

For the immediate right-half cover, a simpler route already exists: use the
proved punctured half-disk directly through a finite predetermined rational
staircase of local rectangular leaves.  This avoids both the circular
dyadic seam and the unnecessary negative-real half of the Rouché circle.
Until the remaining complement is completely covered, the full right-half
zero count, unit-circle exclusion, outer attracting Floquet index, nonlinear
attracting tube, history separator, physical pulse onset, and biological
control theorem all remain false.

Reproduce with

```bash
OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/leaky_floquet_outer_grushin_stage1.py

PYTHONPATH=src /usr/bin/python3 -m pytest -q \
  tests/test_leaky_floquet_outer_grushin_stage1.py
```
