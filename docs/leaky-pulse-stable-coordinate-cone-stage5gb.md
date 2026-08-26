# Stage 5G-b: full-interval stable-coordinate cone

Status: **PROVED stable-coordinate ball / no stable graph or crossing theorem.**

Stage 5G-b works on the single continuously differentiable selected Route-C
event branch and in the same complete-history space, section, physical
Grushin normalization, and projection used by Stages 5D, 5E, 5F, and 5G-a.
It proves

\[
 P_s\kappa(I_J)\subset
 \overline B_Y\!\left(0,\frac{47}{5000}\right)\cap\ker f_{\rm phys}.
\]

This is a stable-coordinate ball inclusion.  It does not construct a stable
graph or prove that a future graph domain contains the ball.

## 1. Sharpened derivative bound

The reference history \(X_*\) and the physical pair \((q,f)\) are fixed while
\(J\) varies.  With

\[
 z(J)=P_s(K(J)-X_*),\qquad P_s=I-qf,
\]

Stage 5D gives \(z'(J)=P_sD_JK(J)\) as a continuous \(Y\)-valued derivative,
including the event-translation term.  Stage 5E forms the correlated residual

\[
 Y_*(J)=D_JK(J)-c_*q,\qquad c_*=-252,
\]

before taking its complete-history norm.  The exact identity

\[
 P_sD_JK=Y_*+q\bigl(c_*-f(D_JK)\bigr)
\]

therefore gives

\[
 \|P_sD_JK\|_Y\le
 L_s:=R_*+Q_*\delta_f.
\]

Here \(R_*\) and \(\delta_f\) are imported from their Stage-5E proof fields,
while \(Q_*\) is the direct Stage-5G-a norm of the same \(q_{\rm phys}\) on
all 512 continuous history cells and the current recovery coordinate.  The
older Stage-5F Wiener norm is retained only as a comparison and is not used
in \(L_s\).

## 2. Two-ended Banach-space cone

Let \(I_J=[J_-,J_+]\) and \(W=J_+-J_-=3/20000\).  Stage 5G-a supplies both
endpoint bounds \(\|z(J_-)\|_Y\le E_-\) and
\(\|z(J_+)\|_Y\le E_+\).  The Banach-space fundamental theorem of calculus
gives, for \(x=J-J_-\),

\[
 \|z(J)\|_Y\le
 \min\{E_-+L_sx,\ E_++L_s(W-x)\}.
\]

The certificate interprets every serialized outward decimal as an exact
rational bound and recomputes

\[
 x_* = \frac{E_+-E_-+L_sW}{2L_s},\qquad
 E_{\rm cone}=\frac{E_-+E_++L_sW}{2}.
\]

Exact rational comparisons and an independent 192-bit directed serialization
both prove \(0<x_*<W\) and \(E_{\rm cone}<47/5000\).  No finite parameter
sample or endpoint interpolation is used.

## 3. Sharper conditional stable-gap slope

Stage 5E also supplies the real interval
\(f(D_JK)\in[A_-,A_+]\).  For a future graph in the identical coordinates,

\[
 H'=f(D_JK)-D\psi(z)[P_sD_JK].
\]

Consequently Stage 5G-b proves the exact arithmetic implication

\[
 \sup\|D\psi\|\le16
 \quad\Longrightarrow\quad
 H'(I_J)\subset[A_--16L_s,A_++16L_s]\subset(-\infty,0).
\]

The JSON also records the strictly larger threshold
\(-A_+/L_s\) at which this upper estimate could reach zero.  These are only
conditional implications: this stage supplies neither \(\psi\) nor the bound
\(\sup\|D\psi\|\le16\), so it does not claim an unconditional stable-gap
derivative.

## 4. Exact claim boundary

Stage 5G-b proves:

- the sharper complete-history bound on \(\|P_sD_JK\|_Y\);
- strict interior intersection of the two endpoint cones;
- the full-interval radius-\(47/5000\) stable-coordinate ball inclusion;
- the displayed conditional stable-gap derivative arithmetic.

The following remain **OPEN**:

- a quantitative stable graph in this registered chart;
- proof that a future graph domain contains the radius-\(47/5000\) ball;
- the graph derivative and endpoint graph-height hypotheses themselves;
- actual stable-gap endpoint signs and a selected-event stable-sheet crossing;
- identification with an ordinal crossing, biological onset, two-sided basin
  routing, capture, or any safety radius.

If a future graph parent proves domain containment on this same ball, the
present theorem discharges only the stable-coordinate domain premise of the
selected-crossing proposition.  Interval Newton is neither used nor claimed.
