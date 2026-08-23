# Schur--Melnikov response of a special-flow history graph

Status: **Gate C calculus proved; the model-specific Gate C remains open.**
The exact block derivative, the derivative of a reduced complete-history gap,
the quantitative root lemmas, and the codimension-one statement for a
nonzero continuous response functional are proved below.  The
projection-neutral cubic theorem is conditional on the operator expansion
(5.3), the anisotropic Hessian bounds (5.9), and a nonzero model-specific
witness.  Those hypotheses are substantial Paper II proof obligations, not
consequences of the abstract Schur algebra.

The derivative-loss seam between the special-flow Picard jets and this block
calculus is closed abstractly in
[the Banach-scale linkage theorem](banach-scale-history-schur-link.md).
That result uses \(C_b^9\), \(C_b^8\), and \(C_b^7\) response levels and
does not assert a same-space \(C^2\) implicit-function theorem.  Its concrete
selected-trace and endpoint hypotheses still have to be verified for the
node-network model.

The theorem is written for the special-flow graph residual from
[special-flow-graph-theorem.md](special-flow-graph-theorem.md).  Any trace,
phase, and endpoint equations used to define the scalar matching gap are
first solved in a declared chart and are then included in the reduced gap
functional below.  This convention prevents endpoint and history terms from
being silently dropped.

## 1. Residual and reduced gap

Let

\[
 \mathcal X=\mathcal X_c\times\mathcal X_\perp,
 \qquad
 \mathcal Y=\mathcal Y_c\times\mathcal Y_\perp
\]

be real Banach spaces.  In the special-flow application, an element of
\(\mathcal X_c\) is the reduced vector field \(Q\), and an element of
\(\mathcal X_\perp\) is the stable graph \(H\).  Let \(\mathfrak R\) be a
real Banach space of structural perturbations.  Consider \(C^2\) maps

\[
 \mathbf G:\mathcal X\times\mathbb R\times\mathfrak R
 \longrightarrow\mathcal Y,
 \qquad
 \mathscr D:\mathcal X\times\mathbb R\times\mathfrak R
 \longrightarrow\mathbb R.
\tag{1.1}
\]

The first map is the graph residual

\[
 \mathbf G(Q,H;\mu,\mathcal R)
 =\binom{Q-\mathcal T_Q(Q,H;\mu,\mathcal R)}
 {H-\mathcal T_H(Q,H;\mu,\mathcal R)}.
\tag{1.2}
\]

The functional \(\mathscr D\) is the scalar, phase-normal matching gap after
the trace variables have been solved.  It is allowed to depend on \(H\) and
explicitly on \((\mu,\mathcal R)\).  Those two dependences contain, among
other things, complete-history, moving-section, and endpoint contributions.

Fix a base point

\[
 (Z_0,\mu_0,0),\qquad Z_0=(Q_0,H_0),\qquad
 \mathbf G(Z_0;\mu_0,0)=0.
\tag{1.3}
\]

At this point write

\[
 L=D_Z\mathbf G
 =\begin{pmatrix}\mathsf A&\mathsf B\\
                  \mathsf C&\mathsf D\end{pmatrix}.
\tag{1.4}
\]

Assume \(\mathsf D\) and

\[
 \mathsf S=\mathsf A-\mathsf B\mathsf D^{-1}\mathsf C
\tag{1.5}
\]

are bounded isomorphisms.  These hypotheses imply that \(L\) is a bounded
isomorphism.  The implicit-function theorem gives a unique local graph
\(Z(\mu,\mathcal R)\), and we define the reduced gap

\[
 d(\mu,\mathcal R)
 =\mathscr D(Z(\mu,\mathcal R);\mu,\mathcal R).
\tag{1.6}
\]

All derivatives in Sections 2--3 are evaluated at (1.3), unless another
point is displayed.

## 2. Exact Schur derivative

For a parameter direction \(\xi=(\dot\mu,\mathcal R)\), set

\[
 D_{(\mu,\mathcal R)}\mathbf G[\xi]
 =\binom{g_c[\xi]}{g_\perp[\xi]}.
\tag{2.1}
\]

### Theorem 2.1 -- block derivative of the invariant graph

The derivative \((\dot Q,\dot H)=DZ[\xi]\) is

\[
 \boxed{
 \begin{aligned}
 \dot Q={}&-\mathsf S^{-1}g_c[\xi]
 +\mathsf S^{-1}\mathsf B\mathsf D^{-1}g_\perp[\xi],\\
 \dot H={}&-\mathsf D^{-1}g_\perp[\xi]
 -\mathsf D^{-1}\mathsf C\dot Q.
 \end{aligned}}
\tag{2.2}
\]

**Proof.**  Differentiating \(\mathbf G(Z(\mu,\mathcal R);
\mu,\mathcal R)=0\) gives

\[
 \mathsf A\dot Q+\mathsf B\dot H=-g_c[\xi],
 \qquad
 \mathsf C\dot Q+\mathsf D\dot H=-g_\perp[\xi].
\tag{2.3}
\]

The second equation gives the formula for \(\dot H\).  Substitution into
the first equation gives

\[
 \mathsf S\dot Q=-g_c[\xi]
 +\mathsf B\mathsf D^{-1}g_\perp[\xi],
\]

which proves (2.2). \(\square\)

For later estimates, put

\[
 K_D=\|\mathsf D^{-1}\|,\qquad
 K_S=\|\mathsf S^{-1}\|,\qquad
 b=\|\mathsf B\|,\qquad c=\|\mathsf C\|.
\]

The exact inverse is

\[
 L^{-1}=
 \begin{pmatrix}
 \mathsf S^{-1}&-\mathsf S^{-1}\mathsf B\mathsf D^{-1}\\
 -\mathsf D^{-1}\mathsf C\mathsf S^{-1}&
 \mathsf D^{-1}+\mathsf D^{-1}\mathsf C\mathsf S^{-1}
 \mathsf B\mathsf D^{-1}
 \end{pmatrix}.
\tag{2.4a}
\]

With the sum norms

\[
 \|(x_c,x_\perp)\|=\|x_c\|_{\mathcal X_c}
 +\|x_\perp\|_{\mathcal X_\perp},\qquad
 \|(y_c,y_\perp)\|=\|y_c\|_{\mathcal Y_c}
 +\|y_\perp\|_{\mathcal Y_\perp},
\]

the block inverse satisfies

\[
 \boxed{
 \|L^{-1}\|\le K_L:=
 \max\left\{
 K_S(1+K_Dc),
 K_D+K_SbK_D(1+K_Dc)
 \right\}.}
\tag{2.4b}
\]

This follows by applying (2.2) to a general right-hand side with the signs
removed.  Thus dimension-uniform bounds for \(\mathsf D^{-1}\),
\(\mathsf S^{-1}\), \(\mathsf B\), and \(\mathsf C\) give a
dimension-uniform full graph inverse.

### Theorem 2.2 -- exact direct plus transverse gap derivative

Write

\[
 m_c=D_Q\mathscr D,\qquad m_\perp=D_H\mathscr D,\qquad
 \beta[\xi]=D_{(\mu,\mathcal R)}\mathscr D[\xi]
\tag{2.5}
\]

and introduce the effective critical gap covector

\[
 \widehat m=m_c-m_\perp\mathsf D^{-1}\mathsf C.
\tag{2.6}
\]

Before any block splitting, the full chain rule is

\[
 \boxed{
 Dd[\xi]=\beta[\xi]+m_c\dot Q+m_\perp\dot H.}
\tag{2.7a}
\]

Substitution of (2.2) gives the exact Schur form

\[
 \boxed{
 \begin{aligned}
 Dd[\xi]
 ={}&\underbrace{\beta[\xi]
 -\widehat m\mathsf S^{-1}g_c[\xi]}_{\mathcal L_{\rm dir}[\xi]}\\
 &+\underbrace{
 \left(\widehat m\mathsf S^{-1}\mathsf B-m_\perp\right)
 \mathsf D^{-1}g_\perp[\xi]
 }_{\mathcal L_{\rm tr}[\xi]}.
 \end{aligned}}
\tag{2.7b}
\]

The first line is the explicit/critical response.  The second line is the
transverse response.  It contains both the nonlinear return through
\(\mathsf B\) and a possible direct reading of the transverse graph by the
gap.

**Proof.**  Equation (2.7a) is the chain rule.  Using (2.2),

\[
\begin{aligned}
 Dd[\xi]
 &=\beta[\xi]+m_c\dot Q+m_\perp\dot H\\
 &=\beta[\xi]+(m_c-m_\perp\mathsf D^{-1}\mathsf C)\dot Q
 -m_\perp\mathsf D^{-1}g_\perp[\xi].
\end{aligned}
\]

Substitution of the first equation in (2.2) gives (2.7b). \(\square\)

If the reduced gap has no explicit parameter dependence and factors through
\(Q\), then \(\beta=0\), \(m_\perp=0\), and (2.7b) reduces to

\[
 Dd[\xi]
 =-m_c\mathsf S^{-1}g_c[\xi]
 +m_c\mathsf S^{-1}\mathsf B\mathsf D^{-1}g_\perp[\xi].
\tag{2.8}
\]

Formula (2.8), rather than the general formula (2.7b), was the short formula
in the initial
program document.  It is exact only under these two additional hypotheses.
In a complete-history problem, endpoint and moving-history terms must either
be shown to vanish or retained as \(\beta\) and \(m_\perp\).

The denominator in a root response is obtained from the same formula.  With
\(\xi=(1,0)\),

\[
 \partial_\mu d
 =\mathcal L_{\rm dir}[(1,0)]
 +\mathcal L_{\rm tr}[(1,0)].
\tag{2.9}
\]

There is no independent reason for replacing this derivative by a formal
whole-line integral unless the one-sided Green and endpoint calculation has
proved that representation.

### Trace and endpoint variables not already reduced

Formula (2.7b) assumes only that the trace and endpoint variables have already
been included in the definition of \(\mathscr D\).  If instead a trace
variable \(W\in\mathcal W\) is kept separate and is determined by

\[
 \mathbf T(W;Z,p)=0,\qquad p=(\mu,\mathcal R),
\tag{2.10}
\]

with \(D_W\mathbf T\) invertible, while the raw gap is
\(\mathcal J(Z,W,p)\), then

\[
 \dot W=-(D_W\mathbf T)^{-1}
 \left(D_Z\mathbf T\,\dot Z+D_p\mathbf T[\xi]\right)
\tag{2.11}
\]

and the most general chain rule is

\[
 \boxed{
 Dd[\xi]
 =D_p\mathcal J[\xi]+D_Z\mathcal J\,\dot Z
 +D_W\mathcal J\,\dot W.}
\tag{2.12}
\]

Equivalently, after solving \(W=W(Z,p)\), the reduced functional has

\[
\begin{aligned}
 D_Z\mathscr D
 &=D_Z\mathcal J-D_W\mathcal J
 (D_W\mathbf T)^{-1}D_Z\mathbf T,\\
 D_p\mathscr D
 &=D_p\mathcal J-D_W\mathcal J
 (D_W\mathbf T)^{-1}D_p\mathbf T.
\end{aligned}
\tag{2.13}
\]

Thus trace, endpoint, phase, and moving-section derivatives either appear
explicitly in (2.11)--(2.12), or are absorbed into \(m_c,m_\perp,\beta\) in
(2.7b) through (2.13).  They may not be omitted in both places.  If
\(D_W\mathbf T\) is not invertible, \(W\) must be retained in the augmented
Fredholm/Lyapunov--Schmidt residual rather than being called a reduced gap.

## 3. Derivative bounds inherited from the residual

The quadratic root estimate below uses derivatives of the reduced gap.  They
can be bounded directly from the residual, rather than introduced as an
untracked constant.

Let \(p=(\mu,\mathcal R)\) and suppose on a neighborhood of the solution
graph that

\[
 \|(D_Z\mathbf G)^{-1}\|\le K,\qquad
 \|D_p\mathbf G\|\le G_1,\qquad
 \|D^2\mathbf G\|\le G_2,
\tag{3.1}
\]

where the last norm is taken on
\((\mathcal X\times(\mathbb R\times\mathfrak R))^2\).  Put

\[
 Z_1=KG_1,\qquad
 Z_2=KG_2(1+Z_1)^2.
\tag{3.2}
\]

Implicit differentiation gives

\[
 \|DZ\|\le Z_1,\qquad \|D^2Z\|\le Z_2.
\tag{3.3}
\]

Indeed, the second derivative solves

\[
 D_Z\mathbf G\,D^2Z[p_1,p_2]
 =-D^2\mathbf G[(DZp_1,p_1),(DZp_2,p_2)].
\]

If

\[
 \|D\mathscr D\|\le J_1,\qquad
 \|D^2\mathscr D\|\le J_2,
\tag{3.4}
\]

then the composite gap satisfies

\[
 \boxed{
 \|Dd\|\le J_1(1+Z_1),\qquad
 \|D^2d\|\le
 M_d:=J_2(1+Z_1)^2+J_1Z_2.}
\tag{3.5}
\]

Together with (2.4b), this displays where the transverse inverse enters the
quadratic root constant.  The schematic expression
\(O(C_NG_N^2\|\mathcal R\|^2/m_N)\) is justified only after the quantities in
(3.1)--(3.4) have been bounded for the stated network class.

For the special-flow residual, (3.1)--(3.4) must not be verified by
asserting a same-space \(C^2\) map on one \(C_b^k\) space.  The valid
replacement is Theorem 5.1 and bounds (5.24)--(5.26) of
[the Banach-scale linkage note](banach-scale-history-schur-link.md), which
put first responses on \(C_b^8\), second responses on \(C_b^7\), and retain
the trace and endpoint Hessians explicitly.

## 4. A quantitative root lemma

The following elementary lemma fixes the radius and the constant hidden by a
quadratic implicit-function remainder.

### Lemma 4.1 -- explicit quadratic displacement

Let \(d:\mathbb R\times\mathfrak R\to\mathbb R\) be \(C^2\) on

\[
 \mathcal C=\{(\mu_0+x,\mathcal R):
 |x|\le r_\mu,\ \|\mathcal R\|\le r_R\},
\]

and suppose

\[
 d(\mu_0,0)=0,\qquad
 a=\partial_\mu d(\mu_0,0),\qquad |a|=m>0,
\tag{4.1}
\]

\[
 \sup_{\|\mathcal R\|\le r_R}
 \|D_\mathcal R d(\mu_0,\mathcal R)\|\le B,\qquad
 \sup_{\mathcal C}\|D^2d\|\le M.
\tag{4.2}
\]

Use the sum norm \(|x|+\|\mathcal R\|\) in (4.2), and set

\[
 \rho_0=\min\left\{
 r_R,\frac{mr_\mu}{2B},
 \frac{m}{2M(1+2B/m)}
 \right\},
\tag{4.3}
\]

where a quotient with zero denominator is interpreted as \(+\infty\).
For \(\|\mathcal R\|=r\le\rho_0\), there is a unique root in

\[
 |\mu-\mu_0|\le \frac{2B}{m}r.
\tag{4.4}
\]

Writing \(\ell=D_\mathcal R d(\mu_0,0)\), the root satisfies

\[
 \boxed{
 \left|
 \mu(\mathcal R)-\mu_0+\frac{\ell[\mathcal R]}{a}
 \right|
 \le
 \frac{M}{2m}\left(1+\frac{2B}{m}\right)^2r^2.}
\tag{4.5}
\]

**Proof.**  On the interval in (4.4), consider

\[
 \mathcal K_\mathcal R(x)
 =x-\frac{d(\mu_0+x,\mathcal R)}a.
\]

By (4.2),

\[
 |\mathcal K_\mathcal R(0)|
 \le Br/m,\qquad
 |\mathcal K_\mathcal R'(x)|
 \le \frac{M}{m}(|x|+r)\le\frac12.
\]

Thus \(\mathcal K_\mathcal R\) maps the interval (4.4) into itself and is
a contraction.  Its fixed point is the unique root there.  Taylor's formula
at \((\mu_0,0)\) gives

\[
 0=ax+\ell[\mathcal R]+E,\qquad
 |E|\le\frac M2(|x|+r)^2.
\]

Using (4.4) in this estimate proves (4.5). \(\square\)

## 5. Projection-neutral cubic law

Projection neutrality has to be imposed in a topology on which the residual
is differentiable.  For fixed delay support, a standard choice is the space
of finite operator-valued signed measures

\[
 \mathcal M_{\rm TV}([0,\Theta_*];\mathcal L(E_N))
\]

with the total-variation norm.  If delay atoms move, Dirac masses are not
continuous in this norm.  One must instead use a finite-dimensional atom
chart \((C_k,\theta_k)\), or let the measures act on a strong orbit space
with one history derivative and prove the corresponding composition
estimate.  No claim below treats a moving atom as a small perturbation in
the \(C^0\)-history operator norm.

Let \(\mathfrak R_{\rm ad}\subset\mathfrak R\) be the closed linear tangent
space cut out by the equality constraints which preserve the selected
equilibrium, fold, unfolding normalization, and all lower-order endpoint
jets.  Inequality constraints such as positivity are handled by taking the
base network in the interior and restricting to a sufficiently small ball in
this tangent space.  Assume that the first structural variation of the delay
measure is a bounded linear map

\[
 \Delta\mathbb B:\mathfrak R_{\rm ad}
 \longrightarrow
 \mathcal M_{\rm TV}([0,\Theta_*];\mathcal L(E_N)).
\]

Define the bounded linear projected-measure map

\[
 \Pi_\parallel:\mathfrak R_{\rm ad}
 \longrightarrow\mathcal M_{\rm TV}([0,\Theta_*]),\qquad
 \Pi_\parallel(\mathcal R)
 =\ell_N^\top\bigl(\Delta\mathbb B[\mathcal R]\bigr)(\,\cdot\,)r_N,
\tag{5.1}
\]

and the projection-neutral Banach space

\[
 \mathfrak R_0=\ker\Pi_\parallel\cap\mathfrak R_{\rm ad}.
\tag{5.2}
\]

Because \(\Pi_\parallel\) is bounded and linear, \(\mathfrak R_0\) is a
closed linear Banach subspace of \(\mathfrak R_{\rm ad}\).  This is
neutrality of the complete projected delay measure.  Equality of one scalar
delay moment is weaker and does not imply (5.2).

For \(0<\delta\le\delta_0\), let \(d_\delta\) be a normalized reduced gap,
let \(\mu_\delta^0\) be its unperturbed simple root, and put

\[
 a_\delta=\partial_\mu d_\delta(\mu_\delta^0,0).
\]

The mixed-jet calculation required by Paper II must establish the operator
expansion

\[
 D_\mathcal R d_\delta(\mu_\delta^0,0)[\mathcal R]
 =\delta^2\lambda_{2,N}
   [\Pi_\parallel\mathcal R]
 +\delta^3\mathcal L_{3,N}[\mathcal R]
 +E_{4,\delta,N}[\mathcal R],
\tag{5.3}
\]

with

\[
 \|E_{4,\delta,N}\|\le E_4\delta^4.
\tag{5.4}
\]

Here (5.4) is the operator norm in
\(\mathcal L(\mathfrak R_{\rm ad},\mathbb R)\), uniformly in every
quantifier, including \(N\), for which a scalable theorem is claimed.

The factorization of the entire \(\delta^2\) functional through
\(\Pi_\parallel\) is part of (5.3); it is not a consequence of notation.
It includes the direct graph, history, phase, and endpoint jets.  On
\(\mathfrak R_0\), equation (5.3) becomes

\[
 D_\mathcal R d_\delta(\mu_\delta^0,0)[\mathcal R]
 =\delta^3\mathcal L_{3,N}[\mathcal R]
 +E_{4,\delta,N}[\mathcal R].
\tag{5.5}
\]

The exact formula (2.7b) splits the cubic functional as

\[
 \mathcal L_{3,N}
 =\mathcal L_{3,N}^{\rm dir}
 +\mathcal L_{3,N}^{\rm tr},
\tag{5.6}
\]

where

\[
\begin{aligned}
 \mathcal L_{3,N}^{\rm dir}
 &=\operatorname {coef}_{\delta^3}
 \left(\beta-\widehat m\mathsf S^{-1}g_c\right),\\
 \mathcal L_{3,N}^{\rm tr}
 &=\operatorname {coef}_{\delta^3}
 \left[
 (\widehat m\mathsf S^{-1}\mathsf B-m_\perp)
 \mathsf D^{-1}g_\perp
 \right].
\end{aligned}
\tag{5.7}
\]

Every coefficient in (5.7) is taken after the mixed graph and trace jets
have been proved in a common Banach scale.  When the complete direct
critical measure and all direct endpoint jets are also fixed,
\(\mathcal L_{3,N}^{\rm dir}=0\), and the coefficient is the pure
transverse-resolvent/nonlinear-return functional.  Projection neutrality by
itself only removes the factored quadratic term in (5.3).

### Theorem 5.1 -- cubic root response with explicit constants

Assume, uniformly for \(0<\delta\le\delta_0\), that there is a declared
limiting normalization \(a_0\), independent of \(\delta\), for which

\[
 |a_\delta|\ge m,\qquad |a_0|\ge m,\qquad
 |a_\delta-a_0|\le A_1\delta,
\tag{5.8}
\]

and on

\[
 |\mu-\mu_\delta^0|\le r_\mu,\qquad
 \mathcal R\in\mathfrak R_0,\quad\|\mathcal R\|\le r_R,
\]

that

\[
 |\partial_{\mu\mu}d_\delta|\le M_{00},\qquad
 \|D_{\mu\mathcal R}d_\delta\|\le M_{01}\delta^3,\qquad
 \|D_{\mathcal R\mathcal R}d_\delta\|\le M_{11}\delta^3.
\tag{5.9}
\]

The last two norms are the operator norms of the indicated bounded bilinear
maps on \(\mathbb R\times\mathfrak R_0\) and
\(\mathfrak R_0\times\mathfrak R_0\), respectively.  All three suprema in
(5.9) are over the displayed cylinder and over the same values of
\((\delta,N)\) covered by the theorem.

Let \(L_3=\|\mathcal L_{3,N}\|\) and set

\[
 B_3=L_3+E_4\delta_0+M_{11}r_R,\qquad
 C_x=\frac{2B_3}{m},
\tag{5.10}
\]

\[
 \rho_3=\min\left\{
 r_R,
 \frac{mr_\mu}{2B_3\delta_0^3},
 \frac{m}{2\delta_0^3(M_{01}+2M_{00}B_3/m)}
 \right\},
\tag{5.11}
\]

again interpreting a zero denominator as \(+\infty\).  For
\(\mathcal R\in\mathfrak R_0\), \(r=\|\mathcal R\|\le\rho_3\), there is a
unique root in the interval

\[
 |\mu_\delta(\mathcal R)-\mu_\delta^0|
 \le C_x\delta^3r.
\tag{5.12}
\]

Define the Schur--Melnikov root functional

\[
 \mathfrak M_N=-\frac{\mathcal L_{3,N}}{a_0}.
\tag{5.13}
\]

Then

\[
 \boxed{
 \begin{aligned}
 &\left|
 \mu_\delta(\mathcal R)-\mu_\delta^0
 -\delta^3\mathfrak M_N[\mathcal R]
 \right|\\
 &\hspace{12mm}\le
 C_{\rm lin}\delta^4r+C_{\rm quad}\delta^3r^2,
 \end{aligned}}
\tag{5.14}
\]

with the explicit constants

\[
 C_{\rm lin}=\frac{E_4}{m}+\frac{L_3A_1}{m^2},
\tag{5.15}
\]

\[
 C_{\rm quad}=\frac1m\left[
 \frac{M_{11}}2+
\delta_0^3\left(M_{01}C_x+\frac{M_{00}C_x^2}{2}\right)
 \right].
\tag{5.16}
\]

If the constants in (5.3)--(5.11) are independent of \(N\), so are the
root radius and remainder in (5.14).

**Proof.**  From (5.5), (5.9), and the fundamental theorem of calculus,

\[
 \sup_{\|\mathcal R\|\le r_R}
 \|D_\mathcal R d_\delta(\mu_\delta^0,\mathcal R)\|
 \le B_3\delta^3.
\tag{5.17}
\]

Apply the contraction argument of Lemma 4.1 on the smaller interval
\(|x|\le C_x\delta^3r\).  The derivative of its fixed-point map is bounded
by

\[
 \frac1m\left(M_{00}C_x\delta^3r+M_{01}\delta^3r\right)
 \le\frac12
\]

because of (5.11), and (5.17) gives the self-map estimate.  This proves
(5.12) and uniqueness in the displayed interval.

Taylor's formula with the anisotropic bounds (5.9) gives, for
\(x=\mu_\delta(\mathcal R)-\mu_\delta^0\),

\[
\begin{aligned}
 0={}&a_\delta x+\delta^3\mathcal L_{3,N}[\mathcal R]
 +E_{4,\delta,N}[\mathcal R]+E_{\rm nl},\\
 |E_{\rm nl}|\le{}&
 \frac{M_{00}}2x^2+M_{01}\delta^3|x|r
 +\frac{M_{11}}2\delta^3r^2.
\end{aligned}
\tag{5.18}
\]

Use (5.12), (5.4), and

\[
 \left|\frac1{a_\delta}-\frac1{a_0}\right|
 \le\frac{A_1\delta}{m^2}
\]

in (5.18).  The linear terms give (5.15); the three nonlinear terms give
(5.16).  This proves (5.14). \(\square\)

The bound \(D_{\mathcal R\mathcal R}d_\delta=O(\delta^3)\) in (5.9) is
essential for the \(\delta^3r^2\) remainder.  A generic \(C^2\) implicit
function theorem only gives \(O(r^2)\), which is too weak for (5.14).

## 6. Codimension-one genericity

### Theorem 6.1 -- the exceptional set is a closed hyperplane

Assume \(\mathfrak R_0\ne\{0\}\) and that the coefficient
\(\mathfrak M_N\in\mathfrak R_0^*\) in (5.13) is continuous.  If there is
one admissible witness \(\mathcal R_*\in\mathfrak R_0\) for which

\[
 \mathfrak M_N[\mathcal R_*]\ne0,
\tag{6.1}
\]

then

\[
 \mathcal E_N=\ker\mathfrak M_N
\tag{6.2}
\]

is a closed linear subspace of codimension one in \(\mathfrak R_0\).  Its
complement is open and dense.  Consequently a nonzero cubic root response is
generic relative to the projection-neutral admissible tangent space.

**Proof.**  Continuity makes (6.2) closed.  For any
\(\mathcal R\in\mathfrak R_0\),

\[
 \mathcal R=
 \left(\mathcal R-
 \frac{\mathfrak M_N[\mathcal R]}
 {\mathfrak M_N[\mathcal R_*]}\mathcal R_*\right)
 +\frac{\mathfrak M_N[\mathcal R]}
 {\mathfrak M_N[\mathcal R_*]}\mathcal R_*.
\]

The first summand is in \(\mathcal E_N\), so
\(\mathfrak R_0/\mathcal E_N\) is one-dimensional.  The complement is open
by continuity.  It is dense because every point of the kernel can be
perturbed by an arbitrarily small nonzero multiple of \(\mathcal R_*\).
\(\square\)

This is a fixed-\(N\) statement.  Uniform genericity along a graph sequence
requires normalized witnesses with a uniform lower bound
\(|\mathfrak M_N[\mathcal R_{*,N}]|\ge c>0\); codimension one for every
individual \(N\) does not supply that bound.

If positivity or another biological constraint defines an open subset of
the affine network space and the base network is an interior point, the same
conclusion holds relative to a sufficiently small admissible ball.  At a
boundary point of a cone, a two-sided Banach tangent space may contain
directions that are not feasible; Theorem 6.1 must not be quoted there
without replacing the tangent space by the appropriate one-sided statement.

## 7. Audit of the older direct-sum route

The exact formula (2.7b) resolves the apparent conflict with the older
full-network direct-sum specification.

Suppose at the coefficient-bearing reference point that

\[
 \mathsf B=\mathsf C=0,\qquad
 \beta[\mathcal R]=0,\qquad m_\perp=0,\qquad
 g_c[\mathcal R]=0.
\tag{7.1}
\]

Then (2.7b) gives

\[
 D_\mathcal R d[\mathcal R]=0
\tag{7.2}
\]

for every transverse forcing \(g_\perp[\mathcal R]\).  Hence a strict
critical/transverse direct sum, combined with a critical-only gap and a
projection-neutral perturbation, cannot produce a first-order transverse
return.  This is an algebraic zero, not a missing estimate.

There are three consistent uses of a direct-sum calculation.

1. It may establish the Fredholm index and inverse of a leading operator
   \(L_0\).  The coefficient-bearing operator is then
   \(L_\delta=L_0+\delta L_1+\cdots\), with a nonzero off-diagonal return
   block.  Formula (2.7b) is applied to \(L_\delta\), not to the strict sum
   \(L_0\).
2. A strict sum can produce a response if the gap directly reads the
   transverse component, \(m_\perp\ne0\), or if the endpoint functional has
   explicit perturbation dependence, \(\beta\ne0\).  That is a different
   mechanism and must be named.
3. For multiple center directions, the full Lin--Fredholm problem can still
   be used to count the vector gap.  Its block-index theorem does not by
   itself calculate the scalar Schur return.

Thus the direct-sum theorem target in
[full-network-lin-operator.md](full-network-lin-operator.md) is not false as
an index criterion.  It is insufficient, and under (7.1) incompatible, with
the nonzero coefficient mechanism.  The active one-critical-mode Paper II
route must retain the off-diagonal graph block \(\mathsf B\), at least at the
first order at which the transverse response returns to the critical field.

## 8. What the Gate C calculus proves and what the model theorem still needs

The following statements are proved in this note.

1. The graph derivative is the block Schur formula (2.2).
2. The complete reduced-gap derivative is (2.7a)--(2.7b), including explicit,
   transverse-observation, history, and endpoint terms.
3. Under the operator expansion (5.3) and the anisotropic derivative bounds,
   projection-neutral perturbations have the cubic root law (5.14), with the
   constants (5.15)--(5.16).
4. One nonzero admissible witness makes the exceptional zero-coefficient set
   a closed codimension-one hyperplane.
5. A strict direct sum with a critical-only gap kills the proposed transverse
   mechanism exactly.

For a Paper II network theorem, the following remain model-dependent proof
obligations.

1. Realize the abstract
   [three-level linkage theorem](banach-scale-history-schur-link.md) in
   concrete selected-trace and endpoint spaces for the node network.  The
   graph-side derivative loss and levelwise Schur algebra are proved there;
   the trace inverse, moving endpoints, and complete-history matcher remain
   model-specific.
2. Bound \(K_D,K_S,b,c,G_1,G_2,J_1,J_2\) uniformly in the admitted network
   family.
3. Derive (5.3), including the complete-measure factorization of its
   \(\delta^2\) term and all trace/endpoint contributions.
4. Verify (5.9); ordinary unscaled \(C^2\) regularity is not enough.
5. Evaluate \(\mathcal L_{3,N}\) by the phase-normal Green/adjoint pairing
   and provide a nonzero admissible witness.

The exact finite-dimensional regression in
`src/canard_control/block_schur_response.py` checks (2.2), (2.7b), the
direct-sum zero, and a synthetic projection-neutral cubic scaling with
rational/symbolic arithmetic.  It is a sign and block-order audit, not an
RFDE proof.
