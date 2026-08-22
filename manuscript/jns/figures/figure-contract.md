# Figure contract

## Figure 1: delay redistribution, history lift, and connection gap

- **Reader question and result served:** How can a delay redistribution that
  is invisible in the critical projection move the selected canard
  connection, and why is the matching condition a complete-history condition
  rather than a current-state crossing?  The figure supports the fixed-measure
  proposition, the invariant-history-graph construction, and the definition
  of the scalar connection gap.
- **Status:** Panel (a) is **EXACT** at the level of the displayed atomic
  measures.  Panels (b) and (c) are **SCHEMATIC** projections.  The gray
  parabola in panel (c) is the **EXACT** singular canard
  \(Y=\alpha X^2-(2\alpha)^{-1}\); the colored one-sided traces and their
  nonzero separation are schematic.
- **System, parameters, coordinates, and time convention:** The two-module
  FitzHugh--Nagumo RFDE in fold time \(s=\delta t\), with
  \(0<\theta_0<\theta_1\), critical right/left vectors \(r,\ell\), and
  transverse projector \(P_\perp\).  Panel (b) suppresses one critical and one
  stable coordinate from the graph \(h=H_{\delta,\nu,\eta}(u)\).  Panel (c)
  uses the reduced \((X,Y)\)-plane and forward fold time, which points from
  right to left along the singular canard.
- **Objects, directions, and representative choices:** In panel (a), atom
  locations and the critical weights \(1/3,2/3\) are exact.  Equal and
  opposite transverse arrows encode the coefficients \(+\eta q\) and
  \(-\eta q\); their drawn length is not a numerical value of \(\eta\).
  Panel (b) shows a projected invariant graph, representative stable fibres
  contracting toward it, and one complete history segment
  \(\iota_{\delta,\nu,\eta}(u)\).  Panel (c) shows the section \(X=0\), a
  forward attracting-side trace, a forward repelling-side trace, and their
  scalar normal gap \(\mathfrak d_{\mathcal P}\).
- **Panels and reading order:** (a) projection algebra; (b) complete-history
  lift; (c) one-sided matching.  The left-to-right order is the mechanism used
  in the proof.
- **Line, marker, fill, color, and arrow meanings:** Dark blue solid marks the
  fixed critical projection or attracting-side object; orange dashed marks
  the changed transverse channel or repelling-side object.  Color is always
  reinforced by line style, marker, direct label, or sign.  Gray dotted marks
  the exact singular reference.  Vertical gray arrows in panel (b) represent
  stable contraction, not physical fast jumps.
- **What the figure must not imply:** The schematic graph is not
  one-dimensional; a two-dimensional graph is shown only after coordinate
  suppression.  The one-sided colored curves are not computed trajectories,
  their drawn distance is not quantitative, and the picture does not prove
  existence, uniqueness, global outer selection, or preparation independence.
- **Caption draft:** *Mechanism of the transverse delay shift. (a) The
  critical atomic delay measure is fixed, whereas the transverse measure
  changes by equal and opposite atoms. (b) Stable contraction produces an
  invariant graph whose reduced orbit segment lifts to a complete history.
  (c) The two selected one-sided histories define a scalar normal gap on
  \(X=0\); its zero means equality of the complete histories.  Panel (a) and
  the gray singular canard are exact; the remaining geometry is schematic and
  projected.*
- **Production route and editable source:** ReportLab vector drawing from
  `generate_figures.py`; no raster or generated-image layer.
- **Final placement and size:** Full text width; PDF media box
  \(6.8\,\mathrm{in}\times2.8\,\mathrm{in}\).
- **Checks needed before delivery:** Inspect signs of the two transverse
  atoms, forward-time arrows in panel (c), coordinate suppression disclosure,
  grayscale redundancy, crop, embedded fonts, and absence of raster images.

## Figure 2: exact-chart diagnostic convergence

- **Reader question and result served:** Does the independently computed
  prescribed-history diagnostic reproduce the sign and scale of the analytic
  transverse-return coefficient as \(\delta\) decreases?  The figure supports
  only the numerical sign-and-scale check, not the connection theorem.
- **Status:** **COMPUTED**, by deterministic plotting of the tracked file
  `experiments/results/exact_chart_threshold_convergence.json`.  The plotting
  script does not rerun the RFDE solver or alter the data.
- **System, parameters, coordinates, and time convention:** Exact four-variable
  fold chart with \(K=1\), \((\theta_0,\theta_1)=(0.5,1)\), \(d_w=1.5\), and
  symmetric redistribution step \(h=0.04\), as recorded in the JSON artifact.
  The incoming history is prescribed at \(-S\); the root uses a finite
  leading-energy exit section at \(+S\).
- **Objects, directions, and representative choices:** Upper panel: the
  normalized central quotient
  \(q_{\mathrm{num}}=[\nu_c(h)-\nu_c(-h)]/(2\delta h)\), with the exact analytic
  coefficient from the same data record as a horizontal reference.  Lower
  panel: the absolute relative discrepancy, displayed as a percentage.  Both
  axes use logarithmic \(\delta\); the lower vertical axis is logarithmic.
- **Panels and reading order:** Coefficient and reference first, relative
  discrepancy second.
- **Line, marker, fill, color, and arrow meanings:** Orange circles joined by a
  solid line are recorded diagnostic values.  The black dashed horizontal line
  is the predicted coefficient, not a fit.  Blue squares joined by a dashed
  line are recorded relative discrepancies.  Markers and dashes make every
  distinction grayscale-readable.
- **What the figure must not imply:** The sequence couples decreasing
  \(\delta\) to increasing finite section half-width \(S\).  It does not show a
  complete-history intersection, a rigorous error bar, a convergence rate, a
  section-independent threshold, or a proof of the theorem.  Lines between
  samples guide the eye only.
- **Caption draft:** *Prescribed-history, finite-section diagnostic. The upper
  panel compares the normalized central quotient with the analytic
  transverse-return coefficient (dashed reference, not a fit); the lower
  panel gives the absolute relative discrepancy.  The section half-width
  increases along the sequence as \(\delta\) decreases.  Lines joining samples
  guide the eye.  This is a sign-and-scale diagnostic, not a complete-history
  threshold computation and not part of the proof.*
- **Production route and editable source:** `generate_figures.py` reads the
  tracked JSON artifact and writes a vector PDF using ReportLab with embedded
  TrueType fonts.
- **Data, solver, and reproduction command:** Full solver, tolerance, root,
  section, checksum, and source-revision metadata are retained in the JSON.
  From `manuscript/jns`, run
  `/home/hblu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 figures/generate_figures.py`.
- **Final placement and size:** Approximately \(0.92\) text width; PDF media
  box \(6.2\,\mathrm{in}\times4.7\,\mathrm{in}\).
- **Checks needed before delivery:** Validate all plotted values against the
  JSON, verify that the reference is not fitted, inspect nonmonotone samples
  without smoothing, check logarithmic axes and diagnostic warning, inspect at
  final manuscript size, verify embedded fonts, and confirm no raster images.
