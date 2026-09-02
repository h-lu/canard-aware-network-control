# Fredholm sensitivity to constrained delayed coupling in networks of RFDEs

This directory contains Paper A:

> **Fredholm Sensitivity to Constrained Delayed Coupling in Networks of RFDEs**

## Main results

The instantaneous network matrix is row stochastic. Additional linear
feedback is distributed among finitely many delayed-coupling matrices. Admissible
perturbations preserve the sum of those matrices and have zero stationary row
at each delay. Therefore the stationary projection
of the RFDE vector field is unchanged at every history, although the projected
variables do not satisfy a closed equation.

The paper contains unconditional linear and local results, followed by a
clearly separated conditional model application.

1. With two distinct delay locations, the first delay moment maps the
   unrestricted admissible perturbation space onto the network-transverse
   space. The paper computes its norm and a norm-optimal right inverse in the
   stated norms. For a prescribed matrix pattern, it gives the exact range
   and a fixed-support realization with uniform bounds under Dobrushin mixing.
2. Eliminating the transverse equation gives the dimension-uniform Fredholm
   functional `Lambda_N`. A local RFDE invariant-manifold construction near a
   fast--slow fold identifies this coefficient in the derivative of a
   finite-interval matching function. Explicit growing families show both a
   nonzero response uniform in `N` and the loss of uniformity on local cycles.
3. Separately, if a fixed smooth modification outside the fold neighborhood has the
   required uniform stable and unstable manifold sections and its
   heteroclinic defining function is `C^1`-close to the finite-interval
   matching function, its local connection parameter
   satisfies

   ```text
   D_eta mu_c(delta,eta)
     = delta^3 Lambda_N + O(delta^4 + delta^3 ||eta||),
   ```

   uniformly in the finite network size.

Only the third statement is conditional. The
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
- `../../experiments/results/growing_network_finite_section_diagnostic.json`:
  reproducible values for the growing-network illustration;
- `CLAIM-MAP.md`: theorem-to-proof map and scope boundaries.

The former manuscript is preserved at the immutable tag
`paper-a-pre-rewrite-2026-09-02` and is not an input to the current build.

## Build and tests

```sh
make paper
make check
```

To regenerate both numerical illustrations, run:

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
Figure 2 contains prescribed-history finite-section illustrations of the sign,
scale, and network-size persistence of the local coefficient; it is not the
matching function in the proof, a heteroclinic computation, or a
maximal-canard computation. A public
source release and permanent archive identifier are still required before
submission.
