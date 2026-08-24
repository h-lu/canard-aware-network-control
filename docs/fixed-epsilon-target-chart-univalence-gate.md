# A P-matrix univalence gate for the target causal chart

Status: **exact C4 incoming preparation and analytic incoming
\(\lambda\)-derivative, with a combined binary64 history/physical feasibility
test.** No outward-rounded enclosure of either the C4 history strip or the
physical delay flow is computed here. Thus this note proves neither global
injectivity nor boundary degree nor the open \(C^4\) collar or target graph.

The useful simplification is that global injectivity need not be attacked by
pairwise separation of a sampled boundary. For this chart it reduces to three
P-matrix inequalities for the state and its first transverse variation, plus
two scalar \(X\)-separation inequalities.

## 1. Legacy exact gate and the C4 replacement

Split the retained rectangle at \(t_e=-3\):

\[
 H=[-3-\Theta_*,-3]\times[-r,r],\qquad
 P=[-3,3]\times[-r,r],\qquad r=\frac1{20}.
\]

For the earlier first-order preparation, write \(b(s)=sS(s+1)\). For the flat step,
direct differentiation gives

\[
 S'=\frac{L}{4\cosh^2(h/2)},\qquad
 h=\frac1z-\frac1{1-z},\quad
 L=\frac1{z^2}+\frac1{(1-z)^2}.
\]

Eliminating \(z(1-z)\) yields

\[
 L=h^2+4+2\sqrt{4+h^2}\leq 8+\frac32h^2,
\]

while \(4\cosh^2(h/2)\geq4+h^2\). Hence \(0\leq S'\leq2\) and
\(|b'|\leq3\). The prepared formula satisfies

\[
 X_t=-\frac12+\lambda b',\quad X_\lambda=b,\qquad
 Y_t=\frac{t+q}{2}+\rho\nu,\quad Y_\lambda=1.
\]

Here \(q<0\), \(\rho<1/2\), and \(\nu<1/4\). Consequently

\[
 -X_t\geq\frac7{20},\qquad -Y_t\geq\frac{11}{8}.
\]

Since \(b\leq0\), the output frame

\[
 L_H=\begin{pmatrix}-1&0\\0&1\end{pmatrix}
\]

has two positive diagonal principal minors and

\[
 \det D(L_H\Psi)=-X_t+bY_t\geq\frac7{20}.
\]

The Gale--Nikaido global-univalence theorem therefore proves that the
*legacy first-order* prepared-history chart is one-to-one. This calculation is
exact, but it is not silently transferred to the C4 chart.

The combined candidate instead uses the degree-nine right-Hermite preparation
from the pinned C4 seam certificate. Its incoming label derivative is
evaluated as

\[
 \partial_\lambda h_4(t,\lambda)
 =(0,1)+\sum_{j=1}^4
   \partial_\lambda a_j(\lambda)\,\phi_j(t+3),
\]

where every \(a_j\) is first differentiated exactly as a polynomial over
\(\mathbb Q(\sqrt5,\lambda)\), and only the resulting coefficients are rounded
for binary64 evaluation. No neighboring labels initialize the variational
DDE.

At 1201 history times and all 41 labels, the binary64 C4-history sample gives

\[
 \min(-X_t)=0.36938890759680243,\quad
 \min Y_\lambda=0.9769182273688002,\quad
 \min(-\det D\Psi)=0.45,
\]

with \(\det D\Psi\in[-0.9130384030757663,-0.45]\). These are sampled margins,
not an exact or interval P-matrix proof for the C4 history strip.

## 2. Physical P-matrix theorem contract

Use the integer output frame

\[
 L_P=\begin{pmatrix}-7&2\\3&1\end{pmatrix},
\qquad \det L_P=-13.
\]

### Proposition 2.1

Let \(\Psi\) be \(C^1\) near \(P\). If positive \(m_t,m_\lambda,m_d\)
exist such that everywhere on \(P\)

\[
 (-7,2)\partial_t\Psi\geq m_t,\qquad
 (3,1)\partial_\lambda\Psi\geq m_\lambda,\qquad
 -13\det D\Psi=\det D(L_P\Psi)\geq m_d,
\]

then \(\Psi|_P\) is one-to-one and \(\det D\Psi<0\). Moreover
for every \(y\in L_P\Psi(\operatorname{int}P)\),

\[
 \deg(L_P\Psi,\operatorname{int}P,y)=+1.
\]

The corresponding local degree of the original chart \(\Psi\) is \(-1\);
the positive degree belongs to the oriented output frame \(L_P\Psi\).

Indeed, the displayed quantities are exactly the two diagonal principal
minors and determinant of \(D(L_P\Psi)\). That Jacobian is a P-matrix
throughout the rectangle, so Gale--Nikaido gives global injectivity. The
determinant identity gives the orientation and degree conclusion.

Thus a rigorous physical proof requires only interval enclosures of the
state and first transverse variational DDE. It does not require a general
boundary-intersection algorithm.

## 3. Scalar gluing and collar

Let \(X_e=X(-3,\lambda)\), which remains label-independent under the C4
patch. An interval C4-history P-matrix gate would give
\(X(t,\lambda)>X_e\) for \(t<-3\). It is then enough to validate

\[
 X_t<0\quad\hbox{on }[-3,-2]\times[-r,r],\qquad
 X<X_e\quad\hbox{on }[-2,3]\times[-r,r].
\]

Then every physical interior point lies below \(X=X_e\), every history
interior point lies above it, and the seam map
\(\Psi(-3,\lambda)=(X_e,Y_e+\lambda)\) is injective. Together with the two
P-matrix results this proves injectivity of the entire retained chart.

If the C4-history, physical and cross-separation inequalities all hold on a
larger closed time--label rectangle, including a strictly larger label radius,
its interior is an open embedding collar containing the retained rectangle
compactly. The recursive time and mixed compatibility jets are supplied by
the pinned exact C4 seam certificate. The combined interval chart-and-seam
gate nevertheless remains open.

## 4. True-variational binary64 evidence

The executable calculation integrates the state DDE from the C4 history and
integrates \(v=u_\lambda\) from its analytic derivative above. It differentiates
every current and delayed slot of the physical RFDE. Neighboring labels appear
only in a separately reported centered-difference diagnostic.

At 1201 times and all 41 labels, binary64 DOP853 gives

\[
\begin{aligned}
 \min(-7,2)u_t&=0.26089427467961634,\\
 \min(3,1)u_\lambda&=1,\\
 \min\det D(L_P\Psi)&=1.492347672442828,\\
 \det D\Psi&\in[-3.3610913993282585,-0.11479597480329445].
\end{aligned}
\]

The maximum change between variational integrations with maximum steps
\(0.02\) and \(0.01\) is \(5.91\times10^{-12}\). The discrepancy from the
centered-label diagnostic is \(6.22\times10^{-6}\).

For the scalar gluing gate, the sampled maximum of \(X_t\) on
\([-3,-2]\times[-r,r]\) is \(-0.45\), and

\[
 X_e-\max_{[-2,3]\times[-r,r]}X=0.46123287595913043.
\]

These margins support feasibility but are not outward-rounded bounds.

## 5. Interval acceptance schema

The source supplies a strict rectangular-cell schema. Each physical cell
must carry positive outward-rounded lower bounds for exactly the three
P-matrix quantities. The checker rejects zero margins, holes, duplicates,
nonfinite endpoints, and inexact grid coverage.

This is only an acceptance layer: it does not establish the provenance of
external enclosures. The committed record has both history and physical
interval-cell counts equal to zero. It leaves both interval covers, cross
separation, open collar, global embedding, degree, combined chart/seam
compatibility, and target-graph flags false.

A state-plus-variation Taylor-model method of steps can close the remaining
gate, but a validated interval ODE method of steps with controlled wrapping
would also suffice.

## 6. Reproduction

Run \(\texttt{PYTHONPATH=src /usr/bin/python3
experiments/fixed_epsilon_target_chart_univalence_gate.py}\).
