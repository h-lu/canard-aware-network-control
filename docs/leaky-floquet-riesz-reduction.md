# Finite analytic Riesz reduction for the leaky Floquet indices

Status: **the infinite-dimensional tail is removed for both validated leaky
branches; neither unstable index is yet counted.**  The result reduces the
remaining characteristic-value problem to an analytic
\(258\times258\) Schur determinant on a compact logarithmic keyhole.  It
does not validate that determinant on the keyhole boundary or compute its
winding.

## The logarithmic pencil

For a nonzero multiplier \(\mu\) with \(|\mu|\geq1\), choose

\[
 s=\log|\mu|+i\operatorname{Arg}\mu,
 \qquad \Re s\geq0,
 \qquad -\pi\leq\Im s\leq\pi,
 \qquad \mu=e^s.
\]

The two boundary values \(\Im s=\pm\pi\) represent the same negative-real
multiplier.  This causes no problem for coverage or invertibility, but a
future winding calculation must identify the two copies or use a half-open
seam.

Let \(X(\theta)=x(T\theta)\), let \(g\) denote the instantaneous voltage
coefficient, and let \(H_j\) denote the two delayed variational
coefficients.  Periodicizing a Floquet solution gives

\[
\begin{aligned}
 (\mathcal L_sy)_v={}&(\partial_\theta+s)y_v-Tg*y_v+Ty_w\\
 &-T\sum_{j=0}^1e^{-s\tau_j/T}
 H_j*S_{\tau_j/T}y_v,\\
 (\mathcal L_sy)_w={}&(\partial_\theta+s)y_w
 -T\varepsilon y_v+T\varepsilon y_w .
\end{aligned}
\]

The bottom-right sign is positive: moving
\(T\varepsilon(y_v-y_w)\) to the left gives
\(-T\varepsilon y_v+T\varepsilon y_w\).  Thus the recovery-input column has
norm bound \(1+\varepsilon\), while the recovery contribution in the
voltage-input column is \(\varepsilon\).

Every nonzero multiplier of modulus at least one is represented in this
closed principal strip.  The exponential map has nonzero derivative there,
so it preserves local multiplicity away from the duplicated boundary seam.

## Uniform orbit-ball coefficient bounds

The coefficient norm is the complex-modulus Wiener norm.  For a directed
rectangle the computation uses
\(|z|\leq|\Re z|+|\Im z|\); this is an outward majorant of the complex
modulus, not a claim that rotations preserve the rectangular one-norm.
Fourier translations are isometries in the underlying complex-modulus
Wiener norm.

If the exact voltage is within Wiener distance \(r\) of the source
polynomial \(\bar v\), then

\[
 \|v^2-\bar v^2\|
 \leq(2\|\bar v\|r+r^2),
\]

and the same inequality holds for \(v-1\).  Consequently the instantaneous
coefficient variation is bounded by

\[
 2\|\bar v\|r+r^2
 +3\varepsilon\kappa_3
 \{2\|\bar v-1\|r+r^2\}.
\]

For either delayed slot the corresponding increment is

\[
 \frac{3\varepsilon\kappa_3}{2}
 \{2\|\bar v-1\|r+r^2\}.
\]

No omitted period-shift term is needed in this scalar norm estimate:
although the exact and center shifts use different values of \(\tau_j/T\),
each shift is an isometry, so their coefficient norms equal the norms of the
respective unshifted coefficients.  The two delayed-slot increments are
then added.  The correction ball also gives \(T\leq\bar T+r\).

The resulting lower-order operator bound is the maximum of its two column
sums,

\[
 B=\max\{\|g\|+\|H_0\|+\|H_1\|+\varepsilon,
             1+\varepsilon\}.
\]

For \(\Re s\geq0\), the additional Bloch factors satisfy
\(|e^{-s\tau_j/T}|\leq1\), so the same bound is uniform in the whole right
half-plane.

## Uniform tail inverse

Let \(P\) retain \(|k|\leq64\) and let \(Q=I-P\).  If
\(s=\sigma+i\eta\), with \(\sigma\geq0\) and \(|\eta|\leq\pi\), then for
\(|k|\geq65\),

\[
 |s+2\pi ik|
 \geq|2\pi k+\eta|
 \geq2\pi|k|-\pi
 \geq129\pi.
\]

Writing the tail block as its Fourier diagonal plus its lower-order part,
the source-bound directed estimates give

\[
 \|(D_s|_Q)^{-1}QK_sQ\|
 \leq\frac{T_+B}{129\pi}<1.
\]

The certified upper contractions are approximately \(0.06935\) for the
inner branch and \(0.33058\) for the outer branch.  Hence
\(Q\mathcal L_sQ\) has a uniformly convergent analytic Neumann inverse on
the closed principal right half-strip.

## Analytic Schur equivalence and multiplicity

On the periodic Wiener derivative domain, write

\[
 \mathcal L_s=\begin{pmatrix}A&B_1\\C&D\end{pmatrix},
 \qquad D=Q\mathcal L_sQ,
\]

and define

\[
 \mathscr S(s)=A-B_1D^{-1}C.
\]

The exact analytic block factorization is

\[
 \begin{pmatrix}I&-B_1D^{-1}\\0&I\end{pmatrix}
 \mathcal L_s
 \begin{pmatrix}I&0\\-D^{-1}C&I\end{pmatrix}
 =\begin{pmatrix}\mathscr S(s)&0\\0&D\end{pmatrix}.
\]

Both triangular factors and \(D) are analytically invertible.  Therefore
the characteristic values of \(\mathcal L_s\) in the strip, including their
analytic algebraic multiplicities, are precisely the zeros of
\(\det\mathscr S(s)\).  Since two state components and 129 Fourier modes are
retained, \(\mathscr S(s)\) has complex dimension
\(2(2\cdot64+1)=258\).

For \(\Re s\geq256\), one instead has
\(|s+2\pi ik|\geq\Re s\geq256\) for every Fourier mode.  The second Neumann
ratios are approximately \(0.10979\) and \(0.52333\), so this entire far
right half-plane is excluded.

## Local complex half-disk

The parent theorem supplied a phase-bordered inverse and algebraic
simplicity of the neutral multiplier.  Its local estimates extend from the
imaginary axis to \(\Re s\geq0\), because for \(\alpha>0\)

\[
 e^{-\alpha s}-1
 =-\alpha s\int_0^1e^{-t\alpha s}\,dt,
\]

and

\[
 e^{-\alpha s}-1+\alpha s
 =\alpha^2s^2\int_0^1(1-t)e^{-t\alpha s}\,dt,
\]

while \(|e^{-t\alpha s}|\leq1\) in that half-plane.  The stored first- and
second-order coefficients therefore exclude all characteristic values in

\[
 \Re s\geq0,qquad0<|s|\leq\delta_i,
\]

with

\[
 \delta_{\rm inner}>0.0039588084194080,
 \qquad
 \delta_{\rm outer}>0.0028635052681275.
\]

This is a punctured complex half-disk, not merely a unit-circle arc.

## Exact remaining gate

The remaining region is compact, finite dimensional, and still open.  One
must:

1. choose a seam convention for the principal logarithm;
2. validate \(\mathscr S(s)\) as invertible on the complete keyhole
   boundary between the local disk and \(\Re s=256\);
3. compute its directed determinant winding;
4. prove winding zero for the outer branch and winding one for the inner
   branch.

Until those integers are enclosed, compact-keyhole invertibility, full
unit-circle exclusion, outer attraction, the inner Floquet index and stable
manifold, and physical pulse onset all remain unproved.
