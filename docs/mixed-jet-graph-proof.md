# Mixed-jet closure for the special-flow graph

Status: **proved on a finite scale of spaces under the bounded-cutoff
hypotheses stated below.** This note replaces a same-order Banach
implicit-function argument, which loses one spatial derivative, by explicit
triangular Banach fibers for the mixed jets. It gives the fixed-tube
regularity

\[
 (Q,H)\in C_u^3C_{\delta,\eta}^{3,2}
\]

and a uniform \(C_u^3C_\eta^2\) Taylor remainder of order
\(O(\delta^3)\). It does not give the growing-tube estimate required by
Gate D.

## 1. Setting and the finite regularity scale

Let

\[
\begin{aligned}
 u'&=q_0(u)+\delta
 F\left(u,h,(u_{-\theta_j},h_{-\theta_j})_{j=1}^N;
 \delta,\eta\right),\\
 \delta h'&=Ah+\delta
 G\left(u,h,(u_{-\theta_j},h_{-\theta_j})_{j=1}^N;
 \delta,\eta\right),
\end{aligned}
\tag{1}
\]

where \(A\) is Hurwitz,

\[
 \|e^{Ar}\|\le M_Ae^{-\beta r},\qquad r\ge0,
\tag{2}
\]

and \(0\le\theta_j\le\Theta\). After a fixed smooth cutoff, assume:

1. \(q_0,F,G\in C_b^R\), including all state and
   \((\delta,\eta)\)-derivatives below;
2. the data extend to an open neighborhood of
   \(\Lambda_*=[-\delta_*,\delta_*]\times[-\eta_*,\eta_*]\);
3. \(q_0\), and every vector field in a fixed sufficiently small
   \(C_b^1\) neighborhood, has a complete two-sided flow;
4. \(R\ge12\).

The last number is deliberately not optimized. It provides two unused
spatial derivatives at the top of the finite scale.

For a parameter-dependent map \(f\), write

\[
 J_{a,b,c}f=D_u^a\partial_\delta^b\partial_\eta^c f,
\qquad
 |(a,b,c)|=a+b+c,\qquad
 p(a,b,c)=b+c.
\tag{3}
\]

Fix

\[
 s=3,\qquad B=3,\qquad C=2,\qquad
 N_0=s+B+C=8.
\tag{4}
\]

We use every jet in the triangular index set

\[
 \mathcal I_k=
 \left\{(a,b,c):
 a,b,c\ge0,\ b\le B,\ c\le C,\ a+b+c\le k
 \right\}.
\tag{5}
\]

The desired rectangular family

\[
 0\le a\le3,\qquad0\le b\le3,\qquad0\le c\le2
\tag{6}
\]

is contained in \(\mathcal I_{N_0}\). The larger spatial orders in
\(\mathcal I_{N_0}\) are not extra conclusions sought by the application;
they are the reserve which absorbs the derivative loss caused by
parameter-dependent flows.

**Theorem 1 (finite-scale mixed-jet graph).** Under assumptions 1--4,
there are \(\delta_0,C>0\) such that, for
\(|\delta|\le\delta_0\) and \(|\eta|\le\eta_*\), the graph transform
(10) has a unique fixed point in the contraction neighborhood. It satisfies

\[
 \max_{\substack{0\le b\le3\\0\le c\le2}}
 \|\partial_\delta^b\partial_\eta^c(Q,H)\|
 _{C_b^{\,8-b-c}}
 \le C.
 \tag{T1}
\]

In particular, every mixed derivative in (6) exists and is bounded
uniformly. Moreover,

\[
\begin{aligned}
 Q&=q_0+\delta Q_1+\delta^2Q_2+R_Q,\\
 H&=\delta H_1+\delta^2H_2+R_H,
\end{aligned}
\qquad
 \max_{0\le c\le2}
 \|\partial_\eta^c(R_Q,R_H)\|_{C_b^3}
 \le C|\delta|^3.
 \tag{T2}
\]

The proof occupies Sections 2--7.

From now on, decrease \(\delta_0\) so that \(0<\delta_0<\delta_*\), and
write

\[
 \Lambda_0=[-\delta_0,\delta_0]\times[-\eta_*,\eta_*].
\tag{6a}
\]

The strict inclusion in the ambient parameter neighborhood is used when
parameter derivatives are identified by difference quotients.  Every
fiber and every supremum below is taken over \(\Lambda_0\), not over the
larger rectangle \(\Lambda_*\).

Order the indices first by total grade \(a+b+c\), and, at equal grade, by
parameter grade \(b+c\). Indices with the same two grades form one block.
Thus a jet with fewer parameter derivatives and more spatial derivatives
is constructed first.

For \(\alpha=(a,b,c)\), let

\[
 \mathcal Y_\alpha^e=
 C_b\left(
 \mathbb R^d,
 \mathcal L_{\mathrm{sym}}^a(\mathbb R^d;\mathbb R^e)
 \right)
\tag{7}
\]

with the uniform norm, and let

\[
 \widehat{\mathcal Y}_\alpha^e
 =C(\Lambda_0;\mathcal Y_\alpha^e),\qquad
 \|Y\|=\sup_{(\delta,\eta)\in\Lambda_0}
 \|Y(\delta,\eta)\|_{\mathcal Y_\alpha^e}.
\tag{7a}
\]

The common Banach fiber for a block
\(\mathcal B_{n,p}\subset\mathcal I_{N_0}\) is

\[
 \mathfrak F_{n,p}=
 \prod_{\alpha\in\mathcal B_{n,p}}
 \left(
 \widehat{\mathcal Y}_\alpha^d
 \times\widehat{\mathcal Y}_\alpha^m
 \right),
\tag{8}
\]

with the maximum norm. This is the single common fiber used at that block;
it does not change with the iteration number.

## 2. The derivative-free graph transform

For a complete vector field \(Q\), let \(\Phi_Q^t\) denote its flow and set

\[
 \mathcal E_{Q,H}(u)=
 \left(
 u,H(u),
 \left(\Phi_Q^{-\theta_j}u,
 H(\Phi_Q^{-\theta_j}u)\right)_{j=1}^N
 \right).
\tag{9}
\]

The graph transform is

\[
\begin{aligned}
 \mathcal T_Q(Q,H)(u)
 &=q_0(u)+\delta
 F(\mathcal E_{Q,H}(u);\delta,\eta),\\
 \mathcal T_H(Q,H)(u)
 &=\delta\int_0^\infty e^{Ar}
 G\left(
 \mathcal E_{Q,H}(\Phi_Q^{-\delta r}u);
 \delta,\eta
 \right)\,dr.
\end{aligned}
\tag{10}
\]

It is useful to write the complete list of points entering the integrand:

\[
 \Phi_Q^{-\delta r}u,\qquad
 \Phi_Q^{-(\theta_j+\delta r)}u,
 \qquad j=1,\ldots,N.
\tag{11}
\]

The \(C^0\)-Lipschitz proof gives, after decreasing
\(\delta_0>0\), a uniform contraction on
\(|\delta|\le\delta_0\):

\[
 \|\mathcal T(Z)-\mathcal T(\widetilde Z)\|_{C^0}
 \le \kappa_0\|Z-\widetilde Z\|_{C^0},
 \qquad \kappa_0<1,
\tag{12}
\]

where \(Z=(Q,H)\). It also gives

\[
 \|Q-q_0\|_{C^1}+\|H\|_{C^1}\le C|\delta|.
\tag{13}
\]

The invariant Lipschitz ball used to prove (12) gives this bound for every
iterate as well as for the limit. We start the iteration at

\[
 Z_0=(q_0,0),\qquad Z_{n+1}=\mathcal T(Z_n).
\tag{14}
\]

For completeness, (12) follows directly from the flow estimate

\[
 \|\Phi_Q^t-\Phi_{\widetilde Q}^t\|_\infty
 \le |t|e^{L|t|}\|Q-\widetilde Q\|_\infty,
 \tag{14a}
\]

valid on a common \(C_b^1\) ball.  The Lipschitz bound for \(H\) then
gives, at every point in (11), a bound by

\[
 C(1+\Theta+|\delta|r)e^{L(\Theta+|\delta|r)}
 \|(Q,H)-(\widetilde Q,\widetilde H)\|_{C^0}.
 \tag{14b}
\]

The \(Q\)-component of (10) is therefore Lipschitz with constant
\(C|\delta|\).  In the \(H\)-component, (14b) is multiplied by
\(|\delta|M_Ae^{-\beta r}\).  Taking \(L\delta_0<\beta/2\) makes its
integral finite and again gives a constant \(C|\delta|\).  This proves
(12) after one more reduction of \(\delta_0\).  Differentiating once in
\(u\) gives the invariant \(C_b^1\) ball (13) by the same estimate.  Thus
(12)--(13) are consequences of assumptions 1--4, rather than additional
regularity hypotheses.

The purpose of the remaining proof is to show that the mixed derivatives of
these iterates converge in the common fibers (8).

## 3. Flow-composition lemma on the scale

For \(r\ge0\), define

\[
 \Psi_{j,r}[Q](u)
 =\Phi_Q^{-(\theta_j+\delta r)}u,
\qquad
 \Psi_{*,r}[Q](u)=\Phi_Q^{-\delta r}u.
\tag{15}
\]

The symbol \(j=*\) means \(\theta_*=0\).

**Lemma 1 (triangular mixed flow jets).** Fix
\(K\le N_0+1\). Suppose a family \(Q\) has uniformly bounded jets in
\(\mathcal I_K\) and a uniform \(C_b^1\) bound. For every
\(\alpha\in\mathcal I_K\), there are constants
\(C_\alpha,\Gamma_\alpha>0\) and an integer \(M_\alpha\) such that

\[
 \|J_\alpha\Psi_{j,r}[Q]\|_\infty
 \le
 C_\alpha(1+r^{M_\alpha})
 e^{\Gamma_\alpha(\Theta+|\delta|r)}.
\tag{16}
\]

For the difference estimate, suppose in addition that \(Q,\widetilde Q\)
have a common bound in \(\mathcal I_{K+1}\). If all jet blocks preceding
the block of \(\alpha\) are included in
\(d_{<\alpha}(Q,\widetilde Q)\), where explicitly

\[
 d_{<\alpha}(Q,\widetilde Q)
 =
 \max_{\mathcal B_{n,p}\prec\mathcal B(\alpha)}
 \max_{\gamma\in\mathcal B_{n,p}}
 \|J_\gamma Q-J_\gamma\widetilde Q\|_\infty,
\tag{16a}
\]

with the empty maximum defined as zero, then

\[
\begin{aligned}
 \|J_\alpha\Psi_{j,r}[Q]
  -J_\alpha\Psi_{j,r}[\widetilde Q]\|_\infty
 \le{}&
 C_\alpha(1+r^{M_\alpha})
 e^{\Gamma_\alpha(\Theta+|\delta|r)}
 \\
 &\times\left(
 \|J_\alpha Q-J_\alpha\widetilde Q\|_\infty
 +
 d_{<\alpha}(Q,\widetilde Q)
 \right).
\end{aligned}
\tag{17}
\]

The same estimates hold after composing a family \(H\) with every map in
(15), with the principal block
\((J_\alpha Q,J_\alpha H)\) on the right of (17).

*Proof.* We first keep the terminal time \(t\) independent of the
parameters. The flow satisfies

\[
 \partial_t\Phi_Q^t(u)=Q(\Phi_Q^t(u)).
\tag{18}
\]

One spatial derivative gives the usual variational equation

\[
 \partial_tD_u\Phi_Q^t
 =DQ(\Phi_Q^t)D_u\Phi_Q^t.
\tag{19}
\]

Gronwall's inequality gives
\(\|D_u\Phi_Q^t\|\le e^{L|t|}\), where \(L\) is the common
\(C^1\) bound. At spatial order \(a\ge2\), differentiating (18) gives

\[
 \partial_tD_u^a\Phi_Q^t
 =DQ(\Phi_Q^t)D_u^a\Phi_Q^t
 +D^aQ(\Phi_Q^t)
   [D_u\Phi_Q^t,\ldots,D_u\Phi_Q^t]
 +\mathcal R_a.
\tag{20}
\]

Every term in \(\mathcal R_a\) contains only spatial derivatives of
\(Q\) and \(\Phi_Q^t\) of order strictly below \(a\). Induction in \(a\)
and variation of constants prove (16) for pure spatial derivatives.

For a parameter \(\lambda\in\{\delta,\eta\}\),

\[
\begin{aligned}
 \partial_t\partial_\lambda\Phi_Q^t
 ={}&DQ(\Phi_Q^t)\partial_\lambda\Phi_Q^t
 +(\partial_\lambda Q)(\Phi_Q^t).
\end{aligned}
\tag{21}
\]

Mixed differentiation of (18) has the same form:

\[
 \partial_tJ_\alpha\Phi_Q^t
 =DQ(\Phi_Q^t)J_\alpha\Phi_Q^t
 +\mathcal P_\alpha.
\tag{22}
\]

In \(\mathcal P_\alpha\), the occurrence of \(J_\alpha Q\) is linear.
Every other occurrence of a jet of \(Q\) having the same total grade as
\(\alpha\) has strictly fewer parameter derivatives and strictly more
spatial derivatives. It therefore lies in a preceding block under the
ordering fixed after (5). This is the triangular property.

To verify that assertion, apply the multivariable Faà di Bruno formula to
\(Q(\Phi_Q^t(u),\delta,\eta)\). If one or more parameter derivatives hit
the argument \(\Phi_Q^t\), the explicit parameter multi-index left on
\(Q\) is strictly smaller and its spatial order increases by the number of
argument slots created. Total grade is preserved, but parameter grade
decreases. If no parameter derivative hits the argument, the only
same-block term is \(J_\alpha Q\) evaluated along the flow. Products of two
nonzero parameter jets have strictly smaller total grade in each factor.

Induction over the ordered blocks and variation of constants now prove the
fixed-time version of (16). To obtain (15), compose with

\[
 t_j(\delta,r)=-(\theta_j+\delta r).
\]

Each \(\delta\)-derivative which hits \(t_j\) contributes a factor \(r\)
and a time derivative of the flow. By (18), a time derivative is a
state derivative built from \(Q\) and already controlled jets. Thus only
the polynomial \(1+r^{M_\alpha}\) changes; the triangular highest block is
unchanged.

For differences, subtract (19)--(22). Terms evaluated at two different
orbits are controlled by one reserved spatial derivative, supplied by the
\(\mathcal I_{K+1}\) bound. Variation of constants yields (17).
Applying the ordinary Faà di Bruno formula to
\(H\circ\Psi_{j,r}[Q]\) gives the final assertion. \(\square\)

The use of a reserved spatial derivative in the difference estimate is the
precise reason for working on a scale rather than in a same-order Banach
space.

For later use, define the preceding-block distance for full graph jets by

\[
 d_{<n,p}(Z,\widetilde Z)
 =\max_{\mathcal B_{n',p'}\prec\mathcal B_{n,p}}
   \max_{\gamma\in\mathcal B_{n',p'}}
   \|J_\gamma Z-J_\gamma\widetilde Z\|,
\tag{17a}
\]

again with an empty maximum equal to zero.  The norm on a graph jet is the
maximum of its \(Q\)- and \(H\)-component norms.

The following extraction records the part of the chain rule which is used
in both the invariant-ball and convergence arguments.  It also makes clear
where the factor needed for highest-order contraction occurs.

**Lemma 2 (highest-block fiber map).** Let
\(\mathcal B_{n,p}\subset\mathcal I_{N_0+1}\) be a nonzero block other
than the first pure spatial block \(\mathcal B_{1,0}\), and suppose all
preceding blocks range in fixed bounded sets.  For actual jet families of
a smooth \(Z=(Q,H)\), differentiation of (10) has the exact affine form

\[
 \mathbf J_{n,p}\mathcal T(Z)
 =\mathbf b_{n,p}(\mathbf J_{<n,p}Z)
  +\delta\,\mathscr L_{n,p}(\mathbf J_{<n,p}Z)
       [\mathbf J_{n,p}Z].
\tag{22a}
\]

Here \(\mathscr L_{n,p}\) is a bounded linear operator on the common
fiber \(\mathfrak F_{n,p}\); the formula is affine only in the current
block, while \(\mathbf b_{n,p}\) may be nonlinear in preceding blocks.
This operator is defined constructively as follows.  Replace the current
jet entries by an arbitrary element \(U\in\mathfrak F_{n,p}\), retain the
terms linear in \(U\) in the differentiated variational equations
(19)--(22), and solve those equations with zero initial data for the
corresponding top flow jets.  Substitute those flow jets and the
\(H\)-entries of \(U\) into the terms linear in the current block in the
Faà di Bruno expansions of \(F\) and \(G\), and apply the semigroup
integral in (10) to the latter.  The resulting element of
\(\mathfrak F_{n,p}\) is
\(\mathscr L_{n,p}[U]\); setting \(U=0\) leaves
\(\mathbf b_{n,p}\).  Thus (22a) is a definition by finite variational
equations, not an appeal to an unspecified derivative of the graph
transform.
On the bounded sets under consideration,

\[
 \|\mathscr L_{n,p}\|\le C_{n,p},
\tag{22b}
\]

and for two actual jet families,

\[
\begin{aligned}
 \|\mathbf J_{n,p}\mathcal T(Z)
   -\mathbf J_{n,p}\mathcal T(\widetilde Z)\|
 \le{}& C_{n,p}|\delta|
       \|\mathbf J_{n,p}Z-\mathbf J_{n,p}\widetilde Z\|\\
 &+C_{n,p}d_{<n,p}(Z,\widetilde Z).
\end{aligned}
\tag{22c}
\]

Estimate (22c) also holds for \(\mathcal B_{1,0}\), although (22a) need
not.  On that block the expression after the external factor \(\delta\)
is a bounded nonlinear map of \(D_u(Q,H)\), uniformly Lipschitz on the
invariant \(C_b^1\) ball.

*Proof.* In a total derivative of grade \(n\), a factor carrying the full
current grade can occur only once: every product containing two
positive-grade jet factors places each factor in a lower total grade.
Lemma 1 shows the same fact for the implicitly defined flow jets.  A
same-total-grade flow term in which a parameter derivative hits the flow
argument has smaller parameter grade, and hence belongs to a preceding
block.  Consequently the only current-block occurrence is linear, except
when \((n,p)=(1,0)\).  In that exceptional block, \(DQ\) occurs in the
coefficient of the first variational equation (19), so the flow derivative
depends nonlinearly on \(DQ\).  The difference of two solutions of (19),
Gronwall's inequality, and one reserved second derivative give a uniform
Lipschitz bound on the fixed \(C_b^1\) ball.  The same argument applies to
\(D(H\circ\Phi_Q^t)\).

Both components of (10) carry the displayed external factor \(\delta\).
When a \(\delta\)-derivative removes it, (25) below shows that the remaining
jet has one fewer parameter derivative.  It therefore contributes to
\(\mathbf b_{n,p}\), not to the current-block operator.  The semigroup
majorant (28) and Lemma 1 give (22b).  Subtracting the two affine formulas,
using (17) for changes in the coefficients and putting every preceding
block difference into \(d_{<n,p}\), gives (22c) for all other blocks.  In
the exceptional block, the Lipschitz estimate just obtained is multiplied
by the same external factor \(\delta\), and gives (22c) directly.
\(\square\)

## 4. Common invariant jet balls

Let \(\mathcal B_{n,p}\) be a block of the ordering and put

\[
 \mathbf J_{n,p}Z=
 \left(J_\alpha Z\right)_{\alpha\in\mathcal B_{n,p}}
 \in\mathfrak F_{n,p}.
\tag{23}
\]

**Lemma 3 (invariant mixed-jet balls).** After decreasing \(\delta_0\),
there are radii \(R_{n,p}\), independent of the iteration number and of
\((\delta,\eta)\in\Lambda_0\), such that

\[
 \|\mathbf J_{n,p}Z_k\|_{\mathfrak F_{n,p}}
 \le R_{n,p}
\tag{24}
\]

for every block through \(\mathcal I_{N_0+1}\) and every \(k\ge0\).

*Proof.* Assume the radii have been fixed for all preceding blocks.
Differentiate (10) by a jet \(J_\alpha\) in the current block.

For the \(Q\)-component, the only term not carrying the external factor
\(\delta\) is \(D_u^aq_0\), and it occurs only when \(b=c=0\). If
\(b>0\), the Leibniz formula is

\[
 \partial_\delta^b(\delta\mathcal F)
 =\delta\partial_\delta^b\mathcal F
 +b\,\partial_\delta^{b-1}\mathcal F.
\tag{25}
\]

The second term contains one fewer parameter derivative and belongs to a
preceding block. Eta derivatives never remove the external factor
\(\delta\). The same observations apply to the \(H\)-component.

The order-zero block is bounded by the original contraction ball, and the
first pure spatial block is bounded by (13). For every subsequent block,
Lemma 1 and Faà di Bruno's formula give

\[
 \|\mathbf J_{n,p}Z_{k+1}\|_{\mathfrak F_{n,p}}
 \le C_{n,p}|\delta|
 \|\mathbf J_{n,p}Z_k\|_{\mathfrak F_{n,p}}
 +B_{n,p},
\tag{26}
\]

where \(B_{n,p}\) depends only on the already fixed lower-block radii and
the data.

For the integral component, choose \(\delta_0\) so that

\[
 \Gamma_{N_0+1}\delta_0<\frac{\beta}{2}.
\tag{27}
\]

Then every majorant is integrable because

\[
 e^{-\beta r}
 (1+r^M)e^{\Gamma(\Theta+|\delta|r)}
 \le
 e^{\Gamma\Theta}(1+r^M)e^{-\beta r/2}.
\tag{28}
\]

Finally choose \(\delta_0\) smaller so that
\(C_{n,p}\delta_0\le1/2\) for the finitely many blocks, and choose

\[
 R_{n,p}\ge
 2B_{n,p}
 +\|\mathbf J_{n,p}Z_0\|_{\mathfrak F_{n,p}}.
\tag{29}
\]

Equation (26) proves (24) by induction over the blocks and then over the
iteration number. \(\square\)

## 5. Fiber contraction and convergence

**Lemma 4 (convergence in every common fiber).** The mixed jets
\(\mathbf J_{n,p}Z_k\) converge uniformly over
\(\mathbb R^d\times\Lambda_0\) for every block in
\(\mathcal I_{N_0}\).

*Proof.* The order-zero block converges geometrically by (12). Suppose all
preceding blocks converge. Apply (17) and the differentiated form of (10)
to two consecutive iterates. Equations (25) and (28) give

\[
\begin{aligned}
 \|\mathbf J_{n,p}Z_{k+1}
  -\mathbf J_{n,p}Z_k\|_{\mathfrak F_{n,p}}
 \le{}&
 \kappa_{n,p}
 \|\mathbf J_{n,p}Z_k
  -\mathbf J_{n,p}Z_{k-1}\|_{\mathfrak F_{n,p}}\\
 &+C_{n,p}\,d_{<n,p}(Z_k,Z_{k-1}),
\end{aligned}
\tag{30}
\]

where

\[
 \kappa_{n,p}\le C_{n,p}\delta_0<1.
\tag{31}
\]

By the induction hypothesis, every lower-block increment in the last term
is bounded by \(Cq^k\) for some \(q<1\). This geometric statement follows
simultaneously with convergence: the order-zero block has it by (12), and
the scalar recurrence

\[
 a_{k+1}\le\kappa a_k+Cq^k
\]

has a geometric bound with any rate strictly larger than
\(\max\{\kappa,q\}\). Hence the right-hand side of (30) is summable in
\(k\), and the current fiber is Cauchy. This completes induction over the
finite block ordering. \(\square\)

There is no hidden change of Banach space in Lemma 4: for a fixed block all
jets of \(Q\) and \(H\) live in the single product fiber (8). The reserve
appears only in the coefficients of the fiber map, through Lemma 1.

## 6. Identification of the limiting jets

Let \(Z=(Q,H)\) be the \(C^0\) fixed point. Lemma 4 supplies candidate
mixed derivatives through \(\mathcal I_{N_0}\).

We spell out the closure step because uniform bounds alone would not imply
parameter differentiability.  If \(f_k\to f\) and
\(\partial_\lambda f_k\to g\) uniformly in one of the common fibers, then
for every coordinate segment contained in the ambient parameter
neighborhood,

\[
 f_k(u,\lambda+h)-f_k(u,\lambda)
 =\int_0^h\partial_\lambda f_k(u,\lambda+t)\,dt.
\tag{31a}
\]

Passing to the uniform limit gives the same identity for \(f,g\), hence
\(\partial_\lambda f=g\).  The identical line-segment argument in \(u\)
identifies spatial derivatives.  Starting at the order-zero limit and
applying (31a) successively in the block order identifies every limiting
jet with

\[
 J_{a,b,c}Z
 =D_u^a\partial_\delta^b\partial_\eta^c Z.
\tag{32}
\]

At the boundary of the displayed parameter rectangle, derivatives mean
the restrictions of derivatives obtained on the open parameter
neighborhood from assumption 2.  Equivalently, one may carry out the same
construction on a slightly enlarged eta interval and then restrict to
\(\Lambda_0\).

This is strong closure of uniformly convergent derivatives; no weak
compactness claim is being used.  The common \(\mathcal I_{N_0+1}\) bounds
from Lemma 3 make the top
derivatives uniformly continuous in \(u\), so the identified derivatives
are continuous.  Taking every \(a\le8-b-c\) in (32) proves (T1).  In
particular,

\[
 \sup_{\substack{0\le b\le3\\0\le c\le2}}
 \|\partial_\delta^b\partial_\eta^c(Q,H)\|_{C_b^3}
 <\infty.
\tag{33}
\]

This proves the claimed \(C_u^3C_{\delta,\eta}^{3,2}\) regularity.

## 7. Uniform delta remainder

At \(\delta=0\), (10) is the constant map

\[
 (Q,H)=(q_0,0),
\tag{34}
\]

independently of \(\eta\). Define

\[
 (Q_j,H_j)
 =\frac1{j!}
 \partial_\delta^j(Q,H)\big|_{\delta=0},
 \qquad j=1,2.
\tag{35}
\]

Taylor's formula in the Banach space
\(C_b^3(\mathbb R^d,\mathbb R^{d+m})\) gives

\[
\begin{aligned}
 Q&=q_0+\delta Q_1+\delta^2Q_2+R_Q,\\
 H&=\delta H_1+\delta^2H_2+R_H,
\end{aligned}
\tag{36}
\]

and, for \(0\le c\le2\),

\[
 \|\partial_\eta^c(R_Q,R_H)\|_{C_b^3}
 \le C|\delta|^3.
\tag{37}
\]

Indeed,

\[
 \partial_\eta^c(R_Q,R_H)
 =\frac{\delta^3}{2}
 \int_0^1(1-t)^2
 \partial_\delta^3\partial_\eta^c(Q,H)(t\delta,\eta)\,dt,
\tag{38}
\]

and (33) bounds the integrand uniformly.

Differentiating (10) once at \(\delta=0\) gives

\[
 Q_1=F(\mathcal E_0;0,\eta),\qquad
 H_1=-A^{-1}G(\mathcal E_0;0,\eta),
\tag{39}
\]

where

\[
 \mathcal E_0(u)=
 \left(
 u,0,
 (\phi_0^{-\theta_j}u,0)_{j=1}^N
 \right).
\]

## 8. Why a same-order implicit-function theorem is invalid

The map \(Q\mapsto\Phi_Q^t\) is not a \(C^1\) map from a
\(C_b^3\) vector-field ball to \(C_b^3\) flow maps without an extra
spatial derivative. If \(V=D_Q\Phi_Q^t[\widehat Q]\), then

\[
 \dot V=DQ(\Phi_Q^t)V+\widehat Q(\Phi_Q^t).
\tag{40}
\]

Taking three spatial derivatives of (40) produces, among other terms,

\[
 D^4Q(\Phi_Q^t)
 [D_u\Phi_Q^t,D_u\Phi_Q^t,D_u\Phi_Q^t,V].
\tag{41}
\]

Thus a same-order \(C_b^3\) Banach implicit-function theorem asks for a
derivative not present in its domain. This is a genuine loss, not a
notational inconvenience.

For the finite mixed jet required here, Nash--Moser is unnecessary. The
triangular scale (5), the two reserved grades, and the common fibers (8)
close the iteration. An all-orders or analytic statement would require
either a tame Fréchet/Nash--Moser formulation or a separate analytic
majorant argument.

## 9. The proved boundary

This note proves, for a fixed cutoff tube:

1. common invariant Banach balls for all mixed jets needed by
   \(C_u^3C_{\delta,\eta}^{3,2}\);
2. contraction and convergence of each highest-jet block despite the flow
   derivative loss;
3. a uniform \(C_u^3C_\eta^2\) remainder \(O(\delta^3)\);
4. the first graph coefficients used by the symbolic transverse-return
   calculation.

It does **not** prove that the constants obey
\(\operatorname{poly}(S)e^{CS}\) when the cutoff tube grows with
\(S=S_\delta\). That is a distinct quantitative theorem and is not inferred
from the fixed-tube result.

## 10. Logical status of the proof

The status of each seam is as follows.

1. Formula (10), the invariant \(C_b^1\) ball, and the order-zero fixed
   point are proved from the global bounded-cutoff assumptions by
   (14a)--(14b).  They are not imported from a same-order implicit-function
   theorem.
2. Lemma 1 is a finite-order variational-equation induction.  Its
   difference estimate uses exactly one additional spatial grade; the
   common \(\mathcal I_9\) bound in Lemma 3 supplies that grade for the
   convergence of \(\mathcal I_8\).
3. Lemma 2 identifies an actual bounded linear map on each fixed common
   fiber after the first pure spatial block, and a bounded Lipschitz map on
   that exceptional block.  In both cases it isolates the external factor
   \(\delta\).  Thus the highest-block step in (30) is a contraction, not
   merely a boundedness or compactness argument.
4. Lemma 4 gives strong uniform convergence of actual jets.  Equation
   (31a), rather than a weak-limit assertion, identifies the limits as
   parameter and spatial derivatives.
5. Equations (36)--(38) are then an ordinary Banach-valued Taylor theorem
   and give the stated uniform fixed-tube remainder.

Consequently Theorem 1 is an unconditional abstract theorem under
assumptions 1--4.  Applying it to the final RFDE is conditional only on
constructing a **single fixed cutoff** for which those hypotheses hold.
It gives neither cutoff independence nor constants uniform on the
logarithmically growing tube. Those are separate model-specific claims and
cannot be obtained by taking the cutoff radius to infinity in this theorem.
They are subsequently proved for the frozen preparation-indexed canonical
construction in
[growing-tube-graph-proof.md](growing-tube-graph-proof.md); transfer to a
separately prescribed physical outer selection remains conditional.
