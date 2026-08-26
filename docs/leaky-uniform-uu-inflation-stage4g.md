# Stage 4G: uniform \(C_s^{uu}\) inflation audit

## Outcome

Stage 4E proves, at the periodic base orbit,

\[
 C_{s,\mathrm{base}}^{uu}
 \le 7.905649078257424392625488164113\ldots <12.
\]

Stage 4G asks whether this base value can be inflated over the proposed
radius-\(0.0017\) split ball. The exact available increment is

\[
 12-7.905649078257424392625488164113\ldots
 =4.094350921742575607374511835886\ldots .
\]

Consequently a sufficient Lipschitz gate is

\[
 L_{uu}<
 \frac{12-C_{s,\mathrm{base}}^{uu}}{0.0017}
 =2408.44171867210329845559519758\ldots .
\]

The direct complete-history scalar \(P\)-majorant does **not** supply this
gate. Its current cells all close as directed differential inequalities, but
the resulting tube first ceases to certify containment in the validated
radius-\(0.01\) local return domain on cell 581. At that cell the voltage
coordinate upper bound is about \(0.0100594\). By one period the scalar
majorant has \(P\)-radius about \(10.30023\), corresponding to a voltage
coordinate upper bound about \(2.15131\).

These are upper bounds, not observations that an exact trajectory leaves the
local neighborhood. Their size proves only that this scalar proof route is
too lossy. Stage 4G therefore freezes the first missing ingress and keeps the
uniform \(C_s^{uu}<12\), all six Hessian blocks, stable graph, separator, and
pulse-onset flags false.

The executable source is
[leaky_uniform_uu_inflation_stage4g.py](../src/canard_control/leaky_uniform_uu_inflation_stage4g.py),
the generator is
[leaky_uniform_uu_inflation_stage4g.py](../experiments/leaky_uniform_uu_inflation_stage4g.py),
and the registered result is
[leaky_uniform_uu_inflation_stage4g.json](../experiments/results/leaky_uniform_uu_inflation_stage4g.json).

## 1. What must be varied

For a base history \(x\), write

\[
 C_s^{uu}(x)=\frac{\|G(x)\|_Y}{\|q(x)\|_Y^2},\qquad
 G(x)=Y_{qq}(x)-q(x)\alpha(x),
\]

where

\[
 \alpha(x)=\frac{f_x(Y_{qq}(x))}{f_x(q(x))}.
\]

The event-corrected second history is evaluated for every retained-history
coordinate, not only at the current endpoint:

\[
 Y_{qq}=V_{qq}+2\dot U_q\tau_q+\ddot X\tau_q^2
          +\dot X\tau_{qq}.
\]

For a base-state direction \(h\), the exact first-difference identities are

\[
 D_xG[h]=D_xY_{qq}[h]-D_xq[h]\,\alpha-q\,D_x\alpha[h]
\]

and

\[
 \begin{aligned}
 D_x\alpha[h]
 &=\frac{(D_xf[h])(Y_{qq})+f(D_xY_{qq}[h])}{f(q)}\\
 &\quad-
 \frac{f(Y_{qq})\big((D_xf[h])(q)+f(D_xq[h])\big)}{f(q)^2}.
 \end{aligned}
\]

Thus a genuine uniform inflation requires all of the following on the same
complete-history tube:

1. a base-state mean-flow bound for \(X_x-X_0\);
2. correlated bounds for \(D_xU_q[h]\) and \(D_xV_{qq}[h]\), equivalently the
   relevant third variation \(W_{hqq}\), including the variation of \(q\);
3. physical-time bounds for \(D_x\tau_q[h]\) and \(D_x\tau_{qq}[h]\), with a
   uniform positive event-speed denominator;
4. the moving right history \(D_xq[h]\), the moving atom-plus-density
   covector \(D_xf[h]\), and a nonzero lower bound for \(f_x(q(x))\);
5. the variation of the final normalization \(\|q(x)\|_Y^{-2}\).

The correlated expression must be formed before either a history norm or a
total-variation norm is taken. Separate numerator/denominator triangle
bounds would discard the same cancellation that Stage 4E needed at the base
orbit. None of the five Stage-4B design targets is used as a bound here.

## 2. Directed complete-history mean-flow attempt

Let \(X_0\) be the exact validated periodic orbit and \(X\) a solution whose
initial history differs by at most \(0.0017\) in the split norm. Since the
split projections sum to the identity,

\[
 \|X_0-X\|_Y\le \|X_0-X\|_{\mathrm{split}}.
\]

For \(e=X-X_0\), the cubic RFDE difference has the exact segment-mean form

\[
 \dot e=A_{\mathrm{bar}}(t,e)e
 +B_{0,\mathrm{bar}}(t,e_{\tau_0})e_v(t-\tau_0)
 +B_{1,\mathrm{bar}}(t,e_{\tau_1})e_v(t-\tau_1).
\]

Stage 4G uses the Stage-4E physical grid \(h=\tau_0/512\), for which

\[
 \tau_0=512h,\qquad \tau_1=640h.
\]

On every cell, the exact orbit voltage is enclosed by 192-bit outward MPFR
Taylor--Bernstein ranges plus the validated Fourier coefficient error and
analytic tail. The current segment-mean coefficient is evaluated on this
range enlarged by the unknown current-cell \(P\)-radius. The two delayed
segment-mean coefficients use the exact translated orbit ranges enlarged by
the already validated source-cell voltage radii. A fixed-point loop then
proves the current-cell maximum radius satisfies its own Gronwall inequality.

The initial current-state box has directed \(P\)-radius

\[
 R_P(0)\le 0.0252070506009727\ldots,
\]

and the voltage coordinate obeys

\[
 |e_v|\le 0.2088606946822271\ldots R_P.
\]

Every one of the 1042 current-cell inequalities closes. Nevertheless the
upper tube becomes too large to invoke the local return/event inputs. This
is the first failure in the dependency order, so Stage 4G does not assign
numerical values to the third-variation, event, or moving-projection
Lipschitz pieces.

## 3. Minimal sharper replacement

The scalar logarithmic norm takes an absolute envelope before the
phase-dependent current flow has cancelled its expanding and contracting
pieces. The minimal replacement is a signed propagator calculation:

1. enclose the fundamental matrix of the two-dimensional current ODE along
   the exact base orbit;
2. insert each delayed source by a Volterra expansion;
3. form the stable input as
   \(U(t)P_s=U(t)-U(t)qf/f(q)\) with shared \(q,f\) symbols;
4. sum signed atoms and densities before taking total variation.

The one-period delay-word algebra is finite and particularly small. The
physical constants satisfy

\[
 2\tau_0<T<\tau_0+\tau_1<3\tau_0.
\]

Hence only the empty word, the one-delay words \((\tau_0)\) and
\((\tau_1)\), and the depth-two word \((\tau_0,\tau_0)\) can occur. All other
depth-two words and every depth-three word vanish on \([0,T]\). A directed
certificate for these signed kernels is the exact new parent needed before
the Stage-4G Lipschitz audit can continue.

## 4. Exact scope

Proved by Stage 4G:

- the exact inflation budget and the sufficient Lipschitz threshold;
- the complete error decomposition, including event and moving \(q/f\)
  normalization terms;
- completion and self-closure of the 1042-cell scalar mean-flow majorant;
- strict failure of that majorant to certify the local returned-history ball;
- the finite signed delay-word structure required by the sharper route.

Not proved:

- a validated \(L_{uu}<2408.4417\ldots\);
- uniform \(C_s^{uu}<12\) on the radius-\(0.0017\) split ball;
- the other five Hessian blocks, stable power, or split return tube;
- a quantitative local stable graph, separator crossing, or physical onset.

## 5. Replay

Generate the certificate:

    OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
      /usr/bin/python3 experiments/leaky_uniform_uu_inflation_stage4g.py

Static source/parent validation:

    OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
      /usr/bin/python3 experiments/leaky_uniform_uu_inflation_stage4g.py --check

Full independent recomputation and digest comparison:

    OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
      /usr/bin/python3 experiments/leaky_uniform_uu_inflation_stage4g.py --replay
