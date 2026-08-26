# Stage 3E: relative residual for the outer fundamental flow

## 1. Closed object

Stage 3D reduced the finite delay-word expansion to the primitives
\(F,G,H_j,L_{jk}\).  This certificate closes the first remaining transfer
problem: the instantaneous fundamental matrix and its inverse on the exact
\(10^{-8}\) outer-orbit/period ball.

Write normalized phase as \(x\), split \([0,1]\) into 1024 cells, and use the
centered coordinate \(y\in[-1,1]\).  On each cell the source constructs a
degree-24 matrix polynomial \(\widehat F(y)\).  The retained Fourier
coefficient is expanded to degree 12, while the modes above 96 and the
Fourier--Taylor remainder are paid as separate outward MPFR radii.

The crucial calculation is not an entrywise residual.  It forms

\[
 \operatorname{adj}(\widehat F)
 \bigl(\partial_y\widehat F-hA_{\rm exact}\widehat F\bigr)
\]

as one signed matrix polynomial on the same cell.  Only after its coefficient
convolutions have been carried out is a row norm taken.  The determinant
polynomial of that same \(\widehat F\) is bounded away from zero.  Interface
jumps between independently centered charts, including the initial chart
error, are included explicitly.

For \(F_{\rm exact}=\widehat F Y\), this gives

\[
 \lVert \widehat F^{-1}F_{\rm exact}-I\rVert_\infty
 \le e^\eta-1,
 \qquad
 \lVert G_{\rm exact}\widehat F-I\rVert_\infty
 \le \frac{e^\eta-1}{1-(e^\eta-1)}.
\]

The binary64 ODE solve selects the dyadic coefficients of \(\widehat F\);
its numerical accuracy is never assumed.  Every coefficient is treated as an
exact binary64 constant and its residual is enclosed against the exact orbit
ball.

## 2. Error ledger

The JSON artifact separates six positive contributions to \(\eta\):

1. the same-cell signed polynomial residual;
2. the omitted Fourier tail;
3. the Fourier--Taylor remainder;
4. the exact \(10^{-8}\) orbit ball;
5. the exact period ball;
6. all polynomial-chart interface jumps.

This separation identifies the actual frontier.  At degree 24 on 1024 cells,
the exact-orbit term, amplified by the fundamental condition number, is the
dominant contribution.  Increasing only the polynomial degree or partition
therefore is no longer the useful next step.

## 3. What the triangular H/L bound does and does not prove

The source propagates the certified F/G error through the definitions

\[
 C_j=G B_jF_{-\tau_j},\qquad H_j'=C_j,
 \qquad L_{jk}'=C_jH_k(\cdot-\tau_j).
\]

This produces finite, rigorous uniform majorants for an abstract center
\(\widehat C,\widehat H,\widehat L\).  It is intentionally marked
cancellation-blind: taking separate uniform norms pays the largest F/G
condition number and loses cancellation between delay words, the two
injection branches, and the phase row.

Consequently the triangular majorant is not inserted as \(E_v\) or \(E_w\).
The next certificate must validate piecewise H/L guide residuals and assemble
the complete 21-term signed density polynomial before taking row total
variation.  Until then, arbitrary-\(C^0\) contraction, nonlinear attraction,
capture and physical onset all remain false.
