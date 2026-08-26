# Stage 5D: derivative of the event-aligned physical-pulse history

Status: **directed full-interval first-derivative theorem; not a stable-sheet,
onset, interval-Newton, or routing theorem.**

Let

\[
 J_0=\frac{2409}{8000},\qquad
 h=\frac{3}{40000},\qquad
 \xi=\frac{J-J_0}{h}\in[-1,1].
\]

Stage 5B proves, at every fixed physical time through \(24\sqrt5\),

\[
 z(t,J_0+h\xi)=B(t,\xi)+R(t,\xi),\qquad
 B(t,\xi)=\sum_{k=0}^4b_k(t)\xi^k.
\]

The Stage-5B estimate controls \(R\), not \(\partial_\xi R\). Differentiating
that norm estimate would therefore be invalid. Stage 5D instead encloses the
first variational equation directly.

## 1. The fixed-time first variation

Set

\[
 W=\partial_\xi z=h\partial_Jz,
 \qquad C=\partial_\xi B,
 \qquad E=W-C.
\]

The exact coefficient equations from Stage 5B imply

\[
 \dot E=DF(z)E+\bigl(DF(z)-DF(B)\bigr)C
          +\partial_\xi\operatorname{Tail}_{\ge5}(B).
\]

This identity is the key point: it contains \(R=z-B\), whose size is already
proved, but never differentiates \(R\). Since the vector field is cubic, the
tail is an explicit polynomial of degrees \(5,\ldots,12\). Its derivative is
bounded by outward Bernstein arithmetic on 64 parameter shards. The
linearization difference is written in the correlated forms

\[
 a(B+r)-a(B)
 =-2Br-r^2-3\varepsilon\kappa_3
   \bigl(2(B-1)r+r^2\bigr)
\]

for the current voltage and

\[
 d(B+r)-d(B)
 =\frac{3\varepsilon\kappa_3}{2}
   \bigl(2(B-1)r+r^2\bigr)
\]

for each delayed voltage. Thus the small Stage-5B state remainder is not
decorrelated from the polynomial family before multiplication.

The resulting \(P\)-norm comparison is propagated over the same 1152 exact
time cells used by Stage 5B. Both delays translate cell to cell exactly, and
the pulse release at \(t=1\) is an exact seam. A finite mesh of parameter
values is never used as proof evidence.

## 2. Differentiating the Route-C event

Stage 5C proves one transverse Route-C event \(T(J)\) throughout the full
interval and a positive uniform voltage speed. Differentiating the fixed
section identity gives

\[
 T_\xi(\xi)
 =-\frac{W_v(T(\xi),\xi)}{\dot v(T(\xi),\xi)},
 \qquad T_J=\frac{T_\xi}{h}.
\]

The numerator is evaluated on the entire Stage-5C event-time graph, including
its \(10^{-4}\) remainder. The computation uses 128 parameter Bernstein
shards and every time cell intersected by a shard; it is not an evaluation at
128 sample points.

The resulting full-interval bound has a strict sign:

\[
 336.6243<T_J(J)<456.5741.
\]

Thus increasing the physical pulse amplitude strictly delays this selected
Route-C event throughout the certified interval.

## 3. The complete-history chain rule

For

\[
 K(J)=\left(
   \theta\mapsto v(T(J)+\theta,J),
   w(T(J),J)
 \right)
 \in Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R,
\]

the exact derivative is

\[
 D_JK_v(\theta)
 =\partial_Jv(T(J)+\theta,J)
  +\dot v(T(J)+\theta,J)T_J(J),
\]

with the analogous formula for the current recovery coordinate. Stage 5D
encloses both summands continuously over the full history window. In
particular, the translation term is not dropped. Because the section voltage
is independent of \(J\),

\[
 D_JK_v(0)=0
\]

exactly.

The current recovery derivative also has a strict full-interval sign:

\[
 -17.3507<D_JK_w(J)<-10.1427.
\]

Hence event alignment does not erase all monotonicity: the selected event is
later and its current recovery coordinate is lower when the pulse amplitude is
increased. This is a property of the event family, not yet a sign for the
stable coordinate.

## 4. What the Stage-4D action does and does not give

The fixed center Route-C functional of Stage 4D is an atom-plus-density
measure. Its current-voltage atom vanishes on \(D_JK\) because the section
coordinate above is exactly zero. Hence

\[
 |f_{\rm raw}(D_JK)|
 \le \|\rho_v\|_{\rm TV}\|D_JK_v\|_\infty
     +|a_w|\,|D_JK_w|.
\]

Dividing by the proved lower bound for \(|f_{\rm raw}(q)|\) gives a rigorous
modulus bound for the normalized fixed functional. Stage 4D records directed
moduli and total variation, but not one oriented signed enclosure of every
atom and density coefficient for this pulse-family action. Therefore Stage
5D does **not** prove the sign of \(f(D_JK)\) or exclude zero. That missing
oriented action, together with a quantitative stable graph, is still required
for a stable-gap slope and interval Newton.

The result file records all numerical radii and intervals. Generate or audit
it with

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 \
      experiments/leaky_pulse_event_aligned_derivative_stage5d.py

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 \
      experiments/leaky_pulse_event_aligned_derivative_stage5d.py --check

The stable gap, its endpoint signs and derivative, an interval-Newton image,
\(J_c\), biological onset, two-sided routing, and capture all remain explicitly
null or false.
