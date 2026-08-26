# Shifted coefficients and Fourier--Floquet delay phases

Status: **proved representation identity; legacy FHN claims restored and the
leaky replay repaired.**  An
earlier version of this note incorrectly treated every output-mode phase as
an indexing error.  The physical delayed variational term admits two exactly
equivalent Fourier representations.  Correctness depends on whether the
stored time-periodic coefficient has already been shifted by the delay.
This note records the repaired identity, the actual affected calculation,
and the acceptance protocol.

## 1. The physical coefficient is delayed too

Normalize the periodic orbit to period one and write the unshifted scalar
coefficient as

\[
 b(\theta)=\sum_{p\in\mathbb Z}b_p e^{2\pi ip\theta},
 \qquad
 y(\theta)=\sum_{m\in\mathbb Z}y_m e^{2\pi im\theta},
 \qquad \alpha=\tau/T.
\]

For an RFDE term \(G(v(t-\tau))\), linearization along a periodic orbit
produces

\[
 e^{-s\alpha}b(\theta-\alpha)y(\theta-\alpha),          \tag{1.1}
\]

not \(b(\theta)y(\theta-\alpha)\).  Expanding both delayed factors gives

\[
 \boxed{
 [e^{-s\alpha}b(\cdot-\alpha)y(\cdot-\alpha)]_n
 =e^{-s\alpha-2\pi in\alpha}
   \sum_m b_{n-m}y_m.}                                  \tag{1.2}
\]

Thus, when \(b_p\) denotes the **unshifted** coefficient, the phase belongs
to the output mode \(n\): the convolution matrix is multiplied on the left
by the row-phase diagonal.

Alternatively define the already shifted coefficient

\[
 \widetilde b_p=e^{-2\pi ip\alpha}b_p,
 \qquad b(\theta-\alpha)=
       \sum_p\widetilde b_p e^{2\pi ip\theta}.
\]

Then the same physical term is

\[
 \boxed{
 [e^{-s\alpha}b(\cdot-\alpha)y(\cdot-\alpha)]_n
 =\sum_m\widetilde b_{n-m}
   e^{-s\alpha-2\pi im\alpha}y_m.}                     \tag{1.3}
\]

Here the phase belongs to the input mode \(m\): the shifted-coefficient
convolution matrix is multiplied on the right by a column-phase diagonal.
Equations (1.2) and (1.3) agree entrywise because

\[
 e^{-2\pi i(n-m)\alpha}e^{-2\pi im\alpha}
 =e^{-2\pi in\alpha}.                                  \tag{1.4}
\]

The two invalid mixed representations are therefore

\[
 \text{unshifted coefficient + input/column phase},
 \qquad
 \text{shifted coefficient + output/row phase}.        \tag{1.5}
\]

An oracle that checks only a displayed formula without checking the semantic
meaning of its coefficient sequence cannot distinguish (1.2)--(1.5).

## 2. Period and orbit corrections

The equivalence also fixes the moving-period majorants.  In the shifted
coefficient representation, varying \(T\) changes both
\(\widetilde b_{n-m}\) and the input phase.  Their frequency factors add:

\[
 (n-m)+m=n.                                             \tag{2.1}
\]

Hence the complete physical delay factor varies with the **output**
frequency.  The unshifted-coefficient/row-phase representation exposes this
directly.  In particular:

- every finite-output block, including finite-from-tail, uses the finite
  output cutoff;
- tail-from-finite first carries the tail-output frequency, but multiplication
  by the fast-tail inverse permits the validated \((1+A_{\rm tail}h)\)-type
  cancellation;
- using only the input frequency while treating the shifted coefficient as
  independent of \(T\) omits part of the physical variation.

Coefficient-norm variations unrelated to the delay phase remain separate.
The four orbit/period corrections must be derived from one complete physical
representation and then checked against the equivalent one.

## 3. Actual claim impact

The legacy FHN Bloch and right-half sources store the unshifted sequence
`delayed_state_derivative` and multiply it by output-mode phases.  This is
the physically correct representation (1.2), not an indexing defect.  The
earlier blanket withdrawal on the ground “row phase is wrong” is therefore
retracted.

The new leaky replay briefly combined the unshifted coefficient with input
phases.  That calculation represented neither (1.2) nor (1.3); it was
stopped before any global artifact was issued.  The repaired leaky code now
uses (1.2) as its main matrix and independently verifies (1.3), while hostile
tests reject both mixed forms in (1.5).

For the legacy FHN artifacts, source-level algebra supports their original
phase convention.  The bound theorem notes were restored byte-for-byte, so
their original source manifests remain valid.  An independent regression
test now verifies (1.2)--(1.4), binds the legacy Bloch and right-half sources
to the unshifted/output convention, distinguishes the shifted coefficient
sequences, and rejects both mixed forms by a positive numerical gap.  The
focused legacy source/hash validators and this four-test representation suite
pass.  The legacy hyperbolicity, right-half index and dependent fixed-network
attraction claims therefore retain their original proved status; no proof
tree was changed or silently rebound.

The following results never depended on this representation dispute and
retain their status:

- the two-module complete-history canard theorem;
- periodic-orbit radii, phase-bordered inverse and extrema theorems;
- norm-only Riesz tail and far-right reductions;
- quiet Razumikhin basins and complete-history pulse capture;
- Dobrushin transverse Halanay, complete-line inverse, and nonlinear
  stripwise synchronization;
- periodic parameter-response calculations.

## 4. Mandatory acceptance protocol

A delayed Fourier--Floquet certificate is accepted only if all of the
following hold.

1. The source declares whether each coefficient sequence is unshifted or
   already delay-shifted, separately for every delay slot.
2. A direct entrywise oracle proves
   \[
   \text{unshifted + row phase}
   =\text{shifted + column phase}
   \]
   on finite-to-finite, finite-from-tail, and tail-from-finite blocks.
3. Hostile mutations using either mixed form in (1.5) disagree by a recorded
   positive amount.
4. The orbit/period correction oracle differentiates the complete physical
   term.  It recovers output-frequency bounds and the justified fast-tail
   cancellation; input-only mutations must fail.
5. Deep dyadic geometry uses exact rational endpoints or outward arithmetic
   at adequate precision.
6. Every local disk, compact keyhole, tail, far-right region and conjugate
   half-strip is covered without an unrecorded seam.  One local positive-root
   disk does not prove the total unstable index.
7. Shared arithmetic helpers remain source-neutral, and every source hash,
   parent hash, proof-tree digest and dependent claim is rebound only after
   a changed proof source passes the corrected replay.  A representation
   audit that leaves the bound proof sources unchanged must preserve, rather
   than rewrite, their frozen manifests.

This protocol distinguishes an algebraically equivalent representation from
a genuine mixed-representation error and prevents either a row-only or a
column-only slogan from replacing an operator-level check.
