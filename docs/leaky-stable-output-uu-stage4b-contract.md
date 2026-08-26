# Stage 4B: directed \(s\leftarrow uu\) contract

## Outcome

Stage 4A shows a genuine route to closure, but its three meshes are not
interval evidence. The tight block is

\[
 \Pi_sD^2P(q,q),
\]

not the largest block in absolute size. The isolated pilot threshold for
the stable-output \(uu\) block is about \(13.915\). Stage 4B chooses the
safer directed target

\[
 \boxed{C_s^{uu}\leq12}.
\]

The other five simultaneous design targets are roughly \(1.5\) times their
Stage-4A heuristic envelopes. With these targets, the exact Stage-4 matrix
evaluator gives

\[
 \rho(M)<0.074,\qquad
 \text{weighted row sum}<0.681,
\]

and a stable self-map residual above \(9.9\times10^{-5}\). These are design
margins, not theorem conclusions.

The executable contract is
[leaky_stable_output_uu_stage4b_contract.py](../src/canard_control/leaky_stable_output_uu_stage4b_contract.py),
the generator is
[leaky_stable_output_uu_stage4b_contract.py](../experiments/leaky_stable_output_uu_stage4b_contract.py),
and the result is
[leaky_stable_output_uu_stage4b_contract.json](../experiments/results/leaky_stable_output_uu_stage4b_contract.json).

## 1. Why \(s\leftarrow uu\) is the bottleneck

The Stage-4A heuristic envelope is

\[
 \widehat C_s^{uu}=7.94681563672845125978.
\]

Its isolated closing multiplier is about \(1.7510\), while the largest
absolute block \(\widehat C_u^{uu}=26.1969\) can be inflated by more than a
factor \(44\) when the other blocks are held fixed. Stable-output \(uu\)
consumes the stable self-map slack first.

At the \(240\)-step center,

\[
 C_{s,\mathrm{pilot}}^{uu}=7.26111932801827375528.
\]

The target \(12\) leaves \(4.73888\) above this center and \(4.05318\) above
the heuristic mesh envelope. The heuristic difference is not an interval
error and cannot be entered into a proof.

## 2. Continuous histories, not nodal matrices

For a linear RFDE along a base history, the solution operator on the
declared sup-norm history space has a current-state atomic part and
absolutely continuous density kernels acting on the voltage history. Its
operator norm is bounded by the atom magnitudes plus the total variations
of the density kernels.

Stage 4B therefore requires outward-rounded polynomial enclosures of:

1. every current-state atom;
2. every history-density kernel on each method-of-steps cell;
3. every delay seam and cell residual;
4. the total-variation integrals used in the history sup norm.

A finite nodal matrix, even in long-double arithmetic and on three
converging meshes, does not satisfy this interface.

For

\[
 A_0(t)=
 \begin{pmatrix}a(t)&-1\\ \varepsilon&-\varepsilon\end{pmatrix},
\]

the Euclidean logarithmic norm is

\[
 \mu_2(A_0)
 =\frac{a-\varepsilon+
 \sqrt{(a+\varepsilon)^2+(1-\varepsilon)^2}}2.
\]

A moving-center error radius can obey

\[
 r'\leq\mu_2(A_0)r
 +\lVert A_1\rVert r_{\tau_0}
 +\lVert A_2\rVert r_{\tau_1}
 +R_{\mathrm{cell}}.
\]

The raw logarithmic-norm estimate is expected to be too expansive over one
period. The contract therefore permits a pilot-centered moving frame, but
the frame, inverse, residual, and delay couplings must all be interval
enclosed.

## 3. Only \(U_q\) and \(V_{qq}\) are needed

Let \(q\) be the Stage-3 enclosed Route-C unstable section eigenhistory,
normalized to one unstable coordinate. For each base history \(X\) in the
complete split ball, propagate

\[
\dot U_q=DF(X_t)U_{q,t},\qquad U_{q,0}=q,
\]

and

\[
\dot V_{qq}
=DF(X_t)V_{qq,t}
+D^2F(X_t)[U_{q,t},U_{q,t}],
\qquad V_{qq,0}=0.
\]

The fast-row forcing is

\[
\bigl[-2v-6\varepsilon\kappa_3(v-1)\bigr]U_{q,v}(t)^2
\]

plus, for \(j=0,1\),

\[
3\varepsilon\kappa_3
\bigl(v(t-\tau_j)-1\bigr)
U_{q,v}(t-\tau_j)^2.
\]

The recovery-row second-order forcing is zero. This specialization avoids
propagating the full \(d^3\) nodal Hessian tensor.

The enclosure must be uniform over the entire split ball. Propagation only
along the periodic orbit establishes a base Hessian, not the uniform block
bound needed by the graph theorem.

## 4. The actual split return tube

The target input ball is

\[
 R_s+R_u=10^{-3}+7\times10^{-4}=1.7\times10^{-3}.
\]

Stage 2 already validates the local Route-C voltage section on a history
ball of radius \(10^{-2}\), with event-speed lower bound about \(0.20675\).
Stage 4B must still prove that the whole returned-history tube from the
split input ball stays inside that section ball during the event window.
It must also prove one positive-oriented event near one period and exclude
all earlier hits for every history in the ball.

At the physical return time,

\[
 \tau_q=-\frac{Dh_C[U_q(T)]}{Dh_C[\dot X_T]},
\]

\[
 W_{qq}
 =V_{qq}(T)+2\dot U_q(T)\tau_q+\ddot X_T\tau_q^2,
\]

\[
 \tau_{qq}=-\frac{Dh_C[W_{qq}]}{Dh_C[\dot X_T]},
 \qquad
 Y_{qq}=W_{qq}+\dot X_T\tau_{qq}.
\]

All quantities are complete history segments in physical time.

## 5. Stable deflation must preserve cancellation

The required output is not an absolute bound on \(Y_{qq}\). It is

\[
 \Pi_sY_{qq}
 =Y_{qq}-q\,\frac{f(Y_{qq})}{f(q)},
\]

where \(f\) is the unstable adjoint history functional. This subtraction
must be interval evaluated as one correlated expression before taking the
sup norm. Separately bounding \(Y_{qq}\), \(q\), and \(f(Y_{qq})\) by
absolute values destroys the cancellation responsible for the small
stable-output block.

Stage 3 supplies the right eigenhistory but not a directed upper enclosure
of the left adjoint action. Stage 4B therefore accepts either:

1. an adjoint Grushin eigencolumn with directed normalization and its
   atom-plus-density action; or
2. a direct bordered stable-deflation solve for this specific
   \(Y_{qq}\).

A global transfer through \(\lVert P_s\rVert\) is explicitly disallowed.

## 6. Safe simultaneous target row

The six nonrigorous targets are

\[
\begin{array}{lll}
 C_s^{ss}=0.033704,&C_s^{su}=0.133147,&C_s^{uu}=12,\\
 C_u^{ss}=0.445398,&C_u^{su}=0.424645,&C_u^{uu}=39.2954.
\end{array}
\]

The exact matrix evaluator yields a Perron upper bound about \(0.073825\).
The self-map image is approximately

\[
 \binom{9.00647\times10^{-4}}{1.23785\times10^{-5}},
\]

so both component residuals remain positive. This row quantifies how coarse
the first directed enclosures may be. None of its six entries is currently
a directed bound.

## 7. Current strict status

The strict ingress keeps null:

- the all-power \(K_s\);
- the validated \(1.7\times10^{-3}\) split return ball;
- the returned-history tube radius and return-time bracket;
- the uniform event-speed bound on that tube;
- all six projected Hessian blocks.

It also keeps false every kernel, orbit-ball, return, event-Hessian,
adjoint-deflation, and uniform-block proof flag. Therefore Stage 4B
currently closes only a conditional executable contract, not a stable
graph or pulse theorem.
