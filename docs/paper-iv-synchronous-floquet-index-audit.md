# Synchronous Floquet-index audit and the last attraction gate

Status: **the stable index is not yet proved.**  The existing directed
certificates prove synchronous orbital hyperbolicity on the full microscopic
gain box and size-uniform transverse variational decay for the fixed
dual-scaffold rank-one topology.  They do not determine on which side of the
unit circle the nontrivial synchronous multipliers lie.  Consequently neither
synchronous attraction nor full-network orbital attraction is asserted here.

The executable audit is
[fhn_synchronous_floquet_index_audit.py](../src/canard_control/fhn_synchronous_floquet_index_audit.py),
the driver is
[fhn_synchronous_floquet_index_audit.py](../experiments/fhn_synchronous_floquet_index_audit.py),
and the tracked record is
[fhn_synchronous_floquet_index_audit.json](../experiments/results/fhn_synchronous_floquet_index_audit.json).
Its SHA-256 digest is

```text
328a4207863279cd5136a159dbe1a7deecc50d1b3eb1be30b6fd34e66b2af024
```

The audit is bound to the following source records:

```text
parameter box:  ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0
Bloch exclusion: c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31
transverse decay: ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb
floating candidate: 7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28
```

## 1. What the current Floquet theorem proves

Let \(b=(\kappa _1,\kappa _3)\) range over

\[
 U=\{ |\kappa _1-0.2|\leq10^{-12},
       |\kappa _3-0.25|\leq10^{-12}\},
\]

and let \(\mathcal M_b\) be the one-period history-space monodromy along the
validated synchronous FHN periodic branch.  The bound Bloch record proves

\[
  1\text{ is algebraically simple},\qquad
  \sigma(\mathcal M_b)\cap\{|z|=1\}=\{1\}
  \quad(b\in U).
\tag{1.1}
\]

It also proves that \(\mathcal M_b\) is compact.  Thus every nonzero spectral
value is an isolated eigenvalue of finite algebraic multiplicity.

The 319 outer Bloch cells are direct inverse certificates on the unit-circle
boundary.  They contain neither a determinant phase nor a winding integer.
The local bordered calculation proves that the translation root is simple;
it does not count roots on either side of the boundary.  In particular,

\[
 \sigma(\mathcal M_b)\cap\{|z|=1\}=\{1\}
 \quad\not\Longrightarrow\quad
 \sigma(\mathcal M_b)\setminus\{1\}\subset\{|z|<1\}.
\tag{1.2}
\]

An unstable hyperbolic periodic orbit satisfies the left side of (1.2) as
well.  This is why every attraction flag in the Bloch record is false.

## 2. The missing integer

Define the nontranslation unstable index

\[
 \nu(b)=\sum_{\substack{z\in\sigma(\mathcal M_b)\\ |z|>1}}
             \operatorname{algmult}(z).
\tag{2.1}
\]

Compactness makes the sum finite.  The validated branch depends continuously
on \(b\), hence so does its monodromy in the usual RFDE operator topology.
Equation (1.1) excludes every nontranslation crossing of the unit circle.
Therefore \(\nu(b)\) is locally constant.  Since \(U\) is connected,

\[
                  \nu(b)=\nu(b_0),\qquad b,b_0\in U.
\tag{2.2}
\]

This is the useful positive conclusion of the audit: the parameter-box
transport step is already available.  The mathematically minimal missing
object is one directed center-anchor certificate

\[
                         \boxed{\nu(0.2,0.25)=0}.                 \tag{2.3}
\]

No second full scan of the microscopic gain box is needed after (2.3).

## 3. What the numerical monodromy says

The audit includes an independent floating-point method-of-steps diagnostic.
It Fourier-interpolates the 129-node center orbit, uses four-point cubic
history interpolation, advances the variational equation with classical
RK4, and diagonalizes the resulting finite history map.

| steps | computed translation multiplier | leading nontranslation multiplier | next multiplier |
|---:|---:|---:|---:|
| 150 | \(0.9999592646\) | \(-0.7580490015\) | \(0.2706051220\) |
| 250 | \(0.9999948687\) | \(-0.7580500396\) | \(0.2705927692\) |
| 400 | \(0.9999992798\) | \(-0.7580501931\) | \(0.2705911758\) |
| 600 | \(0.9999998917\) | \(-0.7580502125\) | \(0.2705909573\) |

The leading nontranslation modulus has stabilized near \(0.75805021\), with
a numerical unit-circle gap near \(0.24194979\).  No nontranslation
multiplier outside the disk was observed at any listed resolution.  This is
strong evidence that (2.3) is true and that a directed calculation has useful
room.

It is not a proof.  The matrices use IEEE binary64 arithmetic; there is no
outward-rounded operator-norm truncation error, no contour resolvent bound,
and no certified spectral-pollution exclusion.  The executable record stores
all three missing fields explicitly as false or null and refuses to relabel a
diagnostic row as directed evidence.

## 4. Why the existing ODE route does not close the gate

At zero delayed gain the planar FHN cycle has the floating nontrivial
multiplier

\[
                    1.6793824785\times10^{-11}.
\tag{4.1}
\]

For a validated planar cycle its nontrivial multiplier could also be enclosed
through the divergence integral.  That gives an attractive starting anchor
for a gain homotopy.  The present ODE-persistence record, however, is itself
binary64, says that the cited direct single-delay theorem does not apply, and
does not validate a continuation from zero gain to the target.  The sampled
ODE-to-target orbit distance after phase alignment is approximately
\(0.883961\), so the target is not covered by a tiny perturbative estimate
already in the repository.

Thus the ODE multiplier is a route marker, not an anchor count for the delayed
target orbit.

## 5. Preferred executable certificate

The shortest route is a direct count at the delayed center orbit.

1. Validate a tangent/adjoint pair and the associated rank-one spectral
   projector, then deflate the simple translation multiplier.
2. Choose an outer radius beyond a directed monodromy bound and formulate an
   analytic Fredholm determinant or an equivalent Riesz-index calculation on
   the annulus outside the unit disk.
3. Reuse the existing unit-circle inverse information on the inner boundary,
   but add the information it does not contain: a directed determinant phase
   or Riesz-projection trace.
4. Enclose a finite-section winding with complex directed intervals and prove
   a finite-to-tail homotopy that cannot cross zero on the full contour.
5. Certify that the enclosed integer is exactly zero.  Equation (2.2) then
   transports the count across all of \(U\).

The crucial new line is step 4.  A sampled singular-value plot, a converged
list of eigenvalues, or pointwise invertibility of contour matrices does not
determine the winding integer.

An alternative, longer route is to validate the zero-gain planar cycle,
continue the periodic branch over the entire homotopy

\[
       (\kappa _1,\kappa _3)=h(0.2,0.25),\qquad 0\le h\le1,
\]

and exclude all nontranslation unit multipliers along that whole homotopy.
The known planar index would then transfer to the target.  The current Bloch
certificate covers only the microscopic target box, not this long segment.

## 6. Composition with transverse decay

The separate transverse Halanay record proves exponential decay, with rate
candidate \(0.02\), for every noncollective variational mode of the fixed
dual-scaffold rank-one two-module topology, uniformly for arbitrary positive
module sizes.  It also proves full-network orbital hyperbolicity when combined
with (1.1).

If (2.3) is directed-certified, then all synchronous nontranslation modes and
all transverse modes are stable.  The RFDE linearized-stability theorem can
then yield local full-network orbital attraction for this fixed topology.  A
directed quantitative synchronous decay rate would require one further
spectral-gap or resolvent estimate; the integer count alone yields qualitative
stability, not the numerical rate \(0.02\) for the collective mode.

Nothing in this composition proves nonlinear global synchronization, a basin
beyond a local orbital neighborhood, a general graph theorem, or physical
pulse robustness.

## 7. Executable refusal rules

The audit refuses

- a different parameter-box, Bloch, transverse, or candidate artifact hash;
- a different orbit fingerprint or network model identifier;
- deletion of any proved hyperbolicity or transverse-decay flag;
- promotion of any historical attraction or general-topology flag;
- a self-declared anchor count without a registered directed certificate;
- a floating diagnostic relabeled as outward rounded; and
- invented operator-error or contour-resolvent fields on the binary64 rows.

Reproduce the record with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_synchronous_floquet_index_audit.py
```

and test it with

```bash
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fhn_synchronous_floquet_index_audit.py
```

The correct present conclusion is therefore narrow but encouraging: the
stable-index bottleneck has been reduced to one center integer, and the
non-directed spectrum shows a substantial candidate gap, but attraction is
still unproved until that integer is directed-certified.
