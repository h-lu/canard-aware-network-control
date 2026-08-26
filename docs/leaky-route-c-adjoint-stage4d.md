# Stage 4D: Fourier cokernel to Route-C history measure

## Outcome

Stage 4D closes the bridge deliberately left open by Stage 4C. The exact
Fourier Grushin cokernel row now produces a continuous periodic advanced
adjoint, an atom-plus-density functional on the Route-C history space, and a
directed nonzero normalization \(f(q)\).

Three new statements are rigorous:

1. the correct Fourier transpose is bilinear mode reversal, not Hermitian
   conjugation;
2. the exact adjoint Fourier tail is summable in Wiener \(\ell^1\);
3. the Grushin border normalization gives
   \(3.05\times10^{-4}<|f(q)|<5.47\times10^{-4}\).

The physical event-corrected \(Y_{qq}\) is not yet enclosed in the same
directed representation. Therefore the correlated bound
\(\|Y_{qq}-qf(Y_{qq})\|<12\) remains open.

The executable source is
[leaky_route_c_adjoint_stage4d.py](../src/canard_control/leaky_route_c_adjoint_stage4d.py),
the generator is
[leaky_route_c_adjoint_stage4d.py](../experiments/leaky_route_c_adjoint_stage4d.py),
and the registered result is
[leaky_route_c_adjoint_stage4d.json](../experiments/results/leaky_route_c_adjoint_stage4d.json).

## 1. The exact Fourier reversal

Write the periodic forward Floquet factor as

\[
 u(T\theta)=e^{s\theta}p(\theta).
\]

For a periodic test function \(r\), the bilinear pairing is

\[
 \int_0^1r(\theta)^Tg(\theta)\,d\theta
 =\sum_k\widehat r_{-k}^T\widehat g_k.
\]

Thus, if \(a=E_-\) is the Grushin bottom row, the adjoint coefficients are

\[
 \widehat r_n=a_{-n}.
\]

There is no complex conjugation. For the physical unshifted-coefficient,
output-phase delayed operator,

\[
 e^{-(D+s)\alpha_j}M_{b_j},
\]

the bilinear transpose is

\[
 M_{b_j}e^{-s\alpha_j}S_{+\alpha_j}.
\]

With

\[
 z(T\theta)=e^{-s\theta}r(\theta),
\]

this is precisely

\[
 -z'(t)=A_0(t)^Tz(t)
 +\sum_jA_j(t+\tau_j)^Tz(t+\tau_j).
\]

The source includes a finite Fourier/physical-grid oracle. Both correct
identities agree to about \(10^{-18}\), while a Hermitian-conjugate mutation
is separated by more than \(5\times10^{-3}\). The proof is the coefficient
identity above; the binary oracle only protects its implementation.

## 2. Why the adjoint tail is summable

Stage 4C encloses the exact bottom row in the dual
\(\ell^\infty\) coefficient norm. That alone does not define a continuous
function. Stage 4D separately solves the tail row equation

\[
 a_TL_{TT}=-a_FL_{FT}
\]

in the matrix row-sum norm.

For the exact positive real root, every delay rotation has modulus at most
one. The exact current and two-delay coefficient Wiener norms, the period
ball, the fast and slow diagonal tail inverses, and both state couplings give

\[
 \|D_T^{-1}(L_{TT}-D_T)\|_\infty<0.105.
\]

Consequently \(L_{TT}^{-1}\) is bounded on \(\ell^\infty\). Since the
finite row is in \(\ell^1\), the row identity gives \(a_T\in\ell^1\), with

\[
 \|a_T\|_{1,\mathrm{split}}<0.012.
\]

Uniqueness of the tail solve identifies this summable row with the
Stage-4C dual cokernel row. Mode reversal therefore reconstructs a
continuous periodic \(r\). The recovery-column identity additionally makes
the recovery tail much smaller than the total tail, which is essential for
the nonzero atom below.

## 3. Border normalization equals the history pairing

Write the inverse bordered operator as

\[
 \mathcal L(s)^{-1}
 =\begin{pmatrix}E&E_+\\E_-&E_{-+}\end{pmatrix}.
\]

At the exact root \(s_*\),

\[
 R_+E_+=1,
 \qquad E_-R_-=1,
 \qquad
 E_{-+}'(s_*)=-E_-L'(s_*)E_+.
\]

The derivative of the delayed exponential contributes \(\tau_j\). Averaging
the invariant RFDE bilinear history pairing over one phase gives exactly

\[
 E_-L'(s_*)E_+=f(q).
\]

Hence \(|f(q)|=|E_{-+}'(s_*)|\) for the declared Grushin borders.

The parent Rouché proof bounds

\[
 E_{-+}(s)-a_*(s-s_c)
\]

on the full radius-\(0.1\) boundary by
\(1.208\times10^{-5}\). The refined root is within
\(1.71\times10^{-8}\) of \(s_c\). The maximum principle and Cauchy's
derivative estimate therefore give a derivative-remainder bound below
\(1.208\times10^{-4}\). Subtracting this from the reference slope yields

\[
 0.0003053<|f(q)|<0.00054693.
\]

This is the directed border normalization that Stage 4C lacked.

## 4. A nonzero continuous-history action shard

The summable Fourier tail gives directed current atoms and voltage-history
density total variation. On the recovery-only history

\[
 \phi_v(\theta)=0,
 \qquad \phi_w(0)=1,
\]

the entire density vanishes and

\[
 f(\phi)=z_w(0).
\]

The finite recovery modes, their Stage-4C row enclosure, and the sharpened
recovery-tail relation give a strictly positive lower bound for
\(|z_w(0)|\). After dividing by the upper bound for \(|f(q)|\), the
normalized recovery-only action also stays strictly away from zero. This is
a genuine continuous-history action shard, not a nodal pilot.

The full normalized measure norm is intentionally coarse. It is an
existence and action certificate, not the route used to bound the stable
output: applying its global norm would discard the needed cancellation.

## 5. Shared \(Y_{qq}\) pilot and remaining gate

The 120-, 180-, and 240-step source-bound pilots form

\[
 Y_{qq}-q\,f_N(Y_{qq})
\]

before taking any absolute value. At 240 steps,

\[
 \|Y_{qq}\|_\infty\approx30.59,
 \qquad |f_N(Y_{qq})|\approx26.19,
\]

while the correlated stable output is about \(7.2611\). The separate
triangle estimate is about \(56.78\), almost eight times larger. The
ordering of operations is therefore quantitatively decisive.

These three meshes are not interval evidence. The remaining strict gate is
to propagate the physical-time event-corrected \(Y_{qq}\) in the same
shared interval-polynomial history representation as \(q\) and the adjoint
measure, integrate that shared object, and subtract before taking the norm.
Until this closes, \(C_s^{uu}<12\), the local stable graph, the
\(1.7\times10^{-3}\) graph radius, separator crossing, and onset all remain
false.
