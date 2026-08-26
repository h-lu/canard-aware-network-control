# Stage 5C: the physical pulse reaches the exact Route-C section

Status: **directed event-side theorem.**  This artifact proves a unique
positive Route-C crossing in one declared late time bracket for every

\[
 J\in[6021/20000,753/2500].
\]

It also encloses the four centre-parameter implicit event-time derivatives,
validates a fourth-order event-time polynomial with a uniform remainder, and
pulls the full voltage history and current recovery to the common event graph
inside a continuous \(Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R\) tube.
It does **not** prove that this is the third post-release crossing, construct
the quantitative inner stable graph, validate stable-coordinate endpoint
signs, run interval Newton on the stable gap, or prove onset or either basin
capture.

## 1. A uniform transverse event

The section is the exact phase-zero section of the validated inner orbit,

\[
 h_C(\phi)=\phi_v(0)-V_{\rm true}(0).
\]

The validated orbit-ball interval for \(V_{\rm true}(0)\), rather than the
much narrower Fourier-candidate value, is imported byte-for-byte from the
Route-C stable-manifold contract.  The fixed-time flow family is imported
byte-for-byte from Stage 5B; its correlated polynomial in
\(\xi=(J-J_0)/h\) is never replaced by independent state shards.

On the exact three-cell bracket

\[
 I_C=\left[\frac{555\sqrt5}{24},
             1+\frac{546\sqrt5}{24}\right],
\]

directed Bernstein evaluation proves a strict negative section gap at the
left endpoint, a strict positive gap at the right endpoint, and a positive
lower bound for the exact voltage field throughout all of \(I_C\) and the
entire pulse interval.  Hence every pulse history has one and only one
positive Route-C crossing in \(I_C\).  This is a local event count.  No claim
about the number of crossings before \(I_C\) is inferred from it.

## 2. Implicit event-time jet

At \(J_0=2409/8000\), the centre crossing is first enclosed inside the final
cell of \(I_C\).  On that event bracket, the Stage-5B coefficient tubes are
recursively differentiated through the RFDE.  Delayed mixed derivatives are
taken from the exactly translated source cells, so no numerical interpolation
across a delay seam enters the calculation.

Write

\[
 T(\xi)=T_0+a_1\xi+a_2\xi^2+a_3\xi^3+a_4\xi^4+R_T(\xi).
\]

For each order \(m\), factorial series composition of
\(g(t,\xi)=v(t,J_0+h\xi)-V_{\rm true}(0)\) produces the single linear term
\(g_ta_m\).  All other order-\(m\) terms are enclosed first, after which

\[
 a_m=-\frac{[\xi^m]\,g(T_0+\sum_{j<m}a_j\xi^j,\xi)}{g_t}.
\]

The physical derivatives are

\[
 \tau_m=\partial_J^mT(J_0)=\frac{m!}{h^m}a_m.
\]

The exact intervals are stored in the JSON artifact rather than rounded in
this note.

## 3. A full-width event graph, not only formal coefficients

Midpoints of the four proved coefficient intervals define
\(\widehat T_4(\xi)\).  Candidate times cross internal Stage-5B cell seams as
\(\xi\) varies, so the proof adaptively bisects the parameter interval and
uses every intersected time guide.  At a seam, both adjacent validated guides
are retained.  The proof accepts a shard only when directed evaluation gives

\[
 g(\widehat T_4(\xi)-10^{-4},\xi)<0,
 \qquad
 g(\widehat T_4(\xi)+10^{-4},\xi)>0.
\]

Together with the uniform positive speed, this proves

\[
 |T(\xi)-\widehat T_4(\xi)|\le10^{-4}
 \quad(-1\le\xi\le1).
\]

Thus the displayed coefficients are not merely a formal jet: their degree
four polynomial has a validated full-parameter event-time remainder.

## 4. Pullback of the complete history

Let the exact coefficient solutions from Stage 5B define the continuous
fixed-centre family

\[
 B_c(\xi)=\left(
  \theta\mapsto\sum_{k=0}^4b_{k,v}(T_0+\theta)\xi^k,
  \sum_{k=0}^4b_{k,w}(T_0)\xi^k
 \right).
\]

The event-aligned history is

\[
 \mathcal Y(\xi)=\left(
  \theta\mapsto v(T(\xi)+\theta,J_0+h\xi),
  w(T(\xi),J_0+h\xi)
 \right).
\]

Cellwise vector-field bounds on the whole swept history window give

\[
 \|\mathcal Y(\xi)-B_c(\xi)\|_Y
 \le \max\{F_vd_T+E_{5,v},F_wd_T+E_{5,w}\}.
\]

All constants and the resulting radius are directed and stored in the
artifact.  This proves a continuous full-history tube, not merely a terminal
point enclosure.

The Stage-5B state remainder does not by itself bound its \(J\)-derivative,
and the history window contains propagated smoothness fronts that must be
treated cellwise before claiming a fourth-order \(Y\)-valued jet.  Therefore
the uniform event-history derivative tube is still open.  The centre
event-time derivatives above are unaffected because the centre event and its
recursively used delayed points lie strictly inside their smooth cells.

## 5. Exact stopping point

Stage 4D supplies a continuous Route-C adjoint measure, but not the physical-
time correlated \(Y_{qq}\) action or a quantitative stable graph.  Applying
the adjoint alone would replace a nonlinear stable sheet by its tangent
hyperplane.  Accordingly, endpoint stable-gap signs, a derivative interval,
an interval-Newton image, a unique physical onset, two-sided routing, and
capture all remain explicitly false.

Generate the artifact with

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 \
  experiments/leaky_pulse_route_c_event_stage5c.py
```

`--check` audits the registered source and parent hashes without replay;
`--check --recompute` independently repeats the Stage-5B and Stage-5C
directed calculations.
