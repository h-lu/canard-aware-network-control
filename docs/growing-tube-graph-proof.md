# A logarithmic-tube special-flow graph estimate

Status: **proved below for the graph part of Gate D, with a frozen
target-dependent cutoff.**  The result promotes the fixed-tube Taylor jet to
the pointwise estimate needed in
[`long-delay-selected-trace-proof.md`](long-delay-selected-trace-proof.md),
but only on the shrinking curve-wise tubes specified below.  It does not
construct the attracting or repelling selected traces.  In particular, this
note proves the growing-graph input (27) there, not Lemma T or the physical
maximal-canard root.

There are two qualifications which are part of the theorem, rather than
technical fine print.

1. The cutoff is frozen at the target value of \(\delta\), and a dummy
   amplitude \(\rho\in[-\delta,\delta]\) is used for Taylor's theorem.  One
   never differentiates \(S_\delta\) or the cutoff.
2. A finite set of delay atoms is not by itself a sufficient uncut set.
   Differentiating a delayed flow produces variational integrals along the
   flow segments joining those atoms.  The cutoff must be physical on the
   corresponding **flow hull**.  This repairs the endpoint-only reading of
   (24) in the selected-trace note.

## 1. Canard coordinates and the normal loss

For

\[
 q_0(X,Y)=\binom{Y-\alpha X^2}{-X},
 \qquad
 \gamma_0(s)=
 \left(-\frac{s}{2\alpha},\frac{s^2-2}{4\alpha}\right),
 \tag{1}
\]

introduce the global polynomial coordinates

\[
 \sigma=-2\alpha X,
 \qquad
 d=Y-\alpha X^2+\frac1{2\alpha}.
 \tag{2}
\]

Thus \(\gamma_0(s)\) is \((\sigma,d)=(s,0)\).  Direct differentiation,
with no approximation, gives

\[
 \sigma'=1-2\alpha d,
 \qquad
 d'=\sigma d.
 \tag{3}
\]

Along \(d=0\), a normal variation over a backward time \(t\geq0\)
contains the factor

\[
 \exp\left(-\sigma t+\frac{t^2}{2}\right).
 \tag{4}
\]

Consequently a polynomial-only growing-tube estimate is false.  On every
fixed interval \(0\leq t\leq T\), however, (3), its variational equations,
and induction over a fixed number \(k\) of derivatives give

\[
 \left|D^k\phi_0^{-t}(\Gamma(\sigma,d))\right|
 \leq C_{k,T}\langle\sigma\rangle^{m_k}
             e^{c_{k,T}|\sigma|}
 \tag{5}
\]

as long as \(|d|\leq d_*\) and the segment stays in
\(|d|\leq2d_*\).  Here \(\Gamma\) is the inverse of (2).  Formula (4)
shows that the exponential in (5) is genuine, while also showing that no
Gaussian \(e^{cS^2}\) loss is forced by a *fixed* delay backtrack.

For completeness, (5) follows without an explicit fundamental matrix.
On a segment of length \(T\), (3) gives
\(|\sigma(t)|\leq |\sigma(0)|+C_T\).  The coefficient matrix in the first
variational equation is therefore bounded by
\(C_T(1+|\sigma(0)|)\).  Gronwall proves (5) for \(k=1\).  Every higher
variational equation has the same homogeneous part and a polynomial in
already controlled lower variations; induction gives (5), with different
\(c_{k,T},m_k\).  The same proof applies to a vector field which is
\(o(1)\) close to \(q_0\) on the segment.

## 2. Frozen anisotropic cutoffs

Fix \(p>4\) and put

\[
 S=S_\delta=\sqrt{2p\log(1/\delta)}.
 \tag{6}
\]

Let \(J\) be the largest total jet grade used below; for the final
application one may take

\[
 0\leq a\leq3,\qquad 0\leq b\leq3,\qquad
 0\leq c\leq1,\qquad 0\leq e\leq2,
 \tag{7}
\]

where \(a,b,c,e\) count state, \(\rho\), \(\nu\), and \(\eta\)
derivatives.  Thus a fixed choice \(J\geq9\) is enough; we assume the
cutoff data have \(J+3\) bounded derivatives.

Order the finite rectangular jets by the total-grade/parameter-grade block
ordering of the mixed-jet proof, with the additional \(\nu\)-index included,
and let \(N_{\rm bl}\) be the number of blocks.  Put
\(D=2N_{\rm bl}+4\), and choose

\[
 1>\kappa_0>\kappa_1>\cdots>\kappa_D>0
 \tag{8}
\]

and set

\[
 T_*=\theta_1+1,\qquad B_j=jT_*,
 \qquad B_*=B_D+T_*+2.
\]

Define the nested curve tubes

\[
 \mathcal U_j(\delta)=
 \left\{\Gamma(\sigma,d):
 |\sigma|\leq S+B_j,\quad |d|\leq\delta^{\kappa_j}
 \right\},
 \qquad 0\leq j\leq D.
 \tag{9}
\]

The tube on which the final estimate is asserted is the smaller set

\[
 \mathcal U_{\rm core}(\delta)=
 \left\{\Gamma(\sigma,d):|\sigma|\leq S,
 |d|\leq\delta^{\kappa_0}\right\}.
 \tag{10}
\]

This is large enough for any curve satisfying
\(|d|\leq C\delta\operatorname{poly}(S)e^{cS}\), since
\(\kappa_0<1\).  The nested exponents are needed because a normal
backtrack maps \(\delta^{\kappa_j}\) into
\(e^{cS}\delta^{\kappa_j}\), not back into the identical tube.

Let \(\chi\in C_c^\infty(\mathbb R)\) equal one on \([-1,1]\) and zero
outside \([-2,2]\).  In the coordinates (2), choose cutoffs which equal
one on

\[
 |\sigma|\leq S+B_*,\qquad |d|\leq d_*,
 \tag{11}
\]

and vanish outside the same set with \(S+B_*\) and \(d_*\) replaced
by \(2(S+B_*)\) and \(2d_*\).  For example, the product of the two
corresponding copies of \(\chi\) works.  Multiply the transformed
\(q_0\) by this product, and cut off every state slot of the polynomial
data \(F,G\) in the same way.  In every current and delayed stable
\(h\)-slot use an additional fixed cutoff which is one on
\(|h|\leq h_*\) and zero on \(|h|\geq2h_*\).  Denote the resulting data by
\(q_{0,S},F_S,G_S\).

This cutoff is anisotropic: its longitudinal radius is \(O(S)\), whereas
its transverse radius is fixed.  The graph construction is performed in
the \((\sigma,d)\) coordinates and then transformed back to \((X,Y)\).
Equations (2)--(3) show, for every fixed finite \(r\),

\[
 \|q_{0,S}\|_{C^r}+\|F_S\|_{C^r}+\|G_S\|_{C^r}
 \leq P_r(S),
 \qquad
 \operatorname{Lip}_{(\sigma,d)}(q_{0,S})\leq C(1+S),
 \tag{12}
\]

for polynomials \(P_r\); conversion of a fixed number of state derivatives
back to \((X,Y)\) only changes these polynomials.  The cutoff vector field
is complete.  Notice
that a cutoff made across a transverse layer of width
\(e^{-S^2/2}\) would instead create artificial algebraic powers of
\(\delta^{-1}\); it is neither needed nor used here.

For each *fixed target* \(\delta\), replace every occurrence of the chart
amplitude in the final special-flow system by a dummy \(\rho\), but keep
the cutoff (11) fixed.  The graph transform is

\[
\begin{aligned}
 \mathcal T_{Q,\rho,S}(Q,H)(u)
 &=q_{0,S}(u)+\rho
 F_S(\mathcal E_{Q,H}(u);\rho,\nu,\eta),\\
 \mathcal T_{H,\rho,S}(Q,H)(u)
 &=\rho\int_0^\infty e^{Ar}
 G_S\!\left(
 \mathcal E_{Q,H}(\Phi_Q^{-\rho r}u);
 \rho,\nu,\eta\right)\,dr.
\end{aligned}
\tag{13}
\]

At \(\rho=\delta\), (13) is the cutoff graph transform of the final
model; at \(\rho=0\), it is the constant map \((q_{0,S},0)\).
The global graph estimate below gives
\(\|H_{\rho,S}\|_\infty\leq|\rho|P_0(S)=o(1)\), so all graph states used
in the local hull lie in the region where the stable-slot cutoffs equal
one.

**Theorem 1 (logarithmic-tube graph jet).**  Fix \(p\), the cutoff profile,
\(d_*\), the exponents (8), the finite jet family (7), a compact
\(\nu\)-interval, and \(|\eta|\leq\eta_*\).  There are
\(\delta_0,C,c,m>0\) with the following property.  For every target
\(0<\delta\leq\delta_0\), first set \(S=S_\delta\) and freeze the cutoff
of Section 2.  With that one cutoff held fixed, the full transform (13)
has a unique family of fixed points for every dummy amplitude
\(|\rho|\leq\delta\).  On
\(\mathcal U_{\rm core}(\delta)\) it has the physical expansion

\[
 (Q_{\delta,S},H_{\delta,S})
 =(q_0,0)+\delta(Q_1,H_1)+\delta^2(Q_2,H_2)
 +\delta^3(R_{3,Q},R_{3,H}),
\]

where the first two coefficients have atom depth at most one and two,
respectively, and are independent of every admissible cutoff agreeing on
the depth-two flow hull.  There are \(C,c,m>0\), independent of
\(\delta,\nu,\eta\), such that

\[
 \max_{\substack{0\leq a\leq3,\ 0\leq c\leq1\\0\leq e\leq2}}
 \left|
 D_u^a\partial_\nu^c\partial_\eta^e(R_{3,Q},R_{3,H})
    (\Gamma(\sigma,d))\right|
 \leq C\langle\sigma\rangle^m e^{c|\sigma|}.
 \tag{T}
\]

The same conclusion holds after any fixed additive enlargement of the
phase interval.  Sections 3--7 prove the theorem.

## 3. Global bounds and contraction

Let \(\|e^{Ar}\|\leq M_Ae^{-\beta r}\).  The global flow estimate and
(12) give, for every fixed jet grade \(g\leq J+1\), constants
\(C_g,M_g\) such that all differentiated flow compositions over a fixed
delay are bounded by

\[
 B_g(S):=P_g(S)e^{C_gS}.
 \tag{14}
\]

For the stable convolution the time is \(\rho r\).  Since

\[
 \delta P_g(S)\longrightarrow0,
 \qquad
 \delta P_g(S)e^{C_gS}\longrightarrow0,
 \tag{15}
\]

we may decrease \(\delta_0\) so that the semigroup majorant is
\(e^{-\beta r/2}\) for every grade under consideration.  The
order-zero graph transform and every highest triangular jet block then
have contraction factor

\[
 q_\delta\leq \delta P_J(S)e^{C_JS}=o(1).
 \tag{16}
\]

Repeating the finite common-fiber argument of
[`mixed-jet-graph-proof.md`](mixed-jet-graph-proof.md), now with the
\(S\)-dependent radii (14), proves the following global facts:

\[
\begin{aligned}
 &\text{(i) (13) has a unique fixed point }Z_{\rho,S}=(Q_{\rho,S},H_{\rho,S}),\\
 &\text{(ii) }Z_{\rho,S}\text{ is }C_\rho^3C_\nu^1C_\eta^2
   \text{ with the state derivatives in (7)},\\
 &\text{(iii) every such jet is bounded globally by }B_J(S),
\end{aligned}
\tag{17}
\]

uniformly for \(|\rho|\leq\delta\), \(\nu\) in the fixed compact
interval, and \(|\eta|\leq\eta_*\).

Here there is no passage to a varying Banach space: for a fixed target
\(\delta\), the cutoff, the interval \([-\delta,\delta]\), and every
fiber are fixed.  Formula (15) supplies the smallness which in the
fixed-tube proof was supplied by a constant independent of \(S\).

## 4. Stable-convolution truncation

Put

\[
 R_\delta=L\log(1/\delta).
 \tag{18}
\]

Split the second line of (13) at \(R_\delta\).  The undifferentiated tail
has the elementary bound

\[
 \left\|\rho\int_{R_\delta}^\infty e^{Ar}G_S(\cdots)\,dr\right\|
 \leq \frac{M_A}{\beta}|\rho|\|G_S\|_\infty
       \delta^{\beta L}.
 \tag{19}
\]

For mixed jets, derivatives of \(\Phi_Q^{-\rho r}\) add only a fixed
power of \(r\), while (14)--(15) replace the kernel by
\(e^{-\beta r/2}\).  Hence, for every jet in (7),

\[
 \left\|\mathscr D
   \mathcal T_{H,\rho,S}^{>R_\delta}\right\|_\infty
 \leq
 P_J(S)e^{C_JS}(1+R_\delta)^{M_J}
 e^{-\beta R_\delta/2}.
 \tag{20}
\]

The harmless outer factor \(|\rho|\) is retained when no
\(\rho\)-derivative removes it.  Because
\(P_J(S)e^{C_JS}(1+R_\delta)^{M_J}=\delta^{-o(1)}\), for every prescribed
\(N\) one can choose \(L=L(J,N)\) so that

\[
 \max_{\mathscr D\ {\rm in}\ (7)}
 \left\|\mathscr D
   \mathcal T_{H,\rho,S}^{>R_\delta}\right\|_\infty
 \leq C_N\delta^N.
 \tag{21}
\]

We use \(N=6\).  The often quoted condition \(L>2/\beta\) is sufficient
for the undifferentiated ideal tail in (19) to be \(o(\delta^3)\).  It is
not, by itself, sufficient for all mixed tails in (20), because the proof
has spent half of the semigroup rate and a \(\rho\)-derivative can remove
the outer factor.  Choosing \(L\) after \(J,N\) is the correct uniform
statement.

For \(0\leq r\leq R_\delta\), the additional reduced-flow backtrack is

\[
 |\rho|r\leq\delta R_\delta=o(1).
 \tag{22}
\]

Thus every retained evaluation contains one fixed delay backtrack plus an
\(o(1)\) flow segment.

The split at \(R_\delta\) is used only to estimate (13).  The fixed point
in (17) is the fixed point of the **full** integral from zero to infinity.
No truncated graph is substituted for it.  Consequently the invariant
graph equation and the complete-history lift remain exact.  At a current
point for which the current and delayed graph states lie in (11), that
exact cutoff RFDE equation is the physical RFDE equation, even though the
Lyapunov--Perron formula used to construct its graph samples the cutoff
extension in the remote past.

## 5. Nested local fibers

We next record why the global bound (14) can be sharpened pointwise.
Enlarge \(P_J,C_J\), once and for all, so that they dominate both the
one-step operator coefficients and the global jet radii in (17).
For each gap \(\kappa_j-\kappa_{j+1}>0\), (5), (14), and (15) imply,
after decreasing \(\delta_0\),

\[
 \delta^{\kappa_j}P_J(S)e^{C_JS}
 +\delta P_J(S)e^{C_JS}
 \leq \frac12\delta^{\kappa_{j+1}}.
 \tag{23}
\]

Flow comparison and (22) therefore show that every retained current or
delayed evaluation starting in \(\mathcal U_j\) lies in
\(\mathcal U_{j+1}\), for \(j<D\): the normal inclusion is (23), while
the longitudinal inclusion follows from
\(\theta_1+\delta R_\delta<T_*\).  Evaluations starting in
\(\mathcal U_D\) remain in
the uncut region (11).  This proves at the same time that the retained
transform is physical on all of the nested tubes.

For a jet tensor \(V\), define the local seminorm

\[
 \|V\|_{j;c,m}
 =\sup_{u=\Gamma(\sigma,d)\in\mathcal U_j}
   \frac{|V(u)|}{\langle\sigma\rangle^m e^{c|\sigma|}}.
 \tag{24}
\]

For each jet block take the product of its global \(C^0\) fiber and all
the finitely many fibers (24).  These are common Banach fibers for every
graph iterate and every \(\rho\in[-\delta,\delta]\).  Order them first by
jet grade and, inside one grade, from the outer nested tube back to the
core.  A single flow composition moves at most from level \(j\) to
\(j+1\).

To make the localization step explicit, let
\(Z_{n+1}=\mathcal T_{\rho,S}(Z_n)\), \(Z_0=(q_{0,S},0)\), and denote
the \(\ell\)-th ordered jet block by \(\mathbf J_\ell Z_n\).
The global mixed-fiber proof gives

\[
 \sup_n\|\mathbf J_\ell Z_n\|_{\rm global}\leq B_\ell(S),
 \qquad
 \mathbf J_\ell Z_n\longrightarrow\mathbf J_\ell Z_{\rho,S}
 \quad\hbox{globally}.
 \tag{24a}
\]

Differentiating one graph-transform step gives the exact highest-block
form

\[
 \mathbf J_\ell Z_{n+1}
 =b_\ell(\mathbf J_{<\ell}Z_n)
  +\rho\,\mathscr L_{\ell,n}[\mathbf J_\ell Z_n]
  +E_{\ell,n}^{>R_\delta}.
 \tag{24b}
\]

For the first pure spatial block, \(\mathscr L_{\ell,n}\) is Lipschitz
rather than affine; its difference estimate has the identical bound below.
Every coefficient in \(b_\ell\) is a finite Faà di Bruno product of
preceding graph jets and flow jets.  A current-block flow jet occurs
linearly; every other flow source belongs to a preceding block.  This is
exactly equations (22a)--(22c) of the fixed-tube proof, applied with the
target cutoff frozen.

On \(\mathcal U_j\), (23) puts all arguments of these finite products in
\(\mathcal U_{j+1}\).  Estimate (5) supplies a factor
\(\operatorname{poly}(|\sigma|)e^{c|\sigma|}\); products and a bounded
phase shift merely enlarge \(c,m\).  Finally, (21) bounds the last term
in (24b).  Put

\[
 A_{\ell,j}^{(n)}
 =\|\mathbf J_\ell Z_n\|_{j;c_\ell,m_\ell}.
\]

After enlarging the finitely many weights, (24b) gives the iterate
recurrence

\[
\begin{aligned}
 A_{\ell,j}^{(n+1)}
 \leq{}& C_\ell
 +C_\ell\sum_{h<\ell}\mathcal P_{\ell,h}
       \bigl(A_{h,j+1}^{(n)}\bigr)\\
 &+|\rho|P_\ell(S)e^{C_\ell S}B_\ell(S)
 +C_\ell\delta^6
\end{aligned}
\tag{25}
\]

for \(j<D\).  At the terminal level only the zeroth block is needed; its
lower-block sum is empty and all retained state evaluations remain in the
uncut buffer (11).

We prove by induction over \(\ell\) that

\[
 \sup_n A_{\ell,j}^{(n)}\leq C_\ell
 \quad\text{for every }0\leq j\leq D-\ell.
 \tag{25a}
\]

For \(\ell=0\), the lower-block sum is empty.  Every unknown graph
occurrence is behind \(\rho\), while \((q_{0,S},0)\) is known, so (15)
proves (25a) at all levels.  Suppose it holds for all \(h<\ell\).
If \(j\leq D-\ell\), then \(j+1\leq D-h\) for every \(h<\ell\);
hence every lower-block term in (25) is bounded by induction.  The sole
global current-block term is bounded because

\[
 |\rho|P_\ell(S)e^{C_\ell S}B_\ell(S)=o(1).
 \tag{25b}
\]

This factor was included when \(P_J,C_J\) were enlarged before (23).
Thus (25a) follows.  Since \(D>N_{\rm bl}\), it includes the core
\(j=0\) for every required block.

Global convergence in (24a) implies convergence in every local seminorm
(24): the denominator is at least one and each local domain is contained
in the global domain.  Passing to the limit in (25a) gives

\[
 \|\mathbf J_\ell Z_{\rho,S}\|_{0;c_\ell,m_\ell}
 \leq C_\ell.
 \tag{26}
\]

No \(S\)-dependent lower-block factor has been used without a small
factor: lower blocks in (25) are controlled in the next local weighted
fiber, whereas the sole global current-block term retains \(\rho\).
If a \(\rho\)-derivative removes the external factor in (13), the
remaining graph jet has one fewer \(\rho\)-derivative and is in a
preceding block.  This is the precise local/global seam.

This local/global argument is also the reason that infinite nesting in the
exact fixed point causes no infinite atom-depth loss.  The finitely many
terms which determine a prescribed Taylor coefficient are estimated in
the nested local fibers.  Every further nesting retains a factor
\(q_\delta\) from (16) and is summed in the global contraction fiber.

## 6. Finite atom depth and cutoff independence

Let

\[
 \Theta^{[d]}=
 \left\{\theta_{j_1}+\cdots+\theta_{j_k}:
 0\leq k\leq d,\ j_i\in\{0,1\}\right\}.
 \tag{27}
\]

The endpoint atoms in (27) keep track of how many delayed evaluations can
be nested, but parameter differentiation of a flow also produces
integrals such as

\[
 \int_0^{\theta_j}
 D\phi_0^{-(\theta_j-a)}
 Q_1(\phi_0^{-a}u)\,da.
 \tag{28}
\]

Accordingly, define the depth-\(d\) flow hull

\[
 \mathfrak H^{[d]}(\mathcal U)=
 \left\{\phi_0^{-t}u:
 u\in\mathcal U, 0\leq t\leq d\theta_1\right\}.
 \tag{29}
\]

The hull, rather than only the finite set of endpoint backtracks, is the
correct uncut set.  A fixed flow-tube buffer around all endpoints in (27)
also suffices if it contains (29).

At \(\rho=0\), differentiation of (13) once gives

\[
 Q_1=F_S(\mathcal E_0;0,\nu,\eta),
 \qquad
 H_1=-A^{-1}G_S(\mathcal E_0;0,\nu,\eta).
 \tag{30}
\]

Thus \((Q_1,H_1)\) has atom depth one.  A second derivative can introduce
one of the following and nothing else:

- one explicit \(\rho\)-derivative of \(F_S,G_S\);
- one occurrence of \(Q_1,H_1\);
- one first variation (28) of a delayed flow;
- one moment \(\int_0^\infty r^ke^{Ar}\,dr\) from the stable convolution.

Every state evaluation in this list belongs to
\(\mathfrak H^{[2]}(\mathcal U_{\rm core})\).  Therefore
\((Q_2,H_2)\), where

\[
 (Q_2,H_2)=\frac12\partial_{\rho\rho}
 (Q_{\rho,S},H_{\rho,S})\big|_{\rho=0},
 \tag{31}
\]

has atom depth at most two.  Since (11) is one on the buffered depth-two
flow hull, (30)--(31) are independent of the chosen admissible cutoff and
are exactly the physical coefficients.  In particular, for the final
model they are the coefficients calculated in
[`special-flow-graph-theorem.md`](special-flow-graph-theorem.md), including

\[
 \partial_\eta Q_{2,X}(\gamma_0(s),\nu,0)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
 \tag{32}
\]

## 7. Pointwise mixed Taylor remainder

Apply (26) to

\[
 D_u^a\partial_\nu^c\partial_\eta^e
 \partial_\rho^3(Q_{\rho,S},H_{\rho,S}),
 \qquad
 0\leq a\leq3,\quad c\leq1,\quad e\leq2.
\]

After taking the maximum of the finitely many weights, there are
\(C,c,m>0\), independent of \(\delta,\rho,\nu,\eta\), such that on
\(\mathcal U_{\rm core}\)

\[
 \left|
 D_u^a\partial_\nu^c\partial_\eta^e
 \partial_\rho^3(Q_{\rho,S},H_{\rho,S})(u)
 \right|
 \leq C\langle\sigma\rangle^m e^{c|\sigma|}.
 \tag{33}
\]

Taylor's formula in the fixed common fiber gives

\[
\begin{aligned}
 Q_{\delta,S}&=q_0+\delta Q_1+\delta^2Q_2+R_Q,\\
 H_{\delta,S}&=\delta H_1+\delta^2H_2+R_H,
\end{aligned}
\tag{34}
\]

and, for the same indices,

\[
 \boxed{
 \left|
 D_u^a\partial_\nu^c\partial_\eta^e(R_Q,R_H)
   (\Gamma(\sigma,d))
 \right|
 \leq C\delta^3
 \langle\sigma\rangle^m e^{c|\sigma|}}
 \tag{35}
\]

whenever \(|\sigma|\leq S_\delta\) and
\(|d|\leq\delta^{\kappa_0}\).  Indeed,

\[
 \partial_\nu^c\partial_\eta^e(R_Q,R_H)
 =\frac{\delta^3}{2}\int_0^1(1-t)^2
 \partial_\nu^c\partial_\eta^e\partial_\rho^3
 (Q_{t\delta,S},H_{t\delta,S})\,dt,
\]

and state derivatives commute with this finite integral.  Formula (35) is
the pointwise \(C_\nu^1C_\eta^2\) version of (27) in the selected-trace
note.  Since

\[
 (R_{3,Q},R_{3,H})=\delta^{-3}(R_Q,R_H),
\]

equations (34)--(35) are equivalently the clean rectangular statement

\[
\boxed{
\begin{aligned}
 Q_{\delta,S}
 &=q_0+\delta Q_1+\delta^2Q_2+\delta^3R_{3,Q},\\
 H_{\delta,S}
 &=\delta H_1+\delta^2H_2+\delta^3R_{3,H},\\
 \max_{\substack{0\leq a\leq3,\ 0\leq i\leq1\\0\leq j\leq2}}
 |D_u^a\partial_\nu^i\partial_\eta^j(R_{3,Q},R_{3,H})|
 &\leq C\langle\sigma\rangle^m e^{c|\sigma|}.
\end{aligned}}
\tag{35b}
\]

The coefficient functions \(Q_1,Q_2,H_1,H_2\) in (35b) are the
\(\rho\)-jets at zero with the target cutoff frozen.  Section 6 proves
that their restrictions to the core are independent of both the target
\(\delta\) and the admissible cutoff, because their depth-two flow hull is
physical.
More generally, (25a) gives the same rectangular estimate on every fixed
nested level \(\mathcal U_k\) with
\(k\leq D-N_{\rm bl}\).  In particular, levels \(k=1,2\) provide the
uniform bounds and uncut membership for the first two delayed backtracks
of a core trace.

Since

\[
 \int_{\mathbb R}e^{-s^2/2+c|s|}\langle s\rangle^m\,ds<\infty,
\]

its contribution to the normalized gap is genuinely \(O(\delta^3)\),
with no \(\delta^{-o(1)}\) loss.

For the final model, \(Q_1\) is independent of \(\eta\), while the first
\(\eta\)-dependent reduced coefficient is \(Q_2\).  Combining this fact
with (33)--(35) gives the interface used by the one-sided Green theorem:
for the same state derivatives through order three,

\[
\begin{aligned}
 |Q_{\delta,S}-q_0|+|\partial_\nu Q_{\delta,S}|
 &\leq C\delta\langle\sigma\rangle^m e^{c|\sigma|},\\
 \sum_{i=0}^1\sum_{j=1}^2
 |\partial_\nu^i\partial_\eta^j Q_{\delta,S}|
 &\leq C\delta^2\langle\sigma\rangle^m e^{c|\sigma|}.
\end{aligned}
\tag{35c}
\]

The second line includes the safe overestimate
\(\partial_{\eta\eta}R_Q=O(\delta^3)\leq O(\delta^2)\).

### Fixed additive phase buffers

For every fixed \(B_0>0\), the construction and (35) remain valid with
\(|\sigma|\leq S_\delta+B_0\) in place of
\(|\sigma|\leq S_\delta\).  To see this, start Section 2 with
\(\widehat S=S_\delta+B_0\) and enlarge \(B_*\) by \(B_0\).
Then

\[
 \operatorname{poly}(\widehat S)e^{C\widehat S}
 =O\!\left(\operatorname{poly}(S_\delta)e^{CS_\delta}\right),
\]

with a changed constant, so (15), (16), (20), and (23) are unchanged.
This version covers the \(S_\delta+1\) physical region and the fixed
preparation buffer used by a Green/phase trace construction.

### Interface with a fixed-width prepared planar field

Estimate (35) is deliberately an estimate for the actual graph on a
shrinking tube; an unconditional fixed-width actual-graph estimate would
reintroduce the normal-mode problem.  A fixed-width *prepared* field can
nevertheless be obtained without differentiating a shrinking cutoff.
On \(d=\pm\delta^{\kappa_0}\), extend each component of
\(Q_{\delta,S}-q_0\) in the normal variable by its degree-three Taylor
polynomial, and multiply that polynomial by a cutoff whose transition
width is fixed.  The values and first three normal derivatives at the
boundary obey (33)--(35), so this extension has the same pointwise
\(C_\nu^1C_\eta^2\), state-\(C^3\) bounds with constants independent of
\(\delta\).  There is no factor \(\delta^{-\kappa_0}\), because no cutoff
is rescaled to the shrinking width.  A fixed longitudinal cutoff can then
join this extension to \(q_0\) in the preparation buffer.

If a canonical Green trace satisfies

\[
 |d_{\rm tr}(\sigma)|
 \leq C\delta\langle\sigma\rangle^m e^{c|\sigma|},
 \tag{36}
\]

then (15) and \(\kappa_0<1\) imply that it lies in (10), after decreasing
\(\delta_0\).  The same statement for its finitely many retained
backtracks follows from (23).  Thus (36) is exactly the bootstrap needed
to replace the prepared field by the actual special-flow field along the
central trace and to use the exact history lift.

## 8. Exact claim boundary

This argument establishes the following graph facts for the final
long-delay chart.

1. There is an admissible frozen anisotropic cutoff for every target
   \(\delta\), and its graph transform is a contraction because
   \(\delta\operatorname{poly}(S_\delta)e^{CS_\delta}=o(1)\).
2. \(Q_1,Q_2,H_1,H_2\) have finite atom depth one and two.  Their cutoff
   independence requires the continuous flow hull (29), not only the
   endpoints (27).
3. The stable convolution may be truncated with all required mixed jets;
   choosing \(L\) after the finite jet order makes its tail smaller than
   any prescribed algebraic power.
4. The exact graph has the pointwise remainder (35) on the shrinking
   curve-wise tube.  The normal mode forces the allowed
   \(e^{c|s|}\), but it does not produce an \(e^{cS^2}\) obstruction.

What is not proved in this note is that one-sided traces eliminate the
Gaussian normal mode, nor that a separately prescribed physical outer
history family enters (10) with the parameter bounds in Lemma T. The first
problem is solved for the fixed admissible canonical preparation in
[green-phase-selected-traces.md](green-phase-selected-traces.md), so together
the two notes close canonical Gate D. The second problem is a distinct
physical outer-selection hypothesis and remains open.
