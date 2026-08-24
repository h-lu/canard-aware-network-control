# Singular reachable-hull geometry for the fixed-epsilon graph problem

## 1. Scope

This note proves the exact flow geometry that will be used to replace a
rectangular positive-amplitude history-hull estimate by curved barriers.  It
concerns the uncut singular field only.  It does not construct the target
history graph, show that the graph transform is local, or validate a
fixed-\(\varepsilon\) canard root.

In the global canard coordinates

\[
 \sigma=-2X,\qquad d=Y-X^2+\frac12,
\tag{1.1}
\]

the singular planar field \(q_0=(Y-X^2,-X)\) becomes

\[
 \sigma'=1-2d,\qquad d'=\sigma d.
\tag{1.2}
\]

The object required by the later graph validation is a finite backward flow
hull.  The first integral below gives its exact geometry at \(\rho=0\) and a
barrier identity for \(\rho>0\).  It does not reduce the unknown target graph
to one dimension: at positive amplitude the first integral drifts, and the
graph transform recursively samples its own backward flow.

## 2. First integral and real level sets

Define

\[
 J(\sigma,d)=d\exp\!\left(-2d-\frac{\sigma^2}{2}\right).
\tag{2.1}
\]

### Theorem 2.1 (singular energy geometry)

The function \(J\) is a global \(C^\infty\) first integral of (1.2).  Its
real level sets have the following classification.

1. If \(h<0\), the level \(J=h\) is the single open branch
   \[
    d(\sigma;h)=-\frac12W_0\!\left(-2h e^{\sigma^2/2}\right)<0.
   \tag{2.2}
   \]
   Along it \(\sigma'>1\).  Its maximal uncut trajectory is not complete:
   both ends reach infinity in finite flow time.
2. If \(h=0\), the only finite branch is \(d=0\), on which
   \(\sigma(t)=\sigma(0)+t\).  This is the complete singular canard.
3. If \(0<h<1/(2e)\), put
   \[
    L(h)=\sqrt{-2\{1+\log(2h)\}}.
   \tag{2.3}
   \]
   Real points occur precisely for \(|\sigma|\le L(h)\).  The branches
   \[
   \begin{aligned}
    d_0(\sigma;h)&=-\frac12W_0(-2he^{\sigma^2/2})
       \in(0,1/2],\\
    d_{-1}(\sigma;h)&=-\frac12W_{-1}(-2he^{\sigma^2/2})
       \in[1/2,\infty)
   \end{aligned}
   \tag{2.4}
   \]
   meet at \((\pm L(h),1/2)\) and form a simple closed orbit.  The lower
   branch travels from \(-L(h)\) to \(L(h)\); the upper branch travels back.
4. The level \(h=1/(2e)\) is the equilibrium \((0,1/2)\), not a periodic
   orbit.  Levels \(h>1/(2e)\) are empty.

For the normalization (1.1), the canonical trace integral in the earlier
selected-trace construction satisfies

\[
 \mathscr H(X,Y)=\frac e2J(\sigma,d).
\tag{2.5}
\]

Consequently \(\mathscr H=0\), \(J=0\), and \(d=0\) are equivalent.

#### Proof

The derivatives of (2.1) are

\[
 J_\sigma=-\sigma d e^{-2d-\sigma^2/2},\qquad
 J_d=(1-2d)e^{-2d-\sigma^2/2}.
\tag{2.6}
\]

Their pairing with (1.2) vanishes identically.  Solving \(J=h\) gives

\[
 (-2d)e^{-2d}=-2he^{\sigma^2/2},
\]

which yields (2.2) and (2.4).  The function \(d\mapsto de^{-2d}\) is
strictly increasing on \(( -\infty,1/2)\), strictly decreasing on
\((1/2,\infty)\), and has maximum \(1/(2e)\).  This proves the branch and
turning-point assertions.  The signs of \(1-2d\) give the orientations.

On a negative level the flow-time density is

\[
 \frac{dt}{d\sigma}
 =\frac1{1+W_0(-2he^{\sigma^2/2})}.
\tag{2.7}
\]

For sufficiently large \(|\sigma|\), the Lambert term is bounded below by
a positive multiple of \(\sigma^2\); hence (2.7) is
\(O(|\sigma|^{-2})\).  Its integral to either infinite end is finite.  This
proves incompleteness of the uncut negative-level trajectory.  Finally,
substitution of
\(Y=d+\sigma^2/4-1/2\) into the earlier definition
\(\mathscr H=\tfrac12e^{-2Y}d\) proves (2.5).  \(\square\)

The incompleteness in Theorem 2.1 is not in conflict with the frozen graph
operator.  Its \(C^\infty\) slot cutoff produces a bounded complete-field
datum.  The present theorem instead explains why an uncut flow-box must
carry its maximal-existence qualification.

## 3. Flow time and exact delay hulls

On a regular open or lower branch define

\[
 \vartheta_h(\sigma)
 =\int_0^\sigma
   \frac{d\xi}{1+W_0(-2he^{\xi^2/2})}.
\tag{3.1}
\]

Then \(d\vartheta_h/dt=1\).  Thus, in any injective flow-box
\(\Psi(s,h)\) that does not cross a turning point and remains inside the
maximal flow interval,

\[
 \Phi_{q_0}^{-\tau}\Psi(s,h)=\Psi(s-\tau,h).
\tag{3.2}
\]

For a positive closed level, \(s\) instead belongs to
\(\mathbb R/T(h)\mathbb Z\).  At the equilibrium no phase coordinate exists.

### Proposition 3.1 (through-depth-\(m\) hull)

Let \(I=[s_-,s_+]\) and let \(H\) be a set of regular levels.  For an open
branch, suppose \(I-[0,m\Theta_*]\) is compactly contained in one injective
flow-box and in its maximal phase interval.  For a positive closed level
\(h\), instead use its phase map
\(\Psi_h:\mathbb R/T(h)\mathbb Z\to\{J=h\}\).  With

\[
 \mathcal D=\{4,5,\Theta_*\},\qquad \Theta_*=\max\mathcal D,
\]

the through-depth-\(m\) atomic hull on every open branch is

\[
 \bigcup_{\substack{0\le j\le m\\
             \tau_1,\ldots,\tau_j\in\mathcal D}}
 \Psi\!\left(I-\sum_{k=1}^j\tau_k,H\right).
\tag{3.3}
\]

If each backward ODE integration path is also retained, the continuous hull
is

\[
 \boxed{\ \Psi(I-[0,m\Theta_*],H).\ }
\tag{3.4}
\]

For a closed level, the same formulas hold fiberwise after every phase
interval is projected to \(\mathbb R/T(h)\mathbb Z\); no single injective
flow-box is asserted around the full orbit.  The projected hull may be the
entire phase circle.  For an open negative level the formulas are valid only
under the compact-containment hypothesis above.

#### Proof

Equation (3.2) turns each atomic delay into phase translation.  A chain of
at most \(m\) slots gives (3.3).  Each ODE backtrack of length \(\tau\)
contains all translations in \([0,\tau]\).  Minkowski addition of at most
\(m\) copies of \([0,\Theta_*]\) gives \([0,m\Theta_*]\), proving (3.4).
\(\square\)

On the singular canard the phase is exactly \(s=\sigma\), so no chart
qualification is needed.  Starting from \([-5,5]\times\{0\}\),

\[
 \mathcal H_{\le m}^{\rm cont}
 =[-5-m\Theta_*,5]\times\{0\}.
\tag{3.5}
\]

At the pinned horizon,

\[
\begin{aligned}
 7.3970862959520600&<\Theta_*<7.3970863004241961,\\
 -19.794172600848393&<-5-2\Theta_*
 <-19.794172591904120.
\end{aligned}
\tag{3.6}
\]

Hence the exact backward-only depth-two hull has length between
\(24.794172591904120\) and \(24.794172600848393\).  The earlier seed used
the symmetric interval

\[
 [-(5+2\Theta_*),5+2\Theta_*]
\tag{3.7}
\]

as a convenient conservative enclosure.  It is not the exact reachable
set.  The plateau \(|\sigma|\le20\) contains (3.5), with directed minimum
margin greater than \(0.20582739915160\).

## 4. Why a fixed-width tube is not admissible

### Proposition 4.1 (backward normal expansion)

No nonzero constant-width strip \(|d|\le D\) is backward invariant under
the uncut singular field.  Along the canard,

\[
 D_d\bigl[\pi_d\Phi_{q_0}^{-\tau}(\sigma,0)\bigr]
 =\exp\!\left(-\sigma\tau+\frac{\tau^2}{2}\right).
\tag{4.1}
\]

#### Proof

For backward time \(r=-t\), the normal equation is \(d_r=-\sigma d\).
At every \(\sigma<0\), the vector field points outward on both
\(d=D\) and \(d=-D\).  This disproves backward invariance.  Linearizing
about \(d=0\) and using \(\sigma(-r)=\sigma-r\) gives

\[
 \zeta_r=-(\sigma-r)\zeta,
\]

whose solution is (4.1).  \(\square\)

At \(\sigma=-5\) and \(\tau=\Theta_*\), the directed multiplier is larger
than \(8.7940\times10^{27}\).  A fixed normal radius is therefore not merely
qualitatively wrong; it is catastrophically conditioned on the backward
history scale.

The energy coordinate is itself ill conditioned on a long canard segment.
On a regular level branch,

\[
 \frac{\partial d}{\partial h}
 =\frac{e^{2d+\sigma^2/2}}{1-2d}.
\tag{4.2}
\]

At \((\sigma,d)=(20,0)\), this equals
\(e^{200}>7.2259\times10^{86}\).  Moreover, a positive lower branch reaches
\(|\sigma|=20\) only if

\[
 h\le\frac12e^{-201}<2.5456\times10^{-88}.
\tag{4.3}
\]

Thus \((s,h)\) is useful for barriers and analytic estimates, but a uniform
tensor discretization in these coordinates would be badly scaled.  The
plateau \(|d|\le1\) also crosses the turning locus \(d=1/2\).  It cannot be
covered by one monotone Lambert branch.

## 5. The positive-amplitude barrier identity

Write a planar field in Cartesian components as

\[
 Q=q_0+\Delta,\qquad \Delta=(\Delta_X,\Delta_Y).
\tag{5.1}
\]

The induced perturbation in canard coordinates is

\[
 \Delta_\sigma=-2\Delta_X,\qquad
 \Delta_d=\sigma\Delta_X+\Delta_Y.
\tag{5.2}
\]

### Proposition 5.1 (exact perturbed drift and barriers)

Along (5.1),

\[
\boxed{
 \dot J=e^{-2d-\sigma^2/2}
 \{\sigma\Delta_X+(1-2d)\Delta_Y\}.}
\tag{5.3}
\]

For a differentiable curved boundary \(J=j(\sigma)\),

\[
 \mathcal L_Q(J-j)
 =\dot J-j'(\sigma)(1-2d-2\Delta_X).
\tag{5.4}
\]

For backward invariance of a static band \(j_-\le J\le j_+\), the correct
forward-time boundary signs are

\[
 \dot J\le0\quad\hbox{on }J=j_-,\qquad
 \dot J\ge0\quad\hbox{on }J=j_+.
\tag{5.5}
\]

For a moving backward-time tube

\[
 K_r=\{a(r)\le\sigma\le b(r),\ \ell(r)\le J\le u(r)\},
\]

the sufficient inward conditions are

\[
\begin{array}{ll}
 -1+2d+2\Delta_X\ge a'(r)&\text{on }\sigma=a(r),\\
 -1+2d+2\Delta_X\le b'(r)&\text{on }\sigma=b(r),\\
 -\dot J\ge\ell'(r)&\text{on }J=\ell(r),\\
 -\dot J\le u'(r)&\text{on }J=u(r).
\end{array}
\tag{5.6}
\]

These conditions, verified patch by patch away from the equilibrium, imply
finite-time backward containment by the standard first-exit argument.

#### Proof

Substitution of (5.2) into (2.6) cancels the singular terms and gives
(5.3).  Equation (5.4) is the chain rule.  Backward time changes the signs
of both \(\dot J\) and \(\dot\sigma\); evaluating the first-exit direction
on each face gives (5.5)--(5.6).  \(\square\)

On the uncut synchronous graph, \(\Delta_Y=\rho\nu\).  In a cutoff
transition this simplification is invalid: the complete value
\(Q_Y-(-X)\) must be used.  At \((0,1/2)\), \(\nabla J=0\), so a
\(J\)-barrier alone degenerates and must be replaced or supplemented by a
local quadratic patch.

## 6. Causal localization of the graph operator

The barrier geometry yields a one-sided restriction lemma even though it
does not make the fixed point a finite-depth object.

### Lemma 6.1 (preparation-indexed causal-slab restriction)

Fix \(0<d_*<1/2\).  Let
\(j_\pm\in C^1([s_-,s_+])\) satisfy, for every \(\sigma\),

\[
 J(\sigma,-d_*)<j_-(\sigma)<j_+(\sigma)<J(\sigma,d_*).
\tag{6.1}
\]

Define the nonempty compact lower-component tube

\[
 \Omega=\{s_-\le\sigma\le s_+,\ |d|<d_*,\quad
 j_-(\sigma)\le J(\sigma,d)\le j_+(\sigma)\}.
\tag{6.2}
\]

Because \(J_d>0\) on \(|d|<d_*\), (6.1) makes the two faces unique
\(C^1\) graphs inside this component and keeps \(\overline\Omega\) away from
\(|d|=d_*\).  The explicit component restriction is essential: a positive
level of \(J\) also has an upper Lambert branch with \(d>1/2\).

Fix a locally Lipschitz left germ \(Q_-\) on \(\sigma\le s_-\) that admits a
complete locally Lipschitz extension.  Require its interface trace to agree
with every admitted candidate trace, so that adjoining \(Q_-\) to the
candidate produces one
locally Lipschitz autonomous field \(E_-q\), rather than a latched hybrid
flow.  Assume also

\[
 \dot\sigma_{Q_-}\ge0\qquad(\sigma\le s_-),
\tag{6.3}
\]

so that the left region is backward invariant and a trajectory that has
crossed the interface cannot return.  For every candidate scalar field
\(q=Q_X\), combine \(q\) with the known \(Q_Y\).  Assume uniformly over the
candidate set that each candidate field is locally Lipschitz and

\[
 \dot\sigma_Q=-2q\ge\kappa>0
\tag{6.4}
\]

on \(\Omega\), and impose the explicit forward-time Lie-derivative signs

\[
 \mathcal L_Q(J-j_-)\le0\quad\hbox{on }J=j_-(\sigma),\qquad
 \mathcal L_Q(J-j_+)\ge0\quad\hbox{on }J=j_+(\sigma).
\tag{6.5}
\]

Assume also that the left-germ flow exists for every remaining delay time.
Define \(\mathcal T_{\rm loc}q\) from the declared
current slot and the positive-delay slots of this extended field.  Then:

1. every backward slot based in \(\Omega\) remains in \(\Omega\) until it
   crosses the left face, and thereafter lies in the fixed left germ;
2. \(\mathcal T_{\rm loc}q\) at \(\sigma\le s\) depends only on the
   restriction of \(q\) to \(\sigma\le s\) and on \(Q_-\), never on a right
   completion at \(\sigma>s\);
3. two right completions that agree on \(\Omega\) and use the same left germ
   have identical transforms on \(\Omega\); if the localized fixed point is
   unique, their fixed-point restrictions agree there;
4. this conclusion does not identify fixed points constructed from different
   left germs.

#### Proof

For \(y(r)=\Phi_{E_-q}^{-r}u\), (6.4) gives

\[
 \frac{d}{dr}\sigma(y(r))=-\dot\sigma_Q(y(r))\le-\kappa.
\tag{6.6}
\]

Thus a backward characteristic cannot enter a later longitudinal slab and
crosses a slab of width \(w\) in at most \(w/\kappa\).  The barrier
inequalities and the first-exit argument exclude normal escape before the
left face.  Condition (6.3) prevents return after that crossing.  The
interface matching and local Lipschitz regularity make this the flow of one
autonomous field and give uniqueness across the seam.  On this causal hull,
equality of the two fields and ODE uniqueness give equality of every delayed
slot.  Substitution in the graph
operator proves assertions 2 and 3.  The proof holds the left germ fixed and
therefore gives no comparison between different germs.  \(\square\)

At the order-zero existence level, a natural complete metric space is a
closed uniformly Lipschitz ball in
\(C^{0,1}(\overline\Omega_j)\), with fixed incoming trace and the sup metric.
ODE uniqueness and the causal restriction are valid there.  Smooth graph
and parameter jets are a separate step.  Since differentiating
\(q\mapsto\Phi_q\) consumes a spatial derivative, a finite collocation
inverse does not establish a same-space \(C^3\) Newton theorem.  The declared
grade-nine construction must instead be verified on a loss scale, together
with the already reserved cutoff derivatives through order twelve.

If \(\Omega\) is divided into successive slabs and the derivative of the
local transform has diagonal norm \(\lambda_j<1\) on slab \(j\), then

\[
 (I-D_{q_j}\mathcal T_j)^{-1}
 \quad\hbox{has diagonal norm at most}\quad
 \frac1{1-\lambda_j}.
\tag{6.7}
\]

If \(h_j\) is the slab width, the current-slab field perturbation acts on a
backward characteristic for at most \(h_j/\kappa\).  The flow-variation
equation therefore leads to estimates of the form

\[
 \lambda_j\le
 C_j\frac{h_j}{\kappa}e^{L_j^{\rm flow}\Theta_*}.
\tag{6.8}
\]

This explains why finite subdivision can make the diagonal blocks
contractive after the target clock, barrier, and flow constants have been
validated.  It is not a numerical bound for the present candidate.

In general, one delay path can cross several previous slabs.  If
\(P_{j\ell}\) bounds propagation from slab \(\ell\) to slab \(j\), the
correct lower-triangular estimate is

\[
 e_j\le\frac1{1-\lambda_j}
       \sum_{\ell<j}P_{j\ell}e_\ell.
\tag{6.9}
\]

Equations (6.7)--(6.9) are a proof contract, not target estimates.  A finite
slab chain closes a graph relative to its fixed left preparation by forward
substitution.  A first-order product recurrence is justified only after the
incoming datum has been enlarged to carry the complete \(\Theta_*\)-length
history, or after an upper clock bound proves a one-band structure.  An
infinite weighted tail with weights \(w_j>0\) would require

\[
 \sup_j\frac{1}{(1-\lambda_j)w_j}
 \sum_{\ell<j}P_{j\ell}w_\ell<1.
\tag{6.10}
\]

Neither this bound nor the required initial incoming error is supplied by
the Gaussian factor in (5.3).

### Consequence for remote cutoffs

Lemma 6.1 removes every right-completion ambiguity once its hypotheses are
verified.  The left cutoff remains causal input data and may affect every
later slab.  Thus the remote-cutoff problem has two mathematically different
parts:

- right remote cutoff: irrelevant under the clock and barrier hypotheses;
- left remote cutoff: still requires the declared canonical preparation or
  a quantitative propagation/decay theorem.

Neither part may be summarized as unconditional cutoff independence.

There is also a concrete entrance obstruction for the presently frozen
global extension.  In its exterior current-slot region, \(Q_X=0\), hence
\(\dot\sigma=-2Q_X=0\).  The uniform clock condition (6.4) therefore fails
there.  Lemma 6.1 cannot simply be started at the remote zero exterior.  One
must first construct a compatible clock-positive incoming germ or solve the
flat cutoff transition with a separate contraction/weighted-tail argument.

## 7. Consequence for the graph strategy

The exact depth-two hull (3.5) is about \(1.6\) times shorter than the old
symmetric enclosure, but this alone does not remove the graph radius 537.
The graph fixed-point equation recursively evaluates the unknown field along
its own backward flow.  A finite physical delay horizon therefore does not
make the global fixed point a finite-depth object.

A genuine order-of-magnitude reduction requires a new fixed-target local
graph theorem.  Its proof must supply:

1. a finite collection of regular branch patches and a separate center
   patch if the hull approaches \((0,1/2)\);
2. interval bounds for \(\Delta_X,\Delta_Y\) from a two-dimensional graph
   candidate;
3. the longitudinal and energy inequalities (5.6) through every required
   backtrack;
4. a localized residual/inverse theorem, including a bound on dependence on
   the remote cutoff or an extension variable that restores closure; and
5. a posteriori containment of the actual positive-amplitude depth-two
   physical hull in the graph plateau.

Items 1--5 are the next theorem, not conclusions of this note.

## 8. Status ledger

| Statement | Status |
|---|---|
| Smooth signed first integral and relation to \(\mathscr H\) | **Proved** |
| Complete real Lambert-\(W\) branch classification | **Proved** |
| Maximal-flow and turning-point qualifications | **Proved / recorded** |
| Through-depth-\(m\) flow-box hull formula | **Proved conditionally on chart/existence** |
| Exact asymmetric singular depth-two hull and directed endpoints | **Proved / validated** |
| Constant-width backward-tube obstruction and normal multiplier | **Proved** |
| Exact perturbed \(J\)-drift and moving-barrier conditions | **Proved** |
| Preparation-indexed causal-slab restriction and right-completion independence | **Proved under explicit clock/barrier/existence hypotheses** |
| Failure of the causal clock in the frozen zero exterior | **Proved directly** |
| Positive-amplitude graph candidate or \(\Delta\) enclosure | **Open** |
| Instantiated positive-amplitude barriers and depth-two hull | **Open** |
| Target clock, slab contractions and left-tail propagation | **Open** |
| Preparation-independent or left-cutoff-independent graph | **Open** |
| Graph residual/inverse enclosure and fixed point | **Open** |
| Fixed-\(\varepsilon\) complete-history root | **Open** |

## 9. Reproduction

From the repository root run

```sh
PYTHONPATH=src /usr/bin/python3 \
  experiments/fixed_epsilon_singular_reachable_hull.py
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fixed_epsilon_singular_reachable_hull.py
```

The JSON result stores the directed horizon, asymmetric hull, conditioning
bounds, exact formulas, and a strict proved/open claim ledger.  It stores no
Lambert-W point value as proof evidence.
