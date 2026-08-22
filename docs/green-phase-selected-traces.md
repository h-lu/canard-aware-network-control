# One-sided Green operators and canonical selected traces

Status: **the phase-normal Green calculation and the resulting canonical
planar trace theorem are proved below.  They do not, by themselves, identify
an arbitrarily chosen family of outer RFDE Fenichel manifolds with the
canonical traces.**  The latter identification needs a parameter-coherent
outer selection estimate, stated precisely in Section 8.  Thus this note
closes the tangent/normal and moving-hit parts of the selected-trace problem,
but it does not silently turn an unspecified outer selection into a uniform
`C^1_nu C^2_eta` family.

There is also an orientation correction.  In the coordinates used in
`long-delay-selected-trace-proof.md`,

\[
 \gamma _0(s)=\left(-\frac{s}{2\alpha},
                  \frac{s^2-2}{4\alpha}\right).
 \tag{1}
\]

Consequently the attracting section at `s=-S` has `X>0`, while the
repelling section at `s=S` has `X<0`.  The inequalities in equation (3) of
that note are reversed.  All statements below use the corrected sections

\[
 \Sigma^a_S:\quad Y=\frac{S^2-2}{4\alpha},\ X>0,
 \qquad
 \Sigma^r_S:\quad Y=\frac{S^2-2}{4\alpha},\ X<0.
 \tag{2}
\]

## 1. The exact tangent-normal splitting

For

\[
 q_0(X,Y)=(Y-\alpha X^2,-X)^T,
\]

linearization along (1) gives

\[
 A_0(s)=Dq_0(\gamma _0(s))
 =\begin{pmatrix}s&1\\-1&0\end{pmatrix}.
\]

Thus the inhomogeneous variational equation is

\[
 L_0\xi=f,\qquad
 L_0(U,V)=\binom{U'-sU-V}{V'+U}.
 \tag{3}
\]

Put

\[
 E(s)=e^{s^2/2},\qquad
 I(s)=\int_0^s e^{t^2/2}\,dt,
\]

and define

\[
 \tau(s)=\binom{-1}{s},\qquad
 n(s)=\binom{I(s)}{E(s)-sI(s)}.
 \tag{4}
\]

Both columns solve the homogeneous equation.  The first is the tangent
mode, since `tau=2 alpha gamma_0'`.  The second is the normal mode and has
Gaussian growth at both ends.  Direct calculation gives

\[
 \det[\tau(s),n(s)]=-E(s).
 \tag{5}
\]

Every vector has the unique decomposition

\[
 \xi(s)=a(s)\tau(s)+b(s)n(s),
 \tag{6}
\]

where

\[
\begin{aligned}
 a(s)&=E(s)^{-1}\big[-(E(s)-sI(s))U(s)+I(s)V(s)\big],\\
 b(s)&=E(s)^{-1}\big[sU(s)+V(s)\big].
\end{aligned}
 \tag{7}
\]

Variation of constants in this frame is exact:

\[
\begin{aligned}
 a'(s)&=E(s)^{-1}
  \big[-(E(s)-sI(s))f_1(s)+I(s)f_2(s)\big]=:A_f(s),\\
 b'(s)&=E(s)^{-1}\big[sf_1(s)+f_2(s)\big]=:B_f(s).
\end{aligned}
 \tag{8}
\]

The matching phase is `U(0)=0`.  Since
`tau_1(0)=-1` and `n_1(0)=0`, it is exactly

\[
 a(0)=0.
 \tag{9}
\]

Thus the phase removes the tangent kernel, not the Gaussian normal mode.
The latter must be removed by a one-sided boundary condition.

## 2. Explicit one-sided Green operators

Let `R>=1`.  On `J_a=[-R,0]`, impose the attracting, no-incoming-normal
condition `b(-R)=beta_a`; on `J_r=[0,R]`, impose the repelling,
backward-extendible condition `b(R)=beta_r`.  Together with (9), equations
(8) give

\[
\begin{aligned}
 a_a(s)&=-\int_s^0 A_f(t)\,dt,
 &b_a(s)&=\beta_a+\int_{-R}^s B_f(t)\,dt,\\
 a_r(s)&= \int_0^s A_f(t)\,dt,
 &b_r(s)&=\beta_r-\int_s^R B_f(t)\,dt.
\end{aligned}
 \tag{10}
\]

Equations (4), (6), and (10) define the Green maps
`G^a_R(f,beta_a)` and `G^r_R(f,beta_r)`.  They include the phase projection,
the one-sided normal projection, and current-state evaluation; no spectral
root count is being substituted for these maps.

For `c>=0` and an integer `m>=0`, use the pointwise tame norm

\[
 \|g\|_{E;c,m,J}
 =\sup_{s\in J}e^{-c|s|}\langle s\rangle^{-m}|g(s)|
 \tag{11}
\]

and the normalized boundary norm

\[
 |\beta|_{\partial;c,m,R}
 =e^{R^2/2-cR}\langle R\rangle^{-m}|\beta|.
 \tag{12}
\]

The Gaussian integral norm used in the gap proof is weaker than (11): for
every fixed `c_1>c` and integer `m_1`, a pointwise `E;c,m` estimate implies
a uniform `G;c_1,m_1` estimate after increasing `m` if necessary.

**Lemma 1 (uniform phase-normal Green bound).**  For every fixed `c,m`
there are `C` and an integer `d<=4`, independent of `R`, such that

\[
 \|\mathcal G_R^\sigma(f,\beta_\sigma)\|_{E;c,m+d,J_\sigma}
 \le C\left(
   \|f\|_{E;c,m,J_\sigma}
   +|\beta_\sigma|_{\partial;c,m,R}
 \right),\qquad \sigma=a,r.
 \tag{13}
\]

The same estimate holds componentwise for a fixed finite collection of
parameter derivatives.

**Proof.**  The elementary bounds

\[
 |I(s)|\le C E(s)\langle s\rangle^{-1},\qquad
 |E(s)-sI(s)|\le CE(s)
 \tag{14}
\]

follow by splitting at `|s|=1` and integrating by parts outside that
interval.  They imply

\[
 |A_f(s)|\le C|f(s)|,
 \qquad
 |B_f(s)|\le CE(s)^{-1}\langle s\rangle|f(s)|.
 \tag{15}
\]

The tangent integrals in (10) cost at most two polynomial powers after
multiplication by `tau`.  For the normal integral, the one-sided Gaussian
tail estimate

\[
 E(s)\int_{-R}^s E(t)^{-1}e^{c|t|}\langle t\rangle^{m+1}\,dt
 \le C e^{c|s|}\langle s\rangle^{m+2},\qquad -R\le s\le0,
 \tag{16a}
\]

and its reflected right-hand version

\[
 E(s)\int_s^R E(t)^{-1}e^{c|t|}\langle t\rangle^{m+1}\,dt
 \le C e^{c|s|}\langle s\rangle^{m+2},\qquad 0\le s\le R,
 \tag{16b}
\]

follow once more by splitting at `|s|=1` and one integration by parts.
Equations (14)--(16) bound the integral terms in (10).  The boundary term
is `beta n(s)`.  The function

\[
 e^{(s^2-R^2)/2+c(R-|s|)}
 \langle R\rangle^m\langle s\rangle^{-m-d}
\]

is uniformly bounded for `s` between the relevant endpoint and zero once
`d>=2`; (14) then gives the boundary part of (13).  Taking `d=4` covers
the compact middle interval without separate notation.  The formula is
linear and contains no parameter-dependent kernel, so differentiation of a
fixed finite parameter family gives the last assertion.  `square`

Two facts are worth recording.  First, using an unweighted fundamental
matrix norm would produce `e^{R^2/2}` and lose the theorem; (10) pairs that
growth with the one-sided Gaussian integral before estimating.  Second,
the phase (9) is indispensable: without it, an arbitrary multiple of
`tau` remains.

## 3. A nonlinear canonical trace theorem

This section isolates exactly what can be proved from a reduced field on a
buffered logarithmic tube.  It deliberately does not assume a full RFDE
Green operator on arbitrary off-graph histories.

First take an arbitrary scale `S>=S_0` and put

\[
 R=S+B,
 \tag{17}
\]

where `B>2 theta_1+2` is fixed.  At the end take

\[
 S=S_\delta=\sqrt{2p\log(1/\delta)}.
 \tag{17a}
\]

The constants in the hypotheses below are required to be uniform in
`S>=S_0`; in particular they are fixed before `p` is chosen.  The only
smallness condition coupling `S` and `delta` is

\[
 \delta e^{cS}\langle S\rangle^m\le\rho_*
 \tag{17b}
\]

for a fixed sufficiently small `rho_*`.  Every fixed `p` in (17a) satisfies
(17b) for all sufficiently small `delta`, without changing any tame
constant.

For each fixed `delta,S`, extend the actual
reduced field from the uncut tube to a prepared planar field
`Q^pr_{delta,nu,eta,S}` which:

1. equals the actual reduced field, with its `nu` and `eta` derivatives,
   on the **shrinking** retained tube containing
   `gamma_0([-S-1,S+1])` and every delayed backtrack needed to lift the
   segment `|s|<=S`;
2. equals `q_0` on fixed-width neighborhoods of the prepared endpoints
   `gamma_0(+-R)` and outside them (the choice
   `B>2 theta_1+2` leaves room between every depth-two backtrack and those
   endpoint neighborhoods); and
3. obeys, for `0<=i<=1`, `0<=j<=2`, the pointwise estimates used below,
   with
   constants independent of `delta,S`:

\[
\begin{aligned}
 |Q^{pr}-q_0|+|\partial_\nu Q^{pr}|
   &\le C\delta e^{c_0|s|}\langle s\rangle^{m_0},\\
 \sum_{i=0}^1\sum_{j=1}^2
 |\partial_\nu^i\partial_\eta^jQ^{pr}|
   &\le C\delta^2e^{c_0|s|}\langle s\rangle^{m_0},
\end{aligned}
 \tag{18}
\]

on a fixed-width prepared tubular neighborhood of `gamma_0(s)`.  The
actual-equality region in item 1 is only the shrinking tube
`|d|<=delta^kappa_0` from the growing-graph theorem; no fixed-width exact
graph estimate is assumed.  The corresponding state derivatives through
order three satisfy the same type of bound.  The
cutoff is independent of `nu,eta`; no derivative of `S` is taken in
this theorem.

After \(p\) is chosen, fix one preparation datum

\[
 \mathcal P=(p,B,\chi_{\rm graph},\chi_{\rm plan},
             \mathcal E_\perp,\{\mathscr H=0\}),
\tag{17c}
\]

consisting of the growing-graph cutoff profiles, the fixed-width planar
joining cutoff, one declared degree-three normal extension operator, and
the two tail level conditions. “Canonical” below means canonical relative
to this fixed datum, the phase, and the tail level set. All unadorned
objects \(Q^{\rm pr},z^\sigma,D_{\rm can},\nu_{\rm can}\) in this note are
defined relative to \(\mathcal P\). The finite-\(\delta\) root can depend
on \(\mathcal P\); Lemma 4 proves that any two admissible data with common
finite derivative bounds have the same retained gap through the algebraic
order used in the coefficient. Equivalently, one may write
\(\nu_{{\rm can},\mathcal P}\) and regard all estimates below as uniform
over that bounded admissible class. No preparation-independent exact root
is asserted.

For the final chart these parameter orders are forced, rather than chosen.
Its exact slow equation is

\[
 Y'=-X+\delta\nu,
\]

so `partial_nu Q=delta(0,1)^T+O(delta^2)`.  The redistribution parameter
first enters the transverse `Z` equation with one displayed factor
`delta`; returning through `-2 alpha delta XZ` gives

\[
 \partial_\eta Q=\delta^2\partial_\eta q_2+O(\delta^3).
\]

The fixed-tube mixed-jet theorem proves the displayed pure `delta,eta`
orders.  More importantly here, equations (33)--(35) of
`growing-tube-graph-proof.md` include the rectangular `nu-eta` jets and
make their constants uniform in the target radius with the declared
`poly(|s|)e^{c_0|s|}` growth.

There are two different frozen cutoffs and they must not be conflated.  To
obtain (18), rerun the growing-graph theorem with frozen target

\[
 \widehat S=S+B.
 \tag{18a}
\]

Its proof is unchanged because
`delta poly(S+B)e^{C(S+B)}=o(1)`.  On that graph core, make a second,
planar preparation which remains equal to the graph field on the shrinking
physical tube in item 1, transitions through the spare buffer, and equals
`q_0` near `+-R`.  In the normal `d` coordinate, extend each boundary jet
through order three by a fixed-width Taylor/Seeley extension.  Because this
extension uses the unscaled distance from `d=+-delta^kappa_0`, rather than a
cutoff of `d/delta^kappa_0`, it introduces no inverse power of `delta` in
the declared state or parameter jets.  This preparation is used only for
the one-sided BVP.
The growing-graph Taylor expansion is still taken with its own cutoff
frozen and its dummy amplitude `rho`; the moving quantity `S_delta` is
never differentiated.

The coarse bounds (18) are sufficient for the trace construction, but not
for the coefficient calculation by themselves.  The normalized gap theorem
must additionally invoke the full growing-core expansion

\[
 Q=q_0+\delta Q_1+\delta^2Q_2+R_Q,
 \qquad
 |D_u^a\partial_\nu^i\partial_\eta^jR_Q|
 \le C\delta^3\langle s\rangle^m e^{c|s|},
 \tag{18b}
\]

with the finite indices in equations (34)--(35) of the growing-graph note.
No claim below derives the whole-line coefficient from (18) alone.

At the prepared outer endpoints impose the invariant-tail conditions

\[
 \mathscr H(z^a(-R))=0,\qquad
 \mathscr H(z^r(R))=0,
 \tag{19}
\]

where `mathscr H` is the first integral of `q_0`, and impose

\[
 X^a(0)=X^r(0)=0.
 \tag{20}
\]

Condition (19) says that the left trace has a forward attracting
`q_0`-tail and the right trace has a backward-extendible repelling
`q_0`-tail.  Its linearization is precisely the no-normal condition in
(10): since

\[
 \nabla\mathscr H(\gamma_0(s))
 =\frac{\alpha e}{2}E(s)^{-1}(s,1)^T,
\]

the normalized differential of (19) is `sU+V=E(s)b(s)`.

**Theorem 2 (canonical one-sided traces).**  Under (18), for all sufficiently
small `delta` the two boundary-value problems (19)--(20) have unique
solutions in a tame neighborhood of `gamma_0` on their respective
one-sided intervals.  They have all rectangular mixed jets
`C^1_nu C^2_eta`, and for
some fixed `c,m,C`, independent of `delta`,

\[
\begin{aligned}
 \|z^\sigma-\gamma_0\|_{E;c,m,J_\sigma}&\le C\delta,\\
 \|\partial_\nu z^\sigma\|_{E;c,m,J_\sigma}&\le C\delta,\\
 \|\partial_\eta z^\sigma\|_{E;c,m,J_\sigma}
 +\|\partial_{\eta\eta}z^\sigma\|_{E;c,m,J_\sigma}
 &\le C\delta^2,
\end{aligned}
 \tag{21}
\]

for `sigma=a,r`.  The mixed jets containing an `eta` derivative satisfy

\[
 \|\partial_\nu\partial_\eta z^\sigma\|_{E;c,m,J_\sigma}
 +\|\partial_\nu\partial_{\eta\eta}z^\sigma\|_{E;c,m,J_\sigma}
 \le C\delta^2.
 \tag{21a}
\]

In addition,

\[
 \||\partial_\eta z^\sigma|^2\|_{G;c_1,m_1,J_\sigma}
 \le C\delta^4\le C\delta^2.
 \tag{22}
\]

Thus (21)--(22) imply (T1), with a stronger bound for its quadratic term.

**Proof.**  Write `z=gamma_0+xi`.  Subtracting the equation for `gamma_0`
from the prepared equation gives

\[
 L_0\xi
 =N_{\delta,\nu,\eta}(s,\xi),
 \tag{23}
\]

where (18) and the quadratic nature of `q_0` give, on the tubular
neighborhood,

\[
\begin{aligned}
 |N(s,0)|&\le C\delta e^{c_0|s|}\langle s\rangle^{m_0},\\
 |D_\xi N(s,\xi)|&\le
 C\left(\delta e^{c_0|s|}\langle s\rangle^{m_0}+|\xi|\right).
\end{aligned}
 \tag{24}
\]

The nonlinear boundary equation (19), divided by its nonzero normalized
normal derivative, has the form

\[
 b(\mp R)=\mathcal B_{a/r}(a(\mp R)),
 \qquad
 \mathcal B_{a/r}(0)=D\mathcal B_{a/r}(0)=0,
 \tag{25}
\]

with polynomially tame second and third derivatives.  In fact this boundary
equation can be read off without an abstract manifold theorem.  At an
endpoint with phase coordinate `s`, the identity `mathscr H=0` is exactly

\[
 sU+V=\alpha U^2.
\]

Using (6)--(7), it becomes

\[
 E(s)b=\alpha[-a+I(s)b]^2.
 \tag{25a}
\]

The derivative of the left side minus the right side with respect to `b`
at `(a,b)=(0,0)` is `E(s)>0`.  The implicit-function theorem gives (25),
and (14) gives its tame derivative bounds uniformly in the normalized
boundary norm (12).  Thus (25) is the local graph of the level curve
`mathscr H=0`, with no unproved stable-manifold assertion hidden in the
boundary condition.

Here is the weighted-space seam in the contraction argument. Let \(d_0\)
be the fixed loss in Lemma 1, choose \(c>c_0\) and
\(M>m_0+d_0+2\), and put

\[
\begin{aligned}
 \|\xi\|_{\mathcal X}
 &=\sup_{s\in J_\sigma}
   e^{-c|s|}\langle s\rangle^{-M}|\xi(s)|,\\
 \|f\|_{\mathcal Y}
 &=\sup_{s\in J_\sigma}
   e^{-c|s|}\langle s\rangle^{-(M-d_0)}|f(s)|.
\end{aligned}
\tag{25b}
\]

Lemma 1 is precisely a uniform map
\(\mathcal G_R^\sigma:\mathcal Y\to\mathcal X\), including its normalized
boundary coordinate. On the ball
\(\|\xi\|_{\mathcal X},\|\widetilde\xi\|_{\mathcal X}\le C_0\delta\),
(24) gives

\[
\begin{aligned}
 \|N(\cdot,\xi)\|_{\mathcal Y}
 &\le C\delta+C\delta^2\Lambda_R,\\
 \|N(\cdot,\xi)-N(\cdot,\widetilde\xi)\|_{\mathcal Y}
 &\le C\delta\Lambda_R
       \|\xi-\widetilde\xi\|_{\mathcal X},
\end{aligned}
\tag{25c}
\]

where, after harmlessly increasing its fixed polynomial exponent,

\[
 \Lambda_R=e^{cR}\langle R\rangle^{M+m_0+d_0}.
\tag{25d}
\]

For example, the quadratic term pays
\[
 e^{-c|s|}\langle s\rangle^{-(M-d_0)}
 |\xi(s)|\,|\xi(s)-\widetilde\xi(s)|
 \le C\delta e^{cR}\langle R\rangle^{M+d_0}
 \|\xi-\widetilde\xi\|_{\mathcal X}.
\]
The linear perturbation in (24) is bounded in the same way, with at most
the larger polynomial exponent already included in (25d).

The boundary map has the identical small factor. Equation (25a) and the
implicit-function theorem give
\[
 |\mathcal B(a)|\le CE(R)^{-1}|a|^2,\qquad
 |\mathcal B(a)-\mathcal B(\widetilde a)|
 \le CE(R)^{-1}(|a|+|\widetilde a|)|a-\widetilde a|.
\]
After multiplication by the normalized boundary weight (12), these are
bounded by \(C\delta^2\Lambda_R\) and
\(C\delta\Lambda_R\|\xi-\widetilde\xi\|_{\mathcal X}\), respectively.
This explicitly accounts for the polynomial loss in Lemma 1; no
same-weight estimate is being assumed.

Insert (23) and (25) into (10). Lemma 1 now defines a self-map of the ball

\[
 \|\xi\|_{\mathcal X}\le C_0\delta
 \tag{26}
\]

The estimates (25c) and their boundary analogues show directly that its
nonuniform Lipschitz factor is

\[
 \rho_{\delta,S}=\delta\Lambda_R,
 \tag{27}
\]

which is at most the fixed small number in (17b), after changing its
constants by the fixed buffer \(B\). Hence the map is a strict contraction
for small \(\delta\), uniformly in \(\nu,\eta\). This proves
existence and uniqueness.

Differentiate the fixed-point equation.  The inverse of its linearization
has norm at most `(1-kappa)^{-1}`, uniformly.  From (18), the `nu` source is
`O(delta)`, while the `eta` source is `O(delta^2)`.  A second `eta`
derivative has the form

\[
 (I-\mathcal K)\xi_{\eta\eta}
 =F_{\eta\eta}+2D_\xi F_\eta\xi_\eta
   +D_\xi^2F[\xi_\eta,\xi_\eta],
 \tag{28}
\]

including the analogous differentiated boundary terms.  The first term is
`O(delta^2)`, the second is `O(delta^4)` after (21), and the last is
`O(delta^4)` with at most the vanishing factor (27).  Lemma 1 therefore
gives all three estimates in (21).  Applying one additional `nu`
derivative to the two `eta` equations gives (21a): by (18), every source
which contains an `eta` derivative remains `O(delta^2)`, while every other
product contains an already controlled lower jet.  The pointwise estimate for
`partial_eta z`, multiplied by the Gaussian, gives (22).  `square`

The proof is a finite-scale proof.  It differentiates only the declared
`nu,eta` variables and uses a fixed finite list of state derivatives.  The
same exponent `c` and polynomial order `m` work for the whole list; no
derivative-dependent loss is hidden in (21).

## 4. Moving hitting times and endpoint coordinates

From now on specialize `S` by (17a).  The canonical BVP endpoints `+-R`
are preparation devices, not the
transition sections.  Define `t_a<0<t_r` by the corrected hitting
conditions (2).  The next statement proves the moving-time part of Lemma T.

**Lemma 3 (unique hits and tame hit jets).**  Under Theorem 2, each
canonical trace crosses its section in (2) exactly once on its whole
one-sided interval, and the hit lies in

\[
 |t_a+S_\delta|<1,
 \qquad |t_r-S_\delta|<1,
\]

and

\[
\begin{aligned}
 |t_a+S_\delta|+|t_r-S_\delta|
 &\le C\delta e^{cS_\delta}\langle S_\delta\rangle^m,\\
 |\partial_\nu t_{a/r}|
 &\le C\delta e^{cS_\delta}\langle S_\delta\rangle^m,\\
 |\partial_\eta t_{a/r}|+|\partial_{\eta\eta}t_{a/r}|
 &\le C\delta^2 e^{cS_\delta}\langle S_\delta\rangle^m.
\end{aligned}
 \tag{29}
\]

The mixed hit jets `partial_nu partial_eta t` and
`partial_nu partial_etaeta t` obey the last bound in (29) as well.

At either hit, put

\[
 x_1=-\frac{\alpha X}{\sqrt{\alpha Y}}.
 \tag{30}
\]

Then `x_1` and the same finite list of total parameter derivatives are
bounded by `C e^{cS_delta}<S_delta>^m`.  In particular they satisfy (T2)
with one fixed algebraic loss `delta^{-M}` (indeed any fixed `M>0` works
after decreasing `delta_0`).

**Proof.**  On the singular trace,

\[
 \frac d{ds}Y_0(s)=\frac{s}{2\alpha}.
\]

On the two unit neighborhoods of `+-S_delta`, equations (18) and (21) show
that the perturbed derivative has the same sign and magnitude at least
`S_delta/(4 alpha)` for small `delta`.  The intermediate-value theorem and
strict monotonicity give the local unique hits.  On the remainder of each
outer part (`[-R,-1]` on the left and `[1,R]` on the right),
`X` retains the sign of (1), so `Y'=-X+O(delta)` retains its strict sign.
On the compact inner pieces, `Y=O(1)` while the section height tends to
infinity.  There can therefore be no second hit.  The first line of (29)
follows from the mean-value theorem.  For a parameter `lambda`,

\[
 \partial_\lambda t
 =-\frac{\partial_\lambda Y(t)}{Y'(t)},
 \tag{31}
\]

and

\[
 \partial_{\eta\eta}t
 =-\frac{Y_{\eta\eta}+2Y_{s\eta}t_\eta
                   +Y_{ss}t_\eta^2}{Y_s}\bigg|_{s=t}.
 \tag{32}
\]

Equations (18), (21), (21a), and the lower bound on `|Y_s|` prove the
remaining lines of (29) and its mixed-jet assertion, with room to absorb
inverse powers of `S_delta`.

At a hit, `alpha Y=(S_delta^2-2)/4`, so (30) has a denominator comparable
to `S_delta`.  The chain rule, (21), and (29) give the asserted bounds.
Finally

\[
 e^{cS_\delta}\langle S_\delta\rangle^m
 =o(\delta^{-M})
\]

for every fixed `M>0`, which is the advertised algebraic form.  `square`

## 5. Preparation independence at the matching section

The canonical construction is local in the following quantitative sense.

**Lemma 4 (Gaussian insensitivity to a tame outer boundary).**  Replace
one of the no-normal boundary conditions in (19) by a boundary current-state
error whose declared parameter jets are at most
`A e^{cR}<R>^m`.  After imposing the same phase, its contribution at
`s=0`, and in every Gaussian norm on the retained trace, is bounded by

\[
 CAe^{-R^2/2+cR}\langle R\rangle^{m+2}.
 \tag{33}
\]

The same conclusion holds for the difference of two preparations which
agree on the retained tube and have tame boundary mismatch.

**Proof.**  By (7), a current-state boundary error of the stated size has
normal coefficient

\[
 |\beta|\le CAe^{-R^2/2+cR}\langle R\rangle^{m+1}.
\]

At `s=0`, `n(0)=(0,1)^T`, while the phase makes the tangent coefficient
zero.  Formula (10), Lemma 1, and a contraction resolvent factor
`(1-kappa)^{-1}` give (33).  If two preparations differ throughout the
outer annulus, subtract their equations.  The difference forcing `g` is
supported outside the retained interval.  For a central left point,
the tangent integral `-integral_s^0 A_g` in (10) is therefore zero, while
the normal coefficient contains

\[
 \int_{-R}^{-S}E(t)^{-1}[tg_1(t)+g_2(t)]\,dt
 =O\left(e^{-S^2/2+cS}\langle S\rangle^{m+2}\right).
\]

The reflected argument applies on the right.  The nonlinear difference is
absorbed by the same uniform contraction resolvent.  Parameter
differentiation has the identical support and one-sided structure, proving
the preparation statement as well.  `square`

For `R=S_delta+B`, (33) is

\[
 O\left(\delta^p e^{cS_\delta}
                \langle S_\delta\rangle^{m+2}\right).
 \tag{34}
\]

Choosing `p` after the finite tame loss makes this smaller than any required
algebraic remainder.  This is the precise statement behind “the Gaussian
removes the outer choice”; it is valid only after the outer boundary jets
have a tame bound.

## 6. Lift to the exact RFDE history graph

First verify that the preparation has not changed the retained trace.  In
the canard coordinates of the growing-graph theorem,

\[
 d(X,Y)=Y-\alpha X^2+\frac1{2\alpha},
\]

and, exactly,

\[
 d(\gamma_0(s)+(U,V))=V+sU-\alpha U^2.
 \tag{34a}
\]

Hence (21), on the retained segment and its fixed-time flow hull, gives

\[
 |d|\le C\delta e^{cS}\langle S\rangle^{m+1}
       =o(\delta^{\kappa_0})
 \tag{34b}
\]

for the fixed `kappa_0<1` in the growing-graph construction.  Its nested
tube estimates give the same inclusion for every depth-two backtrack.
Thus a posteriori the canonical trace never uses the artificial normal
extension on the retained interval: there the prepared and exact reduced
fields coincide.

Suppose the growing-tube special-flow construction supplies an injective
history embedding

\[
 \iota_{\delta,\nu,\eta}(u)(\vartheta)
 =\left(\Phi_Q^\vartheta u,
        H_{\delta,\eta}(\Phi_Q^\vartheta u)\right),
 \qquad -\theta_1\le\vartheta\le0,
 \tag{35}
\]

in the chart variables (with the evident grouping of the two critical and
two stable components).  Use the rerun with target `widehat S=S+B` from
(18a), and assume the retained canonical pieces and all backtracks in (35)
lie in its uncut flow hull.  Then, only on the retained intervals

\[
 I_a=[t_a,0],\qquad I_r=[0,t_r],
\]

one has

\[
 \phi^\sigma(s)=\iota_{\delta,\eta}(z^\sigma(s))
 \tag{36}
\]

and these are exact complete-history solutions of the final RFDE.  The
prepared portions between `+-S` and `+-R` are auxiliary planar tails and
are **not** asserted to solve the physical RFDE.  The retained right trace
is backward-extendible inside the history graph because (36) is built from
a complete finite-dimensional special flow; no backward inversion of the
ambient RFDE semiflow is used.

For a source tangent to a fixed history graph, the one-sided history
solution operator is

\[
 \mathbf G^\sigma_\delta f
 =D\iota_{\delta,\nu,\eta}(z^\sigma)
    \mathcal G^\sigma_Rf.
 \tag{37}
\]

For an actual parameter derivative the embedding itself also changes.  The
complete-history jet is, exactly,

\[
 \partial_\lambda\phi^\sigma
 =D\iota_{\delta,\nu,\eta}(z^\sigma)
    \partial_\lambda z^\sigma
  +\partial_\lambda\iota_{\delta,\nu,\eta}(z^\sigma),
 \qquad \lambda\in\{\nu,\eta\},
 \tag{37a}
\]

with the ordinary Faà di Bruno terms at higher mixed order.  The growing
mixed-graph theorem controls the second term with the same
`poly(|s|)e^{c|s|}` loss.  Thus (37) is linear only for a graph-tangent
source; (37a), not (37) alone, is the parameter-trace formula.

It includes history-to-current-state evaluation because evaluation at zero
followed by critical projection is the identity on `u`.  The mixed graph
and delayed-flow estimates multiply (13) by at most
`poly(|s|)e^{c|s|}`, which is exactly the allowed tame loss.

Equation (37), restricted to the retained intervals, is the curve-wise
operator needed for selected traces.  It is
not a right inverse for arbitrary off-graph forcing in the whole Banach
space `C([-theta_1,0],R^4)`, and no such stronger assertion is needed for
the canonical trace derivatives.  Thus the phase-space root count is not
being used to infer an ambient dichotomy.

## 7. Central gap, history equality, and the baseline root

Define the canonical central gap by

\[
 D_{\rm can}(\delta,\nu,\eta)
 =\frac{2}{\alpha e}
  \left[\mathscr H(z^a(0))-\mathscr H(z^r(0))\right].
 \tag{38}
\]

**Lemma 5 (the scalar gap is the complete-history intersection gap).**
For all sufficiently small `delta`,

\[
 D_{\rm can}=0
 \quad\Longleftrightarrow\quad
 z^a(0)=z^r(0)
 \quad\Longleftrightarrow\quad
 \iota_{\delta,\nu,\eta}(z^a(0))
 =\iota_{\delta,\nu,\eta}(z^r(0)).
 \tag{39}
\]

**Proof.**  Both phase-fixed points have `X=0`.  On that section put
`h(Y)=mathscr H(0,Y)`.  At the singular match
`Y_0=-1/(2 alpha)`,

\[
 h'(Y_0)=\frac{\alpha e}{2}\ne0.
\]

Theorem 2 puts both central values in a common neighborhood on which `h`
is injective.  Hence equality of the two `mathscr H` values is equivalent
to equality of their `Y` values, and therefore of the two current reduced
states.  The history embedding is injective because present-time
evaluation followed by critical projection returns `u`; this proves the
last equivalence.  `square`

The leading gap is also fixed rather than assumed.

**Lemma 6 (canonical baseline gap).**  Assume the full growing-core
expansion (18b) and choose `p` after its uniform tame exponents.  Then

\[
 \boxed{
 \frac{D_{\rm can}(\delta,\nu,\eta)}{\delta}
 =\sqrt{2\pi}\left(\nu+\frac{11}{24\alpha}\right)
  +O(\delta).}
 \tag{40}
\]

The error is uniform for `nu,eta` in their fixed compact boxes.

**Proof.**  The prepared endpoint conditions (19) make both outer
`mathscr H` values zero.  Integrating `d mathscr H/ds` on the two prepared
traces therefore gives the exact analogue of the two-piece identity in the
normalized-gap note.  On the retained core, (18b) and the Gaussian Green
bounds permit replacement of each trace by `gamma_0` at cost `O(delta)`
after division by `delta`.  On the prepared parts outside `|s|<=S`, (18)
and the Gaussian factor give

\[
 O\left(e^{-S^2/2+cS}\langle S\rangle^m\right)
 =O(\delta^{p-\kappa})
\]

after the same division, for every fixed `kappa>0`.  Choose `p` so this is
`O(delta)`.  The `delta^2Q_2` and higher terms contribute `O(delta)`.

The actual first graph coefficient on the singular connection is

\[
 Q_{1,X}(\gamma_0(s),\nu)
 =\frac{11s^3-12K(\theta_0+2\theta_1)}{72\alpha},
 \qquad Q_{1,Y}(\gamma_0(s),\nu)=\nu.
 \tag{41}
\]

Using the normalized adjoint
`psi=e^{-s^2/2}(s,1)^T`, the constant delay term in (41) is odd and
integrates to zero, while

\[
 \int_{\mathbb R}e^{-s^2/2}\,ds=\sqrt{2\pi},\qquad
 \int_{\mathbb R}s^4e^{-s^2/2}\,ds=3\sqrt{2\pi}.
\]

The resulting whole-line pairing is exactly the leading term in (40).
`square`

In particular, the leading canonical root is

\[
 \nu_0=-\frac{11}{24\alpha},\qquad
 \partial_\nu(D_{\rm can}/\delta)
 =\sqrt{2\pi}+O(\delta),
 \tag{42}
\]

so it is simple.  Lemmas 5--6 supply the gap-equivalence and baseline inputs
which are separate from the eta-derivative calculation.  Combining them
with the trace-to-gap theorem gives the canonical local root shift; it does
not identify an arbitrary physical outer selection.

**Corollary 7 (canonical local history-connection root).**  Under the
canonical preparation, (18b), the uncut lift of Section 6, and the final
coefficient identity

\[
 \partial_\eta Q_{2,X}(\gamma_0(s),\nu,0)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha}s,
\]

there is a unique root `nu_can(delta,eta)` near `nu_0` for sufficiently
small `delta,eta`, and

\[
 \boxed{
 \nu_{\rm can}(\delta,\eta)-\nu_{\rm can}(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\,\delta\eta
 +O(\delta^2|\eta|+\delta\eta^2).}
 \tag{43}
\]

Equivalently, for `mu=delta^2 nu`,

\[
 \boxed{
 \mu_{\rm can}(\delta,\eta)-\mu_{\rm can}(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\,\delta^3\eta
 +O(\delta^4|\eta|+\delta^3\eta^2).}
 \tag{44}
\]

At this root the two retained complete histories in (36) are equal by
Lemma 5.  This is a theorem about the explicitly prepared **canonical local
history connection**.  It is not a theorem about the earlier arbitrary
outer Fenichel selections and is not labelled a physical maximal canard.

**Proof.**  The trace-to-gap calculation, now applied to Theorem 2 and
(18b), gives

\[
\begin{aligned}
 \partial_\nu D_{\rm can}
  &=\delta\sqrt{2\pi}+O(\delta^2),\\
 \partial_\eta D_{\rm can}
  &=-\frac{K(\theta_0-\theta_1)}{4\alpha}
    \sqrt{2\pi}\,\delta^2
    +O(\delta^3+\delta^2|\eta|),\\
 \partial_{\eta\eta}D_{\rm can}&=O(\delta^2).
\end{aligned}
\]

Lemma 6 and the implicit-function theorem give the unique root.  Implicit
differentiation, followed by integration from zero to `eta`, gives (43);
multiplication by `delta^2` gives (44).  `square`

## 8. What is now proved for a canonical local selection

Combining Theorem 2, Lemma 3, and the lift (35)--(37) proves the
tangent/normal, moving-hit, and `C^1_nu C^2_eta` portions of Lemma T for the
following explicitly defined object:

> the attracting forward and repelling backward-extendible traces selected
> by the invariant prepared tails `mathscr H=0`, the one matching phase
> `X(0)=0`, and the uncut exact RFDE history graph.

Under the pointwise growing-graph bounds (18), these canonical traces obey
(T0)--(T2), after correcting the section orientations in (2).  The constants
are independent of `delta`; their only endpoint loss is
`poly(S_delta)e^{cS_delta}`, hence one fixed algebraic power is more than
enough.  The Gaussian mode has not been discarded: it is removed by the
one-sided boundary projection and is explicitly visible in (10), (12), and
(33).

This gives a short theorem route if the paper defines its threshold by this
canonical local history selection.  It does not prove that a previously
unspecified physical outer Fenichel selection is that same object.  In
particular, if an outer RFDE selection does not already lie on the same
special-flow graph, Lemma 4's planar current-state comparison is
insufficient: a full-history overlap or stable-fiber estimate is required
before (36) can be applied to it.

## 9. Exact obstruction for arbitrary “fixed outer selections”

As currently written, the phrase “fix the attracting and repelling outer
slow-history selections” does not specify a parameter-coherent family.  A
uniform mixed-jet conclusion cannot follow from that phrase.

**Proposition 5 (selection coherence is necessary).**  Suppose that, for
each fixed positive `delta`, an outer Fenichel manifold may be chosen from
an exponentially close nonunique family, with no joint regularity condition
on the choice as a function of `(delta,eta)`.  Then no constants `C,M`
can be deduced for its `eta` derivatives in (T1)--(T2).

**Proof.**  Let `d_delta>0` denote any admissible exponentially small
change of a selected outer slice along its nonunique fiber.  Modulate that
change by

\[
 d_\delta\sin(\eta\omega_\delta),
\]

where `omega_delta` is arbitrary.  For every fixed `delta` this is a smooth
choice and it never leaves the admissible `d_delta` neighborhood.  Its
first derivative at zero is `d_delta omega_delta`.  Choosing
`omega_delta>d_delta^{-1}e^{1/delta}` violates every fixed algebraic or
`e^{cS_delta}` bound.  The same construction with a higher frequency
violates the second derivative bound.  `square`

This is a logical obstruction, not a claim that a canonical Lyapunov--Perron
selection has bad derivatives.  It shows that one of the following must be
put into the theorem statement:

1. use the canonical local selection of Section 8; or
2. define the physical outer manifolds by a parameter-coherent
   Lyapunov--Perron construction and prove that their normalized boundary
   residual and its `C^1_nu C^2_eta` jets are
   `poly(S_delta)e^{cS_delta}`.

Under option 2, Lemma 4 identifies the physical and canonical matching gaps
up to (34), so the coefficient is unchanged.  Without either option,
Lemma T is not a theorem about a well-defined parameterized object.

## 10. Claim boundary

The defensible conclusions are:

- the exact one-sided Green operators, tangent phase removal, and Gaussian
  normal projection are given by (10);
- their constants are uniform on receding intervals in the tame norms of
  Lemma 1;
- a canonical prepared-tail selection has `C^1_nu C^2_eta` trace maps,
  unique moving hits, and the orders required in (T1)--(T2), provided the
  growing reduced field satisfies the explicit pointwise bounds (18);
- the later coefficient/root argument must use the stronger expansion
  (18b), not merely the coarse trace bound (18);
- those traces lift to genuine full RFDE histories on the uncut special-flow
  graph, without an ambient backward RFDE solve;
- arbitrary outer selections are not covered unless a joint selection rule
  and its tame boundary jets are proved; and
- the section signs in the previous statement of Lemma T must be corrected
  before that lemma can be cited.

Accordingly, this note supplies the Green/phase theorem for the canonical
local route.  Equations (33)--(35) and the nested flow-hull estimates in
`growing-tube-graph-proof.md` are the matching model-specific interface;
their target must be enlarged as in (18a), and (34a)--(34b) then give the
bootstrap into the exact shrinking graph.  If the paper insists on its
earlier arbitrary physical outer selections, the additional full-history
outer Lyapunov--Perron compatibility estimate in option 2 remains open.
