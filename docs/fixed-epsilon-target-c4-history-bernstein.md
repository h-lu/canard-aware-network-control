# Exact Bernstein positivity for the C4 incoming target chart

Status: **proved exactly at the frozen target anchor on the full retained
incoming-history rectangle.** This closes the history-side P-matrix and
global-injectivity gate. It does not enclose the physical delay flow and does
not prove injectivity of the glued history--physical chart.

## 1. The polynomial patch

Write \(r=t+3\) and \(\lambda\in[-1/20,1/20]\). On
\(-1/2\le r\le0\), the exact C4 history has the form

\[
 h_4(r,\lambda)=h_0(r,\lambda)
 +\sum_{j=1}^4\bigl(a_j(\lambda)-h_0^{(j)}(0,\lambda)\bigr)
 \frac{r^j}{j!}\chi_9(1+2r),
\]

where

\[
 \chi_9(s)=126s^5-420s^6+540s^7-315s^8+70s^9.
\]

The endpoint polynomials \(a_j\) are those of the exact recursive RFDE seam.
The frozen decimal constants are treated as rationals and
\(\rho=\sqrt5/5\). Hence both components of \(h_4\), and therefore

\[
 p_1=-X_t,\qquad p_2=Y_\lambda,\qquad
 p_3=-\det D_{(t,\lambda)}(X,Y),
\]

are bivariate polynomials over \(\mathbb Q(\sqrt5)\).

## 2. Exact Bernstein certificate

Map the patch to the unit square by

\[
 u=2r+1,qquad v=10\lambda+\frac12.
\]

For a polynomial \(p(u,v)=\sum c_{ij}u^iv^j\) of bidegree \((m,n)\), its
tensor Bernstein coefficients are

\[
 b_{k\ell}=\sum_{i\le k,\,j\le\ell}
 c_{ij}\frac{\binom{k}{i}}{\binom{m}{i}}
       \frac{\binom{\ell}{j}}{\binom{n}{j}}.
\]

The executable proof reconstructs each power polynomial from these
coefficients exactly and decides every sign in \(\mathbb Q(\sqrt5)\) by a
rational squared comparison. All coefficients pass on the original unit
box; no subdivision is required.

| quantity | bidegree | coefficients | exact coefficient lower bound |
|---|---:|---:|---:|
| \(-X_t\) | \((12,3)\) | 52 | \(>9/100\) |
| \(Y_\lambda\) | \((13,1)\) | 28 | \(>24/25\) |
| \(-\det D h_4\) | \((25,4)\) | 130 | \(>2/5\) |

For orientation only, the smallest coefficients evaluate to approximately
\(0.0952451904\), \(0.9616254490\), and \(0.4235529538\), respectively.
These decimals are not used in the proof.

Since tensor Bernstein basis functions are nonnegative and sum to one, the
three rational bounds hold everywhere on the closed patch.

## 3. Far history and global univalence

On the remaining retained history,
\(-\Theta_*\le r\le-1/2\), the Hermite correction vanishes. Directly,

\[
 -X_t=\frac12,qquad Y_\lambda=1,qquad
 -\det D_{(t,\lambda)}(X,Y)=\frac12.
\]

Thus on the entire rectangle

\[
 [-3-\Theta_*,-3]\times[-1/20,1/20]
\]

the Jacobian of the framed map

\[
 L_Hh_4,qquad L_H=\begin{pmatrix}-1&0\\0&1\end{pmatrix},
\]

is a P-matrix, with the strict rational margins

\[
 -X_t>\frac9{100},qquad Y_\lambda>\frac{24}{25},qquad
 \det D(L_Hh_4)=-\det Dh_4>\frac25.
\]

The history is C4 across \(r=-1/2\), the rectangle is convex, and the formula
extends C1 to a neighborhood of its boundary. The Gale--Nikaido theorem
therefore makes \(h_4\) one-to-one on the full retained history rectangle.
It also gives \(\det Dh_4<-2/5\), so the raw history chart has negative
orientation.

## 4. Claim boundary

This result replaces the former binary64 history sampling by an exact proof.
The physical strip still requires a validated state-plus-variational
method-of-steps enclosure. Its three P-matrix inequalities and the two
history--physical (X)-separation inequalities remain open. Consequently
the full target embedding, open collar, boundary degree, fixed graph,
selected traces, and complete-history root are not asserted here.

## 5. Reproduction

Run

```text
PYTHONPATH=src /usr/bin/python3 experiments/fixed_epsilon_target_c4_history_bernstein.py
```
