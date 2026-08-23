# Banach-scale response from a special-flow graph to a complete-history gap

Status: **the abstract Gate A--to--Gate C linkage is proved in this note.**
The proof uses the three levels \(C_b^9\), \(C_b^8\), and \(C_b^7\).
It does not invoke a \(C^2\) implicit-function theorem for the special-flow
residual on one \(C_b^k\) space.  Instead, the first structural response is
obtained by differentiating the fixed-point equation on the middle level,
and the second response is obtained on the lower level.  The resulting
linear response operators have the exact block Schur formulas on both
levels, with constants independent of the stable-fiber dimension.

The theorem is abstract in one important sense.  It proves the transfer once
a selected trace problem and its endpoint maps satisfy the scale assumptions
in Section 5.  It does not construct those selected traces for the node
network, prove a simple canard root, identify a physical pulse, evaluate the
candidate cubic coefficient, or prove that coefficient nonzero.  Those are
separate model-specific gates.

The invariant graph and its mixed jets come from
[the dimension-uniform special-flow theorem](dimension-uniform-special-flow-history-graph.md).
The block algebra and root calculation to which the present result connects
are in
[the Schur--Melnikov response note](general-network-schur-melnikov-proof.md).

## 1. Why a scale is needed

For a complete vector field \(Q\), the graph history contains the flow

\[
 \mathcal I_{Q,H}(u)(\vartheta)
 =\bigl(\Phi_Q^\vartheta u,
        H(\Phi_Q^\vartheta u)\bigr).
 \tag{1.1}
\]

Linearization in \(Q\) is harmless at a fixed smooth base field: its
variational equation defines a bounded operator on each response level
below.  Nonlinear differentiation is different.  A second variation
contains \(Dv\), where \(v\) is a first variation of \(Q\), and therefore
loses one state derivative.  Consequently, ordinary \(C^2\) regularity of

\[
 (Q,H)\longmapsto\mathcal I_{Q,H}
\]

as a self-map of one \(C_b^k\) space is neither assumed nor used.

The regularities needed here are exactly those already supplied by the
triangular Picard-jet proof:

\[
 Z_N\in C_b^9,\qquad
 D_{\mathcal R}Z_N\in C_b^8,\qquad
 D_{\mathcal R}^2Z_N\in C_b^7.
 \tag{1.2}
\]

## 2. Graph and complete-history spaces

Fix the reduced space \(U=\mathbb R^d\), the delay horizon
\(\Theta>0\), and a family of stable Banach fibers \(E_N\).  Put

\[
 X_N=U\times E_N,
 \qquad
 \|(u,h)\|_{X_N}=\max\{|u|,\|h\|_{E_N}\}.
 \tag{2.1}
\]

For \(j=0,1,2\), set \(r_j=7+j\) and define

\[
 \begin{aligned}
 \mathcal X_c^j&=C_b^{r_j}(U,U),\\
 \mathcal X_{\perp,N}^j&=C_b^{r_j}(U,E_N),\\
 \mathcal X_N^j&=\mathcal X_c^j\oplus\mathcal X_{\perp,N}^j.
 \end{aligned}
 \tag{2.2}
\]

We use the maximum product norm unless stated otherwise.  Forgetting the
highest derivatives gives bounded inclusions

\[
 \jmath_{kj,N}:\mathcal X_N^k\longrightarrow\mathcal X_N^j,
 \qquad 0\le j<k\le2,
 \qquad \|\jmath_{kj,N}\|\le1.
 \tag{2.3}
\]

They are restrictions of regularity, not smoothing maps.  No bounded right
inverse \(C_b^7\to C_b^8\) or \(C_b^8\to C_b^9\) is asserted or needed.

The full history \(\mathcal I_{Q,H}(u)\) is not bounded as a function of
\(u\), because its critical current component equals \(u\).  The correct
object is therefore an affine history space.  First define its tangent
space

\[
 \mathcal C_N^j
 =C_b^{r_j}\bigl(
 U;C([-\Theta,0],X_N)\bigr)
 \tag{2.4}
\]

with norm

\[
 \|\Psi\|_{\mathcal C_N^j}
 =\max_{0\le a\le r_j}
   \sup_{u\in U}\sup_{-\Theta\le\vartheta\le0}
   \|D_u^a\Psi(u)(\vartheta)\|.
 \tag{2.5}
\]

Let

\[
 \mathbf i_N(u)(\vartheta)=(u,0),
 \qquad
 \mathfrak C_N^j=\mathbf i_N+\mathcal C_N^j.
 \tag{2.5a}
\]

The difference
\(\mathcal I_{Q,H}-\mathbf i_N\) belongs to \(\mathcal C_N^j\), because
\[
 \Phi_Q^\vartheta u-u
 =\int_0^\vartheta Q(\Phi_Q^s u)\,ds
\]
is uniformly bounded on the fixed delay interval.  Define the affine
augmented history space and its tangent space by

\[
 \mathfrak A_N^j=\mathcal X_c^j\times\mathfrak C_N^j,
 \qquad
 \mathcal A_N^j=\mathcal X_c^j\oplus\mathcal C_N^j.
 \tag{2.6}
\]

The first component retains \(Q\).  Present-state evaluation of a graph
history recovers \(H\), but cannot recover a variation of the reduced vector
field.

### 2.1 History extension and present-state restriction

On the common neighborhood of complete vector fields used by the
special-flow theorem, define the nonlinear history extension

\[
 \mathbf E_N(Q,H)
 =\bigl(Q,\mathcal I_{Q,H}\bigr)\in\mathfrak A_N^2.
 \tag{2.7}
\]

Define the present-state restriction

\[
 \mathbf R_N(q,\Psi)
 =\bigl(q,\pi_E\Psi(\,\cdot\,)(0)\bigr),
 \qquad (q,\Psi)\in\mathfrak A_N^j.
 \tag{2.8}
\]

Its tangent map, denoted by the same symbol, is bounded from
\(\mathcal A_N^j\) to \(\mathcal X_N^j\).  Here
\(\pi_E:U\times E_N\to E_N\).  Then

\[
 \|D\mathbf R_N\|\le1,
 \qquad
 \boxed{\mathbf R_N\mathbf E_N(Z)=Z.}
 \tag{2.9}
\]

Thus \(\mathbf E_N\) is an actual complete-history extension of the graph,
not an identification modulo current state.

Fix a base graph \(Z_*=(Q_*,H_*)\in\mathcal X_N^2\), with its
\(C_b^9\) norm bounded independently of \(N\).  For
\(V=(v,k)\in\mathcal X_N^j\), let \(\chi_v^\vartheta(u)\) solve

\[
 \frac d{d\vartheta}\chi_v^\vartheta(u)
 =DQ_*(\Phi_*^\vartheta u)\chi_v^\vartheta(u)
  +v(\Phi_*^\vartheta u),
 \qquad
 \chi_v^0(u)=0,
 \tag{2.10}
\]

where \(\Phi_*\) is the flow of \(Q_*\).  The first Gate derivative of the
history extension is

\[
 \begin{aligned}
 \mathbf E'_{N,*}[V]
 =\Bigl(v,\ \vartheta\longmapsto
 \bigl(&\chi_v^\vartheta,\,
 k(\Phi_*^\vartheta)
 +DH_*(\Phi_*^\vartheta)\chi_v^\vartheta\bigr)\Bigr).
 \end{aligned}
 \tag{2.11}
\]

For \(j=0,1\), this defines a bounded linear map

\[
 \mathbf E'_{N,*}:\mathcal X_N^j\longrightarrow\mathcal A_N^j.
 \tag{2.12}
\]

For \(V=(v,k)\) and
\(\widetilde V=(\widetilde v,\widetilde k)\) in
\(\mathcal X_N^1\), the second flow variation solves

\[
 \begin{aligned}
 \frac d{d\vartheta}\chi_{v\widetilde v}^\vartheta
 ={}&DQ_*(\Phi_*^\vartheta)\chi_{v\widetilde v}^\vartheta
 +D^2Q_*(\Phi_*^\vartheta)
      [\chi_v^\vartheta,\chi_{\widetilde v}^\vartheta]\\
 &+Dv(\Phi_*^\vartheta)\chi_{\widetilde v}^\vartheta
  +D\widetilde v(\Phi_*^\vartheta)\chi_v^\vartheta,
 \qquad
 \chi_{v\widetilde v}^0=0.
 \end{aligned}
 \tag{2.13}
\]

The stable component of the second history variation is

\[
 \begin{aligned}
 &Dk(\Phi_*^\vartheta)\chi_{\widetilde v}^\vartheta
 +D\widetilde k(\Phi_*^\vartheta)\chi_v^\vartheta
 +D^2H_*(\Phi_*^\vartheta)
       [\chi_v^\vartheta,\chi_{\widetilde v}^\vartheta]\\
 &\hspace{38mm}
 +DH_*(\Phi_*^\vartheta)\chi_{v\widetilde v}^\vartheta.
 \end{aligned}
 \tag{2.14}
\]

Together with a zero \(Q\)-component, (2.13)--(2.14) define

\[
 \mathbf E''_{N,*}:
 \mathcal X_N^1\times\mathcal X_N^1
 \longrightarrow\mathcal A_N^0.
 \tag{2.15}
\]

The one-derivative drop in (2.15) is the reason for the scale.

### Lemma 2.1 (uniform history extension bounds)

There are constants \(C_{E,1},C_{E,2}\), depending only on
\(d,\Theta\) and the common \(C_b^9\) bound of \(Z_*\), such that,
uniformly in \(N\),

\[
 \|\mathbf E'_{N,*}V\|_{\mathcal A_N^j}
 \le C_{E,1}\|V\|_{\mathcal X_N^j},
 \qquad j=0,1,
 \tag{2.16}
\]

and

\[
 \|\mathbf E''_{N,*}[V,\widetilde V]\|_{\mathcal A_N^0}
 \le C_{E,2}
 \|V\|_{\mathcal X_N^1}
 \|\widetilde V\|_{\mathcal X_N^1}.
 \tag{2.17}
\]

Moreover,

\[
 \boxed{
 \mathbf R_N\mathbf E'_{N,*}=I,
 \qquad
 \mathbf R_N\mathbf E''_{N,*}=0.}
 \tag{2.18}
\]

**Proof.**  Differentiate the finite-time flow equation.  Equations
(2.10) and (2.13), their state variational equations through the indicated
orders, and Gronwall's inequality give (2.16)--(2.17).  Only the fixed
dimension of \(U\), the length \(\Theta\), and the stated graph norms enter.
At \(\vartheta=0\), (2.10) and (2.13) vanish, the stable component of
(2.11) is \(k(u)\), and (2.14) vanishes.  This proves (2.18).
\(\square\)

The same variational equations with integral remainders give the scale
chain rule needed later.  If a parameter curve \(Z(\mathcal R)\) is
Frechet differentiable into \(\mathcal X_N^1\) and twice Frechet
differentiable into \(\mathcal X_N^0\), then
\(\mathbf E_N(Z(\mathcal R))\) has the corresponding derivatives

\[
 D_{\mathcal R}(\mathbf E_N\circ Z)
 =\mathbf E'_{N,*}D_{\mathcal R}Z,
 \qquad
 D_{\mathcal R}^2(\mathbf E_N\circ Z)
 =\mathbf E'_{N,*}D_{\mathcal R}^2Z
  +\mathbf E''_{N,*}[D_{\mathcal R}Z,D_{\mathcal R}Z]
 \tag{2.18a}
\]

in \(\mathcal A_N^1\) and \(\mathcal A_N^0\), respectively.  This is a
curvewise scale statement, not \(C^2\) regularity of \(\mathbf E_N\) on
one level.

### 2.2 Delay observations

For the operator-valued measure \(\mathbb B_{N,p}\) in the graph theorem,
define the observation pointwise on the affine history space by

\[
 \mathbf O_{N,p}\Psi(u)
 =\int_{[-\Theta,0]}\mathbb B_{N,p}(d\vartheta)
                   \Psi(u)(\vartheta).
 \tag{2.19}
\]

Its derivative in a tangent-history direction
\(\psi\in\mathcal C_N^j\) satisfies, on every level,

\[
 \|D_\Psi\mathbf O_{N,p}[\psi]\|_{C_b^{r_j}(U,Y_N)}
 \le \|\mathbb B_{N,p}\|_{\rm TV}
       \|\psi\|_{\mathcal C_N^j}.
 \tag{2.20}
\]

Total variation gives the same tangent estimate for declared structural
derivatives of the measure.  It does **not**, by itself, control a structural
measure derivative applied to the unbounded affine anchor
\(\mathbf i_N\).  For global \(C_b^{r_j}\) response bounds one must also
verify

\[
 \sup_N
 \left\|
 \int_{[-\Theta,0]}
 D_{\mathcal R}^e\mathbb B_{N,p}(d\vartheta)
 [R_1,\ldots,R_e]\,\mathbf i_N(\,\cdot\,)(\vartheta)
 \right\|_{C_b^{r_j}(U,Y_N)}
 \le B_{\rm anch}\prod_{m=1}^e\|R_m\|,
 \quad e=1,2,
 \tag{2.21}
\]

or prove the corresponding bound directly after the transformed
nonlinearity is composed with the observation.  Balanced delay
perturbations that annihilate constant critical histories satisfy (2.21)
with \(B_{\rm anch}=0\).  On a bounded physical tube, one may instead track
the tube radius explicitly.  A moving atom is not differentiated by
(2.20); it requires a strong time-history scale and lies outside this
fixed-support theorem.

## 3. Scale derivatives of the special-flow transform

Fix \(\rho,\nu\), and a reference structural parameter, and abbreviate the
special-flow transform by

\[
 \mathcal T_N(Z,\mathcal R)
 =\bigl(\mathcal T_{Q,N},\mathcal T_{H,N}\bigr)(Z,\mathcal R).
 \tag{3.1}
\]

Let \(Z_*\in\mathcal X_N^2\) be its fixed point at
\(\mathcal R=0\).  We use the following precise meaning of a scale
derivative.

* The linear Gate derivative
  \(K_N^j:\mathcal X_N^j\to\mathcal X_N^j\), \(j=0,1\), is obtained
  by differentiating (3.1), using (2.10)--(2.11) for every differentiated
  flow and history.
* The second graph derivative
  \(K_{ZZ,N}^{(2)}:\mathcal X_N^1\times\mathcal X_N^1
  \to\mathcal X_N^0\) is obtained from (2.13)--(2.14).
* The structural source and mixed derivatives are

\[
 \begin{aligned}
 t_{R,N}&:\mathfrak R\longrightarrow\mathcal X_N^1,\\
 t_{RR,N}&:\mathfrak R^2\longrightarrow\mathcal X_N^0,\\
 K_{ZR,N}^{(2)}
 &:\mathcal X_N^1\times\mathfrak R
   \longrightarrow\mathcal X_N^0.
 \end{aligned}
 \tag{3.2}
\]

They are defined by the same differentiated formulas, including derivatives
of \(F_N,G_N\), and \(\mathbb B_{N,\nu,\mathcal R}\).  On smooth affine
curves they agree with ordinary directional derivatives.  Equations
(2.10)--(2.14) define them on the full displayed response fibers, so their
definition does not rely on density of \(C_b^9\) in \(C_b^8\) or
\(C_b^7\).

### Lemma 3.1 (uniform linear and quadratic Gate derivatives)

Under the hypotheses of the dimension-uniform special-flow theorem, together
with the anchor compatibility (2.21) or a directly verified transformed-data
substitute, after decreasing \(\rho_0\) there are constants \(C_T>0\) and
\(0<\kappa<1\), independent of \(N\), such that for
\(|\rho|\le\rho_0\),

\[
 \|K_N^j\|\le\kappa,
 \qquad j=0,1,
 \tag{3.3}
\]

and

\[
 \begin{aligned}
 \|K_{ZZ,N}^{(2)}[V,\widetilde V]\|_{\mathcal X_N^0}
 &\le C_T|\rho|\|V\|_{\mathcal X_N^1}
                    \|\widetilde V\|_{\mathcal X_N^1},\\
 \|t_{R,N}[R]\|_{\mathcal X_N^1}
 &\le C_T|\rho|\|R\|_{\mathfrak R},\\
 \|t_{RR,N}[R_1,R_2]\|_{\mathcal X_N^0}
 &\le C_T|\rho|\|R_1\|_{\mathfrak R}\|R_2\|_{\mathfrak R},\\
 \|K_{ZR,N}^{(2)}[V,R]\|_{\mathcal X_N^0}
 &\le C_T|\rho|\|V\|_{\mathcal X_N^1}\|R\|_{\mathfrak R}.
 \end{aligned}
 \tag{3.4}
\]

The restrictions commute with the linearizations:

\[
 \jmath_{10,N}K_N^1=K_N^0\jmath_{10,N}.
 \tag{3.5}
\]

**Proof.**  Differentiate the two formulas defining the special-flow
transform.  Every differentiated critical component retains its displayed
factor \(\rho\), and every differentiated stable component retains the
factor \(\rho\) in front of its semigroup integral.  State derivatives of
the finite-time histories are controlled by Lemma 2.1 and (2.20).  In the
stable integral, a variation of \(\Phi_Q^{-\rho r}\) contributes a
polynomial in \(r\) and the factor \(e^{\Gamma|\rho|r}\).  The semigroup
contributes \(Me^{-\beta r}\).  Choosing
\(\Gamma\rho_0<\beta/2\) leaves an integrable majorant

\[
 C(1+r^m)e^{-\beta r/2}.
 \tag{3.6}
\]

The \(C_b^{12}\) data bound, the operator-TV tangent bounds, and (2.21)
control all remaining terms.  For a first variation, derivatives through
order eight use the
corresponding eight derivatives of the variation and the ninth derivative
of the base graph.  A second variation through order seven uses the eighth
derivatives of its two arguments, as (2.13)--(2.14) display.  This proves
(3.3)--(3.4).  The differentiated formulas give (3.5).
\(\square\)

Lemma 3.1 is a linear-and-bilinear statement on a scale.  It is not the
claim that \(\mathcal T_N\) is a \(C^2\) self-map of
\(\mathcal X_N^0\), \(\mathcal X_N^1\), or \(\mathcal X_N^2\).

## 4. First and second graph responses

Define the compatible residual linearizations

\[
 L_N^j=I-K_N^j:
 \mathcal X_N^j\longrightarrow\mathcal X_N^j,
 \qquad j=0,1.
 \tag{4.1}
\]

By (3.3),

\[
 (L_N^j)^{-1}=\sum_{m=0}^{\infty}(K_N^j)^m,
 \qquad
 \|(L_N^j)^{-1}\|\le K_L:=\frac1{1-\kappa}.
 \tag{4.2}
\]

The inverses are compatible with restriction:

\[
 \jmath_{10,N}(L_N^1)^{-1}
 =(L_N^0)^{-1}\jmath_{10,N}.
 \tag{4.3}
\]

### Theorem 4.1 (dimension-uniform scale response)

Let \(Z_N(\mathcal R)\) be the fixed-point branch constructed by the
triangular Picard-jet theorem.  For \(R_i\in\mathfrak R\), put

\[
 z_i=D_{\mathcal R}Z_N(0)[R_i]\in\mathcal X_N^1.
 \tag{4.4}
\]

Then \(z_i\) is the unique solution of

\[
 \boxed{L_N^1z_i=t_{R,N}[R_i].}
 \tag{4.5}
\]

The second structural response

\[
 z_{12}=D_{\mathcal R}^2Z_N(0)[R_1,R_2]
 \in\mathcal X_N^0
 \tag{4.6}
\]

is the unique solution of

\[
 \boxed{L_N^0z_{12}=b_{12,N},}
 \tag{4.7}
\]

where

\[
 \begin{aligned}
 b_{12,N}={}&t_{RR,N}[R_1,R_2]
 +K_{ZR,N}^{(2)}[z_1,R_2]
 +K_{ZR,N}^{(2)}[z_2,R_1]\\
 &+K_{ZZ,N}^{(2)}[z_1,z_2].
 \end{aligned}
 \tag{4.8}
\]

For unit structural directions,

\[
 \|z_i\|_{\mathcal X_N^1}\le K_LC_T|\rho|,
 \tag{4.9}
\]

and

\[
 \|z_{12}\|_{\mathcal X_N^0}
 \le K_LC_T|\rho|
 \left(1+2K_LC_T|\rho|+(K_LC_T|\rho|)^2\right).
 \tag{4.10}
\]

All constants are independent of \(N\).

**Proof.**  Differentiate

\[
 Z_N(\mathcal R)
 =\mathcal T_N(Z_N(\mathcal R),\mathcal R)
 \tag{4.11}
\]

once in the triangular common fibers.  This gives (4.5).  Differentiate
the same identity in two structural directions and collect the second
response on the left.  The remaining four terms are exactly (4.8).
The graph theorem has already established that these are genuine Frechet
responses in \(C_b^8\) and \(C_b^7\).  Equations (4.2) and (3.4) give
(4.9)--(4.10).  \(\square\)

Thus these response equations do not merely define formal jets: their
solutions equal the Frechet tensors constructed by the Picard-jet proof.

### 4.1 Levelwise Schur equivalence

Split \(L_N^j\) according to (2.2):

\[
 L_N^j=
 \begin{pmatrix}
 \mathsf A_N^j&\mathsf B_N^j\\
 \mathsf C_N^j&\mathsf D_N^j
 \end{pmatrix}.
 \tag{4.12}
\]

Here, for example,
\(\mathsf B_N^j:\mathcal X_{\perp,N}^j\to\mathcal X_c^j\).
Because \(L_N^j=I-K_N^j\),

\[
 \|(\mathsf D_N^j)^{-1}\|\le K_L.
 \tag{4.13}
\]

Define

\[
 \mathsf S_N^j
 =\mathsf A_N^j
  -\mathsf B_N^j(\mathsf D_N^j)^{-1}\mathsf C_N^j.
 \tag{4.14}
\]

It is an isomorphism and

\[
 (\mathsf S_N^j)^{-1}
 =\pi_c(L_N^j)^{-1}\iota_c,
 \qquad
 \|(\mathsf S_N^j)^{-1}\|\le K_L,
 \tag{4.15}
\]

where \(\iota_cf=(f,0)\) and \(\pi_c(q,h)=q\).  Thus no separate
Schur-invertibility hypothesis is needed for the special-flow contraction.

For any \(b=(b_c,b_\perp)\in\mathcal X_N^j\), the solution of
\(L_N^j(q,h)=b\) is exactly

\[
 \boxed{
 \begin{aligned}
 q&=(\mathsf S_N^j)^{-1}
    \left(b_c-\mathsf B_N^j(\mathsf D_N^j)^{-1}b_\perp\right),\\
 h&=(\mathsf D_N^j)^{-1}
    \left(b_\perp-\mathsf C_N^jq\right).
 \end{aligned}}
 \tag{4.16}
\]

Apply (4.16) with \(j=1\) and \(b=t_{R,N}[R]\) for the first response,
and with \(j=0\) and \(b=b_{12,N}\) for the second response.  In the
second case, writing \(b_{12,N}=(b_{12,c},b_{12,\perp})\), this is

\[
 \begin{aligned}
 D_{\mathcal R}^2Q_N[R_1,R_2]
 &=(\mathsf S_N^0)^{-1}
 \left(
 b_{12,c}
 -\mathsf B_N^0(\mathsf D_N^0)^{-1}b_{12,\perp}
 \right),\\
 D_{\mathcal R}^2H_N[R_1,R_2]
 &=(\mathsf D_N^0)^{-1}
 \left(
 b_{12,\perp}
 -\mathsf C_N^0D_{\mathcal R}^2Q_N[R_1,R_2]
 \right).
 \end{aligned}
 \tag{4.16a}
\]

For the first response, use the
residual convention

\[
 \mathbf G_N(Z,\mathcal R)=Z-\mathcal T_N(Z,\mathcal R),
 \qquad
 g_R=D_{\mathcal R}\mathbf G_N=-t_{R,N},
 \tag{4.17}
\]

the first line of (4.16) becomes

\[
 D_{\mathcal R}Q_N[R]
 =-(\mathsf S_N^1)^{-1}g_c[R]
 +(\mathsf S_N^1)^{-1}\mathsf B_N^1
  (\mathsf D_N^1)^{-1}g_\perp[R].
 \tag{4.18}
\]

This is the exact Gate C Schur formula on a declared response fiber.
Compatibility (4.3) shows that restricting a middle-level response to the
lower level gives the same response as solving there.

## 5. Selected traces and endpoint gaps on the same scale

The graph theorem does not choose attracting and repelling outer traces.
This section states exactly what a trace construction must provide before
its gap can be attached to (4.18).

### 5.1 A declared trace scale

For each \(N\), let

\[
 \mathcal W_N^2\hookrightarrow\mathcal W_N^1
 \hookrightarrow\mathcal W_N^0,
 \qquad
 \mathcal V_N^2\hookrightarrow\mathcal V_N^1
 \hookrightarrow\mathcal V_N^0
 \tag{5.1}
\]

be Banach scales with inclusion norms at most one.
\(\mathcal W_N^j\) contains the selected one-sided trace variables,
including every phase, moving-time, or boundary coordinate retained by the
construction; \(\mathcal V_N^j\) is its residual space.  On the smooth core,
let

\[
 \mathbf T_N:
 \mathcal W_N^2\times\mathfrak A_N^2\times\mathfrak R
 \longrightarrow\mathcal V_N^2,
 \qquad
 \mathbf T_N(W_*;A_*,0)=0,
 \tag{5.2}
\]

where \(A_*=\mathbf E_N(Z_*)\).

The phrase **admissible scale trace problem** means the following.

1. Its linear Gate derivatives extend compatibly to

\[
 \begin{aligned}
 T_{W,N}^j&:\mathcal W_N^j\longrightarrow\mathcal V_N^j,\\
 T_{A,N}^j&:\mathcal A_N^j\longrightarrow\mathcal V_N^j,
 \qquad j=0,1,
 \end{aligned}
 \tag{5.3}
\]

and \(T_{W,N}^j\) is an isomorphism with

\[
 \|(T_{W,N}^j)^{-1}\|\le K_{\rm tr},
 \qquad j=0,1,
 \tag{5.4}
\]

uniformly in \(N\).

2. The structural source is the bounded map

\[
 T_{R,N}=D_{\mathcal R}\mathbf T_N(W_*;A_*,0):
 \mathfrak R\longrightarrow\mathcal V_N^1.
 \tag{5.4a}
\]

The second Gate derivative extends to a bounded bilinear map

\[
 T_N^{(2)}:
 (\mathcal A_N^1\times\mathcal W_N^1\times\mathfrak R)^2
 \longrightarrow\mathcal V_N^0,
 \tag{5.5}
\]

with uniform bounds.  This single form includes
\(AA,AW,WW,AR,WR,RR\) terms.

3. The declared construction gives a local solution operator
   \(W_N=W_N(A,\mathcal R)\) satisfying
   \(\mathbf T_N(W_N(A,\mathcal R);A,\mathcal R)=0\).  It is unique in its
   trace neighborhood, and its first- and second-order difference quotients
   obey the Taylor remainders associated with (5.3)--(5.5), with the first
   responses in \(\mathcal W_N^1\) and second responses in
   \(\mathcal W_N^0\).  Equivalently, these properties may be established
   by a triangular trace contraction.  Invertibility of \(T_{W,N}^j\)
   alone is not used as a same-space \(C^2\) implicit-function theorem.

A fixed-interval RFDE realization makes the endpoint maps concrete.  If
\(J_\sigma\) is a one-sided interval and
\(J_\sigma^\Theta=J_\sigma+[-\Theta,0]\), a trace
\(x^\sigma:J_\sigma^\Theta\to X_N\) has window

\[
 (\operatorname{Win}_\sigma x^\sigma)(s)(\vartheta)
 =x^\sigma(s+\vartheta).
 \tag{5.6}
\]

For a positive weight \(\omega_\sigma\), use

\[
 \|x\|_{C_\omega^k}
 =\max_{0\le a\le k}
  \sup_{s\in J_\sigma^\Theta}
  \omega_\sigma(s)\|x^{(a)}(s)\|_{X_N}.
 \tag{5.7}
\]

If

\[
 C_{\omega,\Theta}
 =\sup_{s\in J_\sigma,\,\vartheta\in[-\Theta,0]}
   \frac{\omega_\sigma(s)}
        {\omega_\sigma(s+\vartheta)}<\infty,
 \tag{5.8}
\]

then

\[
 \operatorname{Win}_\sigma:
 C_\omega^k(J_\sigma^\Theta;X_N)
 \longrightarrow
 C_\omega^k(J_\sigma;C([-\Theta,0],X_N))
 \tag{5.9}
\]

has norm at most \(C_{\omega,\Theta}\), independently of \(N\).  At an
endpoint \(s_\sigma\), the complete-history endpoint map is

\[
 \operatorname{End}_{\sigma,s_\sigma}x
 =x_{s_\sigma}\in C([-\Theta,0],X_N),
 \tag{5.10}
\]

with

\[
 \|\operatorname{End}_{\sigma,s_\sigma}\|
 \le\sup_{\vartheta\in[-\Theta,0]}
       \omega_\sigma(s_\sigma+\vartheta)^{-1}.
 \tag{5.11}
\]

Equations (5.6)--(5.11) show exactly which endpoint factor can grow on a
logarithmic tube.  Matching only \(x(s_\sigma)\) replaces (5.10) by current
evaluation and is not a complete-history match.

### 5.2 Trace and endpoint responses

Let

\[
 \mathbf A_N(\mathcal R)=\mathbf E_N(Z_N(\mathcal R)),
 \qquad
 W_N(\mathcal R)=W_N(\mathbf A_N(\mathcal R),\mathcal R).
 \tag{5.12}
\]

For structural directions \(R_i\), define

\[
 \begin{aligned}
 a_i&=\mathbf E'_{N,*}z_i\in\mathcal A_N^1,\\
 a_{12}&=\mathbf E'_{N,*}z_{12}
          +\mathbf E''_{N,*}[z_1,z_2]
          \in\mathcal A_N^0.
 \end{aligned}
 \tag{5.13}
\]

The trace responses are

\[
 \boxed{
 w_i=-(T_{W,N}^1)^{-1}
 \left(T_{A,N}^1a_i+T_{R,N}[R_i]\right),}
 \tag{5.14}
\]

and

\[
 \boxed{
 w_{12}=-(T_{W,N}^0)^{-1}
 \left(
 T_{A,N}^0a_{12}
 +T_N^{(2)}
 [(a_1,w_1,R_1),(a_2,w_2,R_2)]
 \right).}
 \tag{5.15}
\]

These formulas follow by subtracting and differentiating the trace equation
on levels one and zero.  The scale Taylor remainders in item 3 identify the
solutions of (5.14)--(5.15) with the actual Frechet responses of the trace
branch.

To retain endpoint terms explicitly, let \(\mathcal Z_{\sigma,N}\) be
endpoint spaces and suppose

\[
 e_{\sigma,N}:
 \mathfrak A_N^2\times\mathcal W_N^2\times\mathfrak R
 \longrightarrow\mathcal Z_{\sigma,N},
 \qquad \sigma\in\{a,r\},
 \tag{5.16}
\]

are the selected endpoint maps.  Their first Gate derivatives must extend
to

\[
 e'_{\sigma,N}:
 \mathcal A_N^0\times\mathcal W_N^0\times\mathfrak R
 \longrightarrow\mathcal Z_{\sigma,N},
 \tag{5.17}
\]

and their second Gate derivatives to

\[
 e''_{\sigma,N}:
 (\mathcal A_N^1\times\mathcal W_N^1\times\mathfrak R)^2
 \longrightarrow\mathcal Z_{\sigma,N},
 \tag{5.18}
\]

with uniform operator bounds and the corresponding first- and second-order
scale Taylor remainders.  Fixed-time complete-history evaluation is (5.10).
A moving hitting time contributes the usual time derivative and is covered
only after transversal crossing and the corresponding strong trace bounds
have been proved.

Let

\[
 j_N:
 \mathcal Z_{a,N}\times\mathcal Z_{r,N}\times\mathfrak R
 \longrightarrow\mathbb R
 \tag{5.19}
\]

be the phase-normal scalar matcher, with uniform first and second derivative
bounds.  Define

\[
 \begin{aligned}
 d_N(\mathcal R)
 =j_N\bigl(
 &e_{a,N}(\mathbf A_N(\mathcal R),W_N(\mathcal R),\mathcal R),\\
 &e_{r,N}(\mathbf A_N(\mathcal R),W_N(\mathcal R),\mathcal R),
 \mathcal R\bigr).
 \end{aligned}
 \tag{5.20}
\]

If

\[
 \mathcal J_N(A,W,\mathcal R)
 =j_N\bigl(e_{a,N}(A,W,\mathcal R),
           e_{r,N}(A,W,\mathcal R),\mathcal R\bigr),
 \tag{5.21}
\]

then the ordinary chain rule gives

\[
 \boxed{
 D_{\mathcal R}d_N[R_i]
 =J_Aa_i+J_Ww_i+J_R[R_i],}
 \tag{5.22}
\]

and

\[
 \boxed{
 \begin{aligned}
 D_{\mathcal R}^2d_N[R_1,R_2]
 ={}&J_Aa_{12}+J_Ww_{12}\\
 &+D^2\mathcal J_N
 [(a_1,w_1,R_1),(a_2,w_2,R_2)].
 \end{aligned}}
 \tag{5.23}
\]

All quantities are evaluated at the reference point.  The derivatives
\(J_A,J_W,J_R,D^2\mathcal J_N\) contain the derivatives of both endpoint
maps in (5.16).  Thus a moving section, phase normalization, or complete
history endpoint is present in (5.22)--(5.23); it can disappear only after
a separate calculation proves its contribution zero.

### Theorem 5.1 (uniform graph--trace--gap transfer)

Suppose the special-flow hypotheses, the admissible scale trace hypotheses,
and the endpoint bounds (5.17)--(5.19) hold with constants independent of
\(N\).  Then \(D_{\mathcal R}d_N\) and
\(D_{\mathcal R}^2d_N\) exist as bounded Frechet tensors with uniform
operator norms.

For an explicit bound, take unit structural directions and define

\[
 \begin{aligned}
 Z_1&=K_LC_T|\rho|,\\
 Z_2&=K_LC_T|\rho|(1+2Z_1+Z_1^2),\\
 A_1&=C_{E,1}Z_1,\\
 A_2&=C_{E,1}Z_2+C_{E,2}Z_1^2.
 \end{aligned}
 \tag{5.24}
\]

If \(\|T_A^j\|\le C_{TA}\), \(\|T_R\|\le C_{TR}\), and
\(\|T^{(2)}\|\le C_{T2}\), then

\[
 \begin{aligned}
 W_1&=K_{\rm tr}(C_{TA}A_1+C_{TR}),\\
 W_2&=K_{\rm tr}
       \bigl(C_{TA}A_2+C_{T2}(A_1+W_1+1)^2\bigr)
 \end{aligned}
 \tag{5.25}
\]

bound the trace responses.  If
\(\|D\mathcal J_N\|\le J_1\) and
\(\|D^2\mathcal J_N\|\le J_2\), then

\[
 \begin{aligned}
 \|D_{\mathcal R}d_N\|
 &\le J_1(A_1+W_1+1),\\
 \|D_{\mathcal R}^2d_N\|
 &\le J_1(A_2+W_2)
       +J_2(A_1+W_1+1)^2.
 \end{aligned}
 \tag{5.26}
\]

**Proof.**  The graph bounds are Theorem 4.1.  Lemma 2.1 gives (5.24).
Apply (5.4) to (5.14)--(5.15), then apply (5.22)--(5.23).
\(\square\)

### 5.3 Exact equivalence with the Gate C Schur formula

Eliminate the trace variable only after (5.14) has been retained.  The
derivatives of the reduced pre-graph gap

\[
 \mathscr D_N(Z,\mathcal R)
 =\mathcal J_N\bigl(
   \mathbf E_N(Z),
   W_N(\mathbf E_N(Z),\mathcal R),
   \mathcal R\bigr)
 \tag{5.27}
\]

are

\[
 \begin{aligned}
 D_Z\mathscr D_N
 &=\left(
 J_A-J_W(T_{W,N}^1)^{-1}T_{A,N}^1
 \right)\mathbf E'_{N,*},\\
 D_{\mathcal R}\mathscr D_N[R]
 &=J_R[R]-J_W(T_{W,N}^1)^{-1}T_{R,N}[R].
 \end{aligned}
 \tag{5.28}
\]

Split the first covector and name the explicit part:

\[
 D_Z\mathscr D_N=(m_c,m_\perp),
 \qquad
 \beta[R]=D_{\mathcal R}\mathscr D_N[R].
 \tag{5.29}
\]

Use the level-one blocks in (4.12)--(4.14), set

\[
 \widehat m
 =m_c-m_\perp(\mathsf D_N^1)^{-1}\mathsf C_N^1,
 \tag{5.30}
\]

and use the residual forcing
\(g_R=(g_c,g_\perp)=-t_{R,N}\).  Substitution of (4.18) and its
transverse companion into (5.22) gives

\[
 \boxed{
 \begin{aligned}
 D_{\mathcal R}d_N[R]
 ={}&\beta[R]
 -\widehat m(\mathsf S_N^1)^{-1}g_c[R]\\
 &+\left(
 \widehat m(\mathsf S_N^1)^{-1}\mathsf B_N^1-m_\perp
 \right)
 (\mathsf D_N^1)^{-1}g_\perp[R].
 \end{aligned}}
 \tag{5.31}
\]

This is exactly the Gate C formula.  Equation (5.28) identifies its
previously abstract terms:

* \(\beta\) contains explicit structural, trace, phase, and endpoint
  response;
* \(m_\perp\) contains direct observation of the transverse
  complete-history graph;
* the term with
  \(\mathsf B_N^1(\mathsf D_N^1)^{-1}\) is the nonlinear transverse return
  through the graph equation.

No same-space nonlinear implicit-function theorem occurs in this
derivation.  The only inverses used are bounded linear inverses on their
declared levels.

## 6. What is proved and what remains model-specific

The following statements are proved here under the abstract normal-form
hypotheses already proved for the special-flow graph.

1. The history extension and present-state restriction are bounded uniformly
   in \(N\), satisfy (2.9) and (2.18), and retain the full delay history.
2. The special-flow linearization is bounded and invertible on both response
   levels, while its quadratic Gate derivative loses exactly one declared
   derivative.
3. First and second structural responses are the unique solutions of
   (4.5) and (4.7), with dimension-uniform bounds.
4. Both response equations have the exact levelwise Schur form (4.16).
5. Any admissible scale trace problem transfers those responses to its
   complete-history endpoint gap by (5.14)--(5.23), and its first gap
   derivative is exactly (5.31).

The exact finite-dimensional regression in
[the scale-response test](../tests/test_banach_scale_history_schur_link.py)
checks the signs and factor-of-two conventions in the first and second graph
equations, the Schur solve, trace elimination, two endpoint maps, and the
scalar matcher.  It is an algebraic regression, not evidence for the RFDE
hypotheses or dimension-uniform estimates.

The following are not proved by this linkage theorem.

1. **Node-network fitting.**  The lifted network must still be transformed
   into the prepared normal form with the uniform projection, semigroup,
   operator-TV, affine-anchor compatibility (2.21), and \(C^{12}\) bounds
   required by the graph theorem and Lemma 3.1.
2. **Selected trace construction.**  Paper II must choose the concrete
   weighted spaces in (5.1), prove the trace contraction or scale Taylor
   remainders, and bound \((T_{W,N}^j)^{-1}\) uniformly.  A full RFDE Lin
   BVP is an alternative construction, not a consequence of this note.
3. **Moving delays and moving hits.**  Moving point masses need strong
   history translation estimates.  Moving endpoint times need transversal
   hitting and the bounds in (5.17)--(5.18).
4. **Outer selection.**  The local invariant graph does not show that the
   chosen attracting and repelling outer slow histories lie on its retained
   physical flow hull.
5. **Root regularity.**  Applying a quadratic root lemma in
   \((\nu,\mathcal R)\) additionally requires the missing
   \(\nu\nu\) and mixed trace/gap bounds and a uniform lower bound for
   \(|\partial_\nu d_N|\).  The graph theorem supplies only the parameter
   derivatives it explicitly states.
6. **Cubic asymptotics.**  The complete \(\delta^2\) cancellation, the
   \(\delta^3\) coefficient including endpoint terms, its adjoint/Green
   representation, and a nonzero admissible witness remain conditional.
7. **Pulse control.**  No global return, spike separator, pulse-onset event,
   frequency, amplitude, or control-rank theorem follows from this local
   response link.

In particular, (5.31) proves that the graph response and a correctly
constructed complete-history gap can be placed on compatible Banach levels.
It does not prove that a proposed biological network supplies the trace
package or has a nonzero Schur--Melnikov coefficient.

## 7. Acceptance checks for the linkage gate

The Gate A--to--Gate C link may be invoked for a concrete network only after
the following checks are recorded.

- [x] The graph response levels are
      \(C_b^9\supset C_b^8\supset C_b^7\), with no smoothing inverse.
- [x] The history extension and present-state restriction are (2.7)--(2.9).
- [x] The linear and quadratic Gate derivatives have the domains and ranges
      in (3.2), and their constants are independent of \(N\).
- [x] The first and second graph responses solve (4.5) and (4.7).
- [x] The Schur blocks act on the declared level-one or level-zero spaces.
- [ ] The concrete structural delay family satisfies the affine-anchor
      condition (2.21), or its transformed nonlinearity has the stated
      direct substitute.
- [ ] The concrete trace spaces, weights, restrictions, and endpoint window
      maps satisfy (5.1)--(5.18) uniformly for the chosen node network.
- [ ] The selected trace residual has the uniform inverse (5.4) and the
      scale Taylor remainders in item 3 of Section 5.1.
- [ ] The complete-history scalar matcher, its simple-root slope, and all
      endpoint derivatives have the required uniform bounds.
- [ ] The model-specific asymptotic coefficient and a nonzero witness have
      been computed.

The five checked items are abstractly closed by this note.  The unchecked
items are the remaining model and trace gates; they must not be reported as
completed from the Schur algebra alone.
