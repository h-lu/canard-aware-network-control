# Physical pulse-threshold manuscript

This directory is the focused research working draft for the model-specific
delayed FitzHugh--Nagumo pulse problem.  It intentionally excludes the finite
network canard-root transfer theorem, frequency--amplitude control
coordinates, and asynchronous-network safety estimates.

The proof spine is:

1. construct a common complete-history pulse event;
2. obtain a smooth selected near-two-period return and its hyperbolic linear
   splitting;
3. bound the six continuous-history Hessian blocks needed for an effective
   stable graph;
4. identify that graph with the periodic orbit's stable-set germ;
5. prove a unique pulse/stable-sheet crossing;
6. attach the two sides to the quiet and outer attraction tubes.

Steps 1 and the linear part of step 2 are proved.  The abstract Hessian
identity, quotient norm, bimeasure residual implication, qualitative local
graph, pulse event, derivative, endpoint functional signs, stable-coordinate
containment, and a microscopic outer local return are also proved.  The
preferred-scale return domain, all six numerical Hessian caps, an effective
stable graph, stable-set identification, the crossing, and two-sided routing
remain open.

## Provenance

The general selected-return theorems and the model-specific propositions were
migrated from `manuscript/flagship/` without strengthening their conclusions.
Internal Stage identifiers and full SHA/test ledgers remain in the repository
evidence records and are not part of this paper's mathematical narrative.

## Build

From this directory run:

```sh
make
```

The build uses the shared bibliography at `../../references/references.bib`.

