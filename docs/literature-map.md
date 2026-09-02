# Literature boundary and novelty audit

Search date: **2026-08-24**. This is a targeted primary-literature boundary search, not a bibliometric systematic review. It covers five intersections: delayed canards, slow--fast networks and tipping, frequency--amplitude control, noninvasive delayed feedback and excitable pulses, and DDE threshold numerics.

A companion audit dated **2026-09-02** separately asks whether published RFDE,
fast--slow, network-reduction, and observability papers identify an
experimentally measured threshold with a rigorous root of the original
system.  See
[Experimental physical meaning of roots in delayed and network dynamics](physical-root-literature-audit.md).
Its focused search finds many experimentally real thresholds and several
rigorous roots, but no example combining a natural experimental control,
a proved complete-history connection root in the original RFDE/network, and
an experimental identification theorem.

## Executive conclusion

The ingredients are individually occupied:

- delayed van der Pol/FitzHugh--Nagumo canards and high-order local thresholds;
- spectral/module reduction of network dynamics and prediction of pulsatile tipping;
- frequency--amplitude and phase--amplitude control;
- noninvasive period-delayed feedback, including experimental continuation of
  canard cycles and delayed control of excitable pulses;
- convergence of DDE collocation, periodic BVP, and local bifurcation calculations.

The search did **not** find a result showing that two delayed slow--fast
systems with the same total delayed gain and the same complete critical
projected delay measure can nevertheless have different
preparation-indexed local RFDE history-connection roots because the
transverse organization of the delay layers changes. That is the base
paper's defensible intersection. “Delay + network + oscillator control” is
not a novelty claim.

The search also did not locate a result formulating a finite delayed-network
canard as a one-dimensional complete-history RFDE matching root and proving a
dimension-uniform transfer over a declared finite-network class.  The
successor program now addresses part of that gap in two precise ways: a
heterogeneous-curvature shared-resource Dobrushin response with an explicit
topology resolvent, and a quadratic period-locked dual-scaffold root whose
canonical zero-transverse graph lifts uniformly to every admitted finite
Dobrushin topology.  Neither theorem covers arbitrary histories, closing-gap
families, multiple unslaved recovery centers, or biological onset.  The
frozen two-module JNS manuscript retains its narrower claim.  Likewise, the
search did not find a threshold-specific DDE discretization theorem that
separates Runge--Kutta, delayed-history interpolation, reduction, and root
errors.

## Closest primary literature

### A. Canard geometry and delayed slow--fast systems

| Work | What it establishes | Boundary left for this project |
|---|---|---|
| [Krupa & Szmolyan (2001)](https://doi.org/10.1006/jdeq.2000.3929) | Rigorous geometry of relaxation oscillation and exponentially narrow canard explosion in planar slow--fast ODEs. | No delays, network projection, or inverse control. |
| [Wechselberger (2012)](https://doi.org/10.1090/S0002-9947-2012-05575-9), [Desroches et al. (2012)](https://doi.org/10.1137/100791233) | General folded-singularity theory and a systematic account of canards/MMOs with multiple slow variables; a fold with one fast critical direction need not reduce the full problem to a planar scalar-root geometry. | These finite-dimensional results motivate, but do not prove, the endpoint/Fredholm conditions needed to remove transverse recovery directions in an RFDE network. |
| [Chicone (2003)](https://doi.org/10.1016/S0022-0396(02)00148-1) | Finite-dimensional inertial/slow manifolds and expansions for equations with small delays. | Small-delay regime, not weak feedback with \(\tau=O(\varepsilon^{-1/2})\). |
| [Krupa & Touboul (2016a)](https://doi.org/10.1007/s10884-015-9478-2), [(2016b)](https://doi.org/10.1007/s00332-015-9268-3) | General DDE canard-explosion results plus canards, mixed-mode oscillations, bursting, and delay-dependent structure in delayed FitzHugh--Nagumo. | No network transfer or certified high-order threshold expansion. |
| [Avitabile et al. (2020)](https://doi.org/10.1137/19M1306610) | Local center-manifold theory for spatio-temporal canards with infinite-dimensional fast dynamics, including DDE settings. | Does not transfer the global/section maximal-canard root or quantify a finite-network residual. |
| [Palmer (1984)](https://doi.org/10.1016/0022-0396(84)90082-2), [Lin (1986)](https://doi.org/10.1016/0022-0396(86)90048-3), [Hale & Lin (1986)](https://doi.org/10.1016/0022-0396(86)90032-X), [Hupkes & Verduyn Lunel (2009)](https://doi.org/10.1512/iumj.2009.58.3661) | Exponential-dichotomy/Fredholm foundations and finite-dimensional Lin bifurcation equations for functional differential equations. | Lin reduction in an RFDE/MFDE is not new. The missing result is the singular canard-limit index/inverse estimate and dynamic-adjoint response to a finite-network residual. |
| [Hale & Verduyn Lunel (1993)](https://doi.org/10.1007/978-1-4612-4342-7), [Walther (2003)](https://doi.org/10.1016/j.jde.2003.07.001), [Nishiguchi (2019)](https://doi.org/10.14232/ejqtde.2019.1.91) | RFDE phase spaces and invariant manifolds; classical solution manifolds; Sobolev-history smooth dependence on a discrete delay using translation differentiability in \(L^p\). | These results force the project to distinguish the natural \(C^0\) semiflow from the strong orbit space used for moving-delay derivatives; they do not supply a canard BVP's \(C^2\) uniform constants. |
| [Zhang et al. (2026)](https://doi.org/10.1137/24M1696548) | High-order critical parameter and critical canard manifold for weakly coupled delayed van der Pol via a nonlocal center manifold and nonlinear time transformation. | Single delayed oscillator; no heterogeneous network, inverse design, or numerical threshold certificate. |
| [Jardón-Kojakhmetov & Kuehn (2022)](https://doi.org/10.1007/s10883-021-09553-2) | Feedback stabilization/control of prescribed canard cycles in blow-up coordinates. | “Control a canard” is occupied; no delayed network or independent frequency--amplitude--safety assignment. |

### B. Network canards, tipping, and reduction

| Work | What it establishes | Boundary left for this project |
|---|---|---|
| [Ambrosio & Aziz-Alaoui (2012)](https://doi.org/10.1016/j.camwa.2012.01.056), [Cebrián-Lacasa et al. (2024)](https://doi.org/10.1016/j.physrep.2024.09.014) | Coupled/reaction--diffusion FitzHugh--Nagumo systems and synchronization are established model classes; the survey explicitly records discrete coupling in both activator and recovery components as an FHN variant. | Supports the biological/mathematical legitimacy of the fixed dual-state scaffold, but supplies no canard Lin-gap, delayed threshold transfer, or singular inverse estimate. The scaffold architecture is not a novelty claim. |
| [Laurence et al. (2019)](https://doi.org/10.1103/PhysRevX.9.011042) | Spectral dimension reduction with eigenvector-weighted network observables. | General trajectory/bifurcation approximation, not a nonhyperbolic splitting-root bound. |
| [Thibeault et al. (2020)](https://doi.org/10.1103/PhysRevResearch.2.043215) | Multi-dimensional reduction for modular/heterogeneous network dynamics. | No slow--fast canard threshold transfer theorem. |
| [Masuda & Kundu (2022)](https://doi.org/10.1103/PhysRevResearch.4.023257) | Leading and non-leading spectral observables can differ materially in state and bifurcation accuracy. | Motivates an explicit observable-projection error but does not provide one for canards. |
| [Qin & Lin (2023)](https://doi.org/10.1103/PhysRevResearch.5.043209) | Perron-weighted reduction predicts pulsatile-oscillation tipping in neural, genetic, and ecological slow--fast networks. | Closest scientific competitor; no delay, full/reduced splitting-root error, or three-output control. |
| [Bonetto & Jardón Kojakhmetov (2024)](https://doi.org/10.3934/nhm.2024058) | Rigorous local/maximal canards on nonlinear diffusion/consensus networks under graph assumptions. | Network maximal-canard existence is occupied; the singularity is consensus/transcritical, without delay or low-rank output transfer. |
| [Balzer et al. (2024)](https://doi.org/10.1103/PhysRevLett.133.237401) | Sequential canard cascading in adaptively mean-field-coupled laser networks. | “First canard cascade” is unavailable; no fixed-topology delayed biological threshold-error result. |
| [Ma et al. (2023)](https://arxiv.org/abs/2308.11666) | Community-based reduction numerically predicts states and tipping in heterogeneous delayed networks. | Delayed modular tipping reduction is occupied numerically; no GSPT splitting or uniform error. |
| [Eldo, Rakshit & Masuda (2025/2026)](https://arxiv.org/abs/2503.17268) | Rigorous graphon dynamics and convergence properties of a weighted low-dimensional approximation. | Finite-time/graphon convergence does not imply a nonhyperbolic canard-root transfer. |
| [Bramburger & Holzer (2023)](https://doi.org/10.1137/21M1455875) | Spectral-gap-dependent transfer of ordinary pattern-forming bifurcations from graphons to random finite networks. | A useful proof template, but the invertible/ordinary bifurcation setting excludes canard splitting. |
| [Liu et al. (2026)](https://doi.org/10.1103/qvlk-6df6) | Reduction, data-driven prediction, and circuit validation for the onset of oscillations in networks with delayed feedback. | Generic delayed oscillation onset is occupied; it is not the slow--fast large-pulse canard threshold. |

### C. Frequency--amplitude and phase--amplitude control

| Work | What it establishes | Boundary left for this project |
|---|---|---|
| [Ge et al. (2014)](https://doi.org/10.1103/PhysRevE.90.022909) | Feedback construction for amplitude or frequency modulation in finite-dimensional oscillators, including coupled FitzHugh--Nagumo examples. | No simultaneous canard safety coordinate or delayed threshold uncertainty. |
| [Wilson & Moehlis (2016)](https://doi.org/10.1103/PhysRevE.94.052213) | Isostable reduction retains transverse relaxation information near periodic orbits. | Isostable amplitude is not automatically an experimental peak-to-peak observable; hyperbolicity deteriorates near canards. |
| [Kotani et al. (2020)](https://doi.org/10.1103/PhysRevResearch.2.033106) | Nonlinear phase--amplitude reduction for delay-induced oscillations in an infinite-dimensional DDE phase space. | Existing hyperbolic delayed limit cycle, not slow--fast nonhyperbolic threshold transfer or network inverse design. |
| [Qin, Zhao & Lin (2021)](https://doi.org/10.1038/s41467-021-26182-2) | Joint frequency--amplitude coordination and energy optimization for biological oscillators. | Two-output Hopf/oscillation design; no delay, network canard, or third safety output. |
| [Zhong, Lin & Qin (2023)](https://doi.org/10.1103/PhysRevLett.131.138401) | Noncomputational nonlinear interventions that decouple frequency and amplitude. | Does not address the conditioning and safety margin of an exponentially narrow canard window. |
| [Mircheski, Zhu & Nakao (2023)](https://doi.org/10.1063/5.0161119) | Collective phase--amplitude reduction and optimal phase locking of oscillator networks. | Objective is locking/transverse suppression, not independent \((F,R,\Delta_c)\) assignment. |

### D. DDE computation and threshold bias

| Work | What it establishes | Boundary left for this project |
|---|---|---|
| [Engelborghs et al. (2001)](https://doi.org/10.1137/S1064827599363381) and [Engelborghs, Luzyanina & Roose (2002)](https://doi.org/10.1145/513001.513002) | Periodic-solution collocation and practical DDE-BIFTOOL bifurcation analysis. | General solvers do not supply an RFDE Lin-gap root uncertainty budget. |
| [Andò & Breda (2020)](https://doi.org/10.1137/19M1295015) | Convergence of collocation for periodic solutions of retarded functional differential equations. | Constants are not shown uniform in the singular canard limit; no splitting-root perturbation. |
| [de Wolff et al. (2021)](https://doi.org/10.1137/20M1347577) | Pseudospectral convergence of DDE Hopf bifurcation data. | Positive precedent for local bifurcation transfer, but maximal canards require fold passage and manifold matching. |
| [Andò & Sieber (2025)](https://doi.org/10.1137/24M1711182) | Expected-order collocation convergence for functional BVPs with state-dependent delays under mild differentiability. | Local regularity/invertibility constants may deteriorate near a canard; no threshold-specific estimate. |
| [Xu et al. (2026)](https://doi.org/10.1016/j.chaos.2026.118690) | A linear \(\theta\)-method preserves the DDE Bogdanov--Takens structure, but even the trapezoidal rule generally shifts its branches only with first-order accuracy. | Shows that bifurcation-type preservation and critical-parameter accuracy differ; does not treat a maximal-canard splitting root. |
| [Lu (2026)](https://arxiv.org/abs/2608.04304) | For the exact fixed-step RK map of planar slow--fast ODEs, the local threshold functional selects the chain-tree order-three defect and gives a quantitative maximal-canard shift. | No DDE history interpolation, delay quadrature, center-manifold truncation, or network projection. |

### E. Noninvasive delayed feedback and excitable pulses

| Work | What it establishes | Boundary left for this project |
|---|---|---|
| [Pyragas (1992)](https://doi.org/10.1016/0375-9601(92)90745-8) | Introduces current-minus-one-period delayed feedback that vanishes on the distinguished periodic orbit. | Establishes the noninvasive control principle, not a complete-history canard-root response, a network theorem, or independent frequency--amplitude--threshold assignment. |
| [Sieber & Krauskopf (2007)](https://doi.org/10.1142/S0218127407018646) | Embeds time-delayed difference feedback in control-based continuation and computes the canard family of the forced van der Pol system. | Uses noninvasive feedback to continue/stabilize periodic orbits; it does not prove that an orbit-annihilating channel shifts a selected RFDE canard root while leaving two periodic outputs fixed. |
| [Jardón-Kojakhmetov & Kuehn (2022)](https://doi.org/10.1007/s10883-021-09553-2) | Designs blow-up-based feedback controllers that stabilize prescribed planar canard cycles. | No delayed finite network, complete-history Lin gap, or three-output inverse theorem. |
| [Schneider, Schöll & Dahlem (2009)](https://doi.org/10.1063/1.3096411) | Studies onset and suppression of travelling pulses in an excitable FitzHugh--Nagumo reaction--diffusion model under nonlocal or time-delayed feedback. | Pulse-onset control is occupied, but not as a rigorous selected-history canard root with a quantified basin/event factorization and independent periodic outputs. |
| [Schöll et al. (2009)](https://doi.org/10.1098/rsta.2008.0258) | Analyses delayed-feedback control of synchronization and oscillatory regimes in coupled FitzHugh--Nagumo neurosystems. | No canard-root transfer, full-history onset separator, or local surjectivity of frequency--amplitude--safety outputs. |

The period-locked channel should therefore be positioned
as a **Pyragas-type noninvasive carrier**, not as the invention of delayed
difference feedback.  Its prospective new content is narrower and more
mathematical: a fold-centered nonlinear difference that is exactly zero on a
validated periodic orbit but has a nonzero selected canard-gap jet.  The
linear difference does not supply that result; its first singular Melnikov
candidate cancels by parity.  The quadratic carrier's exact model fit and
fixed-scaled-support complete-history remainder are now proved for sufficiently
small \(\delta\).  What remains a theorem target is the common operating value
\(\varepsilon=1/5\) and the input-independent physical onset comparison.  A
separate uniform Dobrushin zero-graph theorem now supplies canonical
full-network root uniqueness in its anisotropic retained tube; it does not
provide arbitrary-history or basin uniqueness.  At the exact center gain
pair, a further full right-half replay proves that this same noninvasive
carrier preserves local full-network periodic attraction on the explicit box
\(|\eta|\le3\times10^{-6}\) for every finite
\(\tau(Q)\le1/4\) topology.  This is a fixed-gain eta box, not a joint gain
continuation or a pulse-basin theorem.  Thus the defensible novelty is
the combination of orbit noninvasiveness, fold-linear invisibility, a nonzero
preparation-indexed root jet, and its dimension-uniform lift to one genuine
finite-network class, together with a rigorously nonempty stability-preserving
actuator interval, not period-delayed feedback itself.

## Claims that must not appear

The manuscript must not claim:

- the first network canard or network pulsatile-tipping prediction;
- the first rigorous maximal canard on a network;
- the first delayed van der Pol/FitzHugh--Nagumo canard expansion;
- the first delayed-network dimension reduction or oscillation threshold;
- the first canard control, frequency--amplitude control, or collective phase--amplitude control;
- the first noninvasive period-delayed feedback or delayed control of an
  excitable pulse;
- the first canard cascade or sequential recruitment phenomenon;
- graphon convergence alone as evidence of canard-threshold convergence.

## Frozen base-paper claim and proved successor scope

The current defensible claim is:

> For the frozen two-module FitzHugh--Nagumo RFDE and every fixed admissible
> canonical preparation, redistributing two delay layers in a direction that
> preserves the total gain and the complete critical projected delay measure
> changes the local complete-history connection root by
> \(K(\theta_0-\theta_1)\delta^3\eta/(4\alpha)\), with the stated uniform
> remainder.

The preparation-indexed theorem, its exact scope, and its distinction from a
physical outer maximal canard are stated in
[canonical-long-delay-theorem.md](canonical-long-delay-theorem.md).

The successor finite-network project now proves the abstract transfer form

\[
d_N=d_0+D_{\mathcal R}d_0[\mathcal R_N]
+O(C_\varepsilon\Delta_N^2),
\qquad
|\mu_{c,N}-\mu_{c,0}|
\le
\frac{C_\varepsilon}{m_\varepsilon}\Delta_N.
\]

on declared one-critical-mode classes, and separately proves the exact
quadratic canonical zero-graph lift with an \(N\)-uniform
\(-\Theta_*\delta^3\eta/2\) coefficient.  The residuals expose network
weights, delay measures, and node heterogeneity in norms compatible with
delay translation.  The decisive inputs are transverse RFDE semigroup/graph
bounds and complete-history simple-root estimates; an adjacency spectral gap
alone is not accepted as evidence.  These results do not solve the
multiple-center/vector-gap case, the fixed-\(\varepsilon=1/5\) selected root,
or physical onset.

## Terminology correction

A true maximal-canard parameter is a geometric property of the dynamical system and need not depend on the measuring instrument. Therefore:

- use **maximal-canard threshold** only when all Lin matching conditions vanish and the selected invariant manifolds intersect;
- use **Lin-gap root** while proving the one-dimensional matching theorem;
- use **projected output root** for a zero of an arbitrary scalar projection, without identifying it with a canard;
- use **output-event threshold** for a detector-defined amplitude/pulse event.

If the geometric mismatch is genuinely one-dimensional, every projection that does not annihilate that direction has the same root. If different observables produce different roots, they are output-dependent events and require a separate link to pulse onset. Non-smooth order-statistic outputs (first node, all nodes, or a \(q\)-fraction) remain numerical extensions.

## Frozen future numerical-certificate problem

For a method-of-steps calculation, expect a decomposition of the form

\[
\widehat\mu_c-\mu_c
=\Delta_{\rm RK}
+\Delta_{\rm history}
+\Delta_{\rm delay\;quadrature/collocation}
+\Delta_{\rm reduction}
+\Delta_{\rm CM\;truncation}
+\Delta_{\rm interaction}.
\]

The RK chain-tree condition may eliminate only \(\Delta_{\rm RK}\).
Dense-output/history interpolation depends on its own coefficients and on the
fractional delay phase \(\{\tau/\Delta t\}\), so it needs a separate order
condition or a residual-based bound. This certificate belongs to the frozen
finite-network promotion, not the current canonical theorem. The present
base paper uses only a literal method-of-steps asymptotic diagnostic as
falsification evidence and does not promote it to a numerical root theorem.

## Reusable public baselines

- [Zhang et al. delayed-canard reproduction package](https://doi.org/10.5281/zenodo.17051267)
- [RK chain-tree threshold-shift reproduction package](https://doi.org/10.5281/zenodo.21925148)
- [DDE-BIFTOOL](https://github.com/DDE-BifTool/DDE-Biftool)
- [PeriodicNormalizationDDEs.jl](https://github.com/mmbosschaert/PeriodicNormalizationDDEs)

These baselines should be pinned by version and treated as independent comparators rather than copied into the implementation.
