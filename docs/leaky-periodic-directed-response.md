# Directed frequency--amplitude response of both leaky periodic branches

Status: **rigorous first-derivative theorem on the common parameter box.**
For each already validated inner and outer periodic branch, this certificate
studies

\[
 (a,\kappa _3)\longmapsto G(a,\kappa _3)
 =\left(F,A\right)
 =\left(\frac1T,\max_\phi v(\phi)-\min_\phi v(\phi)\right).
\]

Here \(F\) is frequency in cycles per unit physical time and \(A\) is the
unsquared physical voltage amplitude. The common closed box is

\[
 |a-1/4|\leq10^{-10},\qquad
 |\kappa _3-1/200|\leq10^{-10}.
\]

The result proves a directed \(2\times2\) enclosure of \(DG\) on each branch
and a fixed nonzero sign for its determinant. Consequently, \(G\) is a
pointwise local diffeomorphism throughout the box. This local response
result does **not** prove a physical-pulse onset, a unique threshold, a
history-space separator, a network safety threshold, or outer-orbit capture
by a larger pulse.

## What is inherited and what is new

The parent common-box artifact proves, independently for both branches, a
unique phase-fixed RFDE orbit in a radius-\(10^{-5}\) ball, a bounded
bordered inverse, and one simple voltage maximum and minimum. The present
calculation does not claim a new periodic-orbit or inverse validation. It
replays the source-defined parent preconditioner and its outward
\(Y,Z_0,z_1,z_2,z_3\) majorants.

The same majorants close the stricter nested radii

\[
 r_{\rm in}=10^{-7},\qquad r_{\rm out}=10^{-6}.
\]

Their uniform contraction bounds are below \(0.032143\) and \(0.097301\),
with strict radii margins greater than \(4.87\times10^{-8}\) and
\(6.19\times10^{-8}\), respectively. Parent-radius uniqueness identifies
the smaller fixed points with the already validated branches. No floating
inverse is silently promoted to an exact orbit inverse.

## Exact parameter columns

For the leaky RFDE residual

\[
 R_v=D_\phi v-Tf_v,\qquad
 R_w=D_\phi w-T\epsilon(v-a-w),
\]

the parameter columns are

\[
 R_a=(0,+T\epsilon,0),\qquad
 R_{\kappa _3}=(-T\epsilon C(v),0,0),
\]

where

\[
 C(v)=\frac{(v_{\tau_0}-1)^3+(v_{\tau_1}-1)^3}{2}-(v-1)^3.
\]

Thus the bordered sensitivity solve uses the right-hand sides
\((0,-T\epsilon,0)\) and \((+T\epsilon C,0,0)\). In particular, the
\(a\)-column belongs to the leaky recovery row; it is not a renamed
coupling-gain column. Both physical delays remain fixed, so their phase
translations vary exactly through \(\tau_j/T\).

## Uniform sensitivity enclosure

For each center sensitivity \(\bar s_q\), the directed residual budget
separates:

1. the bordered solve residual at the candidate;
2. state-operator variation times \(\bar s_q\);
3. period-column and physical-delay translation variation;
4. the leaky slow-row variation; and
5. variation of the appropriate parameter forcing.

The slow block uses

\[
 \epsilon\rho(\|s_v\|+\|s_w\|)
 +2\epsilon\rho|s_T|,
\]

which includes the recovery leak. The parent preconditioner is applied with
separate directed fast- and slow-input block norms. This structural split is
essential for the outer branch: one global norm discards the row structure
and produces a useless error bound. Division by the strict nested
contraction margin encloses the exact sensitivity \(s_q\).

## Exact extrema and the amplitude row

The amplitude is evaluated at exact extrema, not numerical root locations.
The same branch-independent algorithm starts from each parent
unique-curvature window and finds outward MPFR dyadic endpoints with
opposite strict signs of \(v_\phi\). Parent curvature gives exactly one root
inside each refined window, and the maximum and minimum windows are
disjoint.

At those exact roots,

\[
 A_q=s_{v,q}(\phi_{\max})-s_{v,q}(\phi_{\min}),
\]

because the position terms
\(v_\phi(\phi_*)\,\partial_q\phi_*\) vanish there. The implementation
evaluates the center sensitivity over the whole exact-root window and adds
the validated Wiener sensitivity error at both extrema. It never sets a
position term to zero at a merely floating root. The frequency row is

\[
 F_q=-\frac{T_q}{T^2}.
\]

## Invertibility and branch-centered target balls

The determinant is formed directly from the four directed response entries:

\[
 \det DG_{\rm in}\in[-0.229823,-0.228398],\qquad
 \det DG_{\rm out}\in[0.533847,1.694625].
\]

The fixed negative inner sign and positive outer sign prove nonsingularity
and the pointwise local-diffeomorphism theorem. Singular-value and
inverse-norm bounds use only these rigorous determinant margins and the
response Frobenius bounds.

For each branch, \(B\) is the exact stored binary64 matrix obtained by
inverting the parent response candidate at the exact parameter center
\(p_0=(1/4,1/200)\). A 160-bit directed multiplication audits its formation
against that stored candidate before \(B\) is applied to the rigorous
response box. The directed formation defects are below
\(2.80\times10^{-14}\) and \(9.69\times10^{-16}\). The whole-box tests give

\[
 \sup\|I-B_{\rm in}DG_{\rm in}\|_\infty<0.148457,\qquad
 \sup\|I-B_{\rm out}DG_{\rm out}\|_\infty<0.584356.
\]

These are common bounds over every parameter in the closed box, not samples
at \(p_0\). For \(h=10^{-10}\), set

\[
 H_y(p)=p-B(G(p)-y).
\]

If \(q=\sup\|I-BDG\|_\infty<1\), then \(H_y\) is a contraction of the
parameter \(\ell^\infty\)-box into itself whenever

\[
 \|y-G(p_0)\|_2
 \leq \frac{h(1-q)}{\|B\|_{2\to\infty}}.
\]

Banach's theorem gives one inverse image and the corresponding inverse
Lipschitz bound. The branch radii are greater than
\(4.0971\times10^{-13}\) (inner) and \(4.5363\times10^{-12}\) (outer).
The recorded common radius is their minimum. These are two
**branch-centered** Euclidean output balls, centered at the exact values
\(G_{\rm in}(p_0)\) and \(G_{\rm out}(p_0)\). “Common” does not mean that the
balls are concentric, and no floating output replaces either exact center.
No second-order response radius is inferred from a padded numerical
determinant.

For the flagship interface, the first two coordinates of
\(Q=(F_{\rm out},A_{\rm out},J-J_c)\) come from the **outer** periodic orbit.
Its two-coordinate target gate therefore uses the outer radius
\(4.5363\times10^{-12}\), not the smaller simultaneous-two-branch radius.
The minimum is retained only as an optional statement that both distinct
branch-centered responses can be tuned at the same output-radius scale.
This bookkeeping does not validate \(J_c\), a physical onset, or the
third-coordinate pulse theorem; those claims remain separate and open here.

## Reproduction

Run:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src \
      /usr/bin/python3 experiments/leaky_periodic_directed_response.py

The tracked result binds the common-box parent, both orbit parents, every
claim-bearing source, the runtime, the exact certificate schema, and all
hashes. Its validator reconstructs the parent preconditioners, repeats the
directed calculation, normalizes dataclass tuples to JSON arrays, and
rejects altered values, types, claim flags, parent hashes, source hashes, or
extra schema fields.
