# Projection-neutral cancellation in the shared-resource class

Status: **the interior order-three cancellation is proved.**  The result is
an exact mixed-jet statement on the singular canard for the homogeneous
shared-resource network of
[paper-ii-shared-resource-dobrushin-class.md](paper-ii-shared-resource-dobrushin-class.md).
It is not a selected-history root theorem: trace, preparation, and endpoint
terms remain separate until a concrete matching construction is proved.

## 1. Question

The shared-resource class supplies a dimension-uniform two-dimensional
history graph for arbitrary finite Markov networks.  It is therefore a
natural candidate for the positive topology-response example in Paper II.
That conclusion is not automatic.  With homogeneous node curvature, the
first transverse graph response is constant along the singular canard, and
every balanced delay operator annihilates a constant history.

The consequence is a useful no-go statement.  Preserving the complete
critical projected delay measure removes the reduced order-\(\delta\)
direct response; the vanishing zeroth stable graph removes a reduced
order-\(\delta^2\) return; and the constant first stable response also
removes the first candidate reduced order-\(\delta^3\) transverse return.
Under the usual \(\mu=\delta^2\nu\) canard scaling, the last two coefficients
would generate physical root shifts of orders \(\delta^3\) and \(\delta^4\),
respectively.

## 2. Fixed-support structural direction

Write the atomic delay measure as

\[
 \mathbb B_\zeta(d\theta)
 =\sum_{k=0}^{m} (B_k+\zeta R_k)\,\delta_{\theta_k}(d\theta),
 \qquad
 C_\zeta=\sum_k(B_k+\zeta R_k).
 \tag{2.1}
\]

Let \(P_c=\mathbf1\pi^\top\), \(P_\perp=I-P_c\), and
\(A=D(P-I)|_{E_N}\).  Assume the complete projected measure is fixed:

\[
 \pi^\top R_k\mathbf1=0
 \qquad\text{for every distinct atom }\theta_k.
 \tag{2.2}
\]

This is stronger than preserving a scalar moment.  Define

\[
 M_1=\sum_k\theta_kB_k,
 \qquad
 \dot M_1=\sum_k\theta_kR_k.
 \tag{2.3}
\]

The singular canard of
\(X'=Y-X^2,\ Y'=-X\) is

\[
 \gamma_0(s)
 =\left(-\frac{s}{2},\frac{s^2-2}{4}\right).
 \tag{2.4}
\]

Hence

\[
 X_0(s)-X_0(s-\theta_k)=-\frac{\theta_k}{2}.
 \tag{2.5}
\]

## 3. Exact cancellation

> **Proposition 3.1 (constant first stable response).**  On the invariant
> history graph, the first \(\delta\)-coefficient of the transverse response
> to the direction \((R_k)\), restricted to \(\gamma_0\), is
> \[
>  D_\zeta z_1(\gamma_0(s))
>  =\frac K2 A^{-1}P_\perp\dot M_1\mathbf1.
>  \tag{3.1}
> \]
> It is independent of \(s\).

**Proof.**  Insert
\(z=\delta z_1+O(\delta^2)\) in the stable equation (3.3) of the
shared-resource class.  Its order-\(\delta\) equation is

\[
 Az_1+KP_\perp\mathcal L[\mathbf1X_0]=0.
 \tag{3.2}
\]

Equations (2.1) and (2.5) give
\(D_\zeta\mathcal L[\mathbf1X_0]
=-\dot M_1\mathbf1/2\).  Inverting \(A\) on \(E_N\) proves (3.1).
\(\square\)

> **Theorem 3.2 (interior \(\delta^3\) cancellation).**  Under (2.2), the
> derivative of the reduced order-\(\delta\) direct critical delay term is
> zero.  The reduced order-\(\delta^2\) transverse return is zero because the
> stable graph vanishes at \(\delta=0\).  The full interior
> stable-to-critical derivative at reduced order \(\delta^3\) is
> \[
>  K\pi^\top\left(
>    (D_\zeta\mathcal L_0)[z_{1,0}(\gamma_0)]
>    +\mathcal L_0[D_\zeta z_1(\gamma_0)]
>  \right),
>  \tag{3.3}
> \]
> and it also vanishes exactly.  Consequently the interior coefficients
> that could produce physical root shifts at orders
> \(\delta^3=\varepsilon^{3/2}\) and \(\delta^4=\varepsilon^2\) both vanish.

**Proof.**  Condition (2.2) annihilates the direct critical response atom by
atom.  Applying the calculation of Proposition 3.1 without differentiating
in \(\zeta\) also gives

\[
 z_{1,0}(\gamma_0(s))
 =\frac K2A^{-1}P_\perp M_1\mathbf1,
 \tag{3.4}
\]

so both the base first stable jet and its structural derivative are constant
histories.  For every \(\zeta\), the current matrix in
\(\mathcal L_\zeta\) is the sum of its delayed layers.  Consequently

\[
 \mathcal L_\zeta[c]
 =C_\zeta c-\sum_k(B_k+\zeta R_k)c=0
 \tag{3.5}
\]

for every constant vector \(c\).  Differentiating this identity shows that
both terms in (3.3) vanish; omitting the first term would not be a valid
chain rule.  The homogeneous local
quadratic return is \(-\delta^2\pi^\top z^{\circ2}\); because
\(z=O(\delta)\), it starts at order \(\delta^4\) and has no linear
order-three contribution.  No other transverse term occurs through the
displayed order in the exact chart. \(\square\)

## 4. Root-level consequence and boundary

If a selected-history construction is subsequently proved with
structurally fixed preparation, phase, and endpoint data through this order,
and its gap inherits the displayed mixed-jet expansion, Theorem 3.2 makes
the **interior contribution** to the physical root response satisfy

\[
 \bigl(\partial_\zeta\mu_c(\delta,0)\bigr)_{\rm interior}
 =o(\delta^4).
 \tag{4.1}
\]

An explicit \(O(\delta^5)\) bound or coefficient needs one additional
uniform \(\delta\)-jet, together with the selected-trace remainder; it is
not claimed here.

Without fixed trace and endpoint data, (4.1) does not follow from the
interior calculation: an explicit structural dependence of the matching
sections can contribute at the same order.  Thus this note proves a
mechanism-level cancellation, not a complete-history canard root.

The result changes the Paper II model choice.  The shared-resource class is
a clean positive example for the dimension-uniform graph theorem, but it is
not the required nonzero \(\varepsilon^{3/2}\) topology-response witness.
Such a witness must retain heterogeneous curvature, a nontrivial stable
shift, or another proved return channel, as in the lifted two-module class.

## 5. Reproduction

Run

    PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
      tests/test_shared_resource_response.py

The exact tests use a nonuniform stationary distribution.  They verify a
projection-neutral direction with nonzero transverse first moment and
nonzero stable graph response, while its constant-history critical return
and entire interior order-three coefficient are exactly zero.
