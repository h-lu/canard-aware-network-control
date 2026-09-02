# Experimental physical meaning of roots in delayed and network dynamics

Search date: **2026-09-02**.

This is a targeted primary-literature audit for future background writing.  It
is not a systematic or bibliometric review.  Its purpose is to prevent four
different objects from being described by the same word *root*:

1. a parameter with a physical interpretation or unit;
2. an operational threshold observed in an experiment;
3. an exact spectral, algebraic, or invariant-manifold root of a mathematical
   model; and
4. a theorem identifying the experimental threshold with a unique,
   nondegenerate root of the original model.

The fourth level is the relevant benchmark for calling a complete-history
connection root *experimentally physical*.

## Executive finding

Published work contains many genuine experimental thresholds and several
rigorous roots.  The closest literature examined here does **not** contain one
example that simultaneously provides

- a naturally controlled experimental parameter;
- an intrinsic complete-history invariant-manifold connection root in the
  original RFDE or network;
- an existence, uniqueness, and nondegeneracy theorem for that root; and
- experimental calibration or validation identifying the measured threshold
  with the mathematical root.

Instead, the literature separates into two strong but largely disjoint
groups.  Rigorous RFDE canard theory constructs history-space connections
without experimental calibration.  Delay, laser, circuit, and thermo-fluid
experiments measure sharp transitions, but interpret them through spectral
stability, numerical continuation, singular reduction, or phenomenological
models rather than a proved complete-history connection equation.

This conclusion is deliberately limited to the targeted works below.  It is
evidence for a literature boundary, not a universal nonexistence claim.

## Root taxonomy

| Object | Typical equation or definition | Experimental meaning | Relation to Paper A |
| --- | --- | --- | --- |
| Spectral root | `det Delta(lambda,p)=0`, with `Re lambda=0` at onset | Often strong: onset delay, gain, or current can be measured | Not a heteroclinic history root |
| Singular/algebraic root | Fold, critical-manifold, or switching equation at `epsilon=0` | Parameter may be physical, but finite-`epsilon` threshold generally shifts | Useful mechanism, not automatically the actual threshold |
| Operational threshold | First observed spike, oscillation, switching event, or amplitude jump | Directly measurable, with protocol dependence | Requires a separate identification theorem |
| Reduced-model root | Zero or bifurcation of a mean-field, spectral, or low-dimensional model | Predictive when reduction is accurate | Equality with the original-network threshold is usually not proved |
| Complete-history connection root | A gap between selected unstable and stable full histories vanishes | Intrinsic to the stated RFDE once the invariant objects are natural | This is Paper A's mathematical object |

In the tables, **E1** means a natural physical control or measured quantity,
**E2** an experimental transition, **M1** an exact root in the original model
(possibly only in its singular limit), and **M2** a theorem identifying the
experimental transition with that root.

## RFDEs and physical delay systems

| Work | Physical or experimental content | Mathematical root actually used | Assessment |
| --- | --- | --- | --- |
| [Campbell, Stone & Erneux (2009)](https://doi.org/10.1080/14689360902852547) | The delay is one spindle revolution and the control parameter is related to chip width and cutting force.  Representative aluminium-machining values are used, but no machining threshold is measured. | A small-delay inertial-manifold approximation and DDE continuation locate Hopf and canard transitions.  The paper explicitly notes that its high-speed limit is not physically attainable. | **E1**; numerical/asymptotic threshold; no complete-history connection theorem or **E2/M2**. |
| [Krupa & Touboul (2016a)](https://doi.org/10.1007/s10884-015-9478-2) | Canonical delayed van der Pol setting; no experimental calibration. | Under stated hypotheses, a smooth parameter curve connects attracting and saddle slow manifolds in DDE history space.  Verification for the concrete model is partly analytic and partly numerical. | Closest rigorous RFDE-side comparator: **M1** at the theorem level, but no **E1/E2/M2**. |
| [Krupa & Touboul (2016b)](https://doi.org/10.1007/s00332-015-9268-3) | Delayed FitzHugh--Nagumo parameters have neuronal interpretations, but are not fitted to an experiment. | Hopf and Bogdanov--Takens curves are analysed; global branches, mixed-mode oscillations, bursting, and chaos rely substantially on numerical continuation. | Model-level physical semantics, not an experimentally identified history root. |
| [Talla Mbé et al. (2015)](https://doi.org/10.1103/PhysRevE.91.012902) | A delayed optoelectronic oscillator uses measured pump current, loop gain, Mach--Zehnder bias, and a 4 km fibre delay.  Experimental and DDE time series are compared. | Canard geometry is read from a two-dimensional Liénard critical manifold obtained in a singular zero-delay reduction; the full DDE is simulated. | Strong **E1+E2**, but no full-history **M1/M2**. |
| [Romeira et al. (2016)](https://doi.org/10.1038/srep19510) | A resonant-tunnelling-diode/laser/fibre device demonstrates write, storage, and recovery of regenerative optical memory. | DDE-BIFTOOL locates Hopf and saddle-node-of-cycles values and a rapid canard-like amplitude growth. | **E1+E2** for the device; continuation values are not proved history-connection roots. |
| [Liu et al. (2026)](https://doi.org/10.1103/qvlk-6df6) | Programmable delayed-network circuits display onset of oscillations at measurable delays, close to reduced-model predictions. | A reduced characteristic equation predicts the critical delay for a Hopf crossing. | Strongest current delay-network reduction plus experiment comparator: **E1+E2**, but the root is spectral rather than heteroclinic. |

The key distinction for future prose is therefore not “physical versus
mathematical.”  Both groups are physical and mathematical in legitimate
senses.  The missing bridge is an identification theorem between a measured
threshold and an invariant-manifold root in the original RFDE history space.

## Experimental and application-facing fast--slow systems

| Work | Application | What is observed or computed | Root boundary |
| --- | --- | --- | --- |
| [Itoh & Tomiyasu (1990)](https://globals.ieice.org/en_transactions/transactions/10.1587/e73-e_6_848/_p) | Nonlinear electronic circuit | Direct experimental observation of short-lived canards and subsequent irregular or period-two oscillations | An observed phenomenon, not a proved unique parameter root |
| [Marino et al. (2011)](https://doi.org/10.1103/PhysRevE.84.047201) | Light-emitting diode with optoelectronic feedback | Experimental mixed-mode oscillations interpreted through a low-dimensional slow--fast model | Genuine **E1+E2**; not an RFDE complete-history root |
| [Bhavi et al. (2024)](https://doi.org/10.1063/5.0223320) | Turbulent reactive thermo-fluid system | Experimental rapid continuous amplitude growth and bursting over a narrow control range; a phenomenological thermoacoustic model explains the slow--fast mechanism | Strong experimental canard evidence, without a rigorous model-root identification |
| [Mitry et al. (2013)](https://doi.org/10.1186/2190-8567-3-12) | Post-inhibitory rebound in a neuron model motivated by propofol anaesthesia | A folded-saddle canard forms a firing-threshold manifold and moves with the inhibitory-current time scale | Biophysically meaningful model threshold; no direct experimental calibration of the canard root |
| [Rotstein et al. (2003)](https://doi.org/10.1063/1.1614752) | Belousov--Zhabotinsky reaction with global feedback | Canard asymptotics and a cluster reduction give critical feedback values | Experimentally controllable interpretation, but approximate reduced thresholds rather than original-system roots |
| [Rotstein & Kuske (2006)](https://doi.org/10.1016/j.physd.2006.01.007) | Coupled intracellular calcium oscillators | Effective IP3-related parameters are compared with asymptotic canard thresholds | Natural biochemical semantics; no cell experiment or exact network root |
| [Awal et al. (2024)](https://doi.org/10.1007/s00332-024-10033-7) | Coupled Lengyel--Epstein chemical oscillators | Folded singularities organise symmetry breaking and asymmetric canard explosions | Natural chemical model and strong geometry; theoretical/numerical rather than experimentally calibrated |

These papers justify saying that canards organise experimentally relevant
threshold phenomena in electronic, photonic, neuronal, chemical, machining,
and thermo-fluid settings.  They do not justify calling an unrelated model's
connection root an experimental threshold.

## Network canards and network reduction

| Work | Original network and control quantity | Root or threshold | Assessment |
| --- | --- | --- | --- |
| [Dolcemascolo et al. (2020)](https://doi.org/10.1103/PhysRevE.101.052208) | A real network of 451 VCSELs; common pump current and individual lasing thresholds are measured. | An exact implicit equation describes branches of the original `N`-laser singular critical manifold.  The experimental upper bifurcation current is an operational threshold. | Closest experimental-network case: **E1+E2+M1(singular)**, but no theorem that the measured bifurcation current is the unique algebraic root (**no M2**). |
| [D'Huys et al. (2021)](https://doi.org/10.1088/2515-7647/abcbe3) | The same heterogeneous VCSEL platform; single-node excitability and network trajectories are observed. | “Canard resonance” is a nonzero minimum of trajectory dispersion versus model noise strength, not a zero of a connection equation. | Experimental relevance, but no physical calibration of the noise optimum and no connection root. |
| [Balzer et al. (2024)](https://doi.org/10.1103/PhysRevLett.133.237401) | Adaptive mean-field laser network with pump and feedback parameters | Exact singular switching equations define on/off crossings; finite-time canard cascading is studied numerically. | **M1(singular)** with laser semantics; no experimental validation or single finite-`epsilon` connection root. |
| [Jardón-Kojakhmetov & Kuehn (2020)](https://doi.org/10.1007/s00332-020-09634-9) | Fast--slow consensus network with a dynamic edge weight | The original graph Laplacian has a second zero eigenvalue at an explicit edge-weight root, which organises a maximal canard. | Mathematically clean original-network root; no physical apparatus, unit, or experiment. |
| [Avitabile, Desroches & Ermentrout (2022)](https://doi.org/10.1371/journal.pcbi.1010569) | Networks of quadratic integrate-and-fire neurons driven by a slow input amplitude | Folded-saddle canards form effective excitation thresholds in an exact mean field for one network class and in heuristic reductions for others. | Biologically interpretable threshold supported by network numerics, not an experimental or full finite-network scalar root. |
| [Qin & Lin (2023)](https://doi.org/10.1103/PhysRevResearch.5.043209) | Neural, gene-regulatory, and ecological slow--fast networks | A Perron-weighted two-dimensional reduction predicts pulsatile tipping.  The leading singular threshold solves reduced fold equations; finite-network tipping is defined operationally in simulations. | Closest slow--fast reduction comparator; no experiment and no equality theorem for an original-network connection root. |

Two comparisons should remain separate in the introduction.  Dolcemascolo et
al. are the closest experimental large-network comparator.  Jardón-Kojakhmetov
and Kuehn are the cleanest exact original-network-root comparator.  Neither
combines those two strengths.

## Reduction, memory, identifiability, and observability

| Work | What is recovered or predicted | Why it is not the present root |
| --- | --- | --- |
| [Laurence et al. (2019)](https://doi.org/10.1103/PhysRevX.9.011042) | Spectral observables approximate states and bifurcation points of complex networks. | A reduced critical point is not an exact nonhyperbolic connection root of every finite network. |
| [Jiang et al. (2018)](https://doi.org/10.1073/pnas.1714958115) | A two-dimensional reduction predicts collapse points on 59 empirical plant--pollinator topologies. | The topologies are empirical, but abundances and tipping parameters are generated by the model rather than measured ecological collapses. |
| [Herrera-Delgado, Briscoe & Sollich (2020)](https://doi.org/10.1103/PhysRevResearch.2.043069) | Mori--Zwanzig memory terms preserve transient behaviour and approximate basin separatrices and a Hopf curve after variables are projected out. | This is the nearest conceptual comparator for transverse information returning as memory, but it does not define or prove a scalar invariant-manifold connection root. |
| [Banerjee et al. (2021)](https://doi.org/10.1103/PhysRevX.11.031014) | Links and heterogeneous delays are inferred from noisy optoelectronic-network experiments. | The recovered objects are network parameters; link classification is an inverse problem, not a dynamical threshold. |
| [Zhang et al. (2019)](https://doi.org/10.1103/PhysRevE.99.042311) | Coupling strengths and delays are reconstructed analytically and numerically with hidden nodes and fast noise. | Parameter identifiability is distinct from a parameter value at which invariant histories connect. |
| [Haehne et al. (2019)](https://doi.org/10.1103/PhysRevLett.122.158301) and [Porfiri (2020)](https://doi.org/10.1103/PhysRevLett.124.168301) | Detection-matrix rank is used to infer hidden units or network size, and its relation to observability is analysed. | The “experiments” are transient probes and the output is a rank/integer estimate, not a physical bifurcation root. |

This literature also fixes an important terminology boundary:
projection-blindness of one stationary aggregate is **not** the same as
non-observability from full time-series data.  Paper A's perturbation is
invisible to a specified stationary projection at every complete history;
the full transverse dynamics can still carry and reveal its effect.

## Placement of Paper A

| Case | Exact original-system root | Natural experimental control | Experimental identification |
| --- | --- | --- | --- |
| Krupa--Touboul RFDE canard theory | Yes, under theorem hypotheses | No calibrated apparatus | No |
| Delayed optoelectronic and photonic experiments | No proved complete-history connection root | Yes | Yes for the observed transition, not for a connection equation |
| Dolcemascolo et al. VCSEL network | Exact singular branch equation | Yes | No equality theorem for the measured upper bifurcation current |
| Jardón-Kojakhmetov--Kuehn consensus canard | Yes | No concrete apparatus or units | No |
| **Paper A** | **Yes, for every fixed anchored RFDE in the stated class** | **The global anchor is not experimentally calibrated** | **No** |

Paper A therefore occupies the rigorous-root/nonexperimental quadrant.  Its
root is independent of finite proof preparation and intrinsic to each fixed
anchored RFDE, but roots for different global anchors need not agree.  The
paper does not currently establish an experimental pulse, onset, or maximal-
canard threshold for an unanchored biological, chemical, or physical system.

Use **anchored complete-history connection root** or **anchored heteroclinic-
canard root** for the proved object.  Avoid the unqualified phrase *physical
root*: it can be misread as claiming experimental calibration.  Reserve
*experimentally physical root* for a future result that closes the full
control--observable--connection identification chain.

## Safe background claims

The following claims are supported by the audited literature:

- Canard-mediated sharp transitions have been observed in real electronic,
  optoelectronic, photonic, and turbulent thermo-fluid systems.
- Rigorous DDE theory can construct canard connections in a history-space
  setting, independently of experimental calibration.
- Network reductions can predict Hopf onset, collapse, and pulsatile tipping,
  and recent delayed-network work validates a reduced Hopf threshold in a
  programmable circuit.
- Memory and observability methods can recover effects or parameters hidden by
  a chosen projection.
- Exact graph or singular-limit roots exist in several network-canard models.

The following claims are **not** supported:

- that every experimentally observed canard-like transition is the zero of a
  proved invariant-manifold gap;
- that a reduced or singular-limit threshold equals the finite original-
  network threshold without an error or identification theorem;
- that a parameter with biological or physical semantics has been
  experimentally calibrated;
- that Paper A's fixed anchor is a natural physical selection principle; or
- that prior observability results already prove Paper A's projection-blind
  transverse-return mechanism.

## Draft-ready literature bridge

A future introduction can safely compress the audit as follows:

> Experiments on electronic, optoelectronic, photonic, and thermo-fluid
> systems show that canard-mediated transitions can occur at sharply
> localised values of measurable control parameters.  Separately, RFDE
> canard theory constructs invariant-history connections, while network
> reduction predicts spectral onset and pulsatile tipping and projection
> methods recover memory left by unresolved variables.  In the literature
> examined here, these strands do not yield a theorem identifying an
> experimentally measured network threshold with a unique complete-history
> connection root of the original RFDE.

For Paper A, the next sentence must remain model-specific: its new object is a
proved root of each fixed anchored RFDE, not an experimentally calibrated
threshold.  The defensible new mechanism is that a delay redistribution which
is exactly invisible to the declared stationary history projection can still
move that root through dimension-uniform transverse return.

## What would close the experimental bridge

An application paper would need all of the following:

1. a natural platform and control variable, such as fibre delay, pump current,
   feedback gain, chip width, or a calibrated stimulus;
2. a fixed experimental protocol and observable defining the onset event;
3. a parameter map, with units and uncertainty, from the apparatus to the
   RFDE;
4. a theorem relating the event zero set to the complete-history connection
   root, including uniqueness and transversality; and
5. an experimental bracket or estimate whose uncertainty can be compared with
   the mathematical prediction.

Without Step 4, an experiment may validate a useful threshold model but does
not validate the invariant-manifold root.  Without Steps 1--3 and 5, a rigorous
root remains a mathematical result rather than an experimentally physical one.

## Bibliographic routing

The shared BibTeX file is [`../references/references.bib`](../references/references.bib).
Useful citation groups are:

- rigorous RFDE and delayed-canard geometry:
  `krupa2016explosion`, `krupa2016complex`, `avitabile2020local`;
- physical delayed systems:
  `campbell2009delay`, `tallambe2015mixed`,
  `romeira2016regenerative`, `liu2026predicting`;
- experimental/application canards:
  `itoh1990experimental`, `marino2011mixed`, `bhavi2024canard`,
  `mitry2013excitable`, `rotstein2003canard`, `rotstein2006localized`,
  `awal2024strong`;
- network canards and reduction:
  `jardon2020consensus`, `dolcemascolo2020effective`,
  `dhuys2021canard`, `balzer2024cascading`,
  `avitabile2022crossscale`, `qin2023tipping`,
  `laurence2019spectral`, `jiang2018predicting`;
- memory, reconstruction, and observability:
  `herrera2020tractable`, `herrera2018memory`,
  `banerjee2021machine`, `zhang2019reconstruction`,
  `haehne2019detecting`, `porfiri2020validity`.

