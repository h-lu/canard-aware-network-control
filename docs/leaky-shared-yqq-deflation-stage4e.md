# Stage 4E: physical-time shared \(Y_{qq}\) deflation

## Outcome

Stage 4E validates the previously open bottleneck **at the periodic base
orbit**.  It encloses the physical second variation on 1042 directed
method-of-steps cells, evaluates the continuous Route-C covector on the same
history, forms

\[
  Y_{qq}-q\frac{f(Y_{qq})}{f(q)}
\]

before taking a norm, and proves a base-orbit normalized upper bound strictly
below the Stage-4B design value \(12\).

This is not yet the quantitative local-stable-graph theorem.  The other five
Hessian blocks, stable power constant, uniform radius-\(1.7\times10^{-3}\)
split return tube, and first-return event enclosure remain open.  Consequently
the six-block Stage-4B matrix remains a conditional design calculation.

The executable source is
[leaky_shared_yqq_deflation_stage4e.py](../src/canard_control/leaky_shared_yqq_deflation_stage4e.py),
the generator is
[leaky_shared_yqq_deflation_stage4e.py](../experiments/leaky_shared_yqq_deflation_stage4e.py),
and the registered result is
[leaky_shared_yqq_deflation_stage4e.json](../experiments/results/leaky_shared_yqq_deflation_stage4e.json).

## 1. Physical-time directed tube

Let \(h=\tau_0/512\).  The stored physical delays satisfy

\[
 \tau_0=512h,\qquad \tau_1=640h,
\]

so every delayed source is taken from a whole earlier cell.  A degree-24
Taylor guide is constructed on 1041 full cells and one final short cell.
Every residual polynomial is recomputed with 192-bit outward MPFR arithmetic,
converted to Bernstein form on \([0,1]\), and augmented by analytic Taylor
tails and the explicit sum of trimmed coefficients.

The guide residual is not estimated by comparing meshes.  Its directed cell
bounds enter a two-coordinate \(P\)-norm error inequality.  Current terms use
the \(P\)-logarithmic norm; delayed errors use the already-propagated radii of
the cells shifted by 512 and 640 steps.  This gives a continuous-time tube for
the complete base-orbit \(V_{qq}\), including every cell seam.

## 2. Continuous-history Route-C action

Stage 4D supplies the advanced adjoint as a current atom plus a
voltage-history density and proves an absolutely summable Fourier tail.  The
Stage-4E action retains the declared space

\[
  C([-\tau_{\max},0],\mathbb R)\times\mathbb R.
\]

voltage is bounded over the whole history, while recovery contributes only
at the current endpoint.  Treating recovery as a second retained history
would be a different norm and is not done.

The exact-minus-guide error equation is transported from time \(T\) to phase
zero with the correct Floquet covariance \(e^s\).  Because the exact advanced
covector annihilates the phase tangent, uncertainty in \(\tau_{qq}\) does not
enter the unstable scalar action, although it correctly remains in the final
history sup error.

## 3. Why the correlated quotient closes

A separate numerator/denominator interval loses the decisive cancellation.
Set the binary centre quotient to

\[
 c=\frac{f_0(Y_{qq,0})}{f_0(q_0)}.
\]

For the exact objects,

\[
 \frac{f(Y_{qq})}{f(q)}-c
 =\frac{f(Y_{qq}-cq)}{f(q)}.
\]

Stage 4E encloses the right-hand side directly.  The adjoint-row error acts on
the event-corrected nonphase guide radius.  The code bounds that radius by the
correlated centre history plus the explicit
\(|\tau_{qq}|\|\dot X\|\) phase term; it does not call the radius small.  The
change of the \(V_{qq}\) source is paired in physical time against the same
advanced covector.  Parseval gives an outward bound for its time-integrated
voltage component, retaining Fourier cancellation without using a sampled
mesh as error evidence.

The centre scalar is defined by a direct atom-plus-density action of the
stored Fourier row on the piecewise Taylor guide.  This avoids assuming that
an approximate Fourier row satisfies an exact inhomogeneous-adjoint identity.
A second 192-bit Taylor calculation integrates every stored density against
every intersected guide cell and encloses its analytic tail.  The registered
field `center_adjoint_inhomogeneous_identity_defect_upper` is the remaining
direct-action cancellation defect.

The exact-minus-guide equation then contains all four genuine sources:
voltage guide residual, recovery guide residual, model residual, and every
cell-seam jump.  The first three are paired continuously with separate
Parseval bounds for the voltage and recovery adjoint components.  Seam jumps
are summed as directed \(P\)-radii and paired with the Wiener norm of the
current adjoint.  Thus none of these errors is hidden in a mesh-spread
surrogate or omitted from the action ledger.

The exact history density is a product \(a_{\mathrm{exact}}B_{\mathrm{exact}}\),
whereas the direct centre action uses \(a_0B_0\).  The field
`history_measure_difference_upper` contains all three product differences:
the adjoint-row error times \(1+\sum_j\tau_j\|B_j\|\), the stored voltage-row
norm times \(\sum_j\tau_j\|B_{j,\mathrm{exact}}-B_{j,0}\|\), and a separate
outward convolution-rounding guard.  This same functional-difference bound
enters both the deflated centre action and the normalization error.
The additional field `adjoint_density_basis_shift_upper` covers the change of
the physical/phase Fourier basis with \((s,T)\): finite modes use the explicit
factor
\((2\pi|n|+|s|)\tau_{\max}\delta T/T^2+\tau_{\max}\delta s/T\),
while the refined summable tail uses its two-sided \(\ell^1\) error.

For normalization, the lower bound is centred at the direct history action
\(f(q)\).  The separately computed \(L'(s)\) value and its tiny discrepancy
remain in the ledger as an identity diagnostic, not as the quotient centre.

The registered ledger separately records:

- the centre correlated history norm;
- the history-measure error on the event-corrected nonphase guide radius;
- the physical \(V_{qq}\) guide-plus-model residual and seam action errors;
- event and section-history action errors;
- the normalization lower bound and correlated quotient error.

Only after summing these directed terms is the continuous-history norm taken
and divided by the proved lower bound for \(\|q^\Sigma\|^2\).

## 4. Exact scope of the advance

The new proved statement is a base-orbit Hessian-direction certificate:

\[
 C_{s,\mathrm{base}}^{uu}<12.
\]

It removes the numerical/covector obstruction in the Stage-4B bottleneck and
shows that the shared deflation mechanism is quantitatively viable.  It does
not prove

\[
 \sup_{\|z\|_{s,u}\le 1.7\times10^{-3}} C_s^{uu}(z)<12.
\]

Substituting this base value together with the five Stage-4B design targets
still produces the previously recorded positive matrix with Perron root below
one and a graph box inside radius \(1.7\times10^{-3}\).  That substitution is
conditional because the five targets and the uniform tube are not directed
bounds.  The artifact therefore keeps every stable-graph, graph-radius,
separator, and pulse-onset flag false.

## 5. Replay

Generate and validate:

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_shared_yqq_deflation_stage4e.py
```

Recompute in a fresh process and compare the canonical artifact digest:

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_shared_yqq_deflation_stage4e.py --replay
```

The static `--check` path verifies the registered source hashes, parent-byte
hashes, claim ledger, and quantitative inequalities without rerunning the
long integration.
