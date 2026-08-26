# Outer leaky Floquet cover: rectilinear calibration ledger

This note records a failed algorithmic calibration.  It is deliberately
separate from the theorem artifact: neither run completes the upper
principal rectangle, and no Floquet count is promoted.

## Corrected local ownership

The upper rectangle is partitioned into the exact roots

\[
 [0,a]^2,\qquad [a,256]\times[0,\pi^+],\qquad
 [0,a]\times[a,\pi^+],\qquad a=0.002.
\]

Exact rational arithmetic verifies that the first root lies strictly inside
the parent's punctured neutral disk.  It is accepted once, as the unique
`riesz_local_disk` leaf.  Every cell descended from either complementary
root uses the full infinite-operator Neumann test, even if that cell happens
to lie inside the circular parent disk.  This fixed ownership is essential:
an earlier calibration mistakenly reapplied the circular shortcut inside the
complement, produced 93 local leaves after 5,000 cells, and recreated the
non-dyadic circular seam.  That trajectory is superseded and claim-free.

The checkpoint and final validators now require exactly one local leaf with
`root_id="neutral_core"` and the empty path.  A noncore local leaf, a split
neutral core, or a pending neutral core is rejected.

## Equal-budget threshold comparison

Both corrected runs bind the same engine source, Riesz parent, exact-center
outer orbit, 160-bit arithmetic, three root rectangles, mode-64 finite
cutoff, full coefficient support through mode 256, and nested orbit radius
\(10^{-8}\).  They differ only in the cell-acceptance threshold.

| budget | threshold | accepted | local | Neumann | pending | depth | worst accepted \(q\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 200 | 0.999 | 81 | 1 | 80 | 41 | 43 | 0.8869047156191458739 |
| 200 | 0.9999 | 81 | 1 | 80 | 41 | 43 | 0.8869047156191458739 |
| 5,000 | 0.999 | 2,482 | 1 | 2,481 | 39 | 43 | 0.9987714193377148382 |
| 5,000 | 0.9999 | 2,482 | 1 | 2,481 | 39 | 43 | 0.9998498402736018019 |

At 5,000 processed cells the accepted normalized areas are respectively

\[
 5.309192894673245\times10^{-9},\qquad
 5.310329754168677\times10^{-9}.
\]

The looser threshold therefore gains only \(0.0214130381\%\) in accepted
area, with exactly the same accepted and pending counts.  It does not remove
the near-neutral conditioning cost.  A 300,000-cell run was consequently not
started.  Pending cells remain in a finite complement near
\(\operatorname{Re}s\simeq0.002\), so this is no longer an infinite circular
seam; nevertheless the observed scale is too large to treat brute-force
subdivision as the flagship proof route.

## Proposed pole-subtracted route

A non-rigorous binary64 diagnostic at \(s=0\) supports a one-dimensional
Grushin reduction.  For the outer cutoff-64 finite pencil, the smallest and
second-smallest singular values were approximately

\[
 4.90\times10^{-13},\qquad 1.92159.
\]

With fixed SVD-guide border scales 20 and 5, the bordered finite matrix had
condition number about 217.76, one-norm inverse about 1.44461, and candidate
effective-Hamiltonian slope
\(|E'_{-+}(0)|\approx2.66812\times10^{-4}\).  These are feasibility
diagnostics only; they are not directed enclosures and carry no claim.

The next rigorous route should:

1. construct a fixed-border complete Grushin operator from the exact-center
   outer source, retaining coefficient support 256 and tail modes through
   320;
2. prove its finite-plus-tail inverse uniformly on a small closed complex
   disk, with the \(10^{-8}\) orbit correction, period variation, and the
   physical unshifted-coefficient/output-row delay phase;
3. use the exact autonomous translation root and the parent's algebraic
   simplicity theorem to factor \(E_{-+}(s)=s g(s)\);
4. give a directed Rouché or homotopy bound
   \(\lvert g(s)-a_*\rvert<\lvert a_*\rvert\), thereby excluding every
   nontranslation zero in that disk; and
5. hand the remaining, now well-separated rectangles back to the existing
   full-operator Neumann cover, followed by independent 256-bit and finer-cell
   stress replay.

The parameter-box-uniform version would additionally require a directed
parameter-to-orbit sensitivity and a neutral projection continuation.  It
cannot be inferred from the exact-center \(10^{-8}\) ball.

## Claim ledger

All theorem-facing flags remain false: complete right-half zero exclusion,
the centre outer Floquet count, parameter-box-uniform count, unit-circle
exclusion, attracting Floquet index, quantitative semigroup or stable-tube
bounds, nonlinear attraction, a history separator, and biological pulse
control.  In particular, these calibrations neither establish a spectral
gap to the left of the imaginary axis nor provide the resolvent/semigroup
constants and nonlinear history remainder needed for an attracting tube.
