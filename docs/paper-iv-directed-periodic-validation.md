# Directed validation of the finite FHN periodic problem

Status of this finite precursor to D1--D2: **the exact 97-node odd-Fourier collocation equations have a unique
phase-fixed root in an explicit MPFR-directed box, and their finite bordered
Jacobian is invertible throughout that box.** The complete residual of the
associated trigonometric polynomial, including modes outside the collocation
band, is also enclosed by directed Fourier convolution. **This does not yet
validate a periodic orbit or bordered inverse of the infinite-dimensional
RFDE.** The finite--tail coupling and nonlinear correction-tail estimates
needed for the infinite radii polynomial have not been supplied. Issue 15
therefore [remains open](https://github.com/h-lu/canard-aware-network-control/issues/15).
The later de-aliased finite/tail argument in
[paper-iv-infinite-periodic-validation.md](paper-iv-infinite-periodic-validation.md)
now closes the center-orbit RFDE radii inequality; the present note is retained
as the finite-stage record and falsifier.

The reusable interval arithmetic is implemented in
[directed_interval.py](../src/canard_control/directed_interval.py), and the
model validation is in
[fhn_periodic_directed_validation.py](../src/canard_control/fhn_periodic_directed_validation.py).
The driver, exact dependencies, and machine-readable result are
[fhn_periodic_directed_validation.py](../experiments/fhn_periodic_directed_validation.py),
[requirements-fhn-periodic-validation.txt](../experiments/requirements-fhn-periodic-validation.txt),
and
[fhn_periodic_directed_validation.json](../experiments/results/fhn_periodic_directed_validation.json).
The tests are in
[test_fhn_periodic_directed_validation.py](../tests/test_fhn_periodic_directed_validation.py).
The frozen JNS manuscript is not modified or used as evidence.

## 1. Arithmetic and the exact finite problem

The host has no Arb, FLINT, MPFI, Sage, or an interval FFT package. It does
have gmpy2 2.2.2 linked to MPFR 4.2.1. Every interval endpoint in this note
is evaluated by MPFR at 160 bits, once with `RoundDown` and once with
`RoundUp`. Decimal parameters such as \(0.2\) are parsed as directed
enclosures of the exact decimal real; the stored orbit values are interpreted
as exact binary64 numbers. Decimal values written to JSON are pushed one MPFR
number outward before conversion, so the printed upper and lower bounds
retain their stated direction.

Let \(N=97\), \(K=(N-1)/2=48\), and let \(D_N\) and \(S_{j,N}(T)\) be the
exact odd-Fourier derivative and delay-shift matrices. Their entries are
enclosed from

\[
 (D_N)_{m\ell}
 =\begin{cases}
  \pi(-1)^{m-\ell}
  \csc\!\left(\dfrac{\pi(m-\ell)}N\right),&m\ne\ell,\\
  0,&m=\ell,
 \end{cases}
 \tag{1.1}
\]

and

\[
 (S_{j,N})_{m\ell}
 =\frac1N\left[1+2\sum_{k=1}^{K}
 \cos\!\left(2\pi k
 \left\{\frac{m-\ell}{N}-\frac{\tau_j}{T}\right\}
 \right)\right].
 \tag{1.2}
\]

Interior extrema of every trigonometric interval are tested using MPFR
integer turn bounds; no binary64 range reduction is used in the interval
trigonometry.

For the synchronous FHN field \(f\), define the exact finite map

\[
 \mathcal F_N(X,T)=
 \begin{pmatrix}
  D_NX-Tf(X,S_{0,N}(T)X,S_{1,N}(T)X)\\
  \ell_N(X)
 \end{pmatrix}
 \in\mathbb R^{2N+1},
 \tag{1.3}
\]

where \(\ell_N\) is the fixed integral phase border from the floating
candidate. The derivative of (1.3) uses the exact moving-delay period column

\[
 c_T=-f-\sum_{j=0}^1
 \frac{\tau_j}{T}B_jS_{j,N}(T)D_NX.
 \tag{1.4}
\]

The interval Jacobian is evaluated twice: at the stored point and over a
full infinity-norm box in all \(2N+1\) unknowns. Thus the result below is a
statement about the exact real map (1.3), not merely about the binary matrix
returned by NumPy.

## 2. A directed contraction theorem for the nodal equations

Let \(\bar x_N\) be the stored binary candidate, \(\bar J_N\) its binary
Jacobian, and \(A_N=\operatorname{fl}(\bar J_N^{-1})\), interpreted after
construction as an exact real matrix of binary64 entries. Directed interval
evaluation gives

\[
 R_N\ge\|\mathcal F_N(\bar x_N)\|_\infty,
 \qquad
 \Delta_N\ge
 \|D\mathcal F_N(\bar x_N)-\bar J_N\|_\infty.
 \tag{2.1}
\]

The product \(A_N\bar J_N\) is formed in binary64 only as an accelerator.
Its exact-real defect is bounded using

\[
 \|\operatorname{fl}(A_N\bar J_N)-A_N\bar J_N\|_\infty
 \le
 \gamma_{2N+1}\|A_N\|_\infty\|\bar J_N\|_\infty
 +(2N+1)^2 2^{-1022},
 \tag{2.2}
\]

where \(\gamma_m=mu/(1-mu)\) and \(u=2^{-53}\). All norms and the right-hand
side of (2.2) are then accumulated upward in MPFR. The calculation checks
that the host uses IEEE binary64, that the process rounding mode is
round-to-nearest both before and after the product, and that every binary
input and product is finite. The conservative smallest-normal correction
also covers a kernel that flushes subnormal results. This use of the standard
IEEE-754 dot-product model is recorded in the result; it is not replaced by
an empirical inverse residual.

Set

\[
 Y_N=\|A_N\|_\infty R_N,
 \qquad
 Z_N(r)=sup_{\|x-\bar x_N\|_\infty\le r}
 \|I-A_ND\mathcal F_N(x)\|_\infty.
 \tag{2.3}
\]

The interval Jacobian over the whole box supplies \(Z_N(r)\). The verified
numbers are

\[
\begin{aligned}
 R_N&\le1.751501685734954\times10^{-13},\\
 \Delta_N&\le5.187417423663838\times10^{-13},\\
 \|A_N\|_\infty&\le20.39025089582423,\\
 \|I-A_ND\mathcal F_N(\bar x_N)\|_\infty
 &\le4.441595447617694\times10^{-10},\\
 Y_N&\le3.571355881659479\times10^{-12}.
 \tag{2.4}
\end{aligned}
\]

For

\[
 r_N=7.142711766491460\times10^{-12},
 \tag{2.5}
\]

the uniform derivative bound and radii inequality are

\[
 Z_N(r_N)\le2.682564565818246\times10^{-6}<1,
 \tag{2.6}
\]

\[
 Y_N+Z_N(r_N)r_N
 \le3.571375042444967\times10^{-12}
 <r_N,
 \tag{2.7}
\]

with directed lower margin

\[
 r_N-\{Y_N+Z_N(r_N)r_N\}
 \ge3.571336724046493\times10^{-12}>0.
 \tag{2.8}
\]

> **Proposition 2.1 (exact finite collocation root).** At the exact decimal
> parameter values
> \((\varepsilon,a,\Theta_0,\Theta_1,\kappa_1,\kappa_3)
> =(0.2,0.6,4,5,0.2,0.25)\), the exact finite map \(\mathcal F_{97}\) has a
> unique zero in the closed infinity-norm ball
> \(\overline B_{r_N}(\bar x_N)\). Its bordered Jacobian is invertible
> throughout that ball.

**Proof.** The map

\[
 \mathcal T_N(x)=x-A_N\mathcal F_N(x)
 \tag{2.9}
\]

has Lipschitz constant at most (2.6) on the ball. Equations (2.7)--(2.8)
show that it maps the ball strictly into itself. Banach's theorem gives a
unique fixed point. The pointwise defect bound below one makes
\(A_ND\mathcal F_N\), and hence both square factors, invertible. Therefore a
fixed point of (2.9) is a zero of \(\mathcal F_N\). The uniform form of
(2.6) proves bordered invertibility throughout the ball. \(\square\)

The machine record also gives the corresponding uniform inverse-norm bound

\[
 \sup_{\|x-\bar x_N\|_\infty\le r_N}
 \|D\mathcal F_N(x)^{-1}\|_\infty
 \le20.39030559413551.
 \tag{2.10}
\]

Proposition 2.1 is an exact theorem about a \(195\)-dimensional algebraic-
trigonometric system. It is not yet a theorem about the RFDE.

## 3. The complete residual of the trigonometric polynomial

The nodal residual in (2.4) is not a bound between nodes. To expose aliasing,
the code reconstructs every Fourier coefficient by an MPFR-directed DFT.
Delay shifts multiply mode \(k\) by a directed enclosure of
\(e^{-2\pi ik\tau_j/T}\). The quadratic and cubic terms are evaluated by
finite interval convolution. Since the approximate orbit has support
\(|k|\le K\), the polynomial FHN residual has exact finite support
\(|k|\le3K=144\); no FFT truncation is used in this residual calculation.

With the vector \(\ell^1\) norm and the mild weight \(\nu=1.001\), the
directed bounds are

\[
\begin{aligned}
 6.040895917698562\times10^{-6}
 &\le\|\mathcal R(\bar X,\bar T)\|_{\ell^1}
 \le6.040895917698563\times10^{-6},\\
 \|\mathcal R(\bar X,\bar T)\|_{\ell^1_\nu}
 &\le6.340990736688841\times10^{-6},\\
 3.020447921307180\times10^{-6}
 &\le\|Q_K\mathcal R(\bar X,\bar T)\|_{\ell^1}
 \le3.020447921307181\times10^{-6},\\
 4.876964462986438\times10^{-7}
 &\le\max_k\|\mathcal R_k\|
 \le4.876964462986439\times10^{-7}.
 \tag{3.1}
\end{aligned}
\]

Here \(Q_K\) selects modes outside the original collocation band. The directed
two-sided bounds imply

\[
 0.499999993785342
 <\frac{\|Q_K\mathcal R\|_{\ell^1}}
         {\|\mathcal R\|_{\ell^1}}
 <0.499999993785343.
 \tag{3.2}
\]

Thus the out-of-band residual is proved strictly nonzero and accounts for
essentially half of the full residual. The binary nodal residual
\(6.75\times10^{-14}\) cannot be used as an RFDE residual: the collocation
equations alias the high modes back onto the grid. This is the principal
directed falsifier produced by the present stage.

The last three orbit modes have total coefficient bound

\[
 1.439925306519508\times10^{-8}.
 \tag{3.3}
\]

This is a resolved-tail diagnostic, not a bound on the unknown correction
tail.

## 4. What the tail estimate proves—and what it does not

Let \(\mathcal B\) denote the lower-order current and delayed coefficient
operator in the linearization at the approximate polynomial. Directed
Wiener algebra estimates give

\[
 \|\mathcal B\|_{\ell^1\to\ell^1}
 \le6.192110915004497.
 \tag{4.1}
\]

On modes \(|k|\ge K+1\), the inverse derivative contributes
\((2\pi|k|)^{-1}\). Hence

\[
 \rho_K:=
 \frac{\bar T\|\mathcal B\|}{2\pi(K+1)}
 \le0.332666038252441<1.
 \tag{4.2}
\]

Equation (4.2) validates the elementary tail-diagonal Neumann gate for the
linearization at the approximate polynomial. It does **not** validate the
full bordered operator. Multiplication by the nonconstant orbit coefficients
couples finite and tail modes, and the finite inverse in Proposition 2.1 is
the inverse of a nodal aliasing discretization rather than the finite block
of a de-aliased infinite coefficient operator.

To pass from the present result to even the center-point infinite parts of
D1--D2, one must define one infinite
approximate inverse \(\mathcal A\) and bound all four blocks

\[
\begin{pmatrix}
 P_K(I-\mathcal A D\mathcal F)P_K&
 P_K(I-\mathcal A D\mathcal F)Q_K\\
 Q_K(I-\mathcal A D\mathcal F)P_K&
 Q_K(I-\mathcal A D\mathcal F)Q_K
\end{pmatrix}.
\tag{4.3}
\]

In particular, the following quantities are still absent:

1. a de-aliased finite coefficient Jacobian and its directed inverse;
2. the two finite--tail cross norms in (4.3);
3. a tail inverse compatible with the phase and period border;
4. a bound for the change of all four blocks on a correction ball; and
5. the quadratic/cubic correction-tail convolution entering the infinite
   radii polynomial.

Until these are supplied, the implication

\[
 \text{finite root} + \text{small polynomial residual}
 \Longrightarrow \text{RFDE periodic orbit}
 \tag{4.4}
\]

is invalid. The source and JSON therefore hard-code
`periodic_rfde_orbit_validated=false` and
`bordered_rfde_inverse_validated=false`.

## 5. The next radii polynomial

Use the real-conjugate Fourier space

\[
 \mathcal X_\nu=
 \{(V_k,W_k)_{k\in\mathbb Z}:x_{-k}=\overline{x_k},
 \ \|x\|_\nu=\sum_k\|x_k\|\nu^{|k|}<\infty\}
 \times\mathbb R_T,
 \tag{5.1}
\]

with the phase border retained. Construct \(\mathcal A\) from a directed
inverse of a de-aliased finite block and the diagonal derivative inverse on
the tail. Required outward bounds have the standard roles

\[
\begin{aligned}
 Y&\ge\|\mathcal A\mathcal F(\bar x)\|_\nu,\\
 Z_0&\ge\|I-\mathcal A D\mathcal F(\bar x)\|,\\
 Z_1r+Z_2r^2&\ge
 \sup_{\|h\|_\nu\le r}
 \|\mathcal A
  \{D\mathcal F(\bar x+h)-D\mathcal F(\bar x)\}h\|_\nu.
 \tag{5.2}
\end{aligned}
\]

The decisive check is

\[
 p(r)=Y+(Z_0+Z_1r+Z_2r^2)r-r<0.
 \tag{5.3}
\]

The full-polynomial bound (3.1) contributes to \(Y\), and (4.2) contributes
to the tail part of \(Z_0\). Neither determines the cross blocks or the
nonlinear terms in (5.2). The executable refusal is therefore:

\[
 \boxed{
 \text{do not evaluate or report }p(r)
 \text{ until every term in (5.2) is directed and finite}.}
 \tag{5.4}
\]

This was the remaining center-point route after the finite-stage
calculation.  The later de-aliased finite/tail note supplies (4.3) and (5.2)
and validates the center orbit. Repeating the finite nodal validation at a
larger \(N\) can reduce (3.1), but it cannot replace those estimates. Issue
15 still requires Floquet transfer, parameter-box continuation, extrema and
response enclosures.

## 6. Reproduction

From the repository root:

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_periodic_directed_validation.py
```

The exact validation dependencies are in
`experiments/requirements-fhn-periodic-validation.txt`. Run the focused
tests with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_periodic_directed_validation.py
```

The generated JSON records the MPFR version, precision, rounding policy,
finite theorem flags, infinite refusal flags, every directed constant above,
and the missing-tail falsifier.

## 7. Claim ledger

| Claim | Status |
|---|---|
| Reusable MPFR real/complex interval arithmetic | Implemented and tested |
| Directed odd-Fourier derivative and delay matrices | Implemented and tested across two precisions |
| Exact 97-node phase-fixed collocation root | Proved by Proposition 2.1 |
| Exact finite bordered inverse on the validation ball | Proved by the uniform defect bound |
| Full trigonometric-polynomial FHN residual through mode \(3K\) | Directed two-sided Wiener bounds proved computationally |
| Tail derivative Neumann gate at the approximate polynomial | Directed bound \(\rho_K<1\) |
| De-aliased finite/tail bordered inverse | Not supplied at this finite stage; supplied by the later infinite note |
| Nonlinear correction-tail radii bound | Not supplied at this finite stage; supplied by the later infinite note |
| Infinite radii polynomial | Not evaluated here; negative in the later infinite note |
| Synchronous FHN periodic RFDE orbit | Not validated here; validated at the center by the later infinite note |
| Infinite RFDE bordered inverse | Not validated here; phase-bordered inverse validated at the center by the later infinite note |
| Issue 15 | Open |
