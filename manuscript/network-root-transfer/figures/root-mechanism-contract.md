# Figure contract: blind control and hidden-return readout

- Reader question and result served: see, in one pass, why a perturbation that
  is exactly invisible to the stationary projection can still excite every
  transverse direction when two delay locations are available, and how the
  resulting nonlinear root responses determine the compressed transverse
  return covector.
- Status: `MIXED`. Panel (a) contains the exact singular parabola and phase
  section, together with schematic retained RFDE traces and preparation tails.
  Panel (b) is a diagram of proved identities, sharp bounds, and the proved
  finite-scale asymptotic readout; only the spatial arrangement of its boxes
  and arrows is schematic.
- System, parameters, coordinates, and time convention: panel (a) uses
  \(\widehat X=\alpha X\), \(\widehat Y=\alpha Y\), and slow time
  \(s=\delta t\). Panel (b) uses the operators of the blind-controllability
  theorem: \(\mathsf S_N\), \(\mathsf Q_N\), \(\mathsf T_N\), \(A_N\),
  the leading response \(\Lambda_N\), and the compressed return covector
  \(\mathfrak r_N\).
- Objects, directions, and representative choices: atomwise stationary-row
  neutrality and \(\sum_kR_k=0\) are the exact blindness and pure-
  redistribution constraints. Two extreme, distinct delay atoms provide the
  displayed sharp right inverse. Coincident atoms are understood to have been
  merged before the one-distinct-delay no-go is applied. The curvature and
  recovery boxes are separate realization profiles, not additional steps in
  the abstract reconstruction theorem.
- Panels and reading order: (a) singular fold geometry, retained one-sided
  histories, selected complete-history match; (b) exact blindness and zero
  zeroth moment, two-delay source surjectivity (with the single-delay no-go as
  a side branch), stable transverse lift, nonlinear root readout, and dual
  reconstruction. Read panel (b) from top to bottom.
- Line, marker, fill, color, and arrow meanings: solid dark boxes and arrows
  form the proved main dependency chain; the gray side branch is the exact
  no-go; blue and orange dashed-outline boxes identify the two inequivalent
  model realization profiles. In panel (a), blue/orange solid curves are the
  two retained one-sided traces, gray dotted pieces are preparation tails,
  and the thin gray parabola is the exact singular curve. Direct labels and
  line styles make the figure grayscale-safe.
- What the figure must not imply: the schematic traces prove existence; the
  finite-section root is preparation independent; one scalar probe determines
  a covector of dimension \(N-1\); the full network or the full return operator
  is reconstructed; an arbitrary irreducible transition matrix is sparse; or
  the curvature and recovery channels occur simultaneously in one model.
- Caption draft: identify exact versus schematic elements, state the two-delay
  surjectivity and single-delay obstruction, describe the finite-scale root
  readout and reconstruction formula, and identify curvature/recovery only as
  two realization profiles.
- Production route and editable source: reproducible Matplotlib source
  `root_mechanism.py`, vector PDF `root-mechanism.pdf`; `make figure`
  regenerates the artifact.
- Final placement and size: first cited at the end of the introduction and
  placed at full text width. Nominal source size is 7.15 by 4.05 inches, which
  is reduced to the 6.5-inch text width in the manuscript.
- Checks needed before delivery: equations and signs against the theorem;
  arrow direction; exact/schematic disclosure; one-delay wording; no claim of
  full-network recovery; final-size label legibility; crop and overlap;
  grayscale redundancy; embedded fonts; absence of rasterized line art; and
  balance on the rendered manuscript page.
