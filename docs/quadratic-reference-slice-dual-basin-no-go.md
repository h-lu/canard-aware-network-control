# Dual-basin and permanent-face no-go on the quadratic reference slice

Status: **proved spectral no-go for the synchronous rest state, proved
detector-face recurrence obstruction for periodic capture, and open global
multistability.**  At

\[
 \varepsilon={1\over5},\qquad a={3\over5},\qquad
 (\kappa_1,\kappa_3)=\left({1\over5},{1\over4}\right)
\tag{0.1}
\]

and throughout the validated microscopic gain box, the unique synchronous
equilibrium has two distinct characteristic roots in the open right half-
plane.  The conclusion remains true for \(|\eta|\le10^{-3}\), a much larger
interval than the controlled-transfer bound.  Therefore that rest state is
not a quiet attractor.

On the \(\eta=0\) slice, the validated attracting periodic orbit crosses the
detector faces \(+1\), \(+3/2\), and \(-1\) on every period and lies strictly
above \(-6/5\).  A trajectory captured by this orbit must accordingly leave
each of the one-sided regions used by the handoff theorem.  Thus permanent detector-face no-return is incompatible
with capture by the validated pulse orbit.

This does not exclude a different quiet attractor elsewhere in the RFDE
phase space, nor does it prove that the validated periodic orbit is the
global attractor.  The exact conclusion is a no-go for the conventional
“synchronous rest versus pulse cycle” dual basin and for permanent one-sided
voltage claims, not a global uniqueness theorem.

The executable algebra is in
[quadratic_reference_dual_basin_no_go.py](../src/canard_control/quadratic_reference_dual_basin_no_go.py),
the generator is
[quadratic_reference_dual_basin_no_go.py](../experiments/quadratic_reference_dual_basin_no_go.py),
and hostile tests are in
[test_quadratic_reference_dual_basin_no_go.py](../tests/test_quadratic_reference_dual_basin_no_go.py).

## 1. Plant and meanings of “basin” and “no-return”

On synchrony the quadratic dual-scaffold RFDE is

\[
\begin{aligned}
 \dot v={}&v-{v^3\over3}-w
 +\varepsilon\kappa_1
 \left\{{v(t-\tau_0)+v(t-\tau_1)\over2}-v\right\}\\
 &+\varepsilon\kappa_3
 \left\{{H(v(t-\tau_0))+H(v(t-\tau_1))\over2}-H(v)\right\}\\
 &+\varepsilon\eta\left[(v(t)-1)^2-(v(t-T_*)-1)^2\right],\\
 \dot w={}&\varepsilon(v-a),
 \qquad H(v)=(v-1)^3.
\end{aligned}
\tag{1.1}
\]

A physical basin here means the basin of an attractor of one fixed
autonomous RFDE.  A quiet basin in the standard rest-versus-pulse
interpretation must contain a neighborhood attracted to a stable rest
state.  A lower-dimensional stable set of an unstable equilibrium is not a
quiet basin.

Permanent upper-face no-return at a level \(c\) means that, after a hit, the
physical voltage remains in \(v\ge c\) forever; the lower-face version uses
\(v\le c\).  This is different from a discrete label that remembers a past
hit.  The finite-horizon handoff theorem proves no reversal only until its
terminal face, not either permanent statement.

## 2. The synchronous equilibrium is not a quiet attractor

Every constant synchronous state annihilates all delayed-difference
channels, including the quadratic carrier.  The recovery equation therefore
forces \(v=a\), and then the voltage equation forces
\(w=v-v^3/3\).  Hence the unique synchronous equilibrium is

\[
 (v_e,w_e)=\left({3\over5},{66\over125}\right).
\tag{2.1}
\]

At this state

\[
 f'(v_e)={16\over25},\qquad H'(v_e)={12\over25},
\tag{2.2}
\]

and at the gain center the total delayed-minus-current coefficient is

\[
 C_*={1\over5}\left({1\over5}+{1\over4}{12\over25}\right)
 ={8\over125}.
\tag{2.3}
\]

For \(\eta=0\), the synchronous characteristic determinant is

\[
 \Delta_*(\lambda)=
 \lambda^2-{72\over125}\lambda+{1\over5}
 -{4\over125}\lambda
 \left(e^{-\tau_0\lambda}+e^{-\tau_1\lambda}\right).
\tag{2.4}
\]

### 2.1 Two exact Rouché disks

Remove the delayed term and define

\[
 p(\lambda)=\lambda^2-{72\over125}\lambda+{1\over5}.
\tag{2.5}
\]

Its roots are

\[
 z_\pm={36\over125}\pm i{\sqrt{1829}\over125},
 \qquad |z_\pm|={1\over\sqrt5}.
\tag{2.6}
\]

Let \(D_\pm=\{|\lambda-z_\pm|<1/10\}\).  The disks are disjoint and

\[
 \inf_{D_\pm}\Re\lambda
 ={36\over125}-{1\over10}={47\over250}>0.
\tag{2.7}
\]

On either boundary,

\[
 |p(\lambda)|\ge
 {1\over10}\left({2\sqrt{1829}\over125}-{1\over10}\right)
 =-{1\over100}+{\sqrt{1829}\over625}
 =0.0584268952970\ldots.
\tag{2.8}
\]

The gain box has half-width \(10^{-12}\).  If

\[
 C={1\over5}\left(\kappa_1+{12\over25}\kappa_3\right),
\tag{2.9}
\]

then

\[
 |C-C_*|\le {37\over125\cdot10^{12}}.
\tag{2.10}
\]

The quadratic-channel linearization is

\[
 d_\eta\{x(t)-x(t-T_*)\},
 \qquad d_\eta=-{4\over25}\eta.
\tag{2.11}
\]

For every positive delay, exponentials have modulus at most one on
\(\overline D_\pm\).  Uniformly for the gain box and
\(|\eta|\le10^{-3}\), the difference between the full characteristic
determinant and \(p\) is bounded on either circle by

\[
 \left({4020000000037\over62500000000000}\right)
 \left({1\over\sqrt5}+{1\over10}\right)
 =0.0351967784629\ldots.
\tag{2.12}
\]

The exact Rouché margin is

\[
 {\sqrt{1829}\over625}-{1\over100}
 -{4020000000037\over62500000000000}
  \left({1\over\sqrt5}+{1\over10}\right)
 =0.0232301168342\ldots>0.
\tag{2.13}
\]

> **Theorem 2.1 (uniform synchronous-rest instability).**  For the
> microscopic gain box, \(|\eta|\le10^{-3}\), and arbitrary positive values
> of the three delays, the synchronous characteristic determinant has one
> zero in each disk \(D_+\) and \(D_-\).  In particular it has at least two
> distinct open-right-half-plane roots.

**Proof.**  Each disk contains exactly one zero of \(p\).  Equations
(2.8)--(2.13) give the strict Rouché inequality on both boundaries.  Rouché's
theorem preserves the zero count in each disk.  Equation (2.7) places both
zeros in the open right half-plane. \(\square\)

Every balanced network preserves the synchronous subspace, so these
unstable synchronous roots are also roots of the full-network linearization.
The equilibrium is therefore not a local attractor and cannot furnish the
quiet basin in a rest-versus-pulse theorem.  This conclusion does not assert
that no asynchronous equilibrium, small cycle, chaotic invariant set, or
other quiet attractor exists.

## 3. Periodic capture forbids permanent detector-side residence

On the \(\eta=0\) microscopic gain box, the directed periodic validation
gives

\[
\begin{aligned}
 1.9340632715192051840\ldots
 &<V_{\max}<1.9340645938610316010\ldots,\\
 -1.0133141019114247846\ldots
 &<V_{\min}<-1.0133129515062279318\ldots.
\end{aligned}
\tag{3.1}
\]

Consequently:

- the orbit takes values on both sides of \(+1\), \(+3/2\), and \(-1\);
- the whole orbit lies strictly above \(-6/5\), with lower margin
  \(0.1866858980885752\ldots\).

The periodic-attraction certificate gives local full-network orbital
attraction on every fixed finite admitted Dobrushin network, and its
hyperbolic synchronous source gives asymptotic phase.  If a full-network
trajectory converges to the synchronous periodic orbit with asymptotic
phase, then at the two strictly separated phases in (3.1), every component
eventually inherits the corresponding strict inequality.  Repeating those
phases once per period yields infinitely many visits.

> **Theorem 3.1 (face-recurrence no-go).**  A trajectory captured by the
> validated pulse periodic orbit cannot, after a finite time, remain forever
> above \(+1\) or \(+3/2\), nor forever below \(-1\) or \(-6/5\).  For the
> first three faces the limiting orbit visits both sides infinitely often;
> for \(-6/5\) the limiting orbit lies strictly on the upper side.

This theorem does not weaken the handoff result.  The handoff result asserts
a finite first excursion and finite-horizon no reversal.  Theorem 3.1 says
that upgrading it to permanent physical one-sidedness would contradict the
proposed periodic capture target.

## 4. Exact status of pulse/quiet dual basins

The current certificates support one local pulse basin at \(\eta=0\): an
unspecified neighborhood of the validated synchronous periodic orbit for
each fixed finite network in the Dobrushin class.  They do not provide a
uniform radius or terminal-block containment.

The natural quiet candidate, the synchronous equilibrium, is excluded by
Theorem 2.1.  Therefore the current slice does not support a validated
rest-versus-pulse dual-basin theorem.  A stronger statement—that no other
quiet attractor exists—is open.  No global absorbing set, Morse
decomposition, Conley-index exclusion, or exhaustive equilibrium/periodic-
orbit enumeration has been proved.  It would be incorrect to promote this
local spectral no-go to “the periodic orbit is globally unique.”

## 5. Three repairs and their non-interchangeable meanings

### 5.1 Genuine repair: validate one autonomous bistable slice

This is the only route below that preserves the literal goal of two physical
basins in the same autonomous RFDE.  A parameter box must satisfy all of:

1. zero right-half-plane characteristic roots for a quiet equilibrium,
   including collective and transverse modes;
2. an attracting nonconstant periodic orbit on the same parameter box;
3. two disjoint directed trapping neighborhoods for the two attractors;
4. directed inclusion of the intended terminal histories in the respective
   basins; and
5. either a global separator theorem or an explicitly bounded domain on
   which the basin partition is certified.

The numerical search should continue the equilibrium characteristic roots
and the periodic branch jointly in \((a,\eta,\kappa_1,\kappa_3)\), looking
for an overlap of zero equilibrium unstable index and zero nontranslation
periodic unstable index.  A candidate overlap is only diagnostic.  The final
proof needs an argument-principle/Riesz count for the equilibrium, a directed
Floquet count for the orbit, and radii-polynomial or isolating-block basin
certificates.  No such box has yet been found or validated.

### 5.2 Semantic repair: latch the first event

Introduce a discrete label \(L\in\{0,+,-\}\).  On a transverse first hit of
a predeclared detector during the declared autonomous segment, set
\(L=+\) or \(L=-\) once and never reset it.  Then the label is immutable event memory
even though the physical voltage later recrosses the face.

This is useful for event classification, but the latch is not a physical basin,
not an invariant voltage half-space, and not evidence for a quiet
attractor.  If the trajectory entering the autonomous segment was created by
a branch-selecting controller, the label also does not turn that history
into input-independent physical onset.

### 5.3 Controlled repair: an explicit post-event parameter switch

One may declare a hybrid rule that changes the parameter vector to
\(p_+\) after a positive event and to \(p_-\) after a negative event.  A
valid theorem would need:

1. the switching rule, hysteresis, dwell time, and both post-event slices;
2. a validated target attractor for each slice;
3. inclusion of every allowed switching history in the corresponding target
   basin; and
4. robustness margins for event-time and switching uncertainty.

If completed, this would be policy-dependent hybrid capture.  It would not
be an autonomous dual basin and would not prove input-independent onset.
The switch must appear in the model and theorem statement; hiding it inside
the word “capture” would change the target.

## 6. Claim ledger

The machine certificate proves the unique synchronous equilibrium, two
right-half-plane roots uniformly on the stated gain/\(\eta\) box, the four
directed orbit/face relations, and the resulting incompatibility between
periodic capture and permanent detector-face no-return.  It records that a
latched first-hit label is immutable by definition and specifies validation
contracts for genuine bistability and explicit switching.

It refuses a quiet equilibrium basin, terminal-block basin containment,
global uniqueness of the pulse orbit, exclusion or existence of a different
quiet attractor, completion of any bistable or switched repair, promotion of
an immutable label to a physical basin, and input-independent physical
onset.

Proof-object SHA-256: `6e8bb5f3168d1355e0f2276208105d25802cc0ab68e1c36db9865b9d295436dd`.
