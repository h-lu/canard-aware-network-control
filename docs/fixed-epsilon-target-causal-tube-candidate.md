# A target-amplitude prepared causal-tube candidate

Status: **binary64 numerical candidate, not a target graph theorem.**  This
note evaluates the physical delayed vector field at

\[
 \rho_*=\frac1{\sqrt5},\qquad \eta=0,
 \qquad \Theta_*=7.3970862981881309.
\]

It produces a two-dimensional prepared solution tube at the target amplitude
and tests its clock, planar embedding, delayed-slot hull, and relation to the
previous clocked-tail operator.  The computation identifies a viable new
phase coordinate, but it uses binary64 point samples and therefore proves no
global injectivity, interval self-map, or fixed graph.

## 1. Why the singular tube is replaced

The clocked-tail calculation showed that the singular slots at
\(s=3\) have negative \(\dot\sigma\) when
\(\rho=1/\sqrt5\).  That calculation did not evaluate an actual target
trajectory.  The present experiment resolves that ambiguity: on the computed
target-amplitude family, the sampled \(\sigma\)-clock ranges from

\[
 -0.8393810940116787
 \quad\hbox{to}\quad
 1.4053267001615291.
\]

It is negative for sampled times between \(2.79\) and \(3\).  Thus replacing
the singular slots by actual numerical slots does not restore the old phase
clock on this operating slice.

There is a second obstruction.  The current states stay inside the old
physical plateau \(-29\leq\sigma\leq21\), \(|d|\leq1\), but delayed states do
not.  In particular, the sampled delay-\(\Theta_*\) normal coordinate reaches
\(-1.5637763796601902\).  The smallest old delayed-slot cutoff weight is only
\(0.3731681245554917\), and the maximum discrepancy between the old
clocked-tail transform and the uncut physical transform on these slots is
\(0.3119607802188851\).  Consequently the family computed below is **not** a
fixed point of the old clocked-tail operator.  A target proof must recenter its
cutoff on the finite-amplitude tube.

## 2. A compatible transverse preparation

We use the finest section-three values

\[
 \nu=0.21256022233963731,
 \qquad q=-0.061579261574946566
\]

from the two-sided binary64 candidate only as an operating anchor.  That
parent calculation explicitly does not construct the selected attracting and
repelling trace bundles, so these numbers are not a validated selected root.

Let \(h_0(t)\), \(t\leq-3\), be its compatible incoming history template.
For \(|\lambda|\leq0.05\), put

\[
 h_\lambda(t)=h_0(t)+\lambda\bigl(b(t+3),1\bigr),
 \tag{2.1}
\]

where

\[
 b(r)=
 \begin{cases}
 0, &r\leq-1,\\
 rS(r+1),&-1<r\leq0,
 \end{cases}
 \tag{2.2}
\]

and \(S\) is the flat smooth step used in the clocked-tail extension.  The
two endpoint identities

\[
 b(0)=0,\qquad b'_-(0)=1
 \tag{2.3}
\]

make the family exactly compatible at \(t=-3\).  Indeed, its current
\(X\)-coordinate and all three delayed \(X\)-coordinates are unchanged there,
whereas the current \(Y\)-coordinate increases by \(\lambda\).  Since the fast
field is affine in current \(Y\), its value increases by exactly
\(\lambda\).  Equation (2.3) adds the same \(\lambda\) to
\(\partial_t h_{\lambda,X}(-3)\).  The slow component is unchanged.  The
recorded binary64 compatibility residual is
\(1.12\times10^{-16}\).

This calculation closes only the first RFDE compatibility condition.  A
\(C_b^3\) planar field constructed from (3.5) generally requires a \(C^4\)
chart.  Across \(t=-3\), that means matching the recursively determined time
jets through order four, together with the mixed \((t,\lambda)\)-jets of total
order at most four.  The present preparation matches only the value and first
time derivative.  It therefore supplies neither a \(C^4\) chart seam nor a
\(C_b^3\) target graph.

This transverse family is materially different from varying the phase shift
\(q\).  At singular order, varying \(q\) merely translates time and therefore
does not supply a transverse planar coordinate; (2.1) does.

## 3. The prepared causal chart

Starting from each history (2.1), we solve the uncut physical delay equation
by the method of steps on \([-3,3]\).  Write the resulting family as

\[
 \Psi(t,\lambda)=u(t,\lambda),
 \qquad
 (t,\lambda)\in[-3-\Theta_*,3]\times[-0.05,0.05],
 \tag{3.1}
\]

where (2.1) defines the portion with \(t\leq-3\).  Every physical delayed slot
has the form

\[
 \Psi(t-4,\lambda),\qquad
 \Psi(t-5,\lambda),\qquad
 \Psi(t-\Theta_*,\lambda).
 \tag{3.2}
\]

Thus the label is preserved and every delayed time is smaller than the
current time.  This is a causal slot representation that was absent from the
singular-slot check; by itself it is not a self-map of any candidate class.

The relation between an exact tube and a local fixed graph is not merely
heuristic.  The following conditional result records it precisely.  Put
\(\tau_{\max}=\max\{4,5,\Theta_*\}\).

### Proposition 3.1 (a complete extension of an embedded solution family)

Let \(U\subset\mathbb R^2\) be open and let
\(\Psi:U\to\mathbb R^2\) be a \(C^2\) embedding.  Write
\(\Omega=\Psi(U)\), which is open.  Choose \(a<b\) and \(r>0\) so that the
compact retained rectangle

\[
 K=[a-\tau_{\max},b]\times[-r,r]\Subset U
 \tag{3.3}
\]

On the smaller current rectangle \(K_0=[a,b]\times[-r,r]\), suppose that
\(\Psi\) is an exact solution family of the physical RFDE:

\[
 \partial_t\Psi(t,\lambda)
 =\mathcal F_{\rm phys}\bigl(
    \Psi(t,\lambda),\Psi(t-4,\lambda),
    \Psi(t-5,\lambda),\Psi(t-\Theta_*,\lambda)
   \bigr).
 \tag{3.4}
\]

The open chart defines

\[
 Q_0=\partial_t\Psi\circ\Psi^{-1}
 \qquad\hbox{on }\Omega.
 \tag{3.5}
\]

Choose \(\chi\in C_c^\infty(\Omega)\) equal to one on an open neighborhood
of \(\Psi(K)\), and define the full-plane field

\[
 \widetilde Q(u)=
 \begin{cases}
  \chi(u)Q_0(u),&u\in\Omega,\\
  0,&u\notin\Omega.
 \end{cases}
 \tag{3.6}
\]

Then \(\widetilde Q\in C_b^1(\mathbb R^2)\), so it is globally Lipschitz and
complete.  For \((t,\lambda)\in K_0\) and
\(0\leq\tau\leq\tau_{\max}\), the whole chart segment
\([t-\tau,t]\times\{\lambda\}\) lies in \(K\).  Hence uniqueness for the
complete field gives the local flow identity

\[
 \Phi_{\widetilde Q}^{-\tau}(\Psi(t,\lambda))
 =\Psi(t-\tau,\lambda).
 \tag{3.7}
\]

Let \(\mathcal T_{\rm phys}\) be the complete-field special-flow transform

\[
 \mathcal T_{\rm phys}(\widetilde Q)(u)
 =\mathcal F_{\rm phys}\bigl(
   u,\Phi_{\widetilde Q}^{-4}u,
   \Phi_{\widetilde Q}^{-5}u,
   \Phi_{\widetilde Q}^{-\Theta_*}u
  \bigr).
\]

Then, only on the smaller current image \(\Psi(K_0)\),

\[
 \mathcal T_{\rm phys}(\widetilde Q)=\widetilde Q.
 \tag{3.8}
\]

If \(\vartheta\) and \(\ell\) denote the two inverse coordinates,
\((\vartheta,\ell)=\Psi^{-1}\), then

\[
 D\vartheta[\widetilde Q]=1,
 \qquad
 D\ell[\widetilde Q]=0
 \tag{3.9}
\]

on the retained agreement neighborhood where \(\chi=1\).  In particular,
\(\ell\) is a local first integral there.  The two functions

\[
 J_-=\ell+r,
 \qquad
 J_+=r-\ell
 \tag{3.10}
\]

are nonnegative on the tube and satisfy

\[
 DJ_-[\widetilde Q]=DJ_+[\widetilde Q]=0.
 \tag{3.11}
\]

Thus the retained portions of the faces \(\ell=\pm r\) are invariant
nonstrict barriers.  This gives neither a strict barrier margin uniform over
neighboring candidate fields nor a candidate-class self-map.

More generally, for an integer \(k\geq1\), \(\Psi\in C^{k+1}\) gives
\(Q_0\in C^k\) and
\(\widetilde Q\in C_b^k\).  In particular, if \(\Psi\in C^4\), then
\(\widetilde Q\in C_b^3\).  No identity outside \(\Psi(K_0)\) follows, and
the proposition does not assert a global fixed point.

**Proof.**  The equal-dimensional embedding is a diffeomorphism from \(U\)
onto open \(\Omega\).  Thus (3.5) is \(C^1\).  Since \(\Psi(K)\) is compact
in \(\Omega\), the stated cutoff exists.  Its support is compactly contained
in \(\Omega\), so extension by zero in (3.6) is \(C_b^1\); bounded first
derivative makes it globally Lipschitz and therefore complete.  On every
retained segment, \(\chi=1\), and
\(s\mapsto\Psi(t+s,\lambda)\) solves
\(\dot u=\widetilde Q(u)\).  Global uniqueness proves (3.7).  Taking
\(\tau=4,5,\Theta_*\) and using (3.4) proves (3.8).  Differentiating the two
inverse-coordinate identities in \(t\) proves (3.9), hence (3.11).  Finally,
one derivative is lost in (3.5), which gives the stated \(C_b^k\) regularity.
\(\square\)

For the computed family below, (3.5) is used only as a candidate definition.
The exact proposition cannot be applied until the embedding, exact-solution,
regularity, compact-containment, and full-segment hypotheses are validated.
In particular, its intrinsic time identity

\[
 \nabla\vartheta\cdot\widetilde Q=1
 \tag{3.12}
\]

is algebraic wherever the chart is invertible.  What remains numerical is the
hypothesis that (3.1) is globally one-to-one with a uniformly bounded inverse.

## 4. Numerical evidence

The computation uses 41 equally spaced transverse labels, 601 current-time
samples, and 1001 samples on the retained time interval.  DOP853 refinements
with maximum steps \(0.04,0.02,0.01\) give successive maximum state changes

\[
 5.9192\times10^{-9},\qquad 2.9088\times10^{-14}.
\]

A centered-difference check of the DDE derivative has maximum residual
\(2.64\times10^{-10}\).  These are discretization diagnostics, not rigorous
error bounds.

The sampled canard-coordinate hulls are:

| slot | \(\sigma_{\min}\) | \(\sigma_{\max}\) | \(d_{\min}\) | \(d_{\max}\) |
|---|---:|---:|---:|---:|
| current | -3.06158 | 3.37455 | -0.927906 | 0.0746501 |
| delay 4 | -7.06158 | -1.07687 | -1.24085 | -0.680007 |
| delay 5 | -8.06158 | -2.08578 | -1.33591 | -0.745338 |
| delay \(\Theta_*\) | -10.4587 | -4.45867 | -1.56378 | -0.893417 |

On the interior transverse grid, the sampled determinant of
\(D_{(t,\lambda)}\Psi\) lies in

\[
 [-3.0225082748203054,-0.11490937642316638].
 \tag{4.1}
\]

The largest sampled \(\|\nabla\vartheta\|\) is
\(6.611895440680889\), and the floating-point residual in (3.12) is at most
\(8.89\times10^{-16}\).  A polygonal sampling of the image boundary has no
strict nonadjacent segment intersection and has signed area
\(0.6112143739562050\).  These observations support a nondegenerate
target-centered chart, but neither pointwise determinants nor a sampled
boundary prove global injectivity.

## 5. Exact next gate

The result changes the target strategy in a concrete way.  The next proof
should not try to repair the \(\sigma\)-clock or enlarge the old symmetric
normal cutoff about \(d=0\).  It should instead use \(t\) as phase and freeze a
cutoff plateau around the curved hull (3.1)--(3.2).

The smallest rigorous gate is:

1. integrate the prepared DDE and its \(\lambda\)-variational equation with
   interval or Taylor-model arithmetic on
   \([-3-\Theta_*,3]\times[-0.05,0.05]\);
2. enclose \(\det D\Psi\) away from zero and certify degree one from an
   interval boundary separation, thereby proving that \(\Psi\) is one-to-one;
3. construct a smooth target-centered plateau containing the complete
   interval hull of the current, 4-, 5-, and \(\Theta_*\)-slots;
4. replace the present first-order-compatible seam by a parameterized
   preparation satisfying the recursive time and mixed compatibility jets
   through total order four;
5. bound the inverse chart, curved-face barriers, flow Lipschitz constants,
   and delayed-slot derivatives needed by the causal Volterra theorem; and
6. repeat uniformly on a nonzero \((\nu,\eta,\Theta)\)-box before attaching
   selected traces, the \(W^{1,p}\) Fredholm problem, or a complete-history
   root argument.

Until these six items are completed, the present object is a reproducible
local causal-graph candidate and a design for the interval proof—not an
actual validated target fixed graph.

## 6. Reproduction

Run

```bash
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_causal_tube_candidate.py
```

The generated JSON records the parent hashes, operating slice, refinement
rows, four slot hulls, both clock diagnostics, sampled chart margins, cutoff
defect, the proved conditional embedding proposition, and a Boolean ledger
that leaves every numerical target-validation gate false.
