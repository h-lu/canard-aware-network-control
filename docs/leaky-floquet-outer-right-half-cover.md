# Outer leaky Floquet right-half cover

This certificate addresses one sharply delimited question at the fixed
centre parameter values: apart from the autonomous translation root, does
the source-validated outer periodic orbit have a characteristic value in
the closed right half-plane?  It does not claim persistence of that count
on the common parameter box, nonlinear orbital attraction, a history-space
separator, or physical pulse onset.

## Operator and arithmetic

On normalized time, with (D e_k=2\pi i k e_k), the full two-component
characteristic pencil has finite block

\[
 \mathcal L_s=
 \begin{pmatrix}
 D+s-T A_s & T I\\
 -T\varepsilon I & D+s+T\varepsilon
 \end{pmatrix}.
\]

The bottom-right entry is therefore (D+s+T\varepsilon), not the
non-leaky (D+s) entry.  The proof uses separate exact Fourier-tail
inverses for (D+s) and (D+s+T\varepsilon).  The 257-node orbit makes the
quadratic variational coefficients nonzero through mode 256, and the
finite/tail convolution blocks retain that full support.

Write \(b\) for the unshifted derivative coefficient of the delayed
nonlinearity, and put \(\alpha=\tau/T\).  The physical linearized term is
\(e^{-s\alpha}S_\alpha M_b y\), so its entry at output mode \(k\) and input
mode \(j\) is

\[
 b_{k-j}\exp[-\alpha(s+2\pi i k)].
\]

Thus this module's unshifted-coefficient representation multiplies output
rows.  If instead
\(c^{(\tau)}_\ell=b_\ell e^{-2\pi i\ell\alpha}\) is stored separately for
each delay, then the exactly equivalent entry is

\[
 c^{(\tau)}_{k-j}\exp[-\alpha(s+2\pi i j)],
\]

which multiplies input columns.  A Gaussian-integer basis oracle checks the
two representations entry by entry in the finite--finite, finite--tail, and
tail--finite blocks, while a directed oracle checks the actual outer-orbit
coefficient boxes.  Both mixed conventions (unshifted coefficient with a
column phase, or shifted coefficient with a row phase) are required to
separate strictly.  Every shift uses an outward enclosure of the exact ratio
\(\alpha\); binary exponentials remain stored guides with explicit distance
bounds.  Phase-neutral binary norm and four-real-GEMM helpers live in the
shared arithmetic module.  The certificate has no source dependency on the
earlier FHN cover.

For orbit and period variation the unshifted representation is especially
useful: changing \(T\) changes the shift of the whole product.  Hence the
frequency is the total output frequency.  Both finite--finite and
finite-from-tail corrections use \(|k|\le64\); after the fast tail inverse,
the tail-from-finite phase term has the directed
\(1+A_{\rm tail}h\) cancellation.  Treating the shifted coefficient as
independent of \(T\) would miss its \((k-j)\)-frequency contribution.  A
separate directed four-term oracle recomputes the physical correction and
rejects both input-only mutants.

For each nonlocal dyadic rectangle a binary64 midpoint inverse is only a
guide.  Four-real-GEMM rounding bounds, 160-bit outward MPFR coefficient
and rotation bounds, the complete state/period correction, and a complex
split Wiener norm validate

\[
  \lVert I-\mathcal A_s\mathcal L_s\rVert <1.
\]

The straight-line Neumann homotopy is then invertible on the entire cell;
no binary64 determinant winding is promoted to proof.

## Nested fixed-parameter orbit ball

The registered outer source validates its nonlinear majorant on every
(0\le r\le10^{-5}).  This certificate re-evaluates the same source-bound
(Y,Z_0,Z_1,Z_2,Z_3) endpoints with outward arithmetic at (r=10^{-8}):

\[
 q(r)=Z_0+Z_1r+Z_2r^2+Z_3r^3,
 \qquad Y+q(r)r<r.
\]

Thus the exact centre-parameter orbit belongs to the nested ball.  The
larger common-parameter-box residual also closes a (10^{-6}) ball, but
that coarser radius gives a failed contraction diagnostic near the neutral
pole and is not used as claim-bearing evidence here.  In particular, the
present result must not be read as a uniform parameter-box Floquet count.

## Complete strip decomposition

The upper principal rectangle is
\([0,256]\times[0,\pi^+]\), where \(\pi^+\) is one registered outward MPFR
upper endpoint used identically by construction, serialization, and replay.
To avoid an infinite dyadic chase along the circular neutral seam, set the
exact decimal \(a=0.002\) and partition it into the three closed roots

\[
 [0,a]^2,\qquad [a,256]\times[0,\pi^+],\qquad
 [0,a]\times[a,\pi^+].
\]

Their interiors are disjoint, their union is the full principal rectangle,
and the shared edges are deliberately covered from both sides.  Exact
rational arithmetic proves \(2a^2<r_0^2\), where \(r_0\) is the parent's
local exclusion radius.  The whole first root is therefore discharged by
the local punctured-disk theorem and algebraic simplicity of the translation
root.  Every nonlocal root is at distance at least \(a\) from zero, removing
the non-finitely-alignable circular straddling cells.  Local ownership is
fixed at that one unsplit square: every descendant of either complementary
root uses the full-operator Neumann estimate, even if it happens to lie
geometrically inside the circular Riesz disk.  Reintroducing a circular
shortcut there would recreate precisely the seam that this partition removes.

Prefix completeness is checked separately on all three roots.  Root-area
weights and the exact rational identity

\[
 \frac{1}{256\pi^+}
 \sum_{Q\ \mathrm{leaf}} |R_{\mathrm{root}(Q)}|
 2^{-\operatorname{depth}(Q)}=1
\]

exclude positive-area gaps, overlaps, and duplicate leaves; explicit seam
ownership checks protect the zero-area shared edges and both corners.  The
parent Riesz theorem
handles \(\operatorname{Re}s\ge256\); real conjugacy supplies the lower
half-strip, with the real-axis seam already contained in the upper cover.

The tracked certificate also repeats the limiting cell at 256-bit MPFR
precision and on its four dyadic grandchildren.  This is an independent
pressure replay of the rounding and cell-width estimates, not a substitute
for the 160-bit proof tree.

## Source-bound interruption recovery

The dyadic traversal can be checkpointed without turning a partial run into
evidence.  A checkpoint binds the complete source manifest, Riesz and orbit
parents, arithmetic environment, exact root rectangles and outward
\(\pi^+\), precision, threshold, maximum depth, correction radius, and the
specified depth-first stack and final leaf-sort conventions.  Its accepted
leaves together with its pending rectangles must replay as one exact
prefix-complete root partition; counts, proof-kind classification, geometry,
current worst cell, partial leaf digest, and stack order are checked before
resumption.  The writer is atomic, and it refuses to emit a checkpoint if a
bound source changes while the process is running.

Resumption appends to exactly that validated DFS frontier.  Since the final
claim digest sorts leaves by root and dyadic path, an interrupted-and-resumed
run has the same certificate and leaf digest as a one-shot run.  A real
outer-operator regression (20 cells, resume to 40, versus one-shot 40)
agreed in every dataclass field and in the leaf digest
`0e7ba9dbaa2bf563be003fc495689bb71ce590299eab49ace3f6217167789260`.
Checkpoint digest, source hash, geometry, precision, or stack-order mutants
are rejected.  The checkpoint itself never sets a theorem flag; only a
complete registered final partition can do so.

## Claim boundary

When the tracked cover is complete, it proves that the fixed-centre outer
orbit has zero nontranslation characteristic values in
(\operatorname{Re}s\ge0), hence no nontrivial Floquet multiplier on or
outside the unit circle and attracting linear Floquet index zero.  The
common-parameter-box count remains false in the ledger.  Establishing that
persistence will require a separate parameter-to-orbit variation estimate
and a neutral-pole-subtracted homotopy; shrinking the present centre ball
does not supply it.  Nonlinear attraction and biological pulse-control
claims also remain outside this certificate.
