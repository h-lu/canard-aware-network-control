# A directed zero-free cover for the synchronous Floquet right half-plane

Status: **proved for the validated microscopic gain box and the fixed
rank-one two-module topology.** A finite directed cover proves that the
exact synchronous logarithmic Floquet operator has no nontranslation
characteristic value in the closed right half-plane. Thus the synchronous
nontranslation unstable index is $\nu(b)=0$. The standard RFDE principle of
linearized orbital stability gives local synchronous orbital attraction;
the existing transverse Halanay theorem then gives local full-network
orbital attraction for every fixed finite pair of positive module sizes in
the declared fixed rank-one topology; no module-size-uniform nonlinear basin
is asserted.

This is not a general-network canard theorem, a general-topology
synchronization theorem, or a biological pulse-capture theorem.

The executable proof is
[fhn_synchronous_floquet_right_half_cover.py](../src/canard_control/fhn_synchronous_floquet_right_half_cover.py),
the driver is
[fhn_synchronous_floquet_right_half_cover.py](../experiments/fhn_synchronous_floquet_right_half_cover.py),
and the proof object is
[fhn_synchronous_floquet_right_half_cover.json](../experiments/results/fhn_synchronous_floquet_right_half_cover.json).
Its SHA-256 digest is

~~~text
6795e6f19f31ffb6bfcf9abd24efb1c5dde4dccf54d896d01298b3e8f9a0d1c3
~~~

## 1. Source-bound pencil and norms

For every gain parameter $b$ in the directed $D^1$ continuation box, let
$X_b$ and $T_b$ be the exact real periodic orbit and period. The logarithmic
Floquet pencil is

\[
\begin{aligned}
 (\mathcal L_{b,s}y)_{v,k}
 &= (s+2\pi i k)y_{v,k}-T_b(g_b*y_v)_k+T_by_{w,k}\\
 &\quad-T_b\sum_{j=0}^1
 e^{-(s+2\pi i k)\tau_j/T_b}(H_b*y_v)_k,\\
 (\mathcal L_{b,s}y)_{w,k}
 &= (s+2\pi i k)y_{w,k}-T_b\varepsilon y_{v,k}.
\end{aligned}
\tag{1.1}
\]

The proof is hash-bound to these records:

~~~text
parameter box  ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0
Bloch theorem  c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31
Riesz theorem  b68483ae12421195a485e6c9af950d8d101cf04497565cf079fcf57ba57793f6
transverse     ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb
candidate      7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28
~~~

The repaired Riesz theorem uses the complex-modulus Wiener norm:

\[
 B_+\le 6.66733892222795790351,\qquad
 q_{\rm tail}\le0.27211885631864062767,\qquad
 q_{\Re s\ge128}\le0.86156540147572521155.
\tag{1.2}
\]

The present computation instead uses the split component norm

\[
 \|y\|_{\square}
 =\sum_k\bigl(
 |\Re y_{v,k}|+|\Im y_{v,k}|+
 |\Re y_{w,k}|+|\Im y_{w,k}|
 \bigr).
\tag{1.3}
\]

These equivalent norms can support separate invertibility arguments, but
they are not mixed inside one numerical inequality.  The directed source
coefficient bounds were formed in the split norm, which dominates the
complex-modulus norm coefficientwise; hence they are also valid inputs for
the separate Riesz modulus-norm estimate.

## 2. Exact keyhole geometry

The local bordered theorem excludes

\[
 0<|s|\le\delta_0,\qquad \Re s\ge0,\qquad
 \delta_0
 \ge0.00110371801789578632406620967700529547\ldots .
\tag{2.1}
\]

Set

\[
 \rho=0.00055185900894789316203310483850264773\ldots
      \approx\frac{\delta_0^{\rm recorded}}2 .
\tag{2.2}
\]

The half-square

\[
 0\le\Re s\le\rho,\qquad |\Im s|\le\rho
\tag{2.3}
\]

lies strictly in that disk because $\sqrt2\rho<\delta_0$. It remains to
cover

\[
 [\rho,128]\times[0,\pi]
 \quad\text{and}\quad
 [0,\rho]\times[\rho,\pi].
\tag{2.4}
\]

Since the exact branch is real, mode-reversal conjugation satisfies

\[
 (Cy)_k=\overline{y_{-k}},\qquad
 C\mathcal L_{b,s}C^{-1}=\mathcal L_{b,\bar s}.
\tag{2.5}
\]

The earlier Bloch proof audits this conjugacy on the imaginary axis; the
additional scalar $\Re s$ is unchanged. Hence the negative half-strip
follows from the positive one. The analytic estimate (1.2) covers
$\Re s\ge128$.

## 3. Directed four-block rectangle estimate

Let $P$ retain $|k|\le64$, let $Q=I-P$, and let
$s_c=\sigma_c+i\varphi_c$ be the checked binary64 centre of one decimal
rectangle. If its directed coordinate radii are
$h_\sigma,h_\varphi$, put

\[
 h=h_\sigma+h_\varphi.
\tag{3.1}
\]

This sum is required because multiplication by
$d=d_\sigma+i d_\varphi$ has induced split norm
$|d_\sigma|+|d_\varphi|$. Use

\[
 \mathcal A_c=\operatorname{diag}(R_c,D_{Q,c}^{-1}),
 \qquad
 R_c=(P\mathcal L_{\bar X,s_c}P)^{-1}.
\tag{3.2}
\]

Here $\bar X$ is the stored 129-node Fourier polynomial and
$D_{Q,c}y_k=(s_c+2\pi i k)y_k$. In the split norm,

\[
 \|(\sigma_c+i\omega)^{-1}\|_{1,\mathbb R^2}
 =\frac{\sigma_c+|\omega|}{\sigma_c^2+\omega^2}.
\tag{3.3}
\]

The Euclidean reciprocal would be false here. For
$0\le\sigma_c\le128$ and tail frequencies, (3.3) decreases with
$|\omega|$; $k=\pm65$ give the infinite-tail supremum.

The unaliased candidate retains support through $\pm128$. Every binary
FFT/convolution coefficient and delay-rotation basis is compared directly
with an MPFR interval enclosure. Matrix products use four real GEMMs,

\[
 \Re(AB)=A_rB_r-A_iB_i,\qquad
 \Im(AB)=A_rB_i+A_iB_r,
\tag{3.4}
\]

with a conservative $\gamma_{2n+5}$ error and gradual-underflow allowance.
The binary rounding environment is checked before and after every GEMM.
No complex-BLAS or transcendental-library accuracy promise is assumed.

Let the four block bounds of
$I-\mathcal A_c\mathcal L_{b,s}$ be
$Z_{PP},Z_{PQ},Z_{QP},Z_{QQ}$. They have the form

\[
\begin{aligned}
 Z_{PP}&=\eta+h\mu+h^2\nu_P+\|R_c\|\Gamma_{\rm full},\\
 Z_{PQ}&=p_0+hp_1+h^2\nu_P+\|R_c\|\Gamma_{\rm conv},\\
 Z_{QP}&=q_0+hq_1+h^2\nu_Q+\Gamma_{QP},\\
 Z_{QQ}&=d_c\bigl(h+T_+B_{\square,+}\bigr).
\end{aligned}
\tag{3.5}
\]

Here $\eta$ contains the audited inverse defect and exact-box matrix
distance. The first derivative products are $\mu,p_1,q_1$, while

\[
 \nu_P=\|R_c\|C_2,\qquad \nu_Q=d_cC_2,\qquad
 C_2=\frac{T\sqrt2\|H\|}{2}
 \sum_{j=0}^1(\tau_j/T)^2.
\tag{3.6}
\]

The complex Taylor segment stays in $\Re s\ge0$, so

\[
 |e^{-\alpha(s_c+d)}-e^{-\alpha s_c}
   +\alpha d e^{-\alpha s_c}|
 \le\frac{\alpha^2|d|^2}{2}.
\tag{3.7}
\]

The three $\Gamma$ terms include the exact $D^1$ orbit radius, gain-box
coefficient variations, and moving-period correction for the fixed delays.
The tail period term uses

\[
 \|D_{Q,c}^{-1}(s+2\pi i k)\|_\square
 \le1+d_ch.
\tag{3.8}
\]

The two input-column bounds are

\[
 Q_P=Z_{PP}+Z_{QP},\qquad
 Q_Q=Z_{PQ}+Z_{QQ},\qquad
 q=\max\{Q_P,Q_Q\}.
\tag{3.9}
\]

Here $\mathcal A_c:\mathcal W^0\to\mathcal W^1$ is a block-diagonal
isomorphism. Every accepted leaf satisfies $q\le0.995<1$. Therefore

\[
 I-t(I-\mathcal A_c\mathcal L_{b,s}),\qquad0\le t\le1,
\tag{3.10}
\]

is invertible throughout that rectangle. This is a Neumann homotopy from
the identity to the left-preconditioned full operator
$\mathcal A_c\mathcal L_{b,s}$; invertibility of the preconditioner then
gives invertibility of $\mathcal L_{b,s}$. It is neither a homotopy directly
from $\mathcal L_{b,s}$ to the identity nor the previously proposed
exact-Schur-to-candidate finite-block homotopy.

## 4. Cover completeness and winding

Both rectangles in (2.4) are split dyadically. The proof object stores every
leaf path and both input-column bounds. For each root, a prefix-trie audit
requires every internal node to have exactly the two children "x0,x1" or
"y0,y1"; an exact rational Kraft sum must equal one. Thus no area or seam
can disappear.

~~~text
processed cells:          64090
accepted leaves:          32046
pending cells:            0
maximum accepted q:       0.9949969734691212177432801648052352667472012755814612224
minimum margin 1-q:       0.0050030265308787822567198351947647332527987244185387776
maximum dyadic depth:     42
leaf-partition SHA-256:   9ee81b724449c8ef8b465d332b2fb9a78843870dca59e77b440aa459203ea7b2
~~~

Together with the local disk, conjugacy, and outer exclusion, the cover
proves

\[
 \ker\mathcal L_{b,s}=\{0\}
 \quad\text{for}\quad
 \Re s\ge0,\ -\pi\le\Im s\le\pi,\ s\ne0.
\tag{4.1}
\]

The exact 258-dimensional Schur determinant is nonzero throughout the
keyhole domain and boundary. Its argument-principle winding is therefore

\[
 [\operatorname{wind},\operatorname{wind}]=[0,0].
\tag{4.2}
\]

This integer is deduced exactly from zero-freedom; it is not an
outward-rounded determinant-phase computation and does not use the old
binary phase table.

## 5. Unstable index and attraction

The generalized-Floquet spectral-set correspondence gives

\[
 \ker\mathcal L_{b,s}\ne\{0\}
 \quad\Longleftrightarrow\quad
 e^s\text{ is a nonzero history-monodromy multiplier}.
\tag{5.1}
\]

Thus (4.1) excludes every nontranslation multiplier of modulus at least one.
No general analytic-to-monodromy multiplicity bridge is needed for this
absence statement. The translation theorem proves that the unit multiplier
is algebraically simple. Hence the synchronous nontranslation unstable
index is $\nu(b)=0$.

The discrete-delay RFDE vector field is polynomial, hence $C^\infty$, and
one-period smoothing makes monodromy compact.  The unit multiplier is
algebraically simple and every complementary multiplier lies strictly
inside the unit disk.  Therefore the synchronized stable manifold in
[Hale--Verduyn Lunel, Chapter 10, Section 10.3, Theorem 3.3,
pp. 321--324](https://doi.org/10.1007/978-1-4612-4342-7) has codimension
zero.  Equivalently, an open neighborhood converges to a phase translate
of the periodic orbit.  This gives local nonlinear orbital attraction,
with asymptotic phase, for each parameter in the box.  No parameter-uniform
nonlinear basin size is asserted.

The independent Halanay record proves size-uniform exponential decay of
every transverse variational mode for the fixed rank-one two-module
topology with voltage scaffold $3$ and recovery scaffold $2$. Exact modal
decomposition and the synchronous unstable-index result leave only the simple phase
multiplier in the full network. The same RFDE theorem gives local
full-network orbital attraction, with asymptotic phase, for each fixed pair
of positive finite module sizes in that fixed topology.  No basin uniform
in the two module sizes is asserted.

## 6. Claim boundary

Now proved:

- exact right-half zero-freedom and Schur winding zero on the microscopic
  gain box;
- synchronous nontranslation unstable index $\nu(b)=0$ and local nonlinear
  orbital attraction; and
- local full-network nonlinear orbital attraction for every fixed finite pair
  of positive module sizes in the fixed rank-one two-module topology.

Still not proved:

- arbitrary balanced or general network topology;
- a general network canard theorem;
- global attraction or an explicit nonlinear basin;
- a same-model path from pulse onset into this local periodic-orbit basin;
- autonomous biological pulse capture, robustness, or hardware safety; or
- a general arbitrary-multiplier analytic-to-monodromy multiplicity theorem.
