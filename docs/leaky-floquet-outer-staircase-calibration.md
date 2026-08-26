# Predetermined local staircase for the outer Floquet cover

Status: **calibration, not a theorem artifact.**  The already proved parent
radius

\[
 \delta_p>0.0028635052681275253
\]

owns eight predetermined rational rectangles.  Their upper-right corners
are checked by exact fraction arithmetic to satisfy
\(x^2+y^2<\delta_p^2\).  Each is accepted only at its empty root path.  All
complementary roots and descendants use the complete infinite-operator
Neumann estimate, even if a descendant happens to lie inside the circle.
This fixed ownership removes the circular dyadic seam.

The lowest local band is

\[
 [0,0.00274]\times[0,0.0008],
\]

which contains the previously observed pending region near
\(\operatorname{Re}s=0.0021\)--\(0.0023\),
\(\operatorname{Im}s<0.00077\).  Higher bands step inward until imaginary
height \(0.00286\); an exact complementary rectangle is paired with every
band, followed by one upper complement.  Exact areas prove that the seventeen
roots partition \([0,256]\times[0,\pi^+]\).

The result records equal 200-cell and 5,000-cell budgets at threshold
\(0.999\), accepted and pending counts, exact normalized accepted areas,
root/leaf digests, and the remaining pending coordinate envelope.  A finite
budget run remains claim-free unless every root prefix and the exact area
close.  Even a completed calibration would still require the independent
256-bit limiting-cell/finer-split stress replay before promotion to the
outer zero-count theorem.

The corrected traversal registers all eight local roots before any Neumann
work and then processes all nine complementary roots breadth-first.  The
result therefore records a count and coordinate envelope for every root;
an untouched upper rectangle can no longer hide behind a global pending
count.  With 200 processed cells, the breadth-first run has 80 accepted
Neumann leaves, 57 materialized frontier cells, and accepted normalized area
greater than (0.75005).  With 5,000 processed cells, it has 1,548 accepted
Neumann leaves, 1,921 materialized frontier cells, and accepted normalized
area

\[
 0.9580421909316368741251\ldots .
\]

Every thin-band complement receives between 489 and 491 processed cells and
the upper complement receives 1,070.  The thin-band pending real envelopes
now have upper endpoint below (1.097); the upper complement retains the
full real endpoint (11).  Thus the run rigorously clears most of the
far-right bulk and localizes every frontier, but no complementary root is
complete.  The 1,921 breadth-first frontier cells are not comparable to the
old 39-cell depth-first frontier: breadth-first traversal deliberately
materializes all roots.  A pending-count decrease or accepted-area increase
is only a calibration metric; unless every per-root pending count vanishes,
the complement has not drained.

Reproduce with

```bash
OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/leaky_floquet_outer_staircase_calibration.py
```

The complete right-half zero count, outer attracting Floquet index,
nonlinear attracting tube, physical pulse onset, and parameter-box result
all remain false in this calibration.
