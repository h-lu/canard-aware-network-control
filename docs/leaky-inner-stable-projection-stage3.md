# Inner stable projection Stage 3: a lower bound and a scalar-majorant no-go

## 1. Strict result

Let

\[
Y=C([-\tau_{\max},0],\mathbb R)\times\mathbb R,
\qquad
\|(\phi,w)\|_Y=\max\{\|\phi\|_\infty,|w|\},
\]

and use the exact Route-C section

\[
\Sigma=\{(\phi,w):\phi(0)=0\}
\]

through the validated inner periodic orbit.  If \(P_s\) is the stable Riesz
projection of the phase-fixed return derivative on this section, then

\[
\boxed{\|P_s\|_{\mathcal L(\Sigma)}\ge2.}
\tag{1.1}
\]

This is a proved **lower** bound, not a projection-norm certificate suitable
for the Lyapunov--Perron upper estimate.  It has two exact consequences for
the scalar majorant disclosed in Stages 1--2.

1. At the selected strengthened rate and sequence weight, the old
   \(C_N=10\) row has left-hand side at least

   \[
   4606.5225670707\ldots>2500,
   \]

   so that row is impossible.
2. Moving the sequence weight arbitrarily close to one cannot rescue
   \(C_N=10\): the infimum of the same left-hand side is at least

   \[
   4032.2413521710\ldots>2500.
   \]

The corresponding necessary ceilings are \(C_N<5.4270873\ldots\) for the
selected weight and \(C_N<6.2000257\ldots\) after optimizing over all
admissible weights.  No actual return-map \(C_N\) has been validated.
Therefore (1.1) disproves the old design row, not the possibility of using
the current history norm with a sharper nonlinear estimate.

## 2. Refined positive exponent and the normalized kernel column

The parent Grushin theorem proves exactly one simple real characteristic
value in the disk of radius \(0.1\) about \(0.6983604129095\).  At each of the
two real points \(s_-=0.6983604100\) and \(s_+=0.6983604300\), Stage 3 uses the
complete finite-plus-tail preconditioner and encloses the scalar effective
Hamiltonian.  Its enclosure is strictly negative at \(s_-\) and strictly
positive at \(s_+\).  Thus

\[
0.6983604100<s_u<0.6983604300.
\tag{2.1}
\]

At the midpoint \(s_0=0.6983604200\), let \(b\) be the last column of the
binary64 finite bordered inverse.  Instead of multiplying its norm by the
worst full-operator defect, the proof evaluates the residual of this
particular column.  If \(q<1\) is the already directed complete Grushin
contraction and \(\eta\) is that column residual, then

\[
\|E_+(s_u)-b\|_{\ell^1_{\rm split}}
\le \frac{\eta}{1-q}
<2.968014\times10^{-8}.
\tag{2.2}
\]

This includes the exact orbit correction, the root interval, finite
roundoff, finite--tail and tail--finite couplings, and the infinite tail.
The finite SVD or bordered column alone is not promoted to an eigenhistory.

## 3. From the Floquet profile to the Route-C section

For a normalized Floquet profile \(y\), the physical eigenhistory at phase
zero is

\[
q_v(\theta)=e^{s_u\theta/T}y_v(\theta/T).
\]

The section vector is

\[
q^\Sigma=q-\dot x_0\frac{q_v(0)}{\dot v(0)}.
\tag{3.1}
\]

Stage 3 evaluates (3.1) with directed arithmetic at
\(\theta_*=-3.1724\).  The physical-time phase \(t/T\), the refined root
interval, the nested \(10^{-12}\) orbit ball, and the RFDE vector field are
all included.  The result is

\[
|q_v^\Sigma(\theta_*)|
\ge0.07755431589814\ldots,
\qquad
|q_w^\Sigma|
\le0.05624517801905\ldots,
\tag{3.2}
\]

with margin greater than \(0.02130913\).  Hence

\[
\|q^\Sigma\|_Y=\|q_v^\Sigma\|_\infty.
\tag{3.3}
\]

## 4. Why component dominance forces \(\|P_s\|\ge2\)

Let \(f\) be the adjoint covector for the nonneutral multiplier, restricted
to \(\Sigma\).  For a retarded equation with finitely many discrete delays,
the standard RFDE bilinear pairing writes \(f\) as current-state atoms plus
an absolutely continuous history density.  In this model the delay matrices
act only on voltage.  Thus the voltage-history part of \(f\) has no atom at
any \(\theta<0\).

The unstable and stable projections on the section are

\[
P_u z=q^\Sigma\frac{f(z)}{f(q^\Sigma)},
\qquad P_s=I-P_u.
\]

At a non-atomic history point,

\[
\bigl\|\delta_\theta-
q_v^\Sigma(\theta)f/f(q^\Sigma)\bigr\|
=1+|q_v^\Sigma(\theta)|
  \frac{\|f\|}{|f(q^\Sigma)|}.
\]

Taking a sequence of non-atomic points approaching the voltage supremum and
using

\[
|f(q^\Sigma)|\le\|f\|\,\|q^\Sigma\|_Y
\]

gives

\[
\|P_s\|\ge
1+\frac{\|q_v^\Sigma\|_\infty}{\|q^\Sigma\|_Y}=2,
\]

where the last equality is (3.3).  The nonneutral adjoint annihilates the
translation eigenvector, so restricting it after the Route-C event
projection does not change this eigencovector argument.

## 5. What an adapted splitting norm does and does not buy

The direct-sum norm

\[
\|x\|_{\rm split}=\|P_sx\|_Y+\|P_ux\|_Y
\tag{5.1}
\]

makes both projections isometric.  But it is not a free improvement.  From
an old-norm nonlinear estimate alone one obtains only

\[
\|x\|_Y\le\|x\|_{\rm split}
\le(\|P_s\|+\|P_u\|)\|x\|_Y,
\]

and therefore the black-box transfer

\[
C_N^{\rm split}
\le(\|P_s\|+\|P_u\|)C_N^Y.
\tag{5.2}
\]

The gain \(p_s=p_u=1\) can be lost through (5.2).  Weighted sum norms do not
improve this black-box factor: its minimum occurs at equal weights.

The mathematically useful replacement route is to use stable-history and
unstable-scalar coordinates and validate the six independent projected
blocks of \(D^2P\) directly (eight ordered blocks before using input
symmetry).  Such a calculation can exploit small block structure and
avoid the global norm-equivalence multiplier.  No such projected return
\(C^2\) certificate, stable power bound, projection upper bound, stable
graph, pulse separator, or onset theorem is asserted here.

## 6. Binary diagnostic, kept separate

A method-of-steps discretization on 41, 81, and 161 history nodes gives

\[
\|P_u\|\approx1.40142,
\qquad
\|P_s\|\approx2.40112,
\qquad
\|L_s\|\approx0.00412.
\]

These values explain why the lower bound (1.1) is plausible and suggest that
stable transient growth may be mild after projection.  They are binary64
diagnostics only.  In particular, they supply none of the missing upper
bounds.

Reproduce the source-bound artifact with

```bash
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
  /usr/bin/python3 experiments/leaky_inner_stable_projection_stage3.py

PYTHONPATH=src /usr/bin/python3 -m pytest -q \
  tests/test_leaky_inner_stable_projection_stage3.py
```
