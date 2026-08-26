# Stage 4I: directed residuals for the inner four-word primitives

## Outcome

Stage 4I validates the first directed ingress behind the Stage-4H signed
stable-flow calculation.  It encloses cubic guides for the current
fundamental matrix \(F\), its inverse \(G\), and the three active word
primitives \(C_0,C_1,C_{00}\) on the 1042-cell delay-aligned physical grid.
Every guide residual is recomputed with 192-bit outward MPFR arithmetic,
Taylor-expanded coefficient polynomials, Bernstein range bounds, and
explicit analytic Fourier tails.  Every binary Hermite seam is also inserted
as an outward jump before the next-cell error is propagated.

This is a primitive certificate, not yet the stable-power theorem.  The
remaining decisive object is a common two-variable enclosure of the signed
history density after subtracting the Stage-4D rank-one row.  Until its
absolute integral and continuous output-time supremum are outward bounded,
Stage 4I does not prove \(\|LP_s\|<\rho_s\), \(K_s=1\), the split tube, the
stable graph, separator crossing, or onset.

The executable source is
[leaky_inner_word_primitive_stage4i.py](../src/canard_control/leaky_inner_word_primitive_stage4i.py),
the generator is
[leaky_inner_word_primitive_stage4i.py](../experiments/leaky_inner_word_primitive_stage4i.py),
and the registered result is
[leaky_inner_word_primitive_stage4i.json](../experiments/results/leaky_inner_word_primitive_stage4i.json).

## 1. Triangular primitive system

With \(A(t)\) the current two-dimensional coefficient and
\(B_j(t)=b_j(t)e_1e_1^T\), write \(F'=AF\) and \(G'=-GA\).  The one-delay
primitives satisfy

\[
 C_j'(t)=G(t)e_1b_j(t)e_1^TF(t-\tau_j)\quad(t>\tau_j),
 \qquad C_j(t)=0\quad(t\le\tau_j),
\]

and the only two-delay primitive satisfies

\[
 C_{00}'(t)=G(t)e_1b_0(t)e_1^TF(t-\tau_0)C_0(t-\tau_0)
 \quad(t>2\tau_0),
 \qquad C_{00}(t)=0\quad(t\le2\tau_0).
\]

The dependency order is triangular:

\[
 (F,G)\longrightarrow(C_0,C_1)\longrightarrow C_{00}.
\]

Thus the residual error tubes can be propagated without a circular delay
majorant.

## 2. Directed residual calculation

The physical step is \(h=\tau_0/512=\tau_1/640\).  On each cell, binary
DOP853 values and endpoint slopes define a cubic Hermite guide.  These
binary values are not treated as exact solutions.  Instead, the source
recomputes

\[
 p_F'-A p_F,
 \quad p_G'+p_GA,
 \quad p_{C_j}'-p_Ge_1b_je_1^Tp_F(\cdot-\tau_j),
\]

and the analogous \(C_{00}\) residual as interval polynomials.  Bernstein
conversion bounds the polynomial part over the complete cell.  Analytic
Taylor tails and every trimmed Fourier coefficient are added before the
matrix-entry norm is taken.

The validated orbit uncertainty enters separately as errors in the current
and delayed coefficients.  The resulting cellwise radii propagate in the
same triangular order as the exact primitive system.  At a seam, Stage 4I
adds the outward guide jump.  For the fundamental matrix it uses

\[
 j_k=\|P_k(0)^{-1}\|_\infty
     \|P_{k-1}(1)-P_k(0)\|_\infty
\]

and adds \(\log(1+j_k)\) to the moving-frame logarithmic budget.  Thus no
binary continuity assumption is hidden in the propagation.

A specified scalar propagation in the original physical frame is also
strictly rejected for this certificate: it retains the unstable Floquet growth and inflates
sub-microscopic local residuals to unusable \(F,G\) radii.  Stage 4I instead
uses the directed defect

\[
 \|G_{\rm g}F_{\rm g}-I\|_\infty<1
\]

to validate a guide inverse and accumulates the relative residual in moving
coordinates.  This makes the four-word primitives usable, but it does not
solve the stable-row problem by propagating those primitives separately.
The next certificate must impose the phase correction and rank-one
deflation at the level of the common density.  Its error should be closed on
\(\ker f\), through a bordered stable inverse or a moving \(P_s(t)\), so the
unstable direction is absent from the error equation from the outset.

## 3. Interpretation

The artifact compares a deliberately coarse measure-error consequence of
the primitive tubes with the \(0.9908904951\ldots\) numerical margin left by
Stage 4H.  Even if this primitive-only budget fits inside that margin, it
does not turn the sampled Stage-4H centre into an upper bound.  A theorem
still needs interval polynomials for the common signed density
\(S(t,\theta)\), outward integration of \(|S(t,\theta)|\), a continuous
supremum in \(t\), and the Stage-4D row/normalization uncertainties in that
same expression.

The artifact states its mixed norm convention explicitly: \(F,G\) error
radii are matrix \(\infty\)-norm bounds, while \(C_0,C_1,C_{00}\) error
radii are maximum-entry bounds.  All conversion factors are inserted in the
induced measure estimate.  In particular, the two-delay history density has
support length at most \(\tau_0\), not \(T-2\tau_0\).

## 4. Replay

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_word_primitive_stage4i.py
```

The static source/parent audit is

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_word_primitive_stage4i.py --check
```
