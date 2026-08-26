# A quantitative stable spectral gap for the center inner orbit

Status: **the center-orbit Poincare spectrum has a source-bound nonzero
stable gap.**  Apart from the algebraically simple translation multiplier
and the algebraically simple unstable multiplier, every multiplier lies in

\[
 |\mu|\le e^{-0.001}<1.
\]

This is a spectral statement for the single validated center orbit.  It is
not uniform on a parameter box and does not construct a spectral projection,
stable manifold, nonlinear saddle block, pulse intersection, or onset.

## 1. A full complex neutral disk

The earlier Riesz theorem excluded a punctured neutral half-disk only for
\(\operatorname{Re}s\ge0\).  That result cannot simply be translated to the
left.  Let \(D\) be the validated phase-bordered inverse norm, and let
\(c_1,c_2\) be the first- and second-order coefficients from the neutral
simplicity transfer.  On the full disk \(|s|\le r_0\), where
\(r_0=0.0039\), the delay integral remainders acquire the factor

\[
 E_0=\exp\!\left(\frac{\tau_{\max}}{T_{\min}}r_0\right).
\]

Thus the full-disk coefficients are bounded by

\[
 c_1^{\rm full}=1+(c_1-1)E_0,
 \qquad c_2^{\rm full}=c_2E_0.
\]

Directed MPFR arithmetic verifies both strict inequalities

\[
 D c_1^{\rm full}r_0<1,
 \qquad \frac{D c_2^{\rm full}r_0}{T_{\min}}<1.
\]

The corresponding certified upper bounds are
`0.492628541371579835090717268692381647870716817624478387` and
`0.00266528884534508329139305370756729654195803486036981987`.

The phase-bordered argument and the already proved algebraic simplicity
then show that the full complex disk contains exactly one characteristic
value: \(s=0\), with algebraic multiplicity one.  Its boundary is zero-free.

## 2. The negative-real-part corrections

The right-half cell engine used three estimates that are false without
modification on \(\operatorname{Re}s<0\).  The independent left-strip engine
repairs each one.

First, every delayed term and every delay-exponential Taylor remainder is
multiplied by

\[
 E_\gamma=\exp\!\left(
   \frac{\tau_{\max}}{T_{\min}}\gamma
 \right),\qquad \gamma=0.001.
\]

Second, binary tail-formation error uses \(|\operatorname{Re}s|\), not the
right endpoint of a negative interval.  Third, the same factor
\(E_\gamma\) enters the infinite tail-to-tail delayed coefficient and the
orbit/period correction.  The physical main representation remains the
audited unshifted coefficient with output-row phase; the equivalent shifted
coefficient/input-column formula is inherited from the right-half parent.

## 3. Exact left-strip cover and seam ownership

Two exact rectangles tile the upper left strip:

\[
 [-0.001,0]\times[0,1],\qquad
 [-0.001,0]\times[1,\pi_{\rm up}].
\]

A dyadic leaf is accepted only if it lies strictly in the full neutral disk
or its complete Fourier operator has a strict Neumann inverse.  Any leaf
meeting the neutral-disk boundary is therefore a Neumann leaf.  Exact prefix
completeness and rational area exclude gaps on the horizontal seam.
For a negative-real rectangle, the disk test uses the farthest of all four
corners, in particular \(\max(|\sigma_-|,|\sigma_+|)\); it does not reuse the
right-half-only \(\sigma_+\) shortcut.

The completed left tree has 660 leaves after 1,318 processed cells: 16
neutral-disk leaves and 644 full-operator Neumann leaves.  Its worst
160-bit contraction upper bound is
`0.9947278955023612064055528045831350165658013849449109211`, leaving
the strict invertibility margin
`0.0052721044976387935944471954168649834341986150550890789`.

The stored binary64 finite inverses and products are replayed with
`OPENBLAS_NUM_THREADS=1`.  This schedule is part of the certificate, and a
direct build under any other setting is rejected; callers that need a
bitwise replay must start a fresh single-threaded subprocess before NumPy
loads OpenBLAS.  The surrounding MPFR error bounds remain rigorous, but
binary thread schedules are not interchangeable for artifact equality.

The line \(\operatorname{Re}s=0\) is shared with the audited right-half
parent.  The neutral root is assigned to that parent.  The new closed left
strip contains only this seam root, so its open part
\(-0.001\le\operatorname{Re}s<0\) is zero-free.  Real conjugacy supplies the
lower half of the principal strip.  Combining this fact with the right-half
count proves that the shifted closed strip contains only \(0\) and the known
positive root.

## 4. Spectral consequence and scope

For every stable nonzero multiplier, choose its principal logarithm.  The
source-validated regularity bridge identifies that multiplier with a
Fourier characteristic value in the principal strip.  The left-strip
exclusion gives \(\operatorname{Re}s<-0.001\), hence

\[
 \rho_s\le e^{-0.001}<1.
\]

Zero multipliers of the source-validated compact RFDE history monodromy also
satisfy this bound.  Both compactness and the history-to-Fourier spectral
bridge are hard parent gates in the certificate, not informal consequences
of the finite Fourier sections.  The certificate does not construct the
stable spectral projection or control its norm.  In particular, the small
denominator needed by a quantitative stable graph transform is a separate
gate.  Common-parameter, manifold, nonlinear, asynchronous-network,
history-separator, and physical-onset flags remain false.
