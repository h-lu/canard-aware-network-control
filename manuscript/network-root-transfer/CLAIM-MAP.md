# Paper A theorem and proof map

This file maps the public statements of the rewritten manuscript to their
proofs. It is a maintenance aid, not part of the submitted article.

## Main statements

| Claim | Public statement | Proof |
| --- | --- | --- |
| Exact projection identity | Equation `eq:rw-projection-identity` | Directly from `pi_N^T Delta B_k=0` in Section 2 |
| Range of the unrestricted first delay moment | Theorem `thm:rw-first-moment-map` | `prop:fredholm-two-delay-inverse` |
| Exact range under a prescribed matrix pattern | Theorem `thm:rw-structured-delay-range` | `prop:fredholm-structured-delay-range` |
| Dimension-independent inverse bounds | Theorems `thm:rw-first-moment-map`, `thm:rw-structured-delay-range`, and Corollary `cor:rw-fold-fredholm-coefficient` | Rank-one and generator-supported constructions plus `lem:fredholm-dobrushin-inverse` in Section 3 |
| Fredholm solvability formula | `thm:fredholm-reduction` | Collective/network-transverse block elimination and Gaussian cokernel pairing in Section 3 |
| Uniform response and sparse-cycle boundary for growing networks | `prop:rw-growing-families` | `prop:fredholm-growing-families` |
| Sensitivity theorem from a defining function | `thm:fredholm-heteroclinic-sensitivity` | Quantitative implicit-function argument in Section 3 |
| Fold reduction and locally invariant manifold | `prop:fold-invariant-histories` | Section 4 and Appendix A |
| Local invariant manifold and finite-interval matching sensitivity | `thm:rw-local-fold-matching` | Section 4 and `prop:finite-gap-bridge` in Appendix A |
| Global invariant manifolds and heteroclinic defining function | Explicit hypotheses in Section 5 | Application-specific input; not proved for the displayed smooth modification |
| `C^1` comparison with the finite-interval matching function | Explicit hypothesis in Section 5 | Application-specific input; the required estimate is stated, not verified |
| Conditional heteroclinic parameter value | `cor:rw-conditional-connection` | General sensitivity theorem plus the Section 5 hypotheses |
| Conditional parameter derivative and conormal | `cor:rw-root-sensitivity` | Implicit differentiation and `cor:modified-conormal` in Section 5 |

## What can be reused

The following statements are independent of the particular quadratic
fast--slow model once their hypotheses are verified:

- the first-moment map for two distinct delays, its unrestricted right inverse,
  and its exact range under a prescribed linear matrix pattern;
- the Dobrushin inverse on \(\ker\pi_N^T\), with bounds independent of network size;
- the block Fredholm formula `-ell B L_perp^{-1} S / (ell f_nu)`;
- the quantitative sensitivity theorem for any separately constructed scalar
  defining function satisfying the stated expansion.

Section 6 gives the dictionary needed to apply these statements to another
RFDE. In particular, another application must construct its own invariant
manifolds and a scalar defining function; the abstract theorem does not
provide them automatically.

## Model-specific ingredients

A heteroclinic application additionally requires:

- the explicit affine singular fold orbit and Gaussian adjoint solution;
- heterogeneous quadratic coefficients;
- the chosen smooth modification of the recovery equation outside the fold neighborhood;
- the stated spectral indices, uniform hyperbolicity, and
  parameter-dependent invariant-manifold sections;
- a quantitative comparison between a finite-interval matching function and the
  stable manifold of that same RFDE.

The local fold ingredients are computed in the paper. The global
invariant-manifold and comparison estimates remain assumptions for the
displayed extension and must be proved in every concrete application.

## Scope boundaries

- The unmodified recovery law does not have the two prescribed equilibria
  outside the fold neighborhood used in the conditional application.
- Different admissible smooth modifications may yield different parameter values.
  Under the stated hypotheses, the separately centered leading conormal has
  the same limit.
- The theorem does not identify a biological onset, pulse threshold, or
  experimentally measured parameter.
- The one-delay statement concerns the first moment on the stated
  perturbation space. It does not exclude higher-order responses or other
  perturbation classes.
- Uniformity is over finite networks satisfying the common Dobrushin,
  coefficient, delay-support, and parameter bounds written in the theorem.
- Figure 2 integrates prescribed incoming histories and imposes a scalar
  outgoing-section condition. It checks the sign and scale of the three-node
  coefficient and its persistence along one growing family, but is not the
  two-trace function `D_N^fin`, the connection defining function `G`, or
  evidence for the global invariant-manifold hypotheses.
