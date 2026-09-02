# Paper A: full rewrite for JNS readability, proof visibility, and reuse

Tracking issue: <https://github.com/h-lu/canard-aware-network-control/issues/34>

## Frozen baseline

- Source tag: `paper-a-pre-rewrite-2026-09-02`
- Commit: `22752faf992acef50fcab8157761602174a8f179`
- Archived PDFs: <https://github.com/h-lu/canard-aware-network-control/releases/tag/paper-a-pre-rewrite-2026-09-02>
- Verification at freeze: the main paper and supplement compile; all 95 Paper A tests pass.

The frozen tag and release are provenance records. Rewriting must occur on a separate branch and must not alter the frozen baseline.

## Rewrite outcome (2026-09-02)

The source audit performed during the rewrite found that the frozen draft did
not prove the network-size-uniform global invariant-manifold construction and
the weighted (C^1) comparison needed for an unconditional heteroclinic
connection in the displayed modified RFDE.  The rewritten paper therefore
narrows its claims instead of carrying that gap into a new presentation.

The first-moment range theorem, its explicit right inverse, the
dimension-uniform transverse inverse, the abstract Fredholm sensitivity
formula, and its local fold realization are unconditional.  Existence and
parameter sensitivity of a heteroclinic connection for the modified RFDE are
stated as a conditional corollary whose global invariant-manifold, defining-
function, comparison, and tracking assumptions must be verified in each
application.  No root of the unmodified biological model and no general
network-canard theory is claimed.

The checklist below records the original rewrite brief.  Any item that asked
the rewrite merely to present an unconditional exact connection has been
superseded by the narrower, audited claim boundary above.

## Initial editorial diagnosis

The frozen draft presented the mathematical result as closed, but still had a high desk-rejection risk at *Journal of Nonlinear Science*. The source audit later corrected that status as described above. Its initial expository problems were:

1. The main theorem appears before the reader has seen the network or the globally modified RFDE to which the exact heteroclinic root belongs.
2. The elementary source--transverse inverse--Fredholm pairing that explains the parameter response appears much later than the formal theorem.
3. Preparation-dependent comparison objects occupy more of the main text than their role in the final theorem warrants.
4. The decisive passage from a local comparison gap to an exact complete-history heteroclinic connection is largely deferred to the supplement.
5. The paper contains too much project terminology and repeatedly uses `physical` for a root of a fixed globally modified model. This conflicts with ordinary mathematical and experimental usage.
6. The reusable Fredholm argument is divided among many statements, whereas the model-specific construction of the exact connection has no comparably concise interface for a new application.
7. The current first figure combines three different reader tasks and mixes exact and schematic layers at a size that is difficult to read.

## Initial mathematical claim target

For the stated finite Markov RFDE networks with a network-size-uniform Dobrushin gap, a class of constrained perturbations of the delay layers is annihilated exactly by the stationary projection on every full history. With at least two distinct delays, its first delay moment can generate arbitrary transverse forcing with a network-size-uniform right inverse. The transverse response contributes to the collective Fredholm solvability condition through node heterogeneity. The frozen draft further aimed to identify this pairing with the leading derivative of a heteroclinic-connection parameter:

\[
D_\eta\mu_{c,N}^{\mathrm{anc}}
=\delta^3\Lambda_N+O(\delta^4+\delta^3\|\eta\|),
\]

with constants uniform in the network size. With a single merged delay, this first-moment mechanism vanishes on the redistribution class.

The first three conclusions are proved unconditionally in the rewrite.  The
displayed sensitivity statement is retained only under the explicit global
hypotheses described in the rewrite outcome.  Within that corrected scope,
the rewrite preserves all hypotheses, quantifier order, uniformity statements,
signs, scales, remainder bounds, and distinctions between exact, asymptotic,
and comparison objects.

## Hard terminology constraint

The rewrite must use established mathematical language wherever it exists. Preferred vocabulary includes:

- retarded functional differential equation (RFDE);
- stationary projection and non-closed projected dynamics;
- collective/transverse decomposition;
- Dobrushin contraction and transverse inverse;
- Fredholm alternative, adjoint kernel, cokernel, and Lyapunov--Schmidt reduction;
- stable and unstable manifolds in history space;
- complete orbit, heteroclinic connection, canard segment, and parameter sensitivity.

Remove project or promotional language such as `flagship theorem`, `declared channel`, `finite-core toolkit`, `preparation template`, and similar workflow labels. Do not coin a name for the source--inverse--pairing chain merely to brand it. A nonstandard term may remain only if it denotes a mathematically distinct object, is defined once, and is genuinely needed throughout the proof.

Use `anchored`, `globally modified`, or `intrinsic to the fixed modified RFDE`; do not redefine `physical` to mean membership in that model. Experimental or physical language may be used only when tied to a natural model, measurable quantity, and relevant literature.

## Rewrite tasks

### 1. Rebuild the first eight pages

- [ ] Open with the mathematical phenomenon: identical stationary projections need not imply identical connection-parameter sensitivity when the projection is not a closed quotient.
- [ ] Write the original shared-resource RFDE and the fixed globally modified RFDE before stating the exact-root theorem.
- [ ] Define the complete-history heteroclinic canard parameter in ordinary dynamical-systems language.
- [ ] Explain on one page the map
  \[
  \eta\longmapsto S_N\eta
  \longmapsto A_N^{-1}S_N\eta
  \longmapsto \Lambda_N(\eta).
  \]
- [ ] State in plain language why two distinct delays give a first-moment source and one merged delay does not.
- [ ] State the essential scope boundary once: the theorem concerns a fixed globally modified RFDE, not an experimentally identified root of the unmodified recovery law.
- [ ] Rewrite the abstract after the body is stable; it must state the question, theorem, mechanism, and scope without listing the proof machinery.

### 2. Replace the five-part main theorem by a clear hierarchy

- [ ] State one result for exact projection equality, the two-delay range/right inverse, the one-delay obstruction, and the resulting Fredholm sensitivity covector.
- [ ] State a separate result proving that the same covector is the leading derivative of the exact complete-history heteroclinic canard parameter in the fixed modified RFDE.
- [ ] Move dual recovery, conormal convergence, and comparison across admissible global modifications to corollaries.
- [ ] Qualify movement of the root by the non-vanishing of `\Lambda_N`; do not imply nonzero response for every admitted network.

### 3. Make the Fredholm argument directly reusable

- [ ] Consolidate the projection chain rule, moment inversion, transverse inverse, cokernel pairing, and root sensitivity into the smallest number of results supported by the current proofs.
- [ ] Formulate the reusable result using an exact connection-defining function whose zero set is the complete heteroclinic connection, rather than assuming an already constructed root.
- [ ] Give a one-page dictionary mapping the abstract objects `\Pi`, `S`, `L_\perp^{-1}`, `B`, the adjoint functional, and the connection-defining function to their realization in the shared-resource network.
- [ ] State explicitly what a new RFDE application must reprove: the transverse inverse, the scalar Fredholm obstruction, the complete-history invariant objects, and the comparison estimate.
- [ ] Distinguish structural arguments from the cubic shared-resource field, Gaussian adjoint calculation, curvature pairing, and the particular global modification.

### 4. Put the decisive exact-connection argument in the main text

- [ ] Include the spectral reason for the dimensions of the incoming unstable manifold and outgoing stable sheet.
- [ ] Display the half-line Lyapunov--Perron equation and explain the forward/backward integration directions actually used.
- [ ] State the contraction estimate and the history norm in which the stable sheet is obtained.
- [ ] Prove in the main text that the connection-defining function has zero set exactly equal to the complete-history heteroclinic connection.
- [ ] Include the central weighted `C^1` estimate transferring the local comparison coefficient to the exact connection-defining function.
- [ ] Explain the endpoint signs or transversality needed for the implicit-function argument.
- [ ] Retain detailed constants and subordinate estimates in the supplement only when the main text states their inputs, outputs, and role.

### 5. Demote proof scaffolding

- [ ] Replace the long preparation definition by one comparison construction and one proposition giving the exact properties later used.
- [ ] Move alternative preparations, equivalence of response jets, finite-section noncanonicity, raywise variants, and high-order bookkeeping to the supplement unless they are logically indispensable in the main argument.
- [ ] Merge repeated implicit-function and conormal statements.
- [ ] Remove repeated nonclaim paragraphs; retain one scope table and a concise closing qualification.
- [ ] Remove evidence-ledger and workflow language from the paper narrative.

### 6. Add a hand-checkable network example

- [ ] Give an explicit small stochastic matrix, stationary vector, two redistribution matrices, and heterogeneous curvature vector.
- [ ] Verify directly
  \[
  \pi_N^TR_k=0,\qquad R_0+R_1=0,\qquad
  S_NR\ne0,\qquad \Lambda_N(R)\ne0.
  \]
- [ ] Use the same example to show disappearance of the leading response for one merged delay and for the relevant homogeneous case.
- [ ] Keep the example inside the exact hypotheses of the theorem; do not use it as evidence for an experimental claim.

### 7. Redesign the figures by mathematical function

- [ ] Figure 1: one readable diagram showing stationary projection equality, transverse forcing from distinct delay moments, the transverse inverse, and the scalar Fredholm pairing. Mark exact identities and schematic layout separately.
- [ ] Figure 2: one history-space schematic showing the incoming branch, fold passage, outgoing stable sheet, and the complete heteroclinic connection in the fixed modified RFDE.
- [ ] Move comparison across different global modifications to a later scalar graph or omit it if prose and the conormal corollary suffice.
- [ ] Use different visual encodings for trajectories, invariant sheets, sections, exact algebraic arrows, and schematic guides. Inspect every figure at final printed size.

### 8. Rebuild the literature and application positioning

- [ ] Organize related work around the precise obstruction: exact projection equality removes direct sensitivity, but a non-closed projection can retain transverse dynamics that returns through the Fredholm obstruction.
- [ ] Compare separately with RFDE invariant-manifold theory, fast--slow/canard theory, Markov-network reduction or lumpability, observability/identifiability, and network-size-uniform contraction.
- [ ] Use the physical-root literature audit only to motivate real delayed systems and experimental thresholds. State explicitly that this paper does not calibrate the modified RFDE to an experiment.
- [ ] Do not argue novelty merely by claiming that a conjunction of familiar tools has not appeared before; identify the prior obstruction and the exact new implication.

### 9. Clean notation and prose

- [ ] Resolve collisions involving `C_N`, `S_N`, `P`, `Q`, and other reused symbols.
- [ ] Introduce notation at first use rather than in a project-status table.
- [ ] Use section titles naming mathematical objects or conclusions, not stages, interfaces, toolkits, or gates.
- [ ] Replace repeated internal qualifiers with one exact definition and one scope statement.
- [ ] Audit every nonstandard term for necessity and literature compatibility.

## Proposed main-text order

1. Introduction: problem, model, globally modified equation, exact connection parameter, main results, and scope.
2. Stationary projection and delay redistribution: exact identity, two-delay range, one-delay obstruction, and a small example.
3. Collective/transverse reduction and Fredholm sensitivity formula.
4. Complete-history invariant manifolds for the fixed globally modified RFDE.
5. Local canard matching and comparison with the exact connection-defining function.
6. Proof of the exact parameter-sensitivity theorem and consequences.
7. Conditions needed in other RFDEs, limitations, and discussion.

The final numbering may differ, but the reader must encounter the concrete RFDE and the exact root before the abstract reduction and proof scaffolding.

## Non-goals

- Do not add another biological, physical, or chemical model merely to claim relevance.
- Do not claim an experimentally measured or unmodified-model maximal canard.
- Do not claim a general theory of canards in arbitrary networks or RFDEs.
- Do not add new theorem layers unless they remove a precise obstacle to naturality or reuse.
- Do not expand the manuscript to preserve every development-stage result in the main text.

## Acceptance gates

- [ ] A nonlinear-dynamics reader can identify within the first five pages: the equation, the invisible perturbation, the transverse quantity that remains, the returned scalar, the exact root, and the scope boundary.
- [ ] The main theorem can be restated without using project-specific terminology.
- [ ] Every theorem clause maps to a locatable proof and preserves the frozen claim's hypotheses, scales, uniformity, and remainder.
- [ ] The main text alone exposes the decisive comparison from the local coefficient to the exact complete-history connection.
- [ ] A reader working on another RFDE can list the hypotheses that must be verified without reverse-engineering the shared-resource calculation.
- [ ] The small network example can be checked by hand from the displayed matrices.
- [ ] Each figure has one primary mathematical purpose and remains legible in the rendered PDF.
- [ ] The words `physical`, `flagship`, `pipeline`, `toolkit`, `ledger`, and `template` do not carry mathematical claims unless their ordinary meaning is intended and justified.
- [ ] The main paper and supplement compile from a clean tree; all Paper A tests pass.
- [ ] A main-text-only cold read reconstructs the object, theorem, prior obstruction, mechanism, proof spine, reusable part, model-specific part, and one important nonclaim.
- [ ] The submission-facing repository and frozen release are publicly accessible and match the cited version.
