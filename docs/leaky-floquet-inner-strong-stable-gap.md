# A strengthened stable spectral gap for the center inner orbit

Status: **the center-orbit stable spectral gap is strengthened to**

\[
 \gamma=0.01,
 \qquad \rho_s\le e^{-0.01}<1.
\]

This is a source-bound spectral theorem for the single validated center
inner orbit.  It does not make the estimate uniform on a parameter box and
does not construct a spectral projection, a boundary semigroup power bound,
a stable manifold, a nonlinear separator, or physical onset.

## 1. Extension rather than replacement

The base certificate proves that the full complex neutral disk contains only
the simple translation value and that the open strip

\[
 -0.001\le \operatorname{Re}s<0,
 \qquad |\operatorname{Im}s|\le\pi,
\]

is zero-free.  The strengthened certificate preserves that artifact and
covers only the additional slab

\[
 -0.01\le \operatorname{Re}s\le-0.001,
 \qquad |\operatorname{Im}s|\le\pi.
\]

The shared line \(\operatorname{Re}s=-0.001\) is itself covered and
zero-free, so analytic count additivity has neither a gap nor a duplicated
root.  The base and extension results together imply that the full open
strip \(-0.01\le\operatorname{Re}s<0\) is zero-free.

## 2. Corrected negative-real full operator

The two upper-half rectangles are

\[
 [-0.01,-0.001]\times[0,1],\qquad
 [-0.01,-0.001]\times[1,\pi_{\rm up}].
\]

The physical pencil retains unshifted delayed coefficients with output-row
phases.  Every negative-real delayed term carries the outward factor

\[
 \exp\!\left(|\operatorname{Re}s|\frac{\tau_{\max}}{T_{\min}}\right),
\]

where \(T_{\min}\) includes the nested orbit correction radius.  Tail
formation uses \(|\operatorname{Re}s|\), and the same exponential factor is
present in the delay Taylor remainder, orbit/period correction, and infinite
tail-to-tail delayed term.  The tail diagonal edge-monotonicity inequality is
checked separately with directed arithmetic.

A rectangle strictly inside the already validated full neutral disk is
zero-free because the extension slab cannot contain \(s=0\).  All other
rectangles, including every disk-boundary straddler, require a strict
full-operator Neumann inverse.  The left-disk geometry uses the farthest of
all four exact rational corners.

## 3. Exact tree and consequence

The completed upper extension tree has 5,254 leaves after 10,506 processed
cells: 50 inherit zero-freeness from the full neutral disk, and 5,204 are
strict full-operator Neumann leaves.  Prefix completeness and exact rational
area give a gap-free partition.  The worst 160-bit contraction upper bound is

`0.9948835204460725319628852401962484852333177560663284035`,

leaving the strict margin

`0.0051164795539274680371147598037515147666822439336715965`.

As in the base certificate, the stored binary64 finite inverses and products
are pinned to `OPENBLAS_NUM_THREADS=1`.  A direct build under another
schedule is rejected; bitwise replay from such an environment must occur in
a fresh single-threaded subprocess.

Real conjugacy supplies the lower half.  Compactness of the history
monodromy and the history-to-Fourier regularity bridge are inherited as hard
gates from the base certificate.  Hence every stable nonzero multiplier has
a principal characteristic logarithm with real part strictly below
\(-0.01\); zero multipliers satisfy the same bound by compactness.  Therefore

\[
 \rho_s\le e^{-0.01}
 =0.99004983374916805357390597718003655777207908125490723\ldots<1.
\]

This spectral-radius estimate is not, by itself, a bound on powers of the
stable boundary evolution.  Projection norms, transient growth, graph
transform constants, common-parameter continuation, and nonlinear capture
remain separate gates.
