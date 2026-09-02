# Manuscript workspaces

The repository separates papers by mathematical question. Shared source
history is retained in one repository; the papers are not maintained as
permanently divergent Git branches.

| Workspace | Question | Status |
| --- | --- | --- |
| `network-root-transfer/` | How can constrained perturbations of delayed coupling enter a Fredholm solvability condition when the stationary projection is unchanged? | Rewritten article and supplement |
| `pulse-threshold/` | Can a physical pulse threshold in a delayed FitzHugh--Nagumo model be proved through a stable-manifold crossing and two-sided routing? | Incomplete research draft |
| `rfde-methods-notes/` | Which regularity and event-map statements for RFDEs are independently reusable? | Working notes |
| `jns/`, `flagship/` | Earlier combined manuscripts | Historical material only |

Paper A uses standard RFDE, invariant-manifold, Fredholm, and fast--slow
terminology. Its unconditional results are the first-delay-moment range
theorem, the uniform Fredholm factorization, and the local fold coefficient.
The heteroclinic application is stated under explicit global
invariant-manifold and comparison hypotheses. It makes no claim about an
experimental threshold or a maximal canard for the unmodified law.

The pre-rewrite state is frozen at `paper-a-pre-rewrite-2026-09-02`. Current
Paper A sources are under `network-root-transfer/rewrite-sections/` and
`network-root-transfer/rewrite-supplement/`.

Build all active paper workspaces with:

```sh
make split
```

Build and test Paper A alone with:

```sh
make -C network-root-transfer paper
make -C network-root-transfer check
```
