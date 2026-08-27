# Paper A claim and proof map

This file maps the acceptance criteria in
[Issue #30](https://github.com/h-lu/canard-aware-network-control/issues/30)
to the proof-strengthened manuscript.  It is an audit aid, not part of the
paper.

## Central principle

For every common value of the matching parameter `nu`, an atomwise
stationary-row-neutral delay redistribution satisfies the exact identity

```text
Pi_N F_{N,delta,nu,zeta} = Pi_N F_{N,delta,nu,0}
```

on the full RFDE history space.  The two `nu`-parametrized matching problems
nevertheless have different selected complete-history roots whenever the
leading transverse-return coefficient is uniformly nonzero.  The mechanism
is

```text
delay moment -> transverse Markov resolvent -> heterogeneous curvature
             -> normalized complete-history gap -> selected root shift.
```

## Acceptance map

| Acceptance item | Manuscript statement | Proof location |
| --- | --- | --- |
| Exact projection blindness | `prop:projection-blindness` | Direct use of `pi_N^T R_{k,N}=0` in Section 2 |
| Existence of the preparation class | `lem:preparation-existence` | Plateau, saturation, flow-box, and normal-extension construction in Section 2; tame frozen-flow verification in Appendix A |
| Dimension-uniform root and response | `thm:shared-resource` | Invariant-history graph and trace range in Section 4 and Appendix A; exact finite-section gap in Appendix B; abstract root transfer in Section 3 |
| Projection non-identifiability | `cor:projection-nonidentifiability` | Root-separation estimate following the main theorem proof |
| Generic leading response | `thm:response-directions` | Bounded functional, codimension-one kernel, and curvature-variance witness in Section 4.1.2 |
| Two-preparation leading universality | `cor:preparation-universality` | Difference of the two uniform response expansions |
| Uniform robust neighborhood | first part of `cor:robust-asynchronous` | Lipschitz bound for `Lambda_N` around the reference direction in Section 4.1.3 |
| Actual asynchronous root orbit | second part of `cor:robust-asynchronous` | Fixed slow-time profile and oscillation lower bound in Section 4.1.3 |
| No nontrivial synchrony quotient | explicit witness after `cor:preparation-universality` | Failure of vector-field tangency to every nonsingleton polydiagonal |

## Contribution map

```text
projection and network-canard theories allow collective reduction
    but do not decide a history-matching root from a projected functional
        -> atomwise row neutrality gives exact projected blindness
        -> a uniform invariant-history range problem exposes the hidden mode
        -> transverse resolvent and heterogeneous curvature return that mode
        -> an adjoint gap identity transfers the return into a root shift.
```

The new conclusion is the failure of projection identifiability for a
selected complete-history root.  Dobrushin contraction, the fold normal form,
and the scalar implicit-function theorem are enabling ingredients rather than
the claimed novelty.

## Proof spine and verification gates

| Link | Input | Output | Decisive reason | Required location |
| --- | --- | --- | --- | --- |
| Transverse inverse | Common Dobrushin gap | `N`-uniform semigroup and resolvent bounds on `E_N` | Poisson expansion in oscillation norm | Section 4.1.1 |
| History graph | Prepared chart field and fixed atomic evaluations | Injective invariant complete-history graph with finite mixed jets | Special-flow contraction plus finite block-triangular prolongation | Section 4.1.1 and Appendix A |
| Selected traces | Reduced graph field and endpoint/phase rows | Two one-sided solutions with uniform inverse | Explicit Gaussian Green operator | Section 4.1.1 |
| Hidden return | Row-neutral delay moment and heterogeneous curvature | `D_zeta q_1=0`, explicit `D_zeta q_2` | Direct projected term cancels while the transverse resolvent survives | Section 4.1.2 |
| Exact gap | Selected finite traces and first integral | Uniform gap and derivative expansions | Finite-section identity plus an explicit six-part error decomposition | Appendix B |
| Root response | Gap transversality and structural coefficient | Local root and `delta^3` displacement | Uniform range-to-root theorem | Section 3 and the model application in Section 4 |

No theorem is promoted on the strength of a formal coefficient alone.  The
history-graph and exact-gap links are the two load-bearing proof gates.

## Quantifier boundaries

- Open/dense genericity is asserted for each fixed finite network, not for an
  unrestricted sequence space of network families.
- The robust ball is uniform in network size but is an operator-norm ball; it
  need not preserve entrywise positivity of every delayed layer.
- Preparation universality concerns the leading response increment from each
  preparation's own `zeta=0` baseline.  Equality of the finite-`delta`
  baselines is not claimed.
- Vanishing of the leading coefficient does not exclude a higher-order root
  response.
- The selected root is not identified with a preparation-independent maximal
  canard or a physical pulse threshold.

## Reproduction and provenance

From this directory, run:

```bash
make
```

The generated manuscript PDF is intentionally ignored; the figure source and
vector figure are tracked.  The pre-refocus source is preserved by the tag
`paper-a-before-hidden-response-refocus`.

The proof-strengthened build has 44 letter-size pages.  Its final local PDF
has SHA-256
`4f1139e07b64960c2a6b8179e946ff1d07650f93d8e8634d6db2b4fc0254c0a9`.
The corresponding proof-source commit is
`050fedf3a75421ef5caaf4ec3f177653899af6eb`.
The final `latexmk` log has no unresolved citation/reference, box, font, or
fatal diagnostics; every PDF font is embedded.  Two independent cold reads
reconstructed the history-graph and finite-gap bridges and found no fatal
proof break after the reported local quantifier and notation repairs were
applied.
