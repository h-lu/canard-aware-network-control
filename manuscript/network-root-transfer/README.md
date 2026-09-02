# Sensitivity of heteroclinic connections in networks of RFDEs

This directory contains Paper A:

> **Sensitivity of Heteroclinic Connections to Constrained Delayed Coupling
> in Networks of RFDEs**

## Main results

The instantaneous network matrix is row stochastic. Additional linear
feedback is distributed among finitely many delayed-coupling matrices. Admissible
perturbations preserve the sum of those matrices and have zero stationary row
at each delay. Therefore the stationary projection
of the RFDE vector field is unchanged at every history, although the projected
variables do not satisfy a closed equation.

The paper contains proved linear and local results, an abstract theorem under
explicit hypotheses, and a conditional model application.

1. With two distinct delay locations, the first moment of the constrained
   perturbation matrices maps onto the network-transverse space. The paper
   gives a sharp explicit right inverse and dimension-independent bounds.
   Eliminating the network-transverse equation in a Fredholm reduction yields
   a bounded linear functional `Lambda_N`.
2. A general Lyapunov--Schmidt theorem gives the derivative of a scalar
   defining function for a codimension-one connection once its invariant manifolds,
   transversality, and uniform expansion have been verified. For the
   polynomial network, the local fold calculation identifies the coefficient
   `Lambda_N`.
3. If a fixed smooth modification outside the fold neighborhood has the
   required uniform stable and unstable manifold sections and its
   heteroclinic defining function is `C^1`-close to the finite-interval
   matching function, its local connection parameter
   satisfies

   ```text
   D_eta mu_c(delta,eta)
     = delta^3 Lambda_N + O(delta^4 + delta^3 ||eta||),
   ```

   uniformly in the finite network size.

The third statement is an application theorem under explicit hypotheses; the
global invariant-manifold verification for the displayed modified equation is
not claimed complete. Different modified recovery equations may have
different finite-`delta` connection parameters. The paper does not prove a heteroclinic or
maximal canard for the unmodified recovery equation and does not identify an
experimental threshold.

## Source layout

- `main.tex`: article front matter, main text, appendices, declarations, and bibliography;
- `rewrite-sections/`: introduction, model and results, abstract Fredholm
  theorem, fold calculation, heteroclinic-connection hypotheses, and application
  conditions;
- `appendices/`: detailed estimates for the
  locally invariant manifold near the fold and the
  functional-analytic form of the global connection hypotheses; these are
  included in `main.pdf`, not issued as a separate supplement;
- `figures/`: editable Python sources, figure contracts, and generated vector
  PDFs;
- `../../experiments/results/three_node_finite_section_diagnostic.json`:
  reproducible values for the three-node numerical illustration;
- `CLAIM-MAP.md`: theorem-to-proof map and scope boundaries.

The former manuscript is preserved at the immutable tag
`paper-a-pre-rewrite-2026-09-02` and is not an input to the current build.

## Build and tests

```sh
make paper
make check
```

To regenerate the three-node values separately, run:

```sh
make diagnostic-data
```

Useful final checks are:

```sh
rg -n 'Warning|undefined|Overfull|Underfull' main.log
pdfinfo main.pdf
pdffonts main.pdf
```

The theorem is analytic and does not rely on a numerical certificate.
Figure 2 is a prescribed-history finite-section illustration of the sign and
scale of the local coefficient; it is not the matching function in the
proof, a heteroclinic computation, or a maximal-canard computation.  A public
source release and permanent archive identifier are still required before
submission.
