# A target-amplitude raw-slot tilted-phase comparison

## 1. Result and scope

At \(\rho_*=1/\sqrt5\), the raw singular-slot value of the clocked-tail
operator has \(\dot\sigma<0\) at \(s=3\).  Thus the canard coordinate
\(\sigma=-2X\) cannot be used as a target clock merely by continuity from
\(\rho=0\).

This note studies whether a variable tilt repairs that failure on the
**independent raw-slot comparison geometry**.  It does not construct a phase
on an actual target causal graph.  For

\[
 0\le \nu\le\frac15,\qquad \eta=0,
\tag{1.1}
\]

it proves the following statements.

1. The raw target singular-slot vector has exactly three simple
   \(\sigma\)-clock reversals and three associated stall parameters.  At a
   stall the entire raw \((\sigma,d)\)-vector vanishes, so no \(C^1\) phase
   can be strictly increasing there.
2. No constant affine phase \(a\sigma+bd\), oriented consistently with the
   incoming tail, can be increasing at both \(s=-3\) and \(s=3\).
3. At the frozen operating anchor
   \(\nu_{\rm anc}=0.21256022233963731\), an exact shifted-slot equilibrium
   lies inside the radius-\(1/1000\) product geometry.  Hence no \(C^1\)
   phase can have a strictly positive clock there.
4. A \(C^3\) tapered comparison phase, equal to \(\sigma\) on the incoming
   tail, has raw singular-slot speed greater than \(1/200\) throughout (1.1).
5. On an explicit product tube of radius \(1/1000\) about the target
   singular current, delay-four, and delay-five slots for
   \(-20\le s\le20\), 256-bit directed arithmetic proves
   \(\dot\vartheta>1/1000\) and proves that \(\vartheta\) is a submersion.
6. A separate analytic estimate gives \(\dot\vartheta\ge1\) on the
   incoming-to-core product corridor \(-30\le s\le-20\), including the
   longitudinal cutoff transition.

Items 5--6 prove a **raw-slot product-tube comparison inequality** from the
fixed incoming face to the right end of the preparation core, and only for
the parameter box (1.1).  They do not prove the clock inequality on an actual
target causal graph.  They also do not prove that backward characteristics
stay in this tube, that the graph transform maps a candidate class into
itself, or that an actual target graph exists.  No one-sided trace, Fredholm
inverse, complete-history root, network lift, or biological-control
conclusion is drawn here.

The box (1.1) is a comparison box, not a validated bracket for the selected
root.  The no-go in Proposition 2.3 below is stronger for the frozen
operating anchor: extending the same product-tube estimate from
\(\nu\le1/5\) to \(\nu_{\rm anc}\) already encounters a zero vector at a
normal displacement smaller than \(1/1000\).

## 2. Raw target-slot algebra

Use

\[
 \sigma=-2X,\qquad d=Y-X^2+\frac12.
\tag{2.1}
\]

At \(\eta=0\), evaluate the uncut target operator on

\[
 \Gamma(s,0),\qquad \Gamma(s-4,0),\qquad \Gamma(s-5,0).
\tag{2.2}
\]

The \(\Theta_*\)-slot is inactive.  Direct substitution gives

\[
 S_*(s):=\dot\sigma
 =1+\frac{\sqrt5}{2400}
   \left(-40s^3-81s^2+369s-999\right)
\tag{2.3}
\]

and, because \(Q_Y=\sigma/2+\nu/\sqrt5\),

\[
 D_\nu(s):=\dot d
 =\frac{s}{2}\{1-S_*(s)\}+\frac{\nu}{\sqrt5}.
\tag{2.4}
\]

In particular,

\[
 D_0(s)=\frac{\sqrt5}{4800}
 \left(40s^4+81s^3-369s^2+999s\right).
\tag{2.5}
\]

The identity behind (2.4) is exact for every plateau slot:

\[
 \dot d=Q_Y-2XQ_X
       =\frac{\sigma}{2}(1-\dot\sigma)+\frac{\nu}{\sqrt5}.
\tag{2.6}
\]

### Proposition 2.1 (raw reversals and stalls)

The cubic \(S_*\) has exactly three simple real zeros.  Directed isolating
intervals are

\[
\begin{aligned}
 s_1&\in[-4.143276804,-4.143276802],\\
 s_2&\in[-0.193924651,-0.193924650],\\
 s_3&\in[ 2.312201453, 2.312201455].
\end{aligned}
\tag{2.7}
\]

The raw vector \((S_*(s),D_\nu(s))\) vanishes precisely when

\[
 S_*(s_j)=0,
 \qquad
 \nu=\nu_j:=-\frac{\sqrt5}{2}s_j.
\tag{2.8}
\]

The corresponding parameter enclosures are

\[
\begin{aligned}
 \nu_1&\in[4.6323242894349683,4.6323242916710363],\\
 \nu_2&\in[0.2168143499564272,0.2168143510744613],\\
 \nu_3&\in[-2.585119815526961,-2.585119813290892].
\end{aligned}
\tag{2.9}
\]

In particular, \(\nu_2\in(1/10,1/4)\).

#### Proof

The exact Sturm sequence of (2.3) has three more variations at
\(-\infty\) than at \(+\infty\), while
\(\gcd(S_*,S_*')=1\).  Exact Sturm counts give one zero in each interval
of (2.7).  At a zero of \(S_*\), (2.4) becomes
\(s/2+\nu/\sqrt5\), which proves (2.8).  The directed images of (2.7)
under \(s\mapsto-\sqrt5s/2\) give (2.9). \(\square\)

At any point in (2.8), \(L_V\vartheta=0\) for every \(C^1\) scalar
function \(\vartheta\).  Therefore no positive-clock theorem can hold on a
set containing that raw slot tuple.  This is a vector-field obstruction,
not a defect of a particular phase formula.

### Lemma 2.2 (constant affine phases cannot repair the clock)

Let \(0\le\nu\le1/5\).  No phase \(a\sigma+bd\) with \(a>0\) is strictly
increasing on the raw target slots at both \(s=-3\) and \(s=3\).

#### Proof

Exact substitution in (2.3)--(2.4) gives

\[
 S_*(-3)<0,\quad D_\nu(-3)<0,
 \qquad
 S_*(3)<0,\quad D_\nu(3)>0
\tag{2.10}
\]

uniformly on the parameter interval.  Positivity at \(-3\) would require
\(b<0\), whereas positivity at \(3\) would require \(b>0\). \(\square\)

Thus the variable tilt below is forced by the geometry; it is not an
expository change of coordinates.

### Proposition 2.3 (frozen-anchor product-tube no-go)

Interpret the written decimal

\[
 \nu_{\rm anc}=0.21256022233963731
 =\frac{21256022233963731}{10^{17}}
\tag{2.11}
\]

as an exact rational number.  This is a frozen numerical operating anchor,
not a validated selected root.  Define the raw-slot forcing

\[
 g_*(s):=\frac{1-S_*(s)}2
 =\frac{\sqrt5}{4800}
   \left(40s^3+81s^2-369s+999\right).
\tag{2.12}
\]

For the shifted raw-slot family with current slot \(\Gamma(s,d)\), delayed
slots \(\Gamma(s-4,0)\) and \(\Gamma(s-5,0)\), and \(\eta=0\), the two
physical components are

\[
 Q_X=d-\frac12+g_*(s),\qquad
 Q_Y=\frac{s}{2}+\frac{\nu}{\sqrt5}.
\tag{2.13}
\]

Consequently

\[
 s_e=-\frac{2\nu_{\rm anc}}{\sqrt5},\qquad
 d_e=\frac12-g_*(s_e)=\frac{S_*(s_e)}2
\tag{2.14}
\]

makes the raw-slot vector exactly zero.  A 256-bit outward-rounded enclosure
gives

\[
\begin{aligned}
 -0.190119642585559367
 &<s_e<-0.190119642585559366,\\
 0.000701368783306192
 &<d_e<0.000701368783306194<\frac1{1000}.
\end{aligned}
\tag{2.15}
\]

Thus this slot tuple belongs to the radius-\(1/1000\) product tube with
nominal phase \(s=s_e\).  At that tuple,

\[
 L_Q\vartheta=\nabla\vartheta\mathbin{\cdot}(0,0)=0
\tag{2.16}
\]

for every \(C^1\) phase \(\vartheta\).  Therefore no strict product-tube
clock---tapered or otherwise---can result by merely enlarging the parameter
box (1.1) to include \(\nu_{\rm anc}\).

The word *equilibrium* here refers to a zero of the shifted independent-slot
transform (2.13).  The delayed slots have phases \(s_e-4\) and \(s_e-5\), so
this proposition does not assert the existence of a constant RFDE history or
an invariant target graph.

## 3. A comparison phase compatible with the incoming tail

Let

\[
 \beta(\sigma)=
 \begin{cases}
 0,&\sigma\le-6,\\
 35z^4-84z^5+70z^6-20z^7,
    &-6<\sigma<-5,\quad z=\sigma+6,\\
 1,&\sigma\ge-5.
 \end{cases}
\tag{3.1}
\]

The septic joins with three derivatives, so \(\beta\in C^3\),
\(0\le\beta\le1\), and

\[
 \beta'(\sigma)=140z^3(1-z)^3
\tag{3.2}
\]

on the transition.  Define

\[
 \vartheta(\sigma,d)
 =\sigma+8\beta(\sigma)D_0(\sigma)d.
\tag{3.3}
\]

For \(\sigma\le-6\), this is exactly \(\sigma\).  Hence the incoming face
\(\sigma=-30\) is also the constant phase face
\(\vartheta=-30\), independently of \(d\).  On the clocked tail \(Q_v\),

\[
 L_{Q_v}\vartheta=\dot\sigma=v_R(\sigma)>0
 \qquad(\sigma\le-6).
\tag{3.4}
\]

### Theorem 3.1 (raw target clock)

For every \(s\in\mathbb R\) and every \(0\le\nu\le1/5\), the raw
singular-slot vector satisfies

\[
 L_{(S_*,D_\nu)}\vartheta(s,0)>\frac1{200}.
\tag{3.5}
\]

#### Proof

Where \(\beta=1\),

\[
 H_\nu(s):=L_{(S_*,D_\nu)}\vartheta(s,0)
 =S_*(s)+8D_0(s)D_\nu(s).
\tag{3.6}
\]

For each fixed \(s\), this expression is affine in \(\nu\).  It therefore
suffices to check the endpoints \(\nu=0,1/5\).  For both endpoints, the
exact Sturm sequence of \(H_\nu-1/200\) has nine members and four sign
variations at each infinite end.  Thus it has no real zero.  Its value at
zero is

\[
 \frac{199}{200}-\frac{333\sqrt5}{800}>0,
\tag{3.7}
\]

which proves \(H_\nu>1/200\) throughout the parameter interval.

For \(s\le-6\), one has \(\beta=0\).  The exact Sturm count gives no zero
of \(S_*-1/200\) on \(( -\infty,-6]\), and its value at \(-6\) is
positive.  On \([-6,-5]\), the numerator of \(S_*-1\) is decreasing and
has value \(131\) at \(-5\), hence \(S_*>1\).  Consequently
\(D_0>0\) and \(D_\nu>0\) there.  Since

\[
 L\vartheta=(1-\beta)S_*+\beta H_\nu,
\]

the same lower bound holds through the taper. \(\square\)

The theorem is an exact raw-slot result.  It is stronger than evaluating a
finite mesh, but it still does not say that slots generated by an unknown
target graph remain close to (2.2).

## 4. A directed raw-slot product tube

Put \(r=1/1000\).  For \(-20\le s\le20\), define the independent slot
product by

\[
\begin{aligned}
 |\sigma_0-s|&\le r,& |d_0|&\le r,\\
 |\sigma_4-(s-4)|&\le r,& |d_4|&\le r,\\
 |\sigma_5-(s-5)|&\le r,& |d_5|&\le r.
\end{aligned}
\tag{4.1}
\]

The \(\Theta_*\)-slot is inactive at \(\eta=0\).  Every slot in (4.1)
lies strictly in the unit plateau of the clocked-tail graph cutoff.  The
smallest longitudinal or normal margin is

\[
 1-r=\frac{999}{1000}.
\tag{4.2}
\]

Thus the extended operator agrees exactly with the physical target slot
operator on (4.1).

For arbitrary independent slots in (4.1), let \((\dot\sigma,\dot d)\) be
the coordinate velocity produced by that operator.  From (3.3),

\[
\begin{aligned}
 \vartheta_\sigma
 &=1+8\{\beta'D_0+\beta D_0'\}d_0,\\
 \vartheta_d&=8\beta D_0,\\
 \dot\vartheta
 &=\vartheta_\sigma\dot\sigma+\vartheta_d\dot d.
\end{aligned}
\tag{4.3}
\]

### Theorem 4.1 (directed raw-slot product-tube clock)

On (4.1), uniformly for \(0\le\nu\le1/5\),

\[
 \dot\vartheta>\frac1{1000},
 \qquad
 |\nabla\vartheta|^2>\frac1{100}.
\tag{4.4}
\]

#### Directed proof

Partition \([-20,20]\) into \(20000\) exact rational cells of width
\(1/500\).  On each cell, evaluate the independent current and delayed
slot intervals in (4.1), the exact physical polynomial operator, (2.6),
and (4.3), using 256-bit MPFR arithmetic with outward rounding.  The least
lower endpoint for the phase speed is

\[
 0.0011409071019661816122405482562768642\ldots
 >\frac1{1000}.
\tag{4.5}
\]

It occurs in cell 9911.  The least lower endpoint for the squared gradient
is

\[
 0.93648109241450593907325255773953030\ldots
 >\frac1{100}.
\tag{4.6}
\]

It occurs in cell 7534.  The taper and its derivative are enclosed by
monotonic endpoint evaluation and the exact maximum
\(\max\beta'=35/16\).  Hence every operation in (4.3) is outward rounded,
and (4.4) follows. \(\square\)

The product structure is deliberately hostile: the delayed slots are
varied independently, not tied to one numerical orbit.  It proves that the
clock survives all slot errors of the stated size.  It does not prove that
such errors contain the delayed slots of a fixed graph.

## 5. The incoming-to-core corridor

The directed core tube begins at nominal phase \(-20\), whereas the exact
incoming self-map is at \(\sigma=-30\).  The interval between them crosses
the longitudinal graph cutoff.  A direct estimate avoids differentiating
that flat cutoff.

Let the nominal phase lie in \([-30,-20]\), retain radius \(r=1/1000\),
and allow all graph weights \(w_0,w_4,w_5\) to vary independently in
\([0,1]\).  In this corridor the current voltage coordinate
\(x=X_0\) is at least nine, and

\[
 a=X_4-X_0,\qquad b=X_5-X_0
\]

lie in \([1,3]\).  Since \(2/5<\rho_*<1/2\) and
\(\rho_*^3<1/10\), the target fast component satisfies

\[
 \mathcal T_X
 \le-\frac12+w_0\left{
 r-\frac{2x^3}{15}+\frac3{10}
 +\frac{9x^2+27x+27}{40}
 \right}.
\tag{5.1}
\]

The expression in braces has value

\[
 -\frac{17981}{250}<0
\tag{5.2}
\]

at \(x=9\), while its derivative there is

\[
 -\frac{1107}{40}<0
\tag{5.3}
\]

and decreases thereafter.  Thus \(\mathcal T_X\le-1/2\).  Since
\(\beta=0\) throughout this corridor,

\[
 \dot\vartheta=\dot\sigma=-2\mathcal T_X\ge1.
\tag{5.4}
\]

This includes the exterior, cutoff transition, and unit plateau without
assuming that any transition weight equals zero or one.  Combining (5.4)
with Theorem 4.1 supplies a positive slotwise clock from the incoming face
through nominal phase \(20\).

## 6. What is and is not closed

The earlier target list contained five graph-level gates: a self-map, a
compact retained hull, a uniform clock, barrier inequalities, and numerical
Volterra constants.  This note supplies a comparison estimate relevant to the
third gate, but does **not** close that graph-level gate because no actual
target graph has been placed in the product tube.  More precisely:

| Statement | Status |
|---|---|
| Raw coordinate algebra and three simple \(\sigma\)-clock reversals | **Proved** |
| Three exact raw stalls and impossibility of a positive phase at each stall | **Proved** |
| Constant affine-phase no-go | **Proved on \(0\le\nu\le1/5\)** |
| Frozen-anchor shifted-slot zero with \(0<d_e<1/1000\) | **Exact algebra and 256-bit directed enclosure** |
| Strict clock on the same product geometry at \(\nu_{\rm anc}\) | **Impossible for every \(C^1\) phase** |
| Incoming-compatible tapered raw phase with speed \(>1/200\) | **Proved on \(0\le\nu\le1/5\)** |
| Radius-\(1/1000\) core slot-product clock and submersion | **Directed-validated** |
| Incoming-to-core product-corridor clock | **Proved analytically** |
| Backward invariance or no-return of the slot tube | **Open** |
| Moving \(J\)- or \(d\)-barriers | **Open** |
| Graph-transform self-map and target fixed graph | **Open** |
| Prepared \(C^3\) one-sided traces and \(W^{1,p}\) Fredholm inverse | **Open** |
| Fixed-\(\varepsilon\) complete-history root and response | **Open** |
| General-network lift and biological-control chain | **Open** |

In particular, the fixed-radius product tube must not be called a retained
hull or an actual target causal phase domain.  A backward characteristic can
leave it through a normal face; moreover Proposition 2.3 prevents the same
product geometry from carrying a strict clock at the frozen anchor.  A target
theorem must instead use an intrinsic coordinate on an actual reference flow
or graph, together with barriers and a proof of delayed-slot closure.

## 7. Reproduction

The exact and directed calculations are implemented in
`src/canard_control/fixed_epsilon_target_tilted_phase.py`.  Regenerate the
serialized record from the repository root with

```bash
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_tilted_phase.py
```

The result pins its clocked-tail parent, exact Sturm sign data, directed
stall and frozen-anchor enclosures, all 20000 raw-slot product cells, and the
strict open-claim ledger.
