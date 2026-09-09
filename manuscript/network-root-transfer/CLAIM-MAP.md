# Paper A statement and proof map

This file maps the current local revision of **Local fold matching in RFDE
networks with constrained delayed coupling** to its proofs. It is a
maintenance aid, not part of the article or a claim that this revision has
been publicly released.

## Main statements

| Claim | Statement | Proof |
| --- | --- | --- |
| Compatible-history manifold, finite matching function, and uniform derivatives | First main theorem, `thm:rw-local-fold-matching` in Section 2 | Section 4, `prop:fold-invariant-histories`, and `prop:finite-gap-bridge` in Appendix A |
| Unique nearby finite matching zero and derivative of `mu_N^fin` | `thm:rw-local-fold-matching`; `eq:rw-local-root-sensitivity` and `eq:rw-local-root-increment` | Nonzero matching slope, implicit differentiation, and integration along parameter segments in Section 4 |
| Exact stationary projection identity | `eq:rw-projection-identity` | Directly from `pi_N^T Delta B_k = 0` in Section 2 |
| Unrestricted first-moment range and norm-optimal right inverse | `thm:rw-first-moment-map` | Proof of that theorem in Section 3, using the rank-one construction |
| Exact range under a prescribed matrix pattern | `thm:rw-structured-delay-range` | Proof of that theorem in Section 3, including generator-supported directions |
| Dimension-independent transverse inverse | `lem:fredholm-dobrushin-inverse` | Dobrushin contraction and the Poisson semigroup expansion in Section 3 |
| Gaussian collective cokernel and triangular Fredholm formula | `lem:fredholm-collective-cokernel` and `thm:fredholm-reduction` | Weighted collective operator analysis and block elimination in Section 3 |
| Uniform fold sensitivity functional and reconstruction bounds | `cor:rw-fold-fredholm-coefficient` | Section 3, `prop:fredholm-dual-recovery`, and the explicit graph derivative/Gaussian pairing in Section 4 |
| Uniform nonzero response and cycle obstruction | `prop:rw-growing-families` | Proof of that proposition in Section 3 |
| Global invariant-manifold sections and scalar connection defining function | Hypotheses of `cor:rw-conditional-connection` in Section 5 | Application-specific input; not proved for the specified recovery modification |
| Comparison `E = G - D_N^fin`: level and `nu` derivative `O(delta^2)`, matrix derivative `O(delta^3)` | `eq:rw-conditional-connection-hypothesis` | Separate assumption in Section 5; not supplied by the local theorem |
| Conditional heteroclinic parameter on the specified branch | `cor:rw-conditional-connection` | Sign change, strict monotonicity, and the assumed invariant-manifold zero-set identity in Section 5 |
| Conditional connection sensitivity and centered conormal | `cor:rw-root-sensitivity`; remark containing `eq:rw-conormal-limit` | Direct implicit differentiation and centering in Section 5 |

Section 3 contains proofs of the range and growing-family statements, rather
than duplicate propositions. Appendix A contains the local graph and matching
estimates. The former connection Appendix B is removed; no active appendix
asserts a proof of the global comparison.

## Proof mechanism and its scope

The local result uses this chain:

1. The perturbation disappears under the stationary projection at a fixed
   history, but its first delay moment forces the transverse equation.
2. Uniform transverse contraction constructs a compatible-history invariant
   graph and controls its state and parameter derivatives on the growing
   fold interval.
3. The graph derivative gives `A_N^{-1} S_N`; heterogeneous quadratic
   coefficients and the Gaussian adjoint produce `Lambda_N`.
4. Differentiated finite boundary-value estimates transfer that coefficient
   to `D_N^fin`. Its nonvanishing `nu` derivative gives the unique nearby
   finite matching zero and its `delta^3` physical-parameter sensitivity.
5. Only an independently constructed global defining function and the stated
   comparison estimates allow the same calculation for a heteroclinic
   connection parameter.

The first-moment range calculation, Dobrushin inverse estimate, and triangular
Fredholm elimination can be used under their own hypotheses. They do not
supply a compatible-history invariant manifold or a differentiated matching
estimate for another RFDE. The affine singular fold orbit, Gaussian cokernel,
and explicit curvature pairing belong to the polynomial network model;
Section 6 identifies what must be established in another equation. The paper
does not claim a general new reduction method.

## Scope boundaries

- `mu_N^fin` depends on the specified finite boundary-value problems and is
  not asserted to be a global RFDE connection parameter.
- Uniformity concerns finite networks with common Dobrushin, coefficient,
  delay-support, and parameter bounds. Invertibility for each fixed network
  alone does not give that uniformity.
- The unrestricted right inverse generally uses dense matrices. Prescribed
  patterns have their own attainable range and bounds.
- The one-delay and layerwise row-sum degeneracies concern the first-moment
  contribution on the stated perturbation space. They do not exclude
  higher-order effects or other perturbation classes.
- The unmodified recovery equation does not provide the two prescribed outer
  equilibria used in the conditional application. Different smooth recovery
  modifications can have different finite-`delta` connection parameters.
- Neither the local theorem nor the conditional corollary identifies an
  experimental onset or pulse threshold.
- Figure 1 and the independent nine-point window grid use prescribed incoming
  histories and an outgoing-section condition. They do not compute `D_N^fin`
  or `G`, and their three solver refinements are not rigorous error bounds or
  evidence for the global invariant-manifold hypotheses.

## Source checks and version history

`tests/test_paper_a_sources.py` checks the active source inputs, unique and
resolved labels, bibliography keys, and supplied graphics. Analytic identities
and numerical regressions have separate tests; none substitutes for a proof
of the RFDE results.

`paper-a-pre-rewrite-2026-09-02` and `paper-a-dcds-submission-v1` archive earlier
versions. The current local revision has not yet been pushed or released.
