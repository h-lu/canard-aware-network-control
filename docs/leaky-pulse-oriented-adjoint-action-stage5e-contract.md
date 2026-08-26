# Stage 5E contract: oriented same-row action on the event derivative

Status: **theorem design / OPEN numerical certificate.**  Stage 5D proves a
continuous event-aligned derivative \(D_JK(J)\) on the full pulse interval,
but its total-variation estimate gives only a disk containing zero.  Stage 5E
must retain the signed history and the common adjoint row long enough to
produce a real interval that excludes zero.  It is not, by itself, a stable
graph, stable-gap, interval-Newton, onset, or routing theorem.

## 1. Exact target

Let \(\ell\) be the raw complex Fourier--Grushin row reconstructed as the
Stage-4D atom--density functional, and let \(\widetilde q\) be the exact
Route--C section eigencolumn in the complex Grushin gauge stored by Stage 3.
The stored eigencolumn is **not** itself a real history: it is a common
nonzero complex phase times one.  Let

\[
 \chi(y)=y_v(-3.1724),\qquad
 \gamma=\frac{\chi(\widetilde q)}{|\chi(\widetilde q)|},\qquad
 q_{\rm phys}=\frac{\widetilde q}{\gamma}.
 \tag{1.1}
\]

Stage 3 proves \(|\chi(\widetilde q)|>0\).  Reality of the RFDE and geometric
simplicity of the real unstable multiplier then imply that
\(q_{\rm phys}\) is real, with
\(\chi(q_{\rm phys})=|\chi(\widetilde q)|>0\).  The oriented normalized real
functional is

\[
 f_{\rm phys}(y)
 =\frac{\ell(y)}{\ell(q_{\rm phys})}
 =\gamma\frac{\ell(y)}{\ell(\widetilde q)}.
 \tag{1.2}
\]

For real \(y\), the exact quantity in (1.2) is real.  In contrast, the raw
complex-gauge quotient \(\ell(y)/\ell(\widetilde q)\) is generally **not**
real and must never be assigned an order or sign.  Multiplying \(\ell\) by
any nonzero complex number changes neither (1.2) nor its sign.  The projection
is likewise gauge invariant:

\[
 q_{\rm phys}f_{\rm phys}(y)
 =\widetilde q\,\frac{\ell(y)}{\ell(\widetilde q)}.
 \tag{1.3}
\]

The preferred a posteriori identity is the same one that closes the
Stage-4E correlated \(uu\) block.  Choose a source-bound real center
\(c_*\), form the complete history

\[
 Y_*(J)=D_JK(J)-c_*q_{\rm phys},
 \tag{1.4}
\]

and use

\[
 f_{\rm phys}(D_JK(J))-c_*
 =\frac{\ell(Y_*(J))}{\ell(q_{\rm phys})}.
 \tag{1.5}
\]

If one common directed computation proves

\[
 \sup_{J\in I_J}|\ell(Y_*(J))|\le r_A,
 \qquad |\ell(\widetilde q)|=|\ell(q_{\rm phys})|\ge b_->0,
 \tag{1.6}
\]

then

\[
 f_{\rm phys}(D_JK(I_J))
 \subset I_f:=[c_*-r_A/b_-,c_*+r_A/b_-].
 \tag{1.7}
\]

The oriented action is proved exactly when \(0\notin I_f\).  Separate
modulus estimates for \(\ell(D_JK)\) and \(\ell(q_{\rm phys})\) are forbidden
because they discard the cancellation in (1.4).

## 2. Source-bound parents

The certificate must bind the exact bytes and mathematical sources of:

1. Stage 5B, for the correlated fixed-time fourth-order pulse family and
   fifth-order remainder on all 1152 cells;
2. Stage 5C, for the unique Route--C event graph, its \(10^{-4}\) remainder,
   and the positive speed interval;
3. Stage 5D, for the direct first-variation comparison and the full history
   chain rule;
4. Stage 4D, for the finite Fourier row, summable tail, atom--density
   reconstruction, and nonzero normalization;
5. Stage 4E, for the already validated same-row residual-action machinery;
6. Stage 3, for the complex Grushin eigencolumn \(\widetilde q\), the
   nonzero component \(\chi(\widetilde q)\), and the resulting oriented real
   history \(q_{\rm phys}\).

The current Stage-5D theorem-level inputs are

\[
 T_J\in[336.624302835,456.574093812],
 \qquad \|D_JK\|_Y\le142.200203,
 \tag{2.1}
\]

\[
 D_JK_v(0)=0,\qquad
 D_JK_w(0)\in[-17.350656459,-10.142798861].
 \tag{2.2}
\]

These hulls are sanity bounds, not the representation used in (1.4).

## 3. Correlated event-history representation

For \(J=J_0+h\zeta\), the voltage-history derivative is

\[
 D_JK_v(J)(\theta)
 =h^{-1}\left[
 W_v(T(\zeta)+\theta,\zeta)
 +\dot v(T(\zeta)+\theta,\zeta)T_\zeta(\zeta)
 \right].
 \tag{3.1}
\]

The current recovery coordinate has the analogous formula.  The source must
retain (3.1) on each intersected parameter--time--history cell.  A single
global hull for \(W_v\), \(\dot v\), or \(T_\zeta\) is not admissible.
Specifically:

- the Stage-5B coefficient polynomials remain in \(\zeta\);
- the Stage-5D comparison radius is inserted only after the nominal
  fixed-time derivative has been formed;
- the Stage-5C polynomial event graph and its remainder remain correlated
  with every translated history cell;
- the two summands in (3.1) are added before an absolute value;
- \(D_JK_v(0)=0\) is imposed as the exact differentiated section identity,
  not merely enclosed by a wide interval;
- the history \(c_*q_{\rm phys}\) is subtracted cellwise before the adjoint
  action; the interval construction of \(\gamma\) is retained in this
  subtraction.

The natural representation is a tensor Taylor--Bernstein polynomial in
local time, history position, and \(\zeta\), with exact delay and event seams.
Adaptive subdivision is allowed, but finite sampling is never error
evidence.

## 4. Same-row action and error budget

For the discrete-delay variational equation, write the raw functional on
\(Y=C([-\tau_{\max},0],\mathbb R)\times\mathbb R\) as

\[
 \ell(y)=a_vy_v(0)+a_wy_w(0)
         +\int_{-\tau_{\max}}^0\rho_v(\theta)y_v(\theta)\,d\theta.
 \tag{4.1}
\]

The Route--C section identities give

\[
 D_JK_v(0)=q_{{\rm phys},v}(0)=Y_{*,v}(0)=0
 \tag{4.2}
\]

exactly.  Hence the voltage current atom vanishes identically on the already
deflated history (1.4); it is not discarded by a small numerical estimate.
The current recovery atom and both voltage-density pieces remain and must be
evaluated on the common residual.

The implementation may expose a genuinely disjoint numerical decomposition,
but it must not pretend that nested or overlapping mechanisms are additive.
The present certificate uses two joint outward envelopes:

\[
 r_A=r_{\rm joint,guide}+r_{\rm joint,measure}.
 \tag{4.3}
\]

Here \(r_{\rm joint,guide}\) is the modulus of one common directed action box
that already contains the exact Stage-5B/5D pulse boxes, the Stage-5C event
graph and translation, all delay/history seams, and the stored finite-plus-
Neumann-tail atom--density guide.  The second envelope is

\[
 r_{\rm joint,measure}
 =\|\ell-\ell_0\|\,\|Y_*\|_Y,
\]

using the source-bound Stage-4E complete-measure difference.  The acceptance
arithmetic adds only these two joint envelopes.

The result must additionally carry the following eight-entry **coverage
ledger**.  Its entries identify where each required mechanism is enclosed;
they are nested or overlapping and must not be summed again:

- guide, pulse, event, and seam mechanisms are nested in
  \(r_{\rm joint,guide}\);
- finite-row, tail, orbit/covariance, and rounding mechanisms overlap inside
  \(r_{\rm joint,measure}\).

The validator must independently check
\(r_{\rm joint,guide}\ge\sup|\ell_0(Y_*)|\) and
\(r_{\rm joint,measure}\ge\|\ell-\ell_0\|\|Y_*\|_Y\).

The denominator lower bound \(b_-\) must be recomputed or imported from a
source-bound same-row certificate.  Stage 4E already proves a stronger
complex-gauge Route--C lower bound than the coarse Stage-4D modulus:

\[
 |\ell(\widetilde q)|
 =|\ell(q_{\rm phys})|\ge 0.0004256385267872.
 \tag{4.4}
\]

The source must verify that the definition, section, and Grushin
normalization of \(\widetilde q\) in (4.4) are identical to those used to
construct \(q_{\rm phys}\) in (1.1).  Since \(|\gamma|=1\), the modulus lower
bound is unchanged by this phase correction.  A lower bound from a different
chart is inadmissible.

## 5. Acceptance inequalities

Stage 5E may set the oriented-action **interval-validated** flag to true once
the first two acceptance conditions hold,

\[
 b_->0,\qquad r_A<\infty.
\tag{5.1}
\]

The distinct **excludes-zero** flag is true if and only if

\[
 0\notin[c_*-r_A/b_-,c_*+r_A/b_-].
 \tag{5.2}
\]

Thus existence of the certified real interval is unconditional after the
directed quotient arithmetic closes; only its nonzero orientation is
conditional.  The stable-gap interface must expose these as separate fields.

The result file must expose \(c_*\), both joint envelopes in (4.3), the full
eight-entry coverage ledger, \(b_-\), the quotient radius \(r_A/b_-\), and
the final real interval \(I_f\).  It must also record both the complex-disk
statement and the theorem that the exact quotient is real.

For diagnosis only, the source-bound center replay gives
\(f_{\rm phys}(D_JK)\) near \(-252\).  The earlier value near \(-14\) was the
current-recovery derivative shard, not the normalized unstable coefficient,
and is rejected as a center.  The chosen exact center \(c_*\) is merely a
preconditioner; all uncertainty must enter through (1.6).

## 6. Interface with the stable graph

Even \(0\notin I_f\) is not yet a stable-gap slope.  If Stage 4 supplies

\[
 \|D\psi\|\le L_\psi,\qquad
 \|(I-qf)D_JK\|\le M_s,
 \tag{6.1}
\]

then

\[
 \partial_JH(I_J)
 \subset I_f+[-L_\psi M_s,L_\psi M_s].
 \tag{6.2}
\]

Only exclusion of zero from (6.2) may set the stable-gap derivative flag.
Endpoint gap signs and a strict interval-Newton inclusion are separate
certificates.  Two-sided basin routing and biological onset remain separate
again.

## 7. Mandatory claim ledger

When (5.1) closes, Stage 5E may mark only the following statements true
(with the exclusion statement additionally conditional on (5.2)):

- the Stage-5D event-history derivative is consumed without dropping the
  translation term;
- numerator and denominator use the same adjoint row and normalization;
- the physical-phase normalized action has an oriented real interval, while
  the raw quotient \(\ell(D_JK)/\ell(\widetilde q)\) remains a complex-gauge
  diagnostic only;
- that interval excludes zero, if and only if (5.2) holds.

The following remain null or false until their own inputs exist:

- quantitative inner stable graph;
- stable-gap derivative interval and exclusion;
- stable-gap endpoint signs;
- interval-Newton image and \(J_c\);
- ordinal third-crossing statement;
- physical onset, two-sided routing, and capture;
- frequency--amplitude--safety target radius;
- asynchronous network safety radius.

Hostile tests must reject omission or independent rounding of the event
translation term, the \(c_*q_{\rm phys}\) subtraction, the recovery atom, any
density piece, the finite-row error, the adjoint tail, the denominator error,
the phase interval \(\gamma\), or any seam.  They must also reject promotion
from an action interval to a stable-gap or onset conclusion.
The attacks must refresh the canonical digest and, where relevant, recompute
all downstream scalar fields; rejection may not rely only on a stale hash.
In particular, the validator must reject shrinking either joint envelope
below its ingress inequality and replacing the Stage-4E source-bound
denominator even when the quotient radius and final interval are changed
consistently with the attack.
