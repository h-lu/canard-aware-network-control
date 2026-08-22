# Leading delay-moment calibration

Status: **proved by polynomial solvability for the scalar calibration model; network lift remains a candidate.**

## 1. Scaled invariant-graph problem

From [model v0](model-v0.md),

\[
X'=Y-X^2+\delta\left[-\frac{X^3}{3}
+K\bigl(X-X_\Theta\bigr)\right],
\qquad
Y'=-X+\delta\nu,
\tag{1}
\]

where \(X_\Theta=X(s-\Theta)\). Seek

\[
Y(X;\delta)=Y_0+\delta Y_1+\delta^2Y_2+\cdots,
\qquad
\nu(\delta)=\nu_0+\delta\nu_1+\cdots.
\tag{2}
\]

The invariant-graph equation is

\[
Y_X\left[Y-X^2+\delta\left(-\frac{X^3}{3}
+K(X-X_\Theta)\right)\right]+X-\delta\nu=0.
\tag{3}
\]

The delay is imposed nonlocally through

\[
W(X;\delta)-W(X_\Theta;\delta)=\Theta,
\qquad
W_X=\frac1{X'}.
\tag{4}
\]

## 2. Zeroth order

Polynomial solvability gives

\[
Y_0=X^2-\frac12,
\qquad
X'_0=-\frac12.
\tag{5}
\]

Consequently the delayed point on the unperturbed critical orbit is exact:

\[
X_{\Theta,0}=X+\frac{\Theta}{2}.
\tag{6}
\]

## 3. First graph correction

At order \(\delta\), set \(Y_1=a_0+a_1X+a_2X^2+a_3X^3\). Matching every power of \(X\) in (3) yields

\[
Y_1=\frac{X^3}{3}+\frac X4+\frac{K\Theta}{2},
\qquad
\nu_0=-\frac18.
\tag{7}
\]

A useful cancellation follows:

\[
V_1:=Y_1-\frac{X^3}{3}
+K(X-X_{\Theta,0})=\frac X4,
\tag{8}
\]

so the first correction to the time map is independent of \(K\) and \(\Theta\). Since \(W_0=-2X\) and \(W_1=-X^2/2\), (4) gives

\[
X_{\Theta,1}=-\frac{\Theta(4X+\Theta)}{16}.
\tag{9}
\]

## 4. Second solvability condition

At order \(\delta^2\), a quadratic ansatz gives

\[
Y_2=-\frac{X^2}{8}-\frac{K\Theta X}{4}
-\frac{K\Theta^2}{16}-\frac{3}{32},
\qquad
\boxed{\nu_1=\frac{K\Theta}{8}}.
\tag{10}
\]

Because \(a=1+\delta^2\nu\) and \(\delta=\sqrt\varepsilon\), the scalar critical parameter is therefore

\[
\boxed{
a_c(\varepsilon,K,\Theta)
=1-\frac18\varepsilon
+\frac{K\Theta}{8}\varepsilon^{3/2}
+O(\varepsilon^2).
}
\tag{11}

The executable derivation is `src/canard_control/leading_delay_moment.py`; its unit test checks every displayed coefficient.

## 5. Independent source comparison

The public Maple worksheet accompanying Zhang et al. (2026) reports \(\nu_0=-1/8\) and \(\nu_1=K\widetilde\tau/8\), matching (7) and (10). Source artifact:

- DOI: [10.5281/zenodo.17051267](https://doi.org/10.5281/zenodo.17051267)
- file: `Maple program.mw`
- MD5: `4e4cfc5395f3744a2ae93ab2c2c3ca6e`

The third-party worksheet is not redistributed in this repository.

## 6. Network-lift hypothesis

For a synchronized rank-one skeleton with normalized critical right profile \(r\), left projection \(\ell\), and \(\ell^\top r=1\), define

\[
M_1(W,\Theta;\ell,r)
=\sum_{i,j}\ell_iW_{ij}r_j\Theta_{ij}.
\tag{12}
\]

Projecting only the unperturbed delayed translation suggests the candidate replacement

\[
K\Theta\longmapsto K M_1,
\qquad
a_{c,N}^{h}
=1-\frac18\varepsilon
+\frac{K M_1}{8}\varepsilon^{3/2}
+\cdots.
\tag{13}
\]

Equation (13) is **not yet a network theorem**. It is valid as a research hypothesis only after showing that:

1. the critical collective mode is closed at the required order;
2. transverse delayed modes do not add another order-\(\varepsilon^{3/2}\) functional;
3. module-pair delay residuals are smaller than the selected term;
4. the observable/adjoint normalization produces exactly (12);
5. the threshold-transfer error is \(o(\varepsilon^{3/2})\).

The two-module derivation must test these five points before the coefficient is used in control design.

## 7. Exact rank-one row-measure lift

There is one nontrivial network class where the first-moment replacement is already exact at the reduction level. Assume \(W\) is row-stochastic and each row has the same weighted scaled-delay measure

\[
\rho_i=\sum_jW_{ij}\delta_{\Theta_{ij}}=\rho.
\tag{14}
\]

For any synchronous history \(X_i(s+\xi)=\phi(\xi)\), the coupling at node \(i\) is

\[
\sum_jW_{ij}\left[\phi(0)-\phi(-\Theta_{ij})\right]
=\phi(0)-\int\phi(-\theta)\,d\rho(\theta),
\tag{15}
\]

which is independent of \(i\). Hence the synchronous RFDE history space is exactly invariant, even when individual edge delays differ.

Let

\[
m_k=\int\theta^k\,d\rho(\theta).
\tag{16}
\]

Along the zeroth-order critical orbit,

\[
\mathbb E_\rho X_{\theta,0}=X+\frac{m_1}{2},
\qquad
\mathbb E_\rho X_{\theta,1}
=-\frac{m_2+4Xm_1}{16}.
\tag{17}
\]

Repeating the solvability calculation gives

\[
Y_2=-\frac{X^2}{8}-\frac{Km_1X}{4}
-\frac{Km_2}{16}-\frac{3}{32},
\qquad
\boxed{\nu_1=\frac{Km_1}{8}}.
\tag{18}
\]

Thus the first moment shifts the parameter at \(O(\varepsilon^{3/2})\), while the second moment already changes the critical graph at the same graph order but cancels from this parameter solvability condition. The exact invariance statement is elementary; the displayed asymptotic coefficient is a formal polynomial-solvability result pending a uniform remainder proof.

This row-measure class is the rank-one calibration for the topology-weighted law. General rank-\(r\) modules with different \(\rho_{ab}\) still require the adjoint/transverse calculation in (12)--(13).
