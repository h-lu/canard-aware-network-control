# Stage 5G-b contract: sharp stable-coordinate cone on the full pulse interval

Status: **THEOREM DESIGN / pending Stage-5G-a parent freeze.**  This stage
uses the direct complete-history norm of the fixed physical unstable column
from Stage 5G-a to sharpen the Stage-5F stable derivative bound.  It then
combines that derivative bound with both endpoint stable-coordinate boxes.
The intended conclusion is a source-bound enclosure of the entire pulse
curve in a stable-coordinate ball of radius \(0.0094\).  It supplies no
stable graph by itself.

## 1. Fixed coordinates and the sharper derivative identity

All quantities remain in

\[
 Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R,
 \qquad \Sigma=\{y\in Y:y_v(0)=0\},
\]

with the Stage-5E physical Grushin normalization

\[
 f(q)=1,\qquad P_s=I-qf.
\]

The inner reference history \(X_*\) is fixed while \(J\) varies, hence

\[
 \frac{d}{dJ}P_s(K(J)-X_*)=P_sD_JK(J).              \tag{1.1}
\]

Stage 5E uses the exact center \(c_*=-252\) and forms the correlated
complete-history residual

\[
 Y_*(J)=D_JK(J)-c_*q                              \tag{1.2}
\]

before taking a norm.  The exact projection identity is

\[
 P_sD_JK
   =Y_*+q\bigl(c_*-f(D_JK)\bigr).                    \tag{1.3}
\]

Therefore the same-coordinate directed inputs

\[
 \|Y_*\|_Y\le R_*,\qquad
 |c_*-f(D_JK)|\le\delta_f,\qquad
 \|q\|_Y\le Q_*                                    \tag{1.4}
\]

give

\[
 \|P_sD_JK\|_Y\le L_s:=R_*+Q_*\delta_f.             \tag{1.5}
\]

Stage 5F used the valid but coarse Wiener value
\(Q_*<1.382981\), producing \(L_s<14.727579\).  Stage 5G-a instead
encloses the same fixed physical \(q\) directly on all 512 continuous
history segments and the recovery coordinate.  Its diagnostic value is

\[
 Q_*\lesssim0.086274581.                             \tag{1.6}
\]

Together with the released Stage-5E values

\[
 R_*\le5.397270394399,\qquad
 \delta_f\le6.746521015805,                          \tag{1.7}
\]

this predicts

\[
 L_s\le5.979324.                                     \tag{1.8}
\]

The numbers in (1.6)--(1.8) become theorem data only after Stage 5G-a is
frozen and this stage binds and revalidates that parent.  The improvement
does not alter \(q,f,P_s\); it replaces only a coarse norm enclosure of the
same \(q\).

## 2. Two-ended cone lemma

Let

\[
 z(J)=P_s(K(J)-X_*),\qquad
 I_J=[J_-,J_+],\qquad W=J_+-J_-=\frac3{20000}.
\]

Suppose

\[
 \|z(J_-)\|_Y\le E_-,\qquad
 \|z(J_+)\|_Y\le E_+,
 \qquad \sup_{I_J}\|z'(J)\|_Y\le L_s.              \tag{2.1}
\]

For \(x=J-J_-\in[0,W]\), the fundamental theorem of calculus gives both

\[
 \|z(J)\|_Y\le E_-+L_sx,
 \qquad
 \|z(J)\|_Y\le E_++L_s(W-x).                        \tag{2.2}
\]

Thus

\[
 \|z(J)\|_Y
 \le\min\{E_-+L_sx,E_++L_s(W-x)\}.                 \tag{2.3}
\]

If

\[
 x_*:=\frac{E_+-E_-+L_sW}{2L_s}\in[0,W],            \tag{2.4}
\]

the increasing and decreasing affine bounds meet inside the interval, and

\[
 \sup_{J\in I_J}\|z(J)\|_Y
 \le E_{\rm cone}:=\frac{E_-+E_++L_sW}{2}.           \tag{2.5}
\]

This argument uses the complete-history Banach norm and the whole-interval
derivative bound.  It is not a sampled interpolation and needs no
parameter-sharded state recomputation.

## 3. Target arithmetic

The Stage-5G-a diagnostic endpoint values are

\[
 E_-\lesssim0.008935972,\qquad
 E_+\lesssim0.008927665.                             \tag{3.1}
\]

With (1.8), the meeting point in (2.4) lies strictly inside \(I_J\), near
the center, and directed arithmetic is expected to give

\[
 E_{\rm cone}<0.009381<0.0094=\frac{47}{5000}.       \tag{3.2}
\]

The released Stage-5F coarse \(q\)-norm would instead give about
\(0.0100364\), so the direct Stage-5G-a \(q\)-norm is essential to (3.2).
No endpoint lower bound is inferred from an upper enclosure; only the upper
ball inclusion is used.

Once source-bound, (3.2) proves

\[
 P_s\kappa(I_J)\subset
 \overline B_Y(0,0.0094)\cap\ker f.                 \tag{3.3}
\]

It does **not** prove that a stable graph exists on this ball.  If a future
quantitative graph parent independently proves that its stable domain
contains the closed radius-\(0.0094\) ball in the identical \(P_s,Y\)
coordinates, then (3.3) discharges the full-interval graph-domain premise
of the selected-crossing proposition.

## 4. Sharper conditional stable-gap slope

For a future graph in the identical coordinates,

\[
 H'(J)=f(D_JK(J))
       -D\psi(z(J))[P_sD_JK(J)].                    \tag{4.1}
\]

If Stage 5E supplies
\(f(D_JK)\in[A_-,A_+]\), then (1.5) gives the exact implication

\[
 \sup\|D\psi\|\le L_\psi
 \quad\Longrightarrow\quad
 H'(I_J)\subset
 [A_--L_\psi L_s,\ A_++L_\psi L_s].                \tag{4.2}
\]

For \(L_\psi=16\), the sharper direct-\(q\) calculation is expected to give

\[
 H'(I_J)\subset[-354.416,-149.584]\subset(-\infty,0), \tag{4.3}
\]

and the maximum admissible graph derivative before the upper endpoint can
reach zero is expected to exceed \(41.01\).  These are **CONDITIONAL**
graph implications: Stage 5G-b may prove their arithmetic, but it supplies
no \(\psi\) and therefore no unconditional stable-gap derivative.  They
strictly strengthen the Stage-5F interval
\([-494.388,-9.612]\) without changing its coordinates or proof mechanism.

## 5. Compatible enlarged graph design

The Stage-4K \(r=0.0090\) diagnostic design is too small for (3.2).  The
same exact two-by-two evaluator remains favorable for the cone-compatible
hypothetical design

\[
 r=0.0094,\qquad R_s=0.0099,\qquad
 \widehat R_u=0.00005,\qquad R_s+\widehat R_u=0.00995.
\]

With all six Stage-4A heuristic blocks multiplied simultaneously by two,
the diagnostic exact arithmetic gives approximately

\[
 \rho(M)<0.126,\qquad
 \text{self-map slacks}>2.61\times10^{-5},
                         1.40\times10^{-5},          \tag{5.1}
\]

and unit-coordinate graph height below \(3.60\times10^{-5}\).  These values
are **DIAGNOSTIC**: \(K_s=1\), the return tube, the continuous-\(Y\)
normalization transfer and all six uniform Hessian blocks remain open.
They show only that replacing \(r=0.0090\) by the rigorously useful
\(r=0.0094\) does not destroy the matrix design.

## 6. Release fields and hostile tests

A Stage-5G-b result may set the full-interval stable-coordinate radius flag
to true only if it:

- binds and normally validates Stages 5D, 5E, 5F and 5G-a;
- checks the identical \(Y,\Sigma,q,f,P_s,K,X_*\) registration in every
  parent;
- imports \(R_*,\delta_f,Q_*,E_-,E_+\) from their proof-bearing fields;
- recomputes (1.5), (2.4), (2.5) and the conditional interval (4.2) with
  exact rationals and directed
  serialization;
- proves \(0<x_*<W\) and \(E_{\rm cone}<47/5000\) strictly;
- records exact schemas, parent/source hashes, a canonical digest, current
  runtime equality, validate-before-write atomic generation and a fresh
  independent replay.

Hostile tests must refresh the outer digest and still reject: the old coarse
\(q\)-norm relabelled as the direct norm; a different \(q/f\) normalization;
an endpoint norm from only one side; a missing derivative translation term;
using \(J\)-half-width in place of the full width \(W\); omitting the
inside-intersection test; replacing the Banach-space fundamental theorem of
calculus by sampled interpolation; or promoting (3.3) to a graph,
stable-sheet crossing, onset, routing or safety theorem.

The exact claim boundary after release is:

- **PROVED:** the selected center pulse curve's stable coordinate lies in
  the closed \(Y\)-ball of radius \(0.0094\) on all of \(I_J\);
- **CONDITIONAL:** this supplies graph-domain containment if a future graph
  is validated on that same ball;
- **OPEN:** the graph, graph-height-adjusted endpoint signs, selected
  crossing, biological onset, routing, capture and network safety.
