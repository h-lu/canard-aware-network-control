# A bounded clocked-tail extension for the fixed-epsilon graph problem

## 1. Scope and proof status

The zero exterior in the earlier
[frozen graph operator](fixed-epsilon-frozen-graph-operator.md) makes the
global vector fields bounded and complete, but it also gives
\(Q_X=0\), hence \(\dot\sigma=-2Q_X=0\), outside the cutoff.  A backward
characteristic can therefore stop advancing in the canard phase, and the
causal-slab argument in the
[singular reachable-hull note](fixed-epsilon-singular-reachable-hull.md)
cannot start there.

This note replaces that zero exterior by a bounded complete field whose
canard phase is strictly increasing at every finite point.  It proves:

1. the smoothness, boundedness, completeness, and exact canard-coordinate
   dynamics of the new tail;
2. the cutoff and slot algebra of the extended graph operator;
3. an exact, parameter-independent incoming self-map at \(\sigma=-30\);
4. the explicit and unique graph fixed point at \(\rho=0\);
5. the first \(\rho\)-derivative of the transform on the declared singular
   phase slots;
6. a unique full-plane \(C_b^3\) graph family in a non-explicit
   \(O(|\rho|)\) contraction neighborhood for sufficiently small
   \(|\rho|\); and
7. a separate planar preparation realizing the field/jet clause of the
   fixed-window seed.

It also proves an abstract, preparation-indexed Volterra--Weissinger fixed
point theorem.  That theorem is retained as a target-amplitude causal route,
but it is not applied at \(\rho_*=1/\sqrt5\): the required target self-map,
clock, barrier, flow, and slot estimates have not been established.  In
particular, this note does not validate a target graph or history hull,
construct trace pairs, prove a complete-history root, lift the result to a
general network, or establish biological pulse controllability.

The longitudinal radius \(537\) from the old theorem-native nesting estimate
is not reused.  Its nesting inclusions were never validated at the target.
The number \(64\) below instead defines a bounded clock profile; it is not a
claim about a target reachable hull.

## 2. Canard coordinates and a bounded positive clock

Use the global polynomial coordinates

\[
 \sigma=-2X,\qquad d=Y-X^2+\frac12,
\tag{2.1}
\]

and let \(c:[0,\infty)\to[0,1]\) be the flat radial cutoff

\[
 c(r)=
 \begin{cases}
 1,&0\le r\le1,\\
 \displaystyle
 \frac{e^{-1/(2-r)}}
 {e^{-1/(r-1)}+e^{-1/(2-r)}},&1<r<2,\\
 0,&r\ge2.
 \end{cases}
\tag{2.2}
\]

For \(R=64\), define

\[
 v_R(\sigma)=
 \begin{cases}
 1,&r\le1,\\
 c(r)+\dfrac{1-c(r)}r,&1<r<2,\\
 \dfrac1r,&r\ge2,
 \end{cases}
 \qquad r=\frac{|\sigma|}{R},
\tag{2.3}
\]

and

\[
 Q_v(X,Y)=\left(-\frac{v_R(\sigma)}2,
                    \frac{\sigma v_R(\sigma)}2\right).
\tag{2.4}
\]

The threshold \(|\sigma|=128\) is the beginning of the explicit far-field
formula \(v_R=64/|\sigma|\); it is not a support boundary.

### Proposition 2.1 (bounded complete clocked tail)

The field \(Q_v\) belongs to \(C_b^\infty(\mathbb R^2,\mathbb R^2)\), and

\[
 |Q_{v,X}|\le\frac12,\qquad |Q_{v,Y}|\le64.
\tag{2.5}
\]

Every maximal solution is defined for all positive and negative times.  In
the coordinates (2.1),

\[
 \dot\sigma=v_R(\sigma)>0,\qquad \dot d=0.
\tag{2.6}
\]

The positivity in (2.6) is pointwise.  Globally,
\(\inf_{\sigma\in\mathbb R}v_R(\sigma)=0\), so (2.6) does not supply a
uniform target clock bound on a noncompact set.

#### Proof

Flatness of \(c\) at one and two makes the three formulas in (2.3) agree to
all orders.  Reflection through \(\sigma=0\) causes no loss of smoothness
because \(v_R\equiv1\) near zero.  Thus \(v_R\in C^\infty\), with
\(0<v_R\le1\).  On \(1<r<2\),

\[
 |\sigma|v_R=64\{rc(r)+1-c(r)\}\le128,
\]

while this product is at most \(64\) for \(r\le1\) and equals \(64\) for
\(r\ge2\).  This proves (2.5).  Outside the two compact transition
intervals, the components are either constant or proportional to
\(|\sigma|^{-1}\); all their derivatives are bounded.  Hence
\(Q_v\in C_b^\infty\).

Substitution of (2.4) into the derivative of (2.1) gives (2.6).  Since
\(d\) is constant, completeness reduces to the scalar clock equation.  For
\(|\sigma|\ge128\),

\[
 \frac{dt}{d\sigma}=\frac1{v_R(\sigma)}
 =\frac{|\sigma|}{64}.
\]

Its integral diverges at both infinite ends.  A trajectory therefore cannot
reach either end in finite time, proving two-sided completeness. \(\square\)

The unbounded affine germ \((-1/2,-X)\) would give the simpler identities
\(\dot\sigma=1\), \(\dot d=0\), but it is not a \(C_b\) field.  The profile
(2.3) preserves the same unit clock on the whole cutoff support while
remaining bounded.

## 3. Cutoff and the extended slot operator

Let

\[
 S(z)=
 \begin{cases}
 0,&z\le0,\\
 \displaystyle
 \frac{e^{-1/z}}{e^{-1/z}+e^{-1/(1-z)}},&0<z<1,\\
 1,&z\ge1,
 \end{cases}
\tag{3.1}
\]

and set

\[
 a(\sigma)=S(\sigma+30)S(22-\sigma),\qquad
 w(\sigma,d)=a(\sigma)c(|d|).
\tag{3.2}
\]

Then \(a=0\) on \(( -\infty,-30]\cup[22,\infty)\), and \(a=1\) on
\([-29,21]\).  The normal factor is one for \(|d|\le1\) and zero for
\(|d|\ge2\).  Consequently every point with \(w\ne0\) has
\(|\sigma|<64\), where \(v_R=1\).

### Lemma 3.1 (cutoff regularity)

The functions \(a\) and \(w\) are \(C^\infty\), take values in \([0,1]\),
and have bounded derivatives of every finite order.  Their plateau and
exterior sets are exactly as stated above.

#### Proof

The standard exponential germs in (2.2) and (3.1) are flat at every joining
endpoint.  Products and composition with the polynomial coordinates (2.1)
preserve smoothness.  All nonconstant derivatives are supported where
\(-30<\sigma<-29\), \(21<\sigma<22\), or \(1<|d|<2\); on this set the
polynomial coordinate factors that enter a fixed derivative are bounded.
The range and plateau assertions follow directly from (2.2), (3.1), and
(3.2). \(\square\)

The zero-amplitude base field is

\[
 B=Q_v+w(q_0-Q_v),\qquad q_0=(Y-X^2,-X).
\tag{3.3}
\]

Writing \(w_0=w(\sigma,d)\), the identity \(v_R=1\) on the support of
\(w_0\) gives the global formulas

\[
 B_X=-\frac{v_0}{2}+w_0d,\qquad
 B_Y=\frac{\sigma v_0}{2},
\tag{3.4}
\]

and hence

\[
 \dot\sigma=v_0-2w_0d,\qquad
 \dot d=\sigma w_0d.
\tag{3.5}
\]

The perturbation \(w(q_0-Q_v)\) is smooth and compactly supported.  Hence
\(B\in C_b^\infty\); boundedness and local Lipschitz regularity imply that
its flow is complete in both time directions.

Here and below \(v_j=v_R(\sigma_j)\).  The tail \(Q_v\) preserves every
level of \(d\); the interpolated field \(B\) preserves \(d=0\), not every
level of \(d\).

The pointwise positive clock of the tail must not be transferred to the
base field without an estimate.  On the unit plateau, (3.5) reads
\(\dot\sigma=1-2d\), which vanishes at \(d=1/2\) and is negative above it.
Thus even at \(\rho=0\), a causal Lambert component needs an upper bound
\(d<d_+<1/2\).  This clock condition is distinct from the symmetric
\(|d|\le1\) condition that makes the chosen normal cutoff equal to one.

For current, delay-four, delay-five, and delay-\(\Theta_*\) slots write
\(u_j=(X_j,Y_j)\) and \(w_j=w(u_j)\), with \(X_0=X\).  Define

\[
\begin{aligned}
 \mathcal T_X={}&-\frac{v_0}{2}+w_0d
 -\rho w_0\frac{X^3}{3}\\
 &+\frac{\rho w_0w_4w_5}{5}
   \left(\frac{X_4+X_5}{2}-X\right)\\
 &+\rho^2\eta w_0w_\Theta(X^2-X_\Theta^2)\\
 &+\frac{\rho^3w_0w_4w_5}{4}
   \left(\frac{X_4^3+X_5^3}{2}-X^3\right),\\
 \mathcal T_Y={}&\frac{\sigma v_0}{2}+\rho\nu w_0.
\end{aligned}
\tag{3.6}
\]

The active slot sets are respectively \(\{0\}\) for the base, local cubic,
and slow-unfolding terms, \(\{0,4,5\}\) for both delay-four/five terms,
and \(\{0,\Theta_*\}\) for the \(\eta\)-term.  In particular,
\(\Theta_*\) is inactive in the value equation when \(\eta=0\).  The
factor \(w_0\) on \(\rho\nu\) is essential for the incoming identity below.

### Proposition 3.2 (plateau agreement and fixed exterior)

If every slot active in a term of (3.6) lies in the unit plateau, that term
is exactly the corresponding term of the uncut physical graph operator.
If \(w_0=0\), then

\[
 \mathcal T(u_0,u_4,u_5,u_\Theta;\rho,\nu,\eta)=Q_v(u_0)
\tag{3.7}
\]

for every choice of delayed slots and parameters.  Thus the class of
candidate fields fixed to \(Q_v\) on \(w=0\) is preserved by the slot
operator.  The joins at \(\sigma=-30\) and \(\sigma=22\) match to all
orders.

#### Proof

On the unit plateau all relevant weights equal one and \(v_0=1\), so direct
substitution in (3.6) gives the uncut operator term by term.  If \(w_0=0\),
every physical, delayed, and slow-unfolding channel vanishes, leaving
(3.7).  All-order matching follows from the flatness of \(S\). \(\square\)

Bounded uniformly Lipschitz scalar candidates with this fixed exterior
produce bounded complete planar fields after adjoining the known
\(Y\)-component.  This fact makes every finite backward slot meaningful.
It does not show that a chosen positive-amplitude candidate class is mapped
into itself.

## 4. Incoming self-map and the zero-amplitude fixed point

Let

\[
 \Gamma(\sigma,d)=
 \left(-\frac\sigma2,\frac{\sigma^2}{4}-\frac12+d\right).
\tag{4.1}
\]

### Proposition 4.1 (exact incoming trace)

For every finite \(d\), all delayed slots, and all \((\rho,\nu,\eta)\),

\[
 \mathcal T\bigl(\Gamma(-30,d),u_4,u_5,u_\Theta;
                  \rho,\nu,\eta\bigr)
 =Q_v(\Gamma(-30,d))=\left(-\frac12,-15\right).
\tag{4.2}
\]

Thus the left trace is a parameter-independent self-map identity.  Every
positive parameter derivative and every \(d\)-derivative of this trace
vanishes.

#### Proof

At \(\sigma=-30\), the flat step in (3.2) gives \(w_0=0\), whereas
\(v_R(-30)=1\).  Equation (4.2) follows from (3.7).  The right-hand side has
no dependence on the listed variables, proving the derivative statements.
\(\square\)

This identity fixes an incoming preparation for a causal construction.  It
does not prove that fixed points obtained from different left preparations
coincide.

The prepared tail also has unit speed throughout one maximal delay behind
the interface, since

\[
 -30-\Theta_*>-37.397086301>-64.
\tag{4.3}
\]

This is a property of the fixed incoming tail, not a retained-hull estimate
for an unknown positive-amplitude graph.

### Proposition 4.2 (the graph at \(\rho=0\))

At \(\rho=0\), the graph transform is independent of its candidate and has
the unique fixed point \(B\) in (3.3).  Its Fréchet derivative with respect
to the graph candidate is zero.  The orbit \(d=0\) is complete; on
\(-21\le\sigma\le21\) it satisfies

\[
 \dot\sigma=1,\qquad
 B(\Gamma(\sigma,0))=q_0(\Gamma(\sigma,0)).
\tag{4.4}
\]

#### Proof

Every candidate-dependent delayed term in (3.6) contains a positive power
of \(\rho\).  At \(\rho=0\), (3.6) is therefore the constant map with value
\(B\), proving existence, uniqueness, and the zero derivative.  Equation
(3.5) makes \(d=0\) invariant and reduces its phase equation to
\(\dot\sigma=v_R(\sigma)\).  Proposition 2.1 gives completeness.  On the
declared interval \(v_R=w=1\), which gives (4.4). \(\square\)

For \(s\in[-21,21]\) and
\(\tau\in\{0,4,5,\Theta_*\}\), the smallest slot phase is

\[
 -21-\Theta_*>-28.397086301>-29,
\tag{4.5}
\]

and the largest is \(21\).  Hence every singular slot
\(\Gamma(s-\tau,0)\) lies in the unit plateau.

### Proposition 4.3 (declared-window transform jet)

On the singular slots from (4.5),

\[
 \left.\partial_\rho\mathcal T
 \bigl(\Gamma(s,0),\Gamma(s-4,0),\Gamma(s-5,0),
       \Gamma(s-\Theta_*,0);\rho,\nu,\eta\bigr)
 \right|_{\rho=0}
 =\left(\frac{s^3}{24}+\frac9{20},\nu\right).
\tag{4.6}
\]

#### Proof

All slot weights in (4.6) equal one.  Since
\(X=-s/2\), \(X_4=-s/2+2\), and \(X_5=-s/2+5/2\),

\[
 -\frac{X^3}{3}=\frac{s^3}{24},\qquad
 \frac15\left(\frac{X_4+X_5}{2}-X\right)=\frac9{20}.
\]

The \(\eta\)- and cubic-delay terms have orders \(\rho^2\) and \(\rho^3\),
while \(\partial_\rho\mathcal T_Y|_{\rho=0}=\nu\).  This proves (4.6).
\(\square\)

Equation (4.6) is an exact derivative of the slot transform.  If a
differentiable positive-\(\rho\) fixed-point family is subsequently proved,
then \(D_q\mathcal T|_{\rho=0}=0\) makes (4.6) its first graph jet.  Such a
family is supplied for sufficiently small \(|\rho|\) by the next theorem.

## 5. The full-plane graph for non-explicit small amplitude

Fix one \(\Theta_*\) in the pinned interval and a compact parameter box

\[
 \mathcal P=[-\nu_*,\nu_*]\times[-\eta_*,\eta_*].
\tag{5.1}
\]

For a complete candidate field \(Q\), put
\(u_\tau=\Phi_Q^{-\tau}(u)\) and evaluate the weights and Cartesian
coordinates of Section 3 at these slots.  The graph transform can be written
exactly as

\[
 \mathcal T_{\rho,\nu,\eta}(Q)
 =B+\rho\widehat F(\mathcal E_Q;\rho,\nu,\eta),
\tag{5.2}
\]

where \(\mathcal E_Q=(u,u_4,u_5,u_{\Theta_*})\) and

\[
\begin{aligned}
 \widehat F_X={}&-w_0\frac{X^3}{3}
 +\frac{w_0w_4w_5}{5}
   \left(\frac{X_4+X_5}{2}-X\right)\\
 &+\rho\eta w_0w_\Theta(X^2-X_\Theta^2)\\
 &+\frac{\rho^2w_0w_4w_5}{4}
   \left(\frac{X_4^3+X_5^3}{2}-X^3\right),\\
 \widehat F_Y={}&\nu w_0.
\end{aligned}
\tag{5.3}
\]

### Theorem 5.1 (small-amplitude clocked-tail graph)

There is a non-explicit \(\rho_0>0\), uniform for
\((\nu,\eta)\in\mathcal P\), such that for \(|\rho|\le\rho_0\) the transform
(5.2) has a fixed point

\[
 Q_{\rho,\nu,\eta}\in
 C_b^3(\mathbb R^2,\mathbb R^2)
\tag{5.4}
\]

in the declared contraction class about \(B\).  It is the unique fixed
point in that \(O(|\rho|)\) class and satisfies

\[
 \|Q_{\rho,\nu,\eta}-B\|_{C_b^1}
 \le C|\rho|.
\tag{5.5}
\]

The family is \(C^3\) in \(\rho\), with values in \(C_b^3\), and its mixed
spatial/\((\rho,\eta)\) derivatives have the finite-scale bounds of
[the mixed-jet graph theorem](mixed-jet-graph-proof.md).  In particular,

\[
 Q_{\rho,\nu,\eta}
 =B+\rho Q_1(\nu)+\rho^2Q_2(\nu,\eta)
   +O_{C_b^3}(|\rho|^3).
\tag{5.6}
\]

No uniqueness among fixed points outside the stated \(O(|\rho|)\)
contraction neighborhood is asserted.

The cited mixed-jet theorem literally treats one distinguished auxiliary
parameter through order two.  Here \(\eta\) is distinguished and \(\nu\) is
kept in a passive compact box; the names can be exchanged if \(\nu\)-jets
are required instead.  This statement does not assert a full joint
\((\nu,\eta,\Theta)\) rectangular jet family, and \(\Theta_*\) is fixed.
For the passive use of \(\nu\), take every invariant-ball and fiber norm
uniformly over its compact box; \(\nu\) is never differentiated, and the
uniform \(C_b^R\) data bounds give the same contraction constants.  At
physical \(\eta=0\), applying the theorem again with \(\nu\) as the
distinguished parameter gives the joint \(C^1(\rho,\nu)\) regularity needed
for the field/jet statement below.  Local fixed-point uniqueness identifies
the two parameterized constructions as the same graph family.

#### Proof

Lemma 3.1 and Proposition 2.1 give
\(B\in C_b^\infty\).  Every polynomial state factor in (5.3) is multiplied
by all the current or delayed slot weights on which it depends.  Those
weights localize the corresponding variables to a compact set.  Therefore
\(\widehat F\), including all state and
\((\rho,\nu,\eta)\)-derivatives, belongs to \(C_b^\infty\) on an open
parameter neighborhood of
\([ -\rho_*,\rho_*]\times\mathcal P\) after enlarging the box slightly.

Every field in a bounded \(C_b^1\) ball about \(B\) is bounded and globally
Lipschitz, hence has a complete two-sided flow.  Candidate dependence in
(5.2) occurs only through the strictly positive delays
\(4,5,\Theta_*\), and all of it carries the displayed external factor
\(\rho\).  Formula (5.3) is polynomial in \(\rho\), so it provides the
negative-\(\rho\) extension required for a two-sided Taylor theorem.

Thus the bounded-cutoff hypotheses of the
[special-flow graph theorem](special-flow-graph-theorem.md) hold with
base field \(B\), no stable fiber, and \(\nu\) treated as a passive compact
parameter.  Its contraction argument gives a non-explicit \(\rho_0\), the
fixed point, (5.5), and uniqueness in the contraction neighborhood.  The
zero-dimensional stable fiber is only a notational convention.  If one
requires a positive-dimensional fiber, adjoin a dummy variable with
\(A=-1\) and \(G=0\); its unique graph is \(H=0\), and the reduced operator
(5.2) is unchanged.  The
finite-scale theorem in
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md) applies because the
data are \(C_b^\infty\), hence satisfy its \(R\ge12\) requirement.  It gives
the claimed \(C_b^3\) mixed regularity and (5.6). \(\square\)

### Corollary 5.2 (actual first graph jet on the declared window)

For \(-21\le s\le21\),

\[
 \left.\partial_\rho
 Q_{\rho,\nu,\eta}(\Gamma(s,0))\right|_{\rho=0}
 =\left(\frac{s^3}{24}+\frac9{20},\nu\right).
\tag{5.7}
\]

#### Proof

At \(\rho=0\), the fixed point is \(B\) and
\(D_Q\mathcal T_{0,\nu,\eta}=0\).  Differentiating the fixed-point identity
therefore identifies \(Q_1\) with the transform derivative.  Moreover,
on the declared slots,

\[
 \Phi_B^{-\tau}\Gamma(s,0)=\Gamma(s-\tau,0),
 \qquad \tau\in\{4,5,\Theta_*\},
\]

because \(d=0\) is invariant and \(v_R=w=1\) throughout every intervening
phase segment.  Proposition 4.3 now gives (5.7). \(\square\)

Theorem 5.1 is a genuine small-amplitude graph theorem on the frozen
full-plane cutoff.  Its radius is non-explicit and is not known to contain
\(\rho_*=1/\sqrt5\).  It supplies neither target-amplitude causal geometry
nor cutoff/preparation independence.

## 6. A planar preparation realizing the fixed-window seed jet

Let \(\chi_{\rm plan}\) be the even septic cutoff from the
[fixed-window seed](fixed-window-prepared-gap-seed.md): it is one on
\(|\sigma|\le20\), zero on \(|\sigma|\ge21\), and \(C^3\) across the two
transition intervals.  For the graph family in Theorem 5.1 define

\[
 Q^{\rm pr}_{\rho,\nu,\eta}
 =q_0+\chi_{\rm plan}(\sigma)
       (Q_{\rho,\nu,\eta}-B).
\tag{6.1}
\]

Because both graph fields equal the fixed tail on \(w=0\), their difference
is supported in the bounded graph-cutoff region.  Hence (6.1) is a
well-defined full-plane \(C^3\) field.  If one starts instead from the graph
restricted to \(|d|\le1\), the Seeley normal extension \(E_\perp\) in the
[frozen-operator note](fixed-epsilon-frozen-graph-operator.md) may be used:

\[
 Q^{\rm pr}=q_0+\chi_{\rm plan}
 E_\perp\bigl[(Q_{\rho,\nu,\eta}-B)|_{|d|\le1}\bigr].
\tag{6.2}
\]

Both versions agree on the singular orbit.

### Proposition 6.1 (realization of the seed field/jet datum)

The preparation (6.1) satisfies

\[
 Q^{\rm pr}_{0,\nu,\eta}=q_0,
\qquad
 \left.\partial_\rho
 Q^{\rm pr}_{\rho,\nu,0}(\Gamma(s,0))\right|_{\rho=0}
 =f_\chi(s;\nu),
\tag{6.3}
\]

where

\[
 f_\chi(s;\nu)=\chi_{\rm plan}(s)
 \left(\frac{s^3}{24}+\frac9{20},\nu\right).
\tag{6.4}
\]

Thus the field and first-jet requirements in condition (21) of the
fixed-window seed are realized by one frozen family.

#### Proof

Theorem 5.1 gives \(Q_{0,\nu,\eta}=B\), proving the first identity.  On
\(|s|\le21\), Corollary 5.2 gives the derivative of the graph; multiplication
by \(\chi_{\rm plan}\) gives (6.4).  Outside this interval the cutoff and
both sides of (6.4) vanish. \(\square\)

The preparation is not a fixed point of the graph transform: it is a
separate planar field obtained by joining the graph perturbation to \(q_0\).
It also does not preserve the incoming identity (4.2).  For example, at
\(\sigma=-30\), it equals \(q_0\), whereas the graph exterior equals
\(Q_v\).  Nor is global completeness available: (6.1) equals the uncut
\(q_0\) at \(\rho=0\), and that field is not complete.  Indeed, along its
orbit from \((\sigma,d)=(0,-1)\), put \(z=-d>0\).  Conservation of \(J\)
gives

\[
 z e^{2z-\sigma^2/2}=e^2,
 \qquad 2z+\log z=2+\frac{\sigma^2}{2}.
\]

Since \(\log z\le z\), one has
\(z\ge2/3+\sigma^2/6\), and therefore
\(\dot\sigma=1+2z\ge7/3+\sigma^2/3\).  Scalar comparison shows that
\(\sigma\) reaches infinity in finite positive time.

Proposition 6.1 closes only the field/jet clause (21).  It does not construct
the jointly regular one-sided trace family assumed later in the seed note,
validate its differentiated boundary-value problem, or prove a nonlinear
gap root.  Tail levels, phase normalization, trace/Fredholm inversion, and
the complete-history root therefore remain open.

## 7. A preparation-indexed Volterra--Weissinger theorem

The next theorem isolates the causal mechanism needed for an order-zero
graph solve.  It is abstract: no target constants are inserted.

Let \(\Omega\) be a compact tube with
\(a\le\sigma\le b\), and put

\[
 \Omega_s=\{u\in\Omega:\sigma(u)\le s\},\qquad
 E_s(q,p)=\sup_{u\in\Omega_s}|q(u)-p(u)|.
\tag{7.1}
\]

Fix one complete left preparation at \(\sigma=a\), including its incoming
trace.  Let \(\mathscr X\) be a nonempty closed candidate class, complete in
the uniform metric, whose members have that same preparation and trace.

### Theorem 7.1 (causal fixed point relative to a preparation)

Suppose \(\mathcal T:\mathscr X\to\mathscr X\) is a self-map and the
following estimates hold uniformly for \(q,p\in\mathscr X\).

1. The prepared planar fields \(F_q\) are complete and have a common spatial
   Lipschitz bound \(L_F\).
2. Their dependence on the scalar candidate is prefix-local:
   \[
    \sup_{\Omega_s}|F_q-F_p|\le B_F E_s(q,p).
\tag{7.2}
   \]
3. Every backward characteristic used by the operator stays in the tube
   until it crosses the left face, cannot return after crossing, and obeys
   \(\dot\sigma_{F_q}\ge\kappa>0\) before crossing.
4. Candidate dependence of \(\mathcal T\) occurs only through strictly
   positive delayed slots \(\tau_i>0\).  On the retained slot hull the
   algebraic dependence on slot \(i\) has Lipschitz bound \(A_i\).
5. The operator has the fixed incoming compatibility required by
   \(\mathscr X\).

Then, with

\[
 C_V=\frac{B_F}{\kappa}
     \sum_i A_i e^{L_F\tau_i},
\tag{7.3}
\]

one has the prefix estimate

\[
 E_s(\mathcal Tq,\mathcal Tp)
 \le C_V\int_a^s E_\xi(q,p)\,d\xi,
 \qquad a\le s\le b.
\tag{7.4}
\]

Consequently, for every integer \(n\ge0\),

\[
 E_s(\mathcal T^nq,\mathcal T^np)
 \le\frac{[C_V(s-a)]^n}{n!}E_s(q,p).
\tag{7.5}
\]

The map \(\mathcal T\) has a unique fixed point in \(\mathscr X\).  No
smallness condition \(C_V(b-a)<1\) is required.

#### Proof

Let \(y_q(r)=\Phi_{F_q}^{-r}(u)\) and
\(y_p(r)=\Phi_{F_p}^{-r}(u)\).  The standard variation estimate, (7.2), and
the common spatial Lipschitz bound give, before the left crossing,

\[
 |y_q(r)-y_p(r)|
 \le B_F e^{L_Fr}\int_0^r E_{s-\kappa t}(q,p)\,dt.
\tag{7.6}
\]

Once the common phase bound \(s-\kappa t\) is below \(a\), both
characteristics lie in the common left preparation and their direct field
difference is zero.  Extending \(E_\xi\) by zero for \(\xi<a\) and changing
variables in (7.6) therefore yield, at delay \(\tau_i\),

\[
 |y_q(\tau_i)-y_p(\tau_i)|
 \le\frac{B_F e^{L_F\tau_i}}{\kappa}
     \int_a^s E_\xi(q,p)\,d\xi.
\tag{7.7}
\]

Multiplication by the slot bounds and summation prove (7.4).  Iterating
(7.4) over the ordered simplex
\(a\le\xi_n\le\cdots\le\xi_1\le s\) proves (7.5).
At \(s=b\), the coefficients

\[
 \frac{[C_V(b-a)]^n}{n!}
\]

form a summable sequence.  The Weissinger fixed point theorem applied to
the complete space \(\mathscr X\) gives existence and uniqueness. \(\square\)

The same hypotheses give a conditional order-zero stability estimate for
the residual \(\mathcal R=I-\mathcal T\).  Indeed,

\[
 E_s(q,p)
 \le E_s(\mathcal Rq,\mathcal Rp)
       +C_V\int_a^sE_\xi(q,p)\,d\xi,
\]

so Gronwall's inequality yields

\[
 \|q-p\|_\infty
 \le e^{C_V(b-a)}
      \|\mathcal Rq-\mathcal Rp\|_\infty.
\tag{7.8}
\]

This is an inverse bound on the range of \(\mathcal R\).  It proves neither
local surjectivity nor a same-space \(C^3\) inverse theorem.

### Why Theorem 7.1 is not yet a target graph theorem

For the operator (3.6), the incoming identity (4.2), the positive-delay slot
structure, and bounded complete-field framework match parts of Theorem 7.1.
The remaining application hypotheses have not been proved at
\(\rho_*=1/\sqrt5\).  In particular, there is no validated target candidate
class with:

- a self-map estimate;
- a compact retained hull and target \(J\)-barriers;
- a uniform clock lower bound \(\kappa>0\);
- numerical bounds for \(B_F,L_F,A_i\), hence for \(C_V\); or
- target-amplitude loss-scale spatial and parameter estimates needed for
  the later \(C^3\) trace construction.

The theorem therefore supplies a route that can be matched by future
estimates, not a completed target-amplitude localized graph result.  The
non-explicit small-\(\rho\) full-plane graph is already supplied by Theorem
5.1 through a different argument.  Theorem 7.1 is relative to the fixed left
preparation; preparation independence is a separate open problem.

## 8. Target clock warning and barrier identity

A raw singular-slot evaluation already rules out one tempting shortcut.  Set
\(\eta=0\), \(\rho=1/\sqrt5\), and evaluate (3.6) at the singular slots with
current phase \(s=3\).  Direct algebra gives

\[
 \mathcal T_X=-\frac12+\frac{567}{320\sqrt5}>0,
\qquad
 \dot\sigma=-2\mathcal T_X
 =1-\frac{567}{160\sqrt5}<0.
\tag{8.1}
\]

Thus the singular slots do not provide a positive target clock estimate.
Equation (8.1) is not an evaluation of an actual target fixed-point graph,
because no such graph has yet been computed.  It neither proves nor
disproves that a different target tube or a different phase coordinate can
satisfy the causal hypotheses.

For later barrier work, if \(Q=q_0+\Delta\), with
\(\Delta=(\Delta_X,\Delta_Y)\), and

\[
 J(\sigma,d)=d\exp\!\left(-2d-\frac{\sigma^2}{2}\right),
\tag{8.2}
\]

then the exact identity from the singular reachable-hull calculation is

\[
 \dot J=e^{-2d-\sigma^2/2}
 \{\sigma\Delta_X+(1-2d)\Delta_Y\}.
\tag{8.3}
\]

This identity identifies what must be bounded on curved faces.  No target
sign condition from (8.3) is validated here.  A compact causal Lambert tube
may have asymmetric normal bounds

\[
 d_-<d<d_+<\frac12.
\tag{8.4}
\]

The upper bound \(d_+<1/2\), rather than a symmetric \(|d|\)-bound, is what
ensures

\[
 J_d=(1-2d)e^{-2d-\sigma^2/2}>0
\tag{8.5}
\]

throughout that component.  Separately, exact recovery of the physical
operator under the present normal cutoff requires every active slot to
satisfy \(|d|\le1\).  The cutoff plateau is therefore an algebraic
slot condition, not by itself a causal Lambert component.

## 9. Exact claim ledger

| Statement | Status in this note |
|---|---|
| \(Q_v\in C_b^\infty\), is complete, and has the pointwise clock (2.6) | Proved |
| Cutoff algebra, active slot sets, plateau agreement, and fixed exterior | Proved |
| Parameter-independent incoming self-map at \(\sigma=-30\) | Proved |
| Unique \(\rho=0\) graph fixed point and complete \(d=0\) orbit | Proved |
| Declared-window first \(\rho\)-derivative of the slot transform | Proved |
| Full-plane \(C_b^3\) graph for non-explicit small \(|\rho|\), unique in its \(O(|\rho|)\) contraction class | Proved by Theorem 5.1 |
| Actual declared-window first graph jet | Proved by Corollary 5.2 |
| Planar preparation realizing seed condition (21), field/jet clause only | Proved by Proposition 6.1 |
| Global completeness or graph-fixed-point status of that planar preparation | Not claimed; generally false for this construction |
| Volterra--Weissinger fixed point theorem relative to one preparation | Proved under the hypotheses of Theorem 7.1 |
| Order-zero residual inverse bound on its range | Conditional consequence of the same hypotheses |
| Target graph at \(\rho_*=1/\sqrt5\) | Open |
| Target clock, \(J\)-barriers, and retained two-dimensional history hull | Open |
| Target-amplitude loss-scale \(C^3\) continuation and prepared trace pair | Open |
| Nonlinear trace BVP and regularized-gap root | Open |
| Fixed-\(\varepsilon\) complete-history root | Open |
| Independence of the left preparation | Open |
| General-network fixed-\(\varepsilon\) lift | Open |
| Biological pulse-control theorem | Open |

The executable formulas and directed interval checks are implemented in
`src/canard_control/fixed_epsilon_clocked_tail_graph_extension.py`.  Their
presence records the algebra and claim boundary above; it is not a numerical
validation of any open target item.

## 10. Reproduction

From the repository root, regenerate the structural record with

```bash
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_clocked_tail_graph_extension.py
```

The generated JSON contains exact formula identifiers, directed enclosures
for \(\Theta_*\), slot-containment margins, the raw clock counterexample,
and the target-gate Boolean ledger.  It contains no target-amplitude interval
flow, target graph, trace solve, or root certificate.  The non-explicit
small-\(\rho\) theorem above is a deduction from the serialized operator and
the two cited bounded-cutoff graph theorems; it is not a numerical target
certificate in that JSON.
