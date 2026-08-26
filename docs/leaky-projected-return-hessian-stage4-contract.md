# Stage 4: direct projected return-Hessian contract

## Outcome

Stage 3 proves, in the declared reduced-history sup norm, that
\(\lVert P_s\rVert\geq 2\). Consequently the old scalar Lyapunov--Perron
row with \(C_N=10\) cannot close. That conclusion is deliberately narrower
than an impossibility theorem for the norm: no validated upper bound for the
actual Poincare return Hessian is yet available.

This Stage-4 artifact replaces that scalar row by a direct split-coordinate
contract. It identifies the six independent projected blocks of \(D^2P\),
evaluates their \(2\times2\) positive majorant exactly over rational decimal
inputs, and records the continuous-history variational equations needed to
produce those inputs. The current model adapter remains incomplete, so this
artifact proves no stable graph, separator crossing, or pulse onset.

The executable source is
[leaky_projected_return_hessian_stage4_contract.py](../src/canard_control/leaky_projected_return_hessian_stage4_contract.py),
the generator is
[leaky_projected_return_hessian_stage4_contract.py](../experiments/leaky_projected_return_hessian_stage4_contract.py),
and the registered output is
[leaky_projected_return_hessian_stage4_contract.json](../experiments/results/leaky_projected_return_hessian_stage4_contract.json).

## 1. Why the adapted norm does not solve the problem by itself

Let \(Y=E_s\oplus E_u\), with \(\dim E_u=1\), and use

\[
 \lVert(x_s,x_u)\rVert_{\mathrm{split}}
 =\lVert x_s\rVert_Y+\lvert x_u\rvert .
\]

The two coordinate projections have norm one in this direct-sum norm.
However, from the old history norm alone one only gets

\[
 \lVert x\rVert_{\mathrm{old}}
 \leq \lVert x\rVert_{\mathrm{split}}
 \leq (p_s^{\mathrm{old}}+p_u^{\mathrm{old}})
       \lVert x\rVert_{\mathrm{old}} .
\]

Therefore a black-box Hessian transfer can cost

\[
 C_{\mathrm{split}}
 \leq (p_s^{\mathrm{old}}+p_u^{\mathrm{old}})
 C_{\mathrm{old}} .
\]

Projection isometry alone does not establish a better nonlinear budget.
The useful route is to apply stable-history and unstable-scalar output
coordinates before taking norms, and validate the resulting blocks
directly.

## 2. There are six independent Hessian blocks

Write

\[
 B_i^{jk}
 =\Pi_i D^2P\big|_{E_j\times E_k},
 \qquad i,j,k\in\{s,u\}.
\]

Symmetry of the two input slots identifies \(B_i^{su}=B_i^{us}\), but it
does not remove the output index. Hence the independent blocks are

\[
\begin{array}{lll}
 B_s^{ss},&B_s^{su},&B_s^{uu},\\
 B_u^{ss},&B_u^{su},&B_u^{uu}.
\end{array}
\]

The certificate must provide uniform upper bounds
\(C_i^{jk}\geq\lVert B_i^{jk}\rVert\) on one validated split return ball.
A four-block shortcut omits two genuinely different input sectors and is
not an admissible theorem input.

## 3. The positive matrix majorant

Choose graph-box radii \(R_s,R_u>0\), a stable seed radius \(r>0\), a
sequence weight \(\beta\), and power estimates

\[
 \lVert A_s^n\rVert\leq K_s\rho_s^n,\qquad
 \lVert A_u^{-n}\rVert\leq K_u\rho_u^n,
 \qquad 0<\rho_s<\beta<1,\quad 0<\rho_u<1 .
\]

On the graph box, define

\[
\begin{aligned}
 L_{i,s}&=C_i^{ss}R_s+C_i^{su}R_u,\\
 L_{i,u}&=C_i^{su}R_s+C_i^{uu}R_u .
\end{aligned}
\]

Set

\[
 a_s=\frac{K_s}{\beta-\rho_s},\qquad
 a_u=\frac{K_u\rho_u}{1-\beta\rho_u}.
\]

The derivative majorant is

\[
 M=
 \begin{pmatrix}
  a_sL_{s,s}&a_sL_{s,u}\\
  a_uL_{u,s}&a_uL_{u,u}
 \end{pmatrix}.
\]

For a nonnegative \(2\times2\) matrix,

\[
 \rho(M)=\frac{m_{11}+m_{22}
 +\sqrt{(m_{11}-m_{22})^2+4m_{12}m_{21}}}{2}.
\]

The executable evaluator computes a rigorous upper bound by an integer
square-root enclosure. It also checks the equivalent exact rational
\(M\)-matrix conditions

\[
 m_{11}<1,\qquad m_{22}<1,\qquad
 \det(I-M)>0.
\]

When these inequalities hold,

\[
 w=(I-M)^{-1}\binom11>0
\]

is a canonical weight and \(Mw=w-(1,1)^T\). The artifact reports both the
Perron bound and the induced weighted row-sum bound.

## 4. Self-map residual, graph height, and derivative

Define the quadratic value bounds

\[
 Q_i(R_s,R_u)
 =\frac12 C_i^{ss}R_s^2
  +C_i^{su}R_sR_u
  +\frac12 C_i^{uu}R_u^2 .
\]

The componentwise self-map conditions are

\[
 K_sr+a_sQ_s\leq R_s,\qquad
 a_uQ_u\leq R_u .
\]

The artifact reports the image vector and the directed lower residual

\[
 \binom{R_s-K_sr-a_sQ_s}{R_u-a_uQ_u}.
\]

It separately requires \(R_s+R_u\) to lie inside a validated split return
ball. Thus a small matrix alone cannot certify a graph outside the domain
where the return map and its Hessian have been enclosed.

For the unstable graph height, the quadratic sequence weight gives the
sharper coefficient

\[
 a_u^{(2)}
 =\frac{K_u\rho_u}{1-\beta^2\rho_u},
 \qquad
 \lVert h\rVert\leq a_u^{(2)}Q_u .
\]

For sensitivity to a unit stable seed, let

\[
 \binom{d_s}{d_u}
 =(I-M)^{-1}\binom{K_s}{0}.
\]

The conservative reported derivative bound is
\(\lVert Dh\rVert\leq d_u\). A final theorem may sharpen the evaluation-at-zero
step, but it may not replace this bound by an unsupported binary estimate.

## 5. Continuous-history variational equations

Let \(X_t\) be a base RFDE history. For initial-history directions \(h,k\),
the first and second variations solve

\[
\begin{aligned}
 \dot U_h(t)&=DF(X_t)U_{h,t},\qquad U_{h,0}=h,\\
 \dot V_{hk}(t)&=DF(X_t)V_{hk,t}
 +D^2F(X_t)[U_{h,t},U_{k,t}],\qquad V_{hk,0}=0.
\end{aligned}
\]

For the leaky two-delay FHN field, the only nonzero second derivatives are
in the fast row. The current-voltage entry is

\[
 -2v(t)-6\varepsilon\kappa_3\bigl(v(t)-1\bigr),
\]

and the delayed-voltage entry for each delay is

\[
 3\varepsilon\kappa_3\bigl(v(t-\tau_j)-1\bigr),
 \qquad j=0,1.
\]

All mixed entries and all recovery-row Hessian entries vanish. The
corresponding third derivatives are

\[
 -2-6\varepsilon\kappa_3
 \quad\hbox{and}\quad
 3\varepsilon\kappa_3
\]

for the current and each delayed voltage slot, respectively. These formulas
make a directed method-of-steps or interval Taylor enclosure concrete rather
than leaving \(D^2F\) as an unspecified oracle.

## 6. First-return differentiation in physical time

Let the affine Route-C section be \(h_C=0\), and let \(T\) denote the first
positive physical return time near one period. A proof must exclude all
earlier section hits on the whole return tube. Set

\[
 a=Dh_C[\dot X_T]>0 .
\]

The first return-time derivative is

\[
 \tau_h=-\frac{Dh_C[U_h(T)]}{a}.
\]

For the second derivative, define

\[
 W_{hk}
 =V_{hk}(T)
 +\dot U_h(T)\tau_k+\dot U_k(T)\tau_h
 +\ddot X_T\tau_h\tau_k .
\]

Then

\[
 \tau_{hk}=-\frac{Dh_C[W_{hk}]}{a},
 \qquad
 D^2P[h,k]=W_{hk}+\dot X_T\tau_{hk}.
\]

Every term is a returned history segment in physical time. A normalized
Fourier-phase derivative has a different scale and cannot be substituted
without the period factors.

## 7. Minimal executable certificate input and output

A closing certificate must supply:

1. A validated split return ball, a unique first positive return on its
   tube, and a uniform event-speed lower bound.
2. Direct stable propagator power bounds with numeric \(K_s,\rho_s\), and
   direct one-dimensional unstable backward bounds with \(K_u,\rho_u\).
3. Continuous-history enclosures for \(U_s,U_u\), their physical-time
   derivatives at return, and \(V_{ss},V_{su},V_{uu}\).
4. Event traces
   \(\tau_s,\tau_u,W_{ss},W_{su},W_{uu},
   \tau_{ss},\tau_{su},\tau_{uu}\).
5. The six projected operator bounds, after applying the output coordinates
   and before taking norms.

From these inputs, the executable output consists of:

1. The matrix \(M\), a Perron upper bound, and a positive weighted row-sum
   certificate.
2. The nonlinear value vector, self-map image vector, and self-map residual
   vector.
3. A graph-box containment check against the validated return ball.
4. Bounds on \(\lVert h\rVert\) and \(\lVert Dh\rVert\).
5. A final Boolean conjunction that closes only if contraction, self-map,
   and domain containment all hold.

Finite sampled monodromy matrices, binary SVDs, or the old scalar
\(C_N\) transferred through norm equivalence do not satisfy this interface.

## 8. Registered status and the \(1.7\times10^{-3}\) target

The Stage-2 rates are imported:

\[
\rho_s=
0.995024916874584026786952988590018278886039540627453615,
\]

\[
\rho_u=
0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934,
\]

and

\[
\beta=
0.999378114609323003348369123573752284860754942578431701875.
\]

The numeric \(K_s\), all six \(C_i^{jk}\), and the validated split return
ball are still null. Therefore the registered matrix evaluation is
incomplete and every graph or pulse claim remains false.

The design box

\[
 R_s=10^{-3},\qquad R_u=7\times10^{-4},\qquad
 R_s+R_u=1.7\times10^{-3}
\]

is motivated by a wider third-return crossing diagnostic. It is a target,
not an enclosed graph radius, and is not used in a crossing or onset claim.
The immediate mathematical gap is now sharply localized: produce one
numeric stable power constant, one split return ball, and six directed
projected return-Hessian bounds.
