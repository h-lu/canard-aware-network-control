# Stage 5E: physical-phase action of the event derivative

Status: **directed certificate; the numerical interval and strict-exclusion
flag are recorded in the source-bound JSON result.**  This stage evaluates a
fixed Route-C functional on the Stage-5D event-aligned pulse derivative.  It
does not construct a stable graph or prove a pulse onset.

## 1. The complex Grushin gauge is not a physical orientation

Stage 3 stores an exact eigencolumn \(\widetilde q\) in the normalization of
the complex Grushin problem.  Its 129-mode finite guide has a common complex
phase; it is not itself a real unstable history.  The same is true of the raw
Stage-4D left row.  Therefore

\[
  \frac{\ell(y)}{\ell(\widetilde q)}
\]

is generally complex even when \(y\) is real.  Its real part has no invariant
sign and is not the quantity certified here.

Let \(\chi(y)=y_v(-3.1724)\).  Stage 3 proves
\(|\chi(\widetilde q)|>0\).  Define

\[
 \gamma=\frac{\chi(\widetilde q)}{|\chi(\widetilde q)|},\qquad
 q_{\rm phys}=\frac{\widetilde q}{\gamma},\qquad
 f_{\rm phys}(y)=\gamma\frac{\ell(y)}{\ell(\widetilde q)}.
\]

Because the RFDE is real and the unstable real multiplier is geometrically
simple, \(q_{\rm phys}\) is real and
\(\chi(q_{\rm phys})>0\).  For real \(y\), \(f_{\rm phys}(y)\) is real.  The
projection itself is unchanged:

\[
 q_{\rm phys}f_{\rm phys}(y)
 =\widetilde q\frac{\ell(y)}{\ell(\widetilde q)}.
\]

This phase correction explains the earlier misleading raw quotient with a
large imaginary part.  It also shows why the event-current recovery
derivative, which is near \(-14\), is not the normalized unstable
coefficient.  The source uses the exact residual center \(c_*=-252\).

## 2. Correlated residual calculation

For every \(J\) in the exact Stage-5B interval the source forms

\[
 Y_*(J)=D_JK(J)-c_*q_{\rm phys}
\]

before applying the common adjoint row.  The calculation covers the
normalized pulse parameter with 128 closed intervals and partitions both
pieces of the delay history into 256 closed intervals each.  Every operation
uses 192-bit outward MPFR arithmetic.  These are interval covers, not sample
points.

On each box the source retains

\[
 D_JK_v(\theta)
 =h^{-1}\left[W_v(T+\theta,\xi)
              +F_v(z_{T+\theta})T_\xi\right],
 \qquad
 T_\xi=-\frac{W_v(T,\xi)}{F_v(z_T)}.
\]

Thus the fixed-time sensitivity and event translation are added before the
residual is bounded.  The Stage-5D comparison radius is inserted only after
the nominal parameter derivative is formed.  The recovery atom, both delay
density pieces, the finite Fourier row, the full Neumann tail, the event and
delay seams, and the Stage-5C \(10^{-4}\) event-graph remainder all remain in
the same calculation.  The voltage current atom vanishes by the exact
differentiated section identity for both \(D_JK\) and \(q_{\rm phys}\).

The recreated finite-plus-tail atom-density guide gives one directed complex
box for \(\ell_0(Y_*)\).  Stage 4E supplies a source-bound operator-norm
enclosure of \(\ell-\ell_0\), including finite-row, adjoint-tail, periodic
orbit, covariance, convolution, and rounding errors.  It acts on the already
deflated history norm; numerator and denominator are never rounded
independently.

The numerical acceptance budget therefore has exactly two additive joint
envelopes: the common guide-action disk and the complete-measure-difference
bound times \(\|Y_*\|_Y\).  An eight-entry coverage ledger records guide,
pulse, event, row, tail, orbit/covariance, seam, and rounding mechanisms, but
those entries are nested or overlapping and are not falsely added as eight
independent radii.  The validator recomputes both ingress inequalities and
the two-envelope sum.

## 3. What the result proves

With the Stage-4E same-row lower bound

\[
 |\ell(\widetilde q)|=|\ell(q_{\rm phys})|
 \ge 0.0004256385267872,
\]

the JSON result records a residual modulus \(r_A\), the quotient radius
\(r_A/b_-\), and

\[
 f_{\rm phys}(D_JK(I_J))
 \subset[c_*-r_A/b_-,c_*+r_A/b_-].
\]

The claim ledger always records the directed action interval once the
quotient arithmetic closes, and sets a separate exclusion flag exactly when
this interval excludes zero.  Regardless of that exclusion flag, all quantitative stable
graph, stable-gap, endpoint-sign, interval-Newton, \(J_c\), crossing ordinal,
physical-onset, routing, capture, and network-safety flags remain false or
null.  Those require separate certificates.
