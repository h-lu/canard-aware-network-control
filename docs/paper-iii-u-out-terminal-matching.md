# Paper III Gate U-OUT: exact causal continuation and terminal matching

Status: **the fixed-\(\delta\) continuation-or-exit theorem, the exact
curve-restricted history identity, the scalar terminal-transfer
counterexample, and the monotone matching lemma in this note are proved.
The fixed-logarithmic-chart/action-scale no-go and the independence of the
terminal value and parameter-jet budgets are also proved in the companion
closure audit.
For the physical two-module RFDE, reset containment is conditional on the
action-supercritical boundary-value contract in Theorem 6.1.  The physical
terminal-normalized family, its exact common-leaf factorization, its
two-sided action sensitivity, and the supercritical residual estimate have
not been constructed.  Therefore Gate U-OUT remains open.**

The executable identities and logarithmic budgets are in
`src/canard_control/unforced_outer_tracker.py`; their tests are in
`tests/test_unforced_outer_tracker.py`.  The sharp scale and parameter-jet
audits are in
[paper-iii-u-out-action-scale-closure-audit.md](paper-iii-u-out-action-scale-closure-audit.md),
with executable checks in `src/canard_control/u_out_action_scale.py`.
This note neither modifies the frozen JNS manuscript nor asserts a pulse
outcome.

## 1. Model, coordinates, and quantifier order

Let

\[
 r=(1,2)^T,\quad \ell=(1/2,1/4)^T,\qquad
 q=(1,-2)^T,\quad m=(1/2,-1/4)^T,
\]

so that \(\ell^Tr=m^Tq=1\) and \(\ell^Tq=m^Tr=0\).  For the physical
two-module model write

\[
 v-v_*=r\xi+q\zeta,\qquad
 w-w_*=r\rho+q\kappa,qquad \varepsilon=\delta^2.
\tag{1.1}
\]

In fast time \(t\), the RFDE is

\[
\begin{aligned}
 \dot v={}&F(v,w)+\varepsilon K
 \left[Bv-C_0^\eta v(t-\theta_0/\delta)
           -C_1^\eta v(t-\theta_1/\delta)\right],\\
 \dot w={}&\varepsilon(v_1-\sigma-\mu,v_2-2\mu)^T
            -D_wP_\perp(w-w_*).
\end{aligned}
\tag{1.2}
\]

The direct modal calculation gives

\[
\begin{aligned}
 \dot\xi={}&-\rho-\frac56\xi^3+\frac32\xi^2\zeta
 -\frac{\sqrt6}{4}\xi^2-\frac52\xi\zeta^2
 -\frac{\sqrt6}{2}\xi\zeta
 +\frac12\zeta^3-\frac{\sqrt6}{4}\zeta^2\\
 &+\varepsilon K\left(\xi-\frac13\xi_0-\frac23\xi_1
 -\frac16\zeta+\frac1{12}\zeta_0+\frac1{12}\zeta_1\right),\\
 \dot\zeta={}&-\kappa+\frac12\xi^3-\frac52\xi^2\zeta
 -\frac{\sqrt6}{4}\xi^2+\frac32\xi\zeta^2
 -\frac{\sqrt6}{2}\xi\zeta
 -\frac56\zeta^3-\frac{\sqrt6}{4}\zeta^2-2\zeta\\
 &+\varepsilon K\left[
 -\eta\xi_0+\eta\xi_1-\eta\zeta_0+\eta\zeta_1
 +\frac16\zeta-\frac1{12}\zeta_0-\frac1{12}\zeta_1
 \right],\\
 \dot\rho={}&\varepsilon(\xi-\mu),\\
 \dot\kappa={}&-D_w\kappa+\varepsilon\zeta,
\end{aligned}
\tag{1.3}
\]

where \((\xi_k,\zeta_k)=(\xi,\zeta)(t-\theta_k/\delta)\).
In slow time \(T=\varepsilon t\), the delay lengths are exactly

\[
 h_k=\delta\theta_k,
\qquad \rho_T=Q:=\xi-\mu.
\tag{1.4}
\]

The quantifiers needed below are the following.

1. First fix \(K\ne0\), \(D_w>0\),
   \(0<\theta_0<\theta_1\), a compact control box \(U\) whose
   \(\eta\)-coordinate lies compactly in \((-1/6,1/12)\), the reset value
   \(\rho_R=-1/2\), an outgoing overlap section, a buffered physical
   middle tube, and a terminal normalization.
2. Fix the admissible preparation used in the canonical right-fold theorem.
   For every \(0<\delta\leq\delta_0\) and \(u\in U\), set
   \(\mu=\mu_c(\delta,u)\) and take the corresponding exact outgoing
   complete history \(\phi^{\rm can}_{\delta,u}\).
3. Only then seek constants uniform in \((\delta,u)\), or a
   terminal-coordinate map \(\beta_*(\delta,u)\).  Smoothness below means
   \(C^1\) in \(u\) for each fixed positive \(\delta\).  No derivative in
   \(\delta\), and no uniform mixed-jet bound, follows from ordinary RFDE
   well-posedness.

This order keeps the preparation-indexed local root distinct from an
unproved preparation-independent physical outer canard.

## 2. What exact forward continuation already gives

For fixed \(\delta\), let

\[
 X_\delta=C([ -\theta_1/\delta,0],\mathbb R^4)
\tag{2.1}
\]

or its standard \(C^1\) solution manifold when parameter differentiation
is required.  Let \(\mathscr T_{\delta,u}\subset X_\delta\) be an open,
bounded, buffered history tube around the outgoing middle branch, on whose
closure the RFDE has the uniform local bounds required for continuation.
Its buffer must contain the complete initial history and every delayed
query used before the declared exit.  Suppose throughout this tube that

\[
 -Q_{\delta}\leq \xi-\mu\leq-q_{\delta}<0.
\tag{2.2}
\]

Here \(q_\delta,Q_\delta>0\) may depend on \(\delta\); no uniform lower
bound is needed for the elementary theorem.

> **Theorem 2.1 (exact canonical continuation or tube exit).**
> Assume the physical RFDE is locally well posed on
> \(\mathscr T_{\delta,u}\), and let its initial history be the exact
> canonical outgoing history \(\phi^{\rm can}_{\delta,u}\), whose present
> recovery value \(\rho_{\rm in}\) satisfies
> \(\rho_R<\rho_{\rm in}\).  Then there is a unique forward physical
> solution until the first of the following events:
>
> 1. the solution history leaves \(\mathscr T_{\delta,u}\); or
> 2. the current recovery coordinate reaches \(\rho_R\).
>
> Before either event, \(\rho\) is strictly decreasing and the solution is
> an exact curve-restricted complete-history tracker.  If no tube exit
> occurs, the reset hit occurs no later than
>
> \[
>  t_R\leq
>  \frac{\rho_{\rm in}-\rho_R}{\delta^2q_\delta}.
> \tag{2.3}
> \]
>
> A delayed query is causal and upstream: in slow time,
>
> \[
>  0\leq \rho(T-h_k)-\rho(T)
>  \leq Q_\delta\delta\theta_k.
> \tag{2.4}
> \]
>
> If the vector field and initial canonical history are \(C^1\) in \(u\),
> and the orbit reaches \(\rho_R\) through the interior of the tube, then
> the tracker and its reset hit are \(C^1\) in \(u\) for this fixed
> \(\delta\).

**Proof.**  Local RFDE existence and forward uniqueness give the solution
up to its maximal interval in the open tube.  By (1.3) and (2.2),

\[
 \dot\rho=\delta^2(\xi-\mu)\leq-\delta^2q_\delta<0.
\tag{2.5}
\]

Thus \(\rho\) is a valid coordinate until exit.  If the orbit remains in
the tube for the right-hand side of (2.3), integration of (2.5) forces it
to reach \(\rho_R\), proving the alternative and the time bound.  In slow
time, (2.2) gives

\[
 \rho(T-h_k)-\rho(T)
 =-\int_{T-h_k}^{T}Q(s)\,ds
 \in[0,Q_\delta h_k],
\]

which is (2.4).

Let \(r=\rho(T)\), let \(T=T(r)\), and define

\[
 \mathcal K_{\delta,u}(r)=x(T(r)),\qquad
 \mathfrak I_{\delta,u}(r)(\vartheta)
 =x(T(r)+\delta\vartheta),
 \quad -\theta_1\leq\vartheta\leq0.
\tag{2.6}
\]

If \(\Phi_Q\) denotes the scalar base flow, then exactly

\[
 \mathfrak I_{\delta,u}(r)(\vartheta)
 =\mathcal K_{\delta,u}
   (\Phi_Q^{\delta\vartheta}(r)),
\tag{2.7}
\]

and the chain rule gives the physical curve-restricted parameterization
equation

\[
 D\mathcal K_{\delta,u}(r)Q_{\delta,u}(r)
 =\mathcal V_{\delta,u}(\mathfrak I_{\delta,u}(r)).
\tag{2.8}
\]

The initial member of (2.6) is the same complete history, not merely a
nearby current state, because the IVP was seeded by
\(\phi^{\rm can}_{\delta,u}\).  Standard fixed-\(\delta\) differentiable
dependence for RFDEs gives the final assertion on compact time intervals.
At reset,
\(\partial_t(\rho-\rho_R)=\delta^2(\xi-\mu)\ne0\), so the ordinary
implicit-function theorem gives differentiability of the hit time.  This
argument supplies no estimate uniform as \(\delta\downarrow0\).  \(\square\)

The theorem proves exact continuation and exact common history at the
outgoing overlap.  It does **not** prove which event occurs first.  Gate
U-OUT is precisely the missing assertion that reset wins over tube exit.

## 3. Why local exactness does not prove outer containment

On the singular middle branch, let \(n\) be the forward-unstable normal
coordinate.  Its leading propagation over a fixed slow segment has the
form

\[
 \varepsilon n_s=a(s)n,qquad a(s)>0,qquad 0\leq s\leq L,
\tag{3.1}
\]

and define the positive action

\[
 A=\int_0^L a(s)\,ds.
\tag{3.2}
\]

This ODE is itself an RFDE whose functional ignores the past.

> **Proposition 3.1 (exact terminal-transfer obstruction).**
> Prescribe \(n(0)=h\) and a terminal normalization \(n(L)=\beta\).
> Then
>
> \[
>  h=e^{-A/\varepsilon}\beta,
>  \qquad \beta=e^{A/\varepsilon}h.
> \tag{3.3}
> \]
>
> Hence a bounded terminal tube \(|\beta|\leq R\) matches the incoming
> value exactly if and only if
>
> \[
>  |h|\leq Re^{-A/\varepsilon}.
> \tag{3.4}
> \]
>
> For every fixed \(p,c>0\), neither \(h=\delta^p\) nor
> \(h=e^{-c/\delta}\) satisfies (3.4) for all small \(\delta\).  Exact
> \(h=0\) does, and
> \(h=e^{-(A+\chi)/\varepsilon}\), \(\chi>0\), gives the bounded terminal
> coordinate \(\beta=e^{-\chi/\varepsilon}\).

**Proof.**  The solution of (3.1) is

\[
 n(s)=h\exp\left(\varepsilon^{-1}
                   \int_0^s a(\sigma)\,d\sigma\right),
\]

which proves (3.3)--(3.4).  For \(h=\delta^p\),

\[
 \log|\beta|=p\log\delta+A/\delta^2\longrightarrow+\infty.
\]

For \(h=e^{-c/\delta}\),

\[
 \log|\beta|=-c/\delta+A/\delta^2\longrightarrow+\infty.
\]

The last two statements follow directly from (3.3).  \(\square\)

For the singular two-module middle branch ending at \(\rho_R=-1/2\), the
model-specific action used by the existing geometric audit is

\[
 A_R=\int_{\rho_{\rm fold}}^{\rho_R}
       \frac{\lambda_u(\rho)}{\xi^m(\rho)}\,d\rho>0.
\tag{3.5}
\]

Its numerical value is a diagnostic, not a proof of the nonlinear RFDE
transfer estimate.  Proposition 3.1 nevertheless proves that algebraic
control of the local outgoing history, or even an \(e^{-c/\delta}\)
history error, is categorically too weak for a fixed outer tube.  The
comparison must be exact or must beat the full repelling action.

## 4. Exact terminal normalization is a boundary-value problem

Let \(\Sigma_{\rm in}=\{\rho=\rho_{\rm in}\}\) be the outgoing overlap
section and \(\Sigma_R=\{\rho=\rho_R\}\).  A terminal-normalized family is
not obtained by inverting the retarded semiflow.  It must be constructed as
a finite-interval boundary-value problem, for example by a dichotomy Green
operator with:

- phase fixed by \(\rho\);
- the center-stable coordinates fixed at the incoming section by the
  chosen common-leaf normalization; and
- the one forward-unstable coordinate fixed at the terminal section, with
  \(\beta\in[-R,R]\) left free.

This is the causal two-point orientation: forward-stable data propagate
from the incoming end, while the forward-unstable coordinate is propagated
backward only inside the Green boundary-value problem.  It is not an
ambient backward RFDE initial-value solve.

Schematically, in a normal history coordinate \(n\), the required fixed
point has the form

\[
\begin{aligned}
 n(s)={}&U(s,0)P^{cs}(0)\alpha
 +\int_0^sU(s,r)P^{cs}(r)\mathcal N(r,n_r)\,dr\\
 &+U(s,L)P^u(L)\beta
 -\int_s^LU(s,r)P^u(r)\mathcal N(r,n_r)\,dr.
\end{aligned}
\tag{4.1a}
\]

The last two terms use the inverse evolution only on the finite-dimensional
unstable range.  Constructing (4.1a) for the physical long-delay normal
equation, including its history insertion operator, is part of B1 below.

Denote its exact incoming history trace by

\[
 G_{\delta,u}(\beta)\in X_\delta.
\tag{4.1}
\]

There is an infinite-dimensional compatibility issue here.  One scalar
observable cannot in general certify equality of two histories.  The
minimal exact hypothesis is a common-leaf chart: there must be a local
Banach chart

\[
 \Xi_{\delta,u}:\mathcal N\subset X_\delta
 \longrightarrow \mathbb R\times Y_{\delta,u},
 \qquad \Xi=(\pi_u,\pi_c),
\tag{4.2}
\]

such that

\[
 \pi_c\Xi_{\delta,u}(G_{\delta,u}(\beta))
 =\pi_c\Xi_{\delta,u}(\phi^{\rm can}_{\delta,u})
 \quad\text{for every }|\beta|\leq R.
\tag{4.3}
\]

Then the scalar mismatch

\[
 m_{\delta,u}(\beta)
 =\pi_u\Xi_{\delta,u}(G_{\delta,u}(\beta))
  -\pi_u\Xi_{\delta,u}(\phi^{\rm can}_{\delta,u})
\tag{4.4}
\]

satisfies the exact equivalence

\[
 m_{\delta,u}(\beta)=0
 \quad\Longleftrightarrow\quad
 G_{\delta,u}(\beta)=\phi^{\rm can}_{\delta,u}.
\tag{4.5}
\]

Condition (4.3) is the exact common-history requirement.  It cannot be
replaced by \(O(e^{-A/\varepsilon})\) closeness to a Fenichel family.

> **Lemma 4.1 (monotone exact terminal match).**
> Let \(m\in C^1([-R,R]\times U,\mathbb R)\).  Suppose, for every
> \((\beta,u)\), that \(\partial_\beta m\) has one fixed sign and
>
> \[
>  |\partial_\beta m(\beta,u)|\geq d_\delta>0,
>  \qquad |m(0,u)|\leq r_\delta<d_\delta R.
> \tag{4.6}
> \]
>
> Then for every \(u\) there is a unique
> \(\beta_*(u)\in(-R,R)\) such that \(m(\beta_*(u),u)=0\), and
>
> \[
>  |\beta_*(u)|\leq r_\delta/d_\delta.
> \tag{4.7}
> \]
>
> The map \(u\mapsto\beta_*(u)\) is \(C^1\), with
>
> \[
> D_u\beta_*(u)
> =-\frac{D_um(\beta_*(u),u)}
>         {\partial_\beta m(\beta_*(u),u)}.
> \tag{4.8}
> \]

**Proof.**  Suppose first \(\partial_\beta m\geq d_\delta\).  Then

\[
 m(-R,u)\leq r_\delta-d_\delta R<0,
 \qquad
 m(R,u)\geq-r_\delta+d_\delta R>0.
\]

The intermediate-value theorem gives a zero and strict monotonicity makes
it unique.  The mean-value theorem between zero and \(\beta_*\) yields
(4.7).  The case \(\partial_\beta m\leq-d_\delta\) is identical with the
signs reversed.  The implicit-function theorem gives (4.8).  \(\square\)

The lower derivative bound in (4.6) is essential.  An upper sensitivity
estimate alone does not give a solvable terminal correction.

## 5. The action-supercritical budget

The natural two-sided terminal sensitivity over the repelling segment is
exponentially small at the incoming section.  Allowing polynomial and
long-delay losses, the minimal useful bounds are

\[
 d_\delta\geq
 c_d\delta^{M_d}
 \exp\left(-\frac{A}{\delta^2}-\frac{L_d}{\delta}\right),
\tag{5.1}
\]

and

\[
 r_\delta\leq
 C_r\delta^{-M_r}
 \exp\left(-\frac{A+\chi}{\delta^2}+\frac{L_r}{\delta}\right),
 \qquad \chi>0.
\tag{5.2}
\]

Their exact ratio is bounded by

\[
 \frac{r_\delta}{d_\delta}
 \leq \frac{C_r}{c_d}\,
 \delta^{-(M_r+M_d)}
 \exp\left(-\frac{\chi}{\delta^2}
            +\frac{L_d+L_r}{\delta}\right)
 \longrightarrow0.
\tag{5.3}
\]

Thus a fixed positive action margin beats every fixed polynomial loss and
the combined \(e^{(L_d+L_r)/\delta}\) history loss produced by a slow
delay of length \(\delta\theta_1\).  The logarithmic calculation in the
executable audit uses (5.3) directly and does not exponentiate canard-scale
numbers until a display value is requested.

The estimate (5.1) must be proved from a differentiated physical Green
identity, not inferred from a Neumann norm alone.  If the base evolution,
projectors, or Green operator depends on \(u\), parameter differentiation
contains the corresponding \(D_uG\) terms.  A valid proof must either keep
the base Green operator fixed or establish uniform bounds for those terms.

## 6. Minimal model-specific completion theorem

The following statement is deliberately a conditional theorem.  It is the
smallest boundary-value package found here that turns the exact canonical
right-fold history into an exact reset-reaching outer tracker.

> **Theorem 6.1 (action-supercritical U-OUT completion; conditional).**
> Fix the data and quantifiers of Section 1.  Suppose there are constants
> \(R,A,\chi,c_d,C_r>0\), \(L_d,L_r,M_d,M_r\geq0\), and
> \(\delta_0>0\),
> independent of \((\delta,u)\), such that for every
> \(0<\delta\leq\delta_0\) and \(u\in U\):
>
> **B1 (physical terminal family).**  A \(C^1\) terminal-normalized
> curve-restricted boundary-value family exists for
> \(\beta\in[-R,R]\).  Every member is an exact solution of the uncut
> physical RFDE, remains in the buffered middle tube from
> \(\Sigma_{\rm in}\) to \(\Sigma_R\), and has the delay backtrack buffer
> required by (2.4).
>
> **B2 (exact trace factorization).**  Its incoming trace and the canonical
> history lie in one chart satisfying (4.2)--(4.5).  In particular, zero
> scalar mismatch is equivalent to equality of complete histories.
>
> **B3 (two-sided action sensitivity).**  The exact mismatch has one
> derivative sign, \(|\partial_\beta m|\geq d_\delta\) throughout
> \([-R,R]\times U\), and \(d_\delta\) satisfies (5.1).  This estimate
> includes all parameter dependence of the physical evolution and
> projectors.
>
> **B4 (action-supercritical residual).**  The reference terminal
> normalization has \(|m(0,u)|\leq r_\delta\), where \(r_\delta\)
> satisfies (5.2).
>
> Then, after decreasing \(\delta_0\), there is a unique terminal
> coordinate \(\beta_*(\delta,u)\in(-R,R)\), with
> \(\beta_*(\delta,\cdot)\in C^1(U)\) for each fixed \(\delta\), and
>
> \[
>  |\beta_*(\delta,u)|
>  \leq\frac{C_r}{c_d}\,
>  \delta^{-(M_r+M_d)}
>  \exp\left(-\frac{\chi}{\delta^2}
>             +\frac{L_d+L_r}{\delta}\right).
> \tag{6.1}
> \]
>
> The corresponding terminal trace equals
> \(\phi^{\rm can}_{\delta,u}\) as a complete history.  By forward RFDE
> uniqueness, it is exactly the canonical forward orbit.  It stays inside
> the declared middle tube and reaches \(\rho_R=-1/2\).  Consequently it
> supplies a parameter-coherent selected outer history tracker.

**Proof.**  Equation (5.3) is less than \(R\) for all sufficiently small
\(\delta\).  Lemma 4.1 applied with (5.1)--(5.2) gives the unique root and
(6.1).  By B2, its incoming history is exactly the canonical outgoing
history.  B1 gives an exact in-tube RFDE solution reaching the reset
section.  Forward uniqueness identifies that solution with the canonical
IVP of Theorem 2.1.  Fixed-\(\delta\) \(C^1\) dependence follows from
Lemma 4.1.  \(\square\)

The exact-normalization special case is \(m_{\delta,u}(0)=0\): then
\(\beta_*=0\) without any residual estimate.  But proving that identity
for the physical RFDE is equivalent to proving that the canonical history
already lies on the chosen exact terminal-normalized outer family; it
cannot be assumed from asymptotic matching.

Theorem 6.1 closes the value-level Gate U-OUT, not the strengthened jet
gate U-OUT\({}^+\).  The companion closure audit proves two facts that
cannot be supplied by enlarging the constants in B1--B4:

1. for every fixed logarithmic-chart power \(p\), the existing Gaussian
   endpoint estimate is \(\delta^{p-o(1)}\), which is too large to imply
   (5.2) for a fixed \(A+\chi>0\); and
2. even exact action-supercritical B3--B4 bounds need not control
   \(D_u\beta_*\).

One robust sufficient choice for the second step is the additional
differentiated residual

\[
 \|D_um_\delta(\beta_*(\delta,u),u)\|
 \leq C_s\delta^{-M_s}
 \exp\left[-\frac{A+\chi_s}{\delta^2}
              +\frac{L_s}{\delta}\right],
 \qquad \chi_s>0,
\tag{6.2}
\]

together with the declared terminal-family mixed-jet bounds.  Then exact
implicit differentiation gives

\[
 \|D_u\beta_*\|
 \leq
 \frac{\|D_um_\delta(\beta_*,u)\|}{d_\delta},
\tag{6.3}
\]

which is superalgebraically small.  We call (6.2) **B5**.  B4 and B5 are
not duplicates: B4 controls the root value, whereas B5 controls its
parameter jet.  An exact reference identity holding jointly in \(u\)
makes both residuals zero.

## 7. Proved, conditional, and open

### Proved in this note and the companion closure audit

- The canonical outgoing complete history has a unique exact causal
  continuation until reset or first middle-tube exit.
- While \(\xi-\mu<0\), recovery is an exact base coordinate, delayed
  histories lie upstream, and (2.3)--(2.8) hold.
- At a transverse reset hit, fixed-\(\delta\) parameter dependence is
  \(C^1\).
- The scalar RFDE-subclass calculation (3.3) is exact and rules out
  algebraic or merely \(e^{-c/\delta}\) mismatch control.
- The monotone scalar terminal root and the action-supercritical ratio
  implication are exact.
- A fixed-\(p\) logarithmic endpoint estimate cannot imply the fixed outer
  action scale; the scalar RFDE-subclass obstruction is exact.
- B1--B4 do not imply uniform parameter jets. Exact implicit
  differentiation gives the sharp ratio bound; B5 is one robust sufficient
  estimate for making that ratio small after the terminal-family losses.

### Conditional

- Theorem 6.1 closes Gate U-OUT if B1--B4 are established for the physical
  two-module RFDE.
- Uniform parameter derivatives additionally require differentiated Green
  identities, including \(D_uG\) whenever the base evolution or projectors
  depend on \(u\).
- Gate U-OUT\({}^+\) additionally requires uniform terminal-family mixed
  jets and a quantitative derivative-residual ratio of the needed order.
  B5 is one sufficient formulation; an exact joint identity in \(u\) makes
  the residuals vanish.

### Open model-specific lemmas

1. **U-OUT-BVP:** construct the terminal-normalized exact physical family
   on the full segment from the overlap to \(\rho_R=-1/2\), with its delay
   buffer and no tube exit.
2. **U-OUT-LEAF:** prove the exact common-leaf chart (4.2)--(4.5).  A scalar
   current-state projection is insufficient.
3. **U-OUT-SENS:** prove the one-sign lower sensitivity (5.1), together
   with the matching upper bounds and differentiated Green identity.
4. **U-OUT-RES:** prove either exact reference matching
   \(m_{\delta,u}(0)=0\), or the action-supercritical residual (5.2).
5. **U-OUT-RES-J:** prove B5, the differentiated action-supercritical
   residual (6.2), or another quantitative bound making the exact ratio
   \(\|D_um_\delta\|/d_\delta\) sufficiently small after all known
   terminal-family losses; exact joint matching is a zero-residual case.
6. **U-OUT-J (separate strengthened gate):** after the exact finite tracker
   has been constructed, prove its uniform parameter jets, moving-frame
   bounds, \(O(\delta)\) perturbation estimate, and \(O(\delta^2)\) slow
   drift required in (5.1) of
   [paper-iii-strong-unstable-history-splitting.md](paper-iii-strong-unstable-history-splitting.md).
   Gate U-OUT together with U-OUT-J is denoted U-OUT\({}^+\).

Until the first four U-OUT items are closed, the local preparation-indexed canonical
root is not a proved geometric reset-reaching canard. Even after the first
four U-OUT items are closed, the direct relative-growth graph and reset
transversality require U-OUT-J. Biological pulse outcomes remain a further
separate gate.
