# The second method-of-steps cover of the target C4 chart

Status: **rigorous computer-assisted cover of the complete second
method-of-steps rectangle**

\[
 P_2=[1,3]\times[-1/20,1/20].
\]

Together with the pinned first-step certificate on
$[-3,1]\times[-1/20,1/20]$, this proves the physical P-matrix inequalities
on the full strip $[-3,3]\times[-1/20,1/20]$.  It also proves the late
scalar separation

\[
 X(t,\lambda)<X_e:=X(-3,\lambda),
 \qquad (t,\lambda)\in[-2,3]\times[-1/20,1/20].
\]

Combined with the already proved inequality $X_t<0$ on
$[-3,-2]\times[-1/20,1/20]$, the two physical cross-separation conditions
are now closed on the stated rectangle.  These results do not yet supply an
enlarged label collar, the gluing theorem on such a collar, a global target
graph, or a complete-history root.

## 1. Exact delayed-source partition

At the frozen target slice, the $\Theta$-delay coefficient vanishes and the
active delays are four and five.  For $1<t\leq3$,

\[
 t-4\in(-3,-1],\qquad t-5\in(-4,-2].
\]

The source of each slot is therefore known before the second method step is
started.  More precisely,

| Current time | Delay-four source | Delay-five source |
|---|---|---|
| $1<t<3/2$ | first-step solution on $(-3,-5/2)$ | affine history on $(-4,-7/2)$ |
| $3/2<t<2$ | first-step solution on $(-5/2,-2)$ | C4 patch on $(-7/2,-3)$ |
| $2<t\leq3$ | first-step solution on $(-2,-1]$ | first-step solution on $(-3,-2]$ |

Thus the only interior formula changes are $t=3/2$ and $t=2$.  At the first,
the degree-nine cutoff begins with a fifth-order zero, so the affine history
and patch have the same jets through order four.  At the second, the pinned
C4 preparation matches the recursively determined physical jets through
order four.  The proof grid splits at both points; it never evaluates a cell
across a source-formula change.

The delay-four slot uses 8,000 retained solution subcells over all labels.
The delay-five slot uses 2,000 affine-history subcells, 2,000 C4-patch
subcells, and 4,000 retained solution subcells.  These counts are checked by
the certificate.

## 2. Reusing the first-step enclosures

For each label cell, the first-step proof is replayed and its strict
polynomial tubes are retained for

\[
 z_c(t)=z(t,\lambda_c),\qquad
 v_c(t)=\partial_\lambda z(t,\lambda_c),\qquad
 w(t,\lambda)=\partial_{\lambda\lambda}z(t,\lambda).
\]

The first-step grid has width $10^{-2}$ and the second-step grid has width
$5\times10^{-3}$.  Since both delays are integers, a delayed second-step
half-cell has exactly the same normalized coordinate as one half of a stored
first-step cell.  If $p(u)$ is a retained polynomial on $0\leq u\leq1$, the
source inserted into a second-step cell is exactly

\[
 p(v/2)\quad\hbox{or}\quad p((1+v)/2),
 \qquad 0\leq v\leq1.
\]

The code performs this affine polynomial composition with outward-rounded
coefficients.  No interpolation, sampled history value, or dense binary64
output is used as a delayed enclosure.  Binary64 values only choose local
polynomial centers.

The full-label families are recovered by the same two mean-value enclosures
as in the first step:

\[
 \partial_\lambda z(t,\Lambda)
 \subset v_c(t)+(\Lambda-\lambda_c)w(t,\Lambda),
\]

\[
 z(t,\Lambda)
 \subset z_c(t)+(\Lambda-\lambda_c)
                    \partial_\lambda z(t,\Lambda).
\]

These are ordinary mean-value identities for the smooth parameterized ODE
on each method step, not finite-difference estimates.

## 3. The logarithmic-norm enclosure

A rectangular forward propagation closes most of the interval but eventually
loses a principal-minor sign through rotational wrapping.  The second-step
proof instead retains Euclidean error balls.  State, first variation, and
second variation all have the same current two-dimensional linear part

\[
 A(X)=\begin{pmatrix}F_X&1\\-1&0\end{pmatrix}.
\]

Its symmetric part is diagonal:

\[
 \frac{A(X)+A(X)^\top}{2}
   =\operatorname{diag}(F_X,0),
 \qquad \mu_2(A)=\max\{F_X,0\}.
\]

This identity is checked symbolically against the implemented RFDE field.
On one cell, let $p$ be the degree-eight coupled Taylor center, let $r_0$ be
the incoming error radius, let $\delta$ bound the Bernstein range of the
defect at the center, and let $\mu$ bound the displayed logarithmic norm on
the candidate tube.  The differential inequality for the error gives

\[
 r(s)\leq e^{\mu s}r_0+
 \begin{cases}
   \dfrac{e^{\mu s}-1}{\mu}\,\delta,&\mu>0,\\[6pt]
   s\delta,&\mu=0.
 \end{cases}
\]

A strict ball inclusion at $s=h$ proves the continuous-time tube and its
endpoint.  For the second variation, the candidate ball is first used in the
two mean-value reconstructions; the resulting state tube supplies both the
coefficient $A(X)$ and its logarithmic-norm bound.  This preserves the actual
dependence of the second variational equation instead of freezing it at the
central label.

All field, defect, logarithmic-norm, exponential, polynomial-composition and
Bernstein operations used in this argument have directed MPFR rounding.  The
degree-eight Taylor polynomial is only a center: its accuracy is never an
acceptance criterion.

## 4. Certified margins

The primary 192-bit computation covers 400 time cells for each of 20 label
cells, hence 8,000 second-step rectangles.  Its global outward bounds are

\[
\begin{aligned}
 \inf (-7,2)z_t
   &\geq 0.11429961118133590537,\\
 \inf (3,1)z_\lambda
   &\geq 1.2890305141442167,\\
 \inf\{-13\det(z_t,z_\lambda)\}
   &\geq 2.1324351402549470,\\
 \sup\det(z_t,z_\lambda)
   &\leq-0.1640334723273036194,\\
 \inf\{X_e-X(t,\lambda): -2\leq t\leq3\}
   &\geq0.46123227896685597435.
\end{aligned}
\]

The smallest strict enclosure gaps for the central state, central first
variation, and full-label second variation are respectively
$5.60\times10^{-7}$, $4.71\times10^{-5}$, and $4.39\times10^{-3}$.

A separate 256-bit execution of the same source kernel covers the same 8,000
rectangles and returns the same displayed margins to the shown digits.  This
is a same-kernel precision replay.  It is useful evidence against accidental
precision sensitivity, but it is **not an independent implementation or an
independent proof**.

The theorem status is therefore:

| Statement | Status |
|---|---|
| Second-step P-matrix cover on $[1,3]\times[-1/20,1/20]$ | **proved here** |
| Full physical P-matrix cover on $[-3,3]\times[-1/20,1/20]$ | **proved by composition with the pinned first step** |
| Late separation $X<X_e$ on $[-2,3]\times[-1/20,1/20]$ | **proved here** |
| Both physical cross-separation inequalities | **proved by composition** |
| Enlarged label collar | open |
| C4-history/physical global embedding on an open collar | open |
| Target global graph and complete-history root | open |

## 5. Recoverable reproduction

Each precision is split into twenty deterministic label shards.  A completed
shard is reused only after its label, precision, exact interval, 400-cell
count, delayed-source counts, strict margins, body digest, and pinned
proof-cell digest have all been checked.

Run or resume the primary proof with

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_second_step_cover.py --run-missing --precision 192
```

Run or resume the same-kernel precision replay with

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_second_step_cover.py --run-missing --precision 256
```

After both sets are present, aggregate and validate the source-bound result:

```text
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_second_step_cover.py --aggregate
```

Running the generator without arguments performs these three operations in
order.  It uses only the local CPU and can resume after interruption without
recomputing validated shards.
