# A synchronous-FHN periodic response candidate and its proof contract

Status: **the normalized two-delay BVP, its moving-delay period column, the
two gain-sensitivity equations, and the finite-dimensional response
calculation are implemented reproducibly.** At the candidate point below,
four Fourier resolutions agree and a nine-point gain-box sample has a
positive floating-point Weyl margin. **This is not a directed interval
proof.** No outward rounding, Fourier-tail enclosure, parametric continuum
enclosure, RFDE operator inverse, or interval extremum isolation has been
completed. Consequently the validated FHN hypothesis in
[paper-iv-reset-only-block-control.md](paper-iv-reset-only-block-control.md)
remains open.

The implementation is
[fhn_periodic_candidate.py](../src/canard_control/fhn_periodic_candidate.py),
the reproducible driver is
[fhn_periodic_box_candidate.py](../experiments/fhn_periodic_box_candidate.py),
and the generated binary64 record is
[fhn_periodic_box_candidate.json](../experiments/results/fhn_periodic_box_candidate.json).
The tests are in
[test_fhn_periodic_candidate.py](../tests/test_fhn_periodic_candidate.py).
Nothing in the frozen JNS manuscript is changed or used as evidence here.

## 1. Declared equation and candidate operating point

On the completely synchronous history, the frozen two-module model is

\[
\begin{aligned}
 \dot V={}&V-\frac{V^3}{3}-W
 +\varepsilon\kappa _1
 \left\{\frac{V(t-\tau _0)+V(t-\tau _1)}2-V(t)\right\}\\
 &+\varepsilon\kappa _3
 \left\{\frac{(V(t-\tau _0)-1)^3+(V(t-\tau _1)-1)^3}{2}
 -(V(t)-1)^3\right\},\\
 \dot W={}&\varepsilon(V-a),
 \qquad \tau_j=\Theta_j/\sqrt\varepsilon .
 \tag{1.1}
\end{aligned}
\]

The two baseline controls are

\[
 b=(\kappa _1,\kappa _3),
 \qquad
 P(b)=\bigl(F(b),R(b)\bigr),
 \quad F=T^{-1},
 \quad R=(\max V-\min V)^2.
 \tag{1.2}
\]

The numerical search selected the following candidate, because a shorter
delay pair produced response columns that were nearly parallel:

\[
 \varepsilon=0.2,
 \quad a=0.6,
 \quad (\Theta_0,\Theta_1)=(4,5),
 \quad b_*=(0.2,0.25).
 \tag{1.3}
\]

Thus

\[
 (\tau_0,\tau_1)
 =(8.94427190999916,11.18033988749895).
 \tag{1.4}
\]

This is a candidate operating point for the periodic block, not frozen
theorem data. In particular, \(\varepsilon=0.2\) is not asserted to lie in
any asymptotic canard regime. The periodic block theorem itself is a
fixed-positive-parameter statement, but connecting this point to the
singular threshold program would require the separate Paper II and Paper III
gates. The symbol \(a\) in (1.1)--(1.3) is the fixed recovery-nullcline
parameter, not the reset-only operational actuator \(a_{\rm op}\).

The synchronous history space is exactly invariant, so (1.1) is an exact
restriction of the network. No calculation below proves transverse
stability in the full network. The candidate can therefore support the
two-output synchronous response block only; it is not yet evidence that the
rhythm is an attracting biological network state.

## 2. Odd Fourier BVP

Put \(\theta=t/T\) and write \(X=(V,W)\) as a one-periodic function. Let
\(D_N\) be the odd Fourier differentiation matrix on
\(\theta_n=n/N\), and let

\[
 S_j(T)=\mathcal F_N^{-1}
 \operatorname{diag}\left(
 e^{-2\pi i k\tau_j/T}
 \right)\mathcal F_N .
 \tag{2.1}
\]

Odd \(N\) avoids an unpaired Nyquist mode. The collocation equations are

\[
 \Phi_N(X,T;b)=D_NX-Tf(X,S_0(T)X,S_1(T)X;b)=0
 \tag{2.2}
\]

together with the integral phase discretization

\[
 \ell_N(X)=\frac1N
 \sum_{n=0}^{N-1}
 (D_NX_{\rm ref})_n^T(X_n-X_{{\rm ref},n})=0.
 \tag{2.3}
\]

At zero delayed gains an accurately integrated FHN ODE cycle initializes
the BVP. Eight equal gain steps continue to (1.3); a damped Newton solve is
used at every step. This initialization is only numerical. The BVP, rather
than the time integration, determines the reported delayed orbit.

### 2.1 The period column

Let \(C_0\) be the current Jacobian and \(B_j\) the delayed Jacobians from
Section 6 of
[paper-iv-periodic-rfde-adjoints.md](paper-iv-periodic-rfde-adjoints.md).
At fixed Fourier coefficients,

\[
 \partial_T S_j(T)X
 =\frac{\tau_j}{T^2}S_j(T)D_NX.
 \tag{2.4}
\]

Therefore the state block is the Fourier discretization of the retarded
linearized operator, while the period column is

\[
 c_T=-f-\sum_{j=0}^1
 \frac{\tau_j}{T}B_jS_j(T)D_NX.
 \tag{2.5}
\]

The second term in (2.5) is essential. Replacing the column by \(-f\)
would hold normalized delay fractions fixed while changing the physical
period and would differentiate a different problem. A finite-difference
test differentiates every state coordinate and \(T\) and checks the full
analytic matrix.

## 3. Forward sensitivities, discrete adjoints, and extrema

Write \(J_N\) for the bordered Jacobian of (2.2)--(2.3). Because the
physical delays are fixed when either gain changes, the two bordered
sensitivities solve

\[
 J_N
 \begin{pmatrix}X_{\kappa_q}\\T_{\kappa_q}\end{pmatrix}
 =
 \begin{pmatrix}Tf_{\kappa_q}\\0\end{pmatrix},
 \qquad q\in\{1,3\}.
 \tag{3.1}
\]

The frequency row is

\[
 F_{\kappa_q}=-T_{\kappa_q}/T^2.
 \tag{3.2}
\]

The code isolates every zero of the resolved Fourier derivative \(V'\) on
a dense phase scan and refines each sign-changing bracket. At a candidate
simple maximum \(\theta_+\) and minimum \(\theta_-\), the envelope formula
is

\[
 R_{\kappa_q}
 =2\Delta_V
 \{V_{\kappa_q}(\theta_+)
    -V_{\kappa_q}(\theta_-)\},
 \qquad
 \Delta_V=V(\theta_+)-V(\theta_-).
 \tag{3.3}
\]

For each output gradient \(d_N\), a separate transpose solve

\[
 J_N^Tq_N=d_N
 \tag{3.4}
\]

reproduces \(d_N^TJ_N^{-1}g_q=q_N^Tg_q\). This is a useful sign and
transpose audit, not an independent error bound: both calculations use the
same finite matrix. A stronger nonlinear check re-solves the BVP at the
four axial box points and compares (3.1)--(3.3) with centered differences
of the resulting \((F,R)\).

## 4. Executable center candidate

At \(N=129\), the computation gives

\[
 T_*=16.540387798180934,
 \qquad F_*=0.06045807463534665,
 \tag{4.1}
\]

\[
 V_{\max}=1.9340639326901532,
 \qquad
 V_{\min}=-1.0133135267088629,
 \qquad R_*=8.6870338881734.
 \tag{4.2}
\]

The two resolved critical phases and curvatures are

\[
\begin{array}{c|c|c}
 &\theta&V''(\theta)\\ \hline
 \text{maximum}&0.09717902129278594&-77.72199338568275\\
 \text{minimum}&0.7981139838594246&84.41542953714621.
\end{array}
\tag{4.3}
\]

There are exactly two roots in the floating scan, with cyclic separation at
least \(0.2990650374\). These facts are strong root-isolation candidates,
but only interval signs on the complementary phase arcs can prove that no
additional roots occur.

The response matrix in the input and output units of (1.2) is

\[
 \boxed{
 B_*=
 \begin{pmatrix}
  0.0366998279955020&0.136339460687778\\
 -3.64561577177141&-6.13633797445939
 \end{pmatrix}.}
 \tag{4.4}
\]

Its binary64 diagnostics are

\[
 \det B_*=0.271838740013244,
 \qquad
 \sigma(B_*)=(7.13888251,0.0380786124).
 \tag{4.5}
\]

The bordered \(259\)-dimensional matrix has

\[
 \sigma_{\min}(J_{129})=0.4395291894,
 \quad \kappa_2(J_{129})=961.7140,
 \quad
 \|I-J_{129}\operatorname{fl}(J_{129}^{-1})\|_\infty
 =1.14\times10^{-12}.
 \tag{4.6}
\]

The collocation residual is \(1.14\times10^{-13}\), the sixfold
off-grid residual is \(2.18\times10^{-8}\), and the discrete translation
residual \(\|L_ND_NX\|_\infty\) is \(9.02\times10^{-6}\). The forward and
transpose response calculations disagree by at most
\(5.45\times10^{-13}\) over the sampled box.

### 4.1 Spectral convergence

Independent ODE-to-gain continuations give:

| \(N\) | \(T\) | off-grid residual | spectral-tail diagnostic | \(R_{\kappa_1}\) | \(R_{\kappa_3}\) |
|---:|---:|---:|---:|---:|---:|
| 65 | 16.5403877970093 | \(1.36\times10^{-3}\) | \(6.62\times10^{-5}\) | -3.645199993 | -6.134785764 |
| 97 | 16.5403877981809 | \(5.82\times10^{-6}\) | \(5.73\times10^{-7}\) | -3.645615089 | -6.136335941 |
| 129 | 16.5403877981809 | \(2.18\times10^{-8}\) | \(5.06\times10^{-9}\) | -3.645615772 | -6.136337974 |
| 193 | 16.5403877981810 | \(6.03\times10^{-13}\) | \(5.74\times10^{-13}\) | -3.645615770 | -6.136337968 |

The frequency row is stable to the displayed digits from \(N=97\) onward.
This convergence is compelling numerical evidence, but agreement of
truncations is not a tail proof. In particular, the \(N=65\) nodal
collocation residual is already about \(10^{-14}\) while its off-grid
residual is still \(1.36\times10^{-3}\). The \(N=193\) off-grid value
cannot be inferred from the nodal residual; it comes from resolving the
Fourier tail. Neither value is an interval residual bound.

## 5. The sampled gain-box candidate

Take

\[
 U_{\rm cand}=
 [0.2-5\times10^{-5},0.2+5\times10^{-5}]
 \times
 [0.25-5\times10^{-5},0.25+5\times10^{-5}].
 \tag{5.1}
\]

The driver solves the center, four edge midpoints, and four corners
independently from the center candidate. Every sampled orbit has two simple
resolved extrema. The smallest singular value among the nine sampled
response matrices is

\[
 \min_{b\in U_{3\times3}}
 \sigma_{\min}(B_N(b))=0.0380193361.
 \tag{5.2}
\]

Relative to (4.4), the entrywise sampled radius, after adding the declared
floating discrepancy padding, is

\[
 R_{\rm samp}=
 \begin{pmatrix}
  7.40\times10^{-6}&2.75\times10^{-5}\\
  6.31\times10^{-3}&1.8277\times10^{-2}
 \end{pmatrix},
 \qquad
 \|R_{\rm samp}\|_F=0.0193344470.
 \tag{5.3}
\]

Thus the ordinary floating analogue of the interval Weyl test is

\[
 \beta_{\rm cand}
 =\operatorname{fl}\{\sigma_{\min}(B_*)
   -\|R_{\rm samp}\|_F\}
 =0.0187441654>0.
 \tag{5.4}
\]

The centered output finite difference is

\[
 \begin{pmatrix}
 0.0366998279&0.1363394596\\
 -3.645615706&-6.136338117
 \end{pmatrix},
 \tag{5.5}
\]

whose maximum row-sum difference from (4.4) is
\(2.09\times10^{-7}\).

Equations (5.2)--(5.4) cover **only nine computed matrices**. They do not
bound the continuum in (5.1), and their arithmetic is not directed. The
name \(\beta_{\rm cand}\), rather than \(\beta_{\rm box}\), is intentional.

## 6. Preferred direct validated-RFDE route

A direct proof can retain the same normalized-period formulation. One
possible contract is the following.

### Gate D1: parametric orbit enclosure

Choose a weighted Fourier coefficient space with enough derivative loss to
control \(T\mapsto S_{\tau/T}\). Construct a finite approximate inverse of
the bordered operator and analytic tail preconditioner. With interval
parameters \(b\in U_{\rm cand}\), verify a Krawczyk or radii-polynomial
inequality

\[
 Y+Z(r)<r
 \tag{6.1}
\]

using outward-rounded FFT or coefficient convolution bounds. This must
enclose the infinite Fourier tail, the phase condition, and the dependence
of every multiplier \(e^{-2\pi i k\tau_j/T}\) on the interval period.

### Gate D2: RFDE nondegeneracy

The validation must give an inverse bound for the infinite bordered
operator, not merely \(\sigma_{\min}(J_N)>0\). Equivalently, it must prove
the simple phase kernel and the nonzero period-border pairing used in
Section 2 of the adjoint note.

### Gate D3: exactly two extrema

Isolate one zero of \(V'\) in each of two phase intervals; bound \(V''<0\)
on the first and \(V''>0\) on the second; and prove a strict interval sign
for \(V'\) on the complement. This supplies the unique-extrema hypothesis
and makes (3.3) rigorous.

### Gate D4: parametric response enclosure

Either validate the two extended sensitivity equations (3.1), or combine
a parameter-uniform inverse with outward-rounded right-hand sides. Evaluate
the period and extremum functionals with interval Fourier evaluation to get

\[
 B(b)\in\bar B+[-R_B,R_B]
 \quad\text{for every }b\in U_{\rm cand}.
 \tag{6.2}
\]

Finally compute a directed lower bound \(\underline s_B\) and upper bound
\(\overline r_B\) and verify

\[
 \underline s_B-\overline r_B>0.
 \tag{6.3}
\]

Only (6.3), after D1--D4, supplies the missing \(\beta\) in the reset-only
block theorem.

## 7. ODE-persistence route: relevant, but not a direct shortcut here

Gimeno, Lessard, Mireles James, and Yang prove persistence of periodic
orbits under a state-dependent delayed perturbation of an ODE using a
Chebyshev validation of the ODE orbit and its forward and backward
variational equations, followed by six interval polynomial inequalities
\(Q,P_0,P_1,P_2,\mu_1,\mu_2\). See the
[arXiv preprint](https://arxiv.org/abs/2111.06391) and the
[published SIADS article](https://doi.org/10.1137/22M1499418).

For fixed \(\varepsilon,a,\kappa_1,\kappa_3\), (1.1) can be written
exactly as

\[
 \dot x=f_0(x)+\varepsilon
 \{P_c(x(t))+P_0(x(t-\tau_0))+P_1(x(t-\tau_1))\},
 \tag{7.1}
\]

where

\[
\begin{aligned}
 f_0(V,W)&=(V-V^3/3-W,\ \varepsilon(V-a))^T,\\
 P_c(V,W)&=(-\kappa_1V-\kappa_3(V-1)^3,0)^T,\\
 P_j(V,W)&=\tfrac12
 (\kappa_1V+\kappa_3(V-1)^3,0)^T,
 \qquad j=0,1.
 \tag{7.2}
\end{aligned}
\]

This is close in spirit to the published framework, and constant delays
have the favorable property \(Dr_j=0\). It is **not a literal application
of the displayed single-perturbation theorem**, because (7.1) is a sum of a
zero-delay term and two distinct delayed terms. The article states that
multiple delays can be treated by the same framework, but the polynomial
bounds become longer. Those modified inequalities must be derived and
verified; citing the remark is not the verification.

At the candidate center, the executable ODE audit gives

\[
\begin{aligned}
 T_{\rm ODE}&=20.0081341148,\\
 \operatorname{spec}\Phi(T_{\rm ODE})
 &\approx\{0.999999999965,1.6794\times10^{-11}\},\\
 \max_t\|\Phi(t)\|_2&\approx5.84,
 \qquad
 \max_t\|\Phi(t)^{-1}\|_2\approx3.47\times10^{11},\\
 \varepsilon\|P\|_{\rm sampled}&\approx0.547,\\
 \min_{\text{discrete phase shifts}}
 \|X_{\rm DDE}-X_{\rm ODE}\|_{C^0}&\approx0.884.
 \tag{7.3}
\end{aligned}
\]

These are not interval quantities and are not the coefficients of the six
published polynomials. They do show why the ODE route should not be assumed
to close automatically at this strong-response point: the DDE orbit is not
numerically close to the ODE orbit, and the backward variational flow is
severely conditioned. Only an actual outward-rounded evaluation of the
adapted inequalities can decide the matter.

Even a successful persistence proof would close only part of Paper IV. To
obtain the response box it must be made uniform in
\((\kappa_1,\kappa_3)\), differentiated with respect to those gains, and
combined with interval extremum isolation. Hence this route can replace the
full DDE orbit existence validation, but it cannot replace D3, D4, or the
directed test (6.3).

For the present candidate, direct parametric RFDE collocation is therefore
the preferred proof route. The ODE-persistence route remains valuable for a
second search targeted at weaker feedback, where its polynomial
inequalities may close even though the response margin is smaller.

## 8. Exact conditional theorem supplied by a future certificate

The numerical package is designed around the following clean implication.

> **Conditional FHN response theorem.** Suppose a directed validation on
> \(U\subset\mathbb R^2\) proves a unique phase-fixed periodic branch of
> (1.1), invertibility of its infinite bordered linearization, exactly one
> nondegenerate voltage maximum and minimum, and an enclosure
> \(B(b)\in\bar B+[-R_B,R_B]\) satisfying (6.3). Then
> \[
>  \inf_{b\in U}\sigma_{\min}D_b(F,R)>0.
> \]
> Consequently, after the independent controlled-separator hypotheses and
> reset transversality bounds in the reset-only note are supplied, its exact
> block theorem yields a locally invertible three-output map.

The implication is elementary from the periodic adjoint theorem, the
envelope formula, Weyl's inequality, and the reset-only block theorem. Its
hypotheses are not claimed here.

## 9. Reproduction and refusal conditions

From the repository root, run

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_periodic_box_candidate.py
```

and test the implementation with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_periodic_candidate.py
```

The candidate must be rejected, not silently reported, if Newton fails, the
period becomes nonpositive, the resolved extrema cease to form one simple
maximum/minimum pair, or the input domain leaves
\(\varepsilon>0\), \(-1<a<1\), and positive scaled delays. A positive
binary64 \(\beta_{\rm cand}\) must never be renamed
\(\beta_{\rm box}\) without D1--D4 and directed rounding.

## 10. Claim ledger

| Claim | Status |
|---|---|
| Exact synchronous reduction (1.1) | Proved in the frozen reference model |
| Moving-delay Fourier period column (2.5) | Exact algebra; finite-difference tested |
| Finite bordered sensitivities and transpose identity | Implemented and tested |
| Reproducible orbit at (1.3) | Binary64 candidate |
| Two resolved simple extrema | Binary64 candidate; no interval complement signs |
| Positive center response singular value | Binary64 candidate |
| Positive nine-sample Weyl margin | Binary64 finite-sample candidate only |
| Periodic branch for every point of (5.1) | Open at validated-numerics level |
| Infinite RFDE bordered inverse | Open |
| Transverse stability of this orbit in the full FHN network | Open |
| Directed interval \(2\times2\) response certificate | Open; contract D1--D4 specified |
| Direct application of the published single-delay ODE theorem | No; multiple-term adaptation required |
| Adapted ODE-persistence proof at (1.3) | Open; current diagnostics are unfavorable |
| Positive reset-only \(3\times3\) FHN theorem | Conditional on this certificate and separator/reset bounds |
