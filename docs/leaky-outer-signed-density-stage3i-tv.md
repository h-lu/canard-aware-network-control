# Stage 3I: continuous signed-density total variation

Stage 3I addresses the remaining linear gap in the outer phase-fixed return:
Stage 3H bounds the two phase-combined adjoint rows, but leaves a reserve of
\(0.01\) for replacing the Stage-2 discrete history shadow by the continuous
reduced-history measure. The present computation encloses that continuous
measure directly. It is a linear statement along the binary center orbit; it
does not construct a nonlinear phase chart, an attracting tube, or a pulse
capture region.

Let \(T\) be the center period, \(t_\delta=T-\delta\), and let
\(r\in[0,\tau_1]\) denote history depth. For every active delay set
\(s_j=\tau_j-r\). Write \(\widehat S(s,t)\) for the Stage-3G candidate
resolvent, \(b_j(s)\) for the scalar delayed coefficient, and

\[
  \alpha(\delta)=\frac{q_v(T-\delta)}{q_v(0)},
  \qquad
  \beta=\frac{q_w(0)}{q_v(0)}.
\]

The denominator \(q_v(0)\) is enclosed strictly away from zero before either
ratio is formed. The voltage-output history density and its recovery atom
are

\[
  k_v(\delta,r)
  =\sum_{j:r\leq\tau_j}
     \left(
       [\widehat S(s_j,t_\delta)]_{vv}
       -\alpha(\delta)[\widehat S(s_j,T)]_{vv}
     \right)b_j(s_j),
\]

\[
  a_v(\delta)
  =[\widehat S(0,t_\delta)]_{vw}
   -\alpha(\delta)[\widehat S(0,T)]_{vw}.
\]

At the recovery output section, the corresponding quantities are

\[
  k_w(r)
  =\sum_{j:r\leq\tau_j}
     \left(
       [\widehat S(s_j,T)]_{wv}
       -\beta[\widehat S(s_j,T)]_{vv}
     \right)b_j(s_j),
\]

\[
  a_w=[\widehat S(0,T)]_{ww}-\beta[\widehat S(0,T)]_{vw}.
\]

Thus the two candidate reduced-history row norms are

\[
  \widehat Q_v
  =\sup_{0\leq\delta\leq\tau_1}
      \left(\int_0^{\tau_1}|k_v(\delta,r)|\,dr+|a_v(\delta)|\right),
  \qquad
  \widehat Q_w
  =\int_0^{\tau_1}|k_w(r)|\,dr+|a_w|.
\]

The order of operations is essential. Within every history cell, both active
delayed injections and the phase-subtraction term are added with their signs
intact; only the resulting scalar interval is replaced by its absolute upper
bound. The atom is not folded into the density integral.

## Directed cell cover

The output offset and history depth are each divided into \(20\times8=160\)
subintervals, hence \(25{,}600\) rectangles for \(k_v\). The binary delays
are locked to \(\tau_0=16h\) and \(\tau_1=20h\). Every requested lag interval
is checked before the expensive sweep to lie in the Stage-3G chart domain
\(0\leq\ell\leq48-d\), where \(d\) is the output-offset mesh cell.

Stage-3G Chebyshev coefficients are treated as exact dyadics and restricted
to each cell by exact rational Chebyshev-to-Bernstein transformations at
192-bit Arb precision. At an integer lag seam, the cell convention is
lower-open and upper-closed: a lower endpoint uses the right chart, whereas
an upper endpoint takes the union of the adjacent one-sided charts. This
covers the essential supremum needed by the integral without interpolating
across an event jump. Cell lengths are multiplied as exact rational fractions
of \(h\), not through binary floating-point round trips.

## One-sided reserve and exact-orbit row budget

For \(x\in\{v,w\}\), let \(Q_x^{(2)}\) be the source-bound Stage-2 shadow
upper bound. The center reserve is the scalar one-sided slack

\[
  E_x^{\mathrm{center}}
  =\max\{0,\widehat Q_x-Q_x^{(2)}\}.
\]

This identity proves
\(\widehat Q_x\leq Q_x^{(2)}+E_x^{\mathrm{center}}\). It is not a bound on
the norm of the difference between the continuous and discrete operators.
The exact target comparison is

\[
  E_v^{\mathrm{center}}<0.01,
  \qquad E_w^{\mathrm{center}}<0.01,
\]

with the decimal \(0.01\) converted directly to Arb rather than first to a
binary float. This is an auxiliary closeness target inherited from the
Stage-3F/3H conditional frontier. It is sufficient but not necessary for
linear contraction once the actual continuous row budgets have been
computed.

The exact-orbit row budget adds the center slack and four further
nonnegative contributions once:

\[
  E_x
  =E_x^{\mathrm{center}}
   +E_x^{\mathrm{direct}}
   +E_x^{\mathrm{orbit}}
   +E_x^{\mathrm{phase}}
   +E_x^{\mathrm{residual/atom}}.
\]

The certified conclusion has the form

\[
  Q_x^{\mathrm{exact}}\leq Q_x^{(2)}+E_x.
\]

Because \(E_x\) contains the one-sided scalar slack
\(E_x^{\mathrm{center}}\), the total \(E_x\) is not a bound on
\(\lVert L_{\mathrm{exact}}-L_{\mathrm{shadow}}\rVert\). Only the explicitly
named Stage-3F/3G contributions in the sum are operator-transfer bounds.

Here the Stage-3H output-specific row sizes control the coefficient-transfer
terms, Stage 3G supplies the candidate-to-guide residual and boundary costs,
and Stage 3F supplies the guide-to-exact-orbit coefficient and phase defects.
The certificate recomputes this ledger from its serialized candidate bounds
and frozen parents, so duplicating or omitting a contribution invalidates the
artifact. The row-budget values \(E_v\) and \(E_w\) are recorded whenever the
continuous integral is validated, even if the \(0.01\) or contraction gate
fails.

The directed sweep does not meet the auxiliary target:

\[
  E_v^{\mathrm{center}}\leq 0.4216206073896348,
  \qquad
  E_w^{\mathrm{center}}\leq 0.025408332707923597.
\]

Nevertheless, after all four exact-orbit transfer contributions are added,

\[
  Q_v^{(2)}+E_v\leq 0.55051563144094195<1,
  \qquad
  Q_w^{(2)}+E_w\leq 0.028280815376548179<1.
\]

These are the two rows of the phase-fixed return on the continuous reduced
history space
\(C([-\tau_1,0],\mathbb R)_v\times\mathbb R_{w(0)}\), with
\(h_v(0)=0\). Hence the actual row gate proves arbitrary-\(C^0\)
reduced-history linear contraction even though the \(0.01\) diagnostic is
false. This is not a contraction theorem on an unreduced ambient
\(C([-\tau_1,0],\mathbb R^2)\) chart. The nonlinear phase chart, outer return
tube, quantitative attraction, pulse capture, and physical onset flags
remain false.
