# A dimension-uniform special-flow history graph

Status: **the invariant-graph part of Gate A is proved below at the abstract
normal-form level, and its logarithmic corollary is proved for the explicit
fold preparation and the uniform transformed-data bound (4.6c).**  The
stable fiber may have arbitrary finite dimension, or may range over a family
of Banach spaces.  The constants do not use that dimension.  They depend on
the fixed reduced-flow data, the uniform stable-semigroup constants, uniform
finite-jet bounds, the delay horizon, and the operator total variation of the
delay measures.

This is a successor-paper result.  It is not inserted into, and is not a
claim of, the completed two-module JNS manuscript.  Applying the theorem to
an original node network still requires a separate, dimension-uniform
normal-form/model-fitting lemma.

The theorem also supplies first and second Frechet responses with respect to
a Banach structural perturbation.  Their abstract three-level identification
with the later Schur--Melnikov response is proved in
[the Banach-scale linkage note](banach-scale-history-schur-link.md).
Concrete selected-trace spaces and endpoint estimates for a node network
remain model-specific.

## 1. Uniform family and the norm that carries the network size

Let \(U=\mathbb R^d\), where \(d\) is fixed.  In the canard application
\(d=2\).  Let \(\mathfrak N\) be an arbitrary index set.  For each
\(N\in\mathfrak N\), let \(E_N\) and \(Y_N\) be real Banach spaces and set

\[
 X_N=U\times E_N,
 \qquad
 \|(u,h)\|_{X_N}=\max\{|u|,\|h\|_{E_N}\}.
 \tag{1.1}
\]

The notation \(N\) is only a family label.  It may denote network size, but
the theorem also covers a fixed infinite-dimensional stable fiber.

Fix a delay horizon \(\Theta>0\).  Let \(\lambda\), specified below, denote
the unfolding and structural parameters.  Let
\(\mathbb B_{N,\lambda}\) be a countably additive
\(\mathcal L(X_N,Y_N)\)-valued measure on \([-\Theta,0]\), and define

\[
 \mathscr D_{N,\lambda}\varphi
 =\int_{[-\Theta,0]}\mathbb B_{N,\lambda}(d\vartheta)
       \varphi(\vartheta),
 \qquad
 \varphi\in C([-\Theta,0],X_N).
 \tag{1.2}
\]

The decisive estimate is

\[
 \|\mathscr D_{N,\lambda}\varphi
       -\mathscr D_{N,\lambda}\widetilde\varphi\|_{Y_N}
 \leq
 \|\mathbb B_{N,\lambda}\|_{\mathrm{TV}}
 \|\varphi-\widetilde\varphi\|_{C}.
 \tag{1.3}
\]

Thus no sum over nodes or delay atoms enters the proof.  A finite list of
delay operators is included by taking \(Y_N\) to be their product with the
maximum norm and by including the corresponding sum of variations in the
constant below.

Let \(\mathfrak R\) be a fixed real Banach space of structural
perturbations.  Choose a compact interval \(I_\nu\) and a bounded open
interval \(\widehat I_\nu\) with
\(I_\nu\Subset\widehat I_\nu\), radii
\(0<r_{\mathcal R}<\widehat r_{\mathcal R}\), and put

\[
 \mathcal P=
 I_\nu\times\overline B_{\mathfrak R}(0,r_{\mathcal R}),
 \qquad
 \widehat{\mathcal P}=
 \widehat I_\nu\times B_{\mathfrak R}
     (0,\widehat r_{\mathcal R}),
 \qquad
 \lambda=(\nu,\mathcal R).
 \tag{1.4a}
\]

One may replace \(\mathfrak R\) by a family \(\mathfrak R_N\); all
statements then use the corresponding multilinear operator norms and require
the same displayed constants uniformly in \(N\).  We keep a fixed
\(\mathfrak R\) only to simplify notation.

The closed parameter cylinder \(\mathcal P\) need not be compact.  Every
bound below is assumed uniformly on the larger open cylinder
\(\widehat{\mathcal P}\).  Let

\[
 \mathcal M_N=
 \mathcal M_{\mathrm{TV}}\bigl(
 [-\Theta,0];\mathcal L(X_N,Y_N)\bigr).
 \tag{1.4b}
\]

Assume explicitly that

\[
 \widehat{\mathcal P}\ni(\nu,\mathcal R)
 \longmapsto\mathbb B_{N,\nu,\mathcal R}\in\mathcal M_N
 \quad\text{belongs to }C_\nu^1C_{\mathcal R}^2
 \tag{1.4c}
\]

in the Frechet sense, including all mixed derivatives, and that

\[
 \sup_N\sup_{\lambda\in\widehat{\mathcal P}}
 \max_{\substack{0\leq i\leq1\\0\leq e\leq2}}
 \left\|
 \partial_\nu^iD_{\mathcal R}^e
       \mathbb B_{N,\lambda}
 \right\|_{
   \mathcal L_{\mathrm{sym}}^e(\mathfrak R;\mathcal M_N)}
 \leq B_{\mathrm{TV}}.
 \tag{1.4}
\]

The full graph history has critical component
\(\Phi_Q^\vartheta u=u+O(1)\) and therefore belongs to an affine, rather
than an ordinary bounded, history space over \(U=\mathbb R^d\).  Total
variation controls every tangent-history variation, but it does not by
itself control a parameter derivative of the measure applied to the
unbounded constant anchor.  Let
\(\iota_U:U\to X_N\) be \(\iota_Uu=(u,0)\).  For the global
\(C_b^k\) parameter-response statement, assume the balanced-anchor
condition

\[
 \left(
 \partial_\nu^iD_{\mathcal R}^e
 \mathbb B_{N,\lambda}
 [\widehat{\mathcal R}_1,\ldots,\widehat{\mathcal R}_e]
 \right)([-\Theta,0])\iota_U=0,
 \qquad
 1\le i+e,\quad i\le1,\quad e\le2,
 \tag{1.4d}
\]

uniformly in the displayed parameters and directions.  Fixed measures
satisfy (1.4d) trivially.  A model may replace (1.4d) by a direct uniform
bound for the actual differentiated transformed-data composite after its
affine delay argument has been prepared; that substitute must be stated and
proved in the model-fitting lemma.

Condition (1.4d) is not cosmetic.  Take \(U=\mathbb R\), \(q_0=0\),
no stable fiber, \(F(y)=\sin y\), and
\(\mathbb B_{\mathcal R}=\mathcal R\delta_0\) on the critical coordinate.
All measure derivatives are bounded in total variation, but the transform
gives
\[
 Q_{\mathcal R}(u)=\rho\sin(\mathcal R u).
\]
For every \(\mathcal R\ne0\),
\(\|Q_{\mathcal R}-Q_0\|_{C_b}=|\rho|\), so the branch is not even
continuous at \(\mathcal R=0\) in \(C_b\).  The missing hypothesis is
exactly control of the affine anchor.

For \(e=0\), the norm in (1.4) is the total-variation norm in
\(\mathcal M_N\).  Fixed measures need only the order-zero part.  A moving
point mass \(\delta_{-\theta(\lambda)}\) is not differentiable in total
variation.  Such a delay is therefore not covered by pretending that (1.4)
holds; it must be exposed as a moving evaluation on a stronger orbit space.

For each \(N\), let \(A_N:D(A_N)\subset E_N\to E_N\) generate a strongly
continuous semigroup \(T_N(r)\) satisfying

\[
 \|T_N(r)\|_{\mathcal L(E_N)}
 \leq M e^{-\beta r},
 \qquad r\geq0,\quad N\in\mathfrak N,
 \tag{1.5}
\]

with the same \(M\geq1\) and \(\beta>0\).  The generators may be unbounded.
In particular, the theorem does not use a matrix representation of \(A_N\).

Let \(q_0\in C_b^{12}(U,U)\) be a bounded complete vector field.  Assume
that every vector field in a fixed sufficiently small \(C_b^1\)
neighborhood of \(q_0\) is complete.  Let

\[
 \begin{aligned}
 F_N&:U\times E_N\times Y_N\times
      [-\rho_*,\rho_*]\times\widehat{\mathcal P}\longrightarrow U,\\
 G_N&:U\times E_N\times Y_N\times
      [-\rho_*,\rho_*]\times\widehat{\mathcal P}\longrightarrow E_N
 \end{aligned}
 \tag{1.6}
\]

extend to an open neighborhood of
\([-\rho_*,\rho_*]\times\widehat{\mathcal P}\) and be \(C_b^{12}\) there.
All Frechet
derivatives through order twelve, in the product operator norms induced by
(1.1), are assumed bounded by one constant \(K_{12}\), uniformly in \(N\).
These uniform bounds, rather than a
coordinatewise bound, are essential.  Replacing the product norm by an
uncontrolled Euclidean coordinate norm could reintroduce factors such as
\(N^{1/2}\).

For \(\rho>0\), consider the prepared retarded system

\[
 \begin{aligned}
 u'(s)&=q_0(u(s))+
 \rho F_N\bigl(u(s),h(s),\mathscr D_{N,\lambda}x_s;
               \rho,\lambda\bigr),\\
 \rho h'(s)&=A_Nh(s)+
 \rho G_N\bigl(u(s),h(s),\mathscr D_{N,\lambda}x_s;
               \rho,\lambda\bigr),
 \end{aligned}
 \tag{1.7}
\]

where \(x_s(\vartheta)=(u(s+\vartheta),h(s+\vartheta))\).  The second line
is interpreted in the mild sense when \(A_N\) is unbounded.  Standard local
well-posedness of this semilinear RFDE is assumed in the phase space
\(C([-\Theta,0],X_N)\); it follows, for example, from the bounded local
Lipschitz hypotheses already imposed.

## 2. The dimension-uniform fixed-tube theorem

For a complete \(C_b^1\) vector field \(Q:U\to U\), write
\(\Phi_Q^s\) for its flow.  For \(H:U\to E_N\), define the complete graph
history based at \(u\) by

\[
 \mathcal I_{Q,H}(u)(\vartheta)
 =\bigl(\Phi_Q^\vartheta u,
        H(\Phi_Q^\vartheta u)\bigr),
 \qquad -\Theta\leq\vartheta\leq0,
 \tag{2.1}
\]

and abbreviate

\[
 \mathcal E_{N,\lambda}[Q,H](u)
 =\bigl(u,H(u),
        \mathscr D_{N,\lambda}\mathcal I_{Q,H}(u)\bigr).
 \tag{2.2}
\]

The derivative-free special-flow transform is

\[
 \begin{aligned}
 \mathcal T_{Q,N}(Q,H)(u)
 &=q_0(u)+\rho
 F_N\bigl(\mathcal E_{N,\lambda}[Q,H](u);
          \rho,\lambda\bigr),\\
 \mathcal T_{H,N}(Q,H)(u)
 &=\rho\int_0^\infty T_N(r)
 G_N\bigl(
   \mathcal E_{N,\lambda}[Q,H](\Phi_Q^{-\rho r}u);
   \rho,\lambda\bigr)\,dr.
 \end{aligned}
 \tag{2.3}
\]

For \(\rho<0\), (2.3) is only an auxiliary smooth fixed-point equation used
for Taylor expansion.  The RFDE interpretation is asserted only at
\(\rho>0\).

### Theorem 2.1 (uniform Banach-fiber history graph)

Under (1.1)--(1.6), there are \(0<\rho_0<\rho_*\) and \(C>0\), independent
of \(N\), such that for every

\[
 N\in\mathfrak N,\qquad |\rho|\leq\rho_0,\qquad
 \lambda\in\mathcal P,
\]

the transform (2.3) has a unique fixed point
\((Q_{N,\rho,\lambda},H_{N,\rho,\lambda})\)
in one common Lipschitz neighborhood of \((q_0,0)\).  On each parameter
slice,

\[
 \|Q_{N,\rho,\lambda}-q_0\|_{C_b^1}
 +\|H_{N,\rho,\lambda}\|_{C_b^1(U,E_N)}
 \leq C|\rho|.
 \tag{2.4}
\]

For a map into \(U\times E_N\), the notation
\(\|D_{\mathcal R}^ef\|_{C_b^a}\) means the supremum operator norm in

\[
 \mathcal L_{\mathrm{sym}}^a\left(
 U;\mathcal L_{\mathrm{sym}}^e
 (\mathfrak R;U\times E_N)\right).
 \tag{2.4a}
\]

With this convention, the fixed points have the uniform mixed regularity

\[
 \max_{\substack{0\leq b\leq3,
                  \,0\leq i\leq1,
                  \,0\leq e\leq2}}
 \left\|
 \partial_\rho^b\partial_\nu^iD_{\mathcal R}^e
       (Q_{N,\rho,\lambda},H_{N,\rho,\lambda})
 \right\|_{C_b^{\,9-b-i-e}}
 \leq C.
 \tag{2.5}
\]

Here and below every norm is an operator norm; the right-hand side is not
multiplied by \(\dim E_N\).  Define

\[
 Z_{0}=(q_0,0),
 \qquad
 Z_{j,N,\lambda}=\frac1{j!}
 \partial_\rho^j
 (Q_{N,\rho,\lambda},H_{N,\rho,\lambda})\big|_{\rho=0},
 \quad j=1,2.
 \tag{2.6}
\]

Then

\[
 (Q_{N,\rho,\lambda},H_{N,\rho,\lambda})
 =Z_0+\rho Z_{1,N,\lambda}+\rho^2Z_{2,N,\lambda}
   +\rho^3R_{3,N}(\rho,\lambda),
 \tag{2.7}
\]

and the mixed residual jets satisfy

\[
 \max_{\substack{0\leq i\leq1\\0\leq e\leq2}}
 \|\partial_\nu^iD_{\mathcal R}^e
 R_{3,N}(\rho,\lambda)\|_{C_b^3}
 \leq C.
 \tag{2.8}
\]

If \(\phi_0^s\) is the flow of \(q_0\), put

\[
 \mathcal I_0(u)(\vartheta)=(\phi_0^\vartheta u,0),
 \qquad
 \zeta_{0,N,\lambda}(u)
 =\bigl(u,0,\mathscr D_{N,\lambda}\mathcal I_0(u)\bigr).
 \tag{2.9}
\]

The first coefficients are

\[
 \begin{aligned}
 Q_{1,N,\lambda}(u)
 &=F_N(\zeta_{0,N,\lambda}(u);0,\lambda),\\
 H_{1,N,\lambda}(u)
 &=\int_0^\infty T_N(r)\,dr\,
     G_N(\zeta_{0,N,\lambda}(u);0,\lambda)\\
 &=-A_N^{-1}G_N(\zeta_{0,N,\lambda}(u);0,\lambda).
 \end{aligned}
 \tag{2.10}
\]

Exponential stability in (1.5) implies \(0\in\rho(A_N)\) and
\(\|A_N^{-1}\|\leq M/\beta\), so (2.10) is meaningful even when \(A_N\)
is unbounded.  Semigroup integrals in this document are strong operator
integrals: they are defined by Bochner integration after application to a
vector in \(E_N\).  Norm continuity of \(r\mapsto T_N(r)\) is not assumed.

For every physical \(0<\rho\leq\rho_0\), the map

\[
 \iota_{N,\rho,\lambda}:U\longrightarrow C([-\Theta,0],X_N),
 \qquad
 \iota_{N,\rho,\lambda}(u)
 =\mathcal I_{Q_{N,\rho,\lambda},H_{N,\rho,\lambda}}(u),
 \tag{2.11}
\]

is an injective \(C^3\) embedding.  If
\(\mathcal S_{N,\lambda}^s\) is the mild
semiflow of the prepared equation, then

\[
 \mathcal S_{N,\lambda}^s\iota_{N,\rho,\lambda}(u)
 =\iota_{N,\rho,\lambda}
   (\Phi_{Q_{N,\rho,\lambda}}^s u),
 \qquad s\geq0.
 \tag{2.12}
\]

If the current graph points and their whole delay-support backtracks lie in
a region where the preparation agrees with the physical equation, (2.12) is
an exact identity for that physical RFDE on the retained segment.

The constants \(\rho_0,C\) depend only on the fixed jet orders, the fixed
reduced dimension and parameter cylinder, \(\Theta\), the \(C^{12}\) bound of
\(q_0\), \(K_{12}\), \(B_{\mathrm{TV}}\), and \((M,\beta)\).  In
the direct-composite alternative to (1.4d), they also depend on that declared
uniform composite bound.  In particular, they do not depend on \(N\),
\(\dim E_N\), the number of delay
atoms, or a matrix realization of \(A_N\).

### Banach perturbation responses supplied by the theorem

Write \(Z_N=(Q_N,H_N)\).  For
\(\widehat{\mathcal R}_1,\widehat{\mathcal R}_2\in\mathfrak R\),
Theorem 2.1 gives genuine Frechet tensors

\[
 D_{\mathcal R}Z_N[\widehat{\mathcal R}_1]\in C_b^8(U;U\times E_N),
 \qquad
 D_{\mathcal R}^2Z_N[
 \widehat{\mathcal R}_1,\widehat{\mathcal R}_2]
 \in C_b^7(U;U\times E_N),
 \tag{2.13}
\]

with operator norms bounded uniformly in \(N\).  Differentiating the
fixed-point identity twice gives, block by block on the triangular scale
(3.9),

\[
 \begin{aligned}
 D_{\mathcal R}Z_N
 &=D_{\mathcal R}\mathcal T_N
   +D_Z\mathcal T_N[D_{\mathcal R}Z_N],\\
 D_{\mathcal R}^2Z_N[
   \widehat{\mathcal R}_1,\widehat{\mathcal R}_2]
 &=D_{\mathcal R}^2\mathcal T_N[
      \widehat{\mathcal R}_1,\widehat{\mathcal R}_2]
   +D_{Z\mathcal R}^2\mathcal T_N[
      D_{\mathcal R}Z_N[\widehat{\mathcal R}_1],
      \widehat{\mathcal R}_2]\\
 &\quad
   +D_{Z\mathcal R}^2\mathcal T_N[
      D_{\mathcal R}Z_N[\widehat{\mathcal R}_2],
      \widehat{\mathcal R}_1]
   +D_Z^2\mathcal T_N[
      D_{\mathcal R}Z_N[\widehat{\mathcal R}_1],
      D_{\mathcal R}Z_N[\widehat{\mathcal R}_2]]\\
 &\quad
   +D_Z\mathcal T_N[
      D_{\mathcal R}^2Z_N[
       \widehat{\mathcal R}_1,\widehat{\mathcal R}_2]].
 \end{aligned}
 \tag{2.14}
\]

In each current highest block, the last term in the corresponding line has
operator norm at most \(C\rho_0<1/2\); all other terms are already known
sources.  Thus (2.14) uniquely determines the response tensors and gives
(2.13).  Formula (2.14) is deliberately read on the ordered scale (3.9).
It is not a claim that one same-space derivative
\(D_Z\mathcal T_N:C_b^3\to C_b^3\) is bounded.  Establishing a common
weighted space for (2.14) and the later Schur--Melnikov residual remains the
linkage gate stated above.

## 3. Proof of Theorem 2.1

The proof is included to identify every place at which network size could
otherwise enter.

### 3.1 Uniform order-zero contraction

Fix \(L>\operatorname{Lip}(q_0)\).  On the closed set of bounded Lipschitz
pairs satisfying

\[
 \begin{aligned}
 \|Q-q_0\|_\infty+\operatorname{Lip}(Q-q_0)&\leq b_Q\rho_0,\\
 \|H\|_\infty+\operatorname{Lip}(H)&\leq b_H\rho_0,
 \qquad \operatorname{Lip}(Q)\leq L,
 \end{aligned}
 \tag{3.1}
\]

use the uniform product metric.  This is a complete metric space for every
\(N\): a uniform Cauchy sequence converges in \(C_b(U,U\times E_N)\), and
the fixed Lipschitz inequalities pass to the uniform limit.  If
\(Q,\widetilde Q\) belong to this set, Gronwall gives

\[
 \sup_u|\Phi_Q^t u-\Phi_{\widetilde Q}^t u|
 \leq |t|e^{L|t|}\|Q-\widetilde Q\|_\infty.
 \tag{3.2}
\]

Combining (3.2) with the Lipschitz bound for \(H\), and then using (1.3),
gives

\[
 \begin{aligned}
 &\|\mathscr D_{N,\lambda}\mathcal I_{Q,H}(u)
      -\mathscr D_{N,\lambda}
       \mathcal I_{\widetilde Q,\widetilde H}(u)\|\\
 &\qquad\leq
 C B_{\mathrm{TV}}e^{L\Theta}(1+\Theta)
 \bigl(\|Q-\widetilde Q\|_\infty
       +\|H-\widetilde H\|_\infty\bigr).
 \end{aligned}
 \tag{3.3}
\]

At the shifted base point \(\Phi_Q^{-\rho r}u\), the same argument uses a
flow length at most \(\Theta+|\rho|r\), and yields the majorant

\[
 C(1+B_{\mathrm{TV}})
 (1+\Theta+|\rho|r)e^{L(\Theta+|\rho|r)}
 \|(Q,H)-(\widetilde Q,\widetilde H)\|_{C^0}.
 \tag{3.4}
\]

The two transform components therefore satisfy

\[
 \begin{aligned}
 \|\mathcal T_{Q,N}(Z)-\mathcal T_{Q,N}(\widetilde Z)\|_\infty
 &\leq C|\rho|(1+B_{\mathrm{TV}})\|Z-\widetilde Z\|_{C^0},\\
 \|\mathcal T_{H,N}(Z)-\mathcal T_{H,N}(\widetilde Z)\|_\infty
 &\leq C|\rho|M(1+B_{\mathrm{TV}})e^{L\Theta}\\
 &\quad\times\int_0^\infty
 (1+r)e^{-(\beta-L\rho_0)r}\,dr
 \|Z-\widetilde Z\|_{C^0}.
 \end{aligned}
 \tag{3.5}
\]

For completeness, the corresponding state-Lipschitz estimates are

\[
 \begin{aligned}
 \operatorname{Lip}(\mathcal T_{Q,N}-q_0)
 &\leq C|\rho|(1+B_{\mathrm{TV}})e^{L\Theta},\\
 \operatorname{Lip}(\mathcal T_{H,N})
 &\leq C|\rho|M(1+B_{\mathrm{TV}})e^{L\Theta}
 \int_0^\infty e^{-(\beta-L\rho_0)r}\,dr.
 \end{aligned}
 \tag{3.5a}
\]

Indeed, two histories based at \(u,\widetilde u\) differ by at most
\(C e^{L(\Theta+|\rho|r)}|u-\widetilde u|\); (1.3) and (1.5) then give
(3.5a).  Choose \(L\rho_0<\beta/2\), and then decrease \(\rho_0\) until
the sum of the two coefficients in (3.5) is smaller than one.  The size
estimates

\[
 \|\mathcal T_{Q,N}(Z)-q_0\|_\infty
 \leq |\rho|K_{12},
 \qquad
 \|\mathcal T_{H,N}(Z)\|_\infty
 \leq |\rho|\frac{M}{\beta}K_{12}
 \tag{3.6}
\]

and (3.5a) show, after choosing \(b_Q,b_H\), that the ball (3.1) is
invariant.  Banach's theorem gives a unique fixed point there.
Applying (3.6) at the fixed point gives the sharper slice bound (2.4).

Equations (3.3)--(3.6) are the entire dimension audit at order zero.  Every
finite atom sum from the two-module proof has been replaced by the single
factor \(B_{\mathrm{TV}}\).

### 3.2 Uniform mixed jets

For a parameter-dependent map \(f\), write

 \[
 J_{a,b,i,e}f
 =D_u^a\partial_\rho^b\partial_\nu^iD_{\mathcal R}^ef,
 \qquad
 n=a+b+i+e,
 \qquad
 \wp=b+i+e.
 \tag{3.7}
\]

Use the triangular family

 \[
 \mathcal J_k=
 \{(a,b,i,e):b\leq3,\ i\leq1,\ e\leq2,
                 \ a+b+i+e\leq k\}.
 \tag{3.8}
\]

Order its blocks first by \(n\) and, at equal \(n\), by \(\wp\).  Bound
the Picard iterates through \(\mathcal J_{10}\) and prove convergence
through \(\mathcal J_9\).  The last grade is the one spatial derivative
needed when a highest flow jet is evaluated on two different orbits.

For every block, use the common Banach fiber

 \[
 \prod_{(a,b,i,e)\text{ in the block}}
 C_b\left([-\rho_0,\rho_0]\times\mathcal P;
 C_b\bigl(U,
   \mathcal L_{\mathrm{sym}}^a\bigl(
   U;\mathcal L_{\mathrm{sym}}^e
   (\mathfrak R;U\times E_N)\bigr)\bigr)
 \right)
 \tag{3.9}
\]

with the maximum operator norm.  These are different spaces for different
\(N\), but all contraction radii and factors below are the same.
Start the smooth Picard iteration at
\(Z^{(0)}_N=(q_0,0)\) and set
\(Z^{(k+1)}_N=\mathcal T_N(Z^{(k)}_N)\).

The ordinary variational equations for \(\Phi_Q^t\), followed by induction
in the ordering (3.8), give, uniformly for
\(-\Theta\leq\vartheta\leq0\),

\[
 \|J_{a,b,i,e}\Phi_Q^{\vartheta-\rho r}\|_\infty
 \leq C(1+r^m)e^{\Gamma(\Theta+|\rho|r)}.
 \tag{3.10}
\]

A difference of two such jets is bounded by the same factor times the
current block difference plus preceding-block differences.  The constants
in (3.10) involve only derivatives of the \(U\)-valued field \(Q\), whose
domain dimension is fixed.  Applying \(\mathscr D_{N,\lambda}\), or one of its
parameter derivatives, multiplies the resulting bound by at most
\(C B_{\mathrm{TV}}\), where \(C\) depends only on the finite jet order.
Choose \(\rho_0\) so that

\[
 \Gamma\rho_0<\frac\beta2
 \tag{3.11}
\]

for all of the finitely many required jets.  Every differentiated stable
integrand is then dominated by

\[
 C(1+r^m)e^{-\beta r/2},
 \tag{3.12}
\]

uniformly in \(N\).  This justifies differentiation under the Bochner
integral in (2.3).

We record the triangular point explicitly.  For a terminal time independent
of the parameters, a first variation in
\(\xi=\rho,\nu\), or a direction
\(\widehat{\mathcal R}\in\mathfrak R\), solves

\[
 \frac{d}{dt}D_\xi\Phi_Q^t
 =DQ(\Phi_Q^t)D_\xi\Phi_Q^t
  +(D_\xi Q)(\Phi_Q^t).
 \tag{3.12a}
\]

After arbitrary mixed differentiation, the equation for the current flow
jet is linear in that jet.  The occurrence of the current jet of \(Q\) is
also linear.  If a parameter derivative strikes the argument of a
vector-field jet, that vector-field jet gains a state slot and loses a
parameter derivative, so it lies in an earlier block of (3.8).  A product
of two positive-grade jets uses two strictly lower total grades.  Substituting
the terminal time \(\vartheta-\rho r\) adds only powers of \(r\), because a
\(\rho\)-derivative of the terminal time is converted by
\(\partial_t\Phi_Q^t=Q(\Phi_Q^t)\).  Subtracting two variational systems
requires one additional state derivative of \(Q\), which is the reserved
grade \(\mathcal J_{10}\).

Next differentiate
\(\mathscr D_{N,\lambda}\mathcal I_{Q,H}\).  For
\(\widehat{\mathcal R}_1,\ldots,\widehat{\mathcal R}_e\in\mathfrak R\),
the Frechet product rule is

\[
 \begin{aligned}
 &D_{\mathcal R}^e
 \bigl(\mathscr D_{N,\lambda}\mathcal I_{Q,H}\bigr)
 [\widehat{\mathcal R}_1,\ldots,\widehat{\mathcal R}_e]\\
 &\quad=
 \sum_{S\subset\{1,\ldots,e\}}
 \bigl(D_{\mathcal R}^{|S|}\mathbb B_{N,\lambda}\bigr)
 [\widehat{\mathcal R}_j:j\in S]\,
 \bigl(D_{\mathcal R}^{e-|S|}\mathcal I_{Q,H}\bigr)
 [\widehat{\mathcal R}_j:j\notin S],
 \qquad e=0,1,2.
 \end{aligned}
 \tag{3.12b}
\]

Here the first factor acts by integration on the history in the second
factor.  Applying the optional \(\nu\)-derivative distributes once across
the same factors and is controlled by the mixed part of (1.4).  Thus the
product rule produces a derivative
of the measure and a graph-history jet.  Estimate (1.4) bounds the former.
At order zero in the graph-history jet, write
\(\mathcal I_{Q,H}=\mathbf i_N+
(\mathcal I_{Q,H}-\mathbf i_N)\), where
\(\mathbf i_N(u)(\vartheta)=(u,0)\).  The second summand is uniformly
bounded because \(Q\) is bounded and the delay horizon is fixed; (1.4d)
kills the first summand whenever a parameter derivative strikes the
measure.  This is the affine-anchor step that cannot be obtained from total
variation alone.

If the measure derivative has positive parameter grade, the graph-history
jet has lower parameter grade; otherwise its current highest graph jet occurs
linearly.  In either case (1.3) supplies the same dimension-free bound.

Faà di Bruno's formula for \(F_N\) and \(G_N\) has at most one factor of the
current total grade.  Together with the preceding two paragraphs, this gives
the following highest-block form:

\[
 \mathbf J_{n,\wp}\mathcal T_N(Z)
 =b_{n,\wp}(\mathbf J_{<n,\wp}Z)
  +\rho\,\mathcal L_{n,\wp}
       (\mathbf J_{<n,\wp}Z)
       [\mathbf J_{n,\wp}Z].
 \tag{3.13}
\]

The first pure spatial block is nonlinear, but its difference has the same
factor \(|\rho|\).  If a \(\rho\)-derivative strikes the displayed factor,
the remaining graph jet has lower \(\rho\)-grade and belongs to \(b\).
Consequently

\[
 \begin{aligned}
 &\|\mathbf J_{n,\wp}\mathcal T_N(Z)
       -\mathbf J_{n,\wp}\mathcal T_N(\widetilde Z)\|\\
 &\qquad\leq C|\rho|
   \|\mathbf J_{n,\wp}Z-\mathbf J_{n,\wp}\widetilde Z\|
   +C d_{<n,\wp}(Z,\widetilde Z),
 \end{aligned}
 \tag{3.14}
\]

with one \(C\) valid for every \(N\).  Induction over the finite block list
first gives invariant jet balls: after all preceding radii have been fixed,
the current recurrence has the form
\[
 \|\mathbf J_{n,\wp}\mathcal T_N(Z)\|
 \leq B_{n,\wp}+C\rho_0\|\mathbf J_{n,\wp}Z\|.
 \tag{3.14a}
\]
Taking \(C\rho_0<1/2\) and a radius larger than \(2B_{n,\wp}\) closes that
fiber.  Applied to consecutive Picard iterates,
(3.14) then gives

\[
 a_{k+1}\leq\kappa a_k+Cq^k,
 \qquad \max\{\kappa,q\}<1.
 \tag{3.15}
\]

Thus the jets converge strongly in their common fibers.  The fundamental
theorem of calculus on state and parameter line segments identifies their
limits as actual derivatives.  In particular, for
\(\mathcal R,\mathcal R+\widehat{\mathcal R}\) in the buffered open
cylinder,

\[
 f_k(\mathcal R+\widehat{\mathcal R})-f_k(\mathcal R)
 =\int_0^1D_{\mathcal R}f_k
   (\mathcal R+t\widehat{\mathcal R})
   [\widehat{\mathcal R}]\,dt.
 \tag{3.15a}
\]

Uniform convergence of \(f_k\) and \(D_{\mathcal R}f_k\) passes (3.15a) to
the limit and identifies the first Frechet derivative.  Applying the same
identity to \(D_{\mathcal R}f_k\) identifies
\(D_{\mathcal R}^2f\).  This proves the asserted
\(C_{\mathcal R}^2\) regularity and, in particular, supplies the
\(D_{\mathcal R}\) and \(D_{\mathcal R}^2\) graph responses needed by the
successor root calculation.  No compactness of the parameter ball and no
finite-dimensional property of \(E_N\) is used.

At \(\rho=0\), (2.3) is the constant map \((q_0,0)\).  Taylor's integral
formula gives

\[
 R_{3,N}(\rho,\lambda)
 =\frac12\int_0^1(1-t)^2
   \partial_\rho^3
   (Q_{N,t\rho,\lambda},H_{N,t\rho,\lambda})\,dt.
 \tag{3.16}
\]

Equations (2.7)--(2.8) follow from (2.5).  Differentiating (2.3) once at
\(\rho=0\) proves (2.10).  This also shows directly that the first graph
coefficient is uniformly bounded by \(K_{12}(1+M/\beta)\).

### 3.3 Exact complete histories for an unbounded generator

The matrix proof differentiates the stable convolution.  That step is not
valid without qualification for an unbounded \(A_N\).  Instead fix
\(\rho>0\), let

\[
 u(s)=\Phi_Q^su_*,
 \qquad h(s)=H(u(s)),
\]

and denote the \(G_N\)-forcing along this complete graph curve by \(g(s)\).
The second fixed-point equation is exactly

\[
 h(s)=\int_{-\infty}^s
 T_N\left(\frac{s-\tau}{\rho}\right)g(\tau)\,d\tau.
 \tag{3.17}
\]

For \(s\geq s_0\), split the integral at \(s_0\) and use the semigroup
law.  This gives

\[
 h(s)=T_N\left(\frac{s-s_0}{\rho}\right)h(s_0)
 +\int_{s_0}^s
 T_N\left(\frac{s-\tau}{\rho}\right)g(\tau)\,d\tau.
 \tag{3.18}
\]

Equation (3.18) is precisely the mild stable equation.  The first
fixed-point equation gives the classical \(u\)-equation, including its
complete delay history.  Uniqueness of mild RFDE solutions therefore yields
(2.12).  Present-time evaluation followed by projection to \(U\) is a
continuous left inverse of (2.11).  It is also a left inverse of its
differential.  Hence (2.11) is injective, is a homeomorphism onto its image,
and is a \(C^3\) immersion.  This proves the embedding assertion without
requiring \(H(U)\subset D(A_N)\).

## 4. Uniform logarithmic fold tube

The fixed-tube theorem is abstract.  The following corollary records the
additional, model-specific estimate needed by a canard passage.

Assume now that \(U=\mathbb R^2\) and, before preparation,

\[
 q_0(X,Y)=\binom{Y-\alpha X^2}{-X},
 \qquad \alpha>0.
 \tag{4.1}
\]

Use the polynomial coordinates

\[
 \chi=-2\alpha X,
 \qquad
 d=Y-\alpha X^2+\frac1{2\alpha}.
 \tag{4.2}
\]

Their inverse, used below, is

\[
 \Gamma(\chi,d)=
 \left(-\frac{\chi}{2\alpha},
 d+\frac{\chi^2}{4\alpha}-\frac1{2\alpha}\right).
 \tag{4.2a}
\]

Then the singular canard is \(d=0\) and

\[
 \chi'=1-2\alpha d,
 \qquad d'=\chi d.
 \tag{4.3}
\]

Fix \(p_{\mathrm{log}}>4\) and

\[
 S_\delta=\sqrt{2p_{\mathrm{log}}\log(1/\delta)}.
 \tag{4.4}
\]

Let \(N_{\mathrm{bl}}\) be the number of mixed-jet blocks used in (3.8),
choose \(D>2N_{\mathrm{bl}}+3\), and fix

\[
 1>\kappa_0>\kappa_1>\cdots>\kappa_D>0.
 \tag{4.5}
\]

With \(T_*=\Theta+1\) and fixed buffers \(B_j=jT_*\), define

 \[
 \mathcal U_j(\delta)=
 \{\Gamma(\chi,d):|\chi|\leq S_\delta+B_j,
             \ |d|\leq\delta^{\kappa_j}\}.
 \tag{4.6}
\]

We now prescribe the preparation rather than infer its flow bounds from a
generic polynomial \(C^J\) estimate.  Let
\(\omega\in C_c^\infty(\mathbb R)\) equal one on \([-1,1]\) and vanish
outside \([-2,2]\).  Fix \(d_*>0\), choose
\(B_*>B_D+2(\Theta+1)+2\), and set

\[
 \Xi_S(\chi,d)=
 \omega\left(\frac{\chi}{S+B_*}\right)
 \omega\left(\frac d{d_*}\right).
 \tag{4.6a}
\]

In the \((\chi,d)\) coordinates, prepare the singular field by

\[
 q_{0,S}(\chi,d)=
 \Xi_S(\chi,d)\binom{1-2\alpha d}{\chi d}.
 \tag{4.6b}
\]

This field is compactly supported and therefore complete.
Assume that \(F_N,G_N\) admit global preparations which agree with the
physical data on the uncut set declared below.  In finite-dimensional fibers
these can be made with slotwise cutoffs; existence of smooth bump functions
on an arbitrary Banach fiber is not asserted here.  Put
\(z=(u,h,y)\in U\times E_N\times Y_N\) and \(J=12\).  Require the prepared
transformed Frechet jets to obey

\[
 \sup_{\substack{N,\ |\rho|\leq\delta\\
                  \lambda\in\widehat{\mathcal P}}}
 \max_{\substack{a+b+i+e\leq J\\
                  b\leq3,\ i\leq1,\ e\leq2}}
 \left(
 \|D_z^a\partial_\rho^b\partial_\nu^iD_{\mathcal R}^e
      F_{N,S}\|_\infty
 +\|D_z^a\partial_\rho^b\partial_\nu^iD_{\mathcal R}^e
      G_{N,S}\|_\infty
 \right)
 \leq P_J(S)
 \tag{4.6c}
\]

for one polynomial \(P_J\), uniformly on
\(\widehat{\mathcal P}\).  The graph construction and its flow estimates are
performed in the \((\chi,d)\) coordinates; (4.2a) converts the resulting
history graph back to \((X,Y)\).  For each target \(\delta\), first freeze
this preparation at \(S=S_\delta\), and only then introduce the dummy
amplitude \(\rho\in[-\delta,\delta]\).  Retain (1.4)--(1.5) with the same
constants.

The preparation is required to agree with the physical data on an open
neighborhood of the continuous depth-two delay-flow hull

\[
 \mathfrak H^{[2]}(\mathcal U_D)
 =\{\phi_0^{-t}u:u\in\mathcal U_D,
                    0\leq t\leq2\Theta\},
 \tag{4.7}
\]

enlarged by one fixed buffer and by the \(o(1)\) stable-convolution
backtracks used below.  This neighborhood includes a fixed ball
\(\|h\|_{E_N}\leq h_*\) in every stable current and history slot, with the
same \(h_*>0\) for all \(N\).  For a distributed delay, (4.7), not a list
of endpoints, is the required uncut set.

### Corollary 4.1 (dimension-uniform logarithmic graph jet)

Under these assumptions there are \(\delta_0,C,c,m>0\), independent of
\(N\), such that for every \(0<\delta\leq\delta_0\) and uniformly for
\(\lambda\in\mathcal P\), the frozen transform has a unique fixed-point
family for all \(|\rho|\leq\delta\).  Suppress \(\lambda\) in the notation
below.  At
\(\rho=\delta\), on the core tube \(\mathcal U_0(\delta)\),

\[
 (Q_{N,\delta},H_{N,\delta})
 =(q_0,0)+\delta Z_{1,N}+\delta^2Z_{2,N}
   +\delta^3R_{3,N},
 \tag{4.8}
\]

and

\[
 \max_{\substack{0\leq a\leq3,
                  \,0\leq i\leq1,
                  \,0\leq e\leq2}}
 \left\|
 D_u^a\partial_\nu^iD_{\mathcal R}^e
 R_{3,N}(\Gamma(\chi,d))
 \right\|_{U\times E_N}
 \leq C\langle\chi\rangle^m e^{c|\chi|}.
 \tag{4.9}
\]

The first two coefficients in (4.8) depend only on the physical data on the
depth-one and depth-two continuous flow hulls, respectively.  They are
therefore independent of any two admissible outer preparations that agree
on (4.7).  The history map (2.11) remains an exact injective embedding and
satisfies the exact mild semiconjugacy (2.12) on every retained segment whose
whole delay-support backtrack lies in the uncut hull.

### Proof

For every fixed flow time \(0\leq t\leq T\), (4.3) and its variational
equations give

\[
 \|D^k\phi_0^{-t}(\Gamma(\chi,d))\|
 \leq C_{k,T}\langle\chi\rangle^{m_k}e^{c_{k,T}|\chi|}
 \tag{4.10}
\]

while the segment remains in a fixed normal tube.  The exponential factor is
genuine: on \(d=0\), the backward normal multiplier is
\(\exp(-\chi t+t^2/2)\).  Thus a polynomial-only bound would be false.

We next derive the tame global flow bound from the declared preparation.
On the support of \(\Xi_S\),

\[
 \left|\binom{1-2\alpha d}{\chi d}\right|
 +\left\|D_{(\chi,d)}
 \binom{1-2\alpha d}{\chi d}\right\|
 \leq C(1+S).
 \tag{4.11a}
\]

The longitudinal derivative of \(\Xi_S\) is \(O((1+S)^{-1})\), while its
normal derivative is \(O(1)\).  The product rule in (4.6b) therefore gives

\[
 \operatorname{Lip}(q_{0,S})\leq C(1+S);
 \tag{4.11b}
\]

higher prepared derivatives are polynomial in \(S\).  On the graph-transform
jet balls and for \(|\rho|\leq\delta\), (4.6c) gives

\[
 \operatorname{Lip}(Q)
 \leq C(1+S)+\delta P_J(S)
 \leq \Gamma_J(S):=C_J(1+S)
 \tag{4.11c}
\]

after decreasing \(\delta_0\).  The last inequality uses
\(\delta P_J(S_\delta)\to0\).

Induction in the fixed finite family of flow variational equations, including
the one reserved state grade and their difference equations, now yields the
explicit tame bound

\[
 \|\mathscr J\Phi_Q^{\vartheta-\rho r}\|_\infty
 \leq
 \mathfrak B_J(S)(1+r^{m_J})
 e^{\Gamma_J(S)|\rho|r},
 \qquad
 \mathfrak B_J(S)=P_J^*(S)e^{C_JS},
 \tag{4.11}
\]

for every required mixed jet \(\mathscr J\),
\(-\Theta\leq\vartheta\leq0\), and \(r\geq0\).  The same bound, multiplied
by the current and preceding jet-block differences, holds for two vector
fields in the common graph ball.  Here \(P_J^*\) is a polynomial independent
of \(N\).  Since \(S_\delta=O(\sqrt{\log(1/\delta)})\),

\[
 \mathfrak B_J(S_\delta)=\delta^{-o(1)},\qquad
 \delta\mathfrak B_J(S_\delta)\longrightarrow0,\qquad
 \delta\Gamma_J(S_\delta)\longrightarrow0.
 \tag{4.11d}
\]

More generally,
\[
 \delta^a\mathfrak B_J(S_\delta)
 (1+\log(1/\delta))^{m_J}\longrightarrow0
 \tag{4.11e}
\]
for every fixed \(a>0\).  These are the tame limits used below; polynomial
prepared data bounds alone, without (4.11b)--(4.11), would not imply them.

Equations (1.3) and (1.5) introduce only the uniform factors
\(B_{\mathrm{TV}}\) and \(M e^{-\beta r}\).  Hence every order-zero or
highest-block contraction factor is bounded by

\[
 q_{\delta,N}
 \leq C\delta(1+B_{\mathrm{TV}})
 \mathfrak B_J(S_\delta)=o(1),
 \tag{4.12}
\]

uniformly in \(N\).  This proves the global fixed point and its finite mixed
jets for the one frozen cutoff.  The order-zero estimate also gives
\(\|H_{N,\rho}\|_\infty\leq
C\delta\mathfrak B_J(S_\delta)=o(1)\), so all retained stable slots lie in
the fixed uncut ball for small \(\delta\).

Set \(R_\delta=L\log(1/\delta)\) and split the stable integral only for the
purpose of estimating it.  After any required mixed differentiation, the
tail is bounded by

\[
 C\mathfrak B_J(S_\delta)
 (1+R_\delta)^{m_J}e^{-\beta R_\delta/2}.
 \tag{4.13}
\]

Here \(\delta_0\) has first been decreased so that
\(\Gamma_J(S_\delta)\delta<\beta/2\); half of the semigroup decay therefore
remains after the reduced-flow estimate.  Choose \(L\) after the finite jet
grade so that (4.13) is \(O(\delta^6)\).
For \(0\leq r\leq R_\delta\), the additional base-flow backtrack is at most

\[
 |\rho|r\leq\delta R_\delta=o(1).
 \tag{4.14}
\]

Because every gap \(\kappa_j-\kappa_{j+1}\) is positive,

\[
 \delta^{\kappa_j}\mathfrak B_J(S_\delta)
 +\delta\mathfrak B_J(S_\delta)
 \leq\frac12\delta^{\kappa_{j+1}}
 \tag{4.15}
\]

for small \(\delta\), uniformly in \(N\).  Thus each current or distributed
delay evaluation moves at most one level outward in the nested tubes.

Apply the triangular recurrence (3.13) in weighted local seminorms

\[
 \|V\|_{j;c,m}
 =\sup_{\Gamma(\chi,d)\in\mathcal U_j}
  \frac{\|V(\Gamma(\chi,d))\|}
       {\langle\chi\rangle^m e^{c|\chi|}}.
 \tag{4.16}
\]

Every lower block is evaluated one level farther out; the unique global
current-block term retains \(\rho\), and is \(o(1)\) by (4.12).  Finite
induction over the blocks closes before the outermost tube because of the
choice of \(D\).  Taylor's formula (3.16) then proves (4.8)--(4.9).

At \(\rho=0\), one differentiation of the history evaluation uses at most
one time in the support of \(\mathbb B_{N,\lambda}\).  A second differentiation
uses at most a sum of two such times and a variational integral along the
intervening reduced-flow segment.  Hence \(Z_{1,N}\) and \(Z_{2,N}\) sample
only the continuous hulls of depth one and two.

The stable component requires one extra check.  Write its transform as
\(\rho K_N(\rho,Z(\rho))\).  The coefficient \(H_{1,N}\) is
\(K_N(0,Z_0)\).  The coefficient \(H_{2,N}\) is the first derivative of
\(K_N(\rho,Z(\rho))\) at zero.  Its new terms contain \(Z_{1,N}\), one
reduced-flow variational integral, or one derivative of the base shift
\(\Phi_Q^{-\rho r}\) at zero.  The last term is
\(-r q_0(u)\), not a reduced-flow evaluation at an unbounded time.  The
semigroup moments obey

\[
 \left\|\int_0^\infty r^kT_N(r)\,dr\right\|
 \leq \frac{Mk!}{\beta^{k+1}},
 \qquad k=0,1,
 \tag{4.17}
\]

uniformly in \(N\).  Thus the stable convolution adds an integrable scalar
moment but no third delay backtrack.  Parameter derivatives of a
fixed-support measure do not enlarge its support.  This proves the asserted
depth-two cutoff independence for both components of \(Z_{2,N}\).

The fixed point itself still uses the full integral
\([0,\infty)\); (4.13) never replaces it by a truncated graph.  The mild
argument (3.17)--(3.18) therefore proves the exact history claim.
\(\square\)

## 5. What is reused, what is new, and what remains open

The finite-dimensional source proofs are
[special-flow-graph-theorem.md](special-flow-graph-theorem.md),
[mixed-jet-graph-proof.md](mixed-jet-graph-proof.md), and
[growing-tube-graph-proof.md](growing-tube-graph-proof.md).  Their
publication-form versions are Appendix B and Appendix C of the frozen JNS
manuscript.  The table states exactly which arguments can be cited directly
and which adaptations belong to Paper II.

The proof audit is as follows.

| Component | Status for Gate A | Reason |
|---|---|---|
| Derivative-free special-flow transform | Reused | Formula (2.3) is the existing transform with \(e^{Ar}\) replaced by \(T_N(r)\). |
| Finite delay atoms | Generalized here | Estimate (1.3) controls tangent histories; total variation replaces every atom count and matrix row sum, while (1.4d) handles the affine anchor in parameter derivatives. |
| Finite-dimensional Hurwitz block | Generalized here | The uniform semigroup bound (1.5) is sufficient for the contraction and all Bochner-integral estimates. |
| Exact stable equation | Reproved here | For an unbounded generator, the correct bridge is the mild identity (3.18), not unqualified differentiation of the convolution. |
| Mixed graph jets | Generalized here | The triangular common-fiber induction is retained, while (1.4), (1.4d), (3.9), and (3.12b) replace finite parameter coordinates by Frechet tensors on \(\mathfrak R\) and control the affine anchor. |
| First and second structural responses | Proved here | Uniform strong convergence in the Banach parameter fibers gives (2.13)--(2.14) and the line-segment closure (3.15a). |
| Third-order mixed remainder | Reused | It is the Banach-valued Taylor identity (3.16), after the uniform jet bound. |
| Logarithmic growing tube | Repaired here | The explicit cutoff (4.6a)--(4.6b) gives the linear Lipschitz bound and the tame envelope (4.11); distributed measures require continuous support hulls. |
| Exact history embedding | Strengthened here | Present-state evaluation gives the left inverse, and (3.18) proves exact mild semiconjugacy without \(H(U)\subset D(A_N)\). |

This closes only the invariant-history-graph part of Paper II.  It does not
close the following seams.

1. **Model fitting.**  An original node network must still be put into
   (1.7) with uniformly conditioned projections, a single critical fold
   chain, the semigroup estimate (1.5), the operator-TV bound (1.4), and the
   balanced-anchor condition (1.4d), or its direct transformed-data
   substitute, and the uniform \(C^{12}\) bound (1.6).  These cannot be
   assumed away in the final paper.
2. **Moving delays.**  Moving atoms fail (1.4).  They require explicit moving
   evaluation maps and one additional strong history derivative, with their
   own uniform composition proof.
3. **Multiple critical modes.**  The theorem presupposes the fixed reduced
   space \(U\).  It neither constructs that space nor reduces a vector canard
   gap to a scalar one.
4. **Outer physical selection.**  The graph is locally invariant, but the
   theorem does not identify arbitrary attracting and repelling outer slow
   histories with curves on it.
5. **Canard root and pulse event.**  No Lin gap, simple root, global return,
   spike separator, frequency, amplitude, or control conclusion follows from
   the graph theorem alone.
6. **Loss of uniform stability.**  If \(M=M_N\) grows, \(\beta=\beta_N\)
   vanishes, coordinate projections become ill-conditioned, or the network
   nonlinearities are bounded only componentwise, Theorem 2.1 remains a
   fixed-\(N\) statement but no longer gives a scalable conclusion.
7. **Neutral or state-dependent equations.**  The transform above is for a
   retarded semilinear equation with a fixed delay horizon.  Neutral terms and
   state-dependent delays require different phase spaces and are not covered.
8. **Order-one parameter dependence of the stable generator.**  The
   generators \(A_N\) are fixed in Theorem 2.1.  A family
   \(A_N(\lambda)\) needs
   uniform parameter derivatives of its semigroup or resolvent.  A bounded
   weak perturbation may instead be placed in \(G_N\), but an arbitrary
   order-one generator change cannot be hidden there.
9. **Concrete trace realization.**  The response tensors in
   (2.13)--(2.14) are constructed on an ordered \(C_b^k\) scale.
   The abstract history extension, present-state restriction, levelwise
   Schur inverse, and trace-to-gap response are now proved in
   [the Banach-scale linkage note](banach-scale-history-schur-link.md).
   Paper II must still realize its chosen weighted trace and residual spaces,
   trace inverse, moving endpoint maps, and complete-history matcher with
   the same dimension-uniform constants.

## 6. Gate A acceptance checks

The abstract gate may be cited as passed only when a proposed network family
supplies all of the following data with the displayed uniform bounds.

- [ ] A fixed two-dimensional reduced coordinate and uniformly conditioned
      critical/transverse projections.
- [ ] A proof of (1.5), including a dimension-independent transient constant
      \(M\), not only a static graph spectral gap.
- [ ] Operator-valued delay measures with a dimension-independent
      total-variation bound in the chosen network norm.
- [ ] For parameter-dependent measures, the balanced-anchor identity
      (1.4d), or a direct bound for the differentiated prepared composite.
- [ ] Uniform Frechet \(C^{12}\) bounds for the transformed nonlinearities;
      coordinatewise estimates do not suffice.
- [ ] A preparation which is physical on the full continuous depth-two flow
      hull.
- [ ] For structural responses, the exact
      \(C_\nu^1C_{\mathcal R}^2\) operator-TV bounds (1.4), or a separate
      strong-space proof for moving evaluations.
- [ ] A direct check that the physical RFDE is locally well posed in the
      stated history space.
- [x] An abstract three-level Banach-scale realization of the graph
      responses, history extension/restriction, and Schur operator.
- [ ] For the chosen node network, concrete weighted trace spaces, a uniform
      trace inverse, and complete-history endpoint maps satisfying the
      hypotheses of the Banach-scale linkage theorem.

Only after these checks does Theorem 2.1 provide an \(N\)-uniform object for
the root-response calculation.  It is not itself evidence that a chosen
biological network satisfies them.
