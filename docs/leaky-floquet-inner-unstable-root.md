# A simple positive Floquet exponent of the inner leaky orbit

Status: **one characteristic value is proved, locally and for the validated
center orbit.**  The logarithmic Floquet pencil has exactly one
characteristic value, counted with analytic algebraic multiplicity, in the
disk

\[
 D_u=\{s\in\mathbb C:|s-s_c|<1/10\},
 \qquad s_c=0.6983604129095.
\]

That value is real, simple, and positive.  Its multiplier is therefore real
and strictly larger than one.  This theorem does not count the rest of the
right-half logarithmic strip and hence does not yet prove the total inner
unstable index.

## 1. Correct Fourier form of the delayed pencil

Let (b) be the unshifted derivative of the delayed nonlinearity.  The
physical variational term is (b(t-\tau)y(t-\tau)).  It has two exactly
equivalent Fourier representations:

\[
 \sum_m b_{k-m}e^{-2\pi i k\alpha}y_m
 =\sum_m (b_\alpha)_{k-m}e^{-2\pi i m\alpha}y_m,
 \qquad (b_\alpha)_n=b_ne^{-2\pi i n\alpha}. \tag{1.1}
\]

The executable proof uses the left side: **unshifted coefficient plus output
row phase**.  It checks it entry by entry against the right side, **shifted
coefficient plus input column phase**, on finite--finite, finite--tail, and
tail--finite rectangular blocks.  Directed boxes overlap on every checked
entry.  Both illegal mixtures--unshifted plus column and shifted plus
row--are separated by more than (0.35), so a column-only error cannot pass
silently.

For the leaky recovery model the full logarithmic pencil is

\[
\begin{aligned}
 (\mathcal L_sy)_v={}&(\partial_\theta+s)y_v-Tg*y_v+Ty_w\\
 &-T\sum_{j=0}^1 e^{-(s+\partial_\theta)\tau_j/T}
   (b*y_v),\\
 (\mathcal L_sy)_w={}&(\partial_\theta+s)y_w
 -T\varepsilon y_v+T\varepsilon y_w .
\end{aligned} \tag{1.2}
\]

The bottom-right sign in (1.2) is positive.  Every matrix and tail estimate
below uses the two complex components with the Wiener (ell^1) modulus
norm.  Split real/imaginary sums are only outward majorants for numerical
products.

## 2. A source-bound nested orbit ball

The original inner-orbit theorem proves a radius (10^{-5}), but its
validated radii polynomial is monotone on that interval.  Let
(Y,Z_0,Z_1,Z_2,Z_3) denote the stored outward bounds.  At any smaller
(r\ge0), the same proof gives

\[
 q(r)=Z_0+Z_1r+Z_2r^2+Z_3r^3,
 \qquad
 p(r)=Y+q(r)r-r. \tag{2.1}
\]

Directed MPFR substitution at (r=10^{-12}) gives

\[
 q(10^{-12})
 <0.031542592671804272,
 \qquad
 -p(10^{-12})
 >7.78565109686\times10^{-13}. \tag{2.2}
\]

Hence the exact center orbit lies in the nested radius (10^{-12}) ball.
This is a strict consequence of the already validated center radii
polynomial; it is not a new orbit solve and does not establish a common
parameter-box orbit.

All coefficient estimates are recomputed at the nested radius.  In
particular, the instantaneous and delayed quadratic variations retain the
terms linear and quadratic in (r), the period is allowed to vary by (r),
and the delay factors include the resulting change of (\tau_j/T).

## 3. Infinite-dimensional Grushin problem

Let (P) retain the modes (|k|\le64), and let (Q=I-P).  At the center
(s_c), the cutoff-64 matrix has smallest singular value of order
(10^{-10}), while the second smallest singular value is greater than
(0.95105).  These numbers only choose a one-dimensional border.

Because this discovery matrix is nearly singular, the last few binary64
digits of its SVD border depend on the OpenBLAS reduction schedule.  The
artifact therefore pins `OPENBLAS_NUM_THREADS=8` before NumPy is loaded.
Validation from any differently configured caller performs the full replay
in a fresh subprocess with that pinned schedule.  This is a reproducibility
condition for the stored binary border, not an assumption in the MPFR proof:
every realized border is still enclosed and checked by the directed
complete-operator bounds below.

If (u) and (v) are the binary64 left and right singular vectors, define

\[
 \mathcal G(s)=
 \begin{pmatrix}
  \mathcal L_s&20u\\
  5v^*&0
 \end{pmatrix}. \tag{3.1}
\]

The left vector is the added range column and the right vector defines the
domain functional.  Reversing those roles is not harmless: it greatly
degrades the complete-operator inverse even though the finite square matrix
can remain nonsingular.

The preconditioner consists of the directed finite bordered inverse and the
two exact tail diagonals

\[
 (s_c+2\pi ik)^{-1},
 \qquad
 (s_c+2\pi ik+T\varepsilon)^{-1}. \tag{3.2}
\]

The defect includes the full coefficient support through mode (128), both
finite--tail couplings, the nested orbit ball, period variation, and first-
and second-order delay-exponential remainders.  The period-induced phase
variation follows physical output modes.  The two finite-output blocks use
(|k|\le64).  Tail--finite outputs reach (|k|\le192), but their aligned
factor (s+2\pi i k) is treated only after the fast diagonal inverse, giving
the rigorous (1+\|A_{\rm tail}\|h) cancellation rather than an input/output
mix.

On the entire closed disk (\overline D_u), the executable certificate stores
a strict complete-Grushin contraction below one.  This bound is recomputed
from the physical row-phase pencil; no number from the rejected mixed
representation is reused.

Consequently (mathcal G(s)) is analytically invertible throughout the
disk.  Writing its inverse in Grushin blocks defines a scalar analytic
effective Hamiltonian (E_{-+}(s)).  The usual Grushin factorization shows
that (s) is a characteristic value of (mathcal L_s) exactly when
(E_{-+}(s)=0), with analytic algebraic multiplicity preserved.

## 4. Scalar Rouché count

The boundary circle is covered by 256 certified arcs.  On each arc a fresh
finite bordered inverse is combined with the same infinite tail bounds.
The affine reference is

\[
 h(s)=a_*(s-s_c), \qquad |a_*|>0. \tag{4.1}
\]

Thus (\min_{\partial D_u}|h|>0).

The cellwise Newton expansion includes the center inverse defect, the exact
orbit and period errors, finite--tail feedback, and the first two delay
exponential derivatives.  The tracked certificate verifies the strict
Rouché inequality

\[
 \max_{\partial D_u}|E_{-+}-h|
 <\min_{\partial D_u}|h|. \tag{4.2}
\]

Since (h) has one simple zero in
(D_u), (E_{-+}), and hence the complete RFDE pencil, has exactly one
characteristic value there, counted with algebraic multiplicity.  Its total
multiplicity is one.

The pencil is real and (D_u) is invariant under conjugation.  A nonreal
root would bring its distinct conjugate into the same disk, contradicting
uniqueness.  The root is therefore real.  Moreover,

\[
 0.5983604129095 < s_u < 0.7983604129095,
\]

so (s_u>0) and

\[
 1.8 < \mu_u=e^{s_u}<2.3. \tag{4.3}
\]

## 5. Exact scope and continuation interface

The proof leaves a strictly positive operator-norm budget for an additional
analytic pencil perturbation on this same disk.  This is an interface for a
later parameter-continuation proof;
it does not by itself validate any ((a,\kappa_3)) box.

Nothing here proves that there are no further open-right-half-plane roots
outside (D_u).  The remaining compact keyhole, the total inner unstable
multiplier count, the one-dimensional unstable/stable manifold package,
the pulse intersection, routed basin sides, and physical onset all remain
open.

In particular, the executable ledger records
`inner_no_other_right_half_roots_validated=false`.  The shortest remaining
route is a compact principal-strip cover after removing the neutral-root disk
and this positive-root disk: reuse the same full Grushin inverse/tail-Neumann
cell test on rectangles, use the existing large-|Im s| and Re s>=256
exclusions for the unbounded edges, and finish with an argument-principle
count on the resulting keyhole boundary.  A reusable outer-cover engine needs
only the inner coefficient/orbit loader, these two excluded disks, and the
inner branch's parent hashes changed; it must not inherit an outer-branch
zero-free conclusion.
