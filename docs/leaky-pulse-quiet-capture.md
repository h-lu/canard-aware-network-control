# The physical `J=3/10` pulse enters the quiet basin

Status: **directed complete-history theorem at the declared center
parameters.**  Start from the exact quiet equilibrium history and apply the
voltage current

\[
 u(t)=\begin{cases}3/10,&0\leq t<1,\\0,&t\geq1.\end{cases}
\]

At

\[
 T=161\sqrt5\approx360.0069444
\]

the complete retained history lies strictly inside the large quiet
Razumikhin sublevel:

\[
 \sup_{-5\sqrt5\leq\theta\leq0}
 (z(T+\theta)-E_q)^TP(z(T+\theta)-E_q)<\frac1{125}.
\]

The previously validated large-basin theorem therefore proves convergence
to the quiet equilibrium.  This result proves one quiet-side basin
inclusion.  It does **not** prove an onset, uniqueness of a threshold, a
history-space separator, transversality to the inner stable manifold, or
capture by the outer periodic orbit for a larger pulse.

## Exact causal grid

Write \(s=\sqrt5\) and use the sorted union

\[
 \mathcal G=\{ns/24:n\in\mathbb Z\}
 \cup\{1+ns/24:n\in\mathbb Z\}.
\]

Ordering is decided exactly in \(\mathbb Q(s)\): the sign of
\(A+Bs\) is obtained by integer signs and the comparison of \(A^2\) with
\(5B^2\).  The point \(t=1\) is a grid node, so no cell crosses the jump in
the applied current.  The value assigned at that single time does not alter
the RFDE solution; the implementation uses the forced field on cells to the
left and the released field on cells to the right.

Translation by either delay preserves both node families:

\[
 (o+ns/24)-js=o+(n-24j)s/24,
 \qquad j\in\{4,5\}.
\]

Thus a delayed cell is either wholly in the exact equilibrium history or is
an already completed cell with exactly the same normalized coordinate.
The 7,728-cell calculation contains 192 and 240 initial-history cells for
the two delays, respectively; every later lookup is an exact cell
translation rather than interpolation.

## Taylor guide and P-norm error

On a cell \(I=[t_i,t_{i+1}]\), put
\(u=(t-t_i)/(t_{i+1}-t_i)\).  A degree-24 Taylor polynomial
\(\widehat z_i(u)\) is formed with nearest-rounded 192-bit MPFR arithmetic.
It is only a guide.  The claim-bearing residual

\[
 r_i(u)=F(\widehat z_i(u),
             \widehat v_{i,4}(u),\widehat v_{i,5}(u),u(t))
          -\frac{d}{dt}\widehat z_i(u)
\]

is recomputed with outward rounding.  The maximum recorded residual in the
P norm is below \(1.48\times10^{-36}\).

Let \(e=z-\widehat z_i\) and \(R=\lVert e\rVert_P\).  The current-state
Jacobian is

\[
 A(v)=\begin{pmatrix}
 1-v^2-\epsilon\kappa_1-3\epsilon\kappa_3(v-1)^2&-1\\
 \epsilon&-\epsilon
 \end{pmatrix}.
\]

For the directed voltage tube, the implementation encloses
\(\mu_P(A(v))\) from the two generalized eigenvalues of

\[
 \frac{PA+A^TP}{2}x=\lambda Px.
\]

Convexity of a matrix measure in the scalar current coefficient reduces its
interval maximum to the two endpoints.  The largest value encountered is
less than \(0.607022\).

The coordinate estimate

\[
 |e_v|\leq
 \sqrt{(P^{-1})_{11}}\,\lVert e\rVert_P
 =\sqrt{\frac{p_{22}}{\det P}}\,R
\]

turns each delayed error into a separate forcing.  For
\(j\in\{4,5\}\), its coefficient is bounded by

\[
 b_j=\sqrt{\frac{p_{11}p_{22}}{\det P}}
 \frac{\epsilon}{2}
 \left(\kappa_1+3\kappa_3(\xi_j-1)^2\right),
\]

where \(\xi_j\) ranges over the corresponding delayed guide-and-error
tube.  The cell inequality is therefore

\[
 D^+R(t)\leq\mu_iR(t)+b_{i,4}R_{i,4}
                    +b_{i,5}R_{i,5}+\lVert r_i\rVert_P.
\]

An outward Gronwall step is checked inside a strict self-consistent tube on
every cell.  This includes the exact algebraic enclosure of
\(\alpha=(3/4)^{1/3}\), the rounding jump between consecutive polynomial
centers, both delayed errors, and the pulse discontinuity at one.  The
maximum validated P-error radius is below \(6.03\times10^{-20}\).

## Complete retained-history bound

The left endpoint of the final history is also a grid node:

\[
 T-5\sqrt5=156\sqrt5.
\]

For each of the 240 complete cells in
\([156\sqrt5,161\sqrt5]\), the code forms the degree-48 interval
polynomial

\[
 \widehat V_i(u)
 = (\widehat z_i(u)-E_q)^TP(\widehat z_i(u)-E_q)
\]

and converts its power coefficients to Bernstein form.  The triangle
inequality in the P norm then gives

\[
 \lVert z(t)-E_q\rVert_P
 \leq \sqrt{\sup_{u\in[0,1]}\widehat V_i(u)}+R_i.
\]

Here \(E_q\) is enclosed with the directed 192-bit interval for the exact
root \(\alpha^3=3/4\); it is not replaced by the nearest MPFR guide center.
Thus the terminal Bernstein polynomial includes the final change of center
and the \(2p_{12}xy\) cross term.  The propagated error radius \(R_i\) then
enters through the P-norm triangle inequality, whose square includes the
corresponding guide--error cross term.

The tracked result records

\[
 \sup\widehat V_i<0.006047094,
 \qquad
 \sup V(z)<0.006047094<0.008,
\]

with a strict P-norm margin greater than \(0.01167\) to the basin boundary.
No point samples enter this terminal conclusion.

## Reproduction and claim boundary

Run

```bash
PYTHONPATH=src /usr/bin/python3 experiments/leaky_pulse_quiet_capture.py
```

The result binds the exact pulse-terminal theorem, the large Razumikhin
basin result, the source of its Lyapunov matrix (P), every claim-bearing
source, the arithmetic description, and the complete certificate digest.
Validators reject extra manifest fields, altered parent hashes, changed
runtime or arithmetic records, modified margins or types, or promotion of the
still-open onset and separator claims.
