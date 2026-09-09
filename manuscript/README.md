# Manuscript workspaces

The repository separates papers by mathematical question. Shared source
history is retained in one repository; the papers are not maintained as
permanently divergent Git branches.

| Workspace | Question | Status |
| --- | --- | --- |
| `network-root-transfer/` | How do constrained delayed-coupling perturbations change local fold matching on compatible RFDE histories, uniformly in network size? | Local major revision; single PDF |
| `pulse-threshold/` | Can a physical pulse threshold in a delayed FitzHugh--Nagumo model be proved through a stable-manifold crossing and two-sided routing? | Incomplete research draft |
| `rfde-methods-notes/` | Which regularity and event-map statements for RFDEs are independently reusable? | Working notes |
| `jns/`, `flagship/` | Earlier combined manuscripts | Historical material only |

Paper A is titled **Local fold matching in RFDE networks with constrained
delayed coupling**. Its first main theorem constructs compatible histories
and a finite-interval matching function, proves uniqueness of its nearby
zero, and estimates the matrix derivative of the selected parameter
`mu_N^fin = delta^2 nu_N^fin` uniformly in network size. The first-moment
range and Fredholm formulas support that local result. The heteroclinic
application in Section 5 requires separate invariant-manifold and comparison
hypotheses; it is not a theorem about a maximal canard for the unmodified
recovery equation or an experimental threshold.

The tags `paper-a-pre-rewrite-2026-09-02` and `paper-a-dcds-submission-v1`
archive earlier versions. The current revision is not a tagged release. Its
sources under `network-root-transfer/rewrite-sections/` and
`network-root-transfer/appendices/01-fold-details.tex` build into one PDF with
Appendix A and one numerical figure. The former connection Appendix B and
connection-geometry figure are not included in the normal build.

Build all active paper workspaces with:

```sh
make split
```

Build and test Paper A alone with:

```sh
make -C network-root-transfer paper
make -C network-root-transfer check
```
