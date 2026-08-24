# A finite Riesz reduction for the synchronous Floquet index

Status: **the infinite-dimensional reduction is proved; the stable index is
not yet proved.** The logarithmic Floquet problem on the closed right half
strip is reduced, with analytic characteristic multiplicity, to an analytic
\(258\times258\) Schur complement. Separate directed estimates exclude the
outer half-plane and a punctured complex neighborhood of the translation
root. The remaining calculation is one finite directed boundary winding.
The tracked binary64 winding is zero at two resolutions, but it is not
used as proof of attraction.

The executable reduction is
[fhn_synchronous_floquet_riesz_reduction.py](../src/canard_control/fhn_synchronous_floquet_riesz_reduction.py),
the driver is
[fhn_synchronous_floquet_riesz_reduction.py](../experiments/fhn_synchronous_floquet_riesz_reduction.py),
and the tracked record is
[fhn_synchronous_floquet_riesz_reduction.json](../experiments/results/fhn_synchronous_floquet_riesz_reduction.json).
Its SHA-256 digest is

~~~text
b68483ae12421195a485e6c9af950d8d101cf04497565cf079fcf57ba57793f6
~~~

It is bound to the parameter-box, Bloch, index-audit, and binary candidate
records with respective digests

~~~text
ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0
c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31
328a4207863279cd5136a159dbe1a7deecc50d1b3eb1be30b6fd34e66b2af024
7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28
~~~

## 1. The logarithmic Floquet family

Let \(b=(\kappa _1,\kappa _3)\) belong to the validated microscopic gain
box \(U\), and let \(X_b\) and \(T_b\) denote its synchronous periodic orbit
and period. A nonzero multiplier \(\lambda\) is represented by

\[
 \lambda=e^s,\qquad
 s=\sigma+i\varphi,\qquad
 -\pi\leq\varphi\leq\pi .
\tag{1.1}
\]

In the Fourier realization, the logarithmic Bloch operator is

\[
\begin{aligned}
 (\mathcal L_s y)_{v,k}
 &= (s+2\pi i k)y_{v,k}-T_b(g_b*y_v)_k+T_by_{w,k}\\
 &\quad-T_b\sum_{j=0}^1
 e^{-(s+2\pi i k)\tau_j/T_b}(H_b*y_v)_k,\\
 (\mathcal L_s y)_{w,k}
 &= (s+2\pi i k)y_{w,k}-T_b\varepsilon y_{v,k}.
\end{aligned}
\tag{1.2}
\]

For \(s=i\varphi\), this is exactly the family used by the proved
unit-circle certificate. The same Floquet periodicization and smoothing
argument gives the spectral-set correspondence

\[
 \ker\mathcal L_s\ne\{0\}
 \quad\Longleftrightarrow\quad
 e^s\text{ is a nonzero history-space multiplier}.
\tag{1.3}
\]

The already proved generalized-Floquet argument identifies the analytic
and monodromy algebraic multiplicities at the translation value \(s=0\).
No such multiplicity bridge for an arbitrary nonzero multiplier is
certified here. It is not needed for the intended zero-winding conclusion:
a zero determinant winding would show that there are no characteristic
values in the keyhole domain, and (1.3) then excludes unstable multipliers
as a set.

The parameter-box certificate gives the uniform exact-orbit bounds

\[
\begin{aligned}
 \|g_b\|_{\mathcal W}
 &\leq G_+
 =5.55445523580458007300165867908132815\ldots,\\
 \|H_b\|_{\mathcal W}
 &\leq H_+
 =0.45644184321168890970191183850255443\ldots,\\
 T_b&\leq T_+
 =16.5403878031809337427421269239857793\ldots .
\end{aligned}
\tag{1.4}
\]

These bounds hold for every \(b\in U\); they are not norms of the stored
Fourier polynomial alone.

## 2. Uniform inversion of the infinite tail

For this analytic tail step use the complex-modulus component Wiener norm

\[
 \|y\|_{\mathcal W_{\mathbb C}}
 =\sum_k\bigl(|y_{v,k}|+|y_{w,k}|\bigr).
\]

This is equivalent to the split real/imaginary norm used by the finite
Bloch accelerator, but the distinction matters here: in the modulus norm a
delay rotation has norm one and multiplication by
\((\sigma+i\omega)^{-1}\) has norm
\((\sigma^2+\omega^2)^{-1/2}\).  (In the split norm the latter norm would
instead be \((\sigma+|\omega|)/(\sigma^2+\omega^2)\).)
Let \(P\) retain the modes \(|k|\leq64\), and put \(Q=I-P\). The finite
space has complex dimension

\[
 2(2\cdot64+1)=258.
\tag{2.1}
\]

Write \(D_sy_k=(s+2\pi i k)y_k\). If \(\sigma\geq0\),
\(|\varphi|\leq\pi\), and \(|k|\geq65\), then

\[
 |s+2\pi i k|
 \geq |2\pi k+\varphi|
 \geq129\pi
 =405.265452313083327761680996443055872\ldots .
\tag{2.2}
\]

Since \(|e^{-s\tau_j/T_b}|\leq1\) in the right half-plane, the lower-order
part of (1.2) has complex-modulus norm bound

\[
 B_+
 :=\max\{G_++2H_++\varepsilon,1\}
 \leq6.667338922227958\ldots .
\tag{2.3}
\]

Indeed, the unrotated current convolution contributes \(G_+\), each of
the two delayed output-mode rotations has modulus norm at most \(H_+\),
the voltage input column also contains
\(\varepsilon\), and the recovery input column contributes \(1\).

Consequently,

\[
 \left\|
 I-D_{Q,s}^{-1}Q\mathcal L_sQ
 \right\|
 \leq
 \frac{T_+B_+}{129\pi}
 \leq
 0.272118856318640627662391123614772
 <1.
\tag{2.4}
\]

This estimate is uniform in \(b\in U\) and throughout the closed half
strip. Thus \(Q\mathcal L_sQ\) is invertible there by a Neumann series and
depends analytically on \(s\).

Define

\[
 \mathscr S_b(s)
 =P\mathcal L_sP
 -P\mathcal L_sQ
 (Q\mathcal L_sQ)^{-1}
 Q\mathcal L_sP.
\tag{2.5}
\]

> **Theorem 2.1 (right-half-strip Riesz reduction).** Uniformly for
> \(b\in U\), the characteristic values of \(\mathcal L_s\) in
> \(\{\Re s\geq0,\ |\Im s|\leq\pi\}\) are exactly the zeros of
> \(\det\mathscr S_b(s)\). Their analytic multiplicities agree. The
> determinant is the ordinary determinant of an analytic
> \(258\times258\) matrix.

**Proof.** Regard \(\mathcal L_s\) as the closed analytic pencil from the
one-derivative Wiener domain to the unweighted Wiener range, split in both
spaces by \(P+Q=I\). Estimate (2.4) gives an inverse

\[
 D_b(s)^{-1}:Q\mathcal W^0\longrightarrow Q\mathcal W^1,
 \qquad D_b(s)=Q\mathcal L_sQ.
\tag{2.6}
\]

The Neumann series is analytic in \(s\). Its strict margin also persists in
a complex neighborhood of each point of the closed half strip. If
\(A=P\mathcal L_sP\), \(B=P\mathcal L_sQ\), and
\(C=Q\mathcal L_sP\), then the bounded analytic equivalence

\[
 \begin{pmatrix}I&-BD_b(s)^{-1}\\0&I\end{pmatrix}
 \begin{pmatrix}A&B\\C&D_b(s)\end{pmatrix}
 \begin{pmatrix}I&0\\-D_b(s)^{-1}C&I\end{pmatrix}
 =\begin{pmatrix}\mathscr S_b(s)&0\\0&D_b(s)\end{pmatrix}
\tag{2.7}
\]

holds between those domain and range splittings. Analytic equivalence
preserves characteristic values and their partial multiplicities. Since
\(\mathscr S_b(s)\) acts on the finite range of \(P\), its characteristic
values are precisely the zeros of its determinant, with their orders.
\(\square\)

This theorem removes the infinite-history tail from the missing index
calculation. It does not calculate the finite determinant winding.

## 3. Outer exclusion

For every Fourier mode and every \(\Re s=\sigma\geq128\),

\[
 |s+2\pi i k|\geq\sigma .
\tag{3.1}
\]

The same lower-order estimate gives

\[
 \|I-D_s^{-1}\mathcal L_s\|
 \leq\frac{T_+B_+}{128}
 \leq
 0.861565401475725211547698309141912
 <1.
\tag{3.2}
\]

Hence \(\mathcal L_s\) has no characteristic values with
\(\Re s\geq128\). The right-half-strip count is confined to a compact set.

## 4. A complex punctured neighborhood of the translation root

The local estimate in the unit-circle proof extends to complex \(s\) in
the right half-plane. We record the argument because this extension is a
claim-bearing seam.

Let \(p=X_b'\), let \(b_T\) be the exact moving-delay period column, and set

\[
 \mathcal L_s=\mathcal L_0+E_s.
\tag{4.1}
\]

The moving-delay identity is

\[
 E_0'p=T_bb_T .
\tag{4.2}
\]

For every \(\alpha\geq0\) and every \(s\) with \(\Re s\geq0\), the integral
forms of the first and second Taylor remainders give

\[
\begin{aligned}
 e^{-\alpha s}-1
 &=-\alpha s\int_0^1e^{-t\alpha s}\,dt,\\
 e^{-\alpha s}-1+\alpha s
 &=\alpha^2s^2\int_0^1(1-t)e^{-t\alpha s}\,dt .
\end{aligned}
\tag{4.3}
\]

Because \(|e^{-t\alpha s}|\leq1\), it follows that

\[
 |e^{-\alpha s}-1|\leq\alpha|s|,
 \qquad
 |e^{-\alpha s}-1+\alpha s|
 \leq\frac{\alpha^2|s|^2}{2}.
\tag{4.4}
\]

These inequalities hold uniformly over the exact orbit ball and gain box.
In the complexified real Wiener norm, the stored bounds imply

\[
 \|E_s\|\leq c_{1,U}|s|,
 \qquad
 \|(E_s-sE_0')p\|\leq c_{2,U}|s|^2,
\tag{4.5}
\]

where

\[
\begin{aligned}
 D_U&\leq23.3856903454031773371\ldots,\\
 c_{1,U}&\leq19.3714298055394719997\ldots,\\
 c_{2,U}&\leq232.614166566187522111\ldots,\\
 T_b&\geq T_-
 =16.5403877931809337427\ldots .
\end{aligned}
\tag{4.6}
\]

Here \(D_U\) is the uniform inverse norm of

\[
 \mathcal B_b(z,\eta)
 =(\mathcal L_0z-b_T\eta,\ell(z)).
\tag{4.7}
\]

Suppose \(\mathcal L_sy=0\), decompose \(y=z+cp\) with \(\ell(z)=0\), and
use (4.2). Then

\[
 \mathcal B_b(z,-T_bcs)
 =\bigl(-E_sz-c(E_s-sE_0')p,0\bigr).
\tag{4.8}
\]

Applying the inverse bound and (4.5) yields

\[
 \|z\|+T_b|c||s|
 \leq D_Uc_{1,U}|s|\,\|z\|
      +D_Uc_{2,U}|s|^2|c|.
\tag{4.9}
\]

Define

\[
 \delta_0
 :=\frac12\min\left\{
 \frac1{D_Uc_{1,U}},
 \frac{T_-}{D_Uc_{2,U}},
 \pi
 \right\}.
\tag{4.10}
\]

Its directed lower bound is

\[
 \delta_0
 \geq
 0.00110371801789578632406620967700529548\ldots .
\tag{4.11}
\]

For \(0<|s|\leq\delta_0\), the two coefficients on the right of (4.9)
are at most \(1/2\) after the second term is written as

\[
 \frac{D_Uc_{2,U}|s|}{T_b}\,
 \bigl(T_b|c||s|\bigr).
\tag{4.12}
\]

Thus the right side of (4.9) is at most half its left side, a contradiction
unless \(z=0\) and \(c=0\). Uniformly for \(b\in U\),

\[
 \ker\mathcal L_s=\{0\}
 \quad\text{if}\quad
 \Re s\geq0,\qquad0<|s|\leq\delta_0 .
\tag{4.13}
\]

The tracked keyhole uses

\[
 \delta_*=\delta_0/2
 =0.000551859008947893162033104838502647740\ldots .
\tag{4.14}
\]

Only the simple translation characteristic value at \(s=0\) is removed.

## 5. The remaining finite winding

Let \(\Gamma\) be the positively oriented boundary of

\[
 \{0\leq\Re s\leq128,\ |\Im s|\leq\pi\}
 \setminus
 \{\Re s\geq0,\ |s|<\delta_*\}.
\tag{5.1}
\]

The existing Bloch theorem covers the imaginary-axis parts of \(\Gamma\),
(4.13) covers the indentation, and (3.2) covers the right boundary and
all points beyond it. Theorem 2.1 reduces the proof of absence of unstable
multipliers to the following zero-index task: prove that the
argument-principle winding of
\(\det\mathscr S_{b_0}\) is zero, after the seam and the full boundary have
been directed-certified as nonzero. That conclusion uses the spectral-set
bridge (1.3); it does not claim a multiplicity-preserving monodromy count.

The executable diagnostic replaces the exact Schur complement by the
cutoff-64 finite block built from the stored center Fourier polynomial. The
quadratic coefficient sequences are formed by full discrete convolution
of the polynomial's modes and retain support through modes \(\pm128\);
they are not obtained by squaring on the 129-node grid, which would alias
those modes. The diagnostic uses the **phase** of the complex sign returned
by numpy.linalg.slogdet; it does not use the returned log modulus.

| subdivisions per contour piece | contour points | finite-block winding | largest adjacent phase increment |
|---:|---:|---:|---:|
| 24 | 145 | \(0\) | \(0.4190931237\) |
| 48 | 289 | \(0\) | \(0.2208293599\) |

This is strong evidence for

\[
 \nu(0.2,0.25)=0.
\tag{5.2}
\]

It is not a proof. The determinant phases use binary64 LU factorizations,
and the record does not enclose a zero-free boundary homotopy from the exact
Schur complement (2.5) to the candidate finite block.

The minimal remaining certificate has two coupled clauses:

1. on every cell of \(\Gamma\), validate an invertible homotopy from
   \(\mathscr S_{b_0}(s)\) to the cutoff-64 candidate finite block; and
2. enclose the finite determinant phase increments with directed complex
   arithmetic so that their sum lies in an interval containing exactly the
   integer winding zero.

No new infinite-dimensional tail theorem, outer spectral bound, gain-box
scan, treatment of the translation root, or general
analytic-to-monodromy multiplicity theorem is required for this
zero-index conclusion.

## 6. Claim boundary

The following statements are proved:

- uniform tail-block invertibility on the complete logarithmic right half
  strip;
- an analytic \(258\times258\) Schur reduction preserving analytic
  characteristic multiplicity;
- absence of characteristic values for \(\Re s\geq128\); and
- exclusion of the punctured complex right half-disk around the simple
  translation value.

The following remain unproved:

- the directed winding of the exact finite Schur complement;
- \(\nu(0.2,0.25)=0\);
- equality, at arbitrary nontranslation values, between analytic
  characteristic multiplicity and history-monodromy algebraic
  multiplicity;
- synchronous orbital attraction; and
- full-network orbital attraction.

Once the finite directed winding is zero, the previously proved constancy of
\(\nu(b)\) on the connected gain box transports that center count throughout
\(U\). Combined with the transverse Halanay theorem, this would close local
full-network orbital attraction for the fixed dual-scaffold rank-one
topology. It would still not prove a global basin, a general-graph attraction
theorem, or hardware-robust pulse capture.

Reproduce and test the record with

~~~bash
PYTHONPATH=build/testdeps:src OPENBLAS_NUM_THREADS=1 /usr/bin/python3 \
  experiments/fhn_synchronous_floquet_riesz_reduction.py

PYTHONPATH=build/testdeps:src OPENBLAS_NUM_THREADS=1 /usr/bin/python3 \
  -m pytest -q tests/test_fhn_synchronous_floquet_riesz_reduction.py
~~~
