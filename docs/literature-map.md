# Literature boundary and novelty audit

Search date: **2026-08-22**. This is a targeted primary-literature boundary search, not a bibliometric systematic review. It covers four intersections: delayed canards, slow--fast networks and tipping, frequency--amplitude control, and DDE threshold numerics.

## Executive conclusion

The ingredients are individually occupied:

- delayed van der Pol/FitzHugh--Nagumo canards and high-order local thresholds;
- spectral/module reduction of network dynamics and prediction of pulsatile tipping;
- frequency--amplitude and phase--amplitude control;
- convergence of DDE collocation, periodic BVP, and local bifurcation calculations.

The search did **not** find a result that formulates a finite delayed-network canard as a one-dimensional RFDE Lin-matching root and transfers that root from an exact equitable reference system to a structurally perturbed finite network with an explicit first variation, transverse inverse bound, and second-order remainder. It also did not find a threshold-specific DDE discretization theorem that separates Runge--Kutta, delayed-history interpolation, reduction, and root errors.

This is the paper's defensible intersection. “Delay + network + oscillator control” is not a novelty claim.

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

## Claims that must not appear

The manuscript must not claim:

- the first network canard or network pulsatile-tipping prediction;
- the first rigorous maximal canard on a network;
- the first delayed van der Pol/FitzHugh--Nagumo canard expansion;
- the first delayed-network dimension reduction or oscillation threshold;
- the first canard control, frequency--amplitude control, or collective phase--amplitude control;
- the first canard cascade or sequential recruitment phenomenon;
- graphon convergence alone as evidence of canard-threshold convergence.

## Precise gap and claim

The defensible target is:

> For a finite delayed slow--fast network that is a controlled perturbation of an exact equitable reference system with one canard matching direction, formulate a one-dimensional RFDE Lin gap and derive its structural first variation and root shift with an explicit transverse Green/Fredholm inverse bound.

An appropriate first-order form is

\[
d_N=d_0+D_{\mathcal R}d_0[\mathcal R_N]
+O(C_\varepsilon\Delta_N^2),
\qquad
|\mu_{c,N}-\mu_{c,0}|
\le
\frac{C_\varepsilon}{m_\varepsilon}\Delta_N.
\]

The residual should expose network weights, delay measures, and node heterogeneity in a norm compatible with delay translation. The decisive constant is a transverse RFDE Green/Fredholm inverse bound \(G_\perp(\varepsilon)\); an adjacency spectral gap alone is not a substitute. If a delay-moment term of order \(\varepsilon^{3/2}\) is claimed, the joint limit must make the transfer remainder smaller than that term.

## Terminology correction

A true maximal-canard parameter is a geometric property of the dynamical system and need not depend on the measuring instrument. Therefore:

- use **maximal-canard threshold** only when all Lin matching conditions vanish and the selected invariant manifolds intersect;
- use **Lin-gap root** while proving the one-dimensional matching theorem;
- use **projected output root** for a zero of an arbitrary scalar projection, without identifying it with a canard;
- use **output-event threshold** for a detector-defined amplitude/pulse event.

If the geometric mismatch is genuinely one-dimensional, every projection that does not annihilate that direction has the same root. If different observables produce different roots, they are output-dependent events and require a separate link to pulse onset. Non-smooth order-statistic outputs (first node, all nodes, or a \(q\)-fraction) remain numerical extensions.

## Numerical subproblem embedded in the flagship paper

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

The RK chain-tree condition may eliminate only \(\Delta_{\rm RK}\). Dense-output/history interpolation depends on its own coefficients and on the fractional delay phase \(\{\tau/\Delta t\}\), so it needs a separate order condition or a residual-based bound. This is a supporting validation section of the flagship paper, not a second manuscript or a new RK theorem.

## Reusable public baselines

- [Zhang et al. delayed-canard reproduction package](https://doi.org/10.5281/zenodo.17051267)
- [RK chain-tree threshold-shift reproduction package](https://doi.org/10.5281/zenodo.21925148)
- [DDE-BIFTOOL](https://github.com/DDE-BifTool/DDE-Biftool)
- [PeriodicNormalizationDDEs.jl](https://github.com/mmbosschaert/PeriodicNormalizationDDEs)

These baselines should be pinned by version and treated as independent comparators rather than copied into the implementation.
