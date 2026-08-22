# A uniform special-flow history graph for the singular RFDE chart

Status: **Lipschitz graph proved here; the application-required finite mixed
jets are proved in a companion note.** Steps 1--3 construct the unique bounded
Lipschitz special-flow graph. The common Banach fibers, convergence estimates,
and uniform third-order fixed-tube Taylor remainder needed by the final model
are completed in
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md). The arbitrary-order
version of Theorem target 1 below is not claimed.

The proof is constructive. It does not cite a fixed-parameter RFDE center
manifold theorem across the singular limit. The latter would be invalid here
because the scaled transverse generator contains \(A/\delta\). The regularity
argument follows the fiber-contraction strategy used for parameterization
equations by Yang, Gimeno, and de la Llave (2021). The application-specific
finite-scale proof is separated from the arbitrary-order target below so that
the two statements cannot be confused.

## 1. Abstract system and assumptions

Fix delays

\[
 0\leq \theta_j\leq\Theta,\qquad j=1,\ldots,N,
\]

and a compact parameter set \(P\Subset\mathbb R^a\). Let
\(u\in\mathbb R^d\), \(h\in\mathbb R^m\), and consider

\[
\begin{aligned}
 u'(s)&=q_0(u(s))
 +\delta F\!\left(
 u(s),h(s),
 (u(s-\theta_j),h(s-\theta_j))_{j=1}^N;
 \delta,p\right),\\
 \delta h'(s)&=Ah(s)
 +\delta G\!\left(
 u(s),h(s),
 (u(s-\theta_j),h(s-\theta_j))_{j=1}^N;
 \delta,p\right).
\end{aligned}
\tag{1}
\]

We impose the following hypotheses.

1. \(A\in\mathbb R^{m\times m}\) is Hurwitz. Fix
   \(M_A,\beta>0\) such that

   \[
     \|e^{Ar}\|\leq M_Ae^{-\beta r},\qquad r\geq0.
   \tag{2}
   \]

2. After a smooth cutoff outside a prescribed compact flow tube,
   \(q_0,F,G\in C_b^R\). The parameter-dependent functions extend to an
   open neighborhood of \([ -\delta_*,\delta_*]\times P\), and all mixed
   derivatives through order \(R\) are bounded there. (The extension to
   negative \(\delta\) is used only for Taylor estimates; the RFDE is
   considered for \(\delta>0\).)

3. The cutoff \(q_0\), and every vector field in a sufficiently small
   \(C^1\) neighborhood of it, generates a complete two-sided flow.

4. Every delayed dependence in the \(u\)-equation carries the displayed
   external factor \(\delta\). The stable equation has exactly the form in
   (1); in particular, \(A\) is independent of \(\delta\).

The cutoff is a proof device. In the application it is chosen to equal the
physical polynomial vector field on a compact set containing the selected
entry-to-exit orbit and all of its delay backtracks. No conclusion below is
claimed outside that set.

For a complete vector field \(Q\), denote its flow by \(\Phi_Q^s\), and set

\[
 \mathcal E_{Q,H}(u)=\left(
 u,H(u),
 \bigl(\Phi_Q^{-\theta_j}u,
 H(\Phi_Q^{-\theta_j}u)\bigr)_{j=1}^N
 \right).
\tag{3}
\]

## 2. The graph theorem target

**Theorem target 1 (arbitrary finite-order weak-delay special-flow graph).** Fix finite integers
\(s\geq2\) and \(N_*\geq1\), and suppose
\(R\geq s+N_*+5\). Then there are
\(\delta_0,C,C_{N_*}>0\) such that, for
\(0<\delta\leq\delta_0\) and \(p\in P\), there is a unique pair

\[
 Q_{\delta,p}\in C_b^s(\mathbb R^d,\mathbb R^d),\qquad
 H_{\delta,p}\in C_b^s(\mathbb R^d,\mathbb R^m)
\]

in the fixed contraction neighborhood satisfying

\[
 \|Q_{\delta,p}-q_0\|_{C^1}
 +\|H_{\delta,p}\|_{C^1}\leq C\delta
\tag{4}
\]

and the nonlocal invariance equations

\[
\begin{aligned}
 Q(u)&=q_0(u)+\delta
 F(\mathcal E_{Q,H}(u);\delta,p),\\
 \delta DH(u)Q(u)&=AH(u)+\delta
 G(\mathcal E_{Q,H}(u);\delta,p).
\end{aligned}
\tag{5}
\]

The map

\[
 \iota_{\delta,p}(u)(\vartheta)=
 \left(\Phi_Q^\vartheta u,
 H(\Phi_Q^\vartheta u)\right),
 \qquad -\Theta\leq\vartheta\leq0,
\tag{6}
\]

is a \(C^s\) injective embedding into
\(C([-\Theta,0],\mathbb R^{d+m})\), and the RFDE semiflow satisfies

\[
 \mathcal S_t\iota_{\delta,p}(u)
 =\iota_{\delta,p}(\Phi_Q^tu)
\tag{7}
\]

whenever the current points and every delayed backtrack in the corresponding
special-flow segment stay in the uncut flow tube.

If \(p=(\eta,\widehat p)\), then \((Q,H)\) are \(C^2\) in \(\eta\).
Moreover, they possess uniform expansions

\[
\begin{aligned}
 Q_{\delta,p}
 &=q_0+\sum_{j=1}^{N_*}\delta^jQ_j(p)
 +R_Q^{(N_*)},\\
 H_{\delta,p}
 &=\sum_{j=1}^{N_*}\delta^jH_j(p)
 +R_H^{(N_*)},
\end{aligned}
\tag{8}
\]

with

\[
 \max_{0\leq k\leq2}\left(
 \|\partial_\eta^kR_Q^{(N_*)}\|_{C^s}
 +\|\partial_\eta^kR_H^{(N_*)}\|_{C^s}
 \right)
 \leq C_{N_*}\delta^{N_*+1}.
\tag{9}
\]

If \(\phi_0^s\) is the flow of \(q_0\) and

\[
 \mathcal E_0(u)=\left(
 u,0,(\phi_0^{-\theta_j}u,0)_{j=1}^N
 \right),
\]

then the first coefficients are

\[
 Q_1(u,p)=F(\mathcal E_0(u);0,p),\qquad
 H_1(u,p)=-A^{-1}G(\mathcal E_0(u);0,p).
\tag{10}
\]

### Proof status

Steps 1--3 prove existence and uniqueness of the Lipschitz fixed point and its
exact special-flow solutions. Steps 4--5 give the additional finite-jet proof
scheme required for the full theorem target; that upgrade is not yet closed
at publication level. Step 6 gives the history embedding at the regularity
supplied by the preceding steps.

#### Step 1: a derivative-free fixed-point equation

For bounded Lipschitz \((Q,H)\), define

\[
\begin{aligned}
 \mathcal T_Q(Q,H)(u)
 &=q_0(u)+\delta F(\mathcal E_{Q,H}(u);\delta,p),\\
 \mathcal T_H(Q,H)(u)
 &=\delta\int_0^\infty e^{Ar}
 G\!\left(
 \mathcal E_{Q,H}(\Phi_Q^{-\delta r}u);
 \delta,p\right)\,dr.
\end{aligned}
\tag{11}
\]

The integral is absolutely convergent. Indeed, the integrand is bounded and
(2) gives

\[
 \|\mathcal T_H(Q,H)\|_\infty
 \leq \delta\frac{M_A}{\beta}\|G\|_\infty.
\tag{12}
\]

Likewise,

\[
 \|\mathcal T_Q(Q,H)-q_0\|_\infty
 \leq\delta\|F\|_\infty.
\tag{13}
\]

Choose \(L>\operatorname {Lip}(q_0)\). For constants \(b_Q,b_H\), to be
fixed independently of \(\delta\), let \(\mathscr B_\delta\) be the set of
bounded Lipschitz pairs satisfying

\[
\begin{split}
 \|Q-q_0\|_\infty+\operatorname {Lip}(Q-q_0)&\leq b_Q\delta,\\
 \|H\|_\infty+\operatorname {Lip}(H)&\leq b_H\delta,
 \qquad \operatorname {Lip}(Q)\leq L.
\end{split}
\tag{B}
\]

This is a closed, hence complete, subset in the uniform product metric.
For \(0\leq t\leq\Theta\), the initial-value estimate
\(\operatorname {Lip}(\Phi_Q^{-t})\leq e^{Lt}\), together with (12)--(13),
gives

\[
\begin{split}
 \operatorname {Lip}(\mathcal T_Q-q_0)&\leq C\delta,\\
 \operatorname {Lip}(\mathcal T_H)&\leq
 C\delta\int_0^\infty
 e^{-(\beta-L\delta)r}\,dr.
\end{split}
\tag{B1}
\]

First choose \(b_Q,b_H\) larger than these uniform constants and then take
\(\delta_0\) small. Thus \(\mathcal T\) maps
\(\mathscr B_\delta\) into itself. The advantage of (11) over the
differential invariance equation is that it contains no derivative of the
unknown graph \(H\).

#### Step 2: uniform contraction

If \(Q,\widetilde Q\) have Lipschitz constant at most \(L\), Gronwall's
inequality gives, for \(t\geq0\),

\[
 \sup_u|\Phi_Q^{-t}u-\Phi_{\widetilde Q}^{-t}u|
 \leq te^{Lt}\|Q-\widetilde Q\|_\infty.
\tag{14}
\]

Using (14), the uniform Lipschitz bounds on \(F,G,H\), and the fact that the
 delayed arguments occur at times \(\theta_j+\delta r\), we obtain

\[
 \|\mathcal T_Q(Q,H)-
 \mathcal T_Q(\widetilde Q,\widetilde H)\|_\infty
 \leq C_1\delta
 \bigl(\|Q-\widetilde Q\|_\infty+
 \|H-\widetilde H\|_\infty\bigr).
\tag{15}
\]

For the stable component, the only additional factors are bounded by

\[
 e^{-\beta r}e^{L\delta r}
 \left(1+\Theta+\delta r\right).
\]

Choose \(\delta_0\) so that \(L\delta_0\leq\beta/2\). Then all relevant
integrals are bounded uniformly and

\[
 \|\mathcal T_H(Q,H)-
 \mathcal T_H(\widetilde Q,\widetilde H)\|_\infty
 \leq C_2\delta
 \bigl(\|Q-\widetilde Q\|_\infty+
 \|H-\widetilde H\|_\infty\bigr).
\tag{16}
\]

Taking \(\delta_0\) smaller if necessary gives
\(\kappa=(C_1+C_2)\delta_0<1\). Banach's fixed-point theorem now yields a
unique bounded Lipschitz pair \((Q,H)\) in the declared ball.

#### Step 3: equivalence with the invariance equation

Let \(u(t)=\Phi_Q^t u_0\), \(h(t)=H(u(t))\), and abbreviate the stable
forcing along this orbit by \(g(t)\). The second fixed-point equation is

\[
 h(t)=\int_{-\infty}^t
 e^{A(t-r)/\delta}g(r)\,dr.
\tag{17}
\]

Because \(g\) is bounded and continuous, the convolution in (17) is
continuously differentiable as a function of orbit time, and differentiation
gives

\[
 h'(t)=\frac1\delta Ah(t)+g(t).
\]

The first fixed-point equation gives the \(u\)-equation in (1). Thus the curve
\((u(t),H(u(t)))\) is an exact solution of the RFDE already at the Lipschitz
graph level. The pointwise graph PDE in (5) follows only after the spatial
\(C^1\) upgrade.

Conversely, suppose that a bounded \(C^1\) pair in
\(\mathscr B_\delta\) satisfies (5). Integrating its stable equation along
the complete orbit from \(-T\) to zero gives

\[
 H(u)=e^{AT/\delta}H(\Phi_Q^{-T}u)
 +\int_{-T}^0e^{-Ar/\delta}
 G(\mathcal E_{Q,H}(\Phi_Q^r u);\delta,p)\,dr.
\]

The first term tends uniformly to zero as \(T\to\infty\). Changing variables
in the integral recovers the second equation in (11). Thus every bounded
solution of (5) in the declared neighborhood is the fixed point already
constructed, which proves uniqueness of the bounded fixed point in the
declared Lipschitz ball. The arbitrary-order regularity assertions of Theorem
target 1 still depend on Lemma target 2; the finite orders used by the final
model are proved in the companion note.

#### Step 4: the general mixed-jet target and its proved finite-scale case

A same-order \(C^s\) Banach implicit-function theorem is not applicable:
the map \(Q\mapsto H\circ\Phi_Q^{-\theta}\) loses a derivative. We therefore
record the finite-order jet argument used here. For a \(C^k\) map \(f\), put

\[
 \|f\|_{k,1}=\max_{0\leq j\leq k}\|D^jf\|_\infty
 +\operatorname {Lip}(D^kf).
\]

**Lemma target 2 (general mixed jets of the graph transform).** Let
\(J=s+N_*+3\). On every bounded \(C_b^{J+1,1}\) ball of vector fields there
are constants \(C_j,\Gamma_j\), \(0\leq j\leq J\), such that

\[
 \|D_u^j\Phi_Q^t\|_\infty
 \leq C_j(1+|t|^j)e^{\Gamma_j|t|},
\tag{L1}
\]

and, for \(Q,\widetilde Q\) in that ball,

\[
\begin{split}
 \|D_u^j\Phi_Q^t-D_u^j\Phi_{\widetilde Q}^t\|_\infty
 \leq{}&C_j(1+|t|^{j+1})e^{\Gamma_j|t|}\\
 &\times\left(
 \|D^jQ-D^j\widetilde Q\|_\infty
 +\|Q-\widetilde Q\|_{C^{j-1}}
 \right),
\end{split}
\tag{L2}
\]

where the last term is omitted for \(j=0\). For the iterates
\((Q_{n+1},H_{n+1})=\mathcal T(Q_n,H_n)\), all mixed jets

\[
 D_u^a\partial_\delta^b\partial_\eta^c(Q_n,H_n),
 \qquad a\leq s,\quad b\leq N_*+1,\quad c\leq2,
\tag{L3}
\]

converge uniformly. Their limits are the corresponding derivatives of the
fixed point, and their norms are bounded uniformly for
\(|\delta|\leq\delta_0\) and \(p\in P\).

To prove the lemma, differentiate the flow equation. The first variation is
bounded by Gronwall's inequality. At order \(j\), the only term containing
the highest derivative of the vector field is

\[
 D^jQ(\Phi_Q^t)
 [D\Phi_Q^t,\ldots,D\Phi_Q^t];
\]

all other terms contain lower derivatives. Induction and Gronwall give
(L1). Subtracting the two variational equations gives (L2); the common
Lipschitz bound on \(D^jQ\) controls its evaluation at the two different
orbits. This explains why one unused spatial Lipschitz derivative is kept.

For a parameter-dependent flow, the same differentiated variational
equations separate the term linear in the highest parameter jet of \(Q\).
If \(\mathscr D\) has total order at most \(J\), then there is an integer
\(M_J\), depending only on \(J\), such that, after all lower jets have been
bounded, evaluation at \(t=-(\theta_j+\delta r)\) gives

\[
 C_J(1+r^{M_J})e^{\Gamma_J(\Theta+|\delta|r)}
 \left(1+\|\mathscr D Q\|_\infty\right).
\tag{L4}
\]

Choose \(\delta_0\) so that
\(\Gamma_J\delta_0<\beta/2\). The part independent of the highest jet,
after multiplication by the kernel in (11), has the integrable majorant
\(C(1+r^{M_J})e^{-\beta r/2}\). The part linear in the highest jet is retained
in the fiber operator below. Thus differentiation under the integral is
valid for every finite iterate and every jet in (L3).

It remains to prove convergence, rather than merely boundedness, of those
jets. Order them by total order \(a+b+c\), with the spatial order used to
break ties. Faà di Bruno's formula writes each highest jet of the new iterate
in the form

\[
 \mathscr D(Q_{n+1},H_{n+1})
 =\mathcal A_{\mathscr D,n}
   \mathscr D(Q_n,H_n)+\mathcal B_{\mathscr D,n}.
\tag{L5}
\]

Here \(\mathcal B_{\mathscr D,n}\) contains only lower jets and converges by
induction. Every occurrence of the highest old jet in
\(\mathcal A_{\mathscr D,n}\) retains the external factor \(\delta\) from
(11), and (L1)--(L4) give

\[
\|\mathcal A_{\mathscr D,n}\|\leq C_J|\delta|.
\tag{L6}
\]

Before taking differences, the same decomposition gives

\[
 \|\mathscr D(Q_{n+1},H_{n+1})\|_\infty
 \leq C_J|\delta|\,
 \|\mathscr D(Q_n,H_n)\|_\infty+C_{\mathscr D},
\tag{L6a}
\]

where \(C_{\mathscr D}\) depends only on already bounded lower jets. Once the
common jet fibers and operators in Lemma target 2 are defined, induction from
\((q_0,0)\) in the chosen ordering would provide invariant jet balls through
total order \(J+1\). Applying the estimate once more to spatial difference
quotients and using the \(R\)-th derivative of the data would give the common
top-order Lipschitz bound.

If a \(\delta\)-derivative falls on that external factor, the remaining
composition contains at most \(b-1\) parameter derivatives and hence belongs
to \(\mathcal B_{\mathscr D,n}\); it does not alter (L6). Taking
\(C_J\delta_0<1\), the proposed affine fiber recurrence (L5) would be a
contraction over the order-zero base proved in Step 2. Subject to the missing
operator definitions and convergence bounds, the fiber estimate would then
give uniform convergence of every jet in (L3), while
\(R\geq J+2=s+N_*+5\) supplies the additional derivative and Lipschitz
budget. This identifies the required fiber-contraction mechanism but is not
yet its complete implementation. To promote it to a proof of Lemma
target 2, the common jet fiber, the operators
\(\mathcal A_{\mathscr D,n}\), and convergence of their coefficients must be
defined and bounded explicitly at every mixed order. Once that bookkeeping is
closed, the argument yields the \(C^s\) assertion, the \(C^2\) dependence on
\(\eta\), and (4).

For the finite rectangular jet family actually used below—three spatial and
three \(\delta\) derivatives and two \(\eta\) derivatives—Theorem 1 of
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md) defines the common
fibers, proves their affine highest-block contractions, and establishes
strong convergence. Thus this application case is a theorem; the preceding
paragraph concerns only the more general arbitrary-order target.

#### Step 5: \(\delta\)-jets and their uniform remainders

For this step use (11) itself, not the singularly rescaled unknown
\(H/\delta\). As an operator, (11) extends to negative \(\delta\) near zero;
the extension is only a device for two-sided Taylor's theorem. At
\(\delta<0\), the ball (B) and all estimates are read with
\(|\delta|\) in place of \(\delta\). At \(\delta=0\) the operator is the
constant map

\[
 \mathcal T_{0,p}(Q,H)=(q_0,0).
\]

Under Lemma target 2, the fixed point is \(C^{N_*+1}\) in \(\delta\) with
values in \(C_b^s\), including after zero, and gives uniform bounds on the
same derivatives after applying \(\partial_\eta^k\), \(0\leq k\leq2\).
Set

\[
 Q_j=\frac1{j!}\partial_\delta^jQ_{\delta,p}\big|_{\delta=0},
 \qquad
 H_j=\frac1{j!}\partial_\delta^jH_{\delta,p}\big|_{\delta=0}.
\]

The integral form of Taylor's theorem gives, for either component and for
\(0\leq k\leq2\),

\[
 \partial_\eta^kR^{(N_*)}(\delta,p)
 =\frac{\delta^{N_*+1}}{N_*!}
 \int_0^1(1-t)^{N_*}
 \partial_\delta^{N_*+1}\partial_\eta^k
 (Q,H)(t\delta,p)\,dt.
\tag{L7}
\]

The target uniform mixed-jet bound would prove (8)--(9). For the final model's
third-order expansion, the companion finite-scale theorem supplies this
bound. Differentiating (11) once at \(\delta=0\), and using
\(\int_0^\infty e^{Ar}\,dr=-A^{-1}\), gives exactly (10).

#### Step 6: complete-history embedding

At the Lipschitz level, evaluation at the present time followed by projection
to the \(u\)-coordinates returns \(u\), so \(\iota\) is injective and the
integral equation gives the exact special-flow orbit. For the final model,
the companion theorem upgrades (6) to a \(C^3\) embedding with injective
derivative. Higher arbitrary orders remain conditional on Lemma target 2.

## 3. Exact application to the final two-module chart

The exact chart is recorded in
[`final-model-blowup.md`](final-model-blowup.md). Make the shifts

\[
 \widehat Z=Z+\frac\alpha2X^2,\qquad
 \widehat W=W+\frac{\alpha}{2D_w}X^2,
\tag{20}
\]

and set

\[
 u=(X,Y)^T,\qquad h=(\widehat Z,\widehat W)^T.
\]

Direct substitution gives (1) with

\[
 q_0(X,Y)=\binom{Y-\alpha X^2}{-X},\qquad
 A=\begin{pmatrix}-2&0\\1&-D_w\end{pmatrix}.
\tag{21}
\]

Fix \(D_w>0\). More generally, the estimates are uniform for
\(D_w\in[d_-,d_+]\Subset(0,\infty)\). Then

\[
 \det(\lambda I-A)=(\lambda+2)(\lambda+D_w),
\]

so \(A\) is Hurwitz, including the repeated-eigenvalue case \(D_w=2\).
All remaining terms are exactly divisible by \(\delta\). The executable
certificate
[`nonlocal_graph_jet.py`](../src/canard_control/nonlocal_graph_jet.py)
checks both divisibility residuals symbolically.

Let

\[
 X_{-j}(u)=\pi_X\phi_0^{-\theta_j}(u),\qquad
 \Delta_0X=X_{-0}-X_{-1}.
\]

The first reduced coefficient is

\[
 Q_1=
 \binom{
 K\left(X-\frac13X_{-0}-\frac23X_{-1}\right)
 -\frac{11}{9}\alpha^2X^3
 }{\nu}.
\tag{22}
\]

The stable forcing at \(\delta=0\) is

\[
 G_0=
 \binom{
 \alpha XY+\frac43\alpha^2X^3-K\eta\Delta_0X
 }{
 \dfrac{\alpha}{D_w}X(Y-\alpha X^2)
 }.
\tag{23}
\]

Using (10),

\[
 \partial_\eta H_{1,\widehat Z}
 =-\frac K2\Delta_0X,\qquad
 \partial_\eta H_{1,\widehat W}
 =-\frac{K}{2D_w}\Delta_0X.
\tag{24}
\]

Along every portion of the singular canard that, together with the delayed
flow segments used below, lies in the uncut tube,

\[
 X_0(s)=-\frac{s}{2\alpha},\qquad
 Y_0(s)=\frac{s^2-2}{4\alpha},
\]

we have

\[
 \Delta_0X_0=\frac{\theta_0-\theta_1}{2\alpha},
\]

and hence

\[
 \partial_\eta H_{1,\widehat Z}(u_0(s))
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}.
\tag{25}
\]

Since \(Q_1\) is independent of \(\eta\), the first return to the critical
equation occurs in \(Q_{2,X}\):

\[
\begin{aligned}
 \partial_\eta Q_{2,X}
 &=-2\alpha X\,
 \partial_\eta H_{1,\widehat Z}
 =\alpha KX\Delta_0X,\\
 \partial_\eta Q_{2,X}(u_0(s))
 &=-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
\end{aligned}
\tag{26}
\]

Equations (24)--(26) are the uniquely determined coefficients in the
invariance recursion for the chosen cutoff, and on the stated uncut portion
they use only the physical vector field. Symbolic division checks that no
negative power of \(\delta\) has been hidden. The companion finite-scale
mixed-jet theorem promotes them to Taylor coefficients of the actual graph on
the declared fixed tube. Promoting (26) to a physical long-delay root
coefficient additionally requires the canard tail/matching theorem.

## 4. What is proved and what remains conditional

Combining this note with
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md), the proved part
establishes:

1. a unique bounded special-flow graph for the cut-off local model;
2. a two-sided reduced flow and an injective complete-history map;
3. the application-required finite mixed regularity, a uniform fixed-tube
   \(O(\delta^3)\) Taylor remainder, and the actual graph coefficient (26).

The algebraic coefficient in (26) is also independently verified by symbolic
division. These fixed-tube results do not determine its whole-line canard-root
pairing.

It does not yet establish:

1. that every nearby bounded RFDE orbit lies on this graph;
2. a stable foliation for arbitrary histories;
3. the attracting/repelling slow-curve matching root;
4. the canard displacement remainder;
5. cutoff independence outside the declared compact flow tube.

The cutoff qualification is essential. Formula (11) integrates along the
entire negative \(Q\)-orbit, so two extensions that agree on the physical
tube need not give exactly the same global graph there. A coefficient of a
finite \(\delta\)-jet is independent of the extension only after the cutoff
is known to agree on every finite flow segment and iterated delay backtrack
appearing in that coefficient's recursion. Equations (22)--(26) meet this
condition on the explicitly declared uncut portion. The whole-line Gaussian
pairing is not made cutoff-independent by Theorem target 1 and remains a separate
matching problem.

The first two items are unnecessary for the logical implication
"reduced slow curves intersect \(\Rightarrow\) their embedded complete
histories intersect." If exponential tracking is later required, it must be
proved separately or obtained from a fixed-\(\delta\) spectral-manifold
theorem with uniform constants.

For comparison, Diekmann--van Gils (1991, Theorems 6.5 and 6.13) and
Bosschaert--Janssens--Kuznetsov (2020, Theorem 19 and Corollary 20) provide
direct center-manifold results for regular fixed-history RFDEs. They do not
by themselves supply the singular \(\delta\)-uniform conclusion above.
