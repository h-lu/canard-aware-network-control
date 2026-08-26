# An explicit history-space basin for the leaky quiet equilibrium

Status: **proved exactly at the declared center parameters.**  A rational
quadratic Lyapunov function and a Razumikhin--Halanay estimate give an
explicit forward-invariant neighborhood of the constant quiet history and a
quantitative exponential decay rate.  This is a local basin theorem in the
full RFDE history space.  It does not prove that the physical pulse with
$J=0.30$ enters this neighborhood, and it gives no information about the
outer periodic basin or the onset separator.

The exact arithmetic is implemented in
[`leaky_quiet_history_basin.py`](../src/canard_control/leaky_quiet_history_basin.py),
and the tracked result is
[`leaky_quiet_history_basin.json`](../experiments/results/leaky_quiet_history_basin.json).

## 1. Perturbation equation

Let

\[
 E_q=(\alpha,\alpha-\tfrac14),\qquad
 \alpha=(3/4)^{1/3},
\]

and write

\[
 x=v-\alpha,\qquad y=w-(\alpha-\tfrac14),\qquad z=(x,y)^T.
\]

At

\[
 \varepsilon=\frac15,qquad
 \kappa _1=\frac1{250},\qquad
 \kappa _3=\frac1{200},
\]

the autonomous leaky RFDE becomes

\[
 z'(t)=A_0z(t)+\frac C2e_1
 \{x(t-\tau _0)+x(t-\tau _1)\}+e_1N(t),
\tag{1.1}
\]

where

\[
 A_0=\begin{pmatrix}A&-1\\1/5&-1/5\end{pmatrix},
 \quad
 A=1-\alpha^2-C,
 \quad
 C=\varepsilon\{\kappa _1+3\kappa _3(\alpha-1)^2\}.
\tag{1.2}
\]

The nonlinear remainder is

\[
\begin{aligned}
N={}&-\{\alpha+3\varepsilon\kappa _3(\alpha-1)\}x^2
     -(\tfrac13+\varepsilon\kappa _3)x^3\\
&+\frac{\varepsilon\kappa _3}{2}
 \sum_{j=0}^1
 \{3(\alpha-1)x(t-\tau_j)^2+x(t-\tau_j)^3\}.
\end{aligned}
\tag{1.3}
\]

Equation (1.3) follows by exact polynomial expansion; no Taylor remainder is
discarded.

## 2. A rational Lyapunov matrix

Take

\[
 P=\begin{pmatrix}
 2823/100&-1351/50\\
 -1351/50&13759/100
 \end{pmatrix},
 \qquad V(z)=z^TPz.
\tag{2.1}
\]

The earlier exact equilibrium certificate gives

\[
 0.17362092325<A<0.17380268812,
 \qquad C<0.00082511675.
\tag{2.2}
\]

Exact rational determinants prove

\[
 21I<P<144I,qquad \|Pe_1\|_2<40.
\tag{2.3}
\]

Indeed,

\[
 \det(P-21I)=112.8653,qquad
 \det(144I-P)=12.0053,
\]

and $p_{11}^2+p_{12}^2=1527.0133<1600$.  Put

\[
 Q(A)=-(A_0^TP+PA_0).
\]

Interval evaluation of its two affine entries gives

\[
 Q(A)>\frac{99}{100}I
\tag{2.4}
\]

throughout (2.2).  The exact lower determinant of
$Q(A)-99I/100$ is

\[
 \frac{20922213562808689991}
 {1562500000000000000000000}
 >1.3390\times10^{-5}.
\tag{2.5}
\]

## 3. Nonlinear and delay gain

Fix the Euclidean state radius

\[
 R=10^{-3}.
\tag{3.1}
\]

Whenever the current and both delayed perturbations have norm at most $R$,
(1.3) gives

\[
 |N(t)|\le L(R)
 \max\{|z(t)|,|z(t-\tau_0)|,|z(t-\tau_1)|\},
\tag{3.2}
\]

with the exact rational upper bound

\[
 L(R)=\frac{2728453}{3000000000}
 <9.095\times10^{-4}.
\tag{3.3}
\]

Let

\[
 S(t)=\sup_{t-\tau_1\le s\le t}V(z(s)).
\]

Using (2.3)--(3.3) in the derivative of $V$, followed only by
$2\sqrt{VS}\le V+S$, yields

\[
 D^+V(t)\le-\eta V(t)+bS(t),
\tag{3.4}
\]

where

\[
 a=\frac{99/100}{144}=\frac{11}{1600},
 \qquad
 b=\frac{40\{C+L(R)\}}{21}
 \le\frac{20815213}{6300000000},
 \qquad
 \eta=a-b.
\tag{3.5}
\]

The strict Halanay margin is

\[
 \eta-b=a-2b
 \ge\frac{841037}{3150000000}
 >2.6699\times10^{-4}.
\tag{3.6}
\]

## 4. Explicit basin and rate

Since $\sqrt5<9/4$, the maximal delay satisfies
$\tau_1=5\sqrt5<45/4$.  Choose $\lambda=10^{-4}$.  Then

\[
 e^{\lambda\tau_1}
 <e^{9/8000}
 \le\frac{1}{1-9/8000}
 =\frac{8000}{7991},
\]

and exact arithmetic gives

\[
 \eta-\lambda-be^{\lambda\tau_1}
 >\frac{134750597}{825300000000}
 >1.6327\times10^{-4}.
\tag{4.1}
\]

The Halanay inequality therefore proves the following.

> **Theorem 4.1 (explicit quiet-history basin).**  Let
> $r=5\sqrt5$.  If a continuous initial history $\phi$ satisfies
> \[
>  \sup_{-r\le\theta\le0}
>  (\phi(\theta)-E_q)^TP(\phi(\theta)-E_q)
>  \le\frac{21}{10^6},
> \tag{4.2}
> \]
> then the autonomous leaky RFDE solution exists for all positive time,
> remains in the Euclidean radius-$10^{-3}$ neighborhood of $E_q$, and
> satisfies
> \[
>  V(z(t))\le e^{-t/10000}
>  \sup_{-r\le\theta\le0}V(\phi(\theta)-E_q),
>  \qquad t\ge0.
> \tag{4.3}
> \]

For completeness, the radius hypothesis in (3.2) is not assumed after time
zero.  Since $P>21I$, (4.2) puts the compact initial history strictly inside
the Euclidean radius-$R$ ball.  If a first exit occurred at $t_*>0$, then all
current and delayed states up to $t_*$ would satisfy the radius hypothesis,
so the scalar Halanay comparison would give
$V(z(t_*))<21R^2$.  On the other hand, $|z(t_*)|=R$ and $P>21I$ would give
$V(z(t_*))>21R^2$, a contradiction.  Boundedness then gives global
continuation for this finite-delay polynomial RFDE.

The same comparison also makes the history-space claim explicit.  If
$M_0=\sup_{-r\leq\theta\leq0}V(z(\theta))$, then for $t\geq r$,

\[
 \sup_{-r\leq\theta\leq0}V(z(t+\theta))
 \leq e^{-(t-r)/10000}M_0.
\tag{4.4}
\]

Consequently (4.2) is a closed forward-invariant subset of the quiet basin
in the complete RFDE history space.  It is not a global basin statement.

## 5. Remaining routing gate

For physical onset, one must still prove that the released pulse history, or
a later autonomous history segment, enters (4.2) for a subthreshold endpoint
such as $J=0.30$.  A binary64 trajectory approaching $E_q$ is not enough:
the entire retained history must be enclosed in the ellipsoid simultaneously.
The pulse-side endpoint likewise needs entry into a rigorously attracting
outer-orbit neighborhood.  The present theorem closes only the target
neighborhood on the quiet side.
