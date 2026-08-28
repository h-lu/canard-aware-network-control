# Canard-aware network dynamics and control

Research repository containing the original JNS manuscript and its focused
successors.  The active Paper A target is:

> **Two-Delay Blind Controllability and Selected Fold-Response Readout in
> Retarded Markov Networks**

The original complete LaTeX manuscript, figures, appendices, cover letter,
and submission checklist are in [manuscript/jns](manuscript/jns).  The former
integrated successor draft is retained in
[manuscript/flagship](manuscript/flagship) as a research ledger, not as a
submission manuscript.  Its active descendants are split by proof spine:

- [network-root-transfer](manuscript/network-root-transfer), the first
  publication target, now built as a focused main article plus supplementary
  proof document;
- [pulse-threshold](manuscript/pulse-threshold), the still-open model-specific
  stable-sheet program;
- [rfde-methods-notes](manuscript/rfde-methods-notes), whose independent
  novelty remains to be established.

The workspace, branch, and eventual public-release policy is recorded in
[manuscript/README.md](manuscript/README.md).  The supporting integrated
research design remains in
[docs/flagship-research-design.md](docs/flagship-research-design.md).

> **Floquet representation notice (2026-08-25).**  A delayed coefficient
> evaluated along the delayed orbit has two equivalent Fourier forms:
> unshifted coefficient plus output/row phase, or shifted coefficient plus
> input/column phase.  The earlier blanket statement that every row phase is
> wrong has been retracted.  The legacy FHN 319-cell and 32,046-leaf sources
> use the first, physically correct form.  Their frozen manifests still
> validate, and a separate four-test operator oracle now proves equivalence,
> binds the source semantics and rejects both mixed representations; their
> original claims are therefore retained.  A transient new leaky calculation did
> mix unshifted coefficients with column phases and was stopped before any
> global artifact was issued; the repaired leaky trees use unshifted+row as
> the main representation and verify shifted+column independently.  This
> audit does not affect
> the base two-module complete-history canard theorem, the leaky periodic
> orbit radii theorems, the abstract leaky Riesz tail reduction, the quiet
> Razumikhin/capture certificates, or the Dobrushin transverse complete-line
> inverse.  The exact identity and acceptance protocol are recorded in the
> [Floquet representation audit](docs/floquet-input-mode-phase-integrity-audit.md).

> **Flagship-successor checkpoint (2026-08-26).**  The leaky-recovery program
> now proves dimension- and topology-uniform transverse decay and a
> complete-line Green bound for every finite admitted nonnegative Dobrushin
> network with a row-stochastic current layer and fixed half-row-mass delayed
> layers.  Common delay-layer left balance is no longer required: the
> complete-history Lin operator is upper triangular and has a uniformly
> bounded invertible codomain row reduction to the scalar/transverse direct
> sum.  On the
> scalar physical-pulse side, the exact quiet history under
> (J=0.32) is enclosed at its third positive event within
> (2.637078616900037\times10^{-5}) of the exact outer-orbit phase-zero
> complete history; this is an [ambient history-ball theorem](docs/leaky-pulse-outer-third-return-enclosure.md),
> not yet basin capture.  A [direct phase-fixed return contract](docs/leaky-outer-phase-fixed-return-stage1.md)
> records the signed matrix-measure route from that ambient ball to a strict
> (C^0\)-history contraction.  Its
> [Stage-2 signed-kernel audit](docs/leaky-outer-signed-kernel-stage2.md)
> proves, for the exact stored 360-step shadow, a phase-corrected norm below
> (0.126908) and cancellation factor above (40.73), while explicitly leaving
> the global continuous-density transfer errors and every attraction flag
> open.  A [Stage-3 continuous-kernel shard](docs/leaky-outer-continuous-kernel-stage3-shard.md)
> now validates the first directed Volterra injection cell for both delays;
> it is a composable base cell, not the missing global operator bound.
> [Stage 3C](docs/leaky-outer-delay-word-stage3c-compression.md) uses exact
> delay support to compress the global kernel to 21 signed words of depth at
> most two.  [Stage 3D](docs/leaky-outer-delay-word-stage3d-primitives.md)
> removes every ordered two-simplex in favor of eight one-dimensional
> \(F,G,H,L\) primitives.  [Stage 3E](docs/leaky-outer-delay-word-stage3e-relative-residual.md)
> then proves global exact-orbit multiplicative errors below \(0.0051\) for
> \(F,G\) on 1024 degree-24 cells.  Separate triangular propagation through
> \(H,L\) is rigorously too coarse.  [Stage 3F](docs/leaky-outer-signed-row-stage3f-adjoint.md)
> therefore combines all delay words, both injections and phase subtraction
> in one advanced row before total variation; it proves the instantaneous
> Green/boundary and coefficient/phase-ratio budgets.  The corrected
> [Stage 3G v2](docs/leaky-outer-resolvent-stage3g-tensor.md) now covers all
> \(730+40\) rectangles and \(12{,}320\) patches, including both nonempty
> terminal-clipped cells in every \(\delta\)-strip, and proves the directed
> tensor residual and Green/boundary bootstrap.  The dependent
> [Stage 3H v2](docs/leaky-outer-combined-row-stage3h-size.md) proves strict
> center-guide phase-combined row sizes, with full-row bounds
> \(41.482447\) in voltage and \(1.177738\) in recovery.  The retracted v1
> values remain inadmissible.  Stage 3I now covers all \(25{,}600\)
> event-aware continuous signed-density rectangles and proves exact
> phase-fixed reduced-history return-row bounds \(0.550516\) and
> \(0.028281\).  Thus arbitrary reduced \(C^0\) linear contraction is
> proved even though the auxiliary \(0.01\) closeness target fails;
> [Stage 6A](docs/leaky-outer-nonlinear-tube-stage6a.md) now upgrades this
> linear parent to a source-bound, nonzero nonlinear outer local return and
> attracting tube.  On the exact phase-zero section its radius is
> \(r_6=10^{-335}\), the compatible full complete-history tube has radius
> \(R_6=10^{-3}\), and the nonlinear return constant satisfies
> \(\Lambda_6\le0.561839\).  Its \(C^2\) local event chart and no-earlier-local-hit gate
> are also proved.  This microscopic tube is not biological capture: the
> \(J=0.32\) history first fails ambient-to-section domain containment, and
> reaching its \(2.637079\times10^{-5}\) ambient-proximity scale requires
> \(C_P<17044.784546<17044.785\).  Entry, outer-side attachment, capture,
> routing, and onset remain open.  For
> the inner separator, the old scalar
> (C_N=10) majorant has been rejected and replaced by a six-block
> [projected-Hessian contract](docs/leaky-projected-return-hessian-stage4-contract.md);
> its [three-mesh pilot](docs/leaky-projected-return-hessian-stage4a-pilot.md)
> closes the structured (2\times2) majorant with large diagnostic margins,
> while all continuous-history and directed-block theorem flags remain false.
> [Stage 4C](docs/leaky-route-c-adjoint-stage4c.md) proves the qualitative
> RFDE adjoint/correlated-deflation mechanism and a nonzero tail-aware Fourier
> left row.  [Stage 4D](docs/leaky-route-c-adjoint-stage4d.md) now proves the
> Fourier reversal, summable adjoint tail, border normalization, and the
> continuous Route-C history measure.  [Stage 4E](docs/leaky-shared-yqq-deflation-stage4e.md)
> now propagates the physical-time \(V_{qq}\) tube, evaluates the same
> atom-plus-density row on the directly deflated history, and proves the
> base-orbit block \(C^{uu}_{s,\mathrm{base}}\le7.905650<12\).  This is not
> uniform on the split ball; its inflation, the other five blocks, the
> nonlinear split-return tube, quantitative stable graph and separator remain
> open.  [Stage 4G](docs/leaky-uniform-uu-inflation-stage4g.md) computes the
> exact required Lipschitz cap \(2408.441719\) and rigorously rejects the
> cancellation-blind scalar inflation route at physical cell 581.  It
> reduces the replacement to the four signed words
> \(\varnothing,(\tau_0),(\tau_1),(\tau_0,\tau_0)\); it does not validate the
> uniform block.  [Stage 4H](docs/leaky-inner-signed-stable-flow-stage4h.md)
> constructs that signed row before total variation and records the sampled
> cancellation \(0.00413443\) versus the separate triangle \(5.63547\),
> without promoting the sample.  [Stage 4I](docs/leaky-inner-word-primitive-stage4i.md)
> then validates all five local primitive residuals on \(1042\) cells and
> proves that unprojected physical-frame error propagation excites the
> unstable mode.  Its mixed-norm primitive ingress is only
> \(1.46355\times10^{-3}\).  [Stage 4L](docs/leaky-inner-terminal-stable-row-stage4l.md)
> now forms the fixed-start common event-corrected and stable-deflated row
> before every modulus, covers the complete true returned history, and proves
> \(\|AP_s\|\le0.009896427481610001<0.1\).  Exact intertwining therefore gives
> \(\|A_s^n\|\le0.1^n\) with \(K_s=1\).  This is the selected phase-fixed
> discrete linear map only, not a first return or nonlinear tube.  The full
> intermediate \((s,t)\) projected-residual mechanism in
> [Stage 4J](docs/leaky-inner-projected-stable-flow-stage4j-contract.md)
> remains an optional route to stronger intermediate-flow control, not a gate
> for discrete stable power.  The source-bound
> [Stage 4N feasibility pilot](docs/leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility.md)
> shows why the nonlinear tube still needs signed event-aligned cancellation:
> two disclosed scalar Gronwall routes miss containment by directed lower
> values \(11.971029\ldots\) and \(32.257662\ldots\) decimal orders.  It
> records only the sufficient future target
> \(K_{\rm ret}<188.9122238810816\) (numerically \(188.9122238811\)); every
> nonlinear-return, Hessian, graph, crossing, onset, routing and safety flag
> remains false.  Its nonclosing result SHA-256 is
> 5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de;
> it is not listed as a positive theorem release below.
> [Stage 4O](docs/leaky-inner-event-aligned-return-hessian-stage4o-contract.md)
> now freezes the exact moving-event Hessian, including both event-time
> derivatives, complete-history translation, and exactly one phase
> projection before the fixed stable/unstable split.  It exposes a genuine
> regularity gate: the present one-period argument does not establish a
> \(C^2\) moving complete-history return on an arbitrary continuous-history
> ball; it does not prove that the particular map is non-\(C^2\).  The general
> [Stage 4R theorem](docs/finite-delay-eventually-smooth-selected-return-stage4r.md)
> proves that, for any finite-dimensional fixed-delay \(C^k\) RFDE, a common
> selected event window beginning after \(k\tau_{\max}\), together with the
> stated initial-chart regularity, common solution/event tube, strict endpoint
> signs, positive event speed, and terminal-chart containment, gives a
> \(C^k\) complete-history section return.  No no-earlier-hit premise is
> needed for selected-branch smoothness.  A direct bounded-positive-time
> selected return identifies the intrinsic periodic-orbit stable-set germ
> only under the stated invariant phase-isolating section, common intervening
> tube, retained-domain, and recurrent-hit hypotheses; one need not first
> prove \(Q=P^m\).
> The near-two-period center clears the \(C^2\) threshold by
> \(14.010740123253945\).  The
> [explicit Stage 4U tube](docs/leaky-inner-explicit-lambda-event-tube-stage4u.md)
> proves a common \(C^2\) selected hit for arbitrary continuous histories on
> the microscopic scale \(\lambda_0=9\times10^{-31}\), and the
> [orbit-aware Stage 4V tube](docs/leaky-inner-logarithmic-event-tube-stage4v.md)
> strengthens this to the closed scale \(1.2\times10^{-8}\), with open scale
> \(1.25\times10^{-8}\) and a rigorously audited construction ceiling above
> \(1.2770076307683837\times10^{-8}\).  The improvement comes from an exact
> weighted-energy cancellation and a \(1042\)-cell directed orbit integral;
> it is still not a preferred-scale self-map or graph theorem.  The
> [direct Stage 4T bridge](docs/direct_two_period_derivative_stage4t.md)
> proves \(DQ_Y(Y_*)=A^2\) without a nonlinear identity \(Q=P^2\).  The
> fixed two-step splitting and rates are also proved.
> [Stage 4W](docs/leaky-inner-split-bimeasure-residual-stage4w.md) proves the
> exact stable-row quotient norm, the split-projective signed-bimeasure
> residual implication, and a qualitative local \(C^2\) stable graph for the
> selected map.  Numerical continuous-history Hessian ingress remains
> \(0/6\), so no effective graph radius, pulse crossing, or onset is promoted.
> [Stage 4P](docs/leaky-inner-graph-closure-arithmetic-stage4p.md)
> proves that a future six-block box \((1,10,1000,5,10,1000)\) closes the
> split graph arithmetic with Perron bound below \(0.193086\); after the
> physical normalization it would give graph height below \(0.001623187\),
> endpoint margins above \(0.0180540\) and \(0.0131604\), and
> \(H'\subset[-260.794147,-243.205853]\).
> [Stage 4Q](docs/leaky-inner-signed-second-variation-stage4q-pilot.md)
> preserves the signed event and translation correlations through two
> periods; its \(n_{\rm step}=240\) main row is approximately
> \((7.46\!\times10^{-7},0.00447,29.354,0.595,0.574,158.532)\), and its
> six-block heuristic envelope lies well inside the wide box.  This is a
> tested finite-section pilot, not interval evidence.  The active inner proof
> chain is now enlargement of the microscopic return to the preferred graph
> ball, graph-transform return-domain containment, the six directed
> continuous-history Hessian blocks, and either the direct-return stable-set
> bridge or \(Q=P^2\) on nested domains.
> Once that chain closes, the unique selected-crossing arithmetic is already
> available.
> The [wide Route-C family audit](docs/leaky-pulse-inner-route-c-family-contract.md)
> additionally proves that zero-centered state/variation sharding cannot
> certify the pulse crossing; the active replacement preserves parameter
> correlations with an event-aligned fourth-order jet.  Its
> [center pilot](docs/leaky-pulse-parameter-jet-center-pilot.md) shows a
> rapidly decreasing full-width scaled hierarchy.  The subsequent
> [Stage-5B directed enclosure](docs/leaky-pulse-parameter-jet-directed-enclosure.md)
> rigorously closes all \(1152\) time cells on
> \(J\in[0.30105,0.30120]\), with joint coefficient error below
> \(8.58\times10^{-19}\) and full-width fifth-order remainder below
> \(1.73\times10^{-8}\).  This proves the fixed-common-time wide family.
> [Stage 5C](docs/leaky-pulse-route-c-event-stage5c.md) now also proves, on
> the same full interval, exactly one positive Route-C event in the common
> bracket \([555\sqrt5/24,1+546\sqrt5/24]\), speed at least
> \(0.2133519018\), a fourth-order event-time graph with remainder
> \(10^{-4}\), and a continuous common-event \(Y\)-history tube of radius at
> most \(0.008199932\).  [Stage 5D](docs/leaky-pulse-event-aligned-derivative-stage5d.md)
> directly encloses the first variational equation on all \(1152\) cells,
> proves \(T_J\in[336.624302835,456.574093812]\), retains the full
> event-translation term, and gives a continuous complete-history derivative
> with \(\|D_JK\|_Y\le142.200203\), \(D_JK_v(0)=0\), and
> \(D_JK_w(0)\in[-17.350656459,-10.142798861]\).  Its fixed-functional
> total-variation consequence alone is only \(|f(D_JK)|\le1017.273043\).
> [Stage 5E](docs/leaky-pulse-oriented-adjoint-action-stage5e.md) instead fixes
> the physical real right gauge and propagates the correlated same-row error
> through 128 parameter shards and 512 history cells at 192-bit precision.  It
> proves, uniformly on \(J\in[0.30105,0.30120]\),
> \[
> f_{\rm phys}(D_JK(J))\in
> [-258.746521015805,-245.253478984195]\subset(-\infty,0).
> \]
> This is a signed transversality ingredient for the fixed Route-C event
> functional.  It deliberately proves neither that the event is the third
> post-release crossing nor a stable-sheet crossing, onset, or routing.
> [Stage 5F](docs/leaky-pulse-stable-gap-slope-bridge-stage5f.md) now closes
> the next rank-one bridge in the identical continuous-history max norm
> \(Y\), Route-C section \(\Sigma\), and physically oriented Grushin pair
> \(f_{\rm phys}(q_{\rm phys})=1\).  For the centered coordinate
> \(\kappa(J)=K(J)-X_*\) it proves
> \(\|P_sD_J\kappa\|_Y\le14.727579\), where
> \(P_s=I-q_{\rm phys}f_{\rm phys}\).  If a future quantitative graph is
> constructed in this exact chart, its chart and domain contain the full
> pulse interval, and \(\sup\|D\psi\|\le16\) in the registered operator norm,
> then the centered stable gap satisfies
> \(H'(J)\in[-494.387771,-9.612229]\subset(-\infty,0)\).  Stage 5F proves
> this implication, not its graph/chart/domain antecedents.  These frozen
> Stage-5F values are retained as audit history but are sharpened by
> [Stage 5G-a](docs/leaky-pulse-endpoint-functional-stage5ga.md) and
> [Stage 5G-b](docs/leaky-pulse-stable-coordinate-cone-stage5gb.md).
> Stage 5G-a proves strict opposite signs of the complete-history endpoint
> functional coordinates,
> \[
> f_{\rm phys}(\kappa(J_-))\in[0.019677187,0.023055896],\qquad
> f_{\rm phys}(\kappa(J_+))\in[-0.018164491,-0.014783669],
> \]
> and bounds the endpoint stable coordinates by \(0.008935972\) and
> \(0.008927665\).  Stage 5G-b uses the direct physical-column norm and exact
> projection identity to prove
> \(\|P_sD_J\kappa\|_Y\le5.979324\) and
> \(P_s\kappa(I_J)\subset\overline B_Y(0,47/5000)\cap\ker f_{\rm phys}\).
> Hence a future graph whose stable domain contains that ball and has
> \(\sup\|D\psi\|\le16\) would satisfy
> \(H'(J)\in[-354.415700,-149.584300]\subset(-\infty,0)\).  The endpoint
> functional signs, stable-coordinate cone, and conditional slope arithmetic
> are proved.  The quantitative graph and its derivative/endpoint-height
> bounds, graph-adjusted stable-gap signs, selected crossing, event ordinal,
> physical onset, routing, capture, and asynchronous network safety remain
> open.  Interval Newton is only an optional sharpening after graph-adjusted
> stable-gap endpoint signs and strict monotonicity prove a root.
>
> Frozen validation ledger: the upper-triangular v2 raw result/canonical
> certificate SHA-256 pair is
> 35daf49284a6e7a47da4f5a69df82061d2d44536f7270978e3e8fefffeb47e8b /
> c4b72e1179a80fddd0d34d1e1d650402966350e3d0315d144d4c586df371c322;
> the Stage-3G-v2 pair is
> 52d2c4df0cea7b6d98d898669e45ef54bfed1799965b2cff92161e84bd78ce13 /
> efad1bceffcf44790a2c753d140b3f183faeb1a004b453dcd4de5f7c7b44489b;
> the Stage-3H-v2 pair is
> c0c5b854236f8403dacbb0037c5c409ad5f980364571bdf60fa9981a2e287408 /
> 07ff0895fbe439939afd851cf136d6c9677ecb9dbb3e2acb80e5d8598c14a132;
> the Stage-3I-v2 pair is
> 5fdb1a843070ceb5887f7384431f2414989afc3cb741abc7f19ed44a333d4970 /
> fa82997b4b685ec2791be4d1efa82a0b6e5ba3b358d3d18bfcdd295c55bc7a24;
> the Stage-4L pair is
> 672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e /
> b27631b62d437bf12431d751d4dad79570a03fa9a66fc0115d90f49768e058fc;
> the Stage-5F pair is
> 26acd6d9421a8bf60d5bb96fe4c68918b39f89a443973dd728fed17ccf48652b /
> e38f001e372372ef6186f16339d72c32302ad868441ef7eafbd0f533eb7c793b;
> the Stage-5G-a pair is
> 56e847fc804ced75e6c2fbf09ccbec1bdeabf505638e093c0939c2f2e584dd8c /
> 4bd0671fa9abb155f8ddd75eb7a4d26ce4ebbc783c073420784bdf54a1dbbcfa;
> the Stage-5G-b pair is
> a16e9159d462c6b8f58851c2181147940f27e1a404ee4c2fbeb8999440cf8b64 /
> 9fd06db88ce1743a27d27bef86e2d16891c92c39f8adf7e60ae3d4d00f7ef813;
> and the Stage-6A pair is
> f199cdc2cba603ef9c4a0cb7e5e5383a85f749b05dfa1f99d83245580697caac /
> a4afa5902d95fcbfa50477bae7c30b6998097fd823eab2ea3eee9c26cad0f144.
> The delayed-network six-file chain passed \(28+41=69\) tests, including
> live-parent warm-cache mutation attacks; Stage 3H v2 passed \(18/18\),
> including its fresh Stage-3G parent replay; Stage 3I passed \(18/18\),
> including its public cache-cleared fresh numerical replay; Stage 4L passed
> \(31/31\), including a genuine fresh recomputation and hostile tests for
> inward note rounding, recovery-inclusive rectangle arithmetic, circular
> use of \(K_s\), and theorem-scope promotion; Stage 5F passed \(20/20\) plus
> an independent cold validator; Stage 5G-a passed its full
> \(26/26\) suite including a fresh recomputation; and Stage 5G-b passed
> \(22/22\) plus a separate fresh-interpreter replay.  Stage 6A passed
> \(14/14\), including a fresh directed recomputation and hostile tests that
> reject capture promotion and a double-factorial Taylor remainder.

The current successor proof gates are tracked separately so that a numerical
pilot cannot close a theorem-level task:

- [#24: enlarge the proved microscopic outer return tube to \(J=0.32\) entry and capture](https://github.com/h-lu/canard-aware-network-control/issues/24);
- [#26: inner six-block return Hessian and quantitative separator](https://github.com/h-lu/canard-aware-network-control/issues/26);
- [#25: directed pulse-history family and unique stable-sheet crossing](https://github.com/h-lu/canard-aware-network-control/issues/25);
- [#27: explicit asynchronous Dobrushin threshold and safety transfer](https://github.com/h-lu/canard-aware-network-control/issues/27);
- [#28: JNS flagship theorem assembly and release](https://github.com/h-lu/canard-aware-network-control/issues/28).

Build and verify from the repository root with

```sh
python3 -m pip install -e '.[paper,test]'
make -C manuscript/jns paper
python3 -m pytest -q
```

## Central question

Can two weakly delayed FitzHugh--Nagumo modules have the same total delayed
gain and the same delay measure seen by the critical projection, yet have
different canonical local history-connection roots because the delay forcing
passes through a stable transverse mode?

The first paper has one mathematical spine:

1. freeze one two-module, two-delay RFDE and prove its exact singular spectrum;
2. construct its two-dimensional invariant history graph, including the
   logarithmically growing tube needed for long physical delays;
3. construct phase-normal one-sided traces and prove that their simple gap
   root is equality of the two retained complete RFDE histories.

The broader finite-network transfer and frequency--amplitude--safety control
programs remain separate successors in the repository. They are not
assumptions, promotions, or parallel novelty claims of the base paper.

## Base-paper scope

- exactly two voltage--recovery modules and two fixed scaled delay atoms;
- source-history feedback of size \(O(\varepsilon)\), with physical delays
  \(\tau_k=\theta_k/\sqrt\varepsilon\);
- one fixed, non-actuated transverse recovery coupling that removes the extra
  recovery center while vanishing on the critical recovery line;
- the canonical prepared-tail selection, matching section, and phase
  convention of the local theorem;
- an exact intersection of two retained local RFDE histories, not an
  assertion about every physical outer Fenichel family and not a global spike
  detector;
- delayed van der Pol only as the published scalar calibration.

General finite \(N\), moving delay support, arbitrary node heterogeneity,
three-coordinate control, graphon limits, strong delays, and global pulse
events are frozen or later work, not claims of the base paper.

## Proved canonical theorem

For the fixed two-delay redistribution parameter \(\eta\), the component
proofs assemble the canonical local root law

\[
 \mu_{c,\mathcal P}(\delta,\eta)-\mu_{c,\mathcal P}(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\,\delta^3\eta
 +O(\delta^4|\eta|+\delta^3\eta^2),
 \qquad \delta=\sqrt\varepsilon,
 \qquad \alpha=\frac{\sqrt6}{4}.
\]

even though the total delayed gain and critical projected delay measure are
independent of \(\eta\). The root is defined by the canonical prepared-tail
and phase convention, and zero gap is proved to be equality of the retained
complete histories under the injective history embedding. The growing-tube
graph, one-sided Green/phase trace proof, weighted contraction seam, and
independent falsification audit are complete. The exact finite-\(\delta\)
root is indexed by the fixed admissible preparation datum \(\mathcal P\),
while its displayed expansion is uniform over the declared bounded
preparation class.

This is not an unconditional theorem for an arbitrarily selected physical
outer Fenichel maximal canard. Backward completeness alone does not select
one. Such a physical selection inherits the same coefficient only under the
separate, parameter-coherent compatible-selection and full-history
boundary-jet hypotheses in
[docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md)
and
[docs/paper-iii-outer-selection-blocker-and-repair.md](docs/paper-iii-outer-selection-blocker-and-repair.md).

The precise claim hierarchy and falsification gates are in
[docs/flagship-research-design.md](docs/flagship-research-design.md). The
general-network specifications in
[docs/scope-and-theorems.md](docs/scope-and-theorems.md) are frozen
future-work contracts, not proved inputs or active promotions of this theorem.

## Current proof status

The canonical route is proved; the physical outer-selection route remains
open.

1. **Exact model and spectrum.** The final two-module equation, anisotropic
   blow-up, delay-layer identities, fold data, and singular Jordan structure
   are exact. A separate Rouché--Schur argument proves that the scaled RFDE
   has exactly two simple relevant characteristic roots, near \(\pm i\), and a
   uniform complementary characteristic-root gap.
2. **Compact-tube history reduction.** A constructive contraction proves a
   unique bounded Lipschitz special-flow history graph and an injective
   complete-history map on a fixed compact fold tube. This avoids treating
   backward RFDE evolution as an initial-value problem. A triangular scale of
   common Banach fibers now proves the required
   \(C_u^3C_\delta^3C_\nu^1C_\eta^2\) rectangular mixed regularity and an
   \(O(\delta^3)\) fixed-tube graph remainder.
3. **Actual local graph jet.** The proved
   mixed regularity promotes the invariance recursion to a Taylor coefficient
   of the compact-tube graph, while exact symbolic division independently gives
   \[
   \partial_\eta q_{2,X}(\gamma_0(s))
   =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
   \]
4. **Canonical long-delay Gate D (passed).** A frozen
   target-dependent cutoff gives the required mixed jets and remainder on the
   logarithmically growing flow hull. Explicit one-sided Green operators remove
   the normally growing mode, fix the tangent phase, and construct the
   canonical attracting/repelling traces. The normalized gap calculation and
   injective history lift then give the exact coefficient and remainder above.
   The assembled theorem and verification record are in
   [docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md).
5. **Physical outer-selection Gate D (repaired target open).** The original
   rule is now disproved as sufficient: bounded backward completeness does
   not select the repelling unstable coordinate, and exponential closeness
   does not control rectangular \(C_\nu^1C_\eta^2\) history jets. Transfer
   requires the open compatible-selection Gate P3-A\(^*\), with declared
   curve-wise Lyapunov--Perron boundary coordinates and exact common-graph
   normalization. The unforced causal alternative has an exact
   one-maximal-delay released history and a proved nonempty pulse/quiet
   transition set. Its unforced separator is still open, but the old local
   shortcut is now known to be insufficient: even an exact saddle separator
   need not classify all offsets by fixed-layer first hits when recovery
   drifts. A separate sharp audit proves that the fixed-\(p\) logarithmic
   fold estimate is action-subcritical for every fixed outer action and that
   a value-residual terminal match does not by itself control parameter
   jets. The repaired route splits into an outer U-OUT\({}^+\)
   tracker/relative-growth-history-graph gate U-SF, a repaired
   moving-tube/lower-fold event gate U-EX, and the separate
   U-CAP biological capture/no-return gate. An exact Airy model shows that the
   lower-fold event root can be exponentially displaced from the geometric
   root; the physical comparison requires the stated fold-map factorization,
   and neither root is identified with the canard root without an additional
   theorem. The U-CAP audit further proves that the old fixed-reset-layer
   blocks cannot classify all late exits: an exact two-channel ODE subclass
   has a punctured no-hit set. The shortest unforced positive result is a
   moving-detector deadband certificate; exact capture still requires a
   global complete-history invariant-set exclusion. A
   modified protocol that clamps only the collective recovery coordinate now
   has, for every sufficiently small fixed positive \(\delta\), a proved
   codimension-one complete-history pulse/quiet separator. This is an
   operational controlled threshold, not the unforced canard root.
6. **General-network successor theorem.** For arbitrary finite Markov
   networks with a common Dobrushin gap, one shared recovery resource, and
   heterogeneous fold curvature, a dimension-uniform history graph and
   canonical selected root are proved without a nontrivial synchrony
   quotient. Projection-neutral delay redistribution has the explicit
   resolvent coefficient
   \[
   -\frac{K}{2\alpha^2}\,
   \pi_N^T\operatorname{diag}(c_N)A_N^{-1}
   P_{\perp,N}\dot M_{1,N}\mathbf1,
   \]
   and an all-\(N\) family realizes a common nonzero value. The exact root
   remains preparation-indexed; physical outer selection is not inferred. A
   bounded controller in the same shared-resource RFDE can deliberately use
   those exact roots as offline reset data and transduce the response into a
   nonzero detector-latency response. A policy-offset falsifier shows that
   this exact composition is not an input-independent physical onset law.
7. **Pulse-control successor theorems.** A size-uniform Halanay estimate
   separates transverse synchronization from output conditioning. Under the
   declared physical-root and one-coordinate canard-layer hypotheses, the
   original frequency--amplitude--safety response has an exponentially bad
   right-inverse lower bound. A reset-only operational actuator instead gives
   an exact block-triangular response and a quantitative inverse whenever the
   two-by-two frequency--amplitude block is certified. A parameter-dependent
   complete-history gap calibration further turns that response into the
   exact block diagonal \(\operatorname{diag}(B,-1)\); this is a calibrated
   protocol coordinate, not a naturally decoupled raw actuator, and its raw
   command Jacobian must be bounded separately. The corresponding FHN
   periodic package first supplied a reproducible Fourier-collocation orbit,
   derivative matrix, unique-extrema diagnostics, and a positive nine-sample
   floating response-box candidate. A separate MPFR-directed calculation
   proves the exact 97-node phase-fixed collocation root and finite bordered
   inverse and encloses the complete residual of its trigonometric polynomial.
   It also exposes aliased modes. A de-aliased finite/tail radii argument now
   validates the center RFDE orbit and its phase-bordered inverse. The
   Fredholm--monodromy transfer then proves that the autonomous unit
   multiplier is algebraically simple and gives a directed exclusion on a
   punctured arc about it. A new uniform finite/tail calculation now proves
   a \(C^1\) periodic branch, one maximum and one minimum, and
   \(\inf\sigma_{\min}D_b(F,R_h)\ge0.0162187\) on the declared microscopic
   two-gain box. A legacy full-complex calculation reported 319 Bloch cells,
   and a later right-half calculation reported 32,046 dyadic leaves.  Both
   sources use the physically correct unshifted-coefficient/output-phase
   representation.  Their frozen source manifests and focused validators
   pass, while an independent operator-level oracle verifies the equivalent
   shifted-coefficient/input-phase form and rejects both mixed forms.  Thus
   the hyperbolicity and right-half-index conclusions retain their original
   proved status; the earlier claim that the row phase itself was erroneous
   is retracted.  The simple translation multiplier remains proved. Independently,
   the fixed-matrix enclosure of the two-output derivative
   family now yields, without second sensitivities, a directed
   frequency--squared-range target ball of radius at least
   \(1.6218727378\times10^{-14}\) about the exact center response. An exact
   orbit-amplitude enclosure and inverse-coordinate argument transfer this
   to a three-dimensional frequency--unsquared-amplitude--operational-safety
   ball of radius \(2.7513816601\times10^{-15}\). For every finite
   nonnegative balanced two-half-delay topology, exact-model bounded additive
   feedback on a declared bounded initial-data cylinder prepares the constant
   complete history, realizes the nodewise zero-recovery decision leaf with
   a bounded input, and forces nonsynchronous detector hits and finite signed
   excursions. On the exactly prepared synchronous leaf, a later handoff
   theorem closes every additive input at (+1), respectively at
   (-28/25) after latching the (-1) detector, and proves autonomous
   continuation to (+3/2), respectively (-6/5), before the first delayed
   layer changes. It also proves that closing the negative control already at
   (-1) causes a reversal before (-1.17). A robust extension replaces those
   two exact synchronized handoff histories by explicit open cylinders in the
   full RFDE phase space: asynchronous current and remote-history errors of
   size \(10^{-4}\), arbitrary-sign post-shutdown residuals below \(10^{-5}\),
   and declared nonzero \((\varepsilon,a)\)-errors still give componentwise
   monotone finite terminal capture for every admitted finite balanced
   topology. It is an entrance-cylinder theorem, not a proof that the earlier
   controller reaches that cylinder robustly. The same balance identities
   transfer the three-output target balls to the topology-independent
   synchronous branch. A separate
   transverse Halanay estimate, combined with the synchronous right-half
   certificate, supplies local orbital attraction for each fixed admitted
   network.  The independent oscillation-norm theorem proves uniform
   transverse decay rate \(0.007\) on the \(\eta=0\),
   \(\tau(Q)\le1/4\) balanced class; no network-uniform nonlinear basin is
   inferred.  The inherited nonzero-\(\eta\) replay likewise retains its
   original fixed-network attraction conclusion.  An exact
   cross-model audit also proves that the
   arbitrary-size selected-root RFDE is not the balanced dual-scaffold RFDE
   used by the periodic and handoff theorems, already in its two-module
   restriction. Its present delay-redistribution direction neither preserves
   nor is invisible on the validated synchronous periodic branch. Thus the
   existing results do not by themselves form a same-model
   three-input--three-output theorem. A quadratic period-locked extension now
   supplies one common dual-scaffold RFDE with an exact periodic-output null
   column and a proved small-\(\delta\) selected-root response, as recorded in
   item 8. Its fixed-\(\varepsilon\) root derivative, root/event comparison,
   robust reachability of the handoff entrance cylinder, biological basin
   capture, delay uncertainty, and bandwidth/noise/hardware containment
   remain open.
8. **Same-model nonlinear period-lock successor theorem.** On every finite
   balanced dual-scaffold topology, the quadratic collective channel
   \[
   \varepsilon\eta\Pi\{(v(t)-\mathbf1)^{\circ2}
   -(v(t-\tau_*)-\mathbf1)^{\circ2}\}
   \]
   preserves synchrony and constant histories, vanishes on the distinguished
   center periodic orbit, and has zero value and full Fréchet derivative at
   the right fold.  It therefore leaves the center orbit, period, frequency,
   voltage range, fold state, and fold linearization unchanged.  With fixed
   fold-time support \(\Theta_*\), the canonical enlarged-horizon synchronous
   selected root satisfies
   \[
   a_c(\delta,\eta)-a_c(\delta,0)
   =-\frac{\Theta_*}{2}\delta^3\eta
   +O(\delta^4|\eta|+\delta^3\eta^2).
   \]
   Under a common Dobrushin gap, nonnegative row-stochastic scaffold, positive
   stationary weight, and balanced half-mass delay layers, a uniform
   history-graph theorem makes the exact zero transverse graph the unique
   canonical retained graph.  Hence the synchronous law lifts to the genuine
   full network:
   \[
   a_{c,N}(\delta,\eta)-a_{c,N}(\delta,0)
   =-\frac{\Theta_*}{2}\delta^3\eta
   +O(\delta^4|\eta|+\delta^3\eta^2),
   \]
   with constants independent of network size and admitted topology.  This
   uniqueness is local to the canonical anisotropic tube
   \(P_\perp v=O(\delta^2)\), \(P_\perp w=O(\delta^4)\); it is not uniqueness
   for arbitrary histories or a basin theorem.  The linear period-lock
   alternative has an exactly vanishing leading Melnikov pairing, so a
   nonzero first delay moment is not a root theorem.
   At the exact physical center
   \((\varepsilon,a,\kappa_1,\kappa_3)=(1/5,3/5,1/5,1/4)\), the same carrier
   has a proved nonzero Floquet box
   \(|\eta|\le3\times10^{-6}\), including local attraction for each fixed
   admitted finite topology.  This does not supply a network-uniform basin
   and is logically separate from the selected-root expansion.
   Choosing \(\Theta_*=\delta_*T_*\) makes the quadratic delay equal the
   validated period at \(\delta_*=1/\sqrt5\), but the candidate
   \(-T_*/50\) is not a rigorous enclosure at \(\varepsilon=1/5\).  A
   fixed-\(\varepsilon\) validation blueprint now specifies the two-sided
   complete-history BVP, scalar jump complement, advanced dynamic adjoint,
   and interval radii-polynomial gate.  Its finite-section diagnostic gives
   negative candidates from \(-0.350\) to \(-0.264\), but the section drift is
   too large for any rigorous sign claim.  A later actual two-branch
   discretization solves both RFDE flights, the phase equation, and every
   represented history-jump node; its discrete adjoint, direct tangent, and
   finite difference agree, with finest candidate
   \(\rho_N=-0.3463310348\).  Its entry history now satisfies the RFDE
   solution-manifold compatibility equation exactly, but it is still an
   artificial full template rather than the selected attracting trace.  A
   new exact audit shows that the raw 194-coefficient history ledger has two
   independent endpoint-compatibility equations and hence a 192-dimensional
   compatible level; a rank-193 compatible chart is impossible.  An ambient
   193-coordinate ledger can retain the old 775-by-774 arithmetic only by
   using 192-row projected history matches and six explicit compatibility
   rows, and it still omits the global strong-history multicell seams.
   Separate compatible-history counterexamples prove that the scalar exit
   observable determines neither the complete history nor the future right
   flight.  Thus the actual Fredholm endpoint operator remains unconstructed.
   Parameter-coherent selected entry/exit bundles, the augmented inverse and
   continuous adjoint enclosure, and an input-independent onset comparison
   remain required.
   An exact stop/go composition audit now proves that the existing root,
   preparation, handoff and attraction modules do not imply physical onset:
   their \(\delta/a\) slices, selected histories, plant horizons and basin
   objects fail four literal composition hypotheses.  On the positive side,
   extending the controlled hold to the full \(T_*\) history and cancelling
   the quadratic carrier before release gives a same-plant controlled
   terminal-transfer theorem.  After every additive input is switched off,
   the released carrier fits inside the robust residual budget on both
   channels whenever
   \(|\eta|<250000/12972264861\approx1.92719\times10^{-5}\), for every finite
   admitted balanced topology.  This is policy-dependent finite terminal
   transfer, not onset, basin capture, or permanent no-return.  A separate
   reference-slice no-go theorem proves that the unique synchronous
   equilibrium has two open-right-half-plane characteristic roots throughout
   the microscopic gain box for \(|\eta|\le10^{-3}\), so that equilibrium
   cannot be the quiet attractor.  On \(\eta=0\), the attracting periodic
   orbit crosses \(+1,+3/2,-1\) every period and stays above \(-6/5\), which
   makes periodic capture incompatible with permanent residence on any of
   those detector sides.  This does not exclude a different quiet attractor;
   it forces the biological repair to be an actually validated bistable
   slice, an explicitly semantic latch, or a declared hybrid switch.
9. **Fixed-amplitude causal-chart route.**  The attempt to continue the
   singular \(\sigma\)-clock to \(\rho_*=1/\sqrt5\) now has an exact stopping
   theorem for the proposed geometry: at the frozen target candidate \(\nu\),
   an explicit zero of the shifted independent raw-slot transform lies
   inside the radius-\(10^{-3}\) product tube, so no planar current-state
   \(C^1\) phase can be strictly increasing there.  This is neither an RFDE
   equilibrium nor a no-go for history-dependent phases or other tubes.  A
   tapered phase still has a directed positive clock on the smaller
   \(0\le\nu\le1/5\) raw-slot comparison box, but this is not an actual target
   graph.  The replacement is an exact conditional prepared-chart theorem:
   a sufficiently smooth embedded family \(\Psi(t,\lambda)\) of physical RFDE
   solutions induces \(Q\circ\Psi=\partial_t\Psi\); after a compatible
   complete extension it satisfies a local physical-history identity on a
   smaller current image and has \(\mathcal L_Qt=1\),
   \(\mathcal L_Q\lambda=0\).  A binary64 target chart has sampled
   \(\det D\Psi\in[-3.02251,-0.114909]\).  The frozen-anchor incoming
   preparation seam is now closed exactly through total time--label order
   four by a degree-nine Hermite patch.  Replaying the same C4 history in the
   state and analytic label-variational DDE preserves positive sampled
   P-matrix and cross-separation margins.  The entire retained incoming
   history rectangle is now closed exactly: all 210
   \(\mathbb Q(\sqrt5)\) Bernstein coefficients prove the three P-matrix
   bounds \(9/100,24/25,2/5\), hence negative orientation and global
   injectivity by Gale--Nikaido.  The entire first physical method-of-steps
   rectangle \([-3,1]\times[-1/20,1/20]\) is now enclosed on 8,000
   time--label cells by 192-bit outward-rounded Picard--Bernstein arithmetic
   and a separate same-kernel replay at 256-bit precision.  Its rigorous lower P-matrix margins
   are $0.27854$, $0.99999994$, and $1.47290$; the last 1,000 cells use
   the exact delayed C4 patch.  The complete second method step
   \([1,3]\times[-1/20,1/20]\) is now covered by another 8,000 directed
   cells at 192 bits and a same-kernel 256-bit replay.  Composing the two
   steps proves the physical P-matrix inequalities on the full strip
   \([-3,3]\times[-1/20,1/20]\), while the strict bound
   \(X_e-X>0.4612322\) closes both physical cross-separation conditions.
   The enlarged label collar, C4-history/physical gluing, target graph,
   trace pair, Fredholm inverse and selected root remain open.
10. **Autonomous biological-onset route.**  A leaky-recovery replacement
   keeps the two delayed voltage channels and gives a unique quiet
   equilibrium that is proved locally exponentially stable for every pair of
   positive delays.  Directed finite/tail radii arguments now validate both
   a phase-fixed inner periodic RFDE orbit and a distinct phase-fixed outer
   periodic RFDE orbit, together with their phase-bordered derivatives.  The
   inner proof uses 129 nodes and cutoff 192; the formerly under-resolved
   outer branch uses 257 nodes and cutoff 384.  Both branches, their bordered
   inverses, and their unique simple voltage extrema are now validated on
   the common box
   \(|a-1/4|,|\kappa_3-1/200|\le10^{-10}\).  The neutral multiplier is
   algebraically simple at the center, and an analytic Riesz reduction removes
   the infinite Fourier tail, leaving a \(258\times258\) Schur determinant
   on the principal logarithmic half-strip.  The center inner right-half tree
   is now complete: it counts exactly the simple translation value and one
   simple positive nontranslation value, with zero complementary keyhole
   count.  Hence the center inner orbit has exactly one unstable multiplier.
   Classical RFDE periodic-orbit theory, together with the exact
   reduced-history factorization, now promotes this to a qualitative
   \(C^1\), codimension-one local stable manifold in both the full history
   space and the reduced phase-section representation.  No explicit graph
   radius, specific pulse-section transversality, separator or onset follows
   from that qualitative theorem.  Independent source-bound base and
   extension trees also prove the stronger center stable spectral bound
   \(\rho_s\le e^{-0.01}=0.9900498337\ldots<1\).  With an optimized sequence
   weight this makes one idealized Lyapunov--Perron design row arithmetically
   feasible, but it is not yet a usable graph theorem because the actual
   projection norms, stable-power constants, and nonlinear remainder bound
   remain unproved.  A separate Stage-2 certificate validates an explicit
   phase-zero voltage section with speed at least
   \(0.2067539137\ldots\) throughout its radius-\(0.01\) section ball and a
   unique nearby true-orbit crossing of the old binary64 voltage level.  It
   proves section admissibility, not a pulse/stable-sheet crossing.  The
   index result is not continued over
   the common box, and the outer zero-index remains open.  A corrected
   rectilinear-core calibration proves that simply relaxing the Neumann
   acceptance threshold does not cure the narrow near-neutral workload; the
   next rigorous route is a one-dimensional Grushin/pole-subtracted local
   certificate composed with the existing outer cover.

   The independent directed D4 certificate has status **ACCEPT**: the inner response
   determinant is negative and the outer response determinant is positive on
   the common box.  For the flagship outer \((F,A)\) block, the parameter
   inverse Lipschitz certificate is
   \(22.044336699647400986\ldots<22.044336699647401\), and the
   branch-centered output target radius is at least
   \(4.5363124943378087\times10^{-12}\).  The smaller
   \(4.0971263701603406\times10^{-13}\) lower bound is only the common minimum for
   the two distinct branch-centered response balls.  Under the remaining
   outer/common-box Floquet, history-space routing and pulse-transversality
   hypotheses, the exact block-triangular theorem then makes
   \((a,\kappa_3,J)\mapsto(F,A,J-J_c)\) a local diffeomorphism.  D4 itself
   proves no \(J_c\), separator, onset, safety threshold, routing or capture.
   The physical one-unit pulse has an
   exact jointly smooth release-history map
   $J\mapsto R(J)\in C([-5\sqrt5,0],\mathbb R^2)$; its stimulus tangent is
   componentwise positive on the newly written part of the history, making
   the pulse curve an oriented embedding.  A source-bound finite-section
   shooting calculation then locates
   $J_{\rm sep}^{\rm num}\simeq0.301135337086902$: third-return roots agree
   over 120, 180, and 240 history meshes to $3.3\times10^{-15}$, an
   independent DOP853 refinement ladder spans $5.3\times10^{-15}$, and the
   multiplier-scaled derivative stays near $-3.449$.  An independent
   Razumikhin theorem supplies an explicit complete-history quiet basin, and
   a 7,728-cell directed method-of-steps proof shows that the physical pulse
   \(J=0.30\) enters it at \(T=161\sqrt5\); a 256-bit, 10,304-cell replay
   confirms the strict terminal inequality.  This is one rigorous quiet-side
   capture, not a stable-manifold crossing, routing theorem, threshold, or
   onset proof.

   For every finite topology with \(Q\ge0\), \(Q\mathbf1=\mathbf1\),
   \(\tau(Q)\le1/2\), and fixed \(B_j\ge0\) satisfying
   \(B_j\mathbf1=\mathbf1/2\), the quotient transverse variational equation
   decays at rate \(1/10\).  No common identity
   \(\pi^TB_j=\pi^T/2\) is required.  A forward pullback gives
   \(\|G_{\perp,N}\|\le10\), uniformly in network size and topology.  In
   stationary collective/quotient coordinates the complete-history Lin
   operator is upper triangular.  The exact invertible codomain row operation
   \(T_N(y_\parallel,y_\perp)
   =(y_\parallel-C_NG_{\perp,N}y_\perp,y_\perp)\) reduces it, by
   postcomposition, to the scalar/transverse direct sum, with
   \(\|C_NG_{\perp,N}\|\le(391/2000)\delta_B\).  The full cokernel is
   \(\Psi_N(y_\parallel,y_\perp)
   =\psi(y_\parallel-C_NG_{\perp,N}y_\perp)\).  Therefore any separately
   proved scalar phase-fixed simple root with the declared collective
   preparation transfers with the same Fredholm data, location, slope, and
   orientation; the scalar leaky root itself is not proved.

   A nonlinear companion proves node-diameter decay at the same rate while
   the network stays in the voltage strip.  With
   \(\delta_j=\frac12\|\pi^TB_j-\pi^T/2\|_1\),
   \(\delta_B=\delta_0+\delta_1\), and
   \(\mathcal H_M(t)=\sup_{t-r\le s\le t}M(s)\), the collective forcing obeys
   \[
   |R_{\rm coll}(t)|
   \le\frac{391}{20000}\delta_B\mathcal H_M(t)
      +\frac{703}{200}\mathcal H_M(t)^2.
   \]
   Its delay-resolved accumulated linear coefficient is
   \((391/20000)[\delta_0(10+4\sqrt5)+\delta_1(10+5\sqrt5)]\); using only
   \(\delta_B\) gives the worst linear term
   \(391(2+\sqrt5)\delta_BM_0/4000\), plus
   \((56483/3200)M_0^2\).  In the balanced special case \(\delta_B=0\),
   the sharper exact quadratic accumulation is
   \((703/40+27\sqrt5/800)M_0^2\).  These uniform estimates still need an
   invariant strip and scalar routing/product-lift theorem before they yield
   any asynchronous threshold basin.
   The scalar leaky root, outer and parameter-box Floquet gates, quantitative
   stable separator, threshold derivatives, outer-side capture, and equality
   of a canard root with physical onset remain open.
11. **Numerical diagnostic.** Literal method-of-steps integration of one
   finite-section exact-chart diagnostic gives
   \([\nu_c(\delta,h)-\nu_c(\delta,-h)]/(2\delta h)\) converging from
   \(-0.1969771\) to \(-0.2036174\), against the predicted
   \(K(\theta_0-\theta_1)/(4\alpha)=-0.2041241\). This is falsification
   evidence for the coefficient, not a proof that the diagnostic root equals
   the canonical history root or a physical outer root.

## Repository map

- `manuscript/jns/main.tex` -- JNS manuscript entry point;
- `manuscript/jns/sections/` and `manuscript/jns/appendices/` -- self-contained
  theorem, proof, numerical diagnostic, and technical estimates;
- `manuscript/jns/figures/` -- deterministic vector-figure sources and PDFs;
- `manuscript/jns/submission/` -- cover letter, editor suggestions, checklist,
  and claim-boundary report;
- [manuscript/flagship-successor-outline.md](manuscript/flagship-successor-outline.md) -- proof-first architecture for the larger finite-network root-transfer and physical pulse-threshold control paper, with canard roots and pulse thresholds kept distinct unless a comparison theorem is proved;
- [manuscript/flagship/main.tex](manuscript/flagship/main.tex) -- compiling research draft of the successor manuscript, currently containing the general-network theorem package and an explicitly conditional pulse-completion theorem; it is not submission ready while the listed release gates remain open;
- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- [docs/general-network-canard-pulse-control-program.md](docs/general-network-canard-pulse-control-program.md) -- active successor program: arbitrary finite-\(N\) one-fold history graphs, vector-gap extension, physical pulse onset, and quantitative three-output control/no-go gates;
- [docs/flagship-general-network-biological-control-synthesis.md](docs/flagship-general-network-biological-control-synthesis.md) -- theorem-level synthesis of the proved Dobrushin selected-root response and the balanced-network bounded staged control theorem, with the missing same-model biological interface kept explicit;
- [docs/general-network-one-gap-root-transfer.md](docs/general-network-one-gap-root-transfer.md) -- dimension-uniform scalar root-transfer theorem with quantitative radius and remainder, a proved shared-resource Dobrushin root instance, and the concrete leaky complete-line transverse inverse separated from the still-open scalar leaky root;
- [docs/same-model-shared-resource-root-detector-bridge.md](docs/same-model-shared-resource-root-detector-bridge.md) -- exact controller-mediated policy composition that injects the selected-root displacement into detector latency within one shared-resource RFDE, together with a policy-offset falsifier excluding any intrinsic-onset interpretation;
- [docs/paper-iv-root-periodic-model-compatibility.md](docs/paper-iv-root-periodic-model-compatibility.md) -- exact equation-by-equation audit proving that the current arbitrary-size selected-root and balanced periodic/control theorems use different RFDEs, together with the two-fixed-delay synchronization obstruction and the minimum route to a genuine same-model response theorem;
- [docs/unified-rfde-period-locked-escape.md](docs/unified-rfde-period-locked-escape.md) -- arbitrary-finite-balanced-topology period-locked carrier audit, including the exact linear-channel parity boundary and the distinction between collective moments and complete-history root derivatives;
- [docs/quadratic-period-locked-selected-root.md](docs/quadratic-period-locked-selected-root.md) -- exact nonlinear carrier theorem, qualitative three-parameter periodic branch with zero structural output column, and proved small-\(\delta\) canonical synchronous selected-root law in one extended dual-scaffold RFDE;
- [docs/quadratic-period-lock-dobrushin-full-network.md](docs/quadratic-period-lock-dobrushin-full-network.md) -- dimension-uniform Dobrushin semigroup/model fit and full-network canonical zero-graph lift of the quadratic selected root, with the anisotropic local tube and closing-gap boundary explicit;
- [docs/dual-scaffold-period-locked-root-adjoint-gate.md](docs/dual-scaffold-period-locked-root-adjoint-gate.md) -- normalization-invariant complete-history adjoint ratio, exact linear-carrier cancellation, and the executable fixed-\(\varepsilon\) validation contract for \(\rho_*\);
- [docs/fixed-epsilon-quadratic-root-bvp.md](docs/fixed-epsilon-quadratic-root-bvp.md) -- exact \(\varepsilon=1/5\) two-sided full-history BVP/advanced-adjoint validation blueprint and a deliberately non-promoted finite-section shooting diagnostic;
- [docs/fixed-epsilon-two-sided-candidate.md](docs/fixed-epsilon-two-sided-candidate.md) -- actual binary64 two-branch RFDE solve with phase, nodewise full-history jump and discrete adjoint, together with the explicit wrong-endpoint-geometry reason it is not a selected-root certificate;
- [docs/fixed-epsilon-sliding-window-w1p-bridge.md](docs/fixed-epsilon-sliding-window-w1p-bridge.md) -- proved sliding-window equivalence, exact endpoint-circularity rank collapse, the corrected \(W^{1,p}\to L^p\) scale, and the conditional trace-pair index-\(-1\) theorem; independent selected traces and the fixed-\(\varepsilon\) root remain open;
- [docs/fixed-window-prepared-gap-seed.md](docs/fixed-window-prepared-gap-seed.md) -- proved finite-window linear Green row and MPFR-directed unique affine zero for a singular-hull-compatible longitudinal first-order forcing datum; the field/jet clause of its promotion condition is now realized by the clocked-tail graph below, while the one-sided trace family, target-amplitude continuation, and fixed-\(\varepsilon\) history root remain open;
- [docs/fixed-epsilon-frozen-graph-operator.md](docs/fixed-epsilon-frozen-graph-operator.md) -- exact scalar two-dimensional nonlocal frozen-graph operator, explicit distinct graph/planar cutoff data, directed proof-native nesting radius, residual-variation row, and conditional C3 Seeley preparation rule; no graph fixed point, positive-amplitude hull, prepared trace, or root is validated;
- [docs/fixed-epsilon-singular-reachable-hull.md](docs/fixed-epsilon-singular-reachable-hull.md) -- exact smooth first integral and Lambert-W branch geometry for the singular canard field, the asymmetric continuous backward delay hull, a fixed-width-tube obstruction, the perturbed J-barrier identity, and a preparation-indexed causal-slab restriction lemma; target clock/barrier bounds, left-tail propagation, the positive-amplitude hull, graph inverse, and fixed-epsilon root remain open;
- [docs/fixed-epsilon-clocked-tail-graph-extension.md](docs/fixed-epsilon-clocked-tail-graph-extension.md) -- bounded complete pointwise clock-positive tail, exact parameter-independent incoming germ, an applied fixed-cutoff small-amplitude special-flow graph theorem with finite mixed jets and the prepared seed first jet, plus a preparation-indexed Volterra--Weissinger theorem; the graph at \(\rho_*=1/\sqrt5\), target clock/barriers, trace pair, fixed-epsilon root, network lift, and biological-control chain remain open;
- [docs/fixed-epsilon-target-tilted-phase.md](docs/fixed-epsilon-target-tilted-phase.md) -- exact raw-slot reversal/stall algebra, the frozen-anchor radius-\(10^{-3}\) product-tube positive-clock no-go, and a separate directed tapered-phase comparison on \(0\le\nu\le1/5\); it is not an actual target causal phase;
- [docs/fixed-epsilon-target-causal-tube-candidate.md](docs/fixed-epsilon-target-causal-tube-candidate.md) -- parent binary64 prepared target-amplitude solution tube and the exact conditional theorem that an embedded physical solution family induces a local fixed graph, unit intrinsic time clock and invariant transverse labels; the successor records below replace its first-order seam but leave interval embedding open;
- [docs/fixed-epsilon-target-c4-preparation-seam.md](docs/fixed-epsilon-target-c4-preparation-seam.md) -- exact frozen-anchor fourth-order incoming seam with recursive RFDE time/mixed jets, while the interval solution chart and graph remain open;
- [docs/fixed-epsilon-target-chart-univalence-gate.md](docs/fixed-epsilon-target-chart-univalence-gate.md) -- exact P-matrix/Gale--Nikaido univalence reduction and combined C4 state/analytic-variational binary64 replay, with every interval embedding and degree flag left false;
- [docs/fixed-epsilon-target-c4-history-bernstein.md](docs/fixed-epsilon-target-c4-history-bernstein.md) -- exact \(\mathbb Q(\sqrt5)\) Bernstein positivity and Gale--Nikaido global injectivity for the full retained incoming C4-history rectangle;
- [docs/fixed-epsilon-target-first-step-interval.md](docs/fixed-epsilon-target-first-step-interval.md) -- first rigorous full-label physical Picard--Taylor cell and the local prototype subsequently extended by the full first-step cover;
- [docs/fixed-epsilon-target-first-step-cover.md](docs/fixed-epsilon-target-first-step-cover.md) -- rigorous 8,000-cell Picard--Bernstein cover of the full first physical method step \([-3,1]\times[-1/20,1/20]\), including the delayed C4 patch and a separate same-kernel replay at 256-bit precision;
- [docs/fixed-epsilon-target-second-step-cover.md](docs/fixed-epsilon-target-second-step-cover.md) -- rigorous second 8,000-cell cover on \([1,3]\times[-1/20,1/20]\), full-strip P-matrix composition, and both physical cross-separation inequalities; the enlarged collar, glued embedding, graph and root remain open;
- [docs/fixed-epsilon-selected-attracting-endpoint-chart.md](docs/fixed-epsilon-selected-attracting-endpoint-chart.md) -- finite-mesh attracting-endpoint audit, now explicitly superseded at the continuous level by the sliding-window/\(W^{1,p}\) correction;
- [docs/fixed-epsilon-selected-fredholm-structure.md](docs/fixed-epsilon-selected-fredholm-structure.md) -- earlier projected-history coordinate audit plus the corrected natural full-history \(W^{1,p}\) ledger, with actual trace-range closedness, cokernel and inverse still open;
- [docs/fixed_epsilon_selected_repelling_endpoint.md](docs/fixed_epsilon_selected_repelling_endpoint.md) -- exact same-current, same-exit and compatible-history counterexamples, together with the superseding reduction from a history-chart PDE to one independently selected orbit;
- [docs/quadratic-physical-onset-capture-stop-go.md](docs/quadratic-physical-onset-capture-stop-go.md) -- exact four-gate non-composition theorem plus a same-plant, arbitrary-finite-balanced controlled terminal transfer for an explicit strict small-\(|\eta|\) bound, with onset/basin/no-return claims refused;
- [docs/quadratic-reference-slice-dual-basin-no-go.md](docs/quadratic-reference-slice-dual-basin-no-go.md) -- exact Rouché proof that the reference synchronous rest state is unstable on a nonzero \(\eta\)-box, periodic-orbit face-recurrence obstruction to permanent detector-side residence, and the separated autonomous-bistable, latch, and hybrid-switch repair contracts;
- [docs/autonomous-leaky-recovery-bistable-rfde-proposal.md](docs/autonomous-leaky-recovery-bistable-rfde-proposal.md) -- leaky-recovery two-delay RFDE and conditional autonomous frequency--amplitude--onset theorem; the quiet equilibrium, two periodic branches on a common parameter box, simple extrema, center-inner one-unstable count, directed two-output response, oriented pulse-history curve, and one strict quiet-side pulse capture are proved, while the outer/common-box Floquet gates, separator, routing, safety and onset remain open;
- [docs/leaky-periodic-finite-tail-floquet-contract.md](docs/leaky-periodic-finite-tail-floquet-contract.md) -- equation-level finite/tail and Floquet contract for leaky recovery, including the terms that differ from the nonleaky validator and the remaining spectral gates;
- [docs/leaky-periodic-majorant-audit.md](docs/leaky-periodic-majorant-audit.md) -- independent operator and majorant proof for the leaky recovery term, closing the inner periodic-orbit and phase-bordered-inverse radii theorem while deliberately stopping before Floquet promotion; the later center-inner cover below closes the center count only;
- [docs/leaky-outer-high-resolution-artifact.md](docs/leaky-outer-high-resolution-artifact.md) -- 129/193/257/385-node outer resolution ladder and a 257-node, cutoff-384 directed-radii theorem for the outer phase-fixed periodic RFDE orbit, without an attraction claim;
- [docs/leaky-periodic-parameter-response.md](docs/leaky-periodic-parameter-response.md) -- exact \((a,\kappa_3)\) parameter columns, binary64 frequency--unsquared-amplitude response diagnostics, and the rigorous common orbit/extrema box used by the later directed D4 theorem;
- [docs/leaky-periodic-directed-response.md](docs/leaky-periodic-directed-response.md) -- directed D4 theorem on the common box, with opposite nonzero determinant signs, branch-specific inverse and target-ball bounds, the outer flagship radius kept distinct from the smaller simultaneous-branch minimum, and every onset/safety/capture flag false;
- [docs/leaky-floquet-transfer.md](docs/leaky-floquet-transfer.md) -- RFDE periodic-operator transfer, exact translation mode, phase-bordered inverse and local neutral-multiplier simplicity; its stage-local count refusal is superseded at the center inner orbit by the complete cover below;
- [docs/leaky-floquet-riesz-reduction.md](docs/leaky-floquet-riesz-reduction.md) -- analytic elimination of the infinite Fourier tail and multiplicity-preserving reduction of the closed principal right half-strip to a finite Schur determinant;
- [docs/leaky-floquet-inner-unstable-root.md](docs/leaky-floquet-inner-unstable-root.md) -- directed local proof of exactly one simple positive center-inner characteristic value;
- [docs/leaky-floquet-inner-right-half-cover.md](docs/leaky-floquet-inner-right-half-cover.md) -- complete center-inner closed-right-half-plane count: translation one, positive nontranslation one, complementary keyhole zero; by itself it makes no common-box, stable-manifold or onset promotion;
- [docs/leaky-inner-stable-manifold-stage1-contract.md](docs/leaky-inner-stable-manifold-stage1-contract.md) -- source-bound promotion of the center inner orbit to a qualitative \(C^1\), codimension-one stable manifold in full and reduced history spaces, plus the unpromoted quantitative Lyapunov--Perron interface;
- [docs/leaky-inner-stable-manifold-stage2-contract.md](docs/leaky-inner-stable-manifold-stage2-contract.md) -- source-bound strong-gap design audit and executable orbit-section gates; the optimistic majorant is feasible, while actual projection/power/remainder constants and every pulse crossing or onset claim remain false;
- [docs/leaky-floquet-inner-stable-gap.md](docs/leaky-floquet-inner-stable-gap.md) -- completed center-inner left-strip cover proving \(\rho_s\le e^{-0.001}<1\), while keeping projection norms, a quantitative stable graph and every onset claim false;
- [docs/leaky-floquet-inner-strong-stable-gap.md](docs/leaky-floquet-inner-strong-stable-gap.md) -- completed source-bound extension of the stable strip to \(\operatorname{Re}s=-0.01\), giving \(\rho_s\le e^{-0.01}\) while keeping projection/power constants, a quantitative stable graph, and every onset claim false;
- [docs/leaky-floquet-outer-right-half-cover.md](docs/leaky-floquet-outer-right-half-cover.md) -- outer zero-index cover contract and resumable full-tree checkpoint; no final outer-index certificate has yet been issued;
- [docs/leaky-floquet-outer-right-half-cover-calibration.md](docs/leaky-floquet-outer-right-half-cover-calibration.md) -- corrected rectilinear-core equal-budget calibration showing that threshold relaxation is ineffective and isolating the next pole-subtracted/Grushin proof route; every outer-index and attraction flag remains false;
- [docs/leaky-pulse-terminal-history.md](docs/leaky-pulse-terminal-history.md) -- exact reduction of the one-unit physical pulse to a parameter ODE before either delay returns, with a jointly smooth, injective, positively oriented curve of complete terminal histories;
- [docs/leaky-pulse-separator-candidate.md](docs/leaky-pulse-separator-candidate.md) -- source-bound three-mesh, three-return finite-section shooting candidate near $J=0.301135337086902$, with a separate integration-refinement ladder and every stable-manifold/onset flag kept false;
- [docs/leaky-pulse-separator-validation-contract.md](docs/leaky-pulse-separator-validation-contract.md) -- narrow third-return bracket $[0.30113,0.30114]$, event-time derivative formula, exact Riesz/stable-graph error decomposition, and explicit directed error targets; the accompanying binary64 target keeps every separator/onset/routing flag false;
- [docs/leaky-pulse-separator-bracket-tradeoff.md](docs/leaky-pulse-separator-bracket-tradeoff.md) -- source-bound binary64 comparison of narrow, medium and wider third-return brackets; the recommended wider diagnostic trades a (1.659\times10^{-3}) endpoint mesh radius for a (9.08\times10^{-4}) gap margin, while every continuous-history, covector, stable-graph, crossing, onset and routing flag remains false;
- [docs/leaky-pulse-inner-route-c-family-contract.md](docs/leaky-pulse-inner-route-c-family-contract.md) -- directed failure certificate for the full-width zero-centered pulse tube, one exact 30,000-way shard pilot, and the zero-width variation-wrapping audit that makes an event-aligned parameter jet mandatory;
- [docs/leaky-pulse-event-aligned-parameter-jet-contract.md](docs/leaky-pulse-event-aligned-parameter-jet-contract.md) -- historical factorial fourth-order flow-jet contract with fifth-order remainder, implicit event jets and common-event history pullback; it originally listed an interval-Newton gate, whereas the current completion uses graph-adjusted endpoint signs and strict monotonicity for existence/uniqueness and treats Newton only as optional sharpening;
- [docs/leaky-pulse-parameter-jet-center-pilot.md](docs/leaky-pulse-parameter-jet-center-pilot.md) -- three-refinement correlated \(a_0,\ldots,a_4\) center pilot whose full-width scaled hierarchy decays through fourth order and whose endpoint reconstruction discrepancy is below \(2.70\times10^{-10}\); no directed remainder or event claim;
- [docs/leaky-pulse-parameter-jet-directed-enclosure.md](docs/leaky-pulse-parameter-jet-directed-enclosure.md) -- 192-bit directed full-width Taylor--Bernstein enclosure of the correlated coefficients and fifth-order remainder on all 1152 cells; the fixed-common-time family is proved, while event-time, common-event-history, stable-sign, onset and routing flags remain false;
- [docs/leaky-pulse-route-c-event-stage5c.md](docs/leaky-pulse-route-c-event-stage5c.md) -- independently replayed full-width Route-C event certificate: corrected exact orbit-section level, unique positive event in a common bracket, uniform speed, fourth-order event-time graph and continuous common-event reduced-history tube; third-crossing, stable-sheet, Newton, onset and routing flags remain false;
- [docs/leaky-pulse-event-aligned-derivative-stage5d.md](docs/leaky-pulse-event-aligned-derivative-stage5d.md) -- independently replayed 192-bit first-variation theorem on all 1152 cells, including the event-time derivative and complete-history translation term; it proves a continuous \(D_JK\) but only a modulus bound for the fixed adjoint action, so signed slope, stable gap, Newton, onset and routing remain false;
- [docs/leaky-pulse-oriented-adjoint-action-stage5e-contract.md](docs/leaky-pulse-oriented-adjoint-action-stage5e-contract.md) -- exact next-gate contract for the physical-right-gauge-corrected same-row residual action; it distinguishes the stored complex Grushin eigencolumn from the oriented real unstable history, specifies the correlated event-history budget and sign gate, and keeps the stable-graph correction separate from the action;
- [docs/leaky-pulse-oriented-adjoint-action-stage5e.md](docs/leaky-pulse-oriented-adjoint-action-stage5e.md) -- 192-bit correlated same-row theorem fixing the physical real right gauge and proving \(f_{\rm phys}(D_JK)\in[-258.746522,-245.253478]\) throughout the full pulse interval; this is a fixed-functional action, not by itself a stable-gap slope;
- [docs/leaky-pulse-stable-gap-slope-bridge-stage5f.md](docs/leaky-pulse-stable-gap-slope-bridge-stage5f.md) -- frozen historical parent proving the coarse source-bound projection and conditional-slope bridge in the same \(Y/\Sigma\), physical Grushin normalization, and centered chart; its numerical bounds are sharpened by Stages 5G-a/b;
- [docs/leaky-pulse-endpoint-functional-stage5ga.md](docs/leaky-pulse-endpoint-functional-stage5ga.md) -- source-bound same-row complete-history endpoint certificate proving strict opposite signs of \(f_{\rm phys}(\kappa(J_\pm))\), endpoint stable-coordinate bounds, and the conditional arithmetic of a \(10^{-3}\) graph-height target; it supplies no graph, stable-gap sign, crossing, onset, or routing;
- [docs/leaky-pulse-stable-coordinate-cone-stage5gb.md](docs/leaky-pulse-stable-coordinate-cone-stage5gb.md) -- exact-rational two-ended cone certificate proving \(\|P_sD_J\kappa\|_Y\le5.979324\), full-interval radius \(47/5000\), and the conditional slope interval \([-354.415700,-149.584300]\) under a future same-coordinate graph with \(\|D\psi\|\le16\); graph-domain containment, graph-adjusted signs, crossing, onset, routing, capture, and safety remain false;
- [docs/leaky-route-c-adjoint-stage4c.md](docs/leaky-route-c-adjoint-stage4c.md) -- qualitative RFDE left-adjoint and correlated-deflation theorem plus a directed nonzero infinite-tail Fourier cokernel row;
- [docs/leaky-route-c-adjoint-stage4d.md](docs/leaky-route-c-adjoint-stage4d.md) -- rigorous Fourier-to-continuous-history Route-C bridge, summable adjoint tail, border normalization and nonzero recovery-history action; its finite-section \(Y_{qq}\) pilot is diagnostic, and the former physical-time action gate is closed separately by Stage 4E;
- [docs/leaky-shared-yqq-deflation-stage4e.md](docs/leaky-shared-yqq-deflation-stage4e.md) -- 192-bit physical-time \(V_{qq}\) tube and continuous atom-plus-density same-row quotient certificate proving \(C^{uu}_{s,\mathrm{base}}\le7.905650<12\); uniform split-ball inflation, the other five blocks, nonlinear split return, six-block graph and onset remain false, while discrete stable power is closed separately by Stage 4L;
- [docs/leaky-uniform-uu-inflation-stage4g.md](docs/leaky-uniform-uu-inflation-stage4g.md) -- exact radius-\(0.0017\) inflation budget and a 1042-cell directed failure certificate for the positive scalar \(P\)-majorant; it identifies the first lost section cell and the four-word signed replacement while keeping every uniform-block, graph and onset flag false;
- [docs/leaky-inner-signed-stable-flow-stage4h.md](docs/leaky-inner-signed-stable-flow-stage4h.md) -- exact four-word Volterra support and source-bound signed-flow diagnostic; the rank-one and event rows are combined before total variation, but the sampled one-step norm is not promoted to a directed stable power;
- [docs/leaky-inner-word-primitive-stage4i.md](docs/leaky-inner-word-primitive-stage4i.md) -- 192-bit, 1042-cell primitive residual and moving-frame ingress certificate, together with a rigorous no-go for unprojected physical-frame propagation; the complete two-variable signed row and continuous output-time supremum remain open;
- [docs/leaky-inner-projected-stable-flow-stage4j-contract.md](docs/leaky-inner-projected-stable-flow-stage4j-contract.md) -- a posteriori projected-residual closure \(K\le\widehat K/(1-\Delta)\), including the complete-history identity block, transport seams, and terminal event factor; after Stage 4L it remains an optional stronger intermediate-flow route, not a prerequisite for discrete stable power;
- [docs/leaky-inner-terminal-stable-row-stage4l.md](docs/leaky-inner-terminal-stable-row-stage4l.md) -- source-bound common terminal atom--density row for the selected near-one-period phase-fixed linear map, proving \(\|AP_s\|\le0.009896427481610001<0.1\) and, by exact intertwining, \(\|A_s^n\|\le0.1^n\) with \(K_s=1\); first return, nonlinear tube, six uniform Hessian blocks, stable graph, crossing and onset remain false;
- [docs/leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility.md](docs/leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility.md) -- source-bound nonclosing feasibility pilot rejecting two cancellation-blind scalar Gronwall routes and registering the conditional future signed-kernel target \(K_{\rm ret}<188.9122238810816\); it proves no nonlinear return, Hessian block, graph, crossing or onset theorem;
- [docs/leaky-inner-event-aligned-return-hessian-stage4o-contract.md](docs/leaky-inner-event-aligned-return-hessian-stage4o-contract.md) -- exact fixed-time and moving-event second-variation identities, one-and-only-one phase projection rule, selected-versus-first-return separation, and the failure of the present one-period argument to meet the general sufficient complete-history \(C^2\) threshold;
- [docs/leaky-inner-graph-closure-arithmetic-stage4p.md](docs/leaky-inner-graph-closure-arithmetic-stage4p.md) -- fail-closed one- and two-return six-block majorant design, physical-coordinate normalization audit, and conditional unique-crossing arithmetic; every graph/crossing/onset flag remains false;
- [docs/leaky-inner-signed-second-variation-stage4q-pilot.md](docs/leaky-inner-signed-second-variation-stage4q-pilot.md) -- signed near-two-period finite-section Hessian pilot with corrected one-sided endpoint adapter, three-grid diagnostics, fixed Stage-4L coordinates and all theorem flags false;
- [docs/finite-delay-eventually-smooth-selected-return-stage4r.md](docs/finite-delay-eventually-smooth-selected-return-stage4r.md) -- fail-closed general finite-delay RFDE theorem giving a sufficient \(T_->k\tau_*\) criterion under explicit chart, common-tube, endpoint-sign, speed, and image-containment hypotheses, plus a direct selected-return stable-set-germ lemma under explicit phase-isolation and intervening-flow hypotheses;
- [docs/leaky-reduced-history-factorization.md](docs/leaky-reduced-history-factorization.md) -- exact factorization through voltage history plus current recovery, stable-set pullback, and preservation of all nonzero monodromy multiplicities;
- [docs/leaky-quiet-large-razumikhin-basin.md](docs/leaky-quiet-large-razumikhin-basin.md) -- explicit complete-history Razumikhin sublevel contained in the quiet basin;
- [docs/leaky-pulse-quiet-capture.md](docs/leaky-pulse-quiet-capture.md) -- directed complete-history proof that the physical pulse \(J=0.30\) enters the quiet basin, with a finer independent arithmetic replay and no onset promotion;
- [docs/leaky-dobrushin-transverse-halanay.md](docs/leaky-dobrushin-transverse-halanay.md) -- topology- and dimension-uniform transverse decay for every finite balanced network in the declared Dobrushin class;
- [docs/leaky-dobrushin-nonlinear-synchronization.md](docs/leaky-dobrushin-nonlinear-synchronization.md) -- nonlinear node-diameter decay at rate (1/10), uniform in every finite admitted topology for as long as all node voltages remain in the validated strip; strip invariance and a uniform basin remain open;
- [docs/leaky-dobrushin-collective-defect.md](docs/leaky-dobrushin-collective-defect.md) -- exact network-mean equation, a componentwise delayed quadratic bound, the history-envelope bound \((703/200)\mathcal H_M^2\), and accumulated size \((703/40+27\sqrt5/800)M_0^2\le(56483/3200)M_0^2\), without a scalar shadowing or basin promotion;
- [docs/leaky-dobrushin-async-routing-transfer.md](docs/leaky-dobrushin-async-routing-transfer.md) -- exact conditional first-exit bootstrap, full-history asynchronous routing budget, monotone threshold-shift bound and safety guard; every missing scalar route/lift/gap constant is null, so no concrete network radius or onset is promoted;
- [docs/leaky-dobrushin-complete-line-inverse.md](docs/leaky-dobrushin-complete-line-inverse.md) -- unique bounded complete transverse forced solution, Green bound \(\|G_{\perp,N}\|\le10\), and conditional exact transfer of the scalar root/index/slope to canonical synchronized Lin problems;
- [docs/leaky-dobrushin-upper-triangular-root-transfer.md](docs/leaky-dobrushin-upper-triangular-root-transfer.md) -- removes common delay-layer left balance under fixed nonnegative half-row-mass layers: the Lin operator is uniformly reducible upper triangular, while the nonlinear collective budget records both the delay-resolved linear imbalance and delayed-history residence; the scalar leaky root, invariant strip, and onset remain open;
- [docs/leaky-pulse-onset-proof-route.md](docs/leaky-pulse-onset-proof-route.md) -- quantitative Lyapunov--Perron stable-graph, pulse-transversality, two-exit routing, and block-triangular \((F,A,J-J_c)\) proof architecture, with every unclosed hypothesis listed;
- [docs/leaky-outer-two-sided-routing-contract.md](docs/leaky-outer-two-sided-routing-contract.md) -- executable history-space outer-tube, signed-exit and two-face attachment criteria, proved local outer vector-field bounds, a nonexplicit quiet interval near \(J=0.30\), and a source-bound \(J=0.32\) outer target, while every actual routing/onset flag remains false;
- [docs/leaky-outer-signed-kernel-stage2.md](docs/leaky-outer-signed-kernel-stage2.md) -- 160-bit directed phase subtraction and total variation for the exact stored outer-return shadow, with the exact Dirac--density--scalar decomposition and continuous transfer-error gate; it is not yet an arbitrary-\(C^0\) operator bound;
- [docs/leaky-outer-continuous-kernel-stage3-shard.md](docs/leaky-outer-continuous-kernel-stage3-shard.md) -- first directed continuous resolvent and absolutely continuous density shards for both delay injections, including exact-orbit/period uncertainty and a tested nonzero-delayed-forcing interface; global kernel transfer remains open;
- [docs/leaky-outer-continuous-kernel-stage3b-frontier.md](docs/leaky-outer-continuous-kernel-stage3b-frontier.md) -- independently audited crossing of the first delayed-forcing boundary for both injection branches and a rigorous frontier/count certificate showing why a million-cell positive tiling is not the global signed-kernel proof;
- [docs/leaky-outer-delay-word-stage3c-compression.md](docs/leaky-outer-delay-word-stage3c-compression.md) -- exact support reduction of the global continuous return kernel to 14 history and 7 recovery delay-word integrals, all of order at most two; it replaces the million-cell route by a 21-term signed integration problem but does not yet bound \(E_v,E_w,E_{\rm phase}\);
- [docs/leaky-outer-delay-word-stage3d-primitives.md](docs/leaky-outer-delay-word-stage3d-primitives.md) -- exact Duffy reduction of the 21 depth-two words to eight one-dimensional \(F,G,H,L\) primitives, with phase and cross-word summation ordered before total variation; only the phase-independent projection transfer closes at this stage;
- [docs/leaky-outer-delay-word-stage3e-relative-residual.md](docs/leaky-outer-delay-word-stage3e-relative-residual.md) -- 160-bit degree-24, 1024-cell relative-residual proof for \(F,G\) on the exact orbit/period ball; it validates sub-\(0.0051\) multiplicative errors and rigorously rejects cancellation-blind separate \(H,L\) propagation, while \(E_v,E_w\) and \(C^0\) contraction remain open;
- [docs/leaky-outer-signed-row-stage3f-adjoint.md](docs/leaky-outer-signed-row-stage3f-adjoint.md) -- exact phase-combined advanced-row architecture, instantaneous Green/boundary enclosure, and coefficient/phase-ratio budgets, with signed summation performed before every row norm;
- [docs/leaky-outer-resolvent-stage3g-tensor.md](docs/leaky-outer-resolvent-stage3g-tensor.md) -- corrected v2 theorem on all 730 ordinary plus 40 clipped rectangles and 12,320 patches, proving the directed tensor residual and Green/boundary bootstrap; the incomplete v1 numbers remain withdrawn;
- [docs/leaky-outer-combined-row-stage3h-size.md](docs/leaky-outer-combined-row-stage3h-size.md) -- corrected v2 output-specific theorem proving strict center-guide phase-combined row sizes after one-sided seam splitting; the continuous center-density transfer is not included;
- [docs/leaky-outer-signed-density-stage3i-tv.md](docs/leaky-outer-signed-density-stage3i-tv.md) -- 192-bit event-aware continuous signed-density certificate on all 25,600 rectangles; although the auxiliary \(0.01\) candidate-row excess target fails, exact phase-fixed reduced-history row bounds \(0.550516\) and \(0.028281\) prove arbitrary-\(C^0\) linear contraction;
- [docs/leaky-outer-nonlinear-tube-stage6a.md](docs/leaky-outer-nonlinear-tube-stage6a.md) -- source-bound nonlinear outer local return and attracting-tube theorem at section radius \(r_6=10^{-335}\), full complete-history radius \(R_6=10^{-3}\), and return bound \(\Lambda_6\le0.561839\), with a \(C^2\) local event map and no earlier local-section hit; \(J=0.32\) entry, outer-side attachment, capture, routing, and onset remain open at the ambient-to-section domain-containment gate;
- [docs/leaky-biological-safety-control-contract.md](docs/leaky-biological-safety-control-contract.md) -- source-bound algebraic composition of the validated outer \((F,A)\) inverse, fixed-time wide pulse family, threshold-adapted product theorem, fixed actuator-box radius, pulse containment and Dobrushin safety erosion; v2 binds exactly six proved Stage-5C event outputs by both parent hashes, while every biological \(J_c\), stable-sign/Newton, onset, routing, capture, three-output radius and asynchronous safety value remains null or false;
- [docs/dimension-uniform-special-flow-history-graph.md](docs/dimension-uniform-special-flow-history-graph.md) -- abstract dimension-uniform special-flow graph theorem with operator-TV delays, mixed jets, logarithmic fold tubes, and exact mild history embedding; network model fitting remains separate;
- [docs/banach-scale-history-schur-link.md](docs/banach-scale-history-schur-link.md) -- three-level \(C_b^9\to C_b^8\to C_b^7\) graph-response theorem, complete-history extension/restriction, levelwise Schur formulas, and conditional trace/endpoint transfer without a false same-space \(C^2\) implicit-function theorem;
- [docs/paper-ii-lifted-two-module-class.md](docs/paper-ii-lifted-two-module-class.md) -- exact arbitrary-size unequal-module lift, maximum-norm Gate A model-fitting audit (with weighted algebra retained only as a diagnostic), dimension-independent singular semigroup bound, and operator-TV non-equitable perturbation family;
- [docs/paper-ii-arbitrary-n-blowup-model-fit.md](docs/paper-ii-arbitrary-n-blowup-model-fit.md) -- exact arbitrary-\(N\) anisotropic blow-up, full stable-fiber shift, true divisibility checks, and dimension-uniform prepared-data fit to the abstract history-graph theorem;
- [docs/paper-ii-selected-root-lift-and-symmetry-breaking.md](docs/paper-ii-selected-root-lift-and-symmetry-breaking.md) -- exact compatible-canonical selected-gap/root lift for arbitrary positive module sizes, uniform inherited root coefficient, Reynolds nullity of the pure within-module breaker, and a genuinely non-equitable nonzero combined tangent;
- [docs/paper-ii-heterogeneous-curvature-selected-root.md](docs/paper-ii-heterogeneous-curvature-selected-root.md) -- dimension-uniform, synchrony-quotient-free canonical selected-root theorem for arbitrary finite Dobrushin networks, with an explicit nonzero topology-resolvent coefficient and all-\(N\) witness;
- [docs/paper-ii-shared-resource-dobrushin-class.md](docs/paper-ii-shared-resource-dobrushin-class.md) -- a genuinely arbitrary-\(N\) one-slow-resource class with a uniform Dobrushin contraction; its prepared graph is conditional on the stated tame cutoff and its physical root response remains open;
- [docs/shared-resource-order-three-cancellation.md](docs/shared-resource-order-three-cancellation.md) -- exact projection-neutral interior cancellation through the first two physical root orders in the homogeneous shared-resource class; endpoint/root consequences remain conditional;
- [docs/general-network-schur-melnikov-proof.md](docs/general-network-schur-melnikov-proof.md) -- Gate C calculus: exact graph/gap Schur derivatives, a conditional projection-neutral cubic root theorem with explicit constants, codimension-one genericity once a nonzero witness is known, and the strict direct-sum audit;
- [docs/general-network-vector-gap-codimension.md](docs/general-network-vector-gap-codimension.md) -- abstract complete-history vector-gap theorem, codimension-\(q\) canard locus, quantitative root bounds, and the robust actuator-count obstruction \(m\ge q\); network-specific index and rank remain open;
- [docs/multiple-recovery-center-obstruction.md](docs/multiple-recovery-center-obstruction.md) -- exact \((N+1)\)-dimensional singular center and persistent \(N-1\) slow-root obstruction for standard independent recoveries; the full-history cokernel dimension remains open;
- [docs/paper-iii-physical-outer-pulse-bridge.md](docs/paper-iii-physical-outer-pulse-bridge.md) -- proved singular two-channel geometry, an explicit distinction among geometric, lower-fold-event, biological-channel, and amplitude roots, and the open or conditional outer-history, fold-map, U-CAP, and landing gates;
- [docs/paper-iii-outer-selection-blocker-and-repair.md](docs/paper-iii-outer-selection-blocker-and-repair.md) -- exact counterexample to backward-completeness as a selection rule, curve-restricted history equations, anchored flat-error estimate, repaired Gate P3-A\(^*\), and the causal reset alternative;
- [docs/paper-iii-causal-reset-separator.md](docs/paper-iii-causal-reset-separator.md) -- exact causal release history, voltage-memory overwrite and recovery non-erasure, fixed-fast-time pulse/quiet passage cylinders, and a proved nonempty reset-transition set; its former all-in-one R-S target is decomposed below;
- [docs/paper-iii-unforced-separator-stop-go.md](docs/paper-iii-unforced-separator-stop-go.md) -- exact ODE-subclass obstruction to deriving an unforced first-hit boundary from a local saddle separator and fixed-layer blocks, plus the former U-EX target repaired into a U-SF geometric root, moving-tube/lower-fold event root, and U-CAP biological boundary; it does not disprove the physical FHN separator;
- [docs/paper-iii-u-out-terminal-matching.md](docs/paper-iii-u-out-terminal-matching.md) -- exact continuation-or-exit and terminal-transfer calculus, action-supercritical matching contract, and the still-open physical terminal BVP/common-leaf/jet obligations;
- [docs/paper-iii-u-out-action-scale-closure-audit.md](docs/paper-iii-u-out-action-scale-closure-audit.md) -- proved fixed-logarithmic-chart versus fixed-action no-go, an exact complete-history ODE-subclass counterexample separating value closure from parameter-jet closure, and a robust sufficient terminal-root jet condition with its exact ratio bound;
- [docs/paper-iii-strong-unstable-history-splitting.md](docs/paper-iii-strong-unstable-history-splitting.md) -- direct delay-length-uniform forward Lyapunov--Perron theorem for a selected codimension-one relative-growth history graph and its reset covector; its physical implication is conditional on U-OUT\({}^+\), and it does not claim a phase-space trichotomy or stable foliation;
- [docs/paper-iii-unforced-geometric-separator.md](docs/paper-iii-unforced-geometric-separator.md) -- Gate U-SF theorem package: exact middle-branch action obstruction, the strengthened U-OUT\({}^+\) hypothesis, and the conditional unique selected geometric reset intersection, explicitly without a pulse/quiet outcome claim;
- [docs/paper-iii-unforced-lower-fold-exchange.md](docs/paper-iii-unforced-lower-fold-exchange.md) -- Gate U-EX stop/go theorem: proved physical lower-fold orientation and reset-to-fold action, exact Airy all-offset sign obstruction, moving slow-base/fold event repair, and the still-open physical fold-map and separate U-CAP capture/no-return gates;
- [docs/paper-iii-unforced-capture-no-return.md](docs/paper-iii-unforced-capture-no-return.md) -- Gate U-CAP stop/go theorem: physical fixed-layer detector mismatch, an exact two-attractor RFDE-subclass no-hit counterexample, a finite-deadband complete-history isolating-chain theorem, and the open global two-basin certificate;
- [docs/paper-iii-collective-clamp-separator.md](docs/paper-iii-collective-clamp-separator.md) -- exact collective-recovery-clamped saddle, one-unstable-root criterion, fixed-\(\delta\) complete-history pulse/quiet separator, deadline deadband, and explicit separation from the open unforced U-SF/U-EX/U-CAP route;
- [docs/paper-iv-canard-conditioning-no-go.md](docs/paper-iv-canard-conditioning-no-go.md) -- exact row-cancellation bound showing when amplitude and pulse-safety coordinates become exponentially ill-conditioned inside a canard window; delayed-network applicability is conditional on Paper III;
- [docs/paper-iv-periodic-rfde-adjoints.md](docs/paper-iv-periodic-rfde-adjoints.md) -- proved period/frequency, peak-envelope, distributional amplitude, and causal event adjoints for discrete-delay RFDEs, with exact synchronous-FHN specialization and an explicitly conditional three-row response target;
- [docs/paper-iv-fhn-control-no-go.md](docs/paper-iv-fhn-control-no-go.md) -- full-network modal decomposition, size-uniform transverse Halanay theorem, and sharp two-scale inverse-conditioning no-go for the declared FHN outputs under explicit root/layer hypotheses;
- [docs/paper-iv-reset-only-block-control.md](docs/paper-iv-reset-only-block-control.md) -- controlled complete-history threshold IFT, exact reset-only block-triangular response, singular-value and target-radius bounds, Hopf frequency--amplitude witness, and integration with the now-proved microscopic FHN response box;
- [docs/paper-iv-calibrated-reset-coordinate.md](docs/paper-iv-calibrated-reset-coordinate.md) -- exact local reparameterization of the raw reset preset by its complete-history gap, block-diagonal three-output response, and a quantitative product-neighborhood inverse; the periodic block is now supplied on a microscopic box, while the raw-command Jacobian and physical implementation remain gates;
- [docs/paper-iv-fhn-periodic-box-candidate.md](docs/paper-iv-fhn-periodic-box-candidate.md) -- executable synchronous two-delay FHN periodic BVP, moving-delay sensitivities, extrema/invertibility diagnostics, positive finite-sample response-box candidate, and the direct interval plus ODE-persistence proof contracts; it is explicitly not a validated interval certificate;
- [docs/paper-iv-directed-periodic-validation.md](docs/paper-iv-directed-periodic-validation.md) -- MPFR-directed proof of the exact 97-node finite collocation root and its bordered inverse, full finite Fourier-polynomial residual enclosure, tail-diagonal diagnostic, and explicit finite-stage refusal prior to the later infinite closure;
- [docs/paper-iv-infinite-periodic-validation.md](docs/paper-iv-infinite-periodic-validation.md) -- weighted real-conjugate \(M=144\) coefficient inverse, all four finite/tail block bounds, moving-delay-aware nonlinear radii polynomial, and validated center periodic RFDE orbit/phase-bordered inverse; the later parameter-box certificate builds on this center result;
- [docs/paper-iv-fredholm-monodromy-transfer.md](docs/paper-iv-fredholm-monodromy-transfer.md) -- exact moving-delay phase-border to RFDE-monodromy theorem, algebraic simplicity of the center unit multiplier, and directed local Bloch-arc exclusion;
- [docs/paper-iv-periodic-parameter-box.md](docs/paper-iv-periodic-parameter-box.md) -- MPFR-directed D1/D3/D4 proof on a nonempty microscopic two-gain box: a \(C^1\) periodic branch, unique extrema, auditable finite/tail sensitivity budgets, and response lower bound \(0.0162187\);
- [docs/paper-iv-full-floquet-parameter-box.md](docs/paper-iv-full-floquet-parameter-box.md) -- proved 319-cell unit-circle exclusion using the physically correct unshifted-coefficient/output-phase form, independently cross-checked against the equivalent shifted/input form;
- [docs/paper-iv-direct-response-target-ball.md](docs/paper-iv-direct-response-target-ball.md) -- fixed-derivative-box inverse theorem and MPFR-directed frequency--squared-range target ball on the microscopic FHN gain box, explicitly without a physical pulse-onset promotion;
- [docs/paper-iv-unsquared-amplitude-transfer.md](docs/paper-iv-unsquared-amplitude-transfer.md) -- directed exact-orbit voltage-amplitude enclosure and inverse-coordinate transfer from squared range to the physical unsquared range;
- [docs/paper-iv-same-model-clamped-separator.md](docs/paper-iv-same-model-clamped-separator.md) -- exact fixed-model recovery-clamped complete-history separator with a controlled operational first-hit interpretation;
- [docs/paper-iv-causal-hold-sign-cone.md](docs/paper-iv-causal-hold-sign-cone.md) -- causal one-delay-window history preparation principle and synchronous complete-history sign cones;
- [docs/paper-iv-bounded-additive-preparation.md](docs/paper-iv-bounded-additive-preparation.md) -- finite-time exact preparation of \(\Phi_r\) by bounded additive exact-model feedback on a bounded initial-data cylinder, without overwrite or impulse;
- [docs/paper-iv-full-network-nonlinear-sign-cone.md](docs/paper-iv-full-network-nonlinear-sign-cone.md) -- nonsynchronous nonlinear first-hit and finite-excursion theorem for arbitrary module sizes in the fixed rank-one topology;
- [docs/paper-iv-general-network-sign-cone.md](docs/paper-iv-general-network-sign-cone.md) -- topology-independent nonsynchronous first-hit and excursion theorem for arbitrary finite nonnegative balanced networks under a nodewise zero-recovery constraint;
- [docs/paper-iv-frequency-amplitude-safety-target-ball.md](docs/paper-iv-frequency-amplitude-safety-target-ball.md) -- same-model three-dimensional \((F,A,S_{\rm op})\) target balls in the two signed reset charts;
- [docs/paper-iv-balanced-general-topology-bounded-control-chain.md](docs/paper-iv-balanced-general-topology-bounded-control-chain.md) -- bounded preparation, bounded decision control, signed finite excursions, and synchronous-branch three-output target balls for every finite balanced topology in the declared class;
- [docs/paper-iv-autonomous-handoff-excursion.md](docs/paper-iv-autonomous-handoff-excursion.md) -- exact synchronized positive and negative handoff corridors on which all additive inputs are closed and the baseline delayed FHN network completes a finite excursion before the first delay update, together with the negative unit-face reversal obstruction;
- [docs/paper-iv-robust-handoff-tube.md](docs/paper-iv-robust-handoff-tube.md) -- explicit open cylinders in the full RFDE history space giving asynchronous finite-horizon terminal capture under small state/history/parameter errors and arbitrary-sign shutdown residuals for every finite balanced topology;
- [docs/paper-iv-periodic-transverse-halanay.md](docs/paper-iv-periodic-transverse-halanay.md) -- size-uniform transverse variational decay along the synchronized periodic branch for the fixed rank-one topology;
- [docs/paper-iv-dobrushin-periodic-attraction.md](docs/paper-iv-dobrushin-periodic-attraction.md) -- proved oscillation-norm transverse decay and local orbital attraction for each fixed admitted network, without a network-uniform nonlinear basin;
- [docs/quadratic-period-lock-eta-floquet-stability.md](docs/quadratic-period-lock-eta-floquet-stability.md) -- proved inherited nonzero-\(\eta\) Floquet box and its fixed-network attraction composition;
- [docs/paper-iv-synchronous-floquet-index-audit.md](docs/paper-iv-synchronous-floquet-index-audit.md) -- historical refusal/audit record subsequently superseded by the directed right-half cover;
- [docs/paper-iv-synchronous-floquet-riesz-reduction.md](docs/paper-iv-synchronous-floquet-riesz-reduction.md) -- uniform right-half-strip tail inversion, finite analytic Schur reduction preserving analytic characteristic multiplicity, outer and local complex exclusions, and the remaining finite directed-winding gate;
- [docs/paper-iv-synchronous-floquet-right-half-cover.md](docs/paper-iv-synchronous-floquet-right-half-cover.md) -- proved 32,046-leaf right-half keyhole tree in the physically correct unshifted/output form, with an independent equivalent-form regression oracle;
- [src/canard_control/fixed_epsilon_target_tilted_phase.py](src/canard_control/fixed_epsilon_target_tilted_phase.py) and [src/canard_control/fixed_epsilon_target_causal_tube_candidate.py](src/canard_control/fixed_epsilon_target_causal_tube_candidate.py) -- source-bound raw-slot no-go/comparison certificate and the separate prepared target-chart numerical/conditional-theorem ledger;
- [src/canard_control/autonomous_leaky_recovery_bistable.py](src/canard_control/autonomous_leaky_recovery_bistable.py) -- exact equilibrium characteristic algebra, rational small-gain certificate and strict analytic/candidate/open claim partition for the autonomous replacement;
- `src/canard_control/fhn_periodic_candidate.py` -- odd-Fourier BVP/continuation, analytic period column, gain sensitivities, discrete-adjoint audit, sampled box, and ODE-persistence-route diagnostics;
- `src/canard_control/directed_interval.py` and `src/canard_control/fhn_periodic_directed_validation.py` -- reusable MPFR real/complex interval arithmetic, exact finite nodal contraction, directed DFT/convolution residual bounds, inverse envelope, and machine-readable infinite-tail falsifier;
- `src/canard_control/fhn_periodic_infinite_validation.py` -- weighted independent real-conjugate coefficient Jacobian, binary-accelerated directed inverse, finite/tail cross norms, tail inverse, and moving-delay correction-ball majorant;
- [src/canard_control/leaky_periodic_branch_artifact.py](src/canard_control/leaky_periodic_branch_artifact.py) -- source-hashed inner leaky-branch polynomial replay and independently audited directed-radii proof of a phase-fixed RFDE orbit and bordered inverse, with strict refusal of Floquet promotion;
- [src/canard_control/leaky_outer_high_resolution.py](src/canard_control/leaky_outer_high_resolution.py) -- source-bound high-resolution outer polynomial ladder and directed finite/tail periodic-orbit proof contract;
- [src/canard_control/leaky_pulse_terminal_history.py](src/canard_control/leaky_pulse_terminal_history.py), [src/canard_control/leaky_pulse_separator_candidate.py](src/canard_control/leaky_pulse_separator_candidate.py), and [src/canard_control/leaky_pulse_separator_validation_target.py](src/canard_control/leaky_pulse_separator_validation_target.py) -- exact pulse-to-history orientation followed by deliberately non-directed finite-section separator discovery and a source-bound narrow validation target;
- `src/canard_control/fhn_periodic_parameter_box.py` -- uniform gain-box radii proof, RFDE-based extrema isolation, finite/tail sensitivity residual decomposition, and directed two-output response enclosure;
- `src/canard_control/rfde_floquet_transfer.py` -- theorem-evidence binding, directed local Bloch exclusion, and the historical deliberately non-certifying bare-cell bookkeeping contract;
- `src/canard_control/fhn_bloch_outer_validation.py` -- parameter-box local transfer, arbitrary-complex Bloch symbols, directed binary-product audit, exact-orbit correction budgets, and all four finite/tail cell bounds;
- `src/canard_control/fhn_response_target_ball.py` -- hash-bound directed recomputation of the fixed midpoint singular bound, derivative-family defect, contraction factor, and covered two-output target radius;
- [src/canard_control/shared_resource_root_detector_bridge.py](src/canard_control/shared_resource_root_detector_bridge.py) -- exact latency algebra, all-size witness and strict scope ledger for the one-RFDE root-linked reset policy;
- [src/canard_control/fhn_root_periodic_compatibility.py](src/canard_control/fhn_root_periodic_compatibility.py) -- exact fold, scaffold, delay-layer and actuator-direction comparison for the selected-root and periodic/control models;
- [src/canard_control/fhn_balanced_control_chain.py](src/canard_control/fhn_balanced_control_chain.py) with the bounded-preparation and separator modules -- exact-model finite-time preparation, bounded decision control, and balanced-general-topology staged composition;
- [src/canard_control/fhn_autonomous_handoff_excursion.py](src/canard_control/fhn_autonomous_handoff_excursion.py) -- exact rational phase barriers and method-of-steps clocks for the controlled-to-autonomous synchronized handoff theorem;
- [src/canard_control/fhn_robust_handoff_tube.py](src/canard_control/fhn_robust_handoff_tube.py) -- exact-rational and MPFR-directed Dini/Gronwall certificate for the open asynchronous shutdown tube;
- [src/canard_control/fhn_general_network_sign_cone.py](src/canard_control/fhn_general_network_sign_cone.py) and [src/canard_control/fhn_full_network_nonlinear_sign_cone.py](src/canard_control/fhn_full_network_nonlinear_sign_cone.py) -- balanced-general and fixed-topology nonlinear sign-cone/first-hit calculations;
- [src/canard_control/fhn_same_model_amplitude_safety.py](src/canard_control/fhn_same_model_amplitude_safety.py) with the unsquared-amplitude and three-output modules -- exact-orbit amplitude conversion and source-bound three-output target-ball composition;
- [src/canard_control/fhn_periodic_transverse_halanay.py](src/canard_control/fhn_periodic_transverse_halanay.py), [src/canard_control/fhn_synchronous_floquet_riesz_reduction.py](src/canard_control/fhn_synchronous_floquet_riesz_reduction.py), and [src/canard_control/fhn_synchronous_floquet_right_half_cover.py](src/canard_control/fhn_synchronous_floquet_right_half_cover.py) -- fixed-topology transverse decay, the rigorous infinite-to-finite spectral reduction, and the complete directed stable-index/attraction certificate; the earlier index audit remains the frozen refusal baseline;
- `experiments/fhn_periodic_box_candidate.py` with `experiments/requirements-fhn-periodic-candidate.txt` -- one-command candidate reproduction and exact NumPy/SciPy dependencies;
- `experiments/results/fhn_periodic_box_candidate.json` -- machine-readable binary64 result and software/arithmetic provenance, with all validated-interval flags set to false;
- [experiments/fixed_epsilon_target_tilted_phase.py](experiments/fixed_epsilon_target_tilted_phase.py), [experiments/fixed_epsilon_target_causal_tube_candidate.py](experiments/fixed_epsilon_target_causal_tube_candidate.py), and [experiments/autonomous_leaky_recovery_bistable_probe.py](experiments/autonomous_leaky_recovery_bistable_probe.py) -- one-command target-clock obstruction, prepared-chart candidate, and autonomous bistability/onset reproductions with strict machine-readable claim ledgers;
- `experiments/fhn_periodic_directed_validation.py` with `experiments/requirements-fhn-periodic-validation.txt` -- one-command directed finite validation and its declared gmpy2/NumPy/SciPy dependencies; the result JSON records the exact installed versions;
- `experiments/results/fhn_periodic_directed_validation.json` -- tracked directed bounds, backend/provenance audit, finite theorem flags, stage-local missing infinite-tail bounds, and RFDE refusal flags;
- `experiments/fhn_periodic_infinite_validation.py`, its requirements file, and `experiments/results/fhn_periodic_infinite_validation.json` -- one-command center-orbit infinite radii proof with remaining issue-15 flags kept false;
- `experiments/fhn_periodic_parameter_box.py` and `experiments/results/fhn_periodic_parameter_box.json` -- one-command 160-bit D1/D3/D4 parameter-box certificate and tracked theorem-gate record;
- `experiments/fhn_bloch_outer_validation.py` and `experiments/results/fhn_bloch_outer_validation.json` -- source-bound 319-cell record in the physically correct unshifted-coefficient/output-phase convention, independently checked against the equivalent shifted/input identity;
- `experiments/fhn_response_target_ball.py` and `experiments/results/fhn_response_target_ball.json` -- one-command source-bound derivation and tracked theorem record for the direct two-output target ball;
- [experiments/shared_resource_root_detector_bridge.py](experiments/shared_resource_root_detector_bridge.py) and [experiments/results/shared_resource_root_detector_bridge.json](experiments/results/shared_resource_root_detector_bridge.json) -- exact source-bound policy-transduction record; physical outer selection, input-independent onset and biological claims remain false;
- [experiments/fhn_root_periodic_compatibility.py](experiments/fhn_root_periodic_compatibility.py) and [experiments/results/fhn_root_periodic_compatibility.json](experiments/results/fhn_root_periodic_compatibility.json) -- source-bound incompatibility certificate; it rules out literal composition of the existing results, not every possible unified extension;
- [experiments/fhn_balanced_control_chain.py](experiments/fhn_balanced_control_chain.py) and [experiments/results/fhn_balanced_control_chain.json](experiments/results/fhn_balanced_control_chain.json) -- source-bound staged control record with topology-independent authority, total deadlines, and the three-output radius;
- [experiments/fhn_autonomous_handoff_excursion.py](experiments/fhn_autonomous_handoff_excursion.py) and [experiments/results/fhn_autonomous_handoff_excursion.json](experiments/results/fhn_autonomous_handoff_excursion.json) -- source-bound autonomous-handoff barriers, clocks, recovery bounds, and strict negative unit-face obstruction;
- [experiments/fhn_robust_handoff_tube.py](experiments/fhn_robust_handoff_tube.py) and [experiments/results/fhn_robust_handoff_tube.json](experiments/results/fhn_robust_handoff_tube.json) -- byte-replayable open-cylinder tracking and finite terminal-capture certificate;
- [experiments/fhn_synchronous_floquet_right_half_cover.py](experiments/fhn_synchronous_floquet_right_half_cover.py) and [experiments/results/fhn_synchronous_floquet_right_half_cover.json](experiments/results/fhn_synchronous_floquet_right_half_cover.json) -- source-bound complete dyadic right-half zero-free cover and attraction ledger;
- the matching experiment drivers and result records for bounded preparation, fixed and balanced sign cones, same-model separator/amplitude transfer, transverse Halanay decay, the synchronous stable-index audit, and the Riesz reduction;
- `docs/scope-and-theorems.md` -- frozen general-network future-work contract and its stop/go gates;
- `docs/lin-gap-feasibility.md` -- \(\mathbb R^4\) reference full-history BVP template and correct Fredholm index bookkeeping;
- `docs/full-network-lin-operator.md` -- dual-scaffold \(2N\)-state operator contract, transverse trace-index audit, modal theorem target, and voltage-only negative control;
- `docs/two-module-reference.md` -- frozen FHN benchmark and weak-only transverse obstruction;
- `docs/two-module-moment-counterexample.md` -- exact mode-closure lemma, fixed-moment range-forcing counterexample, and Perron no-go result;
- `docs/shared-recovery-moment.md` -- repaired one-slow-variable benchmark and formal nonzero transverse dynamic-adjoint coefficient, with endpoint terms exposed;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/final-model-exact-algebra.md` -- exact final-model algebra and singular Jordan structure;
- `docs/final-model-blowup.md` -- exact anisotropic fold chart and projected/full-vector residual checks;
- `docs/rfde-relevant-spectrum.md` -- Rouché--Schur count of the two relevant RFDE roots and complementary gap;
- `docs/special-flow-graph-theorem.md` -- constructive Lipschitz compact-tube history graph and injective history map;
- `docs/mixed-jet-graph-proof.md` -- finite-scale mixed-jet closure and the uniform fixed-tube Taylor remainder;
- `docs/reduced-canard-root.md` -- conditional second-order splitting template and exact symbolic integrands;
- `docs/k1-tail-compatibility.md` -- long-delay \(K_1\) obstruction and logarithmic rescue mechanism;
- `docs/long-delay-selected-trace-proof.md` -- normalized trace-to-gap calculation and root displacement;
- [docs/growing-tube-graph-proof.md](docs/growing-tube-graph-proof.md) -- frozen-cutoff logarithmic-tube graph theorem and mixed remainder;
- [docs/green-phase-selected-traces.md](docs/green-phase-selected-traces.md) -- explicit one-sided Green operators, phase normalization, and canonical trace theorem;
- [docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md) -- dependency-explicit canonical history-connection theorem, exact root law, physical-selection corollary, and audit checklist;
- [docs/outer-modal-algebra.md](docs/outer-modal-algebra.md) -- exact physical modal equations and the still-open outer-selection boundary;
- `docs/model-repair-options.md` -- comparison of the long-delay theorem with a lower-risk fixed-physical-delay variant;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/canard_control/transverse_modes.py` -- executable weak-only inner splitting audit;
- `src/canard_control/reference_fhn.py` -- exact collective algebra for the dual-scaffold two-module benchmark;
- `src/canard_control/full_network_blocks.py` -- exact finite-\(N\) collective/transverse projectors, layer residuals, and dual-scaffold singular-Jacobian audit;
- `src/canard_control/two_module_moment.py` -- exact two-layer moment/range-forcing counterexample;
- `src/canard_control/shared_recovery_moment.py` -- executable shared-recovery inner and finite-section adjoint calculations;
- `src/canard_control/final_two_module.py` -- exact final-model algebra and characteristic determinant;
- `src/canard_control/final_model_blowup.py` -- exact chart construction and scaling audit;
- `src/canard_control/nonlocal_graph_jet.py` -- symbolic invariant-graph and mixed-jet calculation;
- `src/canard_control/reduced_canard_root.py` -- conditional splitting and exact Gaussian-integral checks;
- `src/canard_control/lifted_two_module_network.py`, `src/canard_control/lifted_network_blowup.py`, and `src/canard_control/lifted_selected_root_response.py` -- exact arbitrary-size lifting, blow-up/model-fit, Reynolds, and non-equitable response audits;
- `src/canard_control/shared_resource_markov.py` -- Dobrushin contraction and one-shared-resource network identities;
- `src/canard_control/shared_resource_response.py` -- exact constant-history cancellation audit for projection-neutral shared-resource directions;
- `src/canard_control/heterogeneous_curvature_root.py` -- exact arbitrary-\(N\) curvature/resolvent root coefficient and normalized no-synchrony-quotient witness;
- `src/canard_control/block_schur_response.py` -- exact block-response and projection-neutral Schur regressions;
- `src/canard_control/physical_pulse_bridge.py` -- singular fast-channel, Sturm, section-orientation, and detector-action calculations;
- `src/canard_control/causal_reset_separator.py` -- exact causal reset, memory overwrite/non-erasure, endpoint-rank, and scalar root-transfer certificates;
- `src/canard_control/unforced_separator_obstruction.py` -- exact drifting-saddle exit-time and fixed-layer miss identities that falsify the local shortcut to an unforced first-hit separator;
- `src/canard_control/unforced_outer_tracker.py` -- causal continuation-or-exit, terminal-transfer, two-sided action-loss, and U-OUT matching-budget diagnostics;
- `src/canard_control/u_out_action_scale.py` -- logarithmic fold-chart/action-scale comparison, required chart-power audit, and independent scalar root/parameter-jet budgets;
- `src/canard_control/strong_unstable_history.py` -- exact delay-layer norm, delay-length-independent base-history coordinates, and forward Lyapunov--Perron contraction budgets;
- `src/canard_control/unforced_geometric_separator.py` -- singular reset-layer action and unstable-vector audit, logarithmic outer-error propagation, weighted Green/strong-unstable domination ledgers, and scalar geometric-separator root bound;
- `src/canard_control/unforced_lower_fold_exchange.py` -- exact rational lower-fold signs, physical middle-branch action, and underflow-safe Airy fold-boundary diagnostics;
- `src/canard_control/unforced_capture_audit.py` -- physical detector-drift location, exact saturating two-channel fixed-layer miss threshold, and finite-deadband capture-time diagnostics;
- `src/canard_control/clamped_reset_separator.py` -- collective-clamp equilibrium, unstable-index, deadline, and large-delay spectral diagnostics;
- `src/canard_control/outer_selection_coherence.py` -- exact outer-selection nonuniqueness, mixed-jet blow-up, and anchored-boundary suppression diagnostics;
- `src/canard_control/canard_conditioning.py` -- response-row cancellation, determinant shear, and inverse-conditioning bounds;
- `src/canard_control/periodic_rfde_sensitivity.py` -- discrete retarded/advanced transpose, moving-delay, periodic-response, amplitude, and causal landing-adjoint regressions;
- `src/canard_control/fhn_control_no_go.py` -- exact transverse mode decomposition, Halanay constants, response no-go bounds, and sharpness diagnostics;
- `src/canard_control/operational_control_repair.py` -- reset-only block response, quantitative inverse radius, Hopf response, and floating interval-candidate diagnostics;
- `src/canard_control/calibrated_reset_control.py` -- exact calibrated block lower-bound propagation and floating diagnostics for the block-diagonal response and product-neighborhood radius formulas;
- `src/canard_control/multiple_recovery_center.py` -- exact fold-chain, recovery-center, slow-root, and conditional linear matching-count checks;
- [src/canard_control/green_phase.py](src/canard_control/green_phase.py) -- executable tangent/normal frame and one-sided Green identities;
- [src/canard_control/outer_modal_audit.py](src/canard_control/outer_modal_audit.py) -- exact physical modal equations, branch jets, and fast-gap audit;
- `src/canard_control/exact_chart_threshold_diagnostic.py` -- literal method-of-steps integration and finite-section KS energy-gap root for the exact four-dimensional chart, explicitly diagnostic rather than a proof;
- `experiments/transverse_lin_sweep.py` -- finite-interval boundary-condition diagnostic, explicitly not an RFDE inverse certificate;
- `experiments/exact_chart_threshold_diagnostic.py` -- reproducible central-difference convergence table for the formal transverse threshold coefficient;
- `docs/exact-chart-threshold-diagnostic.md` -- archived numerical table and history/section-dependence disclaimer;
- [tests/test_green_phase.py](tests/test_green_phase.py) -- exact tangent/normal frame and one-sided Green regression tests;
- [tests/test_outer_modal_audit.py](tests/test_outer_modal_audit.py) -- physical modal algebra, branch-jet, and fast-gap regression tests;
- `tests/` -- remaining symbolic and numerical regression tests.

## Project tracking

- [Base-paper main theorem](https://github.com/h-lu/canard-aware-network-control/issues/10)
- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)
- [Paper II: general finite-network canard response](https://github.com/h-lu/canard-aware-network-control/milestone/2)
- [Paper III: physical canard to pulse onset](https://github.com/h-lu/canard-aware-network-control/milestone/3)
- [Paper IV: biological pulse-coordinate control](https://github.com/h-lu/canard-aware-network-control/milestone/4)
- [Paper II epic](https://github.com/h-lu/canard-aware-network-control/issues/4)
- [Paper III physical-selection epic](https://github.com/h-lu/canard-aware-network-control/issues/11)
- [Paper III pulse-event theorem](https://github.com/h-lu/canard-aware-network-control/issues/12)
- [Paper IV control/conditioning epic](https://github.com/h-lu/canard-aware-network-control/issues/5)
- [Paper IV periodic FHN validation](https://github.com/h-lu/canard-aware-network-control/issues/15)
- [Fixed-epsilon selected root](https://github.com/h-lu/canard-aware-network-control/issues/16)
- [Autonomous bistable slice](https://github.com/h-lu/canard-aware-network-control/issues/17)
- [Same-plant canard-to-onset comparison](https://github.com/h-lu/canard-aware-network-control/issues/18)
- [Target-amplitude interval causal graph](https://github.com/h-lu/canard-aware-network-control/issues/19)
- [Leaky-recovery periodic/Floquet validation](https://github.com/h-lu/canard-aware-network-control/issues/20)
- [History-space physical-pulse onset](https://github.com/h-lu/canard-aware-network-control/issues/21)
- [Autonomous three-output target ball and network lift](https://github.com/h-lu/canard-aware-network-control/issues/22)
- [Fixed-epsilon finite-network selected-root lift](https://github.com/h-lu/canard-aware-network-control/issues/23)

## Frozen theorem route

Route A was selected on 2026-08-22. The base paper retains the long-delay
scaling

\[
 \tau_k=\theta_k/\delta
\]

and proves an \(O(\delta^3)\) effect for the canonical local history root.
The canonical growing-graph, one-sided trace, gap, and history-lift components
of Gate D and the independent falsification audit have passed. The distinct
physical outer-selection
gate remains open and conditional on parameter-coherent full-history boundary
jets. The fixed-physical-delay variant remains only a documented fallback and
is not an active theorem target.

The general-network and pulse-control work has now been reopened as a
separate successor program. It remains outside this paper. Its primary
one-critical-mode proof route is a dimension-uniform invariant-history graph;
the full \(2N\)-state Lin--Fredholm route is retained for multiple center
directions and vector gaps.
