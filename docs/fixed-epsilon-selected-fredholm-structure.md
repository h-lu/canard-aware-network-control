# The fixed-\(\varepsilon\) selected-Fredholm structure

Status: **an exact discrete endpoint-compatibility and ambient-dimension
repair, not a Fredholm inverse certificate.**  The raw two-state degree-six
multi-cell coefficient space is only \(C^0\) across cell joins and has
dimension 194.  Its discrete RFDE endpoint-compatibility equation has rank
two.  Hence the endpoint-compatible layer has dimension 192, and a
codimension-one attracting trace inside that layer has dimension 191, not
193.

The previously advertised `775 x 774` shape can still be used, but only as
an **ambient-coordinate ledger**: each of the three 194-row history
equalities must be replaced by a 192-row projected equality, and six explicit
endpoint-compatibility rows must be inserted.  This note proves that repaired
\(C^0\) ambient algebra and the projection identity.  It is not yet a
globally \(C^1\) or \(W^{2,p}\) collocation count: such a realization needs a
different basis or explicit internal derivative-jump residuals and a fresh
dimension audit.  The note also does not construct either selected endpoint
chart, assemble the resulting rectangular matrix, or validate its rank,
cokernel, border, tail, root, or response.

The implementation is
[fixed_epsilon_selected_fredholm_structure.py](../src/canard_control/fixed_epsilon_selected_fredholm_structure.py),
the deterministic generator is
[fixed_epsilon_selected_fredholm_structure.py](../experiments/fixed_epsilon_selected_fredholm_structure.py),
and the hostile tests are
[test_fixed_epsilon_selected_fredholm_structure.py](../tests/test_fixed_epsilon_selected_fredholm_structure.py).

## 1. Exact discrete compatibility chart

Let \(H_N^{C^0}\) be the two-state continuous piecewise-polynomial history
coefficient space with degree \(p=6\) on 16 cells.  Per scalar component,
use the 17 shared endpoint values and five endpoint-zero bubble coefficients
per cell.  No derivative matching at the 15 internal joins is imposed.  Thus

\[
 \dim H_N^{C^0}=2\{17+16(5)\}=194.
\tag{1.1}
\]

On the last cell \([ -\ell,0]\), put \(u=(\theta+\ell)/\ell\) and include
the basis function

\[
 b(u)=\ell u(u-1).
\tag{1.2}
\]

It satisfies

\[
 b(0)=b(1)=0,
 \qquad \partial_\theta b(1)=1.
\tag{1.3}
\]

Assume \(0<\ell<\min\{4,5,\Theta_*\}\).  A variation in (1.2) therefore
changes neither the current value nor the values at delays
\(4,5,\Theta_*\).  Let \(b_X,b_Y\) denote (1.2) in the two state
components and define

\[
 C_N(\phi)=\partial_\theta^-\phi(0)
 -f\{\phi(0),\phi(-4),\phi(-5),\phi(-\Theta_*);\nu,\eta\}.
\tag{1.4}
\]

Then, at every frozen history and parameter value,

\[
 DC_N(\phi)[b_X,b_Y]=I_2.
\tag{1.5}
\]

This is a direct proof that the **discrete endpoint map** \(DC_N\) has rank
two on the raw \(C^0\) coefficients.  It does not assert derivative
continuity at any internal cell join, and it does not depend on a
floating-point singular value or on a theorem citation.

Order the raw coefficients as \((r,\alpha_X,\alpha_Y)\), where the last two
coordinates multiply \(b_X,b_Y\), and choose the concrete projection

\[
 P_N=[I_{192}\ \ 0]\in\mathbb R^{192\times194}.
\tag{1.6}
\]

Writing the remaining columns of \(DC_N\) as \(A(\bar\phi)\), equations
(1.5)--(1.6) give

\[
 \begin{bmatrix}P_N\\DC_N(\bar\phi)\end{bmatrix}
 =
 \begin{bmatrix}I_{192}&0\\A(\bar\phi)&I_2\end{bmatrix},
 \qquad
 \det=1,
\tag{1.7}
\]

with exact inverse

\[
 \begin{bmatrix}I_{192}&0\\-A(\bar\phi)&I_2\end{bmatrix}.
\tag{1.8}
\]

Moreover, along the two bubble directions,

\[
 C_N(\phi+b_X\alpha_X+b_Y\alpha_Y)=C_N(\phi)
 +(\alpha_X,\alpha_Y)^T.
\tag{1.9}
\]

Consequently, if two histories are compatible, their full equality is
equivalent to their projected equality under \(P_N\).  Projection is not a
license to discard two equations: compatibility of both histories must come
from explicit rows, a constructed compatible chart, or a flow endpoint row.

## 2. Repaired ambient ledger

At the level of this \(C^0\) ambient algebra, a branch containing 16 history
cells and 8 flight cells has

\[
 2\{6(16+8)+1\}=290
\tag{2.1}
\]

coefficients.  Keep an ambient codimension-one entry chart
\(\Gamma_-:\mathbb R^{193}\to H_N\), but impose
\(C_N\circ\Gamma_-=0\) as two residual rows.  If

\[
 \operatorname{rank}D(C_N\circ\Gamma_-)=2,
\tag{2.2}
\]

its compatible zero fiber has dimension \(193-2=191\), the correct
codimension-one dimension inside the 192-dimensional discrete
endpoint-compatible level.
Condition (2.2) is a construction gate, not a result of this package.

Construct the one-coordinate exit chart \(\Gamma_+\) inside
\(C_N^{-1}(0)\).  Use \(p=6\) right-inclusive flow collocation equations on
each of eight flight cells, so each branch contributes \(2(6)(8)=96\)
rows and a zero flow residual enforces endpoint compatibility at its terminal
history.  These right-inclusive rows do not by themselves match derivatives
at every internal cell join.  The ambient residual blocks are then

| Block | Rows |
|---|---:|
| left and right flow | \(96+96\) |
| left initial compatibility \(C_N(h_-)\) | 2 |
| ambient entry-chart compatibility \(C_N(\Gamma_-(\xi_-))\) | 2 |
| right initial compatibility \(C_N(h_0^+)\) | 2 |
| projected entry equality \(P_N(h_--\Gamma_-(\xi_-))\) | 192 |
| projected seam equality \(P_N(h_0^--h_0^+)\) | 192 |
| projected exit equality \(P_N(h_+-\Gamma_+(\xi_+))\) | 192 |
| phase | 1 |

The entry block uses projected equality and compatibility of both sides.
The seam uses projected equality, right-initial compatibility, and terminal
compatibility propagated by the left flow.  The exit uses projected equality,
terminal compatibility propagated by the right flow, and the declared
construction hypothesis \(\Gamma_+(\xi_+)\in C_N^{-1}(0)\).  Thus the three
raw 194-row equalities have been **replaced**, not silently shortened.

The resulting counts are

\[
 \dim X_N=2(290)+193+1=774,
\tag{2.3}
\]

and

\[
 \dim Y_N=2(96)+3(192)+6+1=775.
\tag{2.4}
\]

This gives a candidate ambient algebra
\(L_N=D_z\mathfrak F_N\in\mathbb R^{775\times774}\).  It is a repaired ambient
ledger only.  Equations (2.3)--(2.4) do not show that \(L_N\) exists
for selected charts, has full column rank, or has a one-dimensional
cokernel.

For comparison, endpoint-compatible coordinates remove two initial history
variables from each branch.  They give 288 coefficients per branch, a
191-coordinate attracting chart, and a one-coordinate exit chart.  The
corresponding \(C^0\) ledger is

\[
 \dim X_N^{\rm int}=2(288)+191+1=768,
 \qquad
 \dim Y_N^{\rm int}=2(96)+3(192)+1=769.
\tag{2.5}
\]

Both ledgers have the intended formal index \(-1\).  Thus the endpoint-
compatible \(C^0\) matrix is \(769\times768\), whereas the repaired ambient
\(C^0\) matrix is \(775\times774\).  Neither is yet a \(W^{2,p}\) Fredholm
discretization.  A globally \(C^1\) basis or added derivative-jump rows can
change the raw matrix size; the analytic invariant eventually sought is the
Fredholm index, not the number 775.

## 3. Conditional raw-template derivative, cokernel, and border

Freeze \((\nu,\eta,T_*)\).  If the repaired ambient \(C^0\) template is
retained, denote its candidate rectangular derivative by

\[
 L_N=D_z\mathfrak F_N
\tag{3.1}
\]

It excludes \(\nu,\eta,T_*\), and the Lin gap \(d\).  One must separately prove
full column rank.  For a numerical matrix, a directed lower bound on
\(\sigma_{\min}(L_N)\) addresses that gate.  It does not supply the missing
left-null vector: the last vector of an economy SVD belongs to the smallest
positive singular value.  The cokernel candidate is the extra column of a
full \(775\times775\) left singular basis, or a direct solution of
\(L_N^T\psi_N=0\).

Every statement in this section is conditional on that raw ambient template.
A strong selected realization may have a different matrix size; then the
same index-minus-one, cokernel, and border argument must be restated in its
actual domain and codomain.

Choose a fixed reconstructible direction \(e_N\) in the 192-row projected
jump slot and validate \(\psi_N^Te_N\ne0\).  Under the normalization
\(\psi_N^Te_N=1\), the true border is

\[
 B_N=[L_N,-e_N]\in\mathbb R^{775\times775},
 \qquad
 B_N^T\psi_N=(0_{774},-1)^T.
\tag{3.2}
\]

The sign in (3.2) follows from the column \(-e_N\).  Formula (3.2) is not a
validated strong-space border.  The square artificial candidate Jacobian
\([J_N,c_\nu]\) is not this border.

If the conditional border is invertible and the bordered implicit-function
argument applies, then along a local gap branch

\[
 \mathfrak F_N(z,\nu,\eta)=d(\nu,\eta)e_N,
\tag{3.3}
\]

and, provided
\(d_\nu=\psi_N^T\mathfrak F_{N,\nu}\ne0\),

\[
 d_\lambda=\psi_N^T\mathfrak F_{N,\lambda},
 \qquad
 \rho=\delta^2\nu_\eta
 =-\delta^2\frac{\psi_N^T\mathfrak F_{N,\eta}}
 {\psi_N^T\mathfrak F_{N,\nu}}.
\tag{3.4}
\]

The gap-root system in variables \((z,d,\nu)\) is
\((\mathfrak F_N-de_N,d)=0\), hence is \(776\times776\).

## 4. Continuous advanced adjoint and parameter columns

With residual convention \(R=x'-f\), the interior variational operator on
either branch is

\[
 Du=u'-A_0u-A_4u(\cdot-4)-A_5u(\cdot-5)
 -A_\Theta u(\cdot-\Theta_*).
\tag{4.1}
\]

Its interior advanced expression is

\[
 -p'(s)=A_0(s)^Tp(s)
 +\sum_{\tau\in\{4,5,\Theta_*\}}
 \mathbf1_{\{s+\tau\in I\}}A_\tau(s+\tau)^Tp(s+\tau),
\tag{4.2}
\]

where

\[
 (A_\Theta)_{11}(s)=-2\delta^2\eta X(s-\Theta_*).
\tag{4.3}
\]

Thus the period-delay state coefficient vanishes at \(\eta=0\).  Formula
(4.2) is not the full adjoint.  With jump convention
\(J=S_-x^--S_+x^+\), the full covector contains

\[
 \Psi=(p_-,p_+,\lambda_-,\lambda_+,\gamma,\mu)
\tag{4.4}
\]

and, in the ambient implementation, compatibility multipliers as well.  Its
boundary, seam, and history equations are defined variationally by
\(L^*\Psi=0\).  Integration by parts contributes endpoint atoms which must
balance the entry, exit, phase, jump, and compatibility transpose loads.
When a flight length is below the smallest positive delay, the flight-to-
flight part of the advanced sum is empty; the delayed transpose load moves to
the stored history and endpoint multipliers rather than disappearing.

In fold time the exact interior residual columns are

\[
 R_\nu=(0,-\delta)^T,
 \qquad
 R_\eta=(-\delta^2\{X^2-X_\Theta^2\},0)^T.
\tag{4.5}
\]

Since \(\Theta=\delta T\), differentiation of the moving delay gives

\[
 R_\Theta=(-2\delta^2\eta X_\Theta X_\Theta',0)^T,
\qquad
 R_T=\delta R_\Theta
 =(-2\delta^3\eta X_\Theta X_\Theta',0)^T.
\tag{4.6}
\]

There is no extra factor of \(T\) in (4.6).  At \(\eta=0\), \(R_T=0\), but

\[
 \left.\partial_\eta R_T\right|_{\eta=0}
 =(-2\delta^3X_\Theta X_\Theta',0)^T
\tag{4.7}
\]

need not vanish.  Every pairing must also include derivatives of both
endpoint charts.  If a domain moves with \(T\), the chosen fixed-domain
trivialization contributes additional columns.

## 5. Exact scope and shortest next certificate

This package proves only:

- the raw history dimension 194;
- the exact rank-two compatibility witness;
- the concrete projection \(P_N\) and its invertible completion with
  \(DC_N\);
- endpoint-compatible \(C^0\) dimension 192 and conditional attracting
  dimension 191;
- the repaired ambient `775 x 774` and endpoint-compatible `769 x 768`
  \(C^0\) algebra ledgers;
- the signs and scaling factors in (4.5)--(4.7).

It does not validate internal derivative continuity, a globally
\(C^1/W^{2,p}\) coefficient realization, selected trace charts, an actual
rectangular derivative, column rank, a cokernel vector, a jump complement, a
bordered inverse, coefficient tails, the continuous advanced adjoint, the
period interval, a selected root, or an enclosure of \(\rho_*\).

The shortest closure route starts by choosing a globally \(C^1/W^{2,p}\)
coefficient realization, or adding internal derivative-jump residuals and
redoing the count.  Then construct \(\Gamma_-\) and \(\Gamma_+\) on one fixed
enlarged horizon, prove (2.2) and
\(\Gamma_+\subset C_N^{-1}(0)\), assemble the right-inclusive derivative,
freeze a jump direction with nonzero cokernel pairing, and validate the
bordered finite block plus coefficient tails.  Only then can interval
pairings in (3.4) support a root or response theorem.
