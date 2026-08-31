# Paper A flagship claim and proof map

This audit map tracks [Issue #31](https://github.com/h-lu/canard-aware-network-control/issues/31)
and the weighted-connection upgrade in
[Issue #32](https://github.com/h-lu/canard-aware-network-control/issues/32).
It is not part of the submitted paper.

## Central theorem package

```text
exact projection blindness
    + two separated delay moments span the transverse source
    + transverse full-history inverse and collective return
    = uniformly identifiable hidden-return covector
    -> fixed-model complete-history heteroclinic-canard displacement.
```

The finite-section selected root remains nonintrinsic and is retained only as
a comparison object.  The flagship root is instead the exact membership
relation between the past-complete incoming branch of `E_N^+` and the
future-asymptotic stable history sheet of `E_N^-` in one fixed anchored RFDE.
Exact roots may change when the global anchor (and hence the RFDE) changes;
after each model is centered at its own baseline, the weighted conormal has the
same uniform limit `(1,-Lambda_N)` over the declared bounded anchor class.

| Flagship requirement | Statement | Proof location |
| --- | --- | --- |
| Integrated flagship theorem | `thm:flagship-synthesis` | Exact blindness, two-delay source dichotomy, fixed anchored-model heteroclinic root, full-dual-norm response, dual recovery, and anchor-universality boundary |
| Anchored global model and exact equilibria | `prop:anchor-central-identity-equilibria` | Nonempty bounded anchor class, literal equality with the original RFDE on the retained history tube, and exact structural-parameter-independent equilibria `E_N^+`, `E_N^-` |
| Hyperbolic history objects | `thm:anchor-indices-manifolds` | Uniform anchor root counts, `dim W^u(E_N^+)=1`, `codim W^s(E_N^-)=1`, past-complete incoming branch, and intrinsic local stable history sheet |
| Half-line stable sheet and tail forgetting | `thm:anchor-annulus-flat-forgetting` | Stable-forward/one-dimensional-unstable-backward Lyapunov--Perron graph, forward central preimage, and full-history capped-action comparison through the declared mixed jets |
| Exact membership relation | `prop:anchor-gap-comparison` | Chart-independent zero fiber equivalent to the complete heteroclinic `E_N^+ -> E_N^-`, with direct anchored gap and endpoint-tail completion |
| Fixed-model canard root and conormal | `thm:anchored-physical-root-conormal` | Unique local root, quantitative canard tracking, `D_eta mu_c=delta^3 Lambda_N+O(delta^4+delta^3||eta||)` in full dual norm, and weighted conormal limit |
| Section/cut/anchor naturality | `prop:anchor-physical-naturality-composition` | Phase, defining-function, regular forward-section, and finite-cut naturality; exact roots across anchors may differ, while centered first conormals share the same uniform limit |
| Abstract two-atom source criterion | `prop:abstract-two-atom-source` | General moment-source norm, explicit extreme-atom right inverse, minimum probe cost, dual isometry, and one-atom no-go |
| Sharp two-delay controllability | `thm:hidden-return-tomography` | Exact source norm, explicit right inverse, and merged-single-delay no-go |
| Dimension-uniform dual recovery | `thm:hidden-return-tomography` | `r(z)=Lambda(Q A z)` and condition bound `(2-gamma)/gamma` |
| Finite-scale curvature pairings | `cor:curvature-tomography` | Unit-probe-ball root remainder and weighted reconstruction |
| Finite-scale recovery pairings | `cor:recovery-tomography` | Second-model pairing formula and arbitrary fixed-`N` covector rays |
| Preparation-relative canonical response germ | `thm:canonical-response-germ` | Pairwise fixed-preparation expansion and uniform derivative limit |
| Selected weighted connection conormal | `thm:weighted-connection-jet`, `thm:structural-ball-connection`, `cor:schur-full-conormal`, `thm:joint-redistribution-conormal` | Both models raywise; shared-resource full structural ball under an admissible rule; cokernel-valued jet; pairwise preparation-independent limiting conormal; fixed-chart covariance with the front-face qualification for chart families |
| Abstract selected-to-physical interface | `prop:physical-weighted-c1-transfer` | Conditional weighted `C^1` criterion retained as a reusable abstract result.  The proposition itself asserts no root; the anchored root is constructed directly by the later half-line membership theorem and does not depend on this criterion |
| Critical-layer precursor | `prop:unprepared-outer-skeleton` | Preparation-independent constant-history critical curve and dimension-uniform leading frozen-resource fast-voltage splitting |
| Positive-`delta` frozen voltage histories | `prop:frozen-voltage-history-splitting`, `rem:frozen-resource-phase-quotient` | Capped-rate full-history stability/splitting for the frozen-resource voltage RFDE, uniform structural `C^2` bounds, and an exact obstruction to the raw full-system one-unstable formulation; no nonautonomous slow tracker |
| Exact tracker/quotient interface | `prop:exact-outer-history-equation`, `prop:physical-history-phase-quotient`, `prop:exact-resource-gauge-quotient` | Uncut if-and-only-if tracker equation; genuine transported longitudinal history; exact stationary-gauge quotient; resource-gauge triangularization and $O(S_\delta^{-1})$ Volterra realization. Conditional on tracker existence and collar bounds; no tracker or dichotomy existence claim |
| Physical backtrack calculus | `prop:physical-backtrack-calculus` | Uniform weighted derivatives of the state-dependent physical delay map and the joint delayed composition/difference through three Fr\'{e}chet derivatives; raw backtrack variations are $O(\delta)$ and their relative contribution is $O(S_\delta^{-1})$ on the logarithmic collar, uniformly in $N$ and $\delta$ |
| Principal endpoint Green splitting | `prop:principal-tracker-endpoint-green` | Exact cancellation coordinate $\mathfrak p=\delta^2Q+\ell_NZ$; dimension-uniform slow right inverse, mixed repelling endpoint lift, action-weighted boundary layers, and sharp one-derivative loss in $Q$. Finite endpoint traces only: no compatible complete-history collar lift or nonlinear tracker |
| Exact nonlinear tracker normal form | `prop:nonlinear-resource-defect-normal-form` | The cancellation coordinate is exactly the physical resource defect $\mathfrak p_{\rm nl}=w_{\rm seed}-w$; exact nonlinear $(Z,\mathfrak p_{\rm nl},Q)$ identities, full Fr\'{e}chet differential, and a local dimension-uniform $C^0$ speed coordinate. No nonlinear tracker fixed point is asserted |
| Raw-compatible endpoint collars | `prop:compatible-endpoint-jet-collar`, `prop:endpoint-scale-not-slow-speed` | Dimension-uniform Hermite endpoint-jet chart satisfying the raw RFDE compatibility recursion; exact resource-defect/speed/backtrack bridge and fixed-history parameter jets, with no extra Fredholm row. The chart is not a Green right inverse, and a sharp scalar boundary layer proves that finite endpoint scale does not control the slow-speed norm |
| Exact fold-time tracker interface | `prop:fold-time-tracker-normal-form` | Direct fixed-delay $(r,Z,\mathfrak p_{\rm nl})$ normal form exactly equivalent to the raw fold-time RFDE; algebraic speed reconstruction and explicit compatible-collar initial-history map. Reparameterization is conditional on nonvanishing speed and makes no past-orbit claim for arbitrary old histories; no mixed-buffer BVP existence is asserted |
| Fixed-phase prescribed-history Green inverse | `prop:fixed-phase-green-collar-buffer` | Dimension-uniform fixed-parameter $C^0$ inverse for the $(Z,p)$ normal block with a prescribed old RFDE voltage-history segment, boundary traces $(Z(0),p(0))$ on the attracting branch or $(Z(0),p(S_r))$ on the repelling branch, and compatible $p(0)$-to-collar feedback. No backward RFDE is used. No high-order slow inverse, phase/event border, speed sign, tracker, or parameter jet is asserted |
| Scaled phase--event core | `prop:scaled-phase-event-core` | Explicit dimension-uniform inverse for the scalar collective phase equation with entry phase and terminal event rows, using the sharp scaled event-time variable $\widehat\tau=\delta\Delta S$. It proves the unscaled $\delta^{-1}$ loss and persistence of any net phase shift after compact speed forcing. The coupled phase--normal inverse and nonlinear moving-event chart are not asserted |
| Normal-to-phase action coupling | `prop:normal-to-phase-action-coupling` | The algebraically reconstructed speed of the normalized fixed-phase normal block, including endpoint/collar boundary layers, maps into $\mathsf H_\phi^0$ with norm $O(r_{\rm out}^2+\delta^{2-2\vartheta})$ and therefore produces a small bordered phase response. No higher phase-source jet, phase-to-normal column, moving-event column, or full coupled inverse is asserted |
| Formal delayed phase core and reverse column | `lem:reduced-flow-phase-defect`, `prop:delayed-phase-event-core` | Exact complete-history phase-delay differential, exact annihilation of constant phase, an $O(\delta[1+\log(r_{\rm out}/\rho_\delta)])$ action bound, and a dimension-uniform delayed scalar phase inverse. The two phase-induced normal sources are identified exactly, including the affine-residual derivative. The collar is the formal $q_0$-flow collar; no raw-compatible collar identification, affine-residual solution bound, or full Schur inverse is asserted |
| Event-aligned normal traces | `prop:event-aligned-normal-traces` | Exact triangularization of raw moving terminal traces by a fixed-$r$ quotient; the scaled event-time unknown disappears from homogeneous normal rows, and the reduced-base trace column is zero. A terminal-relative translation conjugacy preserves fixed-base kernel bounds. Raw trace differentiation instead costs one derivative and a sharp $\delta^{-2}$ strong-norm factor. No moving-family flushing or nonlinear tracker is asserted |
| Terminal-relative trace-scale coordinates | `lem:terminal-relative-trace-scale-chart` | Exact nonlinear $C^2$ translation--restriction coordinates from a supplied $C^{d+2}$ terminal buffer to retained $C^d$ moving-window traces. The event displacement is retained, $E=r^\#(0)-e_1$ is the derived fixed-section row, nonzero-base terminal columns and mixed second derivatives are explicit, pure reference translations cancel, and raw first/second translation derivatives cost $\delta^{-2}$/$\delta^{-4}$. This is neither a same-space chart nor a construction of the strong buffer, parameterized solution family, moving-event residual/inverse, endpoints, tracker, or root |
| Endpoint-centered duration selector | `lem:endpoint-centered-duration-selector` | On a supplied fixed forward envelope, all fixed bulk, collar, seam, causal-entry, and attracting finite-row duration columns vanish.  The only raw moving terminal columns are $p_*'/\delta$ and $Z_*'/\delta$; they factor exactly through the normalized event row.  An explicit range shear yields the triangular derivative $[[L^{\rm ea},0],[\ell_{\rm ter},c_{\rm ter}]]$, with $c_{\rm ter}=q_{*,e}/q_{0,e}$ and, conditional on the supplied reference having the structured scalar terminal germ, $c_{\rm ter}\in[1/2,3/2]$.  Affine duration lifts alter the upper column but preserve the Schur scalar, while event range shears preserve only complete-operator equivalence.  No endpoint reference, diagonal-uniform hybrid inverse for $L^{\rm ea}$, endpoint parameter family, past orbit, or root is constructed |
| Shifted phase-to-normal action response | `prop:phase-delay-action-shift`, `prop:structured-phase-action-green` | Exact shift $p^\sharp=p+\varepsilon P$, structured bulk sources including the affine-residual derivative, shifted attracting and repelling boundary rows, and dimension-uniform true-action bound $O(r_{\rm out}^2+\delta/S_\delta)$. The old normalized-state reverse column is explicitly not uniformly bounded |
| Vanishing base raw-collar correction | `lem:raw-compatible-base-collar-refinement` | The base correction is $O(\varepsilon|e|)$ and therefore $O(\delta^3S_\delta)$ at the inner sections, and this scale is sharp in a quadratic example. This is an independent preparatory refinement; it does not replace the sharply $O(\varepsilon)$ moving-endpoint column used in the Schur inverse and constructs no past orbit |
| Raw-compatible zeroth-order phase--normal border | `lem:raw-phase-boundary-column-assembly`, `thm:raw-compatible-phase-normal-inverse` | Exact boundary column $E_0a\,\gamma_e^{\rm ph}$, repelling closed $p(0)$ feedback and shifted terminal row, total action $O(r_{\rm out}^2+\delta/S_\delta+\delta^{2-2\vartheta})$, and a dimension-uniform Schur inverse for $x=T_\sigma^{\rm rc}a+y$ in the graph norm controlling the normal operator domain, $a$, and the scaled event time. Fixed reduced base and order zero only; no higher jets, moving nonlinear family, tracker, speed sign, past orbit, or physical root |
| Inner-anchored nonlinear phase core | `lem:inner-anchored-nonlinear-phase-chart`, `prop:inner-anchored-relative-phase-schur` | Exact nonlinear chart $\Theta_a=\Phi_{q_0}^{a(r)}(r)$ and action $q_0(r)q_0(\Theta_a(r))a'(r)$, with fold-side anchor and same-sign/orientation preservation for a prescribed pulled-back scalar speed residual in the natural weighted class. Its one-row relative-phase linearization has a dimension-uniform fixed-base raw-compatible Schur inverse and pointwise action $O(r_{\rm out}\{r_{\rm out}+S_\delta^{-2}+\delta^{2-2\vartheta}\})$. This removes the constant-phase obstruction only at the scalar phase/fixed-base linear level; no nonlinear normal tube, terminal-time variable, tracker, past orbit, or physical root is asserted |
| Inner-anchor endpoint-recut obstruction | `prop:inner-anchor-endpoint-recut-obstruction` | An explicit admissible scalar phase source gives wrong-sided outer endpoint displacements on both branches and forces $|\widehat\tau|/\rho_\delta\to\infty$ and $(|\widehat\tau|/\delta)/S_\delta\to\infty$ at fixed $r_{\rm out}$. Hence the inner-anchored relative inverse, strict scalar speed sign, and $O(S_\delta)$ interior buffers do not imply literal original-endpoint recutting. Here $\widehat\tau$ is an algebraic bordered-row coordinate, not a constructed physical event time. This is a phase-core nonimplication theorem, not an assertion that the source is a full RFDE residual or that model-specific cancellation is impossible |
| Receding-collar causal flight time | `thm:receding-collar-causal-flight-time`, `rem:exact-endpoint-flight-moment` | For a prescribed Eulerian scalar speed $q=q_0+\widehat Q<0$, the difference $\beta$ of the perturbed and reference flight-time coordinates solves the exact nonlinear bordered problem $q_0^2\beta'/(1-q_0\beta')=\widehat Q$, $\beta(e_0)=0$, $\beta(e_1)+\widehat\tau=0$. On $r_{{\rm out},\delta}=\varkappa_{\rm ep}(\delta S_\delta^3)^{1/2}$, the structured source class has $|\widehat\tau|=O(\rho_\delta)$, fold-time correction $O(S_\delta)$, an exact causal scalar-coordinate hit at the original endpoint, analytic source dependence, and a dimension-uniform action-weighted scalar terminal Schur inverse. The exact moment identity proves that cancelling only the linear duration moment is insufficient. This theorem prescribes an Eulerian source; by itself it does not identify the reference-pulled RFDE source or close the moving normal column |
| Reference-pulled scalar endpoint | `thm:reference-pulled-causal-endpoint`, `eq:reference-pulled-source-class` | For every prescribed structured source in the stated reference-coordinate class, solves the causal phase IVP, shifts the reference terminal point by the $q_0$ flow, and proves the exact conjugacy $q_E(\Theta_a(r))=q_0(r)\Theta_a'(r)$. The scalar path reaches the original scalar-coordinate endpoint with exact terminal coefficient $q_E(e_1)/q_0(e_1)\in[1/2,3/2]$. Membership of the source produced by the still-open moving RFDE BVP in this class, and the off-diagonal moving-duration correction, are not included |
| Diagonal fixed-base phase--normal inverse | `cor:diagonal-raw-compatible-phase-normal-inverse`, `lem:current-absorbed-delay-splitting`, `lem:repelling-component-generations` | On $R_\delta=\varkappa(\delta S_\delta^3)^{1/2}$ the raw-compatible fixed-reference order-zero phase--normal graph inverse is uniform in $N,\delta$.  The component splitting deletes zero-delay differences, absorbs current terms, and resums the forward-transverse/future-scalar current loop before strict delayed generations are counted.  This fixed-base result has no moving-duration column, endpoint reference, or full terminal Schur factor |
| Joint diagonal wedge and kinetic bound | `lem:joint-diagonal-wedge-kinetic` | Replaces an impossible fixed-$\delta$ rectangle in $0<\varkappa\le\varkappa_0$ by the admissible wedge $\delta/R_\delta^2\le\mathfrak w_*$.  On that wedge the Green, terminal, three-summand, speed-row, phase-projection, and affine-border constants are joint in $(N,\delta,\varkappa)$, $\Omega_{\rm aff}\le C\{\varkappa^2+S_\delta^{-2}+\sqrt\delta S_\delta^{7/2}\}$, and the causal slice $a(e_0)=0$ gains the strong kinetic estimate $O(\lambda_\delta\|a\|_{\mathsf A_{\rm hyb}})$.  The wedge is essential: for fixed $\delta$, taking $\varkappa\downarrow0$ makes $R_\delta<\rho_\delta$ and $\delta/R_\delta^2$ diverge |
| First-order terminal component sources | `prop:diagonal-terminal-component-green` | On explicit $O(S_\delta)$ terminal windows ending at $+\rho_\delta$ and $-R_\delta$, arbitrary continuous incoming histories, one scalar boundary row, and distributed $(F,H)$ sources have a dimension-uniform $m_\delta$-weighted first-order Green estimate.  The strict-delay numbers are $O(\varepsilon/m_{a,T})$ and $O(\varepsilon/m_{r,T})$, incoming terminal-interface data are flushed from the final history window when the distributed sources vanish, and the reconstructed speed and local terminal phase increment are controlled.  The data norm is specified independently of the solution.  This is a fixed-reduced-path terminal propagator, not the rough-middle-to-incoming trace/prefix map, the structured phase column in the same strong norm, a bound for the event shear $K$, a higher jet, an endpoint RFDE family, or a physical root |
| Terminal raw-compatible phase column | `prop:raw-compatible-terminal-phase-column` | The raw-compatible structured phase response enters the first-order terminal norm uniformly in the shifted coordinate $p^\sharp=p+\varepsilon P$.  On the causal-entry phase space the physical $(Z,p)$ column is stronger: its terminal norm is $O(\rho_\delta)$, as are its data before propagation, while its true terminal speed and local phase action are $O(\rho_\delta m_{\sigma,T})$; the additive entry-collar column is separately flushed from the final history window.  Only one phase derivative is used.  The distinction is essential: on the full $\mathsf A_\phi^1$ space the attracting physical $p$ column has a genuine $S_\delta$ loss.  No rough-middle trace, event shear $K$, endpoint reference, moving-duration inverse, or physical root is included |
| Terminal-free diagonal bulk trace | `prop:diagonal-bulk-terminal-prefix-trace` | For the explicit direct data class of $\lambda_\delta$-scaled old-normal data whose distributed sources vanish on the terminal buffer, with $b_r=0$, the fixed normal inverse produces $O(\lambda_\delta)$ global state, weighted speed, incoming terminal data, full first-order terminal trace, and local speed/action.  Every causal prefix is estimated before, and graph membership is deduced after, applying the solution operator; the final history window gains the terminal flushing factor.  The upper-bound ledger contains $\lambda_\delta R_\delta^2/\rho_\delta=2\alpha\varkappa^2+o(1)$, so no $\delta$-small prefix contraction is claimed.  Unit rough data, nonzero repelling terminal rows, localized terminal endpoint/event columns, $K$, the hybrid inverse, endpoint RFDE family, and physical root remain outside the result |
| Localized diagonal normal boundary columns | `prop:diagonal-boundary-prefix-terminal-trace` | For direct zero-distributed-source columns $(\gamma_0,b_\sigma,0,0)$, including the repelling terminal scalar row, the diagonal normal inverse gives a uniform global state and weighted speed.  The exact $H=0$ recovery identity rewrites the speed through $p'$, and cellwise integration by parts controls every causal prefix by $\varepsilon\{1+\log(R_\delta/\rho_\delta)\}$ times the direct data norm; after $\rho_\delta$ normalization the factor is $\eta_{{\rm bd},\delta}=O(\delta S_\delta)=o(1)$.  The causal phase lift is localized in $\mathsf A_\phi^1$, the full terminal recut is uniformly $\mathsf T^1$, and the attracting column and repelling entry-history column flush from the final window.  The repelling terminal scalar column is proved not to flush because $p_r(S_r)=b_r$.  This closes the localized normal boundary half of the source split, not a freely prescribed terminal voltage-history row, the event shear $K$, source-split hybrid assembly, an endpoint RFDE family, or a physical root |
| Terminal-supported distributed source extension | `prop:diagonal-terminal-source-extension` | The component Green formulas extend directly to piecewise-$L^\infty$ distributed sources supported on the terminal buffer, in a solution-independent norm using the natural scalar scale $r_{\sigma,T}m_{\sigma,T}$.  The response has a branchwise state bound, global weighted-speed control, and a full first-order terminal trace.  Only the causal prefix gains $m_{\sigma,T}$, with $m_{a,T}\asymp S_\delta^{-2}$ and $m_{r,T}\asymp R_\delta$; neither the whole state nor the terminal trace is claimed small, and no final-window flushing holds while the source remains active.  This is a fixed-envelope linear result, not nonlinear residual membership, a moving endpoint, or a root |
| Three-summand causal-entry core | `thm:diagonal-source-split-hybrid-core`, `cor:terminal-source-split-hybrid-core` | The terminal-free bulk, zero-source boundary columns, and terminal-supported $L^\infty$ sources form a unique $\ell^1$ direct range before inversion.  The fixed phase--normal operator is a dimension- and diagonal-uniform isomorphism on that range.  Its returned speed is $O(\lambda B+D+T)$, while the normalized prefix is $O(B+\eta_{\rm bd}D+m_{\sigma,T}T)$; a pure terminal source has an $O(m_{\sigma,T})$ event return.  Terminal histories remain observations, not onto RFDE history rows.  No nonlinear split lemma, contraction, moving duration, endpoint reference, or root is asserted |
| Speed-aligned repelling terminal row | `prop:repelling-speed-aligned-terminal-row` | Replacing the future scalar row by the exact row $\varepsilon Q_e$ preserves the fixed-phase normal isomorphism because its pure terminal-column coefficient is $1+O(R_\delta^2+\varepsilon/R_\delta+\mathcal E_{r,T})$.  For a supplied original-endpoint reference satisfying the proposition's terminal normalization, a nonlinear zero gives exactly $Q_e=0$, $q_{*,e}/q_0(e)=1$, $K_p=R_q(e)=O(\varepsilon)$, and $\kappa_p=O(\rho_\delta/R_\delta)=o(1)$.  The terminal phase slack of the later fixed-envelope zero is not shown to vanish, so these original-endpoint consequences cannot be transferred to it without the moving-duration construction |
| Causal-entry weighted-action inverse and rough-source loss | `lem:causal-entry-prefix-action-core`, `thm:diagonal-causal-entry-prefix-action-inverse`, `prop:rough-normal-prefix-action-obstruction` | The fixed-reference order-zero phase--normal operator with the causal entry row is a dimension- and diagonal-uniform isomorphism after the normal range is charged for the weighted speed and records every prefix $\sup_r|\int_{e_0}^r Q/q_0^2|/\rho_\delta$.  On this global source class the prefix summand is uniformly controlled by the weighted-speed summand; it is retained to expose terminal action, not claimed to be independently necessary.  The returned raw-compatible phase column is $o(1)$ in this norm.  The no-delay normal direction $p=\varepsilon r$ has old rough data norm $O(1)$ but forces weighted action and causal phase of exact order $S_\delta^2$, proving that the old rough norm cannot replace the stronger graph charge.  Delay-dependent returned columns are only an $o(1)$ correction.  This theorem has no terminal event row, localized source-split norm, strong terminal history, moving-duration column, or physical root |
| Relative anchored phase-to-state recovery | `prop:relative-structured-phase-response` | The exact delay profile is $O(\delta)$ in the relative phase norm; its original-variable normal sources yield returned normalized state, shifted resource defect, and pointwise true action of size $O(r_{\rm out}+S_\delta^{-1})$. The resulting relative graph--action norm is uniformly equivalent to the anchored graph norm. The estimate is fixed-base and linear and uses $|a(r)|\le |r|\|a\|_{\phi,\mathrm{rel}}$ essentially; by itself it supplies no nonlinear remainder, nonlinear old-history assembler, tracker, past orbit, or physical root |
| Exact nonlinear formal phase-delay defect | `lem:nonlinear-reduced-flow-phase-delay` | Exact $q_0$-flow complete-history functional $\Pi_{\sigma,N}$, with $D\Pi(0)=\mathscr P_{\sigma,N}$, exact constant-phase annihilation, and dimension-uniform two-point quadratic remainder $O(\delta|r|)$ in both value and piecewise derivative. This is the formal reduced-flow history only; it does not identify the nonlinear raw-compatible collar, supply its second endpoint jet, close the full nonlinear normal residual, or construct a physical history/root |
| Fixed-reference nonlinear raw-history assembler | `lem:second-jet-raw-history-assembler` | Direct finite-recursion construction of the raw-compatible old-history segment on one fixed-reference cap ball, with a same-sign enlargement covering all four closed endpoints, two endpoint derivatives, overlap agreement with the original collar chart, and an $\varepsilon^{-1}$-normalized quadratic graph remainder. By itself it closes only the history-boundary nonlinearity; it is not a past orbit, tracker, physical connection, or root |
| Fixed-section nonlinear graph--action residual | `thm:fixed-section-nonlinear-graph-residual` | Exact assembly of the nonlinear formal phase delay, canonical zero-core raw-compatible history rows, resource-defect normal equations, and inner phase anchor on one fixed graph space. The map is $C^1$, has base defect $O(r_{\rm out}+S_\delta^{-2})$, linearizes exactly to the existing dimension-uniform anchored Schur isomorphism, and has a uniform quadratic/two-point remainder. It does not assert a zero, a moving terminal event, a past orbit, a physical connection, or a root |
| Canonical fixed-section zeros | `cor:fixed-section-canonical-zero` | A uniform contraction solves the fixed-section residual at every fixed admissible parameter pair. On each outer branch the zero is unique in the canonical graph slice, is $O(r_{\rm out}+S_\delta^{-2})$, has the displayed first Newton jet and strict speed sign, and reconstructs an exact finite forward segment of the unmodified RFDE. No parameterized branch, moving event, past orbit, invariant sheet, cross-branch handoff, physical connection, or canard root is asserted |
| Fixed-envelope RFDE segment with vanishing repelling terminal speed correction | `thm:fixed-envelope-speed-row-zero` | Hard-splits the exact nonlinear normal residual into bulk, boundary, and terminal summands, uses the speed-projected phase coordinate, and contracts about the $O(1)$ affine bulk predictor in an anisotropically scaled correction norm.  On the admissible wedge it constructs a unique nearby fixed-envelope RFDE segment in the stated affine causal star ball, preserves strict speed sign, and gives $Q_r^{\rm nl,\flat}(x_r^{\rm fe},a_r^{\rm fe})(e_{r,1})=0$ on the repelling branch.  The normal bulk correction is $O(\mathfrak b)$ but its kinetic state contribution is $O(\lambda_\delta\mathfrak b)$; the phase/slack correction is $O(\mathfrak b^2)$.  The row $\tau=-a(e_1)$ only records the mismatch $\Theta_a(e_1)=\Phi_{q_0}^{-\tau}(e_1)$, so this is not a moving-duration or original-endpoint theorem and gives no past orbit, connection, or root |
| Post-flushing terminal second slow jet | `thm:fixed-envelope-terminal-slow-jet` | Differentiates the exact physical fold-time tracker once, keeps every tangent and delayed-tangent term inside the component operator, and flushes the incoming transverse tangent before the protected selector window.  The repelling future tangent row is fixed exactly by $p_s(S_r)=\delta R_q(r_r^{\rm fe}(S_r))$, rather than by a coarse $Q_s/\varepsilon$ estimate.  It proves $\|Z_s\|\le C\varepsilon\delta/\rho_\delta$ and $\|Z_{ss}\|\le C\varepsilon/\rho_\delta$ not only at $L=0$ but throughout the reserved offsets $0\le L\le(A-A_{\rm fl})S_\delta+1$.  This closes the slow-jet size condition used by the actual slow-clock history column below.  The estimate is not a claim about the raw full state, arbitrary terminal $L^\infty$ sources, an original endpoint by itself, a past orbit, a connection, or a root |
| Exact slow terminal clock and physical-event border | `lem:terminal-clock-pullback-border`, `cor:fixed-envelope-terminal-clock-border` | Pulls the unmodified variable-duration RFDE exactly to the old fixed interval by $\Xi_\beta=s+(\beta/\delta)\chi_\delta$, fixes both old and terminal complete histories, and replaces every constant delay by the exact causal foot $\Xi_\beta^{-1}(\Xi_\beta(s)-\theta_k)$.  The fully typed identity is $C_{\rm up}+L_{\rm up}A_\chi=Kc_{\rm ter}$.  Spreading the transition over $a_\chi S_\delta$ makes the foot displacement $O(\mathfrak b)$ and its first two normalized clock derivatives $O(1)$ on the original joint wedge.  The clock lift is not uniformly bounded in the old weighted hybrid phase norm; uniformity is correctly stated in the pullback norm $\|v-A_\chi\beta\|+|\beta|/\rho_\delta$, with the analogous event-aligned range norm, and no raw-product norm equivalence is claimed.  On the explicit closed range of continuous terminal sources, the complete physical-event differential and genuine free history-interface unknown have a dimension-uniform inverse; no right-hand envelope or additional matching subwedge is used.  This is a differential theorem, not yet the nonlinear endpoint segment, parameter family, past orbit, connection, or root |
| Fixed-parameter original-endpoint RFDE segment | `thm:short-clock-original-endpoint-segment` | A clock-aligned strong-space two-point estimate and local contraction correct the fixed-envelope event defect and produce one exact raw-compatible forward segment of the unmodified RFDE at each fixed admissible parameter pair.  Its physical duration reaches the literal original scalar endpoint, its terminal history is the actual complete history, and on the repelling branch $Q_e=0$, $c_{\rm ter}=1$, and $K_p=R_q(e)=O(\varepsilon)$; the actual $K_Z$ and terminal $Z_s,Z_{ss}$ have the uniform slow scales.  The new segment's sharp jet is not inferred from the coarse zero bound: it is re-proved with the $O(\varepsilon\mathfrak b)$ terminal-state ledger and the explicit scale $\mathcal E^{\rm jet}\mathfrak b\rho_\delta/\delta^2\to0$ on both branches.  Uniqueness is asserted only in the displayed clock-aligned $O(\mathfrak b)$ ball.  The canonical entry is not a past-complete orbit, and no action-weighted parameter/gauge family, branch-to-branch connection, preparation-independent relation, or physical root is constructed |
| Raw-gauge fixed-section zeros | `thm:raw-gauge-fixed-section-zero` | The canonical zero extends to a nonempty, infinite-dimensional gauge-indexed class of small $O(\varepsilon)$ raw-compatible attracting and repelling boundary data in the stated natural boundary norms. Each gauge slice has a unique small zero, with a uniform first gauge jet, persistent inverse, fixed-graph $C^1$/Lipschitz dependence, strict speed sign, and exact finite raw-RFDE reconstruction. The theorem does not assert past-orbit generation of the gauges, a common recut for comparing trackers, flat forgetting, parameter jets, physical endpoints, a sheet, connection, or root |
| Generated-interior tracker representatives | `cor:generated-interior-canonical-tracker` | On every retained subsegment whose delay collar lies beyond the first maximal delay, every raw-gauge fixed-section zero admits a physical-coordinate parameterization with exact scalar backtracks, exact uncut outer-history invariance, and the actual generated RFDE history window. Uniform $q$, $V'$, and $W'$ collar bounds realize the stationary and resource quotients, including an $O(S_\delta^{-1})$ Volterra correction. No common-chart gauge comparison is proved for the full reparameterized trackers on their moving domains; only the subsequent fixed interior hit maps have $C^1$ gauge dependence. No flat forgetting, physical endpoints, parameter family, past-complete orbit, branch handoff, connection, or root is asserted |
| Common generated buffer and physical interior hit | `prop:raw-gauge-physical-hit` | At fixed parameters, the sections $r=\pm r_{\rm out}/2$ lie in a common generated buffer for the raw-gauge family. The weak complete-history family is jointly $C^1$ in time and gauge there; each section has a unique hit, and the scaled hit time and hit history have dimension- and $\delta$-uniform first gauge bounds. The hit derivative is exactly $(I-\tau\varrho_N)D_g\mathcal Z$. This is not a $C^2$ strong terminal buffer, a physical-endpoint recut, flat forgetting, a parameter family, a sheet, connection, or root |
| Common strong physical-hit buffer | `prop:raw-gauge-strong-hit-buffer` | On both branches the common generated neighborhood is time-$C_\delta^3$ and $C^1$ in the raw gauge, with dimension- and $\delta$-uniform annular component bounds. A fixed-reference window of length $O(S_\delta)$ with an $O(\delta^{-1})$ chart enlargement supplies the strong input to the terminal-relative trace chart; raw moving recut loses at most $O(\delta^{-2})$. No second gauge derivative, normalized terminal Schur smallness, nonlinear flushing, flat forgetting, endpoint/asymptotic object, connection, or root is asserted |
| Local physical-hit quotient flushing | `prop:physical-hit-quotient-flushing` | On an $AS_\delta$ window centered at either actual fixed-section hit, the exact resource-gauge quotient satisfies a dimension-uniform finite-window Green/Lyapunov--Perron estimate. Attracting influence is propagated from the left; repelling influence is split between the left stable trace and the right one-dimensional current-unstable trace. The contraction is RFDE-specific and yields $\exp\{-cS_\delta\log(1/\delta)\}$ interior decay without backward RFDE evolution. Fixed parameter and already constructed trackers only: no global normal bundle, new BVP inverse, parameter jets, sheet, connection, or root |
| First-order raw-gauge flat physical-hit class | `thm:physical-hit-first-order-flatness` | The exact stationary event quotient and resource reconstruction turn local quotient flushing into $O(\delta^\infty)$ first-gauge-derivative and pairwise raw-gauge equivalence of each complete fixed-section hit history, uniformly in $N$ in the natural $\varepsilon^{-1}$ event norm. This is asymptotic, fixed-parameter, and local to the two separate interior hits. It does not make hit times flat, give exact finite-$\delta$ gauge independence, supply second gauge/parameter jets, recut original endpoints, connect the branches, or prove a physical root |
| Fixed-reference parameter-coherent physical hits | `lem:fixed-reference-parameter-residual`, `prop:parameter-coherent-physical-hit-family` | A fixed rough graph chart avoids the false differentiability of translating piecewise-$W^{1,\infty}$ paths.  An explicit triangular collar/bulk row isomorphism gives an exact $C^4$ forward-RFDE residual, and its zero family has the full rectangular parameter jet, fixed-parameter $C_g^3$ jet, the precise mixed staircase $\mathcal K_{\rm phys}$, a triangular time-jet ledger, uniform two-sided hit margin, and complete-history event reconstruction.  Uniformity is in $N$, $\delta$, and the branch.  The result is relative to one fixed reference chart and its finite boundary rows; it proves neither reference-chart covariance, a past orbit, original endpoints, nor a cross-branch relation/root |
| Rectangular-jet raw-gauge forgetting at physical hits | `thm:physical-hit-rectangular-flatness` | Differentiating the centered finite-window Lyapunov--Perron equation on one fixed fading space gives $O(\delta^\infty)$ for every hit-map derivative in $\mathcal K_{\rm phys}$ containing at least one gauge slot.  Direct endpoint Faà di Bruno expansion then proves pairwise $\mathcal J_{\rm phys}=(C_\nu^1C_\eta^2)\cap(C_\nu^2C_\eta^1)$ equivalence for every uniformly tame $(N,\delta,\sigma)$ gauge family, using $D_g^3$ but no $D_g^4$.  Pure parameter response of one representative is retained.  The theorem gives two separate reference-relative local hit classes, not terminal Schur control, original-endpoint recutting, a repelling sheet, connection gap, or physical root |
| Attracting finite-generation flushing | `lem:current-absorbed-delay-splitting`, `prop:attracting-finite-generation-flushing` | Exact deletion of zero-delay differences, current absorption for positive delays, a fixed seam-partition Banach space, and an order-dependent finite-generation estimate taking arbitrary strong attracting collar data to a genuine slow exit history with dimension-uniform normalized operator norm tending to zero. Fixed parameter only; no phase coupling, tracker, or parameter jet |
| Repelling component-kernel flushing | `lem:repelling-component-generations`, `prop:repelling-component-flushing` | Weighted full-branch coefficient jets; a resummed current loop with forward transverse and future scalar kernels; exact recursive-delay generation count on one additive seam space; and inner-history/terminal-scalar handoff estimates obtained by oriented words and a localized terminal first-exit action. The normalized component traces tend to zero uniformly in network size. Fixed parameter and fixed phase only: no high-order compatible `p(0)`-collar feedback, coupled phase--normal inverse, nonlinear tracker, speed sign, or physical root |
| Compatible repelling-collar closure | `prop:compatible-repelling-collar-closure` | High-order closure of the raw-compatible scalar $p(0)$-to-history feedback, with no extra Fredholm row; separate closed-loop collar and terminal columns; and a cross-column action/generation estimate preserving both normalized handoff limits uniformly in network size. Fixed parameter and fixed phase only; no phase-to-normal/event border, nonlinear tracker, speed sign, or physical root |
| Truncated reduced actions | `cor:outer-reduced-actions` | Formal critical-curve speed and two positive truncated actions for the reduced critical-layer equation; not an invariant slow-history action |
| Weak-selection obstruction | `prop:backward-asymptotic-nonselection` | A common phase row, convergence in an unnormalized history norm, and superalgebraic strong-history closeness do not by themselves select a unique tame RFDE history family; generic logical counterexample, not a model-specific impossibility theorem |
| Obstruction to exact root canonicity | `prop:finite-section-noncanonicity` | Shared-resource localized target-frozen completion bump plus trace/root IFT |
| Abstract mechanism beyond one model | `thm:hidden-return-schur` | Cokernel Schur quotient, coordinate/range invariance, uniform norm bound |
| Whole-line collective cokernel | `lem:fold-gaussian-cokernel` | Explicit fundamental pair and weighted Green inverse |
| Nonlinear persistence | `cor:schur-to-root` | Uniform range-to-root theorem plus Schur profile identity |
| First return channel | `thm:shared-resource` | Markov inverse followed by heterogeneous fast curvature |
| Second return channel | `thm:sensed-recovery-response` | Markov inverse followed by heterogeneous slow recovery sensing |
| Fixed-network genericity | `thm:response-directions`, `thm:sensed-recovery-response` | Nonzero bounded covectors; codimension-one kernels |
| Sparse/high-rank realization | `cor:reset-cycle-response`, `cor:pure-sensing-response` | Directed reset cycle, nonnegative chosen-base-layer-support-preserving perturbations, and rank-`N-1` directions |
| Graph/preparation logical closure | Selection convention `(S1)--(S4)`, `lem:graph-only-retained-expansion`, `lem:preparation-existence` | Concise main-text interface; graph-only retained-tube theorem and construction in the supplement |
| Exact finite-section bridge | `prop:finite-gap-bridge` | Endpoint, tail, moving-trace, parameter, graph-jet, and preparation errors |

## Main novelty boundary

- The principal contribution is the conjunction of exact atomwise projection blindness,
  pure-redistribution control of every transverse source by two separated
  delays, sharp `N`-uniform inverse bounds, and nonlinear complete-history
  root readout.
- Schur elimination, one-dimensional cokernel projection, and recovery of a
  finite-dimensional functional from a right inverse are standard operations
  and are not priority claims.
- The observation theorem reconstructs the compressed return covector for a
  known network skeleton.  It does not reconstruct the hidden network.
- Pairing estimates are uniform over the unit probe ball under the compatible
  base-layer and common preparation hypotheses stated in the corresponding
  corollaries.  Coordinate recovery
  from finitely many noisy probes is not `N`-uniform without a lower frame
  bound, and root measurement noise is amplified by
  `delta^(-3)|zeta|^(-1)`.
- Conormal and Melnikov geometry are not priority claims in isolation.  The
  new conjunction is exact projection blindness, sharp two-delay transverse
  range, dimension-uniform history return, and identification of that same
  covector as the derivative of a fixed-model complete-history heteroclinic
  canard.

## Two model dictionaries

The common blind source is

```text
h_*(R) = (K/(2 alpha)) A_N^(-1) P_perp,N
         (sum_k theta_k R_k) 1.
```

The fast-curvature model returns

```text
Lambda_curv(R) = -(1/alpha) pi_N^T(c_N o h_*(R)).
```

The sensed-recovery model returns

```text
Lambda_rec(R) = pi_N^T((varpi_N-c_N/alpha) o h_*(R)).
```

The limits separate exactly:

- `varpi_N = 1` recovers pure curvature return;
- `c_N = alpha 1` kills curvature return but permits pure sensing return.

## Literature boundary

- Exact lumpability requires factorization through projected history; the
  paper proves equality at each common unreduced history without closure.
- Mori--Zwanzig theory is a conceptual baseline for unresolved return; the
  paper does not derive a memory kernel or generalized Langevin equation.
- Nonidentifiability is from the projected-functional summary, not structural
  input--output unidentifiability, nonlinear-delay observability, or recovery
  of unknown DDE parameters.
- Adjoint/covector sensitivity for time-lag systems is standard.  The new
  step is the exact blind-source factorization, dimension-uniform history
  return, and nonlinear complete-history root remainder.
- Delayed-network reconstruction literature recovers edges, delays, or
  dynamics from data.  Here the network and delays are known and only one
  compressed return covector is reconstructed.
- Existing network canard, Banach-space canard, RFDE Fredholm, and Lin results
  are neighboring tools; no priority claim is made for those theories.

## Quantifier boundaries

- Uniformity is over finite networks with common Dobrushin, delay-support,
  coefficient, structural-ball, and bounded anchor-class constants.
- Preparation independence is pairwise for fixed preparations on intersected
  parameter boxes; it is not a single bound over an unbounded preparation
  class.
- The no-go theorem concerns the stated finite-section axioms.  It does not
  rule out a canard selected by physical outer invariant manifolds.
- The flagship conormal belongs to the exact fixed anchored-model
  complete-history connection locus.  It is independent of proof preparation.
  Exact baselines for different anchor multipliers are not identified; after
  modelwise centering, their first weighted conormals converge uniformly to
  `(1,-Lambda_N)`.  No root or maximal canard is claimed for the original
  unanchored recovery law.  Issue #11 concerns a different Paper III model and
  is not an input to Paper A.
- The preparation-independent critical curve, frozen-resource
  positive-`delta` voltage-history splitting, truncated reduced actions,
  exact tracker/quotient identities, physical-backtrack calculus, and
  principal finite-endpoint Green splitting are proved precursors.  The exact
  nonlinear resource-defect normal form and raw-compatible endpoint collar
  chart are also proved.  The quotient identities assume an exact tracker,
  while the collar chart is not a right inverse for arbitrary Green sources;
  a proved boundary-layer obstruction forces a hybrid slow/action coupling
  on a finite method-of-steps buffer.  The exact fixed-delay fold-time normal
  form now identifies the correct system and collar interface for that
  coupling.  Its fixed-phase `C^0` complete-history Green inverse is proved,
  including the repelling collar feedback without an extra row.  The
  separately bordered scalar phase--event core is also explicit.  The
  attracting and repelling high-order finite-generation component buffers
  are now proved, including the repelling scalar-terminal first-exit
  localization.  The high-order compatible `p(0)`-collar feedback is now
  closed, and the normalized normal-to-phase action column is
  $O(r_{\rm out}^2+\delta^{2-2\vartheta})$.  The exact formal reverse
  phase-delay column, its scalar delayed inverse, and fixed-`r`
  event-aligned normal trace are also proved.  The exact phase-delay shift
  and structured action estimate are now proved.  The raw-compatible collar
  is assembled as a boundary column, the affine-residual bulk response is
  controlled in the shifted/action space, and their combination closes the
  fixed-reduced-base zeroth-order phase--normal inverse in a graph norm.
  The base raw-collar correction is $O(\varepsilon|e|)$, and the
  inner-anchored nonlinear phase chart plus its relative one-row Schur
  inverse remove the constant-phase obstruction at the scalar
  phase/fixed-base linear level.  The endpoint-recut obstruction now proves
  that these scalar hypotheses allow wrong-sided outer endpoints and
  bordered fold-time scales much larger than an $O(S_\delta)$ window.
  The receding-collar flight-time theorem now supplies the correct exact
  scalar replacement: a causal scalar-coordinate hit at the original
  endpoint, nonlinear duration
  moment, $O(S_\delta)$ terminal window, and normalized scalar Schur row.
  The reference-pulled theorem now conjugates every prescribed structured
  reference-coordinate source in its stated class to that Eulerian endpoint
  problem; membership of the source produced by the open moving RFDE BVP
  remains unproved.  Independently, the re-audited
  order-zero raw-compatible phase--normal graph inverse is uniform on the
  receding diagonal.  Its causal-entry restriction is now also uniform in
  the stronger weighted-action graph norm; its weighted-speed term already
  controls the explicitly recorded prefixes on this scale.  The exact
  direction $p=\varepsilon r$ proves that reverting to the old rough norm
  incurs the unavoidable loss
  $R_\delta^2/\rho_\delta\asymp S_\delta^2$ in the no-delay normal block;
  delay-dependent return columns are only a relative $o(1)$ correction.
  The terminal proof now implements the required split between
  $\lambda_\delta$-scaled structured bulk, zero-source boundary columns, and
  terminal-supported distributed sources; it does not use the old
  unrestricted rough norm.
  Separately, the branchwise first-order terminal component theorem now
  handles arbitrary distributed sources on explicit $O(S_\delta)$ windows,
  with the natural weight $m_\delta(r)=|r|+\varepsilon/|r|^2$, strict-delay
  numbers $O(\varepsilon/m_{\sigma,T})$, and a local terminal action bound.
  When the distributed sources vanish, it also flushes incoming-interface
  data from the final window.  It starts from an explicitly supplied incoming
  terminal history.  The raw-compatible structured phase column is now also
  closed in this first-order norm: uniformly in shifted coordinates on the
  full action space, and with an $O(\rho_\delta)$ physical-column bound on the
  actual causal-entry space.  The entry-collar contribution is separately
  flushed.  The $\lambda_\delta$-scaled, terminal-free old-normal bulk
  trace is now also closed directly: its causal prefix is estimated before
  graph membership is concluded, its incoming and full terminal traces are
  $O(\lambda_\delta)$, and its final window is flushed.  This result
  deliberately excludes a nonzero repelling terminal row and records that
  the normalized global prefix has an $O(\varkappa^2)+o(1)$ upper-bound
  budget rather than a $\delta$-small one.  The localized boundary columns
  are now closed, and a direct piecewise-$L^\infty$ terminal-source Green
  extension supplies the third summand with an $O(m_{\sigma,T})$ causal
  prefix.  Their three-summand causal-entry core is a uniform isomorphism.
  The exact speed-aligned future row $\varepsilon Q_e$ also has coefficient
  $1+o(1)$ and forces $K_p=R_q=O(\varepsilon)$ on a supplied
  original-endpoint germ satisfying the selector normalization.  On the
  admissible joint wedge, the exact fixed-envelope nonlinear residual now
  belongs to the three source summands and contracts in an anisotropic
  correction norm.  Its zero has strict physical speed sign and
  $Q_r^{\rm nl,\flat}(x_r^{\rm fe},a_r^{\rm fe})(e_{r,1})=0$ as a terminal
  speed correction.  Its phase slack is not shown to vanish, and the
  original-endpoint normalization does not hold at that fixed-envelope zero.
  The fixed-envelope second-order terminal $Z$ jet is now closed on a
  reserved $O(S_\delta)$ post-flushing window.  An exact slow terminal-clock
  pullback uses that reserve to avoid a right-hand envelope: its normalized
  delay-foot derivatives and complete physical-event border are uniform on
  an explicit continuous-source restriction after the clock direction is
  split from the old weighted phase norm.  A second contraction in that
  clock-aligned norm now produces one literal original-endpoint RFDE segment
  at each fixed parameter pair, with the actual speed/history columns.  Its
  sharp terminal slow jet is independently re-closed by the
  $\mathfrak b$-amplitude flushing ledger, not borrowed from the
  fixed-envelope $\lambda_\delta$ ledger.
  What remains is the action-weighted parameter/gauge family of these
  segments, not the fixed-parameter endpoint segment itself.  The
  relative phase-to-state estimate also
  recovers a uniform old-normalized-state bound and pointwise true action on
  this anchored subspace.  The exact nonlinear formal phase-delay remainder
  and the fixed-reference raw-compatible old-history assembler are now
  closed, including the endpoint/collar second jet and normalized quadratic
  history remainder.  Their exact fixed-section nonlinear graph--action
  residual is also closed, with base size
  $O(r_{\rm out}+S_\delta^{-2})$, exact anchored-Schur linearization, and a
  uniform two-point quadratic remainder.  A uniform contraction now gives
  a unique small canonical zero on each fixed-parameter outer graph slice,
  its first Newton jet, strict speed sign, and an exact finite forward RFDE
  segment.  That zero extends to a nonempty, infinite-dimensional
  raw-compatible gauge-indexed class with uniform slice uniqueness, first
  gauge jet, persistent inverse, and fixed-graph C1/Lipschitz dependence.
  Every retained generated-interior subsegment of every gauge zero whose
  delay collar lies beyond the first maximal delay is an exact
  physical-coordinate tracker and satisfies the quotient and resource-gauge
  Volterra conclusions.  On a common generated buffer, the fixed interior
  sections also have weak-history $C^1$ gauge hit maps with uniformly bounded
  scaled first derivatives and the exact phase quotient.  Their local
  generated neighborhoods are now common time-$C_\delta^3$, gauge-$C^1$
  strong buffers with uniform annular bounds and a fixed-reference trace
  chart.  On those local buffers, the exact quotient now has
  RFDE-specific finite-window flushing, and the complete physical-hit
  histories are first-order raw-gauge equivalent modulo
  $O(\delta^\infty)$ in the normalized event norm.  A separate fixed rough
  chart now supplies the parameter-coherent local hit family and its full
  $\mathcal J_{\rm phys}$ raw-gauge-flat class, with the stated
  $\mathcal K_{\rm phys}$ staircase.  No covariance between different
  fixed-reference charts or common-chart comparison of the full
  gauge-dependent outer domains is asserted.  This does not yet give an
  action-weighted parameter-jet theorem at the original physical endpoints,
  past-complete physical branch endpoints, a
  past-complete history, a cross-branch handoff, or a physical root, and it
  does not prove the global nonautonomous normal bundle.  The generic
  nonselection example is a logical
  counterexample to weak selection criteria, not a model-specific
  impossibility theorem; terminal-to-terminal tracker existence and the
  original-endpoint parameter-jet part of G1 remain open.
- A zero leading covector does not rule out higher-order response.
- The one-delay no-go applies only to the pure-redistribution leading source
  after coincident atoms have been merged.
- No pulse threshold, biological onset, infinite-network limit, moving delay
  support, or closing-gap theorem is claimed.

## Reproduction gate

From this directory, the command below builds both `main.pdf` and
`supplement.pdf`:

```bash
make
```

Before release, record the final commit, PDF hash, page count, clean-log
audit, embedded-font audit, figure-page review, and independent cold reads.
