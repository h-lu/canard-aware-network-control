# Full-network augmented Lin operator for the dual-state scaffold

Status: **secondary proof-oriented specification.** The active Paper II
one-critical-mode route uses the dimension-uniform invariant-history graph in
[general-network-canard-pulse-control-program.md](general-network-canard-pulse-control-program.md).
The full Lin--Fredholm route here is retained for multiple center directions
or networks without a normally slaved transverse graph. Its strict reference
direct sum cannot by itself generate a first-order transverse return; that
return is the graph Schur-complement term in the active program. The
current-state projector
decomposition and singular center count below are exact algebraic facts. The
full RFDE operator decomposition remains conditional on compatible endpoint,
phase, and jump maps. The RFDE center/solution
manifold, compatible endpoint bundles, block Fredholm properties, uniform
inverse bound, simple root, and every threshold expansion remain theorem
targets.

## 1. Frozen model and honest name

Let \(C_1,C_2\) have sizes \(n_1,n_2\), let \(N=n_1+n_2\), and define

\[
 \ell_N^\top x
 =\frac{1}{2n_1}\sum_{j\in C_1}x_j
 +\frac{1}{2n_2}\sum_{j\in C_2}x_j,
 \qquad
 P=\mathbf1_N\ell_N^\top .
 \tag{1}
\]

Then \(P^2=P\) and \(P\mathbf1_N=\mathbf1_N\). The proof-oriented full
network is

\[
\begin{aligned}
 \dot v_i={}&v_i-\frac{v_i^3}{3}-w_i
 +D_v\sum_jP_{ij}(v_j-v_i)\\
 &+\varepsilon\sum_jP_{ij}
 \left\{
 \kappa_1[v_j(t-\tau_{ij})-v_i]
 +\kappa_3[(v_j(t-\tau_{ij})-1)^3-(v_i-1)^3]
 \right\},\\
 \dot w_i={}&\varepsilon(v_i-a)
 +D_w\sum_jP_{ij}(w_j-w_i),
\end{aligned}
\tag{2}
\]

where

\[
 D_v\in[D_v^-,D_v^+],\qquad
 D_w\in[D_w^-,D_w^+],\qquad
 D_v^-,D_w^->0,
 \tag{3}
\]

and the frozen symmetric within/cross delay pattern is

\[
 \Theta_{ab}(s)=
 \begin{cases}
  \Theta_0^0+s,&a=b,\\
  \Theta_1^0+s,&a\ne b,
 \end{cases}
 \qquad
 \tau_{ij}=\Theta_{ab}(s)/\sqrt\varepsilon,
 \qquad i\in C_a,\quad j\in C_b,
 \qquad 0<\Theta_{ab}(s)\leq\Theta_{\max}.
 \tag{4}
\]

The two terms involving \(D_v\) and \(D_w\) are fixed instantaneous
synchronization scaffolds. They are neither actuators nor weak delayed
couplings. Both vanish on a completely synchronous history, so the scalar
synchronous RFDE and its formal delay-moment calibration are unchanged.

Off synchrony, however, (2) is not the original \(N\)-slow FHN network:
only the collective recovery coordinate remains slow, while transverse
recovery differences relax on an \(O(1)\) physical time scale. The model must
therefore be called a **dual-state (voltage--recovery) instantaneously
scaffolded FHN network**. The claim that the extra scaffold is harmless is
limited to the selected synchronous history, not the surrounding network
dynamics.

## 2. Exact algebraic splitting

Set

\[
 E_c=\operatorname{span}\{\mathbf1_N\},\qquad
 E_m=\operatorname{span}\{\chi\},\qquad
 \chi=\mathbf1_{C_1}-\mathbf1_{C_2},
 \tag{5}
\]

and

\[
 E_{w,a}
 =\left\{x\in\mathbb R^N:
 \operatorname{supp}x\subset C_a,\qquad
 \sum_{i\in C_a}x_i=0\right\},
 \qquad a=1,2.
 \tag{6}
\]

Then

\[
 \mathbb R^N
 =E_c\oplus E_m\oplus E_{w,1}\oplus E_{w,2},
 \qquad
 \dim E_{w,a}=n_a-1.
 \tag{7}
\]

The operator \(P-I\) is zero on \(E_c\) and equals \(-I\) on every other
summand.

### Lemma 2.1 -- center dimension of the repaired model

At the synchronous right fold and \(\varepsilon=0\), the current-state
Jacobian is

\[
 A_0=
 \begin{pmatrix}
 D_v(P-I)&-I\\
 0&D_w(P-I)
 \end{pmatrix}.
 \tag{8}
\]

Its collective restriction and every transverse restriction are,
respectively,

\[
 A_c=\begin{pmatrix}0&-1\\0&0\end{pmatrix},
 \qquad
 A_\perp=\begin{pmatrix}-D_v&-1\\0&-D_w\end{pmatrix}.
 \tag{9}
\]

Consequently,

\[
 \dim E^{\mathrm{gen}}_0(A_0)=2,
 \qquad
 \operatorname{spec}(A_\perp)=\{-D_v,-D_w\}.
 \tag{10}
\]

The conclusion remains valid when \(D_v=D_w\); the transverse restriction
may then be a stable Jordan block, but it has no center direction.

**Proof.** The decomposition (7) diagonalizes \(P-I\) into one zero block
and \(N-1\) copies of \(-1\). Substitution gives (9). The first matrix has one
length-two Jordan chain at zero, and every transverse eigenvalue has real part
at most \(-\min\{D_v^-,D_w^-\}<0\). \(\square\)

The symmetric identities
\(\Theta_{11}=\Theta_{22}\) and \(\Theta_{12}=\Theta_{21}\) are what make
the completely synchronous history invariant and make the reference
variational dynamics preserve (7). Arbitrary four independent values of
\(\Theta_{ab}\) would not have either consequence. Subject also to compatible
endpoint and matching maps, a full reference Lin operator can have the block
form

\[
 L_{\delta,N}^{\mathrm{ref}}
 \cong
 L_{c,\delta}
 \oplus L_{m,\delta}
 \oplus L_{w,1,\delta}^{\oplus(n_1-1)}
 \oplus L_{w,2,\delta}^{\oplus(n_2-1)}.
 \tag{11}
\]

Equation (11) is an operator identity only if the endpoint maps, phase
condition, history jump, domain, and codomain commute with the same
projections. The Jacobian calculation alone does not prove a Fredholm
decomposition.

## 3. Full-history spaces

Let \(\delta=\sqrt\varepsilon\), \(r=\Theta_{\max}\), and

\[
 H_N^0=C([-r,0],\mathbb R^{2N}),\qquad
 H_N^1=C^1([-r,0],\mathbb R^{2N}).
 \tag{12}
\]

Classical compatible histories lie on

\[
 \mathcal M_{\delta,N}
 =\{\phi\in H_N^1:
 \phi'(0)=\mathcal F_{\delta,N}(\phi;\nu,\mathcal R_N)\}.
 \tag{13}
\]

The semiflow acts on \(H_N^0\); entry and exit histories in the Lin problem
must belong to (13). A repelling history is not generated by a backward
initial-value solve on all of \(H_N^0\). It must be constructed on a
finite-dimensional backward-extendible center or center-unstable solution
manifold.

Fix \(1<p<\infty\), reference flight times \(T_-^0,T_+^0>0\), and the
extended intervals

\[
 I_-^r=[-T_-^0-r,0],\qquad
 I_+^r=[-r,T_+^0].
 \tag{14}
\]

Flight-time variation is pulled back to these fixed intervals by a declared
smooth affine trivialization. For a quadratic parameter remainder use

\[
 \mathcal W_{-,N}^{2,p}=W^{2,p}(I_-^r,\mathbb R^{2N}),\qquad
 \mathcal W_{+,N}^{2,p}=W^{2,p}(I_+^r,\mathbb R^{2N}),
 \tag{15}
\]

and use

\[
 \mathcal H_N=W^{1,p}([-r,0],\mathbb R^{2N})
 \tag{16}
\]

as the complete-history jump space. A first-order theorem may use weaker
orbit regularity, but moving point delays and a quadratic remainder require
the corresponding twice differentiable composition result.

## 4. Center geometry and endpoint dimensions

Define

\[
 \xi_c(\phi)=\ell_N^\top\pi_v\phi(0)
 \tag{17}
\]

and fix

\[
 \Sigma_{\mathrm{in}}=\{\xi_c=L\},\qquad
 \Sigma=\{\xi_c=0\},\qquad
 \Sigma_{\mathrm{out}}=\{\xi_c=-L\}.
 \tag{18}
\]

The dual scaffold is intended to support a selected two-dimensional
backward-extendible RFDE center/solution manifold
\(\mathcal C_{\delta,N}\). Its attracting and repelling slow objects are
one-dimensional curves
\(S^a_{\delta,N},S^r_{\delta,N}\subset\mathcal C_{\delta,N}\). Therefore

\[
 D^a_{\mathrm{in},N}
 =S^a_{\delta,N}\cap\Sigma_{\mathrm{in}},\qquad
 D^r_{\mathrm{out},N}
 =S^r_{\delta,N}\cap\Sigma_{\mathrm{out}}
 \tag{19}
\]

must satisfy

\[
 \boxed{
 \dim D^a_{\mathrm{in},N}
 =\dim D^r_{\mathrm{out},N}=0.
 }
 \tag{20}
\]

These are full histories, not current-state points. Under a structural
perturbation they may bend away from the synchronous subspace.

### Endpoint trace bundles are not the slow discs

Point slow-manifold slices at both ends do not automatically give an
index-zero transverse BVP. For a two-dimensional current-state transverse
block, let \(d_-\) and \(d_+\) denote the finite defect dimensions admitted by
the incoming and outgoing dichotomy/fiber trace bundles after the canonical
infinite-dimensional RFDE history directions and solution-manifold
constraints have been accounted for. The reduced current-state skeleton then
has the diagnostic trace count

\[
 \operatorname{ind}_{\rm skel}L_\perp=d_-+d_+-2.
 \tag{21}
\]

Thus a necessary reduced-skeleton design target is

\[
 \boxed{d_-+d_+=2}
 \tag{22}
\]

for every module-difference and within-module block. Independently pinning
both endpoints gives the value \(-2\) in this skeleton diagnostic.

Equation (21) is not an RFDE index formula. The actual history trace bundles
may be infinite-dimensional. The theorem must construct their Fredholm pair
or a finite-defect quotient, prove closed range and exponential dichotomies,
and only then identify the transverse RFDE index as zero. Equation (22) is a
falsifier for a proposed reduced endpoint design, not sufficient evidence for
that theorem.

The dimensions in (22) must come from complementary exponential-dichotomy
or invariant-fiber trace bundles, not from artificial recovery degrees of
freedom. The cleanest construction is:

1. reduce the local RFDE to the selected two-dimensional center/solution
   manifold;
2. formulate the scalar canard matching problem there;
3. solve the hyperbolic full-history lift with complementary dichotomy
   boundary bundles satisfying (22);
4. prove that this lift lies on the selected full slow-manifold pieces.

On a finite interval, the two endpoint bundles must be related by the
invariant-fiber holonomy of the same variational equation. They are not two
independent Dirichlet conditions.

### Admissible endpoint contract

Write the endpoint equations abstractly as

\[
 B_{-,N}((u^-)_{-T_-},\alpha_-;\nu,\mathcal R_N)=0,\qquad
 B_{+,N}((u^+)_{T_+},\alpha_+;\nu,\mathcal R_N)=0.
\tag{23}
\]

A concrete local realization chooses split Banach chart spaces
\(A_{\pm,N}\) and compatible-history embeddings

\[
 \Gamma_{\pm,N}(\,\cdot\,;\nu,\mathcal R_N):A_{\pm,N}\longrightarrow
 \mathcal M_{\delta,N}\cap\mathcal H_N,
 \qquad
 B_{\pm,N}(\phi,\alpha;\nu,\mathcal R_N)
 =\phi-\Gamma_{\pm,N}(\alpha;\nu,\mathcal R_N).
 \tag{23a}
\]

Thus each endpoint equation is equality of complete histories. The chart
spaces need not themselves be finite-dimensional: \(d_\pm\) in (21) are the
finite modal defect dimensions left after the canonical RFDE history
directions have been accounted for. An equivalent split-submersion
formulation is admissible only if it has the same linear trace quotient and
Fredholm count.

Here \(\alpha_\pm\) parameterize only the dichotomy/fiber trace bundles.
They do not parameterize new slow recovery coordinates. The maps in
(23)--(23a) are admissible only if:

1. their base histories are the two selected histories in (19);
2. every history satisfies the compatibility condition (13);
3. their history-space tangent pair is Fredholm of index zero in every
   transverse block; any proved finite-defect reduction obeys (22);
4. their tangent spaces are complementary under the transverse evolution;
5. at \(\mathcal R_N=0\), they preserve all four summands in (7);
6. their continuation under \(\mathcal R_N\neq0\) is obtained from the same
   center manifold and invariant foliation, not by resetting transverse
   coordinates to zero;
7. there are declared base and fiber coordinates such that a zero complete-
   history jump forces both endpoint fiber coordinates to vanish; conversely,
   a local intersection of the selected slow histories produces the unique
   zero-fiber matched solution.

The last requirement is a checkable zero-fiber condition, not the desired gap
equivalence restated as an assumption. A nonsingular fibered BVP is not, by
itself, a maximal-canard theorem.

### Three recovery endpoint choices

| choice | consequence | permissible interpretation |
|---|---|---|
| unconstrained ambient recovery values | endpoints need not lie on selected invariant geometry; a family or kernel may remain | not a canard threshold |
| hard conditions \(w_\perp=0\) at both ends | overconstrains the full transverse BVP or silently deletes its blocks | synchronous-subspace canard or synchronization-constrained endpoint event |
| compatible history-space Fredholm trace pair whose reduced defects satisfy (22) | supplies the hyperbolic range equations without inventing slow coordinates | selected local full-network geometric canard root, only after the zero-fiber condition and Fredholm/simple-root hypotheses are proved |

The third choice is the frozen future full-network choice. Artificially synchronized endpoints
must never be called a full-network maximal canard.

## 5. Domain, codomain, phase, and jump

Let \(A_{-,N}\) and \(A_{+,N}\) be the split trace-coordinate spaces in
(23a). Define

\[
 \mathscr X_N
 =\mathcal W_{-,N}^{2,p}\times
 \mathcal W_{+,N}^{2,p}\times
 A_{-,N}\times A_{+,N}\times\mathbb R^2,
 \tag{24}
\]

where the last two coordinates are \(T_-,T_+\). Define

\[
\begin{aligned}
 \mathscr Y_N={}&
 L^p([-T_-^0,0],\mathbb R^{2N})
 \times L^p([0,T_+^0],\mathbb R^{2N})\\
 &\times\mathcal Z_{-,N}\times\mathcal Z_{+,N}
 \times\mathbb R\times\mathcal H_N.
\end{aligned}
\tag{25}
\]

For the equality realization (23a), take
\(\mathcal Z_{-,N}=\mathcal Z_{+,N}=\mathcal H_N\). For an equivalent
split-submersion realization, \(\mathcal Z_{\pm,N}\) are the declared normal
trace spaces. Introducing a chart coordinate in \(A_{\pm,N}\) and its full
trace residual in \(\mathcal Z_{\pm,N}\) must preserve the proved history-
space Fredholm index; endpoint coordinates may not be counted twice. Equation
(21) can only audit a justified finite-defect reduction.

For

\[
 z_N=(u^-,u^+,\alpha_-,\alpha_+,T_-,T_+)
 \tag{26}
\]

set

\[
 \mathfrak F_{\delta,N}(z_N,\nu,\mathcal R_N)=
 \begin{pmatrix}
  \dot u^--\mathcal F_{\delta,N}((u^-)_s;\nu,\mathcal R_N)\\
  \dot u^+-\mathcal F_{\delta,N}((u^+)_s;\nu,\mathcal R_N)\\
  B_{-,N}((u^-)_{-T_-},\alpha_-;\nu,\mathcal R_N)\\
  B_{+,N}((u^+)_{T_+},\alpha_+;\nu,\mathcal R_N)\\
  \xi_c((u^-)_0)\\
  J_N(u^-,u^+)
 \end{pmatrix}.
 \tag{27}
\]

There is exactly one phase condition, namely
\(\xi_c((u^-)_0)=0\). No transverse mode receives a phase condition.

The jump is

\[
 \boxed{
 J_N(u^-,u^+)=(u^-)_0-(u^+)_0\in\mathcal H_N.
 }
 \tag{28}
\]

It matches all \(2N\) state histories on \([-r,0]\). Matching current states,
module averages, or recovery values alone does not splice two RFDE
solutions.

At a selected reference segment define

\[
 L_{\delta,N}
 =D_{z_N}\mathfrak F_{\delta,N}
 (z_{c,\delta,N},\nu_{c,\delta,N},0).
 \tag{29}
\]

Choose \(\psi_{\delta,N}\in\mathscr Y_N^*\) and
\(e_{\delta,N}\in\mathscr Y_N\) such that

\[
 \operatorname{Range}L_{\delta,N}=\ker\psi_{\delta,N},
 \qquad
 \psi_{\delta,N}(e_{\delta,N})=1,
 \tag{30}
\]

where \(e_{\delta,N}\) has only a collective complete-history-jump
component. The augmented operator is

\[
 \widehat L_{\delta,N}(\zeta,\gamma)
 =L_{\delta,N}\zeta-\gamma e_{\delta,N}.
 \tag{31}
\]

No module-difference or within-module jump is left unresolved.

## 6. Modal Fredholm theorem target

### Theorem 6.1 -- one-gap direct-sum criterion

Assume that:

1. the RFDE solution manifold, orbit map, and endpoint maps are \(C^2\) on
   the spaces above;
2. the center/solution manifold and endpoint bundles satisfy Section 4;
3. the collective post-phase block satisfies

   \[
   \ker L_{c,\delta}=\{0\},\qquad
   \dim\operatorname{coker}L_{c,\delta}=1,\qquad
   \operatorname{ind}L_{c,\delta}=-1;
   \tag{32}
   \]

4. every transverse history-space trace pair is Fredholm of index zero and
   the resulting block is an isomorphism; any finite-defect reduction is
   consistent with the skeleton diagnostic (22);
5. the collective range inverse and every transverse inverse admit a common
   upper bound \(G_\perp(\delta)\), uniform in block multiplicity and in the
   admitted parameter wedge.

Then the reference operator has the following index table.

| block | multiplicity | kernel | cokernel | index |
|---|---:|---:|---:|---:|
| collective \(L_{c,\delta}\) | \(1\) | \(0\) | \(1\) | \(-1\) |
| module difference \(L_{m,\delta}\) | \(1\) | \(0\) | \(0\) | \(0\) |
| within \(C_1\), \(L_{w,1,\delta}\) | \(n_1-1\) | \(0\) | \(0\) | \(0\) |
| within \(C_2\), \(L_{w,2,\delta}\) | \(n_2-1\) | \(0\) | \(0\) | \(0\) |
| full \(L_{\delta,N}\) | \(1\) | \(0\) | \(1\) | \(-1\) |
| augmented \(\widehat L_{\delta,N}\) | \(1\) | \(0\) | \(0\) | \(0\) |

In particular, \(\widehat L_{\delta,N}\) is invertible and

\[
 \left\|
 (L_{\delta,N}:\mathscr X_N\to
 \operatorname{Range}L_{\delta,N})^{-1}
 \right\|
 \leq G_\perp(\delta).
 \tag{33}
\]

**Proof architecture.** The exact reference equivariance and endpoint
compatibility give (11) simultaneously in domain and codomain. Fredholm
indices add under finite direct sums. Assumptions (32) and the transverse
isomorphisms give total index \(-1\), zero kernel, and a cokernel inherited
only from the collective block. The normalized collective jump column removes
that cokernel and raises the index to zero. Repeated within-module blocks do
not enlarge the inverse norm in a declared block-weighted product norm. Every
sentence after the first is conditional on the block hypotheses; none follows
from (9) alone.

### Lemma 6.2 -- meaning of a zero

Under Theorem 6.1, solve

\[
 \mathfrak F_{\delta,N}(z_N,\nu,\mathcal R_N)
 =d_{\delta,N}(\nu,\mathcal R_N)e_{\delta,N}.
 \tag{34}
\]

Because \(e_{\delta,N}\) has only a jump component, augmented-IFT uniqueness
gives the non-geometric equivalence

\[
 d_{\delta,N}=0
 \quad\Longleftrightarrow\quad
 J_N=0.
 \tag{35}
\]

If the zero-fiber implication in endpoint-contract item 7 is also proved,
then \(J_N=0\) forces both fiber coordinates to vanish and the common history
belongs to both selected slow pieces. Conversely, a local intersection of
those pieces supplies a zero-fiber solution and, by local uniqueness, a root
of (34). Only with this additional argument does (35) define a geometric
canard intersection.

Under this zero-fiber implication, assume additionally

\[
 |\partial_\nu d_{\delta,N}(\nu_{c,\delta,N},0)|
 \geq m_\delta^{(\nu)}>0,
 \tag{36}
\]

Then the zero is a selected local full-network geometric canard root. It is
not a global pulse threshold without a separate global-return theorem.

Lemma 6.2 does not apply to hard synchronized endpoints or to a connection
between stable fibers whose base slow-manifold histories have not been shown
to match.

## 7. What the repair achieves and what remains open

In fold time, the transverse voltage and recovery rates contain
\(-D_v/\delta\) and \(-D_w/\delta\), whereas the weak delayed terms remain
perturbative. The repair therefore replaces the \(N-1\) near-center recovery
directions by a plausible hyperbolic RFDE range problem. It is the cleanest
proof-oriented future-promotion choice among the two scaffolds considered here.

It does **not** by itself prove a one-gap theorem. The following remain open:

- construct and select the two-dimensional backward-extendible RFDE
  center/solution manifold;
- construct the slow curves and endpoint bundles satisfying all seven
  requirements in Section 4;
- prove exponential dichotomies for the module-difference and within-module
  RFDE blocks, including the case \(D_v=D_w\);
- prove that every transverse block has index zero, zero kernel, zero
  cokernel, and an \(N\)-uniform inverse bound;
- prove the collective statement (32), the simple-root bound (36), and
  \(C^2\) delay-parameter dependence;
- prove the zero-fiber implication that upgrades the automatic equivalence
  (35) from a matched fiber connection to an intersection of the selected
  slow histories;
- prove every threshold expansion, uniform remainder, control corollary, and
  local-to-global pulse statement separately.

Finite-interval singular values obtained with hard endpoint rows do not prove
these claims.

## 8. Voltage-only scaffold as a negative control

Set \(D_w=0\), retaining \(D_v>0\). At \(\varepsilon=0\), every transverse
block is

\[
 \begin{pmatrix}-D_v&-1\\0&0\end{pmatrix},
 \tag{37}
\]

and

\[
 \dim E^{\mathrm{gen}}_0=2+(N-1)=N+1.
 \tag{38}
\]

The finite-dimensional singular skeleton therefore suggests an
\(N\)-dimensional slow geometry. If corresponding RFDE attracting and
repelling slow manifolds are constructed, their scalar-section slices would
have

\[
 \dim D^a_{\mathrm{in},N}
 =\dim D^r_{\mathrm{out},N}=N-1.
 \tag{39}
\]

In that conditional geometry, each transverse mode contributes one reduced
incoming and one reduced outgoing coordinate, so the skeleton diagnostic
(21) is zero, not \(-2\). The
\(N+1\)-dimensional singular center therefore does not, by itself, rule out a
one-gap problem for fixed \(\delta>0\).

What it rules out is the inference that one fast fold automatically gives a
planar, uniformly conditioned Lin operator. At \(\delta=0\), a transverse
block may carry one kernel and one cokernel direction even though its index is
zero. If one freezes the local current-state block at the fold and suppresses
the full long-delay/nonautonomous structure, its formal slow root is

\[
 \lambda_s^{\rm frozen}
 =-\varepsilon/D_v+O(\varepsilon^{3/2}).
 \tag{40}
\]

This local scale suggests possible \(O(\delta^{-1})\) conditioning in fold
time, but neither identifies an RFDE spectral root nor proves a BVP inverse
bound; both depend on the natural endpoint bundles and the long-delay
variational operator.

If the relevant RFDE slow manifolds exist, the geometrically intrinsic
voltage-only choice is to retain their transverse recovery coordinates and
solve for them through complete matching. Unconstrained ambient recovery
values do not define those manifolds, while setting all differences to zero
defines a restricted synchronous event. This is why the voltage-only model
remains a useful negative control and a harder possible theorem, rather than a
proved impossibility.

## 9. Acceptance gates

- [ ] Prove the RFDE center/solution-manifold reduction and its \(C^2\)
  parameter dependence.
- [ ] Construct compatible history-space endpoint bundles, prove their
  tangent pairs are Fredholm of index zero, and recover (22) only in a proved
  finite-defect reduction.
- [ ] Prove the operator splitting (11), including endpoint, phase, and jump
  maps.
- [ ] Prove all transverse index-zero isomorphisms and an \(N\)-uniform
  inverse estimate.
- [ ] Prove the collective one-cokernel statement and simple root.
- [ ] Prove the zero-fiber implication that upgrades the automatic
  equivalence (35) to a full slow-manifold intersection.
- [ ] Keep synchronized endpoint events and finite-section diagnostics
  separate from the geometric root.
- [ ] Treat threshold asymptotics and the global pulse interpretation as
  additional theorems.
