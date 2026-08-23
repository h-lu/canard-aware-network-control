# Canard-conditioned amplitude--pulse control

Status: **the linear-algebra and differential conditioning theorems below
are proved; their delayed-network application is conditional on Paper III.**
The result explains why a nonzero pointwise determinant is not enough to
claim robust independent control of frequency, amplitude, and pulse safety
inside a canard-explosion window.

## 1. Frozen physical outputs

Fix the input and output units before taking a condition number.  Let
\(u\in\mathbb R^m\) be the actuator vector and consider

\[
 \mathcal Q_\varepsilon(u)
 =\bigl(F_\varepsilon(u),A_\varepsilon(u),S_\varepsilon(u)\bigr).
 \tag{1.1}
\]

Here \(F_\varepsilon\) is frequency, \(A_\varepsilon\) is a declared
observable amplitude, and \(S_\varepsilon\) is the signed physical
pulse-channel margin.  The last coordinate is legitimate only after the
physical complete-history canard and pulse/quiet separator have been proved.
A preparation-indexed local root cannot be substituted for it.

Assume that on an operating box the amplitude has a canard-layer
representation

\[
 A_\varepsilon(u)
 =\mathscr A\left(
    \frac{S_\varepsilon(u)}{w_\varepsilon}\right)
  +R_\varepsilon(u),
 \tag{1.2}
\]

where \(w_\varepsilon>0\) is the frozen explosion width in the chosen
physical units.  At one operating point, put

\[
 f=D_uF_\varepsilon,\qquad
 a=D_uA_\varepsilon,\qquad
 s=D_uS_\varepsilon.
 \tag{1.3}
\]

Then

\[
 a=c_\varepsilon s+r_\varepsilon,\qquad
 c_\varepsilon
 =\frac{\mathscr A'(S_\varepsilon/w_\varepsilon)}
        {w_\varepsilon},
 \qquad
 r_\varepsilon=D_uR_\varepsilon.
 \tag{1.4}
\]

The decomposition is exact under (1.2).  It separates threshold translation
from actuator effects that change the pulse shape at fixed safety margin.

## 2. A universal row-cancellation bound

Let \(M\in\mathbb R^{3\times m}\), \(m\ge3\), have rows \(f,a,s\).  To
avoid the nullspace ambiguity for a wide matrix, define its row-surjectivity
modulus by

\[
 \sigma_{\rm sur}(M)
 :=\inf_{\|y\|_2=1}\|M^\top y\|_2
 =\lambda_{\min}(MM^\top)^{1/2}.
 \tag{2.0}
\]

It is positive exactly when \(M:\mathbb R^m\to\mathbb R^3\) has full row
rank.  For a square matrix it is the usual smallest singular value.

### Theorem 2.1 (conditioning bound)

For every scalar \(c\),

\[
 \boxed{
 \sigma_{\rm sur}(M)
 \le\frac{\|a-cs\|_2}{\sqrt{1+c^2}}.}
 \tag{2.1}
\]

If \(m=3\), then additionally

\[
 \det\begin{pmatrix}f\\a\\s\end{pmatrix}
 =\det\begin{pmatrix}f\\a-cs\\s\end{pmatrix}.
 \tag{2.2}
\]

#### Proof

Take

\[
 y=\frac{(0,1,-c)^\top}{\sqrt{1+c^2}}.
\]

Then \(\|y\|_2=1\) and

\[
 y^\top M=\frac{a-cs}{\sqrt{1+c^2}}.
\]

The definition (2.0) proves (2.1).
Equation (2.2) is invariance of the determinant under a row shear.
\(\square\)

### Corollary 2.2 (exponential canard conditioning)

Suppose there are constants
\(\varepsilon_0,a_*,C_R,C,\Lambda>0\), independent of \(\varepsilon\), and
a family of operating boxes on which, for every
\(0<\varepsilon\le\varepsilon_0\),

\[
 |\mathscr A'(S_\varepsilon/w_\varepsilon)|\ge a_*>0,
 \qquad
 \|D_uR_\varepsilon\|_2\le C_R.
 \tag{2.3}
\]

Then

\[
 \sigma_{\rm sur}(D_u\mathcal Q_\varepsilon)
 \le
 \frac{C_Rw_\varepsilon}
      {\sqrt{w_\varepsilon^2+a_*^2}}
 \le\frac{C_R}{a_*}w_\varepsilon.
 \tag{2.4}
\]

If \(w_\varepsilon\le Ce^{-\Lambda/\varepsilon}\), every linear right
inverse \(\mathcal R_\varepsilon:\mathbb R^3\to\mathbb R^m\),
\(D_u\mathcal Q_\varepsilon\mathcal R_\varepsilon=I_3\), satisfies, in the
induced Euclidean norm,

\[
 \|\mathcal R_\varepsilon\|
 \ge \frac{a_*}{C_RC}e^{\Lambda/\varepsilon},
 \tag{2.5}
\]

whenever \(C_R>0\).  If \(C_R=0\), the amplitude and safety rows are exactly
dependent and the response has row rank at most two.

Indeed, a left singular vector for \(\sigma_{\rm sur}\) shows that every
solution operator of \(D_u\mathcal Q_\varepsilon x=y\) has norm at least
\(\sigma_{\rm sur}^{-1}\).  Combining this fact with (2.4) gives (2.5).

Thus an exponentially narrow canard window rules out an
\(\varepsilon\)-uniformly bounded family of linear right inverses unless a
shape response contributes on the same large scale.  Such a large response
is necessary, not sufficient: its component after the safety shear must also
be quantitatively transverse to the remaining rows.  The frequency row
cannot remove the stated obstruction, because
the cancelling left vector in Theorem 2.1 has zero frequency component.

### Corollary 2.3 (fixed output scaling)

Let \(q_A>0\) and \(\kappa_\varepsilon>0\), and use the scaled output rows

\[
 \widehat a=\frac{a}{q_A},\qquad
 \widehat s=\frac{s}{\kappa_\varepsilon}.
\]

The exact relation (1.4) becomes

\[
 \widehat a
 =\frac{\kappa_\varepsilon\mathscr A'}{q_Aw_\varepsilon}
   \widehat s+\frac{r_\varepsilon}{q_A}.
 \tag{2.6}
\]

Consequently, any scaling of the frequency row and the hypotheses of
Corollary 2.2 give

\[
 \boxed{
 \sigma_{\rm sur}(D_u\widehat{\mathcal Q}_\varepsilon)
 \le
 \frac{C_Rw_\varepsilon}
 {\sqrt{q_A^2w_\varepsilon^2+a_*^2\kappa_\varepsilon^2}}
 \le\frac{C_Rw_\varepsilon}{a_*\kappa_\varepsilon}.}
 \tag{2.7}
\]

In particular, the choice
\(\kappa_\varepsilon=\varepsilon^{3/2}\) weakens the unscaled bound by the
polynomial factor \(\varepsilon^{-3/2}\), but it remains exponentially small
when \(w_\varepsilon\le Ce^{-\Lambda/\varepsilon}\).  Scaling safety by the
canard width itself would change the conclusion because it changes the
declared output tolerance.

## 3. Rank is not conditioning

Define the shape row

\[
 r=a-cs.
 \tag{3.1}
\]

The row shear in (2.2) is invertible, so

\[
 \operatorname{rank}\begin{pmatrix}f\\a\\s\end{pmatrix}
 =
 \operatorname{rank}\begin{pmatrix}f\\r\\s\end{pmatrix}.
 \tag{3.2}
\]

Consequently:

1. regular first-order three-output controllability, or a \(C^1\) local
   right inverse, requires \(f,r,s\) to be independent;
2. a nonzero determinant may coexist with the exponentially small bound
   (2.4);
3. a heatmap of \(\det D_u\mathcal Q_\varepsilon\) is not a robustness
   certificate;
4. a quantitative positive theorem must bound the row-surjectivity modulus
   in the frozen physical units on a whole operating box.

Rank deficiency at one point alone is not a nonlinear no-go theorem.  The
conditioning statement is stronger in a different direction: it gives a
neighborhood-scale upper bound on every possible linear right inverse under
the declared amplitude-layer hypothesis.  It does not rule out pointwise
invertibility for a fixed \(\varepsilon>0\); it rules out bounded-gain robust
assignment as \(\varepsilon\to0\).

## 4. Consequences for actuator design

There are three honest outcomes.

### 4.1 Operate outside the sharp explosion layer

If \(\mathscr A'\) is small at the operating point, the large shear
coefficient \(c_\varepsilon\) disappears.  A positive inverse theorem may
then be possible, but it concerns a box outside the sharp pulse transition.

### 4.2 Add a genuine shape direction

An amplitude actuator must produce a component \(r_\varepsilon\) transverse
to both frequency and safety.  Merely translating the canard threshold
changes amplitude through the same scalar coordinate and does not create a
third robust direction.  The full RFDE periodic adjoint must be used to
evaluate this shape component.

### 4.3 Change the third physical output

A phase-fixed external-stimulus threshold can be independent of the
autonomous baseline amplitude.  It requires its own stimulus-response and
event theorem; it cannot be obtained by renaming the autonomous canard
margin.

Rescaling \(S_\varepsilon\) by \(w_\varepsilon^{-1}\) can improve a numerical
condition number, but it changes the output units and the physical error
tolerance.  Such a rescaling is not evidence that the unscaled biological
control problem is well conditioned.

## 5. Positive inverse gate

For a constructive theorem outside the no-go regime, fix positive invertible
diagonal input and output scale matrices \(D_{\rm in},D_{\rm out}\), set

\[
 \widehat u=D_{\rm in}u,\qquad
 \widehat{\mathcal Q}(\widehat u)
 =D_{\rm out}\bigl(\mathcal Q(D_{\rm in}^{-1}\widehat u)-\mathcal Q_0\bigr),
\]

and define

\[
 M_{\rm sc}(\widehat u)
 =D_{\rm out}\,
 D_u\mathcal Q_\varepsilon(D_{\rm in}^{-1}\widehat u)\,
 D_{\rm in}^{-1}.
 \tag{5.1}
\]

The required certificate is

\[
 \inf_{(\varepsilon,\widehat u)\in\widehat{\mathcal B}}
 \sigma_{\rm sur}(M_{\rm sc})\ge\sigma_*>0
 \tag{5.2}
\]

on a nonempty scaled-input box \(\widehat{\mathcal B}\), together with a
Lipschitz bound in the \(\widehat u\) coordinate,

\[
 \operatorname{Lip}_{\widehat{\mathcal B}}(M_{\rm sc})\le L_Q.
 \tag{5.3}
\]

A standard quantitative inverse argument may use a radius satisfying
\[
 r_{\rm inv}\le\frac{\sigma_*}{2L_Q}
\tag{5.4}
\]
when \(L_Q>0\), provided the closed input ball lies in
\(\widehat{\mathcal B}\).  If there are exactly three actuators, restriction
to that ball and
\(\|\widehat y-\widehat{\mathcal Q}(\widehat u_0)\|
\le\sigma_*r_{\rm inv}/2\) give the usual Newton contraction and a unique
solution in the ball.  If \(m>3\), one must first fix a three-dimensional
actuator slice on which the central derivative is invertible and use the
restricted derivative's lower bound in (5.2); the result is a local right
section, not an inverse on the full actuator space.  Equivalent
Newton--Kantorovich self-map conditions may be used, and \(L_Q=0\) is treated
separately.
Network-transfer, physical-outer, pulse-event, adjoint discretization, and
numerical enclosure errors must each be smaller than the response margin
used in (5.2).

## 6. Paper IV theorem alternatives

Paper IV should prove exactly one of the following.

1. **Positive inverse:** a model-specific periodic RFDE adjoint calculation,
   a physical pulse sensitivity, and (5.2)--(5.3) on a declared box.
2. **Conditioning theorem:** verify (1.2)--(2.3) with
   \(w_\varepsilon=e^{-\Lambda/\varepsilon+o(1/\varepsilon)}\), yielding
   (2.4)--(2.5).
3. **Structural rank obstruction:** prove throughout a neighborhood that
   every available actuator changes amplitude only through the safety
   coordinate, so \(r_\varepsilon\) lies in the span of the other rows and
   the rank is at most two.

The abstract result here supplies the second theorem once the amplitude
layer and physical pulse coordinate are verified.  It does not prove those
model-specific hypotheses.
