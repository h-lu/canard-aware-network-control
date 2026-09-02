# Figure plan: three-node finite-section sensitivity diagnostic

- Reader question and result served: Can the three-node perturbation in the
  introduction move a scalar fold-passage zero even though its direct
  stationary projection vanishes, and does the normalized movement have the
  sign and scale of the exact Fredholm coefficient?
- Status: `MIXED`.  The exit-gap curves, roots, and normalized quotients are
  computed.  The projection identity, the coefficient
  `Lambda_3=-2 sigma/3`, and cancellation in the coincident-delay control are
  exact analytic statements.
- System, parameters, coordinates, and time convention: the specialized
  exact fold-coordinate RFDE in equation (4.2), with `N=3`,
  `pi=(1,1,1)/3`, `P=1 pi^T`, `c=(1/2,1,3/2)`, `D=1`, `K=2`,
  `beta=3`, delays `(0,1)`, and perturbation amplitude `zeta`.  Increasing
  `s` is forward fold time.
- Numerical definition: prescribe the singular history
  `(X,Y,h)=(-s/2,(s^2-2)/4,0)` on `[-S-1,-S]`, integrate to `S` by a literal
  method of steps with SciPy Radau, and tune `nu` until
  outgoing section function `E_hat_S=Y(S)-X(S)^2+1/2=0`.  The displayed root is named
  `nu_hat_sec(delta,zeta;S)`.
- Panels and reading order: (a) three section-mismatch curves and their marked
  zero crossings at one fixed `(delta,S)`; the horizontal movement of the
  markers is the visual focus.  (b) the scaled zero displacement along a
  diagonal `(delta,S)` sequence, the exact Fredholm coefficient, and the
  zero coincident-delay control.  The five pairs are
  `(0.12,2.5)`, `(0.08,2.75)`, `(0.05,3)`, `(0.02,3.5)`, and `(0.01,4)`.
- Panel titles and axis language: `(a) Delay redistribution shifts the zero`
  and `(b) Scaled shift versus theory`; the axes pair ordinary descriptions
  (`centered parameter`, `section mismatch`, `scale parameter`, and `scaled
  zero shift`) with the mathematical symbols.
- Line, marker, and color meanings: blue circles, black squares, and orange
  triangles distinguish `zeta=-h,0,+h` in panel (a).  In panel (b), blue
  circles are the two-distinct-delay computation, the black dashed line is
  the exact coefficient, and green triangles are the coincident-delay
  same-delay control.  Every distinction also uses line style or marker shape.
- What the figure must not imply: the prescribed history is not the
  parameter-dependent invariant history graph; the one-orbit outgoing
  condition is not the two-trace boundary-value definition of `D_3^fin`;
  the calculation does not evaluate `G_{3,delta}^g`, construct a
  stable/unstable manifold intersection, prove the uniform theorem
  remainder, or compute a heteroclinic connection or maximal canard.  The
  displayed trend retains finite-history and finite-section bias.
- Editable sources and provenance: numerical kernel
  `src/canard_control/three_node_finite_section.py`; data driver
  `experiments/three_node_finite_section_diagnostic.py`; archived JSON
  `experiments/results/three_node_finite_section_diagnostic.json`; Matplotlib
  source `figures/three_node_finite_section.py`.
- Final placement and size: full text width immediately after the
  finite-interval derivative proposition, with a forward reference after the
  three-node calculation in the introduction.
- Checks required before delivery: projection RHS residual is zero; scalar
  root residuals are small; the centered quotient has negative sign and
  approaches `-1/3`; the coincident-delay computation is independent of
  `zeta`; solver and difference-step refinements are smaller than the
  displayed asymptotic discrepancy; labels remain legible in the final PDF
  and in grayscale.
