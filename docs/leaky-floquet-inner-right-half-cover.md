# The complete center-inner Floquet right-half count

Status: **the target theorem is a center-orbit spectral count.**  It combines
two local analytic counts with a full-operator zero-free cover of their
compact complement.  It does not use a finite SVD or determinant winding as
an infinite-dimensional proof.

## 1. Domain and the two counted disks

Every nonzero multiplier with modulus at least one has a logarithm in the
principal strip

\[
 0\leq \operatorname{Re}s\leq256,
 \qquad |\operatorname{Im}s|\leq\pi .
\]

The Riesz parent excludes the far-right half-plane and proves that the
translation value (s=0) is algebraically simple and is the only value in its
registered punctured neutral disk.  The local Grushin--Rouche parent proves
that the disk centered at

\[
 s_c=0.6983604129095,
 \qquad |s-s_c|<0.1,
\]

contains exactly one algebraically simple characteristic value.  It is real
and positive.  The two closed disks are strictly disjoint.

## 2. Physical delay representation

Writing (b) for the unshifted delayed coefficient, the physical term has the
equivalent forms

\[
 \sum_m b_{k-m}e^{-2\pi i k\alpha}y_m
 =\sum_m (b_\alpha)_{k-m}e^{-2\pi i m\alpha}y_m.
\]

The independent compact-cover engine uses unshifted coefficients and output
row phases.  A directed entrywise oracle verifies equality with the shifted
coefficient/input-column representation and rejects both mixed formulas.
Period-induced phase variation therefore uses output indices: both
finite-output blocks use 64.  For tail--finite, the aligned tail output
frequency is combined with the fast diagonal inverse, yielding the rigorous
(1+\|A_{\rm tail}\|h) cancellation.

Each nonlocal rectangle receives a binary64 finite inverse audited by four
real GEMMs, exact fast and slow tail diagonal bounds, complete support through
mode 128, the source-bound radius (10^{-12}) orbit correction, period
variation, and first/second delay-exponential remainders.  A rectangle is
accepted only when the resulting two-column full-operator Neumann contraction
is strictly below one.

## 3. Exact partition and count

Three rational root rectangles tile the upper compact strip.  Dyadic leaves
are classified in exactly one of three ways:

1. strictly inside the neutral disk;
2. strictly inside the positive-root disk; or
3. a strict full-operator Neumann cell.

Disk-boundary and straddling rectangles are never skipped: they are
subdivided until a full-operator cell closes.  Prefix completeness and exact
rational area prove that no seam is omitted.  The two local disks are treated
as open spectral regions; their boundaries belong to the keyhole remainder
and are covered by strict Neumann cells.  Shared dyadic and root-rectangle
seams are likewise zero-free, so the three spectral regions have neither a
missing boundary nor a double-counted characteristic value.  A 256-bit
replay of the worst cell and its four grandchildren guards the limiting
numerical margin.

The completed tree has 60,432 leaves after 120,861 processed cells.  Of
these, 61 leaves lie strictly in the neutral disk, 202 lie strictly in the
positive disk, and 60,169 are zero-free Neumann leaves.  These are **cover
leaf counts**, not characteristic-value counts.  Analytic Fredholm
argument-principle additivity gives the separate characteristic counts

\[
 N(D_0)=1,\qquad N(D_u)=1,\qquad N(K)=0.
\]

The worst 160-bit contraction upper bound is
`0.9949974758400778845695147246986825668057586726278103554`, leaving the
strict margin
`0.0050025241599221154304852753013174331942413273721896446`.

Once that tree is complete, the upper complement is zero-free.  Real
conjugacy supplies the lower complement.  Therefore the closed right-half
principal strip contains exactly two characteristic values counted with
analytic algebraic multiplicity: the neutral translation value and the one
simple positive value.  Consequently the center inner orbit has exactly one
unstable multiplier and no other multiplier on or outside the unit circle,
apart from translation.

## 4. Claim boundary

This is not a common ((a,\kappa_3)) parameter-box theorem.  It does not yet
construct a stable or unstable manifold, a nonlinear saddle block, an
asynchronous network root, a history-space separator, a pulse intersection,
or physical onset.  Those flags remain false even when the center spectral
count closes.
