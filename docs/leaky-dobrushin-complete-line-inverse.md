# Complete-line transverse inverse and conditional canard-root transfer

Status: **the transverse Green inverse is proved for every finite network in
the balanced Dobrushin class.**  It yields an exact transfer theorem for a
canonical synchronized Lin realization, conditional on a scalar Fredholm
Lin problem and simple scalar canard root.  A scalar complete-history canard root
has not yet been proved for the leaky RFDE.

## 1. Stripwise transverse equation

Let \(Q,B_0,B_1,\pi\) satisfy the assumptions of the finite-network
Dobrushin theorem, normalize \(\pi^T\mathbf1=1\), and let
\(V:\mathbb R\to\mathbb R\) be any complete synchronous scalar trajectory
such that

\[
 \sup_{t\in\mathbb R}|V(t)-1|\leq\frac52.
\]

The identities

\[
 Q\mathbf1=\mathbf1,\quad \pi^TQ=\pi^T,
 \quad B_j\mathbf1=\tfrac12\mathbf1,
 \quad \pi^TB_j=\tfrac12\pi^T
\]

leave both \(\operatorname{span}\{\mathbf1\}\) and \(\ker\pi^T\)
invariant.  Hence the variational equation splits into a scalar collective
block and a transverse block; no simultaneous diagonalization is assumed.

For complex transverse vectors define

\[
 E_{N,\perp}=\ker\pi^T\times\ker\pi^T,
 \qquad
 m(x,y)=\max\{\operatorname{diam}x,3\operatorname{diam}y\},
\]

where \(\operatorname{diam}z=\max_{i,k}|z_i-z_k|\).  Diameter is a norm on
\(\ker\pi^T\): zero diameter makes \(z=c\mathbf1\), and then
\(0=\pi^Tz=c\).  Since \(N\) is finite, this normed space is complete.
Thus

\[
 X_{N,\lambda}=C([-r,0],E_{N,\perp}),
 \qquad
 \|\phi\|_\lambda=
 \sup_{-r\leq\theta\leq0}e^{\lambda\theta}m(\phi(\theta))
\]

is Banach, where \(r=5\sqrt5\) and \(\lambda=1/10\).

The parent Dobrushin calculation does not use periodicity.  Once the
voltage strip is imposed, its coefficient estimates apply pointwise to any
complete synchronous trajectory and give

\[
 D^+M(t)\leq-\alpha M(t)
 +\beta\sup_{t-r\leq u\leq t}M(u),
 \qquad M(t)=m(z(t)).                                      \tag{1.1}
\]

The source-bound directed constants satisfy

\[
 \alpha-\lambda-\beta e^{\lambda r}
 >0.0076664505356400.                                     \tag{1.2}
\]

At a first crossing of the exponentially decaying barrier, every delayed
value is at most \(e^{\lambda r}\) times the current barrier.  Equation
(1.2) therefore gives the current-state estimate, including portions still
in the initial history.  Shifting the retained history then gives

\[
 \|U_\perp(t,s)\phi\|_\lambda
 \leq e^{-\lambda(t-s)}\|\phi\|_\lambda,
 \qquad t\geq s.                                         \tag{1.3}
\]

The constant in (1.3) is one and is independent of \(N\) and the admitted
topology in the declared diameter norm.  No dimension-uniform equivalence
with Euclidean norms, and no uniform nonlinear neighborhood, is asserted.

## 2. Forced comparison and pullback limit

Take \(f\in C_b(\mathbb R,E_{N,\perp})\) and put

\[
 F(t)=\max\{\operatorname{diam}f_v(t),
                 3\operatorname{diam}f_w(t)\},
 \qquad \|f\|_{\perp,\infty}=\sup_tF(t).
\]

Let \(z^S\) be the forward solution begun at time \(S\) with zero retained
history.  Define

\[
 h_S(t)=\int_S^t e^{-\lambda(t-u)}F(u)\,du.
\]

At a first crossing of \(M(z^S(t))\) above \(h_S(t)\), one has
\(h_S(t-\tau_j)\leq e^{\lambda\tau_j}h_S(t)\), while
\(h_S'=-\lambda h_S+F\).  Equation (1.2) makes the upper Dini derivative of
the difference strictly negative, a contradiction.  Including shifted
history points gives the stronger estimate

\[
 \|z_t^S\|_\lambda
 \leq\int_S^t e^{-\lambda(t-u)}F(u)\,du
 \leq\frac{1}{\lambda}\|f\|_{\perp,\infty}.              \tag{2.1}
\]

If \(S_1<S_2\leq t\), the difference
\(z^{S_1}-z^{S_2}\) evolves homogeneously after \(S_2\).  Combining
(1.3) and (2.1) yields

\[
 \|z_t^{S_1}-z_t^{S_2}\|_\lambda
 \leq e^{-\lambda(t-S_2)}
       \frac{\|f\|_{\perp,\infty}}{\lambda}.              \tag{2.2}
\]

Thus \(z^S\) is Cauchy locally uniformly as \(S\to-\infty\).  Continuity of
the retarded equation on each method-of-steps interval shows that its limit
is a bounded complete classical solution.  This construction uses only
forward RFDE solutions.

If two bounded complete solutions existed, their difference \(w\) would
satisfy, for every \(s<t\),

\[
 \|w_t\|_\lambda
 \leq e^{-\lambda(t-s)}\|w_s\|_\lambda.
\]

The complete bound on \(w_s\) and the limit \(s\to-\infty\) force
\(w_t=0\).  Hence the causal Green operator

\[
 G_\perp:C_b(\mathbb R,E_{N,\perp})
 \longrightarrow C_b(\mathbb R,X_{N,\lambda})
\]

is well defined and

\[
 \|G_\perp\|\leq\frac1\lambda=10.                         \tag{2.3}
\]

The number ten is the norm bound for the retained-history component in
these declared spaces.  If the transverse differential operator is given
its classical graph domain

\[
 \mathcal D_\perp=
 \{z\in C_b(\mathbb R,E_{N,\perp})\cap C^1:
 L_\perp z\in C_b(\mathbb R,E_{N,\perp})\},
\]

then \(L_\perp:\mathcal D_\perp\to C_b\) is an isomorphism with the graph
norm.  Equation (2.3) is not advertised as a bound for that larger graph
norm.  At no point is the RFDE semiflow inverted backward.

## 3. Conditional canonical Lin transfer

The following transfer is an implication with explicit hypotheses.  Assume
independently that:

1. the scalar leaky RFDE has a complete synchronous canard connection wholly
   inside the voltage strip;
2. its phase-fixed scalar Lin operator on the declared domain and range is
   Fredholm;
3. its endpoint trace, phase condition, cokernel normalization and scalar
   gap \(d(\nu)\) are fixed;
4. the network Lin spaces use the product splitting induced by
   \(\pi^T\mathbf1=1\), all those auxiliary conditions act only on the
   collective block, and the transverse trace is bounded completeness;
5. the varied parameter and any inhomogeneity defining the gap are
   synchronous.

Under precisely these canonical choices, invariance and Section 2 give

\[
 \mathcal L_N
 =\mathcal L_\parallel\oplus\mathcal L_{\perp,N}.          \tag{3.1}
\]

The second summand is an isomorphism.  Therefore the full operator has the
same Fredholm index, kernel dimension and cokernel dimension as the scalar
block.  Extending the normalized scalar cokernel functional by zero on the
transverse range gives exactly

\[
 d_N(\nu)=d(\nu).                                         \tag{3.2}
\]

Consequently, if

\[
 d(\nu_c)=0,
 \qquad d'(\nu_c)\ne0,
\]

then the canonical synchronized network realization has the same root,
slope and orientation for every admitted finite topology.  The synchronous
nonlinear connection itself lifts because the synchronous restriction is
the scalar RFDE.

This conclusion does not cover independently chosen endpoint rules, a
noncollective phase or gap normalization, or asynchronous parameter
forcing.  It neither proves nonlinear persistence of an asynchronous
network connection nor excludes additional asynchronous roots.

## 4. Remaining scalar and biological gates

The scalar complete-history canard connection, the scalar Fredholm Lin
realization and its nonzero normalized gap slope remain open for this leaky
model.  Therefore this theorem does not establish an unconditional network
canard root, a nonlinear asynchronous canard, physical pulse onset, or a
pulse threshold.
