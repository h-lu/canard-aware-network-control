# Directed D1/D3/D4 audit on a microscopic FHN gain box

Status: **D1, D3, and the directed response lower-bound part of D4 are
proved on the microscopic box declared below.**  The executable record is
authoritative for the directed numerical inequalities and Boolean gates;
Lemmas 2.1 and 4.1 supply the analytic bridges from those inequalities to
the theorem.  This note extends the single-point
\(M=144\) finite/tail argument
of [paper-iv-infinite-periodic-validation.md](paper-iv-infinite-periodic-validation.md)
to a deliberately microscopic two-gain box.  It also implements directed
unique-extremum isolation and a directed enclosure of

\[
 D_{(\kappa _1,\kappa _3)}(F,R_h),
 \qquad F=T^{-1},\qquad
 R_h=(V_{\max}-V_{\min})^2.
\]

The implementation, driver, tracked result, and regression tests are

- [fhn_periodic_parameter_box.py](../src/canard_control/fhn_periodic_parameter_box.py),
- [fhn_periodic_parameter_box.py](../experiments/fhn_periodic_parameter_box.py),
- [fhn_periodic_parameter_box.json](../experiments/results/fhn_periodic_parameter_box.json), and
- [test_fhn_periodic_parameter_box.py](../tests/test_fhn_periodic_parameter_box.py).

No frozen JNS file is changed.  Binary64 solves supply only midpoint
accelerators.  MPFR-directed bounds cover every quantity used by a theorem
flag.

## 1. Declared box and why it is microscopic

The fixed parameters remain

\[
 (\varepsilon,a,\Theta _0,\Theta _1)=(0.2,0.6,4,5),
\]

and the gain box is centered at \((0.2,0.25)\), with the exact decimal
half-width recorded in the JSON result.  The default is \(10^{-12}\) in
each coordinate.  This scale is intentional.  The original \(97\)-node
center polynomial had enough radii margin for a single orbit but interval
dependency in a continuum gain box consumed that margin already near
half-width \(10^{-10}\).  The default proof instead uses the spectrally
sharper \(129\)-node binary midpoint and a much smaller correction ball.

The midpoint has Fourier half-bandwidth \(64\), while the finite inverse
still uses \(M=144\).  Its cubic residual has support through \(|k|=192\).
No coefficient with \(145\le |k|\le192\) is discarded or aliased: those
modes enter the directed tail residual through

\[
 (A_Qy)_k=(2\pi i k)^{-1}y_k.
\]

The finite-to-tail and tail-to-finite bounds use the full support of the
linearized coefficients.  Thus changing the midpoint resolution does not
silently turn the proof into an \(M=144\) truncation.

## 2. D1: one uniform Newton map for every gain

Let \(U\) be the declared gain box and let
\(\bar x=(\bar v,\bar w,\bar T)\)
be the stored trigonometric midpoint.  The coefficient equation
\(\mathcal F_b(x)=0\) and its bordered derivative are exactly those in the
single-point note.  The only change is that \(\kappa _1\) and \(\kappa _3\)
are MPFR intervals from the start.

One binary midpoint inverse \(A_P\), together with the analytic tail
inverse \(A_Q\), is used for all \(b\in U\).  Directed arithmetic encloses

\[
 Y_U=\sup_{b\in U}\|A\mathcal F_b(\bar x)\|_\square
\]

and all four block columns of

\[
 I-A D_x\mathcal F_b(\bar x).
\]

The moving-delay estimates are unchanged: finite output modes are handled
directly and the tail factor \((2\pi i k)^{-1}\) cancels the derivative of
the Fourier rotation.  With \(Z_{0,U}\) denoting the largest complete block
column and \(Z_1,Z_2,Z_3\) the box-uniform nonlinear coefficients, the
program evaluates

\[
 q_U(r)=Z_{0,U}+Z_1r+Z_2r^2+Z_3r^3
\]

and accepts D1 only if

\[
 q_U(r)<1,
 \qquad
 Y_U+q_U(r)r<r.
\tag{2.1}
\]

For each fixed \(b\), (2.1) gives a unique phase-fixed solution in the same
Wiener ball.  Parameter regularity is not inferred by differentiating a
delay shift as a bounded operator on that unweighted ball.  The following
lemma supplies the required derivative-domain bridge.

> **Lemma 2.1 (the validated fixed points form a \(C^1\) branch).**  Let
> \(U\) be the closed gain box below, viewed inside the open positive-gain
> quadrant.  The unique fixed points supplied by (2.1) are the restriction
> to \(U\) of a \(C^1\) map
> \[
>  b\longmapsto x_b=(v_b,w_b,T_b)\in\mathcal X^1_{\mathbb R}.
> \tag{2.2}
> \]
> For \(q\in\{1,3\}\), its derivative \(s_q=\partial_{\kappa_q}x_b\)
> is the unique derivative-domain solution of
> \[
>  D_x\mathcal F_b(x_b)s_q+
>  \partial_{\kappa_q}\mathcal F_b(x_b)=0.
> \tag{2.3}
> \]

**Proof.**  Write \(\mathcal X^0_{\mathbb R}\) for the unweighted
real-conjugate Wiener space and \(\mathcal X^1_{\mathbb R}\) for its
Fourier-derivative domain, as in the center proof.  The contraction acts on
\(\mathcal X^0_{\mathbb R}\).  Its tail fixed-point identity is

\[
 (x_b)_{Q,k}=(2\pi ik)^{-1}T_b[f_b(x_b)]_{Q,k},
 \qquad |k|>M,
\tag{2.4}
\]

so the Wiener algebra property bootstraps every validated fixed point into
\(\mathcal X^1_{\mathbb R}\).

For one fixed physical delay \(\tau\), the nonlinear evaluation map

\[
 (T,v)\longmapsto S_{\tau/T}v,
 \qquad
 (S_{\tau/T}v)_k=e^{-2\pi ik\tau/T}v_k,
\tag{2.5}
\]

is jointly \(C^1\) from
\((0,\infty)\times\mathcal X^1_{\mathbb R}\) to
\(\mathcal X^0_{\mathbb R}\).  Its derivative is

\[
 D(S_{\tau/T}v)[\widehat T,\widehat v]_k
 =e^{-2\pi ik\tau/T}\widehat v_k
 +\frac{2\pi ik\tau}{T^2}e^{-2\pi ik\tau/T}
     v_k\widehat T.
\tag{2.6}
\]

The single Fourier weight gives operator-norm continuity of the
\(\widehat v\)-column from \(\mathcal X^1\) to \(\mathcal X^0\).  For the
scalar \(\widehat T\)-column, weighted summability followed by dominated
convergence gives continuity at each base point; perturbations of \(v\) are
controlled directly by the \(\mathcal X^1\) norm.  Hence the full derivative
in (2.6) is continuous.  This does not assert operator-norm differentiability of
\(T\mapsto S_{\tau/T}\) on \(\mathcal X^0\).  Polynomial Wiener
multiplication now shows that
\((b,x)\mapsto\mathcal F_b(x)\) is jointly \(C^1\) from the positive-gain
parameter set times \(\mathcal X^1_{\mathbb R}\) into the residual space.

There is also a useful weak-space calculation.  Let \(P\) retain the finite
Fourier block, \(Q=I-P\), and let \(\partial^{-1}Q\) be the analytic tail
inverse.  Although \(T\mapsto S_{\tau/T}\) is not operator-norm continuous
on \(\mathcal X^0\), the smoothed map

\[
 (\alpha,u)\longmapsto \partial^{-1}QS_\alpha u
 \tag{2.7}
\]

is jointly \(C^1\) from \(\mathbb R\times\mathcal X^0\) to
\(\mathcal X^0\), with

\[
 D(\partial^{-1}QS_\alpha u)[a,h]
 =\partial^{-1}QS_\alpha h-aQS_\alpha u.
 \tag{2.8}
\]

Indeed, the input column is operator-norm Lipschitz after multiplication by
\(\partial^{-1}Q\), while the scalar column is strongly continuous for the
fixed vector \(u\); the mixed remainder is bounded by
\(C|a|\|h\|_0\).  To make the cancellation explicit, write
\(x=(z,T)\), let \(P^{\rm aug}\) retain \(Pz\) and \(T\), and let
\(\ell\) be the fixed midpoint-tangent phase functional.  The weak
extension of the actual Newton map is

\[
\begin{aligned}
 Q\widetilde N_b(z,T)
   &=T\partial^{-1}Q f_b(z,T),\\
 P^{\rm aug}\widetilde N_b(z,T)
   &=P^{\rm aug}(z,T)-A_P
     \binom{P\{\partial Pz-Tf_b(z,T)\}}{\ell(z-\bar z)}.
\end{aligned}
\tag{2.8a}
\]

The finite expression is finite dimensional.  In the tail expression, each
moving-delay polynomial in this FHN field is a shifted polynomial, so
(2.7)--(2.8), the Wiener algebra property, and the chain rule give a
jointly \(C^1\) map on an open positive-period tube containing the common
closed \(\mathcal X^0\)-ball; all norm estimates are taken on that closed
ball.  On the dense
derivative domain its derivative is
\(I-A D_x\mathcal F_b\), and the bounded \(\mathcal X^0\)-extension of
that operator is precisely the one bounded in (2.1).  The differentiable
contraction theorem therefore gives a \(C^1\) weak-space fixed-point map.

For completeness, the derivative-domain inverse is not inferred merely from
that statement.  Let \(B_b\) denote the bounded \(\mathcal X^0\)-extension
of \(A D_x\mathcal F_b(x_b)\).  The strict finite/tail bound gives
\(\|I-B_b\|<1\) on \(\mathcal X^0\).  For \(g\in\mathcal Y^0\), set
\(h=B_b^{-1}Ag\).  The linear tail equation has the same derivative-inverse
form as (2.4), with only Wiener-algebra lower-order terms on its right, and
hence bootstraps \(h\) into \(\mathcal X^1\).  The reported finite defect
\(\|I-A_PJ_{PP}\|<1\) makes \(A_PJ_{PP}\) invertible; since these are
finite square matrices, \(A_P\) is injective.  The coefficientwise tail
inverse \(A_Q\) is injective as well, so the block operator \(A\) is
injective.  Therefore \(D_x\mathcal F_b(x_b)h=g\).  The same argument gives
injectivity.

Thus

\[
 D_x\mathcal F_b(x_b):\mathcal X^1_{\mathbb R}
       \longrightarrow\mathcal Y^0_{\mathbb R}
 \tag{2.9}
\]

is a bounded bijection between Banach spaces, where \(\mathcal X^1\) carries
its graph norm, so the bounded inverse theorem supplies its strong inverse.
The strong-space Banach implicit-function theorem now gives a
local \(C^1\) branch near every \(b\in U\).  Moreover, both inequalities in
(2.1) have strict uniform margins, and their explicit majorants vary
continuously with the gain endpoints.  Compactness therefore gives an
unquantified open neighborhood \(U_+\supset U\), still inside the positive
gain quadrant, on which the same contraction argument holds.  Pointwise
uniqueness makes the local branches agree on overlaps and hence produces a
single \(C^1\) map on \(U_+\).  All numerical bounds claimed in this note
remain restricted to the certified box \(U\).  Finally, the
injectivity of \(A\) also turns the fixed-point identity
\(A\mathcal F_b(x_b)=0\) into the original coefficient equation, and
differentiating it gives (2.3).
\(\square\)

The phase functional \(\ell\) is independent of \(b\).  With

\[
 L_T(v)=\frac12\sum_{j=0}^1S_{\tau_j/T}v-v,
 \qquad
 \mathcal C_T(v)=\frac12\sum_{j=0}^1S_{\tau_j/T}(v-1)^3-(v-1)^3,
\]

the two parameter columns, including the zero slow and phase rows, are

\[
 \partial_{\kappa_1}\mathcal F_b=(-T\varepsilon L_T,0,0),
 \qquad
 \partial_{\kappa_3}\mathcal F_b=(-T\varepsilon \mathcal C_T,0,0).
\tag{2.10}
\]

Thus the bordered residual evaluated below is exactly the one in (2.3),
including its sign and phase row.  The weak Newton extension is only
\(C^1\); a second period derivative loses another Fourier weight.  No
\(C^2\) branch, second sensitivity, or response-derivative Lipschitz bound
is asserted.

Thus D1 is a branch theorem in the synchronous RFDE coefficient space; it
is not a Floquet theorem for the full network.

## 3. D3: exactly one maximum and one minimum

The D1 ball controls coefficients in an unweighted Wiener norm, so it would
be invalid to differentiate the correction term coefficientwise.  Instead,
the code uses the RFDE itself.  If \(x_b\) is the validated solution, then

\[
 V_b'=T_b f_V(x_b,b).
\]

Wiener algebra estimates, the finite derivative of the midpoint
polynomial, the directed midpoint residual, and the gain-box widths give a
directed global number \(E_{V'}\) satisfying

\[
 \|V_b'-\bar V'\|_\infty\le E_{V'}
 \quad (b\in U).
\tag{3.1}
\]

The phase circle is split into the number of rational cells recorded in the
JSON.  On every cell outside two broad windows, interval evaluation of
\(\bar V'\) plus (3.1) excludes zero.  On the two broad windows the second
derivative is evaluated from the differentiated RFDE,

\[
\begin{aligned}
 V_b''=T_b\bigg[{}&
 \{1-V_b^2-\varepsilon\kappa _1
       -3\varepsilon\kappa _3(V_b-1)^2\}V_b'-W_b'\\
 &+\sum_{j=0}^1\frac{\varepsilon}{2}
  \{\kappa _1+3\kappa _3(V_b(\cdot-\tau_j/T_b)-1)^2\}
  V_b'(\cdot-\tau_j/T_b)\bigg].
\end{aligned}
\tag{3.2}
\]

Equation (3.2) uses only state and first-derivative enclosures; it assumes no
unproved \(X^2\) correction ball.  Strict curvature and endpoint signs prove
one zero in each broad window and no peak switching.  A second dyadic grid,
whose denominator is recorded, then gives narrow directed phase brackets
for D4.  The broad windows, not the narrow brackets, carry the curvature
proof.

## 4. D4: two validated sensitivity columns

The binary collocation solve supplies finite Fourier polynomials
\(\bar s_q\), \(q\in\{1,3\}\), for the two bordered sensitivity equations.
For reference, the exact state coefficients and moving-period column are

\[
\begin{aligned}
 a_{0,b}(v)&=1-v^2-\varepsilon\kappa_1
       -3\varepsilon\kappa_3(v-1)^2,\\
 a_{j,b}(v,T)&=\frac{\varepsilon}{2}
       \{\kappa_1+3\kappa_3(S_{\tau_j/T}v-1)^2\},\\
 c_T(b,x)&=-f_b(x)-\sum_{j=0}^1\frac{\tau_j}{T}
       a_{j,b}(x)S_{\tau_j/T}Dv.
\end{aligned}
\tag{4.0}
\]

These are the four implementation objects `current_coefficient`,
`delayed_coefficients`, `period_voltage`, and `gain_field`, with
\(G_1=L_T\) and \(G_3=\mathcal C_T\).
They are not accepted on their floating residuals.  At the full gain box,
the program evaluates the finite-center, finite-interval-remainder, and
analytic-tail pieces of

\[
 \eta_q=
 \|A\{D_x\mathcal F_b(\bar x)\bar s_q
             +\partial_{\kappa_q}\mathcal F_b(\bar x)\}\|_\square
\]

separately and then sums them.  In particular, modes beyond \(M\) are
multiplied coefficientwise by \((2\pi i k)^{-1}\); they are not folded into
the finite residual or discarded.  Each of the three nonnegative pieces is
recorded in the JSON audit.

More precisely, if \(R_q^0(b)\) denotes the residual inside braces, the
finite coordinate restriction is split into a binary midpoint and an
outward interval remainder, while the tail is summed analytically:

\[
\begin{aligned}
 \eta_{q,P}^{\rm ctr}&=\|A_P R_{q,P}^{\rm mid}\|_1
       +E_{\rm Higham},\\
 \eta_{q,P}^{\rm rad}&=a_P\operatorname{rad}_1(R_{q,P}^0(U)),\\
 \eta_{q,Q}&=\sup_{b\in U}\sum_{\ell=v,w}\sum_{|k|>M}
       \frac{|(R_{q,\ell}^0(b))_k|_\diamond}{2\pi|k|},\\
 \eta_q&=\eta_{q,P}^{\rm ctr}+\eta_{q,P}^{\rm rad}+\eta_{q,Q}.
\end{aligned}
\tag{4.0a}
\]

with outward rounding.  A direction-specific Wiener majorant
\(E_q^{\rm var}\) bounds the change from \(\bar x\) to every solution in
the D1 ball.  In particular, the moving-period column is bounded using the
RFDE estimate (3.1), not an operator-norm derivative of a shift on the
unweighted Wiener space.  The sensitivity error is therefore

\[
 \|s_q-\bar s_q\|_\square
 \le
 \frac{\eta_q+E_q^{\rm var}}{1-q_U(r)}.
\tag{4.1}
\]

The following decomposition records exactly what enters
\(E_q^{\rm var}\); it is included so that the sensitivity enclosure is not
hidden inside the implementation.  Put \(\rho=5\times10^{-9}\),
\(\underline T=\bar T-\rho\), \(\overline T=\bar T+\rho\),
let \(\bar T_-\) be the directed lower endpoint of the stored midpoint
period, put \(\sigma=\sqrt2\), and let \(h_1,h_3\) be the two gain
half-widths, meaning
\(h_i=\sup_{b\in U}|\kappa_i-\bar\kappa_i|\); also put
\(\kappa_{i,+}=\sup_{b\in U}|\kappa_i|\).  If
\(V_0=\|\bar v\|\), \(C_0=\|\bar v-1\|\), and
\(C_j=\|S_j(\bar T)\bar v-1\|\), define

\[
 d_j=\sigma\rho+
 \sigma\|\bar v'\|\frac{\tau_j\rho}
                  {\underline T\,\bar T_-},
 \qquad
 \Delta G_1=\frac{d_0+d_1}{2}+\rho,
\tag{4.1a}
\]

and

\[
 \Delta G_3=\frac12\sum_{j=0}^1
 d_j(3C_j^2+3C_jd_j+d_j^2)
 +\rho(3C_0^2+3C_0\rho+\rho^2).
\tag{4.1b}
\]

For the linear and cubic gain fields \(G_1,G_3\), respectively, the fast-field
variation used in (3.1) is

\[
\begin{aligned}
 E_f={}&2\rho+\rho(V_0^2+V_0\rho+\rho^2/3)\\
 &+\varepsilon\{\kappa_{1,+}\Delta G_1+h_1\|G_1(\bar x)\|\}
 +\varepsilon\{\kappa_{3,+}\Delta G_3+h_3\|G_3(\bar x)\|\},\\
 E_{\dot v}={}&
 \rho\frac{\|\bar v'\|+R_V}{\bar T_-}
 +\overline T E_f+R_V.
\end{aligned}
\tag{4.1c}
\]

Here
\[
 R_V=\sup_{b\in U}\|D\bar v-\bar T f_b(\bar x)\|_{\mathcal W}
\tag{4.1c'}
\]
is the directed fast Fourier residual bound at the fixed midpoint.

Let \(a_0,a_j\) be the current and two delayed voltage coefficients in the
bordered derivative.  Direct polynomial subtraction gives

\[
\begin{aligned}
 \Delta a_0={}&\rho(2V_0+\rho)+\varepsilon h_1
 +3\varepsilon\{\kappa_{3,+}\rho(2C_0+\rho)+h_3C_0^2\},\\
 \Delta a_j={}&\frac{\varepsilon}{2}
 \{h_1+3[\kappa_{3,+}d_j(2C_j+d_j)+h_3C_j^2]\}.
\end{aligned}
\tag{4.1d}
\]

Now fix one finite sensitivity candidate
\(\bar s_q=(\bar s_v,\bar s_w,\bar s_T)\).  Set

\[
 \Delta\alpha_j=\frac{\tau_j\rho}{\underline T\,\bar T_-},
 \quad e_{s,j}=\sigma\|\bar s_v'\|\Delta\alpha_j,
 \quad e_{v',j}=\sigma E_{\dot v}
       +\sigma\|\bar v''\|\Delta\alpha_j.
\tag{4.1e}
\]

Here \(G_1=L_T(\bar v)\) and \(G_3=\mathcal C_T(\bar v)\), consistently with
(2.10).

With \(A_i=\sup_{b\in U}\|a_i(\bar x,b)\|\), evaluated by directed
interval arithmetic, the four raw pieces used by the code are

\[
\begin{aligned}
 E_q^{\rm state}={}&\rho\left(A_0\|\bar s_v\|+\|\bar s_w\|
       +\sum_jA_j\sigma\|\bar s_v\|\right)\\
 &+\overline T\left[\Delta a_0\|\bar s_v\|
   +\sum_j\{\Delta a_j\sigma\|\bar s_v\|
                +(A_j+\Delta a_j)e_{s,j}\}\right],\\
 E^{T}={}&E_f+\sum_j\left[
 \Delta\alpha_jA_j\sigma\|\bar v'\|
 +\frac{\tau_j}{\underline T}
   \{\Delta a_j\sigma\|\bar v'\|
          +(A_j+\Delta a_j)e_{v',j}\}\right],\\
 E_q^{\rm slow}={}&\varepsilon\rho\|\bar s_v\|
      +|\bar s_T|\varepsilon\rho,\\
 E_q^{\rm gain}={}&\varepsilon\{\rho\|G_q(\bar x)\|
       +\overline T\Delta G_q\}.
\end{aligned}
\tag{4.1f}
\]

> **Lemma 4.1 (directed sensitivity error).**  Let
> \(a_P\) be the reported finite inverse-norm upper bound and put
> \[
>  a_*=\max\left\{a_P,
>       \frac1{2\pi(M+1)}\right\}.
> \]
> This is the norm bound for the complete finite--tail preconditioner; in
> the tracked instance its first entry is the larger one.  Uniformly
> for \(b\in U\),
> \[
> E_q^{\rm var}=a_*\{E_q^{\rm state}
>       +|\bar s_T|E^T+E_q^{\rm slow}+E_q^{\rm gain}\}
> \tag{4.1g}
> \]
> bounds the preconditioned change between the exact sensitivity equation
> at \(x_b\) and the candidate equation at \(\bar x\).  Consequently (4.1)
> holds, and its right-hand side bounds the exact derivative in Lemma 2.1.

**Proof.**  The exact sensitivity identity is

\[
 D_x\mathcal F_b(x_b)(s_q-\bar s_q)
 =-\{D_x\mathcal F_b(x_b)\bar s_q
             +\partial_{\kappa_q}\mathcal F_b(x_b)\}.
\tag{4.1h}
\]

Equations (4.1a)--(4.1d) are the Wiener product identity
\(u^3-v^3=(u-v)(u^2+uv+v^2)\), the real-shift norm \(\sigma\), and the
reciprocal-period bound.  In (4.1f), the four lines are respectively the
state Jacobian, moving-period column, slow equation, and direct gain
forcing.  Candidate derivatives are finite polynomials, while the unknown
orbit derivative is controlled through the RFDE bound \(E_{\dot v}\); no
\(X^1\) correction ball is assumed.  Splitting the right side of (4.1h)
into the base residual (4.0a) and its change from \(\bar x\) to \(x_b\),
then summing the four majorants and applying the global preconditioner,
gives (4.1g).  These are safe majorants, not a claim that the pieces are
disjoint.  Finally
\(\|I-A D_x\mathcal F_b(x_b)\|\le q_U(r)<1\), so the Neumann inverse gives
(4.1). \(\square\)

The generated JSON records the three pieces of the base preconditioned
residual, \(a_*\), all four pieces of (4.1g), their raw and preconditioned
totals, and the final exact sensitivity error separately for each control
direction.  Its `period_column_variation_upper` field already includes the
factor \(|\bar s_T|\).

The frequency row follows from

\[
 F_{\kappa_q}=-T_{\kappa_q}/T^2.
\]

For the squared voltage range, the unique extrema from D3 make the envelope
identity rigorous:

\[
 (R_h)_{\kappa_q}
 =2(V_+-V_-)\{V_{\kappa_q}(\theta_+)
                 -V_{\kappa_q}(\theta_-)\}.
\tag{4.2}
\]

The midpoint sensitivity polynomials are evaluated on the narrow dyadic
phase brackets and enlarged by (4.1).  This produces an entrywise interval
matrix \(B(U)\).

For the stored binary midpoint \(B_0\), a directed lower bound is obtained
without trusting an SVD:

\[
 s_0=\frac{|\det B_0|}{\|B_0\|_F}
 \le \sigma_{\min}(B_0).
\]

If \(r_B\) is the directed Frobenius radius of \(B(U)-B_0\), the reported
response lower bound is

\[
 \beta_U=s_0-r_B.
\tag{4.3}
\]

Only a positive directed value in (4.3) sets the D4 flag.

## 5. Directed result

The tracked 160-bit run proves the following statement.

> **Theorem 5.1 (microscopic FHN response box).**  For
> \[
> U=[0.199999999999,0.200000000001]
> \times[0.249999999999,0.250000000001],
> \]
> the phase-fixed synchronous FHN coefficient equation has one periodic
> solution in the Wiener ball of radius \(5\times10^{-9}\) about the
> \(129\)-node midpoint polynomial, for every \(b\in U\).  Its bordered
> inverse, as a map from the residual \(\mathcal Y^0\) norm into the base
> \(\mathcal X^0\) Wiener norm, has norm at most \(23.385691\); this is not
> an \(\mathcal X^1\) graph-norm bound.  Every orbit has exactly one voltage
> maximum and one voltage minimum, with no peak switching.  Moreover,
> \[
> D_b(F,R_h)\in
> \begin{pmatrix}
> [0.03669813,0.03670152]&[0.13633291,0.13634601]\\
> [-3.651073,-3.640159]&[-6.157506,-6.115170]
> \end{pmatrix},
> \]
> and
> \[
> \inf_{b\in U}\sigma_{\min}D_b(F,R_h)
> \ge 0.0162187.
> \]

The underlying directed radii margin is
\(2.9708163648\times10^{-9}\).  The maximum and minimum phase brackets have
width at most \(5.97\times10^{-8}\).  Curvature on the corresponding broad
isolation windows satisfies \(V''<-48.8551\) and \(V''>75.0004\),
respectively.  In (4.3), the midpoint lower bound is \(0.0380780707\) and
the response Frobenius radius is at most \(0.0218593434\).

The gain box in the theorem is the exact human-declared decimal box, which
the MPFR intervals in the JSON enclose.  All displayed response endpoints
and numerical bounds above are rounded outward from their longer directed
values in that record.

## 6. Scope and remaining gates

Even though D1, D3, and the response part of D4 are true, issue 15 remains
open.  This certificate does not supply

1. exclusion of the remaining compact Bloch arc, and hence full Floquet
   hyperbolicity;
2. a directed Lipschitz bound for the response derivative, which requires
   validated second sensitivity equations; or
3. the independent controlled-separator/reset constants and final target
   ball.

The JSON flag `derivative_lipschitz_bound_supplied` is therefore forced to
false, and `issue_15_closed` remains false.  An interval response enclosure
must not be divided by the box half-width and relabeled a Lipschitz bound;
that inference is invalid without second-derivative control.

## 7. Reproduction and refusal

From the repository root run

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_periodic_parameter_box.py
```

and test with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_periodic_parameter_box.py
```

The run refuses D1 if either radii inequality in (2.1) fails, D3 if any
complement cell contains zero or either curvature/endpoint test fails, and
D4 if the directed radius in (4.3) is not smaller than \(s_0\).  Diagnostic
binary64 roots, sensitivities, and SVDs never override those refusals.
