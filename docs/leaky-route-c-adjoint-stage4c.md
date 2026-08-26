# Stage 4C: Route-C left adjoint and correlated deflation

## Outcome

Stage 4C closes two exact structural gates and one Fourier-space numerical
gate:

1. the nonneutral unstable multiplier is algebraically simple, so its left
   adjoint functional satisfies \(f(q)\neq0\);
2. the RFDE adjoint functional has the required current-state atoms plus
   voltage-history density, and it annihilates the neutral flow tangent;
3. a complete cutoff-64 plus infinite-tail Grushin argument encloses a
   nonzero left cokernel row of the periodic characteristic pencil.

It does **not** yet identify that Fourier cokernel row with a numerically
normalized continuous-history adjoint measure. The action on the physical
return history \(Y_{qq}\), and therefore the target
\(C_s^{uu}<12\), remain open theorem gates.

The executable source is
[leaky_route_c_adjoint_stage4c.py](../src/canard_control/leaky_route_c_adjoint_stage4c.py),
the generator is
[leaky_route_c_adjoint_stage4c.py](../experiments/leaky_route_c_adjoint_stage4c.py),
and the registered result is
[leaky_route_c_adjoint_stage4c.json](../experiments/results/leaky_route_c_adjoint_stage4c.json).

## 1. Why \(f(q)\neq0\) is now rigorous

Let \(M\) be the compact history monodromy, let
\(Mq=\lambda q\), and let \(fM=\lambda f\). The validated unstable
restriction is one dimensional and the isolated characteristic root has
analytic algebraic multiplicity one. Thus \(\lambda\) is algebraically
simple.

For a simple compact eigenvalue,

\[
 \operatorname{Range}(M-\lambda I)=\ker f.
\]

If \(f(q)=0\), then \(q=(M-\lambda I)y\) for some \(y\). Hence \(y\)
is a generalized eigenvector, contradicting algebraic simplicity. Therefore

\[
 \boxed{f(q)\neq0}.
\]

This is a qualitative theorem. It permits the normalization \(f(q)=1\),
but does not by itself give a directed numerical representation of that
normalized functional.

## 2. The RFDE atom-plus-density identity

For

\[
 x'(t)=A_0(t)x(t)+\sum_jA_j(t)x(t-\tau_j),
\]

the advanced adjoint satisfies

\[
 -z'(t)=A_0(t)^Tz(t)+\sum_jA_j(t+\tau_j)^Tz(t+\tau_j),
 \qquad z(t+T)=\lambda^{-1}z(t).
\]

Its action on a history \(\phi\) at time \(t\) is

\[
 f_t(\phi)=z(t)^T\phi(0)
 +\sum_j\int_{-\tau_j}^0
 z(t+\theta+\tau_j)^TA_j(t+\theta+\tau_j)\phi(\theta)\,d\theta.
\]

Differentiating this expression along a forward solution cancels the two
delay-boundary terms and gives \(d f_t(x_t)/dt=0\). In this model, the atoms
are \(z_v(t)\) and \(z_w(t)\). For delay \(j\), the only density is in the
voltage history and equals

\[
 z_v(t+\theta+\tau_j)b_j(t+\theta+\tau_j),
\]

where

\[
 b_j(s)=\frac{\varepsilon}{2}
 \left[\kappa_1+3\kappa_3(v(s-\tau_j)-1)^2\right].
\]

Let \(p\) be the neutral flow tangent. Since \(Mp=p\), while
\(fM=\lambda f\) and \(\lambda\neq1\), one has \(f(p)=0\). Therefore the
Route-C section projection

\[
 Q=I-p\,\frac{h_C}{h_C(p)}
\]

preserves the adjoint action: \(f(Qy)=f(y)\). In particular,
\(f(q^\Sigma)=f(q)\neq0\).

## 3. Directed Fourier left row

At \(s=0.69836042\), on a radius \(1.1\times10^{-8}\) that contains the
refined real root, the full Grushin contraction is below \(0.09405\). The
bottom-row residual is below \(3.83\times10^{-10}\). The Neumann row formula
gives

\[
 \|E_-^{\mathrm{exact}}-E_-^{\mathrm{binary}}\|_{(\ell^1)^*}
 <1.18\times10^{-9}.
\]

One finite Fourier component has exact modulus above \(0.0296\), so the full
infinite-dimensional cokernel row is rigorously nonzero. The result stores
all 258 binary64 finite-row coefficients and the directed tail-aware row
distance, making the pencil action reproducible.

This row acts in the complex Wiener \(\ell^1\)-primal/
\(\ell^\infty\)-dual pairing. It is not yet a certified history measure. The
missing bridge must establish the Fourier reversal/conjugation convention,
a summable adjoint tail, and the normalization relating the Grushin border
to the RFDE bilinear functional. The effective-Hamiltonian slope lower bound
is evidence of a transverse simple root; it is not silently relabeled as a
lower bound for \(|f(q)|\).

## 4. Finite-section history-action pilot

For the 120-, 180-, and 240-step Route-C return discretizations, Stage 4C
computes the left unstable covector, normalizes it by \(f_N(q_N)=1\), and
stores the complete finest-grid action

\[
 f_N(y)=\sum_i \ell_i y_v(\theta_i)+\ell_wy_w(0).
\]

At 240 steps the recovery atom is about \(1.3783\), whereas the discrete
voltage-history total variation is about \(2.31\times10^{-2}\). The first
four weak moments and their last-two-grid changes are recorded. These
changes are diagnostics, not interval errors. Cubic interpolation also
introduces padding nodes outside the exact delay interval, so the nodal
covector cannot be promoted to an atom-plus-density measure.

The public pilot function applies

\[
 y\longmapsto y-q\frac{\ell y}{\ell q}
\]

as one numerical expression and verifies that it removes \(q\). A strict
replacement must evaluate \(q\), \(Y_{qq}\), \(f(Y_{qq})\), and their
subtraction in one shared outward interval-polynomial representation.

## 5. Consequence for the \(C_s^{uu}<12\) route

The Stage-4A heuristic envelope remains

\[
 \widehat C_s^{uu}=7.94681563672845125978,
\]

below the design target \(12\) and the isolated pilot failure ceiling
\(13.91505697\). No structural obstruction has appeared. The smallest
remaining certificate is now precise:

1. convert the enclosed Fourier cokernel into a directed normalized Route-C
   history action;
2. propagate a shared directed enclosure of the physical-return
   \(Y_{qq}\);
3. evaluate \(Y_{qq}-qf(Y_{qq})\) before taking the history sup norm.

Until those three operations close, every stable-graph, radius,
separator-crossing, and onset flag remains false.
