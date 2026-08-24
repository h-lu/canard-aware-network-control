# The first outward-rounded physical cell of the target C4 chart

Status: **one rigorous computer-assisted physical cell.**  At the frozen
target anchor, the state and its true transverse variation are enclosed on

\[
 C_0=[-3,-2.99]\times[-1/20,1/20].
\]

The calculation includes directed MPFR rounding, a strict Picard wrapping
box, and an outward-rounded local truncation remainder.  It proves all three
physical P-matrix inequalities on this one rectangle.  It does not yet cover
the rest of the physical strip, the incoming C4-history strip, the two scalar
cross-separation gates, or an enlarged collar.  Consequently no global chart
embedding, degree theorem, fixed graph, or canard root follows from this
single cell.

## 1. Why the first cell is a finite-dimensional validated ODE

Write \(z=(X,Y)\) and \(v=\partial_\lambda z\).  The frozen parameters are

\[
 \rho=\frac1{\sqrt5},\qquad
 \nu=0.21256022233963731,\qquad \eta=0,
\]

where the displayed decimal is treated as an exact rational input.  For
\(t\in[-3,-2.99]\), the latest active delayed time is
\(t-4\leq-6.99\).  This lies strictly to the left of the C4 patch support
\([-3.5,-3]\).  Hence the delayed X coordinates are the exact affine
functions

\[
 X_d(t)=-\frac{t-d+q}{2},\qquad d\in\{4,5\},
\]

and \(\partial_\lambda X_d=0\).  The \(\Theta_*\)-slot is multiplied by
\(\eta=0\).  Thus the RFDE becomes, on this cell,

\[
\begin{aligned}
 X'={}&Y-X^2-\frac\rho3X^3
 +\frac\rho5\left(\frac{X_4+X_5}{2}-X\right)
 +\frac{\rho^3}{4}\left(\frac{X_4^3+X_5^3}{2}-X^3\right),\\
 Y'={}&-X+\rho\nu,\\
 v_X'={}&a(X)v_X+v_Y,\qquad v_Y'=-v_X,\\
 a(X)={}&-2X-\rho X^2-\frac\rho5-\frac{3\rho^3}{4}X^2.
\end{aligned}
\]

At the exact C4 seam the state correction has zero value, so

\[
 z(-3,\lambda)=(X_e,Y_e+\lambda),\qquad
 v(-3,\lambda)=(0,1).
\]

This reduction is special to the initial method-of-steps cell; it is not used
past the point where delayed arguments enter the Hermite patch or the
previously integrated flow.  A separate exact SymPy audit substitutes these
four reduced equations into the authoritative RFDE slot algebra and returns
four identically zero defects.  A second symbolic audit ties the duplicated
decimal anchors to the C4 seam, differentiates the two affine delayed
histories, reconstructs all four total derivatives used below by the chain
rule, and verifies the determinant of the output frame imported from the
univalence contract; its sixteen defects also vanish identically.

## 2. Directed rounding and the wrapping proof

All operations are evaluated by the repository's MPFR-backed
`DirectedInterval` arithmetic at 192 bits.  Each lower endpoint is rounded
downward and each upper endpoint upward.  The stored decimal endpoints are
pushed outward and reparsed before acceptance.  A second 256-bit evaluation
is required to nest inside the primary enclosure.

In coordinate order \((X,Y,v_X,v_Y)\), choose

\[
 B=[1.524,1.532]\times[0.967,1.084]
   \times[-0.001,0.011]\times[0.999,1.001].
\]

Let \(T=[-3,-2.99]\), \(S=[0,0.01]\), and let \(Z_0\) be the outward
interval enclosure of all initial values for
\(\lambda\in[-1/20,1/20]\).  Direct interval evaluation verifies

\[
 Z_0+S f(T,B)\subset\operatorname{int}B.
\]

The lower left/right inclusion gaps in the four coordinates are at least

\[
 (9.99\times10^{-4},\ 1.336\times10^{-3},\ 9.99\times10^{-4},\
  8.89\times10^{-4})
\]

and

\[
 (1.210\times10^{-3},\ 1.293\times10^{-3},\ 9.46\times10^{-4},\
  9.90\times10^{-4}),
\]

respectively.  The interval Picard operator therefore maps the continuous
\(B\)-valued functions strictly into themselves.  Polynomial local
Lipschitz continuity gives uniqueness, and every state--variation trajectory
from the label cell remains in \(B\).  The dependency loss in this rectangular
box is retained explicitly as wrapping; it is not estimated from sampled
trajectories.

## 3. Local truncation and the P-matrix margins

For \(0\leq s\leq0.01\), the integral Taylor formula gives

\[
 z(-3+s)=z(-3)+s f(-3,z(-3))+R_2(s),
 \qquad
 |(R_2)_i|\leq\frac{s^2}{2}
       \sup_{T\times B}\left|\frac{d f_i}{dt}\right|.
\]

The total derivative includes the time derivatives of both known delayed
forcings.  Its interval expression is evaluated on \(T\times B\); the four
outward upper bounds for the resulting local truncation radii are

\[
\begin{split}
 &(2.793751538984923\times10^{-5},
   2.881188682522345\times10^{-5},\\
 &\hspace{32mm}2.198470978285369\times10^{-4},
   5.026802534585647\times10^{-5}).
\end{split}
\]

Evaluating the state vector field on this narrower Taylor enclosure and using
the fixed physical frame

\[
 L_P=\begin{pmatrix}-7&2\\3&1\end{pmatrix}
\]

(whose defining source and determinant \(-13\) are recorded in the
manifest)

gives the rigorous interval lower bounds

\[
\begin{aligned}
 \inf_{C_0}(-7,2)z_t
   &\geq 0.1101001091965242296,\\
 \inf_{C_0}(3,1)z_\lambda
   &\geq 0.9992901906811685328,\\
 \inf_{C_0}\det D(L_P\Psi)
   &\geq 5.3462558514489728497.
\end{aligned}
\]

In addition,

\[
 \det D\Psi\subset
 [-0.570108416784882748,-0.411250450111459449].
\]

Thus this rectangle is an accepted physical P-matrix cell in the sense of the
univalence contract.  These are interval conclusions, not margins inferred
from the earlier DOP853 candidate.

## 4. Backend audit and remaining obstruction

The repository already contained genuine MPFR-directed elementary interval
arithmetic and several Fourier-tail validators.  It did not contain a
validated interval ODE or Taylor-model method of steps.  SciPy dense output is
nonvalidated, and the installed `mpmath.iv` interface does not supply the
proof-specific Picard, truncation, wrapping, or provenance checks needed here.
The present backend therefore implements the minimal first-cell Picard--Taylor
argument directly on top of the audited MPFR arithmetic.

The next mathematical obstruction is continuation, not positivity on this
first cell.  Later cells must carry validated enclosures of previously
computed delayed state and variation segments while controlling wrapping.
Only after a full physical cover is combined with the independent
C4-history cover, cross-separation, and an enlarged label collar may the
conditional Gale--Nikaido argument be used to claim a global target chart.

## 5. Reproduction

Run

```text
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_first_step_interval.py
```

The generator records the proof source, directed-interval backend,
authoritative physical-model source, C4-seam source, univalence-contract
source, note, generator, Python, gmpy2, and MPFR provenance and writes the
complete outward enclosures to the result JSON.
