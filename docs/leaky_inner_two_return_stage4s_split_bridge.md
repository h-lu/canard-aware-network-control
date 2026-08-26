# Stage 4S-C: fixed splitting and the two-return stable-germ bridge

## Status

**Proved linear theorem and model instance; conditional nonlinear bridge;
model-level return/tube/germ still open.**

This certificate answers one narrow question without blurring its three
levels.  Stage 4L proves exact identities for the selected phase-fixed
linear operator (A).  Those identities really do imply a complete fixed
splitting and squared rates for the linear two-step operator (B=A^2).
They do **not** construct a nonlinear selected map (P), a nonlinear
two-return map (Q), or a flow tube.  Stage 4R identifies a return-map stable
set with a periodic-orbit stable-set germ only after its separate nonlinear
same-semiflow hypotheses are verified.

The artifact is therefore intentionally fail closed.  In particular,
(B=A^2) is never silently renamed (Q).

## 1. Pure algebra from (A,q,f)

Let (Sigma) be a Banach space and suppose

\[
 A\in\mathcal L(\Sigma),\qquad q\in\Sigma,\qquad f\in\Sigma^*,
\]

with

\[
 Aq=\mu q,\qquad fA=\mu f,\qquad f(q)=1.
\tag{1.1}
\]

Set

\[
 P_u=qf,\qquad P_s=I-qf,\qquad
 E_u=\operatorname{span}\{q\},\qquad E_s=\ker f.
\tag{1.2}
\]

The normalization (f(q)=1) gives

\[
 P_s^2=P_s,\quad P_u^2=P_u,\quad
 P_sP_u=P_uP_s=0,\quad P_s+P_u=I,
\]

and hence

\[
 \Sigma=E_s\oplus E_u.
\tag{1.3}
\]

The two eigen-relations in (1.1) give the exact intertwining identities

\[
 AP_s=P_sA=P_sAP_s,
 \qquad AP_u=P_uA=\mu P_u.
\tag{1.4}
\]

Thus both subspaces are invariant.  No small numerical residual is involved.

Now define the **linear** two-step operator

\[
 B:=A^2.
\]

Multiplying (1.4) gives

\[
 BP_s=P_sB=P_sBP_s=(AP_s)^2,
 \qquad BP_u=P_uB=\mu^2P_u.
\tag{1.5}
\]

In particular,

\[
 B_s=B|_{E_s}=A_s^2,qquad B_s^n=A_s^{2n}.
\tag{1.6}
\]

Therefore any power estimate

\[
 \|A_s^n\|\le K_s\rho_s^n
\]

implies

\[
 \|B_s^n\|\le K_s(\rho_s^2)^n.
\tag{1.7}
\]

On the one-dimensional unstable space,

\[
 B_u=\mu^2 I_{E_u}.
\]

If (mu\ne0), scalar multiplication has the same operator norm in every
inherited norm on (E_u), so

\[
 \|(B_u)^{-n}\|=|\mu|^{-2n}.
\tag{1.8}
\]

Consequently a one-return inverse bound

\[
 |\mu|^{-1}\le\rho_{u,1}<1
\]

gives

\[
 \|(B_u)^{-n}\|\le(\rho_{u,1}^2)^n,
 \qquad K_u=1,
 \qquad \rho_{u,2}\le\rho_{u,1}^2.
\tag{1.9}
\]

The direction of (1.9) matters.  The unstable **forward** multiplier of
(B) has modulus (|\mu|^2>1).  The number below one is a contraction rate
for inverse/backward powers, not a forward unstable contraction.

## 2. Source-bound inner-orbit instance

Stage 4L supplies, for the selected near-one-period phase-fixed discrete
linear section operator,

\[
 A=\Pi_T\mathcal U(T,0)|_{\Sigma_0},
 \qquad \Sigma_0=\{h\in Y:h_v(0)=0\},
\]

the exact relations

\[
 Aq=\mu_uq,\qquad fA=\mu_uf,\qquad f(q)=1,
\]

and

\[
 AP_s=P_sA=P_sAP_s.
\]

It also proves

\[
 \|A_s^n\|\le\rho_{\rm term}^n\le0.1^n,
 \qquad K_s=1,
\]

with

\[
 \rho_{\rm term}\le
 0.00989642748161000022244199598343033161524171712346077110775160712.
\]

Equations (1.6)--(1.7) now give the proved two-step estimate

\[
 \boxed{\|B_s^n\|\le0.01^n,\qquad K_s=1.}
\tag{2.1}
\]

The sharper one-step bound for (B_s) is

\[
 \|B_s\|\le
 0.0000979392768987656512909542642292023934722690772595215680701268436008663590088133855053307238038569905570840746589878769428346944.
\tag{2.2}
\]

The source-bound Floquet evidence proves that the unique nontranslation
unstable multiplier obeys

\[
 1.81913372574167842375644213779457264168445028000790971
 \le |\mu_u|
 \le
 2.22189495008307196905747671092766936323792280049007467,
\]

and already registers

\[
 \rho_{u,1}\le
 0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934.
\]

The Stage-4L vector (q) is the physical section eigencolumn for this unique
nontranslation unstable multiplier.  Hence (1.8)--(1.9), rather than a new
dichotomy estimate, give

\[
 \boxed{
 \rho_{u,2}\le
 0.302183501335053468766049321268313699617093109911449469063818668425607982682870864983343314167041012216402531488839876224555070910009877958313689944253533344086871769103550439695624961741628356,
 \quad K_u=1.}
\tag{2.3}
\]

This closes the linear two-return splitting and both discrete power rates.
It does not close a nonlinear graph theorem.

## 3. What is needed to write (Q=P^2)

Suppose, separately, that (D\subset\Sigma) is open, (p\in D), and

\[
 P:D\to\Sigma
\]

is a (C^1) selected section map with (P(p)=p) and (DP(p)=A).  Because
(P(D)) need not be contained in (D), the correct composition domain is

\[
 D_2:=\{x\in D:P(x)\in D\}=D\cap P^{-1}(D).
\tag{3.1}
\]

It is open, contains (p), and only on this domain is

\[
 Q=P\circ P
\]

automatically defined.  The chain rule then yields

\[
 DQ(p)=DP(p)^2=A^2=B.
\tag{3.2}
\]

Neither (Q(D_2)\subset D_2) nor (P(D_2)\subset D_2) follows from
(3.1).  An iterative theorem needs an additional patch (N\subset D_2)
with (Q(N)\subset N).  For a conventional same-patch stable set of (P),
one needs the stronger condition (P(N)\subset N).

There is a useful but still conditional discrete fact.  If (Q=P^2:N\to N)
and (P) is continuous at (p), then

\[
 Q^n(x)\to p
 \quad\Longleftrightarrow\quad
 P^j(x)\to p.
\tag{3.3}
\]

Indeed, the even iterates are (Q^n(x)), while the odd iterates are
(P(Q^n(x))\to P(p)=p).  This proves a discrete convergence equivalence;
it says nothing yet about physical-time arcs.

The fixed spaces (E_s,E_u) are invariant under the derivative (DQ(p)).
They are not thereby invariant affine subsets of the nonlinear map (Q).
A nonlinear stable graph still requires a validated (C^2) self-map,
hyperbolicity, a return ball, and the required second-derivative bounds.

## 4. Same-semiflow composition, repeated hits, and the common tube

Assume the one-return map actually has the form

\[
P(x)=\Phi_{\theta(x)}(x)
\]

for one selected branch of the same semiflow, with a continuous positive
time function (	heta:D\to(0,\infty)).  On (D_2), the semiflow law gives

\[
 P^2(x)=\Phi_{\Theta_2(x)}(x),
 \qquad
 \Theta_2(x)=\theta(x)+\theta(P(x)).
\tag{4.1}
\]

This conclusion requires existence of both legs and of their concatenated
trajectory.  An abstract composition of two maps does not supply (4.1).

If (P(p)=p) and (	heta(p)=P_{\rm orb}), then

\[
 Q(p)=p,\qquad \Theta_2(p)=2P_{\rm orb}.
\]

If

\[
 0<\theta_-\le\theta\le\theta_+
\]

on (N\cup P(N)), then

\[
 2\theta_-\le\Theta_2\le2\theta_+.
\]

The composition records a chosen intermediate selected hit (P(x)) and a
chosen terminal selected hit (P^2(x)).  Iterating it requires
(Q(N)\subset N\) and hence the same nested-domain check at every even
iterate.  None of this excludes additional earlier or intervening section
hits, so it does not establish first-positive-return or an ordinal label.

Most importantly, (Q=P^2) is not a substitute for a common flow tube.  To
obtain one tube (G) for a two-leg return, one must prove both

\[
 \Phi_s(x)\in G
 \quad(0\le s\le\theta(x),\ x\in N)
\]

and the corresponding statement for the second leg starting at every
(P(x)\in P(N)), using the **same** (G).  Stage 4L's terminal linear
operator norm controls neither of these physical-time statements.

## 5. Exact Stage-4R stable-germ interface

Stage 4R does not require (Q=P^2).  A direct near-two-period selected
return suffices if all of the following hold on a local section patch (N):

1. (N) is a local section patch containing (p), (Q:N\to N) is
   continuous, (Q(p)=p), and (Q(x)=\Phi_{\Theta(x)}(x)) for the same
   semiflow;
2. (Theta:N\to[\Theta_-,\Theta_+]) is continuous,
   (0<\Theta_-\le\Theta_+<\infty), and
   (Theta(p)=2P_{\rm orb});
3. one common tube (G) contains every intervening arc
   (Phi_s(x)), (0\le s\le\Theta(x));
4. the section is isolated at the periodic orbit:
   (overline N\cap\Gamma=\{p\}).

Then

\[
 W_N^s(Q)=N\cap W_G^s(\Gamma)
\]

and the two sets have the same germ at (p).  The lower time bound makes
the accumulated return times tend to infinity; the upper bound and common
tube control all intervening times; section isolation turns convergence to
the orbit at return times into convergence to (p).

Thus (Q=P^2) on suitable nested domains is one sufficient construction of
the discrete return, but it is neither necessary nor sufficient for the
flow stable-germ conclusion by itself.

## 6. Final ledger

### Proved

- The complementary projections, direct sum, invariance, and intertwining
  for (A) and (B=A^2).
- The model-specific two-return stable bound (K_s=1),
  (ho_{s,2}=0.01), including the sharper bound (2.2).
- The one-dimensional inverse-unstable formula and model-specific backward
  rate (2.3), with (K_u=1).
- The general conditional nested-domain chain-rule, even/odd convergence,
  same-semiflow time-sum, and Stage-4R interface statements.

### Conditional

- (Q=P^2), (DQ(p)=A^2), and repeated selected legs, once a nonlinear
  selected (P) and its nested/invariant domains are validated.
- Equality of the return stable set and periodic-orbit stable-set germ once
  the direct Stage-4R time, tube, fixed-point, and isolation hypotheses hold.
- A stable graph for (Q), once the (C^2) return-ball and nonlinear bounds
  close.

### Open for the model

- A nonlinear selected one-return (P) or direct two-return (Q) on an
  open and invariant section ball.
- The nested composition domain, uniform positive time bounds, repeated
  composability, and one common two-leg flow tube.
- Section isolation, two-return Hessian blocks, and a hyperbolic stable graph.
- No-earlier-hit/first-return semantics, pulse crossing, onset, routing,
  capture, and network safety.

The executable result binds these claims to the exact Stage-4L, Stage-4R,
and unstable-multiplier parent bytes and keeps every open model flag false.
