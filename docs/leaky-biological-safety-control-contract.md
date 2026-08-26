# Biological frequency--amplitude--safety control contract

Status: **the block-triangular inverse, threshold-adapted product theorem,
fixed-box radius formula, pulse-containment test, and network safety-erosion
formula are proved.  The outer frequency--amplitude parent and the
fixed-common-time wide pulse parent are validated.  The source-bound Stage-5C
parent additionally validates the exact Route-C section enclosure, a unique
transverse event in one declared bracket throughout the wide pulse interval,
a fourth-order event-time graph remainder, and a continuous common-event
complete-history tube.  These event facts do not validate the stable-sheet
signs, interval-Newton onset, physical threshold, two-sided routing/capture,
numerical three-output biological radius, or asynchronous biological safety
radius.**

The source is
[leaky_biological_safety_control_contract.py](../src/canard_control/leaky_biological_safety_control_contract.py),
the generator is
[leaky_biological_safety_control_contract.py](../experiments/leaky_biological_safety_control_contract.py),
the result is
[leaky_biological_safety_control_contract.json](../experiments/results/leaky_biological_safety_control_contract.json),
and the hostile tests are
[test_leaky_biological_safety_control_contract.py](../tests/test_leaky_biological_safety_control_contract.py).
The newly imported event facts are bound simultaneously to the Stage-5C
[result](../experiments/results/leaky_pulse_route_c_event_stage5c.json) SHA-256
and its canonical certificate SHA-256; neither identifier may float with the
workspace.

## 1. Exact intrinsic control chart

Let

\[
 P(\xi)=(F(\xi),A(\xi)),\qquad
 S(\xi,J)=J-J_c(\xi),\qquad
 {\cal Q}(\xi,J)=(P(\xi),S(\xi,J)).
\]

Here \(J_c\) must be the unique event-aligned stable-sheet threshold with
two-sided biological routing.  A detector preset or operational reset is not
substituted for it.

With \(B=D_\xi P\) and \(c=D_\xi J_c\),

\[
 D{\cal Q}=
 \begin{pmatrix}B&0\\-c^T&1\end{pmatrix},\qquad
 (D{\cal Q})^{-1}=
 \begin{pmatrix}B^{-1}&0\\c^TB^{-1}&1\end{pmatrix}.
\]

Thus

\[
 \det D{\cal Q}=\det B.
\]

The outer periodic parent proves

\[
 \|B^{-1}\|_2\le
 22.0443366996474009863289788361024421012357819109700835
\]

and a branch-centered frequency--amplitude target radius of at least

\[
 4.5363124943378087357560203269152544299222454294595117
 \times10^{-12}.
\]

These facts prove the two-output block.  They do not define \(J_c\).

## 2. Threshold-adapted product theorem

Suppose \(P:U\to V\) is bijective.  For any safety center \(S_0\) and
\(\sigma>0\), define

\[
 {\cal U}_{S_0,\sigma}
 =
 \{(\xi,J):\xi\in U,\ |J-J_c(\xi)-S_0|<\sigma\}.
\]

Then

\[
 {\cal Q}:{\cal U}_{S_0,\sigma}
 \longrightarrow V\times(S_0-\sigma,S_0+\sigma)
\]

is bijective.  Indeed, invert \(P\) first and then set
\(J=J_c(\xi)+S\).  This intrinsic product theorem does not require a bound
on \(D_\xi J_c\), because the input domain is already aligned with the
threshold graph.

## 3. A fixed actuator box

For a laboratory product box

\[
 \|\xi-\xi_0\|\le R_\xi,\qquad |J-J_0|\le R_J,
\]

assume

\[
 \|P^{-1}(y)-\xi_0\|\le K\|y-P(\xi_0)\|,
 \qquad \|D_\xi J_c\|\le L_c.
\]

Every output ball of radius \(\rho\) is contained when

\[
 \boxed{
 \rho\le
 \min\left\{
 \rho_{FA},\frac{R_\xi}{K},\frac{R_J}{L_cK+1}
 \right\}.}
\]

For a Euclidean input ball, the exact two-by-two shear majorant is

\[
 H=
 \begin{pmatrix}
 K^2(1+L_c^2)&L_cK\\
 L_cK&1
 \end{pmatrix}.
\]

Hence

\[
 \|(D{\cal Q})^{-1}\|_2^2\le\lambda_{\max}(H)
 \le K^2(1+L_c^2)+1.
\]

The executable exact-rational test uses the last inequality.  Pulse
containment additionally requires

\[
 J_0\pm(L_cK+1)\rho\in[J_-,J_+].
\]

The fixed-time pulse parent validates

\[
 [J_-,J_+]=[0.30105,0.30120]
\]

and a full-width fifth-order remainder \(P\)-radius below
\(1.721\times10^{-8}\).  It supplies no \(J_c\) or \(L_c\), so the
model-specific three-output radius remains null.

## 4. Exactly what Stage-5C adds

The biological contract imports exactly six event-side outputs from the
frozen Stage-5C parent.

1. The exact phase-zero Route-C section is
   \(h_C(\phi)=\phi_v(0)-V_{\rm true}(0)\), with the validated exact-orbit
   voltage enclosure
   \[
   V_{\rm true}(0)\in
   [0.905383843282120025506287674943450838327407828420353068999752401,
   0.905403843282120025506287674943450838327407845269557922000191891].
   \]
   The older narrow Fourier-candidate interval is not substituted for this
   exact-orbit enclosure.
2. The event proof covers exactly
   \(J\in[6021/20000,753/2500]\).
3. For each such \(J\), there is one and only one positive Route-C crossing
   in
   \[
   [555\sqrt5/24,\ 1+546\sqrt5/24].
   \]
   No count of earlier crossings is proved, so this is not certified as the
   third post-release crossing.
4. The voltage speed throughout that bracket is positive and lies in
   \[
   [0.213351901873463286891339163985473697827026675282880628193321097,
   0.279199972359585210755085983706906600304258513452988752328974292].
   \]
5. The fourth-order event-time graph has uniform time remainder at most
   \(1/10000\).
6. In \(Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R\), the continuous
   common-event complete-history tube has radius at most
   \[
   0.00819993124842261744392761744249492657918561955934732431617329805.
   \]

These six outputs stop on the event side of the stable sheet.  They do not
define \(J_c\), stable-coordinate endpoint signs, an interval-Newton image,
a physical onset, either routed basin side, or capture.  In particular, no
biological threshold is inferred from event existence alone.

## 5. Network safety erosion

If an asynchronous network gap differs from the scalar gap by at most
\(\epsilon_H\) and the scalar gap slope is at least \(m_J>0\), then

\[
 |J_{c,N}-J_c|\le\Delta_J=\frac{\epsilon_H}{m_J}.
\]

If pulse-amplitude error is at most \(e_J\), every target in a safety
interval centered at \(S_0\) with radius \(\rho_S\) retains one routed sign
provided

\[
 \boxed{|S_0|-\rho_S>\Delta_J+e_J.}
\]

This is a strict erosion rule.  Equality does not preserve a sign.  The
general Dobrushin parent proves the conditional formula, but its scalar gap,
route, product-lift and response constants are still null.

## 6. Claim ledger

| Claim | Status |
|---|---|
| Outer \((F,A)\) inverse and target ball | **Proved by parent** |
| Fixed-time wide pulse Taylor model and fifth-order remainder | **Proved by parent** |
| Exact Route-C section level and wide \(J\)-interval | **Proved by Stage-5C parent** |
| Unique event in the declared bracket and positive event speed | **Proved by Stage-5C parent** |
| Fourth-order event-time graph remainder | **Proved by Stage-5C parent** |
| Continuous common-event complete-history \(Y\)-tube | **Proved by Stage-5C parent** |
| Exact determinant and inverse factorization | **Proved** |
| Threshold-adapted product bijection | **Proved** |
| Rectangular and Euclidean target-radius formulas | **Proved** |
| Pulse-interval containment formula | **Proved** |
| Network threshold shift and safety erosion formulas | **Proved conditionally** |
| Event-aligned biological \(J_c\) | **Open** |
| Bound on \(D_\xi J_c\) | **Open** |
| Stable-coordinate endpoint signs and interval Newton | **Open and null** |
| Unique physical pulse onset | **Open and null** |
| Two-sided quiet/outer biological routing | **Open** |
| Two-sided quiet/outer capture | **Open and null** |
| Numerical three-output biological target radius | **Open and null** |
| Concrete asynchronous biological safety radius | **Open and null** |

The result is an executable completion interface.  It prevents a nonzero
two-output determinant, a fixed-time pulse tube, or an operational detector
coordinate from being promoted to biological safety controllability.
