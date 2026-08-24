# An exact fourth-order preparation seam at the target anchor

Status: **the incoming seam is exact; the target chart and graph remain
open.**  We freeze the target-candidate parameters, interpreting its decimal
values as exact rational inputs, and put \(t_0=-3\).

## 1. Triangular RFDE jets

Let \(\bar h_\lambda\) be the polynomial incoming template with the
transverse shift \((0,\lambda)\).  For the physical fixed-delay field \(F\),
define

\[
 a_0(\lambda)=\bar h_\lambda(t_0),\qquad
 a_{m+1}(\lambda)=m![s^m]F(A_m(s),B_{4,m}(s),B_{5,m}(s),B_{\Theta,m}(s)),
 \tag{1.1}
\]

where \(A_m(s)=\sum_{j=0}^m a_j s^j/j!\) and
\(B_{\tau,m}(s)=\sum_{j=0}^m\bar h_\lambda^{(j)}(t_0-\tau)s^j/j!\).
Positive delays make (1.1) triangular.  For \(m=0,1,2,3\), it determines the
time jets through order four without changing the RFDE.

## 2. Exact right-Hermite patch

Set \(w=1/2\) and

\[
 \chi_9(u)=126u^5-420u^6+540u^7-315u^8+70u^9,
 \qquad
 \phi_j(r)=\frac{r^j}{j!}\chi_9(1+r/w).
\]

Extend \(\phi_j\) by zero for \(r\le-w\).  Direct differentiation gives

\[
 \phi_j^{(k)}(-w)=0,
 \qquad
 \phi_j^{(k)}(0)=\delta_{jk},
 \qquad 0\le j,k\le4.
 \tag{2.1}
\]

Consequently

\[
 H_\lambda(t)=\bar h_\lambda(t)+
 \sum_{j=1}^4\left(a_j(\lambda)-\bar h_\lambda^{(j)}(t_0)\right)
 \phi_j(t-t_0)
 \tag{2.2}
\]

is jointly \(C^4\), equals the unpatched polynomial template for
\(t\le-3.5\), preserves the endpoint curve, and has
\(H_\lambda^{(j)}(t_0)=a_j(\lambda)\).  This unpatched polynomial is not the
parent candidate's first-order bump history on all of the far strip;
consequently the fourth-order state and variational flows must be replayed
rather than inherited.  Equations
(1.1)--(2.2) prove all recursive time compatibilities.  Since they hold as
polynomial identities in \(\lambda\), differentiating proves every mixed
identity with time order plus transverse order at most four.  The executable
audit checks ten vector, hence twenty scalar, zero identities exactly over
\(\mathbb Q(\sqrt5,\lambda)\).

For orientation only, a binary64 sample of the preparation strip gives
\(\det(\partial_tH,\partial_\lambda H)\in[-0.914,-0.449]\) and a maximum
state correction below \(0.018\).  These samples are not interval bounds.

## 3. Claim boundary

The construction closes the finite preparation seam.  Conditional on
existence, standard method of steps now yields a jointly \(C^4\) local
solution family.  No interval continuation through \(t=3\), full-chart
\(C^4\) bound, global injectivity, degree-one boundary certificate,
candidate-class self-map, target graph, selected trace, or complete-history
root is proved here.  In particular the combined flag “target \(C^4\) chart
and seam validated” remains false: only its seam component has been removed.

## 4. Reproduction

```bash
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_c4_preparation_seam.py
```
