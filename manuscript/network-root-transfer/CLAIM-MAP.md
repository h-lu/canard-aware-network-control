# Paper A claim and proof map

This file maps the acceptance criteria in
[Issue #29](https://github.com/h-lu/canard-aware-network-control/issues/29)
to the refocused manuscript.  It is an audit aid, not part of the paper.

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
| Existence of the preparation class | `lem:preparation-existence` | Plateau, saturation, flow-box, and normal-extension construction in Section 2 |
| Dimension-uniform root and response | `thm:shared-resource` | Invariant-history graph, one-sided trace solve, adjoint pairing, and implicit root argument in Section 3 |
| Projection non-identifiability | `cor:projection-nonidentifiability` | Root-separation estimate following the main theorem proof |
| Generic leading response | `thm:response-directions` | Bounded functional, codimension-one kernel, and curvature-variance witness in Section 3 |
| Two-preparation leading universality | `cor:preparation-universality` | Difference of the two uniform response expansions |
| Uniform robust neighborhood | first part of `cor:robust-asynchronous` | Lipschitz bound for `Lambda_N` around the reference direction |
| Actual asynchronous root orbit | second part of `cor:robust-asynchronous` | Fixed slow-time profile and oscillation lower bound in Section 3 |
| No nontrivial synchrony quotient | explicit witness after `cor:preparation-universality` | Failure of vector-field tangency to every nonsingleton polydiagonal |

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

The refocused build produces a 22-page PDF with no LaTeX/BibTeX warnings,
undefined references, or overfull/underfull boxes.  The generated manuscript
PDF is intentionally ignored; the figure source and vector figure are
tracked.  The pre-refocus source is preserved by the tag
`paper-a-before-hidden-response-refocus`.
