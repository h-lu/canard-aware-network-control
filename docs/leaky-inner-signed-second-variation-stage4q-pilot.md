# Stage 4Q: signed near-two-period second-variation pilot

Status: **DIAGNOSTIC / NONRIGOROUS / SOURCE-BOUND**.

Stage 4Q asks a deliberately narrow computational question: after preserving
all signed moving-event and history-translation terms, how large are the
centre-orbit second-return kernel and the six fixed Stage-4M projected Hessian
blocks?

## Why the primary branch has two periods

Let `tau_max=5*sqrt(5)` and let `P` be the validated inner-orbit period.  A
moving-event return on the full continuous history space needs the output
history to lie beyond a second delay horizon.  The relevant centre test is

```
T - tau_max > tau_max.
```

The near-one-period branch fails because `P-2*tau_max<0`.  It is retained in
the JSON only as a formal finite-section diagnostic and is never called a
full-history `C^2` map.  The selected near-two-period branch has
`2P-2*tau_max>0`; this clears the centre smoothing gate, but does not validate
the event branch, a uniform tube, or a continuous-history operator bound.

## Signed calculation order

For each phase-aligned mesh, Stage 4Q:

1. propagates physical first and second variations through two periods;
2. forms both return-time derivatives at the selected terminal event;
3. translates every coordinate in the complete returned history at that same
   event time;
4. contracts inputs with the fixed `P_s` or the fixed unit `q_hat`;
5. applies the same fixed `f_hat` to the already-correlated output sector;
6. subtracts `q_hat*f_hat(sector)`; and
7. only then takes finite-section tensor norms.

The `q_hat,f_hat` pair is the Stage-4L/Stage-4D Grushin pair.  Its harmless
stored complex phase is fixed by requiring `q_w(0)>0`, and the opposite phase
is applied to the covector.  A tiny mesh pairing correction enforces
`f_hat(q_hat)=1` in each finite section.  Neither this correction nor the
sampled continuous `q` norm has a directed discretization error.

At the right history endpoint the primary adapter uses a one-sided four-node
cubic stencil, so it never invents positive-time section coordinates.  The
earlier symmetric-stencil/zero-future convention is retained only as an
explicit discarded-adapter audit.  A second column uses the finite Jacobian's
self-consistent left/right eigensplit; it diagnoses cancellation and supports
comparison with legacy finite-section pilots, but it does not replace the
fixed Stage-4L coordinate and is never used for cap acceptance.

As an independent oracle, the direct two-period tensor is compared against

```
H2 = H1[A1 ., A1 .] + A1 H1.
```

This comparison is a floating-point consistency check, not an error bound.

## Acceptance rows

The six projected rows are primarily compared to Stage 4P's simultaneous
recommended two-return box `(1,10,1000,5,10,1000)`.  That box closes only the
conditional graph arithmetic; it is not a Hessian certificate.  The older
strict Stage-4M common caps are retained as a secondary comparison.  The
ambient signed event-aligned tensor norm is separately compared both to the
Stage-4P two-return conditional target `K_ret<178.632235666...` and to the
legacy Stage-4N one-return target `188.912223881...`.  Stage 4P explicitly
records that scalar `K_ret` is a sufficient return-domain route, not a
necessary matrix graph-transform input.  The last-two-mesh envelope is
`max(last two)+2*last change+1e-18`; it is explicitly heuristic.

The JSON records the mesh series for all six blocks in three columns: the
primary fixed Stage-4L adapter, the self-consistent finite eigensplit oracle,
and the discarded endpoint adapter.  Differences between these columns are
discretization diagnostics, not uncertainty enclosures.

## Claim boundary

Every field in `claim_status` is `false`.  In particular Stage 4Q proves none
of the following: a continuous-history Hessian bound, a uniform nonlinear
selected-return tube, a second-hit or no-earlier-hit property, the six
Stage-4M blocks, a stable graph, a pulse crossing, onset, routing, biological
capture, or network safety.  Its purpose is to identify the next numerical
bottleneck without promoting a finite-grid oracle.

Reproduce with:

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src \
  /usr/bin/python3 \
  experiments/leaky_inner_signed_second_variation_stage4q_pilot.py
```
