# Paper A: JNS rewrite and major-revision record

Tracking issue: <https://github.com/h-lu/canard-aware-network-control/issues/34>

## Frozen baseline

- Source tag: `paper-a-pre-rewrite-2026-09-02`
- Commit: `22752faf992acef50fcab8157761602174a8f179`
- Archived PDFs: <https://github.com/h-lu/canard-aware-network-control/releases/tag/paper-a-pre-rewrite-2026-09-02>

The frozen version is a provenance record. It is not an input to the current
submission build.

## Editorial decision

The revised paper follows the unconditional Fredholm-sensitivity route. It no
longer presents existence of a complete-history heteroclinic connection as
the main theorem. The title is

> **Fredholm Sensitivity to Constrained Delayed Coupling in Networks of RFDEs**

The unconditional results are:

1. the exact stationary-projection identity;
2. the range, norm, and norm-optimal right inverse of the unrestricted first
   delay-moment map;
3. the exact range under a prescribed linear matrix pattern, including a
   fixed-support realization with a dimension-uniform right inverse under the
   Dobrushin hypothesis;
4. the dimension-uniform transverse inverse and Fredholm functional;
5. the realization of that functional in a local RFDE fold-matching problem;
6. an explicit growing network family with nonzero coefficient independent of
   network size, together with a sparse-cycle family showing where uniformity
   fails.

The heteroclinic statement is a separate conditional application. The
spectral indices, global invariant-manifold sections, scalar defining
function, uniform comparison estimate, and orbit tracking are hypotheses.
They are not inferred from the displayed network assumptions.

## Response to the strict review

| Review concern | Revision |
| --- | --- |
| Title and abstract overstate an unproved connection theorem | Retitled and rewrote the front matter around the unconditional Fredholm functional; the connection appears only in the final conditional sentence of the abstract. |
| Main theorem mixes unconditional algebra with conditional global dynamics | Reordered the paper so the unconditional range, inverse, Fredholm, local-fold, and growing-family results precede the modified recovery equation and conditional connection corollary. |
| The admissible matrix space is too broad to preserve a network topology | The unrestricted theorem is now explicitly labeled as such. A separate theorem gives the exact range for any prescribed linear matrix pattern and a generator-supported realization. |
| The dense rank-one inverse is not structurally natural | Added the fixed-support inverse \(J_Ny=(P_N-I)\operatorname{diag}(((P_N-I)|_{E_N})^{-1}y)\), an explicit uniform norm bound, and nonnegative base layers. |
| Layerwise row-sum-preserving perturbations were not discussed | Added the exact obstruction: if every allowed direction has zero row sum, the first-moment map vanishes. |
| The example used a zero delay, so one delayed layer was inactive | Replaced it by two positive delays \((1,2)\); both base layers are active and the theoretical coefficient is unchanged. |
| Uniformity in \(N\) was only stated, not exhibited | Added an analytic growing family with \(\Lambda_N=-K\sigma/(2D\rho)\) for every \(N\), a uniformly bounded perturbation direction, and a numerical sequence for \(N=3,5,9,17,33\). |
| Dobrushin mixing excludes many local sparse networks | Added a lazy-cycle comparison with inverse norm at least \(N/(4D\rho)\), and separated the algebraic transverse-inverse requirement from the exponential stability used by the local invariant graph. |
| The spectral appendix argued circularly | Removed the spectral lemma. Every spectral and global property needed by the conditional application is now part of the explicit global hypothesis. |
| The numerical figure did not directly illustrate the revised main claim | Rebuilt Figure 2 as a three-part diagnostic: movement of the section zero, the \(\delta\)-scaled coefficient and same-delay control, and persistence along a growing network family. Its caption states exactly what is and is not computed. |
| Two-document submission and project vocabulary obstruct readability | The article and proof appendices now build as one PDF. Submission-facing prose uses standard RFDE, Fredholm, invariant-manifold, matrix-pattern, and sensitivity terminology. |

## Reusable interface

For another RFDE application, the operator calculation requires maps

\[
  S:\mathcal T\to\mathcal Y_\perp,
  \qquad L_\perp^{-1},
  \qquad \mathcal B,
  \qquad \ell,
\]

with the direct perturbation terms either absent or in the collective range.
The sensitivity functional is

\[
 -\frac{\ell\mathcal B L_\perp^{-1}S}{\ell f_\nu}.
\]

A connection application must additionally construct its own invariant
manifolds and scalar defining function and verify the required uniform
\(C^1\) expansion. The abstract calculation does not supply these objects.

## Submission gates

- [x] One submission PDF containing both proof appendices.
- [x] Unconditional main result visible in the title, abstract, and first
  pages.
- [x] Conditional global application stated after the unconditional results.
- [x] Exact matrix-pattern range and row-sum obstruction stated.
- [x] Positive-delay hand-checkable example included.
- [x] Growing-network analytic and numerical examples included.
- [x] Figure sources and numerical data are reproducible.
- [x] Public theorem-to-proof map and claim boundaries are current.
- [x] LaTeX build has no undefined references or layout warnings.
- [x] All fonts are embedded and every PDF page has been visually inspected.
- [ ] Freeze a versioned public release and permanent archive identifier for
  the submitted version.

## Scope boundary

The paper does not prove a maximal canard for the unmodified recovery law, an
experimentally calibrated threshold, or a general canard theory for arbitrary
RFDE networks. It proves a dimension-uniform Fredholm sensitivity mechanism
for the stated delayed network class and a local fold realization, with an
explicitly conditional connection application.
