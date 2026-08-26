# Stage 4W: a split-aware bimeasure residual theorem

Status: **proved analytic bridge; qualitative local Hessian only; numerical
ingress open.**

Stage 4W proves the norm and residual theorem needed to turn a future
directed signed-kernel computation into the six continuous-history Hessian
bounds. It does not supply that computation. In particular, none of the
Stage-4Q finite-section rows is used as an error bound.

There is also one qualitative advance. The Stage-4S-A/4R direct selected map,
which Stage 4T byte-binds and types before identifying its center derivative,
is $C^2$ on an open neighborhood. Consequently its Banach Hessian exists, is
continuous, and is uniformly finite on an unknown small ball having the
preferred anisotropic shape. This is not the preferred scale $\lambda=1$.
The radius and bound are not numerical, and the six strict Stage-4P caps
remain open.

The executable source is
[leaky_inner_split_bimeasure_residual_stage4w.py](../src/canard_control/leaky_inner_split_bimeasure_residual_stage4w.py),
the generator is
[leaky_inner_split_bimeasure_residual_stage4w.py](../experiments/leaky_inner_split_bimeasure_residual_stage4w.py),
and the source-bound result is
[leaky_inner_split_bimeasure_residual_stage4w.json](../experiments/results/leaky_inner_split_bimeasure_residual_stage4w.json).

## 1. What the frozen parents now prove

Stage 4W byte-binds Stages 4O, 4P, 4Q, 4S-B, and 4T.

- Stage 4O supplies the exact fixed-time second variation, implicit event,
  complete-history translation, and one-phase-projection formulas.
- Stage 4P supplies only the conditional six-block graph arithmetic and its
  wide target box.
- Stage 4Q is a signed finite-section diagnostic. All nineteen of its
  theorem flags remain false.
- Stage 4S-B proves that finite sampling cannot converge in operator norm on
  an arbitrary unit ball of $C(K)$, and it allocates strict error budgets.
- Stage 4T binds and types the Stage-4S-A/4R direct $C^2$ selected map, proves
  its exact center derivative $DQ_Y(Y_*)=A^2$, and transfers the fixed center
  splitting and rates.

Thus the analytic existence question and the numerical cap question must be
separated. The first is now closed locally; the second is not.

## 2. A qualitative complete-history Hessian

Let $Q_{\rm coord}:D\to E_s\times\mathbb R$ be the Stage-4T coordinate
return. Its initial and terminal charts are affine, and $D$ is an open
neighborhood of the origin. Since $Q_{\rm coord}$ is $C^2$,

$$
H(z)=D^2Q_{\rm coord}(z)
$$

is continuous in the bilinear operator norm at $z=0$. For balls having the
preferred anisotropic shape

$$
\mathcal B_\lambda=
\{(x_s,x_u):\|x_s\|_Y\le 0.0097\lambda,
                 |x_u|\le0.00025\lambda\},
$$

there are therefore some $\lambda_H>0$ and $K_H<\infty$ such that

$$
\mathcal B_{\lambda_H}\subset D,
\qquad
\sup_{z\in\mathcal B_{\lambda_H}}\|H(z)\|\le K_H.
$$

This uses continuity at one point. It does not use compactness of the closed
ball, which would be false in the infinite-dimensional history space.

More sharply, let $B_i(z)$, $i=1,\ldots,6$, denote the six fixed
stable/unstable input/output blocks. If rigorous center bounds satisfy

$$
\|B_i(0)\|<c_i
\quad (i=1,\ldots,6),
$$

then continuity gives a common $\lambda>0$ for which

$$
\sup_{z\in\mathcal B_\lambda}\|B_i(z)\|<c_i
\quad (i=1,\ldots,6).
$$

This is an existence theorem at an unknown small scale, not an effective
radius and not $\lambda=1$. It also gives no same-ball self-map. Stage 4Q
suggests center headroom but does not prove any one of the six center
inequalities.

### 2.1 A qualitative stable graph for the selected map

The same parent chain closes one more qualitative statement without any
Hessian number. In the pullback $J$ norm, put
$Z=Z_s\oplus Z_u=E_s\oplus\mathbb R$. Stage 4T gives

$$
L=DQ_{\rm coord}(0)=J^{-1}A^2J,
$$

with

$$
\|(L|_{Z_s})^n\|\le0.01^n,
\qquad
\|((L|_{Z_u})^{-1})^n\|
\le \rho_{u,2}^n,
\qquad
\rho_{u,2}<0.302184<1.
$$

Write $Q_{\rm coord}(z)=Lz+N(z)$. Since the map is $C^2$,
$N(0)=DN(0)=0$, so the derivative of the nonlinear remainder is arbitrarily
small after shrinking the open domain. The local stable-manifold theorem for
Banach-space maps therefore gives neighborhoods $U_s\subset Z_s$ and
$U\subset Z$ and a $C^2$ function

$$
\psi:U_s\to Z_u,
\qquad
\psi(0)=0,
\qquad
D\psi(0)=0,
$$

whose graph

$$
W_{\rm sel}^{s,\rm loc}
=\{x_s+\psi(x_s):x_s\in U_s\}
$$

is the local stable manifold of the selected coordinate map. After shrinking
$U\subset D\cap D_{\rm out}$, it characterizes the points whose selected-map
iterates remain in $U$ and converge to zero.

A global self-map of the full anisotropic ball is not required: the local
theorem uses the map only while iterates remain in the smaller open
neighborhood. This result has no effective radius, graph height, or slope. It
also does not yet identify this selected-map graph with the periodic orbit's
physical stable-set germ; that step still needs the recurrence and
phase-isolation hypotheses for all intervening flow arcs. No first-return
ordinal or pulse-sheet crossing follows.

## 3. The phase-and-stable quotient norm

Write

$$
Y=C(K,\mathbb R)\times\mathbb R,
\qquad K=[-\tau_{\max},0],
$$

with the max norm. By the Riesz representation theorem,

$$
Y^*=\mathcal M(K)\times\mathbb R,
\qquad
\|(\mu,c)\|_{Y^*}=\|\mu\|_{\rm TV}+|c|.
$$

The phase section is $\Sigma_0=\ker\ell_0$, where
$\ell_0(\phi,w)=\phi(0)$. Let
$\widehat q\in\Sigma_0$ and
$\widehat f\in\Sigma_0^*$ be the fixed pair with
$\|\widehat q\|_Y=1$ and
$\widehat f(\widehat q)=1$. Choose any Hahn--Banach extension
$\widetilde f\in Y^*$. Then

$$
E_s=\ker\ell_0\cap\ker\widetilde f,
\qquad E_u=\operatorname{span}\{\widehat q\}.
$$

For every $\mu\in Y^*$, restriction to the stable space has the exact norm

$$
\boxed{
\|\mu|_{E_s}\|
=\inf_{\alpha,\beta\in\mathbb R}
\|\mu-\alpha\ell_0-\beta\widetilde f\|_{Y^*}.}
\tag{3.1}
$$

Indeed, the restriction $Y^*\to E_s^*$ is a metric quotient by
$E_s^\perp=\operatorname{span}\{\ell_0,\widetilde f\}$; the reverse
inequality is Hahn--Banach. Formula (3.1) is independent of the chosen
extension. For the unstable coordinate,

$$
\sup_{|c|\le1}|\mu(c\widehat q)|=|\mu(\widehat q)|.
\tag{3.2}
$$

Define these two exact row costs by

$$
d_s(\mu)=\operatorname{dist}
(\mu,\operatorname{span}\{\ell_0,\widetilde f\}),
\qquad
d_u(\mu)=|\mu(\widehat q)|.
\tag{3.3}
$$

This is more faithful than first bounding an ambient row and then
multiplying by powers of $\|P_s\|$. Phase atoms and multiples of
$\widehat f$ are removed before total variation, while the unstable action
is evaluated with its sign intact.

## 4. Split projective bimeasures

Consider an absolutely summable or Bochner-integrable signed representation

$$
\mathcal B=\sum_r y_r\otimes\mu_r\otimes\nu_r,
\qquad y_r\in\Sigma_0,
\tag{4.1}
$$

where the input factors are atom--density measures, including the recovery
atom. For output type $o\in\{s,u\}$, put

$$
\omega_s(y)=\|y-\widehat q\widehat f(y)\|_Y,
\qquad
\omega_u(y)=|\widehat f(y)|.
$$

For input types $a,b\in\{s,u\}$, define the split projective cost

$$
\mathcal N_{ab}^o(\mathcal B)
=\inf_{(4.1)}\sum_r
\omega_o(y_r)d_a(\mu_r)d_b(\nu_r),
\tag{4.2}
$$

with the analogous integral for a Bochner representation. Termwise
restriction and the triangle inequality give

$$
\boxed{
\|O_o\mathcal B[I_a\,\cdot,I_b\,\cdot]\|_{\rm bil}
\le \mathcal N_{ab}^o(\mathcal B).}
\tag{4.3}
$$

The infimum is over signed representations, so correlations may be retained.
For the mixed block no factor of two is inserted unless it is actually
present in the chosen symmetric representation.

Equation (4.3) is a sufficient norm on the structured Volterra object
generated by the finite-delay RFDE. It does not assert that arbitrary nodal
data determine such an object. A future computation must construct the
representation and bound its residual in the same projective norm.

## 5. Exact event assembly on the complete history

At a base point $x$, write

$$
n=\ell_0\circ U^T,
\quad d=\dot X_T,
\quad e=\ddot X_T,
\quad a=\ell_0(d)>0.
$$

Here $U^T,\dot U^T$ are complete-history linear maps and $V^T$ is the
fixed-time second variation. Every voltage output phase is evaluated at
$T(x)+\theta$, $-\tau_{\max}\le\theta\le0$, and the recovery component is
evaluated at $T(x)$. The exact preprojection bimeasure is

$$
Z=V^T-a^{-1}
(\dot U^T\otimes n+n\otimes\dot U^T)
+a^{-2}e\otimes n\otimes n.
\tag{5.1}
$$

The selected-return Hessian is

$$
\boxed{
D^2Q_Y=H=Z-a^{-1}d\otimes(\ell_0\circ Z).}
\tag{5.2}
$$

Thus $T_h=-n(h)/a$ and
$T_{hk}=-\ell_0(Z[h,k])/a$. Expanding (5.2) produces inverse powers
through $a^{-3}$. A rigorous computation must use the same positive interval
object for $a$ and its inverse powers; separately rounded event terms destroy
the needed correlation.

The order is mandatory: complete every translated history coordinate, form
(5.1), apply the moving-event phase correction in (5.2) exactly once, and
only then apply the fixed output split. On an elementary tensor,

$$
\begin{aligned}
P_s(y\otimes\mu\otimes\nu)
 &=(y-\widehat q\widehat f(y))\otimes\mu\otimes\nu,\\
\widehat f(y\otimes\mu\otimes\nu)
 &=\widehat f(y)\,\mu\otimes\nu.
\end{aligned}
\tag{5.3}
$$

The continuous atom, density, recovery component, and tail of
$\widehat f$ act on the completed output before the stable subtraction.
A finite-grid pairing correction is not a substitute.

## 6. The six-block residual implication

For block $i$, let $C_i$ be an outward split-projective bound for the signed
center object after (5.1)--(5.3). Let $\delta_{i,r}$ be outward projected
residuals for the six frozen categories:

1. base orbit and coefficient error;
2. first-variation kernel residual;
3. second-variation bimeasure residual;
4. event quotient and history translation;
5. continuous $q/f$ action and output-phase completion;
6. full-ball inflation and return domain.

Then the proved acceptance implication is

$$
C_i+\sum_r\delta_{i,r}<\operatorname{cap}_i
\quad\text{for all six }i
\quad\Longrightarrow\quad
\sup_{z\in\mathcal B_\lambda}\|B_i(z)\|
<\operatorname{cap}_i.
\tag{6.1}
$$

The result JSON copies the exact Stage-4S-B caps, allocations, and strict
reserves. All actual $C_i$ and $\delta_{i,r}$ fields are null. The
simultaneous cancellation-blind ambient route would require a raw remainder
below approximately $7.58219\times10^{-5}$; (3.1)--(4.3) instead permit
direct blockwise residuals and avoid factors as large as $\|P_s\|^3$.

## 7. Minimally sufficient validated algorithm

A closing computation must do the following in one correlated run.

1. Partition source time and output phase at every delay activation,
   method-of-steps seam, event-window endpoint, and history endpoint.
2. Enclose the nonlinear base tube and $DF,D^2F,D^3F$ on the entire
   anisotropic ball by interval Taylor or Picard bounds.
3. Propagate current and delayed first-variation Riesz rows as signed atoms
   plus interval densities. Bound the initial trace and signed equation
   defect in total variation.
4. Assemble the $ss,su,uu$ quadratic sources before taking absolute values
   and solve the Volterra second-variation equation in projective bimeasure
   norm, with its signed defect and zero affine initial second jet.
5. Form (5.1)--(5.2) with one correlated positive event denominator.
6. Cover every output phase, both endpoints, all short cells, and all seams
   with an analytic interval remainder rather than nodal interpolation.
7. Apply the continuous $\widehat q,\widehat f$ pair and (3.1)--(3.3),
   including all atom, density, normalization, and tail errors.
8. Separate a directed center core from a uniform ball residual using the
   $D^3F$ tube and the validated first/second-kernel defects.
9. Take the six split-projective norms once and verify all inequalities
   (6.1) strictly.

The first-variation defect has the form

$$
R_U=\dot{\widetilde U}-DF(\widetilde X_t)\widetilde U,
$$

with all delayed rows and the affine initial trace included. The
second-variation defect is

$$
R_V=\dot{\widetilde V}-DF(\widetilde X_t)\widetilde V
-D^2F(\widetilde X_t)[\widetilde U,\widetilde U].
$$

Both defects must be propagated by a validated retarded resolvent in their
respective signed measure norms. Mesh convergence, binary64 rows, separate
norming of event terms, a finite $q/f$ adapter, or a center-only calculation
cannot replace these residuals.

## 8. Exact remaining gap

The bound parents fill **0 of 6** continuous-history numerical Hessian blocks
and **0 of 37** registered interval ingress fields. What is missing is one
outward atom-density/projective-bimeasure enclosure of the center $D^2Q$,
followed by its uniform residual on a numerically declared preferred-shape
ball after the exact event and $q/f$ actions.

What is no longer missing is the qualitative selected $C^2$ map, existence
and local boundedness of its Hessian, a qualitative $C^2$ stable graph for
the selected map, the center derivative and fixed split, the event-Hessian
identity, or the correct residual norm. This narrows the quantitative
obstruction to a specific validated continuous-kernel computation.

No effective stable-graph radius or slope, selected-map/periodic-orbit
stable-set identification, pulse-sheet crossing, physical onset, biological
control, routing, capture, or network-safety theorem follows from Stage 4W
alone.

## 9. Replay

Run:

    OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src \
      /usr/bin/python3 \
      experiments/leaky_inner_split_bimeasure_residual_stage4w.py
