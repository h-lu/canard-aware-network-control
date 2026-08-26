# Stage 4K v2: cone-compatible enlarged stable-graph design diagnostic

Status: **DIAGNOSTIC — conditional exact arithmetic, not a stable-graph
certificate.**

Stage 4K asks one narrow design question. If the Stage-4A heuristic Hessian
blocks were eventually replaced by directed uniform bounds of comparable
size, if a signed continuous-history calculation proved the hypothetical
stable-power pair, and if a return tube of the stated size were validated,
would the exact Stage-4 Lyapunov--Perron majorant permit a stable radius near
\(9.9\times10^{-3}\)? The exact arithmetic answers yes. None of those
antecedents has been proved here.

The executable source is
[leaky_inner_stable_graph_enlargement_stage4k.py](../src/canard_control/leaky_inner_stable_graph_enlargement_stage4k.py),
the generator is
[leaky_inner_stable_graph_enlargement_stage4k.py](../experiments/leaky_inner_stable_graph_enlargement_stage4k.py),
and the source-bound result is
[leaky_inner_stable_graph_enlargement_stage4k.json](../experiments/results/leaky_inner_stable_graph_enlargement_stage4k.json).

## 1. Proposed anisotropic design

The registered design is

\[
 r=0.0094,\qquad R_s=0.0099,\qquad
 \widehat R_u=0.00005,\qquad \beta=0.9999.
\]

Here (widehat R_u) denotes the proposed unit-(Y) unstable coordinate for
the fixed splitting

\[
 \widehat q=\frac{q}{\lVert q\rVert_Y},\qquad
 \widehat f=\lVert q\rVert_Y f,\qquad
 P_s=I-\widehat q\widehat f.
\]

The internal graph box has split-radius sum \(0.00995\). Stage 4K inserts
that same value as a *hypothetical* return-ball radius solely so that the
existing exact evaluator can test its containment formula. It does not
validate a nonlinear return tube, an event window, or exclusion of earlier
section hits.

Stage 4A normalized its finite-section right vector in nodal
(ell^\infty). Its block row is therefore only a heuristic proxy for this
future continuous-history unit-(Y) coordinate. Stage 4K does not validate
that normalization transfer or the later conversion to a physical Grushin
pair. In particular, (widehat R_u) is not the ambient unstable coordinate
of a pulse endpoint.

This v2 choice retires the earlier \(r=0.0090, R_s=0.0095\) design. It is
motivated by the anticipated Stage-5G-b two-endpoint cone number

\[
 0.0093802671 < r=0.0094,
 \qquad r-0.0093802671=0.0000197329.
\]

That number is an **unbound design expectation** here. Stage 4K neither
loads nor byte-binds a Stage-5G-b result, does not prove that the cone bound
is directed, and does not prove containment of the full pulse interval.
Those flags and every corresponding strict ingress remain false or null.

## 2. Six heuristic blocks

The source-bound Stage-4A refinement envelope is

\[
\begin{array}{lll}
 \widehat C_s^{ss}=0.02246866950,&
 \widehat C_s^{su}=0.08876413561,&
 \widehat C_s^{uu}=7.946815637,\\
 \widehat C_u^{ss}=0.2969314837,&
 \widehat C_u^{su}=0.2830961263,&
 \widehat C_u^{uu}=26.19689184.
\end{array}
\]

These are the maximum of the last two finite meshes plus twice the
last-mesh change and (10^{-15}). That construction is not an interval
discretization error. None of the six numbers is a directed uniform bound
on (D^2P).

Stage 4K scales all six entries simultaneously by (1), (3/2), and (2).
It does not mix individually favorable block caps from different rows.

## 3. Exact majorant arithmetic

For each scaled row, Stage 4K calls the existing
`evaluate_matrix_lyapunov_perron_majorant`. Decimal strings enter as exact
fractions; the evaluator uses rational arithmetic and an integer-square-root
upper bound for the Perron root. Thus the following are exact directed
statements about the displayed *hypothetical numeric budgets*, not about the
RFDE return map.

| simultaneous factor | Perron upper | stable self-map slack | unstable self-map slack |
|---:|---:|---:|---:|
| \(1\) | \(<0.063\) | \(>2.62\times10^{-4}\) | \(>3.20\times10^{-5}\) |
| \(1.5\) | \(<0.095\) | \(>1.44\times10^{-4}\) | \(>2.30\times10^{-5}\) |
| \(2\) | \(<0.126\) | \(>2.61\times10^{-5}\) | \(>1.40\times10^{-5}\) |

The factor-two row also gives, at diagnostic level,

\[
 \lVert h\rVert_Y<3.6\times10^{-5},\qquad
 \lVert Dh\rVert<8.1\times10^{-3}.
\]

The raw Stage-4 evaluator names its conjunction of contraction, self-map,
and numeric box containment `graph_certificate_closes`. In Stage 4K that raw
field is true for all three rows, but it means only that the algebra closes
for a complete numeric budget. Stage 4K separately and forcibly records
`strict_graph_certificate_closes=false`, equivalently

\[
 \texttt{strict\_graph\_certificate\_closes=false}.
\]

## 4. Isolated preferred sensitivity B

The three main rows above are fallback design A: they retain the hypothetical
registered rate \(\rho_s=0.995024916874\ldots\). They do not depend on a
future Stage-4L terminal-row result.

Stage 4K also records one strictly separate sensitivity design B. **If** a
future source-bound Stage-4L certificate proves
\(\rho_{\rm term}\le0.1\) with \(K_s=1\), consider

\[
 r=0.0094,\qquad R_s=0.0097,\qquad
 \widehat R_u=0.00025,qquad R_s+\widehat R_u=0.00995.
\]

For the simultaneous factor-two heuristic blocks, exact-rational arithmetic
then gives

\[
 \rho(M)<0.024589,\quad
 s_s>0.0002966204,\quad s_u>0.0002122224,
\]

and

\[
 \widehat H_{\rm graph}<0.000037773,qquad
 \lVert D\widehat\psi\rVert<0.007376.
\]

Exact probes close at common multiplier \(13.2353\) and fail at
\(13.2354\); the diagnostic ceiling estimate is \(13.23539\). The limiting
gate is the unstable self-map, driven by the \(C_u\) block family, not the
stable row.

There is also a purely conditional coordinate conversion. If the future
graph exists in the same \((\widehat q,\widehat f)\) normalization and an
independently bound Stage-4E adapter gives
\(\alpha=\lVert q\rVert_Y\ge0.0775543158981\), then the *majorant graph
height*, not the box radius \(\widehat R_u\), gives

\[
 |\psi|\le
 \frac{0.000037772893584439}{0.0775543158981}
 <0.0004871<0.001.
\]

The sharper-looking bound \(<0.000487\) does not follow from the displayed
rounded ingress: the quotient is approximately \(0.00048705083\). Neither
Stage 4L, the Stage-4E lower bound, nor the Stage-5G-a target is parent-bound
by Stage 4K. Thus this conversion proves neither a graph nor either endpoint
stable-gap sign.

## 5. What remains null

The strict proof ingress keeps null:

- all six directed uniform projected Hessian blocks;
- a directed stable-power rate and constant, including the main hypothetical
  values \(\rho_s=0.995024916874\ldots\) and \(K_s=1\);
- a validated Stage-5G-b full-pulse stable-coordinate upper bound;
- a validated return-map split ball and returned-history tube.

It keeps false the first-positive-return/no-earlier-hit gate and containment
of the full pulse stable-coordinate interval in \(r=0.0094\). Consequently,
the exact arithmetic proves no stable graph, no selected pulse intersection,
no separator crossing, and no physical onset.

## 6. Directed upgrade target

The factor-two row supplies proof-design caps, not theorem inputs:

\[
\begin{array}{lll}
 C_s^{ss}\le0.04493733901,&
 C_s^{su}\le0.1775282712,&
 C_s^{uu}\le15.89363127,\\
 C_u^{ss}\le0.5938629674,&
 C_u^{su}\le0.5661922527,&
 C_u^{uu}\le52.39378368.
\end{array}
\]

The priority block for the enlarged design is (C_s^{ss}), followed by
(C_u^{ss}). A future directed evaluator must use the fixed splitting,
propagate complete histories and physical event-time variations over the
whole anisotropic box, form the stable deflation and unstable scalar action
before taking norms, and evaluate all six blocks jointly.

Separately, a signed continuous-history row must prove (K_s=1); a
nonlinear flow calculation must validate the moving and terminal return
tubes and exclude earlier hits; and a parameter-sharded pulse calculation
must prove that the full stable-coordinate interval lies inside the seed
radius. Only after those independent antecedents are supplied can the raw
matrix closure participate in a stable-graph theorem.

## 7. Reproducibility boundary

The result binds the Stage-4 and Stage-4A parent bytes, this source, the
generator, and this note. Its artifact has a canonical JSON digest. The
generator builds the artifact, validates it against a fresh replay, writes
an fsynced temporary file, atomically replaces the destination, and fsyncs
the containing directory. These release mechanics protect the diagnostic
record; they do not promote its mathematical status.
