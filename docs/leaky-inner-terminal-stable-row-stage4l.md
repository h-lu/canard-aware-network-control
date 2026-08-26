# Stage 4L: direct terminal stable-row certificate

Status: **PROVED DISCRETE LINEAR INGRESS.**  This stage proves a bound for
the selected near-one-period *linear* phase-fixed map.  It does not prove
that the selected event is the first positive return, and it proves no
nonlinear return tube, stable graph, pulse intersection, crossing, or onset
statement.

## Result

On

\[
 \Sigma _0=\{h\in Y:h_v(0)=0\},\qquad
 Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R,
\]

let

\[
 A=\Pi_T\mathcal U(T,0)|_{\Sigma_0},\qquad
 P_s=I-qf,
\]

where (q=q^\Sigma), (f=f_0/f_0(q^\Sigma)), and

\[
 \Pi_Ty=y-\dot X_T\frac{y_v(0)}{\dot v(T)}.
\]

The source-bound common atom--density calculation proves

\[
 \boxed{\ \|AP_s\|_{\Sigma_0\to Y}
       \le 0.009896427481610001 <0.1.\ }
\]

The exact eigen-relations give

\[
 AP_s=P_sA=P_sAP_s,
 \qquad AP_s(\Sigma_0)\subset E_s:=\ker f.
\]

Consequently, with the inherited (Y) norm on (E_s),

\[
 \|A_s^n\|_{E_s\to Y}\le 0.1^n,
 \qquad K_s=1.
\]

This is the discrete stable-power input requested by the matrix
Lyapunov--Perron theorem.  No additional numerical left projection is used:
the output belongs to (E_s) by the exact intertwining identity.

## What is enclosed in one row

For every returned voltage-history phase and for the recovery output, the
certificate forms

\[
 \mathfrak m_\theta
   =R_\theta\Pi_T\mathcal U(T,0)(I-qf)
\]

coefficientwise before taking any modulus.  Thus both the unstable
deflation and terminal event correction retain their signed cancellation.
This is the required double rank-one construction before the TV norm.
The current-voltage (delta_0) atom is removed exactly by the quotient

\[
 \|m|_{\Sigma_0}\|=\inf_c\|m-c\ell_0\|,
 \qquad \ell_0(h)=h_v(0),
\]

while the current-recovery atom remains active.  A finite-node norm or a
Gaussian quadrature is not used.

The continuous centre calculation covers 641 returned-history phase cells
plus one recovery-output row, against 640 input-history cells, hence 410,880
support rectangles.  Every delay
activation rectangle that meets a diagonal is enclosed both with the word
absent and with it present.  Cubic Taylor balls are converted to bivariate
Bernstein coefficients, absolute density bounds are integrated outward,
and the output-phase supremum is taken over entire cells.  The resulting
common centre bound is

\[
 0.004362999710080374.
\]

## True period and exact word support

The Fourier dictionaries use the displayed binary64 centre period only as
a centre.  The proof separately encloses the true period as

\[
 18.18620994912592099<T<18.18620994912992100
\]

and uses the exact delays \(\tau_0=4\sqrt5\),
\(\tau_1=5\sqrt5\).  Directed lower margins are

\[
\begin{aligned}
 T-\tau_1&>7.005870061626971,\\
 T-2\tau_0&>0.2976661291276024,\\
 \tau_0+\tau_1-T&>1.938401848368187,\\
 3\tau_0-T&>8.646605780867554.
\end{aligned}
\]

Therefore the complete returned history lies after time zero and its only
method-of-steps words are

\[
 \varnothing,\qquad(0),\qquad(1),\qquad(0,0).
\]

The combined displacement between the exact \(T\)/delay grid and the centre
grid is below \(4.0050\times10^{-12}\).  A source-derived common-coordinate
Lipschitz candidate is \(594.72<1000\), so the explicit remainder through
the true \(T_+\) is below \(4.0050\times10^{-9}\).  This is what closes the
small terminal extension; the centre period is never treated as exact.

## Directed error ledger

The final upper bound is the outward sum of:

| term | upper bound |
|---|---:|
| common continuous centre | (0.004362999710080374) |
| independent binary Bernstein guard | (0.000010000000000001) |
| Stage 4I primitive image | (0.001463546183857267) |
| normalized (f), (q), and event rank-one uncertainty | (0.004059226965383500) |
| raw terminal event-ratio uncertainty | (6.506172913144082\times10^{-7}) |
| true-(T_+)/delay coordinate shift | (4.004997545987388\times10^{-9}) |

Each displayed component is rounded outward independently.  Their displayed
sum is at most \(0.009896427481610003\); the unrounded directed sum is the
sharper theorem bound in the result above.

The binary polynomial centre is not justified by `nextafter` alone.  Each
polynomial/outer-product kernel carries a coefficientwise ball.  From the
degree-(6,9) Bernstein tensor, at most ten outer-product terms, both
activation cases, and the 640-term positive reduction, the source derives
70,440 worst-case real operations along one guarded output-bound path and
checks this against the registered cap 131,072.  It also audits every
`BallPoly` and bivariate intermediate array; their actual envelope is below
2347, hence below the registered analytic cap 4096.  Together with
\(u=2^{-53}\), the corresponding \(\gamma_n\) is below
\(1.456\times 10^{-11}\).  The coefficientwise guard is \(10^{-10}\), and an
independent \(10^{-5}\) final guard strictly dominates the remaining modulus
and positive-reduction error (below \(5.97\times 10^{-8}\)).  These
connections, not a bare operation-count assertion, are replayed by the
validator.

The Stage 4I primitive tubes enter only through their direct algebraic image.
Neither the unknown terminal norm nor (K_s) appears in its own error
propagation, so this route bypasses the full Stage 4J intermediate
((s,t))-residual calculation without circularity.

## Scope boundary

The result concerns the selected phase-fixed discrete linear operator.  The
following all remain false: first-positive-return identification, exclusion
of an earlier hit, nonlinear/split return-tube containment, the six uniform
Hessian blocks, a quantitative stable graph, full-pulse seed containment,
stable-sheet intersection, separator crossing, physical onset, two-sided
routing, and network safety.
In particular: no nonlinear return tube, no stable graph, no crossing, and
no onset theorem are claimed here.

Generation performs a fresh independent replay before it fsyncs and
atomically replaces the registered JSON result.  Hostile tests reject, among
other changes, separate norming of rank-one pieces, omission of the event
row or a word, centre-(T)-only coverage, sampled maxima, treating the
section-null voltage atom as active, circular use of (K_s), and any
promotion to first-return or nonlinear conclusions.
The frozen source manifest includes those hostile tests and the directly
used MPFR directed-interval implementation, in addition to the source,
generator, theorem note, and design contract.
