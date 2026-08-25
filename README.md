# Long-delay shifts of local canard connections

Research repository for the JNS manuscript:

> **Long-Delay Shifts of Local Canard Connections in Retarded Fast--Slow
> Systems**

The complete LaTeX manuscript, figures, appendices, cover letter, and
submission checklist are in [manuscript/jns](manuscript/jns).  The supporting
research design is [docs/flagship-research-design.md](docs/flagship-research-design.md).
General finite-network transfer and three-coordinate control are an active
successor program, but remain outside and are not claims of this paper.

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
   two-gain box. A direct unbordered full-complex Fourier proof now validates
   319 connected Bloch cells and excludes every nontrivial unit-circle
   multiplier uniformly on that box, with maximum contraction
   \(q_*\leq0.7026326<1\). A subsequent directed right-half cover has now
   certified 32,046 dyadic leaves with no pending cell and worst contraction
   \(0.9949969735<1\). Together with the simple translation multiplier, this
   proves zero synchronous nontranslation unstable index and local orbital
   attraction with asymptotic phase on the microscopic box. The same
   fixed-matrix enclosure of the two-output derivative
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
   certificate, first gives local full-network orbital attraction for each
   fixed finite pair of module sizes in the fixed rank-one two-module
   topology.  A second oscillation-norm theorem removes that rank-one
   restriction: on the \(\eta=0\) slice, every finite nonnegative balanced
   topology with \(\tau(Q)\le1/4\) has uniform transverse decay rate \(0.007\)
   and, for each fixed network, local nonlinear orbital attraction with
   asymptotic phase.  At the exact center gain pair, a separate full
   32,046-leaf replay extends this conclusion to the quadratic carrier box
   \(|\eta|\le3\times10^{-6}\): the reference orbit is unchanged, its unit
   multiplier remains algebraically simple, and all other multipliers remain
   strictly inside the unit disk.  No topology-uniform nonlinear basin,
   weaker-mixing family, or joint gain--\(\eta\) box is claimed.
   The logarithmic Floquet Riesz reduction and the complete directed cover
   prove the corresponding exact Schur winding to be zero by zero-freedom,
   rather than by an uncertified determinant-phase calculation. An exact
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
   now also has a directed nonzero Floquet box
   \(|\eta|\le3\times10^{-6}\).  Every one of the 32,046 parent right-half
   leaves is recomputed before the eta perturbation is added; the tight total
   contraction is \(0.999520249586\ldots<1\).  Because the carrier has zero
   pure-transverse first variation, this gives local orbital attraction for
   every fixed finite balanced topology with \(\tau(Q)\le1/4\).  This is a
   stability theorem for the exact center gain pair, not a proof that the
   fixed-\(\varepsilon\) selected canard-root derivative is nonzero.
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
   the exact delayed C4 patch.  The second method step \((1,3]\), late cross
   separation, and enlarged collar remain open.  The glued embedding, trace
   pair, Fredholm inverse and selected root therefore remain open.
10. **Autonomous biological-onset route.**  A leaky-recovery replacement
   keeps the two delayed voltage channels and gives a unique quiet
   equilibrium that is proved locally exponentially stable for every pair of
   positive delays.  Directed finite/tail radii arguments now validate both
   a phase-fixed inner periodic RFDE orbit and a distinct phase-fixed outer
   periodic RFDE orbit, together with their phase-bordered derivatives.  The
   inner proof uses 129 nodes and cutoff 192; the formerly under-resolved
   outer branch uses 257 nodes and cutoff 384.  Neither orbit has yet been
   assigned a rigorous Floquet index.  Binary64 finite monodromy matrices
   still indicate one and zero nontranslation unstable multipliers,
   respectively.  Under directed Floquet,
   history-space routing and pulse-transversality hypotheses, the exact
   block-triangular theorem makes
   \((a,\kappa_3,J)\mapsto(F,A,J-J_c)\) a local diffeomorphism whenever the
   two-output response is nonsingular.  The physical one-unit pulse has an
   exact jointly smooth terminal-history map
   $J\mapsto K(J)\in C([-5\sqrt5,0],\mathbb R^2)$; its stimulus tangent is
   componentwise positive on the newly written part of the history, making
   the pulse curve an oriented embedding.  A source-bound finite-section
   shooting calculation then locates
   $J_{\rm sep}^{\rm num}\simeq0.301135337086902$: third-return roots agree
   over 120, 180, and 240 history meshes to $3.3\times10^{-15}$, an
   independent DOP853 refinement ladder spans $5.3\times10^{-15}$, and the
   multiplier-scaled derivative stays near $-3.449$.  These are numerical
   stable-separator diagnostics, not a Floquet covector, stable-manifold,
   routing, threshold, or onset proof.  The response determinant,
   finite-network basin lift and equality of a canard root with physical
   onset also remain open.
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
- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- [docs/general-network-canard-pulse-control-program.md](docs/general-network-canard-pulse-control-program.md) -- active successor program: arbitrary finite-\(N\) one-fold history graphs, vector-gap extension, physical pulse onset, and quantitative three-output control/no-go gates;
- [docs/flagship-general-network-biological-control-synthesis.md](docs/flagship-general-network-biological-control-synthesis.md) -- theorem-level synthesis of the proved Dobrushin selected-root response and the balanced-network bounded staged control theorem, with the missing same-model biological interface kept explicit;
- [docs/general-network-one-gap-root-transfer.md](docs/general-network-one-gap-root-transfer.md) -- dimension-uniform scalar root-transfer theorem with quantitative radius and remainder, a concrete shared-resource Dobrushin instance, and the conditional/open dual-state Lin neighborhood separated;
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
- [docs/fixed-epsilon-target-first-step-cover.md](docs/fixed-epsilon-target-first-step-cover.md) -- rigorous 8,000-cell Picard--Bernstein cover of the full first physical method step \([-3,1]\times[-1/20,1/20]\), including the delayed C4 patch and a separate same-kernel replay at 256-bit precision; the second method step and glued chart remain open;
- [docs/fixed-epsilon-selected-attracting-endpoint-chart.md](docs/fixed-epsilon-selected-attracting-endpoint-chart.md) -- finite-mesh attracting-endpoint audit, now explicitly superseded at the continuous level by the sliding-window/\(W^{1,p}\) correction;
- [docs/fixed-epsilon-selected-fredholm-structure.md](docs/fixed-epsilon-selected-fredholm-structure.md) -- earlier projected-history coordinate audit plus the corrected natural full-history \(W^{1,p}\) ledger, with actual trace-range closedness, cokernel and inverse still open;
- [docs/fixed_epsilon_selected_repelling_endpoint.md](docs/fixed_epsilon_selected_repelling_endpoint.md) -- exact same-current, same-exit and compatible-history counterexamples, together with the superseding reduction from a history-chart PDE to one independently selected orbit;
- [docs/quadratic-physical-onset-capture-stop-go.md](docs/quadratic-physical-onset-capture-stop-go.md) -- exact four-gate non-composition theorem plus a same-plant, arbitrary-finite-balanced controlled terminal transfer for an explicit strict small-\(|\eta|\) bound, with onset/basin/no-return claims refused;
- [docs/quadratic-reference-slice-dual-basin-no-go.md](docs/quadratic-reference-slice-dual-basin-no-go.md) -- exact Rouché proof that the reference synchronous rest state is unstable on a nonzero \(\eta\)-box, periodic-orbit face-recurrence obstruction to permanent detector-side residence, and the separated autonomous-bistable, latch, and hybrid-switch repair contracts;
- [docs/autonomous-leaky-recovery-bistable-rfde-proposal.md](docs/autonomous-leaky-recovery-bistable-rfde-proposal.md) -- leaky-recovery two-delay RFDE and conditional autonomous frequency--amplitude--onset theorem; the quiet equilibrium, two center periodic orbits and oriented pulse-history curve are now proved, while Floquet, routing and onset remain open;
- [docs/leaky-periodic-finite-tail-floquet-contract.md](docs/leaky-periodic-finite-tail-floquet-contract.md) -- equation-level finite/tail and Floquet contract for leaky recovery, including the terms that differ from the nonleaky validator and the remaining spectral gates;
- [docs/leaky-periodic-majorant-audit.md](docs/leaky-periodic-majorant-audit.md) -- independent operator and majorant proof for the leaky recovery term, closing the inner periodic-orbit and phase-bordered-inverse radii theorem while leaving all Floquet claims open;
- [docs/leaky-outer-high-resolution-artifact.md](docs/leaky-outer-high-resolution-artifact.md) -- 129/193/257/385-node outer resolution ladder and a 257-node, cutoff-384 directed-radii theorem for the outer phase-fixed periodic RFDE orbit, without an attraction claim;
- [docs/leaky-pulse-terminal-history.md](docs/leaky-pulse-terminal-history.md) -- exact reduction of the one-unit physical pulse to a parameter ODE before either delay returns, with a jointly smooth, injective, positively oriented curve of complete terminal histories;
- [docs/leaky-pulse-separator-candidate.md](docs/leaky-pulse-separator-candidate.md) -- source-bound three-mesh, three-return finite-section shooting candidate near $J=0.301135337086902$, with a separate integration-refinement ladder and every stable-manifold/onset flag kept false;
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
- [docs/paper-iv-full-floquet-parameter-box.md](docs/paper-iv-full-floquet-parameter-box.md) -- parameter-box unit-root transfer and 319 direct unbordered full-complex finite/tail Bloch cells proving uniform synchronous orbital hyperbolicity, explicitly without attraction or full-network stability;
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
- [docs/paper-iv-dobrushin-periodic-attraction.md](docs/paper-iv-dobrushin-periodic-attraction.md) -- oscillation-norm Halanay lift giving uniform transverse decay and fixed-network local nonlinear orbital attraction on the \(\eta=0\), \(\tau(Q)\le1/4\) balanced Dobrushin class;
- [docs/quadratic-period-lock-eta-floquet-stability.md](docs/quadratic-period-lock-eta-floquet-stability.md) -- full 32,046-leaf base-contraction replay and active-horizon power-compact Floquet bridge proving an explicit nonzero-\(\eta\) local-attraction box at the exact center gain pair for every finite \(\tau(Q)\le1/4\) balanced topology;
- [docs/paper-iv-synchronous-floquet-index-audit.md](docs/paper-iv-synchronous-floquet-index-audit.md) -- frozen refusal certificate that isolated the formerly missing stable-index anchor; the later right-half cover closes that gate without rewriting the audit;
- [docs/paper-iv-synchronous-floquet-riesz-reduction.md](docs/paper-iv-synchronous-floquet-riesz-reduction.md) -- uniform right-half-strip tail inversion, finite analytic Schur reduction preserving analytic characteristic multiplicity, outer and local complex exclusions, and the remaining finite directed-winding gate;
- [docs/paper-iv-synchronous-floquet-right-half-cover.md](docs/paper-iv-synchronous-floquet-right-half-cover.md) -- complete 32,046-leaf directed keyhole cover, exact zero winding deduced from zero-freedom, zero nontranslation unstable index, synchronous local attraction, and fixed-rank-one full-network attraction after the transverse theorem is composed;
- [src/canard_control/fixed_epsilon_target_tilted_phase.py](src/canard_control/fixed_epsilon_target_tilted_phase.py) and [src/canard_control/fixed_epsilon_target_causal_tube_candidate.py](src/canard_control/fixed_epsilon_target_causal_tube_candidate.py) -- source-bound raw-slot no-go/comparison certificate and the separate prepared target-chart numerical/conditional-theorem ledger;
- [src/canard_control/autonomous_leaky_recovery_bistable.py](src/canard_control/autonomous_leaky_recovery_bistable.py) -- exact equilibrium characteristic algebra, rational small-gain certificate and strict analytic/candidate/open claim partition for the autonomous replacement;
- `src/canard_control/fhn_periodic_candidate.py` -- odd-Fourier BVP/continuation, analytic period column, gain sensitivities, discrete-adjoint audit, sampled box, and ODE-persistence-route diagnostics;
- `src/canard_control/directed_interval.py` and `src/canard_control/fhn_periodic_directed_validation.py` -- reusable MPFR real/complex interval arithmetic, exact finite nodal contraction, directed DFT/convolution residual bounds, inverse envelope, and machine-readable infinite-tail falsifier;
- `src/canard_control/fhn_periodic_infinite_validation.py` -- weighted independent real-conjugate coefficient Jacobian, binary-accelerated directed inverse, finite/tail cross norms, tail inverse, and moving-delay correction-ball majorant;
- [src/canard_control/leaky_periodic_branch_artifact.py](src/canard_control/leaky_periodic_branch_artifact.py) -- source-hashed inner leaky-branch polynomial replay and independently audited directed-radii proof of a phase-fixed RFDE orbit and bordered inverse, with strict refusal of Floquet promotion;
- [src/canard_control/leaky_outer_high_resolution.py](src/canard_control/leaky_outer_high_resolution.py) -- source-bound high-resolution outer polynomial ladder and directed finite/tail periodic-orbit proof contract;
- [src/canard_control/leaky_pulse_terminal_history.py](src/canard_control/leaky_pulse_terminal_history.py) and [src/canard_control/leaky_pulse_separator_candidate.py](src/canard_control/leaky_pulse_separator_candidate.py) -- exact pulse-to-history orientation followed by a deliberately non-directed finite-section stable-separator target;
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
- `experiments/fhn_bloch_outer_validation.py` and `experiments/results/fhn_bloch_outer_validation.json` -- parallel one-command 160-bit positive-arc cover, all 319 cell ledgers, exact \(\pi\) coverage, and the uniform synchronous orbital-hyperbolicity theorem record;
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
