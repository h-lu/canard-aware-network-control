# RFDE selected-return method notes

This directory is a self-contained, compiling working-note extraction of two
results from the flagship research draft:

1. the eventually smooth selected-event return theorem; and
2. the direct selected-return stable-set germ lemma.

It is deliberately **not a submission manuscript**.  In particular, it does
not claim that either theorem, its proof mechanism, or their combination is
new relative to the full RFDE literature.

## Source fidelity

The source statements and proofs were migrated from
`manuscript/flagship/sections/02-model-and-results.tex` at repository commit
`d84d43678b98b11eb60d9b39ea1ad06babfd5939`.  The hypotheses, quantifier
order, event-window inequality, endpoint signs, positive-speed condition,
local-domain restrictions, and conclusions have been retained.  The new
setting section only makes the history space, selected event, local stable
sets, and germ convention explicit.

Model-specific canard, network, Floquet, pulse, Hessian, and routing material
has not been imported.

## Provisional contribution map

This is a map of the possible mathematical unit, not a novelty claim.

```text
fixed-time RFDE smooth dependence does not by itself justify differentiating
a moving complete-history event while translated initial history remains
visible
    -> wait beyond k maximum delays and use the triangular mixed-jet hierarchy
    -> obtain joint C^k time/history regularity
    -> strict event signs and speed give a C^k selected hit by the implicit
       function theorem

a selected near-multiple-period hit need not be a first return or a literal
iterate of one
    -> bounded positive return times and one retained flow tube compare all
       intervening arcs with the periodic orbit
    -> recurrent hits plus phase isolation identify the same stable-set germ
```

The candidate reusable message is therefore conditional: selected-event
regularization and stable-germ identification can be separated from a
first-return label.  Whether that separation is already standard or deserves
an independent publication has not yet been established.

## Proof spine

### Eventually smooth selected return

1. The Volterra equation yields the fixed-time triangular variational
   hierarchy through order `k` on the common solution tube.
2. A method-of-steps induction regularizes mixed time/history jets after each
   additional maximum delay.
3. At times greater than `k tau_*`, all jets define continuous
   history-valued derivatives, hence the time/history solution map is jointly
   `C^k`.
4. The event functional is jointly `C^k`; endpoint signs and positive speed
   give one zero in the declared window.
5. The Banach implicit-function theorem gives the event time, composition
   gives the complete-history hit, and a section chart gives the selected
   return map.

### Direct return and the stable-set germ

1. If selected iterates converge to the section base point, the positive
   lower return-time bound sends accumulated time to infinity.
2. Continuity on the bounded intervening time interval sends every late arc
   to the corresponding periodic-orbit arc, hence gives flow convergence.
3. Conversely, flow convergence and recurrent selected hits imply that the
   selected iterates approach the periodic orbit.
4. Phase isolation on the local section converts approach to the orbit into
   convergence to its distinguished section point.

## Decision gates

The notes remain non-submission material until every gate below is closed.

- **Literature gate — open.** Locate and compare the sharpest fixed-delay
  RFDE results on joint time/history regularity, eventual smoothing,
  event-defined Poincare maps, and stable manifolds of periodic orbits.  Record
  exact theorem numbers and decide whether the two results are direct
  corollaries, adaptations, or genuinely distinct statements.
- **Proof-expansion gate — open.** Either expand the mixed Frechet-derivative
  induction in operator norm through order `k`, including the common-domain
  argument, or cite a theorem whose hypotheses match exactly.
- **Stable-germ gate — open.** Compare the direct-return lemma with standard
  local-section and suspension arguments and decide whether it is a theorem,
  a useful explicit lemma, or established folklore.
- **Scope gate — open.** Determine whether `k tau_*` is merely convenient or
  close to a genuine obstruction.  No necessity or sharpness claim may be
  made without a separate argument.
- **Publication-unit gate — open.** Proceed only if the literature audit finds
  an independent mathematical contribution large enough for a methods note.
  Otherwise retain these results as supporting tools in another paper.
- **Release gate — open.** Before any circulation, perform an independent
  proof audit, add precise primary citations, choose a venue, and create a
  frozen source/PDF release.

## Build

From this directory run:

```sh
make
```

The PDF is written to `build/main.pdf`.  The build uses only the local TeX
sources and two manually listed background references; no external
bibliography file is required.

## Directory map

- `main.tex` — title, conservative abstract, status notice, and section order;
- `preamble.tex` — minimal notation and theorem setup;
- `sections/01-introduction.tex` — question, role, and non-novelty boundary;
- `sections/02-setting.tex` — RFDE, selected-event, stable-set, and germ
  definitions;
- `sections/03-eventual-selected-return.tex` — migrated theorem and proof;
- `sections/04-stable-set-germ.tex` — migrated lemma and proof;
- `sections/05-scope-and-literature-gate.tex` — exclusions, audit questions,
  and background references.
